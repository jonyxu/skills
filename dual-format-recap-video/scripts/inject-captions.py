#!/usr/bin/env python3
"""SRT-driven caption track injector for a HyperFrames index.html.

Usage:
  python inject-captions.py --project <hyperframes-root> \
      [--voice-dir assets/voice-clone] [--track 5] [--units-h 36] [--units-v 20]

Reads <voice-dir>/<id>.srt per narration segment, maps each segment's SRT
window to absolute composition time via the matching <audio id="vo-<id>"
data-start="..."> in index.html, splits entries at punctuation into
single-line captions (width budget auto-picked from the root data-width:
larger budget for 1920-wide landscape, smaller for 1080-wide vertical),
and injects:
  - a caption CSS block before </style>
  - one <div class="clip cap" data-start data-duration data-track-index>
    per caption before the root's </div>
Idempotent: previously injected blocks are stripped first.

Caption band rule: captions sit in a reserved band above the metabar; scene
content must end above that band or check reports content_overlap.
"""
import argparse, html, os, re

def units(s):
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s)

def split_text(text, max_units):
    parts = [p for p in re.split(r"(?<=[,。;:!?、])", text) if p.strip()]
    out, cur = [], ""
    for p in parts:
        if units(cur) + units(p) <= max_units:
            cur += p
        else:
            if cur:
                out.append(cur)
            while units(p) > max_units:
                acc = ""
                for ch in p:
                    if units(acc + ch) > max_units:
                        break
                    acc += ch
                out.append(acc)
                p = p[len(acc):]
            cur = p
    if cur:
        out.append(cur)
    return out

def parse_srt(path):
    txt = open(path, encoding="utf-8").read()
    entries = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000
        end = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000
        entries.append((start, end, " ".join(lines[2:])))
    return entries

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice-dir", default="assets/voice-clone")
    ap.add_argument("--track", type=int, default=5)
    ap.add_argument("--units-h", type=float, default=36)
    ap.add_argument("--units-v", type=float, default=20)
    a = ap.parse_args()

    idx = os.path.join(a.project, "index.html")
    txt = open(idx, encoding="utf-8").read()
    starts = {m.group(1): float(m.group(2)) for m in
              re.finditer(r'id="vo-(s\d+)"[^>]*data-start="([\d.]+)"', txt)}
    w = re.search(r'data-width="(\d+)"', txt)
    width = int(w.group(1)) if w else 1920
    max_units = a.units_h if width >= 1920 else a.units_v
    font = 34 if width >= 1920 else 39
    bottom = 130 if width >= 1920 else 152
    label = "横版" if width >= 1920 else "竖版"

    clips, n = [], 0
    for sid in sorted(starts, key=lambda s: int(s[1:])):
        srt = os.path.join(a.project, a.voice_dir, f"{sid}.srt")
        if not os.path.exists(srt):
            print(f"!! missing {srt}")
            continue
        for (t0, t1, text) in parse_srt(srt):
            total = units(text)
            t = t0
            for sub in split_text(text, max_units):
                n += 1
                dur = (t1 - t0) * units(sub) / total
                clips.append(
                    f'      <div class="clip cap" id="cap-{sid}-{n}" '
                    f'data-start="{round(starts[sid] + t, 3)}" data-duration="{round(dur, 3)}" '
                    f'data-track-index="{a.track}"><span class="cap-t">{html.escape(sub)}</span></div>')
                t += dur
    if not clips:
        print("no captions produced")
        return

    css = f"""
      /* CAPTIONS-CSS:BEGIN({label} {width}px:单行字幕带,位于 metabar 上方) */
      .cap {{
        position: absolute;
        left: 50%;
        bottom: {bottom}px;
        transform: translateX(-50%);
        max-width: {'80' if width >= 1920 else '92'}%;
        display: flex;
        justify-content: center;
        pointer-events: none;
        z-index: 20;
      }}
      .cap .cap-t {{
        display: inline-block;
        background: rgba(20, 17, 12, 0.88);
        border: 2px solid rgba(240, 168, 48, 0.55);
        border-radius: 14px;
        padding: 12px 30px;
        font-family: "Noto Sans SC", sans-serif;
        font-weight: 700;
        font-size: {font}px;
        line-height: 1.35;
        color: #f4ead8;
        text-align: center;
        white-space: nowrap;
      }}
      /* CAPTIONS-CSS:END */
"""
    txt = re.sub(r"\n?      <!-- CAPTIONS:BEGIN -->.*?<!-- CAPTIONS:END -->", "", txt, flags=re.S)
    txt = re.sub(r"\n?      /\* CAPTIONS-CSS:BEGIN.*?CAPTIONS-CSS:END \*/", "", txt, flags=re.S)
    txt = txt.replace("    </style>", css + "    </style>", 1)
    block = "      <!-- CAPTIONS:BEGIN -->\n" + "\n".join(clips) + "\n      <!-- CAPTIONS:END -->"
    marker = "    </div>\n\n    <script>"
    if marker not in txt:
        print("!! injection marker not found (expected root </div> before <script>)")
        return
    txt = txt.replace(marker, block + "\n" + marker, 1)
    open(idx, "w", encoding="utf-8").write(txt)
    print(f"{os.path.basename(a.project)} ({label}, {width}px): injected {len(clips)} captions")

if __name__ == "__main__":
    main()
