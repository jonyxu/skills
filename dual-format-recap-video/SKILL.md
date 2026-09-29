---
name: dual-format-recap-video
description: Use when turning an article, newsletter, or weekly news roundup into a narrated explainer video and BOTH a landscape 16:9 cut and a vertical 9:16 cut are wanted; also when re-voicing any HyperFrames video with the 10.20.30.2 voice-clone service (reference voice liuzw), when captions must be driven by the returned SRT files, or when the first frame of a video must read as a clear poster.
---

# Dual-Format Recap Video

Produce a 3–5 minute narrated news-recap video in **both 16:9 and 9:16 from one
audio timeline**. Core principle: **measured audio drives the edit** — every
scene duration, beat, and image swap is anchored to ffprobe-measured voice
segment lengths, never estimates; the vertical cut is a CSS-only re-layout of
the same GSAP timeline.

Route fresh creation through `/hyperframes` first. If the piece is longer than
~3 minutes, `faceless-explainer`'s hard cap is exceeded — route to
`general-video` (multi-scene montage). `flow: automation, storyboard: no` is
the right shape for a one-shot delivery.

## Pipeline

### 1. Scaffold and brief
`npx hyperframes init "videos/<name>" --non-interactive --example=blank --skill=general-video`,
then write `BRIEF.md` (message / aspect 1920x1080 / language zh / length /
voice) as the first action. **Done when:** `npx hyperframes check` runs clean
on the scaffold.

### 2. Collect the article's own images
Ingest every screenshot with `npx hyperframes media-use resolve --type image
--from "<public URL>" --project .`. They land in `.media/images/` and the
composition references **`.media/images/...`, not `assets/images/...`** —
referencing `assets/` fails lint `missing_local_asset`. **Done when:** every
planned scene has an image whose `.media/index.md` entry exists.

### 3. Record narration with the clone service
Author per-segment narration (one speaking beat per segment, targeted at the
duration the brief needs), then run `scripts/clone-voice.py` (see
`references/voice-clone-service.md` for the service contract and its two hard
pitfalls: flaky port windows, and Chinese text that must travel in a UTF-8
file, never on the command line). **Done when:** every segment has a measured
`dur` in `audio_clone_meta.json` (resume-safe), and the sum plus planned gaps
lands inside the requested length window.

### 4. Lay out the timeline from measured durations
Compute: segment starts (gap ~0.6s) → scene slots (gap ~1.5s) → root
`data-duration`. Mount one `<audio id="vo-sNN" data-start data-duration>` per
segment on track 10, with `data-duration` set to the **measured** value
(rounded-up slots trip `clip_media_fit` warnings). Then re-anchor every scene
beat to its segment's local start. **Done when:** sum(slots) == root duration
and each scene's script cites the segment it answers.

### 5. Author the scenes
One sub-composition per scene at `compositions/sN-*.html` (template-wrapped,
`data-composition-id` matching the host slot, element ids scene-prefixed).
News register: dark warm-ink canvas + one amber accent, Noto Sans SC via a
**locally subset @font-face** (`references/chinese-typography.md` has the
Google Fonts `text=` recipe) + JetBrains Mono for data labels with
`tabular-nums`. Motion: `spring-pop-entrance` (power3.out, no overshoot),
`scale-swap-transition` for image swaps, short ken-burns pushes on images,
`sine-wave-loop` ambient breathing. **Done when:** `check` reports 0 errors.

### 6. Fork the vertical cut
New project, same skill; copy `.media/`, `assets/fonts/`, and the voice dir;
rewrite index (root `data-width="1080" data-height="1920"`, **same audio
data-start/data-duration values**) and each scene's CSS for a vertical stack
(headline → chips → full-width image → chips). Keep every GSAP beat time
identical. **Done when:** vertical `check` reports 0 errors.

### 7. Captions + first-frame poster
Run `scripts/inject-captions.py --project .` in each project (auto-picks the
width budget: 36 units for 1920, 20 for 1080). In the intro scene make t=0 a
**complete poster**: kicker, headline, sub, chips, and metabar all at final
state at t=0 (no entrance tweens on them); let ambient glow start at 0.55
opacity and replace entrance pops with a late emphasis pulse. Scene content
must end above the caption band or `check` reports `content_overlap`.
**Done when:** extracting frame 0 from the render shows a complete, readable
cover, and a caption-bearing frame shows the pill clear of scene content.

### 8. Render and verify
`npx hyperframes render -q delivery` per project; verify with ffprobe
(width/height/duration/dual streams), extract spot frames with
`ffmpeg -ss <t> -i out.mp4 -frames:v 1`, delete superseded renders.
**Done when:** both MP4s match their aspect and the intended duration, and
frame 0 plus one mid-caption frame are visually confirmed.

## Quick reference

| Concern | Rule |
|---|---|
| Speed → duration | 0.9 ≈ ×1.2, 1.0 = ×1.0, 1.1 ≈ ×0.95 relative to measured 1.0 audio |
| Caption band | Bottom band above the metabar; all scene content ends higher |
| Image paths | `.media/images/...` (never `assets/images/...`) |
| Audio track | 10; captions 5; visuals 1 |
| Chinese POST bodies | Always `--data-binary @utf8-file` |

## Common mistakes

- **Flattening HTML to one line before stripping `<script>`** — greedy `.*`
  eats the whole body. Strip non-greedily (`[^<]` character classes) or keep
  line-based sed.
- **Ken-burns `fromTo` without `immediateRender: false`** — the later
  fromTo's from-state becomes the resting state for early seeks
  (`gsap_repeated_fromto_without_baseline`).
- **Overlapping tweens on one target** (entrance vs push): start the second
  after the first ends, or lint flags `overlapping_gsap_tweens`.
- **Decorative bleed** — mark intentional ghost/glow overflow with
  `data-layout-allow-overflow`; decoratives that captions cover with
  `data-layout-allow-occlusion`.
- **Treating leaks as fact** — keep "泄露/据悉" wording in both narration and
  on-screen cards for unreleased items.
