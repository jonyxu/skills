# Narration via edge-tts (Microsoft Edge neural voices)

This pipeline generates all narration locally with the `edge-tts` Python
package — no external voice service, no reference audio. This replaces the
retired 10.20.30.2 voice-clone service (CosyVoice/IndextTS); old projects
keep their existing `assets/voice-clone/` audio, new projects use
`assets/voice/` + `audio_tts_meta.json`.

## Voice

Default: **`zh-CN-XiaoxiaoNeural`** — young female, warm and natural; the
house voice for the news recap show.

Alternatives (Chinese, female): `zh-CN-XiaoyiNeural` (younger, brighter,
more lively), `zh-CN-XiaohanNeural` (calm, softer), `zh-CN-XiaomengNeural`
(childlike — avoid for news register). Full catalog:
`python -m edge_tts --list-voices` (filter `zh-CN` / `zh-TW` / `en-US` as
needed).

## Run

`scripts/tts-voice.py` drives the Python API:

```
python tts-voice.py --project <root> --segments segments.json \
    [--voice zh-CN-XiaoxiaoNeural] [--rate +0%] [--outdir assets/voice]
```

Per segment it writes `<id>.mp3` + sentence-level `<id>.srt` (UTF-8),
measures duration with ffprobe, is resume-safe, and writes
`audio_tts_meta.json` `{voice, rate, segments:{id:seconds}, total_s}`.

## Measured rate mapping (XiaoxiaoNeural, same text)

| rate | duration vs +0% |
|---|---|
| +0% | ×1.0 (base 4.920s) |
| +10% | ×0.91 |
| −10% | ×1.11 |

Prefer +0% and instead trim the script text to hit the brief's length
window; rate tweaks change prosody, not just speed.

## Pitfalls

1. **Network required.** edge-tts phones home to Microsoft's endpoint on
   every call — no network means failed segments (the script retries 3×
   and reports FAILED, it never writes silent audio). Verify connectivity
   with a one-line smoke synthesis before a full batch.
2. **CLI rate flag with a leading minus.** `--rate -10%` is parsed as an
   unknown option; write `--rate=-10%`. The Python API has no such issue
   (and the script uses the API, so this only bites ad-hoc CLI callers).
3. **SRT timing is real, not estimated.** The service emits
   `SentenceBoundary` events (offset/duration in 100ns ticks, sentence text
   punctuation included) which map 1:1 to SRT entries. If a segment yields
   no boundaries (shouldn't happen), the SRT falls back to one entry
   spanning the whole measured audio — `inject-captions.py` still splits it
   by punctuation and distributes the window proportionally.
4. **UTF-8 everywhere.** The Python API passes text in-process (no
   Windows codepage mangling, unlike the old curl flow), and both SRT and
   meta files are written UTF-8. Keep it that way if you extend the script.
