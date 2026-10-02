#!/usr/bin/env python3
"""edge-tts narration generator for HyperFrames recap videos.

Usage:
  python tts-voice.py --project <hyperframes-root> --segments segments.json \
      [--voice zh-CN-XiaoxiaoNeural] [--rate +0%] [--outdir assets/voice]

segments.json: {"s01": "第一段解说词", "s02": "...", ...}

For each segment the script:
  1. streams audio from Microsoft Edge's neural TTS through the edge-tts
     Python API (UTF-8 native - no command line, no codepage pitfalls),
  2. writes <id>.mp3 plus a sentence-level <id>.srt (UTF-8; sentence
     timestamps come from the service's SentenceBoundary events, with a
     single full-segment entry as fallback),
  3. measures the real duration with ffprobe (renders must be timed from
     measured audio, never estimates),
  4. is resumable: segments whose mp3 already exists are skipped.

Outputs: <outdir>/<id>.mp3 + <id>.srt per segment, and writes
audio_tts_meta.json {voice, rate, segments:{id:seconds}, total_s} into
--project.

Note: edge-tts requires network access to Microsoft's endpoint. A failed
segment raises after 3 attempts instead of emitting silent audio.
"""
import argparse, asyncio, json, os, subprocess

import edge_tts

def ffprobe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return None

def fmt_ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def build_srt(boundaries, text, total_s):
    """SentenceBoundary events carry sentence-level timestamps directly.

    edge-tts reports offset/duration in 100ns ticks (÷10_000_000 -> s).
    If no boundaries arrive, fall back to one entry over the measured audio.
    """
    entries = [(b["offset"] / 10000000.0,
                (b["offset"] + b["duration"]) / 10000000.0,
                b["text"]) for b in boundaries]
    if not entries:
        entries = [(0.0, total_s, text)]
    return "".join(
        f"{i+1}\n{fmt_ts(a)} --> {fmt_ts(b)}\n{t}\n\n"
        for i, (a, b, t) in enumerate(entries))

async def synth(text, voice, rate, mp3_path, srt_path):
    comm = edge_tts.Communicate(text, voice, rate=rate)
    audio, boundaries = bytearray(), []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            boundaries.append(chunk)
    with open(mp3_path, "wb") as fh:
        fh.write(bytes(audio))
    dur = ffprobe_duration(mp3_path) or 0.0
    with open(srt_path, "w", encoding="utf-8") as fh:
        fh.write(build_srt(boundaries, text, dur))
    return dur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--segments", required=True, help="JSON {id: text}")
    ap.add_argument("--voice", default="zh-CN-XiaoxiaoNeural",
                    help="edge-tts voice name (default: young female Xiaoxiao)")
    ap.add_argument("--rate", default="+0%",
                    help="e.g. +10% or -10% (CLI callers: use --rate=-10% form)")
    ap.add_argument("--outdir", default="assets/voice")
    a = ap.parse_args()

    # utf-8-sig: tolerates the BOM that Windows PowerShell's Out-File adds
    segments = json.load(open(a.segments, encoding="utf-8-sig"))
    out = os.path.join(a.project, a.outdir)
    os.makedirs(out, exist_ok=True)

    async def run():
        results = {}
        for sid, text in segments.items():
            mp3 = os.path.join(out, f"{sid}.mp3")
            dur = ffprobe_duration(mp3) if os.path.exists(mp3) and os.path.getsize(mp3) > 0 else None
            if dur:
                print(f"{sid}: exists ({dur}s), skip")
                results[sid] = dur
                continue
            for attempt in range(3):
                try:
                    dur = await synth(text, a.voice, a.rate, mp3,
                                      os.path.join(out, f"{sid}.srt"))
                    if dur:
                        print(f"{sid}: ok, {dur}s")
                        results[sid] = dur
                        break
                except Exception as e:
                    print(f"{sid}: attempt {attempt+1} failed: {e}")
            if results.get(sid) is None:
                print(f"{sid}: FAILED")
                results[sid] = None
        return results

    results = asyncio.run(run())
    total = sum(d for d in results.values() if d)
    meta = {"voice": a.voice, "rate": a.rate,
            "segments": results, "total_s": round(total, 2)}
    with open(os.path.join(a.project, "audio_tts_meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(f"TOTAL {total:.2f}s -> audio_tts_meta.json")

if __name__ == "__main__":
    main()
