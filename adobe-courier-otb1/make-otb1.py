#!/usr/bin/env python3
"""
make-otb1.py - Generate "Adobe Courier (OTB1)" from "Adobe Courier (OTB)".

OTB1 has the same bitmaps as OTB but +1 pixel of built-in line spacing
(added to ascent), useful for GTK/Pango applications that don't offer
adjustable line spacing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

OLD_FAMILY = "Adobe Courier (OTB)"
NEW_FAMILY = "Adobe Courier (OTB1)"

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_DIR = SCRIPT_DIR.parent / "adobe-courier-otb" / "fonts"
DST_DIR = SCRIPT_DIR / "fonts"

PPEM_RE = re.compile(r"-(\d+)px\.otb$")


def patch_font(src: Path, dst: Path) -> tuple[int, int, int]:
    """Patch one .otb file. Returns (ppem, delta_funits, num_name_records_changed)."""
    m = PPEM_RE.search(src.name)
    if not m:
        raise ValueError(f"Cannot determine ppem from filename: {src.name}")
    ppem = int(m.group(1))

    font = TTFont(str(src), recalcBBoxes=False, recalcTimestamp=False)

    upem = font["head"].unitsPerEm
    if upem % ppem != 0:
        raise ValueError(
            f"{src.name}: unitsPerEm ({upem}) is not divisible by ppem ({ppem})"
        )
    delta = upem // ppem

    # Increase ascent by 1 pixel.
    font["hhea"].ascent += delta
    os2 = font["OS/2"]
    os2.sTypoAscender += delta
    os2.usWinAscent += delta
    font["head"].yMax += delta

    # Normalize underline metrics.
    if "post" in font:
        font["post"].underlinePosition = -delta
        font["post"].underlineThickness = 100

    # Rename family in all relevant name records.
    name_table = font["name"]
    changed = 0
    for rec in name_table.names:
        try:
            s = rec.toUnicode()
        except Exception:
            continue
        if OLD_FAMILY in s:
            new_s = s.replace(OLD_FAMILY, NEW_FAMILY)
            rec.string = new_s.encode(
                "utf-16-be" if rec.platformID == 3 else "ascii", errors="replace"
            )
            changed += 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(dst))
    font.close()
    return ppem, delta, changed


def main() -> int:
    if not SRC_DIR.is_dir():
        print(f"ERROR: source directory not found: {SRC_DIR}", file=sys.stderr)
        return 1

    sources = sorted(SRC_DIR.glob("AdobeCourier-*.otb"))
    if not sources:
        print(f"ERROR: no .otb files found in {SRC_DIR}", file=sys.stderr)
        return 1

    print(f"Source: {SRC_DIR}")
    print(f"Target: {DST_DIR}")
    print(f"Files:  {len(sources)}")
    print("")

    for src in sources:
        dst = DST_DIR / src.name
        ppem, delta, changed = patch_font(src, dst)
        print(
            f"  {src.name:<40s} ppem={ppem:>2d}  +{delta} FUnits  "
            f"({changed} name records renamed)"
        )

    print("")
    print(f"Done. {len(sources)} files written to {DST_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
