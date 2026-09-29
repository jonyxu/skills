#!/usr/bin/env python3
"""Voice-clone narration recorder for the 10.20.30.2 cloning service.

Usage:
  python clone-voice.py --project <hyperframes-root> --segments segments.json \
      [--ref liuzw] [--speed 1.0] [--outdir assets/voice-clone] \
      [--base http://10.20.30.2:8080]

segments.json: {"s01": "第一段解说词", "s02": "...", ...}

For each segment the script:
  1. writes the POST payload to a UTF-8 file (NEVER pass Chinese on the
     command line - the Windows codepage mangles it and the server answers
     "There was an error parsing the body"),
  2. POSTs /api/synth with retries (the service port opens in flaky windows;
     a plain refusal is retried, not fatal),
  3. downloads <name>.mp3 + <name>.srt,
  4. measures the real duration with ffprobe (renders must be timed from
     measured audio, never estimates),
  5. is resumable: segments whose mp3 already exists are skipped.

Outputs: <outdir>/sNN.mp3 + sNN.srt per segment, and writes
audio_clone_meta.json {segments:{id:seconds}, total_s} into --project.
"""
import argparse, json, os, subprocess, sys, time

def curl(args, timeout=240):
    return subprocess.run(
        ["curl.exe", "-s", "--noproxy", "*", "--max-time", str(timeout)] + args,
        capture_output=True, timeout=timeout + 10)

def ffprobe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--segments", required=True, help="JSON {id: text}")
    ap.add_argument("--ref", default="liuzw")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--outdir", default="assets/voice-clone")
    ap.add_argument("--base", default="http://10.20.30.2:8080")
    ap.add_argument("--engine", default="cosyvoice")
    ap.add_argument("--tmp", default=os.environ.get("TEMP", "/tmp") + "/clone-voice")
    ap.add_argument("--tries", type=int, default=30)
    a = ap.parse_args()

    segments = json.load(open(a.segments, encoding="utf-8"))
    out = os.path.join(a.project, a.outdir)
    os.makedirs(out, exist_ok=True)
    os.makedirs(a.tmp, exist_ok=True)

    results = {}
    for sid, text in segments.items():
        mp3 = os.path.join(out, f"{sid}.mp3")
        srt = os.path.join(out, f"{sid}.srt")
        dur = ffprobe_duration(mp3) if os.path.exists(mp3) and os.path.getsize(mp3) > 0 else None
        if dur:
            print(f"{sid}: exists ({dur}s), skip")
            results[sid] = dur
            continue

        payload = os.path.join(a.tmp, f"{sid}.json")
        with open(payload, "w", encoding="utf-8") as fh:
            json.dump({"text": text, "ref": a.ref, "out": f"vc_{sid}",
                       "engine": a.engine, "speed": a.speed}, fh, ensure_ascii=False)

        landed = False
        for attempt in range(a.tries):
            r = curl(["-X", "POST", f"{a.base}/api/synth",
                      "-H", "Content-Type: application/json",
                      "--data-binary", f"@{payload}"])
            body = r.stdout.decode("utf-8", "replace")
            if '"ok":true' in body:
                landed = True
                break
            print(f"{sid}: attempt {attempt+1} -> {body.strip()[:80]}")
            time.sleep(2)
        if not landed:
            print(f"{sid}: FAILED after {a.tries} attempts")
            results[sid] = None
            continue

        for _ in range(15):
            curl(["-o", mp3, f"{a.base}/audio/vc_{sid}.mp3"], timeout=60)
            if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
                break
            time.sleep(1)
        for _ in range(15):
            curl(["-o", srt, f"{a.base}/audio/vc_{sid}.srt"], timeout=60)
            if os.path.exists(srt) and os.path.getsize(srt) > 0:
                break
            time.sleep(1)
        dur = ffprobe_duration(mp3)
        results[sid] = dur
        print(f"{sid}: ok, {dur}s")

    total = sum(d for d in results.values() if d)
    meta = {"ref": a.ref, "speed": a.speed, "segments": results, "total_s": round(total, 2)}
    with open(os.path.join(a.project, "audio_clone_meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(f"TOTAL {total:.2f}s -> audio_clone_meta.json")

if __name__ == "__main__":
    main()
