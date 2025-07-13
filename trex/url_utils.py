import re
import subprocess
from typing import List


def detect_urls(text: str) -> List[str]:
    """
    Detect URLs in the given text.
    
    Args:
        text: The text to search for URLs
        
    Returns:
        List of detected URLs
    """
    # Comprehensive URL regex pattern
    url_pattern = re.compile(
        r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
        r'(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)|'
        r'(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
        r'(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    )
    
    urls = url_pattern.findall(text)
    
    # Add http:// to URLs that start with www. but don't have a protocol
    normalized_urls = []
    for url in urls:
        if url.startswith('www.') and not url.startswith(('http://', 'https://')):
            normalized_urls.append(f'http://{url}')
        else:
            normalized_urls.append(url)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in normalized_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls


def open_urls(urls: List[str]) -> None:
    """
    Open the given URLs in the default browser using xdg-open.
    
    Args:
        urls: List of URLs to open
    """
    for url in urls:
        try:
            subprocess.run(['xdg-open', url], check=False, capture_output=True)
        except Exception:
            # Silently ignore errors when opening URLs
            pass