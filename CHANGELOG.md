# Changelog

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