#!/usr/bin/env python3
"""Render Adobe Courier OTB sample grid to PNG.
Layout: 2 columns (Regular|Bold, Italic|Bold Italic), one group per variant.
Requires: python-gobject; fonts installed via install-all-user.sh.
"""

import os
import subprocess
import sys

try:
    import gi
    gi.require_version('Pango', '1.0')
    gi.require_version('PangoCairo', '1.0')
    from gi.repository import Pango, PangoCairo
    import cairo
except ImportError:
    sys.exit("ERROR: python-gobject not found. Install: pacman -S python-gobject")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIZE_PT = 9
PAD = 10
SEP = 1   # separator between variants

SAMPLE = (
    ' !"#$%&\'()*+,-./0123456789:;<=>?\n'
    '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\n'
    '`abcdefghijklmnopqrstuvwxyz{|}~\n'
    ' ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿\n'
    'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß\n'
    'àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
)

VARIANTS = [
    ('OTB',  'Adobe Courier (OTB)'),
    ('OTB1', 'Adobe Courier (OTB1)'),
    ('OTB2', 'Adobe Courier (OTB2)'),
]

# Two weight-rows, each with 2 columns
WEIGHT_ROWS = [
    [('Regular', Pango.Weight.NORMAL, Pango.Style.NORMAL),
     ('Bold',    Pango.Weight.BOLD,   Pango.Style.NORMAL)],
    [('Italic',      Pango.Weight.NORMAL, Pango.Style.ITALIC),
     ('Bold Italic', Pango.Weight.BOLD,   Pango.Style.ITALIC)],
]


def make_layout(ctx, text, family=None, size_pt=None, weight=None, style=None, desc_str=None):
    layout = PangoCairo.create_layout(ctx)
    if desc_str:
        layout.set_font_description(Pango.FontDescription(desc_str))
    else:
        fd = Pango.FontDescription()
        fd.set_family(family)
        fd.set_size(int(size_pt * Pango.SCALE))
        fd.set_weight(weight)
        fd.set_style(style)
        layout.set_font_description(fd)
    layout.set_text(text, -1)
    return layout


# Measure phase
dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
dctx = cairo.Context(dummy)

col_label_h = make_layout(dctx, 'X', desc_str='Sans 7').get_pixel_size()[1]
col_w = [0, 0]
# row_h[vi][wri] = height of weight-row wri within variant vi
row_h = [[0] * len(WEIGHT_ROWS) for _ in VARIANTS]

for vi, (short, fam) in enumerate(VARIANTS):
    for wri, weight_row in enumerate(WEIGHT_ROWS):
        for ci, (lbl, wt, st) in enumerate(weight_row):
            sl = make_layout(dctx, SAMPLE, family=fam, size_pt=SIZE_PT, weight=wt, style=st)
            tw, th = sl.get_pixel_size()
            ll = make_layout(dctx, f'{short} – {lbl}', desc_str='Sans 7')
            lw, _ = ll.get_pixel_size()
            col_w[ci] = max(col_w[ci], max(tw, lw) + 2 * PAD)
            row_h[vi][wri] = max(row_h[vi][wri], col_label_h + 4 + th + 2 * PAD)

W = sum(col_w)
H = (sum(sum(rh) for rh in row_h)
     + SEP * (len(VARIANTS) - 1))

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surf)
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

y = 0
for vi, (short, fam) in enumerate(VARIANTS):
    if vi > 0:
        ctx.set_source_rgb(0.75, 0.75, 0.75)
        ctx.rectangle(0, y, W, SEP)
        ctx.fill()
        y += SEP

    for wri, weight_row in enumerate(WEIGHT_ROWS):
        x = 0
        for ci, (lbl, wt, st) in enumerate(weight_row):
            ctx.set_source_rgb(0.5, 0.5, 0.5)
            ll = make_layout(ctx, f'{short} – {lbl}', desc_str='Sans 7')
            ctx.move_to(x + PAD, y + PAD)
            PangoCairo.show_layout(ctx, ll)

            ctx.set_source_rgb(0, 0, 0)
            sl = make_layout(ctx, SAMPLE, family=fam, size_pt=SIZE_PT, weight=wt, style=st)
            ctx.move_to(x + PAD, y + PAD + col_label_h + 4)
            PangoCairo.show_layout(ctx, sl)

            x += col_w[ci]
        y += row_h[vi][wri]

out = os.path.join(SCRIPT_DIR, 'sample-all.png')
surf.write_to_png(out)
print(f'wrote {out}  ({W}×{H} px)')
subprocess.Popen(['xdg-open', out])
