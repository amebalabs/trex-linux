"""Command-line interface for TRex"""

import sys
from pathlib import Path
from typing import Optional

import click
from PIL import Image

from .capture import ScreenCapture
from .clipboard import ClipboardManager
from .config import Config
from .utils import setup_logging
from .url_utils import detect_urls, open_urls as open_detected_urls
from .qr_utils import decode_qr_codes, is_qr_content_url


@click.command()
@click.option('-c', '--clipboard', is_flag=True, help='Read image from clipboard')
@click.option('-f', '--file', type=click.Path(exists=True, path_type=Path), help='Read image from file')
@click.option('-l', '--language', default='en', help='OCR language (default: en)')
@click.option('-o', '--output', type=click.Choice(['clipboard', 'stdout']), default='clipboard', help='Output destination')
@click.option('-d', '--debug', is_flag=True, help='Enable debug logging')
@click.option('--accurate', is_flag=True, help='Use EasyOCR for better accuracy (slower)')
@click.option('-u', '--open-urls', is_flag=True, help='Automatically open detected URLs in browser')
@click.option('-q', '--qr', is_flag=True, help='QR code mode - decode QR codes, fallback to OCR if none found')
def main(
    clipboard: bool,
    file: Optional[Path],
    language: str,
    output: str,
    debug: bool,
    accurate: bool,
    open_urls: bool,
    qr: bool,
) -> None:
    """TRex - Text Recognition for Arch Linux / Hyprland
    
    Capture screen areas and extract text using AI-powered OCR.
    
    Default behavior: Interactive screen capture → OCR → copy to clipboard
    """
    # Setup logging
    setup_logging(debug)
    
    # Load configuration
    cfg = Config()
    
    # Override language if specified
    if language != 'en':
        cfg.config['language'] = language
    
    # Use config option as default for open_urls if not specified
    if not open_urls and cfg.open_urls:
        open_urls = True
    
    # Use config option as default for qr mode if not specified
    if not qr and cfg.qr_mode:
        qr = True
    
    # Initialize clipboard manager early (lightweight)
    clipboard_mgr = ClipboardManager()
    
    try:
        # Get image based on input source
        image = None
        
        if clipboard:
            # Get image from clipboard
            image = clipboard_mgr.get_image()
            if not image:
                click.echo("No image found in clipboard", err=True)
                sys.exit(1)
                
        elif file:
            # Read image from file
            try:
                image = Image.open(file)
            except Exception as e:
                click.echo(f"Error reading file: {e}", err=True)
                sys.exit(1)
                
        else:
            # Default: capture screen area
            capture = ScreenCapture()
            image = capture.capture_area()
            
            if not image:
                click.echo("Screen capture cancelled", err=True)
                sys.exit(1)
        
        # Process image - try QR first if enabled, fallback to OCR
        text = None
        qr_detected = False
        
        if qr:
            # QR code mode - but fallback to OCR if no QR codes found
            qr_contents = decode_qr_codes(image)
            if qr_contents:
                # Join multiple QR codes with newlines
                text = '\n'.join(qr_contents)
                qr_detected = True
                
                # If open_urls is enabled and QR contains URLs, open them
                if open_urls:
                    for content in qr_contents:
                        if is_qr_content_url(content):
                            open_detected_urls([content])
        
        if not text:
            # Regular OCR mode (or fallback from QR mode)
            if accurate:
                # Use EasyOCR for better accuracy (slower)
                from .ocr import OCREngine
                ocr_engine = OCREngine(language=cfg.language, gpu=cfg.gpu)
                text = ocr_engine.extract_text(image)
            else:
                # Use Tesseract by default (fast)
                try:
                    from .ocr_tesseract import TesseractOCR
                    # Map common 2-letter codes to Tesseract 3-letter codes
                    lang_map = {
                        'en': 'eng',
                        'de': 'deu', 
                        'fr': 'fra',
                        'es': 'spa',
                        'it': 'ita',
                        'pt': 'por',
                        'ja': 'jpn',
                        'ko': 'kor',
                        'zh': 'chi_sim',
                        'ru': 'rus',
                    }
                    tesseract_lang = lang_map.get(cfg.language, cfg.language)
                    ocr_engine = TesseractOCR(language=tesseract_lang)
                    text = ocr_engine.extract_text(image)
                except RuntimeError as e:
                    if "Tesseract OCR not found" in str(e):
                        click.echo(str(e), err=True)
                        sys.exit(1)
                    raise
            
            if not text:
                click.echo("No text detected", err=True)
                sys.exit(1)
            
            # Detect and open URLs if requested (only for OCR text, not QR)
            if open_urls and not qr_detected:
                urls = detect_urls(text)
                if urls:
                    open_detected_urls(urls)
            
        # Output text
        if output == 'clipboard':
            clipboard_mgr.set_text(text)
            # Silent success - no output to avoid confusion
        else:
            # stdout
            click.echo(text)
            
    except KeyboardInterrupt:
        click.echo("\nCancelled", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()