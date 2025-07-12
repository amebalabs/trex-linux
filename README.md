# TRex - Text Recognition for Arch Linux

Lightning-fast OCR tool optimized for Wayland/Hyprland on Arch Linux. Select screen area → Extract text → Copy to clipboard.

## Features

- 🎯 **Simple** - One command to capture and extract text
- ⚡ **Lightning Fast** - Tesseract by default, results in under 0.5s
- 🖥️ **Wayland Native** - Built for modern Linux desktops
- 📋 **Clipboard Integration** - Automatically copies extracted text
- 🎨 **Flexible** - Fast mode by default, --accurate flag for complex text

## Installation

```bash
# Install system dependencies (Arch Linux)
sudo pacman -S grim slurp wl-clipboard tesseract tesseract-data-eng

# Install TRex (lightweight by default)
pip install trex-linux
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
pip install trex-linux[accurate] --extra-index-url https://download.pytorch.org/whl/cpu

# Or with GPU support (NVIDIA CUDA)
pip install trex-linux[accurate,gpu]
```

Then use `trex --accurate` for better accuracy at the cost of speed.

## License

MIT