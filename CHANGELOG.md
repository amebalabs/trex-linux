# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-13

### Added
- **QR Code Detection** - Automatic QR code recognition and decoding
  - Smart fallback to OCR when no QR codes are found
  - Support for multiple QR codes in a single image
  - `-q/--qr` flag to enable QR mode
- **URL Auto-Opening** - Automatically detect and open URLs
  - `-u/--open-urls` flag to open detected URLs in browser
  - Works with both OCR text and QR code content
  - Smart URL detection with comprehensive regex patterns
- **New Configuration Options**
  - `open_urls`: Set to true to always open detected URLs
  - `qr_mode`: Set to true to use QR mode by default

### Changed
- QR code dependencies (opencv-python, pyzbar) are now included by default
- Improved UX: Single mode can handle both QR codes and text
- Updated project description to reflect QR code capabilities

### Dependencies
- Added opencv-python>=4.5 to core dependencies
- Added pyzbar>=0.1.9 to core dependencies
- New system requirement: zbar library (`sudo pacman -S zbar`)

## [1.0.1] - Previous release
- Bug fixes and minor improvements

## [1.0.0] - 2025-01-12

### Features
- `--accurate` flag to use EasyOCR for complex text recognition
- Interactive Tesseract installation prompt on first run
- Auto-detection of Linux distribution for install commands
- Smart language code mapping (e.g., 'en' → 'eng' for Tesseract)
- CPU-only PyTorch installation by default (when using `[accurate]`)

### Performance
- Default mode: ~0.3-0.5s (Tesseract)
- Accurate mode: ~2-3s (EasyOCR)
- Instant crosshair appearance (<0.02s)

### Design Decisions
- Tesseract by default for speed
- Minimal dependencies (click, Pillow, numpy)
- Lazy loading for instant UI response
- Silent clipboard operation
- CPU-only PyTorch for accurate mode