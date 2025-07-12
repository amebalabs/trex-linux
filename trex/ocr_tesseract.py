"""Fast OCR using Tesseract for speed-critical scenarios"""

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Union
import sys

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


class TesseractOCR:
    """Lightweight OCR using Tesseract - much faster but less accurate than EasyOCR"""
    
    def __init__(self, language: str = 'eng'):
        """Initialize Tesseract OCR
        
        Args:
            language: Tesseract language code (e.g., 'eng', 'deu', 'fra')
        """
        self.language = language
        self._validate_tesseract()
        
    def _validate_tesseract(self) -> None:
        """Check if Tesseract is installed"""
        try:
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode != 0:
                raise RuntimeError("Tesseract not found")
        except FileNotFoundError:
            # Try to install Tesseract interactively
            if self._offer_install():
                # Re-validate after installation
                self._validate_tesseract()
            else:
                raise RuntimeError(
                    "Tesseract OCR is required for fast mode.\n"
                    "Use --accurate flag for AI-powered OCR instead."
                )
    
    def _get_install_command(self) -> str:
        """Get distro-specific install command"""
        try:
            # Check for common distros
            if Path('/etc/arch-release').exists():
                return "  sudo pacman -S tesseract tesseract-data-eng"
            elif Path('/etc/debian_version').exists():
                return "  sudo apt install tesseract-ocr tesseract-ocr-eng"
            elif Path('/etc/fedora-release').exists():
                return "  sudo dnf install tesseract tesseract-langpack-eng"
            elif Path('/etc/os-release').exists():
                # Parse os-release for other distros
                with open('/etc/os-release') as f:
                    content = f.read().lower()
                    if 'ubuntu' in content:
                        return "  sudo apt install tesseract-ocr tesseract-ocr-eng"
                    elif 'suse' in content:
                        return "  sudo zypper install tesseract-ocr"
        except:
            pass
        
        # Generic fallback
        return "  # Check your package manager for 'tesseract' or 'tesseract-ocr'"
    
    def _offer_install(self) -> bool:
        """Offer to install Tesseract automatically"""
        # Check if we're in an interactive terminal
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            return False
            
        install_cmd = self._get_install_command().strip()
        
        # Check if we have a known package manager command
        if install_cmd.startswith('#'):
            print("\nTesseract OCR not found!")
            print("Please install it manually using your package manager.")
            return False
            
        print("\nTesseract OCR not found!")
        print(f"\nWould you like to install it now?")
        print(f"This will run: {install_cmd}")
        
        # Get user input
        try:
            response = input("\nInstall Tesseract? [Y/n]: ").strip().lower()
            if response in ('', 'y', 'yes'):
                print(f"\nInstalling Tesseract...")
                # Run the install command with shell=True to handle sudo properly
                result = subprocess.run(install_cmd, shell=True, check=False)
                if result.returncode == 0:
                    print("✓ Tesseract installed successfully!")
                    # Also try to install language data if it's a separate package
                    if 'tesseract-data-eng' not in install_cmd and 'tesseract-ocr-eng' not in install_cmd:
                        # Language data might already be included
                        pass
                    return True
                else:
                    print("✗ Installation failed. Please install manually.")
                    return False
            else:
                print("\nSkipping installation.")
                return False
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled.")
            return False
            
    def extract_text(self, image: Union[Image.Image, np.ndarray]) -> str:
        """Extract text using Tesseract
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Extracted text
        """
        # Convert numpy array to PIL if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
            
        # Save image to temp file (Tesseract needs file input)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            image.save(tmp_path)
            
        try:
            # Run Tesseract
            result = subprocess.run(
                ['tesseract', str(tmp_path), 'stdout', '-l', self.language],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                text = result.stdout.strip()
                logger.debug(f"Tesseract extracted {len(text)} characters")
                return text
            else:
                logger.error(f"Tesseract failed: {result.stderr}")
                return ""
                
        finally:
            # Clean up
            if tmp_path.exists():
                tmp_path.unlink()