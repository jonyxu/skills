# Deterministic Chinese typography (font subsetting)

Video renders are offline and frame-reproducible; an unbundled display font
either triggers `font_family_without_font_face` lint or fails closed in cloud
renders. The bundled set has no Simplified-Chinese family.

Recipe that worked (Noto Sans SC, weights 400/700/900):

1. After authoring the composition HTML, collect the unique characters of
   every file (Python: read all html, `set()` the text).
2. For each weight, request a subset font from Google Fonts:
   `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@<W>&text=<urlencoded chars>&display=swap`
   with a browser User-Agent. The CSS contains ONE woff2 URL — the URL has
   no `.woff2` suffix (it is a `l/font?kit=` form), so match `url\((https://[^)]+)\)`,
   not a `.woff2` regex.
3. Download to `assets/fonts/noto-sans-sc-<W>.woff2` (~55KB per weight for
   ~420 glyphs) and declare three `@font-face` blocks with `font-display: block`.

The subset covers exactly the authored text, so preview and render agree and
no build-time network fetch happens.

Pairing rule: Noto Sans SC carries statements (900 headlines / 400 body);
JetBrains Mono (bundled) carries data, dates, prices, and labels with
`font-variant-numeric: tabular-nums`. Two roles, two voices — not two sans.
