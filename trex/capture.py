"""Screen capture functionality for Wayland/Hyprland"""

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)


class ScreenCapture:
    """Handle screen capture operations using grim/slurp"""
    
    def __init__(self):
        """Initialize screen capture for Wayland"""
        self._validate_tools()
        
    def _validate_tools(self) -> None:
        """Validate that grim and slurp are available"""
        for tool in ['grim', 'slurp']:
            try:
                subprocess.run([tool, '--help'], 
                             capture_output=True, 
                             check=False)
            except FileNotFoundError:
                raise RuntimeError(
                    f"{tool} not found. Please install it:\n"
                    f"  sudo pacman -S grim slurp"
                )
            
    def capture_area(self) -> Optional[Image.Image]:
        """Interactive area selection with slurp
        
        Returns:
            PIL Image object or None if cancelled
        """
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            
        try:
            # Use slurp for area selection
            slurp_result = subprocess.run(
                ['slurp'], 
                capture_output=True, 
                text=True
            )
            
            if slurp_result.returncode != 0:
                logger.debug("Selection cancelled")
                return None
                
            # Get the selection geometry
            geometry = slurp_result.stdout.strip()
            
            # Capture the selected area
            grim_result = subprocess.run(
                ['grim', '-g', geometry, str(tmp_path)],
                capture_output=True,
                text=True
            )
            
            if grim_result.returncode == 0 and tmp_path.exists():
                return Image.open(tmp_path)
            else:
                logger.error(f"grim failed: {grim_result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None
        finally:
            # Clean up temp file
            if tmp_path.exists():
                tmp_path.unlink()
                
    def capture_fullscreen(self) -> Optional[Image.Image]:
        """Capture entire screen
        
        Returns:
            PIL Image object
        """
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            
        try:
            # Full screen capture
            result = subprocess.run(
                ['grim', str(tmp_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and tmp_path.exists():
                return Image.open(tmp_path)
            else:
                logger.error(f"grim failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None
        finally:
            if tmp_path.exists():
                tmp_path.unlink()