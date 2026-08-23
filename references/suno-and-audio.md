# Music and audio mix

## Music brief

Write `audio/music-brief.md` with thesis, emotional arc, target duration, tempo range, rhythmic density, instrumentation, texture, harmonic movement, opening behavior, central turn, ending behavior, and exclusions.

Example shape:

```text
Instrumental cinematic editorial score. [emotional arc].
[tempo and pulse]. [instruments and material texture].
Begin [opening behavior], develop toward [central turn], end [ending behavior].
Restrained and spatial beneath [language] narration.
Avoid [vocals, oversized drums, trailer clichés, or project-specific exclusions].
```

Generate at least two candidates when the service and account are available. Compare full musical arcs at the opening, central turn, densest narration passage, and ending. Do not choose from the first seconds alone.

If Suno is used, operate through the user's signed-in browser session and record title, prompt, source, duration, and chosen file in `audio/music-manifest.json`. Do not require Suno when the user supplies music or prefers another route.

## Mix behavior

- Establish the music before or after the first word according to the opening design.
- Duck before speech begins and release after it ends.
- Merge neighboring duck windows so music does not pump between close sentences.
- Preserve authentic source audio as a distinct editorial layer.
- Use sound bridges to connect shots when visually motivated.
- Let the final fade fit the ending rather than applying one universal duration.
- Check intelligibility on ordinary speakers at normal volume.

Typical starting values, to be tuned by ear:

- music beneath narration: 18–25% of its full level;
- ducked music: 4–8%;
- duck lead: 0.4–0.6 seconds;
- release: about 0.7–1.1 seconds.

Measure loudness and peaks when tools are available. Avoid clipping and large level jumps between synthetic narration and authentic clips.
