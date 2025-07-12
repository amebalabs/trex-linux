"""Utility functions for TRex"""

import logging
import os
import sys
from pathlib import Path


def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration
    
    Args:
        debug: Enable debug logging
    """
    level = logging.DEBUG if debug else logging.INFO
    
    # Configure logging format
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if debug:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        stream=sys.stderr
    )
    
    # Quiet some noisy loggers
    if not debug:
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.getLogger('pyzbar').setLevel(logging.WARNING)
        

def ensure_directory(path: Path) -> None:
    """Ensure a directory exists
    
    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    

def get_cache_dir() -> Path:
    """Get cache directory for TRex
    
    Returns:
        Path to cache directory
    """
    # Follow XDG Base Directory specification
    xdg_cache = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache:
        cache_dir = Path(xdg_cache) / 'trex'
    else:
        cache_dir = Path.home() / '.cache' / 'trex'
        
    ensure_directory(cache_dir)
    return cache_dir
    

def get_data_dir() -> Path:
    """Get data directory for TRex
    
    Returns:
        Path to data directory
    """
    # Follow XDG Base Directory specification
    xdg_data = os.environ.get('XDG_DATA_HOME')
    if xdg_data:
        data_dir = Path(xdg_data) / 'trex'
    else:
        data_dir = Path.home() / '.local' / 'share' / 'trex'
        
    ensure_directory(data_dir)
    return data_dir
    

def format_size(bytes: int) -> str:
    """Format bytes as human-readable size
    
    Args:
        bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"
    

def validate_image_file(path: Path) -> bool:
    """Validate that a file is a supported image
    
    Args:
        path: File path
        
    Returns:
        True if file is a valid image
    """
    if not path.exists():
        return False
        
    # Check file extension
    supported_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    if path.suffix.lower() not in supported_extensions:
        return False
        
    # Try to open with PIL to validate
    try:
        from PIL import Image
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False
        

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
        
    return text[:max_length - len(suffix)] + suffix