"""Simple configuration for TRex"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    """Minimal configuration for TRex"""
    
    DEFAULT_CONFIG = {
        "language": "en",
        "gpu": False,  # Default to CPU to avoid CUDA dependencies
        "clipboard_timeout_ms": 5000
    }
    
    def __init__(self):
        """Initialize with defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_user_config()
        
    def _load_user_config(self) -> None:
        """Load user config if it exists"""
        config_path = self._get_config_path()
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                    logger.debug(f"Loaded config from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
                
    def _get_config_path(self) -> Path:
        """Get config file path"""
        # Follow XDG Base Directory specification
        xdg_config = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config:
            config_dir = Path(xdg_config) / 'trex'
        else:
            config_dir = Path.home() / '.config' / 'trex'
        return config_dir / 'config.json'
        
    def save(self) -> None:
        """Save configuration to file"""
        config_path = self._get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.debug(f"Saved config to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            
    @property
    def language(self) -> str:
        """Get OCR language"""
        return self.config.get('language', 'en')
        
    @property
    def gpu(self) -> bool:
        """Get GPU usage setting"""
        return self.config.get('gpu', True)
        
    @property
    def clipboard_timeout_ms(self) -> int:
        """Get clipboard timeout in milliseconds"""
        return self.config.get('clipboard_timeout_ms', 5000)