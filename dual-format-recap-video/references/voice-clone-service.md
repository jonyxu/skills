# Voice-clone service (10.20.30.2:8080) — contract and pitfalls

Zero-shot voice cloning: a 3–15s reference voice + any text → MP3 + SRT, no
fine-tuning. Base `$BASE = http://10.20.30.2:8080`.

## Engines and refs

- `GET $BASE/api/engines` — `{"engines":[{"id":"cosyvoice","ok":true,...},{"id":"indextts",...}]}`;
  only call engines with `ok:true`. Default `cosyvoice` (stable, in-process).
- `GET $BASE/api/refs` — available reference voices. The production ref is
  **`liuzw`** (16kHz reference audio; its `prompt_text` is a transcript).
  Never touch other users' refs (e.g. `wusy`).
- `GET $BASE/api/synth_progress` — `{"active":..,"total":..,"done":..}` while
  a job runs.

## Synthesize

```
POST $BASE/api/synth   Content-Type: application/json
{"text":"...", "ref":"liuzw", "out":"vc_s01", "engine":"cosyvoice", "speed":1.0}
→ {"ok":true,"name":"vc_s01","duration":3.72,"mp3":"/audio/vc_s01.mp3",
   "srt":"/audio/vc_s01.srt","segments":1}
GET $BASE/audio/vc_s01.mp3 | .srt
```

- `speed` ×0.5–×2.0 (native engine resample, not post-stretch). Measured on
  this service: 0.9 ≈ ×1.2 duration vs 1.0; 1.1 ≈ ×0.95.
- The service splits long text into multiple SRT entries itself — use those
  real timestamps for captions; do not re-estimate.
- `out` is normalized server-side; server-side synthesis has no HTTP timeout —
  client-side allow 30+ min for long text, or poll progress.

## The two hard pitfalls

1. **Flaky windows.** The port accepts connections in bursts and refuses
   (RST after ~2.3s) for minutes at a time. Ping stays up the whole time, so
   "host reachable" proves nothing. **Always wrap every request in a retry
   loop (≥30 attempts, 2s sleep)** and do POST + both downloads back-to-back
   inside the same window. `scripts/clone-voice.py` implements this.
2. **Chinese must travel as a file.** Passing Chinese text in the curl command
   line from git-bash on a Chinese Windows reaches curl.exe mangled through
   the system codepage → server answers `{"detail":"There was an error
   parsing the body"}`. Write the JSON with Python (`ensure_ascii=False`,
   UTF-8) and send `curl --data-binary @payload.json`. Pure-ASCII bodies work
   from the command line, which is how this pitfall hides during smoke tests.

## Etiquette

- One job per engine at a time (jobs queue; serial).
- No built-in auth — don't expose the port publicly.
