import logging
from typing import List, Optional
from PIL import Image

logger = logging.getLogger(__name__)


def decode_qr_codes(image: Image.Image) -> List[str]:
    """
    Detect and decode QR codes in the given image.
    
    Args:
        image: PIL Image to scan for QR codes
        
    Returns:
        List of decoded QR code contents
    """
    try:
        import cv2
        import numpy as np
        from pyzbar import pyzbar
    except ImportError as e:
        logger.warning(f"QR code libraries not installed: {e}")
        return []
    
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Convert RGB to BGR if needed (OpenCV uses BGR)
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Detect and decode QR codes
    qr_codes = pyzbar.decode(img_array)
    
    results = []
    for qr_code in qr_codes:
        try:
            # Decode the data
            data = qr_code.data.decode('utf-8')
            results.append(data)
            logger.debug(f"Decoded QR code: {data}")
        except Exception as e:
            logger.warning(f"Failed to decode QR code: {e}")
    
    return results


def is_qr_content_url(content: str) -> bool:
    """
    Check if QR code content is a URL.
    
    Args:
        content: Decoded QR code content
        
    Returns:
        True if content appears to be a URL
    """
    return content.startswith(('http://', 'https://', 'www.'))