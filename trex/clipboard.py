"""Clipboard operations for Wayland"""

import io
import logging
import subprocess
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)


class ClipboardManager:
    """Manage clipboard operations using wl-clipboard"""
    
    def __init__(self):
        """Initialize clipboard manager"""
        self._validate_tools()
        
    def _validate_tools(self) -> None:
        """Ensure wl-clipboard tools are available"""
        for tool in ['wl-copy', 'wl-paste']:
            try:
                subprocess.run([tool, '--version'], 
                             capture_output=True, 
                             check=False)
            except FileNotFoundError:
                raise RuntimeError(
                    f"{tool} not found. Please install wl-clipboard:\n"
                    f"  sudo pacman -S wl-clipboard"
                )
            
    def set_text(self, text: str) -> None:
        """Copy text to clipboard
        
        Args:
            text: Text to copy
        """
        try:
            process = subprocess.Popen(['wl-copy'], 
                                     stdin=subprocess.PIPE,
                                     text=True)
            process.communicate(text)
            if process.returncode != 0:
                raise RuntimeError("wl-copy failed")
        except Exception as e:
            logger.error(f"Failed to copy text: {e}")
            raise
            
    def get_text(self) -> Optional[str]:
        """Get text from clipboard
        
        Returns:
            Text content or None
        """
        try:
            result = subprocess.run(['wl-paste', '--no-newline'],
                                  capture_output=True,
                                  text=True)
            if result.returncode == 0:
                return result.stdout
            return None
        except Exception as e:
            logger.error(f"Failed to get text: {e}")
            return None
            
    def get_image(self) -> Optional[Image.Image]:
        """Get image from clipboard
        
        Returns:
            PIL Image or None if no image in clipboard
        """
        try:
            # Check available MIME types
            result = subprocess.run(['wl-paste', '--list-types'],
                                  capture_output=True,
                                  text=True)
            if result.returncode != 0:
                return None
                
            mime_types = result.stdout.strip().split('\n')
            
            # Try image MIME types
            for mime in ['image/png', 'image/jpeg', 'image/bmp']:
                if mime in mime_types:
                    result = subprocess.run(['wl-paste', '--type', mime],
                                          capture_output=True)
                    if result.returncode == 0 and result.stdout:
                        return Image.open(io.BytesIO(result.stdout))
                        
            return None
            
        except Exception as e:
            logger.error(f"Failed to get image from clipboard: {e}")
            return None
            
    def clear(self) -> None:
        """Clear clipboard contents"""
        self.set_text("")