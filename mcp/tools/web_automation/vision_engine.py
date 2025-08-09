#!/usr/bin/env python3
"""
👁️ CHOTU VISION ENGINE
=====================
Computer vision and OCR for smart web element detection
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not installed. Visual element detection will be limited.")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ Tesseract not installed. OCR functionality will be limited.")

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not installed. Image processing will be limited.")

class VisualFinder:
    """Computer vision-based element finder"""
    
    def __init__(self):
        self.confidence_threshold = 0.7
        self.ocr_enabled = TESSERACT_AVAILABLE
        self.vision_enabled = CV2_AVAILABLE and PIL_AVAILABLE
        
        print("👁️ VisualFinder initialized")
        print(f"   OCR Available: {'YES' if self.ocr_enabled else 'NO'}")
        print(f"   Vision Available: {'YES' if self.vision_enabled else 'NO'}")
        
        # Configure Tesseract if available
        if self.ocr_enabled:
            self._configure_tesseract()
    
    def _configure_tesseract(self):
        """Configure Tesseract OCR settings"""
        try:
            # Try to set Tesseract path for macOS
            if sys.platform == 'darwin':  # macOS
                possible_paths = [
                    '/usr/local/bin/tesseract',
                    '/opt/homebrew/bin/tesseract',
                    '/usr/bin/tesseract'
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
        except Exception as e:
            print(f"⚠️ Tesseract configuration warning: {e}")
    
    def find_text_element(self, screenshot_path: str, target_text: str) -> Optional[Tuple[int, int, int, int]]:
        """
        Find element containing specific text using OCR
        
        Args:
            screenshot_path: Path to screenshot image
            target_text: Text to search for
            
        Returns:
            Tuple: (x, y, width, height) of the element or None
        """
        
        if not self.ocr_enabled or not os.path.exists(screenshot_path):
            return None
        
        try:
            print(f"👁️ Searching for text: '{target_text}'")
            
            # Load and preprocess image
            image = cv2.imread(screenshot_path) if CV2_AVAILABLE else None
            if image is None:
                # Fallback to PIL
                pil_image = Image.open(screenshot_path)
                image = np.array(pil_image)
            
            # Convert to grayscale for better OCR
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if CV2_AVAILABLE else image
            else:
                gray = image
            
            # Enhance image for OCR
            gray = self._enhance_for_ocr(gray)
            
            # Perform OCR
            ocr_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
            
            # Search for target text
            target_lower = target_text.lower()
            
            for i, text in enumerate(ocr_data['text']):
                if text.strip() and target_lower in text.lower():
                    confidence = int(ocr_data['conf'][i])
                    
                    if confidence > 50:  # Minimum confidence threshold
                        x = ocr_data['left'][i]
                        y = ocr_data['top'][i]
                        w = ocr_data['width'][i]
                        h = ocr_data['height'][i]
                        
                        print(f"✅ Found text '{text}' at ({x}, {y}) with confidence {confidence}")
                        return (x, y, w, h)
            
            print(f"❌ Text '{target_text}' not found in screenshot")
            return None
            
        except Exception as e:
            print(f"❌ OCR text search failed: {e}")
            return None
    
    def _enhance_for_ocr(self, gray_image):
        """Enhance grayscale image for better OCR results"""
        
        if not CV2_AVAILABLE:
            return gray_image
        
        try:
            # Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
            
            # Adaptive threshold for better text contrast
            enhanced = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            return enhanced
            
        except Exception:
            return gray_image
    
    def find_button_like_elements(self, screenshot_path: str) -> List[Tuple[int, int, int, int]]:
        """
        Find button-like elements using computer vision
        
        Returns:
            List of (x, y, width, height) tuples for detected buttons
        """
        
        if not self.vision_enabled or not os.path.exists(screenshot_path):
            return []
        
        try:
            print("👁️ Detecting button-like elements...")
            
            # Load image
            image = cv2.imread(screenshot_path)
            if image is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect rectangular shapes (potential buttons)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            buttons = []
            
            for contour in contours:
                # Filter by area and aspect ratio
                area = cv2.contourArea(contour)
                if 500 < area < 50000:  # Reasonable button size
                    
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Buttons typically have certain aspect ratios
                    if 0.5 < aspect_ratio < 5.0:
                        buttons.append((x, y, w, h))
            
            print(f"✅ Found {len(buttons)} potential button elements")
            return buttons
            
        except Exception as e:
            print(f"❌ Button detection failed: {e}")
            return []
    
    def find_form_fields(self, screenshot_path: str) -> List[Tuple[int, int, int, int, str]]:
        """
        Find form input fields using computer vision
        
        Returns:
            List of (x, y, width, height, type) tuples for detected form fields
        """
        
        if not self.vision_enabled or not os.path.exists(screenshot_path):
            return []
        
        try:
            print("👁️ Detecting form fields...")
            
            image = cv2.imread(screenshot_path)
            if image is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect rectangular areas that might be input fields
            edges = cv2.Canny(gray, 30, 100)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            fields = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 1000 < area < 30000:  # Reasonable input field size
                    
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Input fields are typically wide and relatively short
                    if aspect_ratio > 2.0:
                        
                        # Classify field type based on context (simplified)
                        field_type = "text"
                        
                        # Check surrounding area for labels using OCR
                        if self.ocr_enabled:
                            # Extract region around the field for context
                            context_region = gray[max(0, y-30):y+h+30, max(0, x-100):x+w+100]
                            
                            try:
                                context_text = pytesseract.image_to_string(context_region).lower()
                                
                                if any(word in context_text for word in ['email', 'mail']):
                                    field_type = "email"
                                elif any(word in context_text for word in ['password', 'pass']):
                                    field_type = "password"
                                elif any(word in context_text for word in ['search']):
                                    field_type = "search"
                                elif any(word in context_text for word in ['phone', 'number']):
                                    field_type = "tel"
                                    
                            except Exception:
                                pass  # Keep default type
                        
                        fields.append((x, y, w, h, field_type))
            
            print(f"✅ Found {len(fields)} potential form fields")
            return fields
            
        except Exception as e:
            print(f"❌ Form field detection failed: {e}")
            return []
    
    def highlight_elements(self, screenshot_path: str, elements: List[Tuple], output_path: str = None) -> str:
        """
        Highlight detected elements on screenshot for debugging
        
        Args:
            screenshot_path: Original screenshot
            elements: List of (x, y, w, h) tuples
            output_path: Where to save highlighted image
            
        Returns:
            Path to highlighted image
        """
        
        if not PIL_AVAILABLE:
            return screenshot_path
        
        try:
            # Load image
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)
            
            # Highlight each element
            for i, element in enumerate(elements):
                if len(element) >= 4:
                    x, y, w, h = element[:4]
                    
                    # Draw rectangle
                    draw.rectangle([x, y, x+w, y+h], outline='red', width=3)
                    
                    # Add number label
                    draw.text((x, y-20), str(i+1), fill='red')
            
            # Save highlighted image
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = screenshot_path.replace('.png', f'_highlighted_{timestamp}.png')
            
            image.save(output_path)
            print(f"🎨 Highlighted image saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Element highlighting failed: {e}")
            return screenshot_path
    
    def analyze_page_layout(self, screenshot_path: str) -> Dict[str, Any]:
        """
        Analyze overall page layout and structure
        
        Returns:
            Dict with layout analysis results
        """
        
        analysis = {
            "buttons": [],
            "form_fields": [],
            "text_regions": [],
            "layout_score": 0,
            "complexity": "unknown"
        }
        
        if not os.path.exists(screenshot_path):
            return analysis
        
        try:
            print("👁️ Analyzing page layout...")
            
            # Find different element types
            analysis["buttons"] = self.find_button_like_elements(screenshot_path)
            analysis["form_fields"] = self.find_form_fields(screenshot_path)
            
            # Simple complexity assessment
            total_elements = len(analysis["buttons"]) + len(analysis["form_fields"])
            
            if total_elements < 5:
                analysis["complexity"] = "simple"
            elif total_elements < 15:
                analysis["complexity"] = "moderate"
            else:
                analysis["complexity"] = "complex"
            
            analysis["layout_score"] = min(100, total_elements * 5)
            
            print(f"✅ Layout analysis complete:")
            print(f"   Buttons: {len(analysis['buttons'])}")
            print(f"   Form fields: {len(analysis['form_fields'])}")
            print(f"   Complexity: {analysis['complexity']}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Layout analysis failed: {e}")
            return analysis

# Example usage
if __name__ == "__main__":
    finder = VisualFinder()
    
    # Test with a screenshot (if available)
    test_screenshot = "test_screenshot.png"
    
    if os.path.exists(test_screenshot):
        # Test text finding
        result = finder.find_text_element(test_screenshot, "Search")
        print(f"Text search result: {result}")
        
        # Test layout analysis
        layout = finder.analyze_page_layout(test_screenshot)
        print(f"Layout analysis: {layout}")
    else:
        print("📷 No test screenshot available for vision testing")
