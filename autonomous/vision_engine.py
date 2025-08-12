"""
Chotu Vision Engine - Advanced Computer Vision and Screen Understanding
Implements OpenCV + PyAutoGUI for autonomous task execution
"""
import cv2
import numpy as np
import pyautogui
import mss
import time
import json
import os
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from pathlib import Path

# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

@dataclass
class ElementSignature:
    """Visual fingerprint of a UI element"""
    name: str
    template_path: str
    confidence: float
    relative_position: Optional[Tuple[int, int]] = None
    size: Optional[Tuple[int, int]] = None
    color_profile: Optional[List[int]] = None
    text_content: Optional[str] = None

@dataclass
class ScreenRegion:
    """Defines a region of the screen for targeted analysis"""
    x: int
    y: int
    width: int
    height: int
    name: str = ""

class VisionEngine:
    """Advanced computer vision engine for autonomous task execution"""
    
    def __init__(self, screenshots_dir: str = "autonomous/screenshots"):
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.templates_dir = Path("autonomous/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Screen capture settings
        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.sct = mss.mss()
        
        # Vision settings
        self.default_confidence = 0.8
        self.template_match_methods = [
            cv2.TM_CCOEFF_NORMED,
            cv2.TM_CCORR_NORMED,
            cv2.TM_SQDIFF_NORMED
        ]
        
        # Element signatures database
        self.element_signatures: Dict[str, ElementSignature] = {}
        self.load_element_signatures()
        
        # Screen state history
        self.screen_history: List[Dict] = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def capture_screen(self, region: Optional[ScreenRegion] = None) -> np.ndarray:
        """Capture current screen or specific region"""
        try:
            if region:
                monitor = {
                    'top': region.y, 
                    'left': region.x, 
                    'width': region.width, 
                    'height': region.height
                }
            else:
                monitor = self.monitor
            
            screenshot = self.sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Save screenshot for debugging
            timestamp = int(time.time())
            cv2.imwrite(str(self.screenshots_dir / f"screen_{timestamp}.png"), img)
            
            return img
        except Exception as e:
            self.logger.error(f"Screen capture failed: {e}")
            return None
    
    def detect_element(self, element_name: str, confidence: Optional[float] = None) -> Optional[Tuple[int, int, int, int]]:
        """Detect UI element using multiple vision techniques"""
        if element_name not in self.element_signatures:
            self.logger.warning(f"Element signature not found: {element_name}")
            return None
        
        signature = self.element_signatures[element_name]
        confidence = confidence or signature.confidence or self.default_confidence
        
        # Capture current screen
        screen = self.capture_screen()
        if screen is None:
            return None
        
        # Try template matching
        result = self._template_match(screen, signature.template_path, confidence)
        if result:
            return result
        
        # Try color-based detection
        if signature.color_profile:
            result = self._color_detection(screen, signature.color_profile, confidence)
            if result:
                return result
        
        # Try text-based detection (OCR)
        if signature.text_content:
            result = self._text_detection(screen, signature.text_content, confidence)
            if result:
                return result
        
        return None
    
    def _template_match(self, screen: np.ndarray, template_path: str, confidence: float) -> Optional[Tuple[int, int, int, int]]:
        """Template matching using OpenCV"""
        try:
            template_full_path = self.templates_dir / template_path
            if not template_full_path.exists():
                self.logger.warning(f"Template not found: {template_full_path}")
                return None
            
            template = cv2.imread(str(template_full_path), cv2.IMREAD_COLOR)
            if template is None:
                return None
            
            h, w = template.shape[:2]
            
            for method in self.template_match_methods:
                result = cv2.matchTemplate(screen, template, method)
                
                if method == cv2.TM_SQDIFF_NORMED:
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if min_val < (1 - confidence):
                        top_left = min_loc
                        return (top_left[0], top_left[1], w, h)
                else:
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > confidence:
                        top_left = max_loc
                        return (top_left[0], top_left[1], w, h)
            
            return None
        except Exception as e:
            self.logger.error(f"Template matching failed: {e}")
            return None
    
    def _color_detection(self, screen: np.ndarray, color_profile: List[int], confidence: float) -> Optional[Tuple[int, int, int, int]]:
        """Color-based element detection"""
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            
            # Create color range
            lower_bound = np.array([max(0, c - 10) for c in color_profile[:3]])
            upper_bound = np.array([min(255, c + 10) for c in color_profile[:3]])
            
            # Create mask
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Check if area is significant enough
                total_pixels = screen.shape[0] * screen.shape[1]
                contour_area = cv2.contourArea(largest_contour)
                
                if contour_area / total_pixels > 0.001:  # At least 0.1% of screen
                    return (x, y, w, h)
            
            return None
        except Exception as e:
            self.logger.error(f"Color detection failed: {e}")
            return None
    
    def _text_detection(self, screen: np.ndarray, text_content: str, confidence: float) -> Optional[Tuple[int, int, int, int]]:
        """Text-based detection using OCR (placeholder for now)"""
        # This would integrate with OCR libraries like pytesseract
        # For now, return None and rely on other detection methods
        return None
    
    def wait_for_element(self, element_name: str, timeout: int = 30, confidence: float = None) -> Optional[Tuple[int, int, int, int]]:
        """Wait for element to appear on screen"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.detect_element(element_name, confidence)
            if result:
                return result
            time.sleep(0.5)
        
        self.logger.warning(f"Element '{element_name}' not found within {timeout} seconds")
        return None
    
    def verify_screen_state(self, expected_elements: List[str], confidence: float = None) -> bool:
        """Verify that expected elements are present on screen"""
        for element in expected_elements:
            if not self.detect_element(element, confidence):
                return False
        return True
    
    def capture_element_template(self, element_name: str, region: ScreenRegion) -> bool:
        """Capture a template for future element recognition"""
        try:
            screen = self.capture_screen()
            if screen is None:
                return False
            
            # Extract region
            template = screen[region.y:region.y + region.height, 
                            region.x:region.x + region.width]
            
            # Save template
            template_path = f"{element_name}.png"
            full_path = self.templates_dir / template_path
            cv2.imwrite(str(full_path), template)
            
            # Create signature
            signature = ElementSignature(
                name=element_name,
                template_path=template_path,
                confidence=self.default_confidence,
                relative_position=(region.x, region.y),
                size=(region.width, region.height)
            )
            
            self.element_signatures[element_name] = signature
            self.save_element_signatures()
            
            self.logger.info(f"Template captured for element: {element_name}")
            return True
        except Exception as e:
            self.logger.error(f"Template capture failed: {e}")
            return False
    
    def get_element_center(self, element_bounds: Tuple[int, int, int, int]) -> Tuple[int, int]:
        """Get center coordinates of element"""
        x, y, w, h = element_bounds
        return (x + w // 2, y + h // 2)
    
    def save_element_signatures(self):
        """Save element signatures to disk"""
        signatures_file = self.templates_dir / "signatures.json"
        signatures_data = {}
        
        for name, signature in self.element_signatures.items():
            signatures_data[name] = {
                'name': signature.name,
                'template_path': signature.template_path,
                'confidence': signature.confidence,
                'relative_position': signature.relative_position,
                'size': signature.size,
                'color_profile': signature.color_profile,
                'text_content': signature.text_content
            }
        
        with open(signatures_file, 'w') as f:
            json.dump(signatures_data, f, indent=2)
    
    def load_element_signatures(self):
        """Load element signatures from disk"""
        signatures_file = self.templates_dir / "signatures.json"
        if not signatures_file.exists():
            return
        
        try:
            with open(signatures_file, 'r') as f:
                signatures_data = json.load(f)
            
            for name, data in signatures_data.items():
                signature = ElementSignature(
                    name=data['name'],
                    template_path=data['template_path'],
                    confidence=data['confidence'],
                    relative_position=tuple(data['relative_position']) if data['relative_position'] else None,
                    size=tuple(data['size']) if data['size'] else None,
                    color_profile=data['color_profile'],
                    text_content=data['text_content']
                )
                self.element_signatures[name] = signature
        except Exception as e:
            self.logger.error(f"Failed to load element signatures: {e}")
    
    def analyze_screen_changes(self, baseline_image: np.ndarray, current_image: np.ndarray) -> Dict[str, Any]:
        """Analyze changes between two screen states"""
        try:
            # Convert to grayscale for comparison
            baseline_gray = cv2.cvtColor(baseline_image, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate difference
            diff = cv2.absdiff(baseline_gray, current_gray)
            
            # Threshold the difference
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            
            # Find contours of changes
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            changes = []
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter small changes
                    x, y, w, h = cv2.boundingRect(contour)
                    changes.append({
                        'region': (x, y, w, h),
                        'area': cv2.contourArea(contour)
                    })
            
            return {
                'changes_detected': len(changes) > 0,
                'change_regions': changes,
                'total_change_area': sum(c['area'] for c in changes)
            }
        except Exception as e:
            self.logger.error(f"Screen change analysis failed: {e}")
            return {'changes_detected': False, 'change_regions': [], 'total_change_area': 0}
    
    def get_dominant_colors(self, image: np.ndarray, k: int = 5) -> List[List[int]]:
        """Extract dominant colors from image using K-means clustering"""
        try:
            # Reshape image to 2D array of pixels
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            # Apply K-means clustering
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert back to uint8
            centers = np.uint8(centers)
            
            return centers.tolist()
        except Exception as e:
            self.logger.error(f"Color extraction failed: {e}")
            return []
