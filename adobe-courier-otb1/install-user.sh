#!/bin/bash
# Adobe Courier (OTB1) - User Installation
# Installs the bitmap fonts for the current user only.
#
# OTB1 is identical to OTB except for +1 pixel of built-in line spacing,
# which helps GTK/Pango applications that do not allow adjusting line
# spacing manually (unlike KDE/Qt apps).

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONT_DIR="$HOME/.local/share/fonts/adobe-courier-otb1"

echo "Adobe Courier (OTB1) - User Installation"
echo "========================================="
echo ""
echo "Target directory: $FONT_DIR"
echo ""

mkdir -p "$FONT_DIR"

count=0
for f in "$SCRIPT_DIR"/fonts/AdobeCourier-*.otb; do
    [ -f "$f" ] || continue
    cp "$f" "$FONT_DIR/"
    count=$((count + 1))
done

if [ "$count" -eq 0 ]; then
    echo "ERROR: No font files found in $SCRIPT_DIR/fonts/"
    exit 1
fi

chmod 644 "$FONT_DIR"/AdobeCourier-*.otb

echo "$count font files installed."
echo "Updating font cache..."
fc-cache -f "$FONT_DIR"
echo ""
echo "Done! The font 'Adobe Courier (OTB1)' is now available."
echo "To uninstall:  rm -rf $FONT_DIR && fc-cache -f"
