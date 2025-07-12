#!/bin/bash
# Installation script for TRex on Arch Linux

set -e

echo "TRex Installation for Arch Linux"
echo "================================"
echo

# Check if running on Arch
if [ ! -f /etc/arch-release ]; then
    echo "This installer is for Arch Linux only."
    echo "For other distributions, install manually:"
    echo "  pip install trex-linux"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo pacman -S --needed --noconfirm grim slurp wl-clipboard

echo
echo "System dependencies installed successfully!"
echo
echo "To install TRex:"
echo "  pip install trex-linux"
echo
echo "Note: EasyOCR will download its models on first use (~100MB)"