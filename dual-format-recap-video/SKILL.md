---
name: dual-format-recap-video
description: Use when turning an article, newsletter, or news roundup of any cadence (daily, weekly, or a special edition) into a narrated explainer video and BOTH a landscape 16:9 cut and a vertical 9:16 cut are wanted; also when re-voicing any HyperFrames video with edge-tts neural voices (default zh-CN-XiaoxiaoNeural, young female), when captions must be driven by the generated SRT files, or when the first frame of a video must read as a clear poster.
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
voice / **cadence + content date range: derive the covered period from the
task prompt AND what the sources actually cover — it may be 单日, 本周,
双周, 月, or a 专题; never assume a fixed cadence**) as the first action.
The derived cadence fixes the show label (e.g. 今日/每日 for one day,
本周/周报 for a week, 专题 for an event); the intro title, kicker, narration
opener, and outro keywords line all derive from it — they must never be
copied from a previous episode. **Done when:** `npx hyperframes check` runs
clean on the scaffold and the brief's cadence + date range match both the
task prompt and the sources' actual coverage.

### 2. Collect the article's own images
Ingest every screenshot with `npx hyperframes media-use resolve --type image
--from "<public URL>" --project .`. They land in `.media/images/` and the
composition references **`.media/images/...`, not `assets/images/...`** —
referencing `assets/` fails lint `missing_local_asset`. **Done when:** every
planned scene has an image whose `.media/index.md` entry exists.

### 3. Generate narration with edge-tts
Author per-segment narration (one speaking beat per segment, targeted at the
duration the brief needs; the opener and closing lines use the brief's
derived cadence label), then run `scripts/tts-voice.py` (default voice
`zh-CN-XiaoxiaoNeural` — young female; see `references/edge-tts.md` for the
voice catalog, the measured rate mapping, and the network pitfall). Each
segment yields an MP3 plus a sentence-level UTF-8 SRT with real timestamps
from the service's sentence boundaries. **Done when:** every segment has a
measured `dur` in `audio_tts_meta.json` (resume-safe), and the sum plus
planned gaps lands inside the requested length window.

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
| Rate → duration | +10% ≈ ×0.91, −10% ≈ ×1.11 vs +0% (measured); prefer trimming the script text over rate tweaks |
| Cadence label | Derived from the task prompt + the content's actual date range (单日/本周/双周/专题…); label must match it, checked before render |
| Caption band | Bottom band above the metabar; all scene content ends higher |
| Image paths | `.media/images/...` (never `assets/images/...`) |
| Audio track | 10; captions 5; visuals 1 |
| TTS text & SRT | Python API (UTF-8 in-process); SRT/meta files always written UTF-8 |

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
- **Assuming TTS works offline** — edge-tts calls Microsoft's endpoint on
  every synthesis; smoke-test one line before a full batch. A failed
  segment is reported FAILED after 3 attempts, never silent audio.
- **Inheriting the previous episode's label** — the show label (intro title,
  kicker, chips, narration opener, outro keywords line) must be re-derived
  from the brief's cadence every episode; the cadence comes from the task
  prompt + the content's actual date range, never a daily/weekly assumption.
  Before rendering, grep `index.html`, `compositions/`, and the narration
  SRTs for period words (今/昨/本/周/双周/月/专题…) and check each hit
  against the brief's cadence.
