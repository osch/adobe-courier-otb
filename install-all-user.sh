#!/bin/bash
# Install OTB, OTB1 and OTB2 for the current user.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for variant in adobe-courier-otb adobe-courier-otb1 adobe-courier-otb2; do
    echo ""
    echo "############################################################"
    echo "# $variant"
    echo "############################################################"
    "$SCRIPT_DIR/$variant/install-user.sh"
done

echo ""
echo "All variants installed."
