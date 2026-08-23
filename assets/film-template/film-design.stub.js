/* UNAUTHORED FILM DESIGN — replace this file after storyboard approval. */

export async function createFilmDesign(runtime) {
  const { renderer, world, camera, ctx, webgl, width, height } = runtime;
  renderer.setClearColor(0x000000, 1);

  function renderAt() {
    renderer.render(world, camera);
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);
    ctx.drawImage(webgl, 0, 0, width, height);
    ctx.fillStyle = 'rgba(255,255,255,.72)';
    ctx.font = '500 18px system-ui,sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('UNAUTHORED FILM DESIGN', 36, 48);
  }

  return { renderAt };
}
