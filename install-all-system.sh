#!/bin/bash
# Install OTB, OTB1 and OTB2 system-wide. Requires root.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root."
    echo "Usage:  sudo $0"
    exit 1
fi

for variant in adobe-courier-otb adobe-courier-otb1 adobe-courier-otb2; do
    echo ""
    echo "############################################################"
    echo "# $variant"
    echo "############################################################"
    "$SCRIPT_DIR/$variant/install-system.sh"
done

echo ""
echo "All variants installed system-wide."
