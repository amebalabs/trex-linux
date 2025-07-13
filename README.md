# TRex - Text Recognition for Arch Linux

[![PyPI version](https://badge.fury.io/py/trex-ocr.svg)](https://badge.fury.io/py/trex-ocr)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-amebalabs%2Ftrex--linux-black?logo=github)](https://github.com/amebalabs/trex-ocr)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)
[![Arch Linux](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff)](https://archlinux.org/)
[![Wayland](https://img.shields.io/badge/Wayland-Native-orange.svg)](https://wayland.freedesktop.org/)

Lightning-fast OCR tool optimized for Wayland/Hyprland on Arch Linux. Select screen area → Extract text → Copy to clipboard.

<p align="center">
  <img src="https://img.shields.io/badge/OCR-Tesseract-green?style=for-the-badge" alt="OCR: Tesseract">
  <img src="https://img.shields.io/badge/OCR-EasyOCR-purple?style=for-the-badge" alt="OCR: EasyOCR">
  <img src="https://img.shields.io/badge/Speed-Lightning%20Fast-yellow?style=for-the-badge" alt="Speed: Lightning Fast">
  <img src="https://img.shields.io/badge/GPU-CUDA%20Ready-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="GPU: CUDA Ready">
</p>

## Features

- 🎯 **Simple** - One command to capture and extract text
- ⚡ **Lightning Fast** - Tesseract by default, results in under 0.5s
- 🖥️ **Wayland Native** - Built for modern Linux desktops
- 📋 **Clipboard Integration** - Automatically copies extracted text
- 🎨 **Flexible** - Fast mode by default, --accurate flag for complex text

## Installation

[![PyPI - Downloads](https://img.shields.io/pypi/dm/trex-ocr)](https://pypi.org/project/trex-ocr/)
[![PyPI - Format](https://img.shields.io/pypi/format/trex-ocr)](https://pypi.org/project/trex-ocr/)

```bash
# Install system dependencies (Arch Linux)
sudo pacman -S grim slurp wl-clipboard tesseract tesseract-data-eng

# Install TRex (lightweight by default)
pip install trex-ocr
```

By default, TRex uses Tesseract for blazing-fast OCR. For better accuracy on complex images, install the accurate mode dependencies.

## Usage

```bash
# Default: Select area → OCR → Copy to clipboard
trex

# OCR image from clipboard
trex -c

# OCR image file
trex -f screenshot.png

# Output to stdout instead of clipboard
trex -o stdout

# Use different language (e.g., German)
trex -l deu

# Use accurate mode for complex/handwritten text
trex --accurate
```

## Performance

- **Default mode**: ~0.3-0.5s (Tesseract)
- **Accurate mode**: ~2-3s (EasyOCR, downloads AI models on first use)

## Languages

**Tesseract (default)**: Uses standard 3-letter codes
- `eng` - English (default)
- `deu` - German
- `fra` - French
- `spa` - Spanish
- `jpn` - Japanese
- Install more: `sudo pacman -S tesseract-data-[lang]`

**EasyOCR (--accurate mode)**: 
- `en`, `de`, `fr`, `es`, `ja`, `ko`, `ch_sim`, etc.
- Full list: https://github.com/JaidedAI/EasyOCR#supported-languages

## Configuration

Optional config file at `~/.config/trex/config.json`:

```json
{
  "language": "en",
  "gpu": false
}
```

Set `"gpu": true` if you have NVIDIA GPU with CUDA support.

## Requirements

- Arch Linux
- Wayland compositor (tested on Hyprland)
- Python 3.8+
- CUDA (optional, for GPU acceleration)

## Accurate Mode Setup

For complex images, handwriting, or multiple languages:

```bash
# Install accurate mode dependencies  
pip install trex-ocr[accurate] --extra-index-url https://download.pytorch.org/whl/cpu

# Or with GPU support (NVIDIA CUDA)
pip install trex-ocr[accurate,gpu]
```

Then use `trex --accurate` for better accuracy at the cost of speed.

## License

MIT