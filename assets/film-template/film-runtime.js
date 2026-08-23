import * as THREE from './node_modules/three/build/three.module.js';
import { Muxer, ArrayBufferTarget } from './node_modules/mp4-muxer/build/mp4-muxer.mjs';


export async function bootFilmRuntime(createFilmDesign) {
  const plan = await fetch('./film-plan.json').then((response) => {
    if (!response.ok) throw new Error(`film-plan.json: ${response.status}`);
    return response.json();
  });
  const W = plan.meta.width;
  const H = plan.meta.height;
  const FPS = plan.meta.fps;
  const DURATION = plan.meta.duration;
  const TRANSITION = plan.design.transition_seconds ?? 2.25;
  const film = document.querySelector('#film');
  const webgl = document.querySelector('#webgl');
  const ctx = film.getContext('2d', { alpha: false });
  const timeInput = document.querySelector('#time');
  const readout = document.querySelector('#readout');
  const status = document.querySelector('#status');
  const renderButton = document.querySelector('#renderButton');
  const download = document.querySelector('#download');
  film.width = webgl.width = W;
  film.height = webgl.height = H;
  timeInput.max = DURATION;
  download.download = `${plan.meta.slug}-silent.mp4`;

  const clamp = (value, min = 0, max = 1) => Math.max(min, Math.min(max, value));
  const mix = (a, b, t) => a + (b - a) * t;
  const smooth = (t) => { t = clamp(t); return t * t * (3 - 2 * t); };
  const smoother = (t) => { t = clamp(t); return t * t * t * (t * (t * 6 - 15) + 10); };
  const out = (t) => 1 - Math.pow(1 - clamp(t), 4);
  const fmt = (seconds) => {
    const value = Math.max(0, Math.floor(seconds));
    return `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
  };
  const sceneAlpha = (def, time, transition = TRANSITION) => {
    const fadeIn = def.start === 0 ? 1 : smoother((time - (def.start - transition)) / (transition * 2));
    const fadeOut = def.end === DURATION ? 1 : smoother(((def.end + transition) - time) / (transition * 2));
    return clamp(Math.min(fadeIn, fadeOut));
  };
  const boundaryMotion = (time, span = TRANSITION * 1.45) => {
    let state = { intensity: 0, phase: 0, boundaryIndex: -1 };
    for (let index = 1; index < plan.scenes.length; index++) {
      const local = (time - (plan.scenes[index].start - span)) / (span * 2);
      if (local < 0 || local > 1) continue;
      const intensity = Math.pow(Math.sin(local * Math.PI), 1.25);
      if (intensity > state.intensity) state = { intensity, phase: local, boundaryIndex: index };
    }
    return state;
  };
  const activeNarration = (time) => {
    const items = plan.narration ?? [];
    for (let index = 0; index < items.length; index++) {
      const item = items[index];
      const next = items[index + 1];
      const end = item.start + (item.duration ?? Math.min(10, (next?.start ?? DURATION) - item.start - .2));
      if (time >= item.start && time <= end) {
        return { item, progress: clamp((time - item.start) / Math.max(.1, end - item.start)) };
      }
    }
    return null;
  };

  const renderer = new THREE.WebGLRenderer({
    canvas: webgl,
    alpha: true,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const world = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, W / H, .1, 200);
  camera.position.set(0, 0, 10);
  const helpers = { clamp, mix, smooth, smoother, out, fmt, sceneAlpha, boundaryMotion, activeNarration };
  const design = await createFilmDesign({
    THREE,
    plan,
    renderer,
    world,
    camera,
    film,
    webgl,
    ctx,
    width: W,
    height: H,
    fps: FPS,
    duration: DURATION,
    transition: TRANSITION,
    helpers,
  });
  if (!design || typeof design.renderAt !== 'function') {
    throw new Error('film-design.js must return { renderAt(time) }');
  }

  function renderAt(time) {
    const safeTime = clamp(Number(time), 0, DURATION);
    design.renderAt(safeTime);
    timeInput.value = safeTime;
    readout.textContent = `${fmt(safeTime)} / ${fmt(DURATION)}`;
  }

  timeInput.addEventListener('input', () => renderAt(timeInput.value));

  async function encodeFilm() {
    document.body.classList.add('rendering');
    renderButton.disabled = true;
    download.hidden = true;
    const target = new ArrayBufferTarget();
    const muxer = new Muxer({
      target,
      video: { codec: 'avc', width: W, height: H },
      fastStart: 'in-memory',
      firstTimestampBehavior: 'offset',
    });
    let encoderError = null;
    const encoder = new VideoEncoder({
      output: (chunk, meta) => muxer.addVideoChunk(chunk, meta),
      error: (error) => { encoderError = error; },
    });
    const config = {
      codec: 'avc1.640028',
      width: W,
      height: H,
      bitrate: 6_400_000,
      framerate: FPS,
      hardwareAcceleration: 'prefer-hardware',
      latencyMode: 'quality',
      avc: { format: 'avc' },
    };
    const support = await VideoEncoder.isConfigSupported(config);
    if (!support.supported) throw new Error('H.264 configuration unavailable');
    encoder.configure(config);
    const requested = Number(new URLSearchParams(location.search).get('duration') || DURATION);
    const encodeDuration = clamp(requested, 1, DURATION);
    const totalFrames = Math.round(encodeDuration * FPS);
    const frameDuration = Math.round(1_000_000 / FPS);
    const started = performance.now();
    for (let frame = 0; frame < totalFrames; frame++) {
      const time = frame / FPS;
      renderAt(time);
      const videoFrame = new VideoFrame(film, {
        timestamp: Math.round(frame * 1_000_000 / FPS),
        duration: frameDuration,
      });
      encoder.encode(videoFrame, { keyFrame: frame % (FPS * 2) === 0 });
      videoFrame.close();
      if (frame % 96 === 95) {
        await encoder.flush();
        if (encoderError) throw encoderError;
        const elapsed = (performance.now() - started) / 1000;
        const progress = (frame + 1) / totalFrames;
        status.textContent = `渲染 ${Math.round(progress * 100)}% · 约剩 ${fmt(elapsed / progress - elapsed)}`;
        await new Promise((resolve) => setTimeout(resolve, 0));
      }
    }
    await encoder.flush();
    if (encoderError) throw encoderError;
    encoder.close();
    muxer.finalize();
    const blob = new Blob([target.buffer], { type: 'video/mp4' });
    if (download.href) URL.revokeObjectURL(download.href);
    download.href = URL.createObjectURL(blob);
    download.hidden = false;
    status.textContent = `无声母片完成 · ${(blob.size / 1024 / 1024).toFixed(1)} MB`;
    document.body.classList.remove('rendering');
    renderButton.disabled = false;
    window.__FILM_RENDERED__ = true;
    window.__FILM_BYTES__ = blob.size;
  }

  renderButton.addEventListener('click', async () => {
    try {
      await encodeFilm();
    } catch (error) {
      console.error(error);
      status.textContent = `渲染失败：${error.message}`;
      document.body.classList.remove('rendering');
      renderButton.disabled = false;
    }
  });

  await document.fonts.ready;
  const query = new URLSearchParams(location.search);
  if (query.get('clean') === '1') document.body.classList.add('clean');
  renderAt(Number(query.get('t') || 0));
  status.textContent = '影片运行时已就绪';
  window.__FILM_RUNTIME__ = { plan, renderAt, design };
}
