#!/usr/bin/env bash
# Regenerate all README images from the KiCad PCB file.
#
# Outputs (in images/):
#   pcb-3d-top.png          isometric 3D render
#   pcb-3d-flat-top.png     orthographic top 3D render
#   pcb-3d-flat-bottom.png  orthographic bottom 3D render
#   pcb-layout-top.svg      F.Cu + F.Silkscreen + F.Mask + Edge.Cuts
#   pcb-layout-bottom.svg   B.Cu + B.Silkscreen + B.Mask + Edge.Cuts (mirrored)
#
# Requires: kicad-cli (KiCad >= 9), ImageMagick (magick)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PCB="$ROOT/pico-stretch2.kicad_pcb"
OUT="$ROOT/images"

KICAD_CLI="${KICAD_CLI:-}"
if [[ -z "$KICAD_CLI" ]]; then
  if command -v kicad-cli >/dev/null 2>&1; then
    KICAD_CLI="kicad-cli"
  elif [[ -x "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]]; then
    KICAD_CLI="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
  else
    echo "error: kicad-cli not found. Set KICAD_CLI=/path/to/kicad-cli or install KiCad." >&2
    exit 1
  fi
fi

if ! command -v magick >/dev/null 2>&1; then
  echo "error: ImageMagick 'magick' not found. brew install imagemagick" >&2
  exit 1
fi

mkdir -p "$OUT"

render_3d() {
  local out="$1" side="$2"; shift 2
  echo ">> render $out ($side)"
  "$KICAD_CLI" pcb render \
    --output "$OUT/$out" \
    --side "$side" \
    --quality high \
    --background transparent \
    "$@" \
    "$PCB" >/dev/null
  magick "$OUT/$out" -trim +repage -bordercolor none -border 40 "$OUT/$out"
}

render_layout() {
  local out="$1" layers="$2"; shift 2
  echo ">> export $out"
  "$KICAD_CLI" pcb export svg \
    --output "$OUT/$out" \
    --layers "$layers" \
    --exclude-drawing-sheet \
    --fit-page-to-board \
    --page-size-mode 2 \
    --mode-single \
    "$@" \
    "$PCB" >/dev/null
}

render_3d pcb-3d-top.png         top    --width 2400 --height 1800 --perspective --rotate "-25,0,25"
render_3d pcb-3d-flat-top.png    top    --width 3000 --height 1000
render_3d pcb-3d-flat-bottom.png bottom --width 3000 --height 1000

render_layout pcb-layout-top.svg    "F.Cu,F.Silkscreen,F.Mask,Edge.Cuts"
render_layout pcb-layout-bottom.svg "B.Cu,B.Silkscreen,B.Mask,Edge.Cuts" --mirror

echo "done. outputs in $OUT/"
