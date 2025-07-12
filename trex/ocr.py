"""OCR processing with EasyOCR"""

import logging
import warnings
from pathlib import Path
from typing import Optional, Union, List

import numpy as np
from PIL import Image

# Suppress PyTorch warnings about pin_memory
warnings.filterwarnings("ignore", message=".*pin_memory.*")

logger = logging.getLogger(__name__)


class OCREngine:
    """OCR engine using EasyOCR"""
    
    def __init__(self, language: str = 'en', gpu: bool = True, fast_mode: bool = False):
        """Initialize OCR engine
        
        Args:
            language: Language code (e.g., 'en', 'fr', 'de')
            gpu: Whether to use GPU acceleration
            fast_mode: Skip preprocessing for faster results
        """
        self.language = self._convert_language_code(language)
        self.fast_mode = fast_mode
        
        # Check if CUDA is actually available
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            use_gpu = gpu and cuda_available
        except ImportError:
            use_gpu = False
        
        # Lazy import easyocr to avoid startup delay
        import easyocr
        
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(
            [self.language], 
            gpu=use_gpu,
            verbose=False
        )
        logger.debug(f"Initialized EasyOCR with language: {self.language}, GPU: {use_gpu}")
        
    def _convert_language_code(self, tesseract_code: str) -> str:
        """Convert Tesseract language codes to EasyOCR format
        
        Args:
            tesseract_code: Tesseract language code
            
        Returns:
            EasyOCR language code
        """
        # Common mappings from Tesseract to EasyOCR
        mappings = {
            'eng': 'en',
            'fra': 'fr',
            'deu': 'de',
            'spa': 'es',
            'por': 'pt',
            'ita': 'it',
            'rus': 'ru',
            'jpn': 'ja',
            'kor': 'ko',
            'chi_sim': 'ch_sim',
            'chi_tra': 'ch_tra',
        }
        
        # Return mapped code or assume it's already in EasyOCR format
        return mappings.get(tesseract_code, tesseract_code)
            
    def extract_text(self, image: Union[Image.Image, np.ndarray]) -> str:
        """Extract text from image using EasyOCR
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Extracted text
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image_array = np.array(image)
        else:
            image_array = image
            
        # Preprocess image for better OCR (skip in fast mode)
        if self.fast_mode:
            processed = image_array
        else:
            processed = self.preprocess_image(image_array)
        
        try:
            # Run OCR
            results = self.reader.readtext(
                processed,
                detail=0,  # Only return text, not bounding boxes
                paragraph=True,  # Combine text into paragraphs
                width_ths=0.7,  # Threshold for grouping text
                height_ths=0.7
            )
            
            # Join results with newlines
            text = '\n'.join(results) if results else ''
            
            # Clean up text
            text = self._clean_text(text)
            
            logger.debug(f"Extracted {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            raise
            
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Enhance image for better OCR accuracy
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        # Lazy import cv2
        import cv2
        
        # Ensure image is uint8
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        # EasyOCR works well with color images, but we can still enhance
        
        # Apply denoising
        if len(image.shape) == 3:
            denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        else:
            denoised = cv2.fastNlMeansDenoising(image)
        
        # Increase contrast using CLAHE
        if len(denoised.shape) == 3:
            # Convert to LAB color space
            lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            
            # Merge and convert back
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
        else:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
        
        return enhanced
        
    def _clean_text(self, text: str) -> str:
        """Clean up extracted text
        
        Args:
            text: Raw text from OCR
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                cleaned_lines.append(line)
                
        return '\n'.join(cleaned_lines)
        
    @staticmethod
    def get_available_languages() -> List[str]:
        """Get list of available EasyOCR languages
        
        Returns:
            List of language codes
        """
        # EasyOCR supported languages
        languages = [
            'en', 'fr', 'de', 'es', 'pt', 'it', 'ru', 'ja', 'ko',
            'ch_sim', 'ch_tra', 'ar', 'hi', 'th', 'vi', 'pl', 'nl',
            'sv', 'no', 'da', 'fi', 'cs', 'hu', 'tr', 'he', 'id',
            'ms', 'uk', 'ro', 'bg', 'hr', 'sk', 'sl', 'et', 'lv',
            'lt', 'fa', 'ur', 'ne', 'si', 'ta', 'te', 'kn', 'mr',
            'bn', 'mn', 'be', 'kk', 'az', 'uz', 'sq', 'mk', 'ka'
        ]
        return sorted(languages)
            
    def extract_data(self, image: Union[Image.Image, np.ndarray]) -> dict:
        """Extract structured data (text, confidence, bounding boxes)
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with detailed OCR data
        """
        if isinstance(image, Image.Image):
            image_array = np.array(image)
        else:
            image_array = image
            
        processed = self.preprocess_image(image_array)
        
        try:
            # Get detailed results with bounding boxes
            results = self.reader.readtext(
                processed,
                detail=1,  # Return full details
                paragraph=False  # Keep individual text elements
            )
            
            # Convert to format similar to Tesseract output
            data = {
                'text': [],
                'conf': [],
                'left': [],
                'top': [],
                'width': [],
                'height': []
            }
            
            for bbox, text, conf in results:
                # bbox is in format [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                left = int(min(x_coords))
                top = int(min(y_coords))
                width = int(max(x_coords) - left)
                height = int(max(y_coords) - top)
                
                data['text'].append(text)
                data['conf'].append(int(conf * 100))  # Convert to percentage
                data['left'].append(left)
                data['top'].append(top)
                data['width'].append(width)
                data['height'].append(height)
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise