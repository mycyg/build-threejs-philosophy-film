# Research, source media, and asset provenance

## Evidence ledger

Assign every material claim an evidence ID. Record the exact locator: page, paragraph, timestamp, commit, UI route, or URL. Distinguish:

- verified quotation;
- faithful paraphrase;
- interpretation;
- visual metaphor;
- reconstruction;
- generated scene.

Never let a generated image masquerade as archival evidence. Label reconstructions when the film's context could mislead a reasonable viewer.

## Source priority

Prefer, in order:

1. supplied originals and first-party publications;
2. primary interviews, talks, filings, papers, product pages, and archives;
3. reputable secondary reporting;
4. commentary useful for context, never as sole support for a strong factual claim.

Record download date, creator or publisher, license or fair-use rationale, original URL, and any transformation.

## Authentic clip verification

For every interview or speech clip:

1. retain the original source URL and full source title;
2. identify the speaker visually and from source metadata;
3. extract the candidate range with original audio;
4. transcribe that exact range locally;
5. compare the transcript to the intended quotation or paraphrase;
6. verify language, topic, and in/out points;
7. record the result in `assets/source-verification.json`;
8. reject the clip when speaker, words, or context cannot be confirmed.

Use `verify_source_clip.py` after the full source file is present locally. The script extracts a precise range, retains original sound, runs local ASR, compares expected wording when supplied, and writes both the verification ledger and asset ledger. The `--speaker-confirmed` and `--context-confirmed` flags represent checks the Agent actually performed; never set them optimistically.

Do not validate a clip from lip movement. Do not place translated or synthetic speech under a real person's face without clear editorial disclosure and user approval.

## Asset roles

Plan assets by edit function:

- primary evidence;
- primary generated scene;
- alternate composition;
- continuity bridge;
- texture or atmosphere;
- macro detail;
- transition material;
- recovery insert for shortening or replacing a weak hold;
- cover or promotional crop.

Every important shot needs a viable replacement. Every long shot needs enough internal material to evolve.

## Asset-surplus policy

Start near three times the number of visuals expected in the final cut. As planning guidance:

- ordinary designed shot: 4–6 candidates;
- hero image, recurring character, or major turn: 8–12 candidates;
- source document: full page, exact crop, contextual crop, and one detail treatment;
- transition: 2–4 details or states;
- recurring motif: at least emergence, recognition, transformation, convergence, and detail states.

These are planning defaults, not quotas. Raise counts for identity continuity or a difficult visual metaphor. Lower them only when the user chooses an economy mode or the source itself is the visual.

## Codex image generation

Use the built-in `image_gen` tool by default. One distinct asset or variant equals one call. Do not use an `n` parameter as a substitute for separately authored prompts. Use the CLI/API fallback only when the user explicitly requests it and accepts the API-key requirement.

For every project-bound result:

1. inspect subject, composition, continuity, text, and avoid constraints;
2. move or copy it from Codex's generated-image location into `assets/generated/`;
3. give it a stable asset ID;
4. write the final prompt, generation route, role, and shot IDs to the ledger;
5. preserve variants non-destructively;
6. mark selected, alternate, candidate, or rejected after review.

Prompt each family from a shared continuity block plus a shot-specific delta. Keep identity, era, lens, aspect ratio, light direction, palette, grain, and material stable unless the storyboard calls for a change.
