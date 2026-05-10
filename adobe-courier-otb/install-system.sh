#!/bin/bash
# Adobe Courier (OTB) - System-wide Installation
# Installs the bitmap fonts for all users. Requires root privileges.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONT_DIR="/usr/local/share/fonts/adobe-courier-otb"

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root."
    echo "Usage:  sudo $0"
    exit 1
fi

echo "Adobe Courier (OTB) - System-wide Installation"
echo "================================================"
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

chmod 755 "$FONT_DIR"
chmod 644 "$FONT_DIR"/*.otb

echo "$count font files installed."
echo "Updating font cache..."
fc-cache -f
echo ""
echo "Done! The font 'Adobe Courier (OTB)' is now available for all users."
echo "To uninstall:  sudo rm -rf $FONT_DIR && sudo fc-cache -f"
