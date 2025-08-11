#!/usr/bin/env python3
"""
🎯 CHOTU COMPUTER VISION TOOL
=============================
Advanced computer vision capabilities using OpenCV for Chotu AI Assistant
"""

import cv2
import numpy as np
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def take_smart_screenshot(filename: Optional[str] = None, analyze: bool = True) -> str:
    """Take screenshot with optional OpenCV analysis"""
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Take screenshot using macOS screencapture
        result = subprocess.run(['screencapture', '-x', filename], capture_output=True)
        
        if result.returncode != 0:
            return "❌ Failed to take screenshot"
        
        if not analyze:
            return f"✅ Screenshot saved as {filename}"
        
        # Analyze screenshot with OpenCV
        analysis = analyze_screenshot(filename)
        return f"✅ Screenshot saved as {filename}\n📊 Analysis: {analysis}"
        
    except Exception as e:
        return f"❌ Screenshot error: {str(e)}"

def analyze_screenshot(image_path: str) -> str:
    """Analyze screenshot using OpenCV computer vision"""
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            return "Could not read image"
        
        height, width, channels = image.shape
        
        # Convert to different color spaces for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Analyze image properties
        analysis = {}
        
        # Basic properties
        analysis['resolution'] = f"{width}x{height}"
        analysis['channels'] = channels
        
        # Brightness analysis
        brightness = np.mean(gray)
        if brightness < 85:
            brightness_level = "Dark"
        elif brightness < 170:
            brightness_level = "Medium"
        else:
            brightness_level = "Bright"
        analysis['brightness'] = f"{brightness_level} ({brightness:.1f})"
        
        # Color analysis
        dominant_colors = get_dominant_colors(image)
        analysis['dominant_colors'] = dominant_colors
        
        # Edge detection for content density
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (width * height) * 100
        analysis['content_density'] = f"{edge_density:.1f}%"
        
        # Text region detection (approximate)
        text_regions = detect_text_regions(gray)
        analysis['text_regions'] = len(text_regions)
        
        # UI element detection
        ui_elements = detect_ui_elements(gray)
        analysis['ui_elements'] = ui_elements
        
        # Format analysis results
        result_lines = []
        for key, value in analysis.items():
            result_lines.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return " | ".join(result_lines)
        
    except Exception as e:
        return f"Analysis error: {str(e)}"

def get_dominant_colors(image: np.ndarray, k: int = 3) -> str:
    """Extract dominant colors from image using K-means clustering"""
    try:
        # Reshape image to be a list of pixels
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        # Apply K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert back to uint8
        centers = np.uint8(centers)
        
        # Get color names
        color_names = []
        for center in centers:
            b, g, r = center
            color_name = get_color_name(r, g, b)
            color_names.append(color_name)
        
        return ", ".join(color_names[:3])
        
    except Exception as e:
        return "Unknown"

def get_color_name(r: int, g: int, b: int) -> str:
    """Get approximate color name from RGB values"""
    # Simple color name mapping
    if r > 200 and g > 200 and b > 200:
        return "White"
    elif r < 50 and g < 50 and b < 50:
        return "Black"
    elif r > g and r > b:
        return "Red" if r > 150 else "Dark Red"
    elif g > r and g > b:
        return "Green" if g > 150 else "Dark Green"
    elif b > r and b > g:
        return "Blue" if b > 150 else "Dark Blue"
    elif r > 150 and g > 150:
        return "Yellow"
    elif r > 150 and b > 150:
        return "Magenta"
    elif g > 150 and b > 150:
        return "Cyan"
    else:
        return "Gray"

def detect_text_regions(gray_image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """Detect potential text regions using MSER"""
    try:
        # Create MSER detector
        mser = cv2.MSER_create()
        
        # Detect regions
        regions, _ = mser.detectRegions(gray_image)
        
        # Convert regions to bounding boxes
        bboxes = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region)
            # Filter out very small or very large regions
            if 10 < w < gray_image.shape[1] // 3 and 5 < h < gray_image.shape[0] // 3:
                bboxes.append((x, y, w, h))
        
        return bboxes
        
    except Exception as e:
        return []

def detect_ui_elements(gray_image: np.ndarray) -> Dict[str, int]:
    """Detect UI elements like buttons, windows, etc."""
    try:
        ui_count = {}
        
        # Detect rectangles (potential buttons/windows)
        edges = cv2.Canny(gray_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangles = 0
        circles = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small contours
                # Approximate contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:  # Rectangle
                    rectangles += 1
                elif len(approx) > 8:  # Potential circle
                    circles += 1
        
        ui_count['buttons/windows'] = rectangles
        ui_count['circular_elements'] = circles
        
        return ui_count
        
    except Exception as e:
        return {'error': 1}

def find_element_in_screenshot(element_description: str, screenshot_path: Optional[str] = None) -> str:
    """Find UI elements in screenshot based on description"""
    try:
        # Take screenshot if not provided
        if not screenshot_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"temp_screenshot_{timestamp}.png"
            result = subprocess.run(['screencapture', '-x', screenshot_path], capture_output=True)
            if result.returncode != 0:
                return "❌ Failed to take screenshot"
        
        # Read screenshot
        image = cv2.imread(screenshot_path)
        if image is None:
            return "❌ Could not read screenshot"
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Simple element detection based on description
        results = []
        
        if "button" in element_description.lower():
            # Look for rectangular shapes
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            button_count = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if 500 < area < 10000:  # Button-sized areas
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    if len(approx) == 4:  # Rectangle
                        button_count += 1
            
            results.append(f"Found {button_count} potential buttons")
        
        if "text" in element_description.lower():
            # Detect text regions
            text_regions = detect_text_regions(gray)
            results.append(f"Found {len(text_regions)} text regions")
        
        if "red" in element_description.lower() or "green" in element_description.lower() or "blue" in element_description.lower():
            # Color-based detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            color_masks = detect_color_regions(hsv, element_description.lower())
            results.append(f"Found color regions matching description")
        
        # Clean up temporary screenshot
        if screenshot_path.startswith("temp_screenshot_"):
            try:
                os.remove(screenshot_path)
            except:
                pass
        
        return " | ".join(results) if results else "No matching elements found"
        
    except Exception as e:
        return f"❌ Element detection error: {str(e)}"

def detect_color_regions(hsv_image: np.ndarray, color_description: str) -> List[Tuple[int, int, int, int]]:
    """Detect regions of specific colors"""
    try:
        # Define color ranges in HSV
        color_ranges = {
            'red': [(0, 50, 50), (10, 255, 255)],
            'green': [(40, 50, 50), (80, 255, 255)],
            'blue': [(100, 50, 50), (130, 255, 255)],
            'yellow': [(20, 50, 50), (40, 255, 255)],
        }
        
        regions = []
        for color, (lower, upper) in color_ranges.items():
            if color in color_description:
                # Create mask
                mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 100:  # Filter small regions
                        x, y, w, h = cv2.boundingRect(contour)
                        regions.append((x, y, w, h))
        
        return regions
        
    except Exception as e:
        return []

def enhance_web_automation_with_vision(target_description: str) -> str:
    """Use computer vision to enhance web automation accuracy"""
    try:
        # Take screenshot of current state
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"web_automation_vision_{timestamp}.png"
        
        result = subprocess.run(['screencapture', '-x', screenshot_path], capture_output=True)
        if result.returncode != 0:
            return "❌ Could not capture screen for vision analysis"
        
        # Analyze screenshot for web elements
        image = cv2.imread(screenshot_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect potential clickable elements
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        clickable_elements = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 100 < area < 50000:  # Reasonable clickable size
                x, y, w, h = cv2.boundingRect(contour)
                # Check aspect ratio for button-like shapes
                aspect_ratio = w / h if h > 0 else 0
                if 0.3 < aspect_ratio < 5:  # Button-like aspect ratios
                    clickable_elements.append({
                        'x': x, 'y': y, 'width': w, 'height': h,
                        'center': (x + w//2, y + h//2),
                        'area': area
                    })
        
        # Analyze for YouTube-specific elements if target mentions YouTube
        if 'youtube' in target_description.lower() or 'video' in target_description.lower():
            youtube_analysis = analyze_youtube_page(gray)
            
            # Clean up screenshot
            try:
                os.remove(screenshot_path)
            except:
                pass
            
            return f"🎥 YouTube Page Analysis: {youtube_analysis} | Found {len(clickable_elements)} clickable elements"
        
        # Clean up screenshot
        try:
            os.remove(screenshot_path)
        except:
            pass
        
        return f"🎯 Vision Analysis: Found {len(clickable_elements)} potential clickable elements"
        
    except Exception as e:
        return f"❌ Vision enhancement error: {str(e)}"

def analyze_youtube_page(gray_image: np.ndarray) -> str:
    """Analyze screenshot specifically for YouTube elements"""
    try:
        analysis_results = []
        
        # Look for video thumbnails (rectangular regions)
        edges = cv2.Canny(gray_image, 30, 100)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        video_thumbnails = 0
        potential_ads = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Large enough for video thumbnail
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # Video thumbnails typically have 16:9 aspect ratio
                if 1.5 < aspect_ratio < 2.0:
                    video_thumbnails += 1
                
                # Small rectangular elements might be ads
                elif 2.0 < aspect_ratio < 4.0 and area < 5000:
                    potential_ads += 1
        
        analysis_results.append(f"Videos: {video_thumbnails}")
        analysis_results.append(f"Potential ads: {potential_ads}")
        
        # Look for text regions (titles, descriptions)
        text_regions = detect_text_regions(gray_image)
        analysis_results.append(f"Text regions: {len(text_regions)}")
        
        return " | ".join(analysis_results)
        
    except Exception as e:
        return "Analysis failed"

def create_element_map(screenshot_path: Optional[str] = None) -> str:
    """Create a map of all UI elements in the current screen"""
    try:
        # Take screenshot if not provided
        if not screenshot_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"element_map_{timestamp}.png"
            result = subprocess.run(['screencapture', '-x', screenshot_path], capture_output=True)
            if result.returncode != 0:
                return "❌ Failed to take screenshot"
        
        # Read and analyze screenshot
        image = cv2.imread(screenshot_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # Create element map
        element_map = {
            'total_elements': 0,
            'buttons': [],
            'text_regions': [],
            'clickable_areas': [],
            'screen_regions': {
                'top_left': (0, 0, width//2, height//2),
                'top_right': (width//2, 0, width//2, height//2),
                'bottom_left': (0, height//2, width//2, height//2),
                'bottom_right': (width//2, height//2, width//2, height//2)
            }
        }
        
        # Detect all elements
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Filter noise
                x, y, w, h = cv2.boundingRect(contour)
                element_info = {
                    'position': (x, y),
                    'size': (w, h),
                    'center': (x + w//2, y + h//2),
                    'area': area
                }
                
                # Classify element type
                aspect_ratio = w / h if h > 0 else 0
                if 0.5 < aspect_ratio < 3 and 500 < area < 10000:
                    element_map['buttons'].append(element_info)
                elif aspect_ratio > 3 and area > 100:
                    element_map['text_regions'].append(element_info)
                elif area > 100:
                    element_map['clickable_areas'].append(element_info)
        
        element_map['total_elements'] = len(element_map['buttons']) + len(element_map['text_regions']) + len(element_map['clickable_areas'])
        
        # Clean up if we created the screenshot
        if screenshot_path.startswith("element_map_"):
            try:
                os.remove(screenshot_path)
            except:
                pass
        
        # Format results
        results = []
        results.append(f"Total elements: {element_map['total_elements']}")
        results.append(f"Buttons: {len(element_map['buttons'])}")
        results.append(f"Text regions: {len(element_map['text_regions'])}")
        results.append(f"Other clickable: {len(element_map['clickable_areas'])}")
        
        return " | ".join(results)
        
    except Exception as e:
        return f"❌ Element mapping error: {str(e)}"

# Main functions for MCP integration
def take_screenshot_with_analysis(filename=None):
    """Main function for taking and analyzing screenshots"""
    return take_smart_screenshot(filename, analyze=True)

def analyze_current_screen():
    """Analyze current screen without saving screenshot"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = f"temp_analysis_{timestamp}.png"
    
    try:
        # Take temporary screenshot
        result = subprocess.run(['screencapture', '-x', temp_file], capture_output=True)
        if result.returncode != 0:
            return "❌ Failed to capture screen"
        
        # Analyze
        analysis = analyze_screenshot(temp_file)
        
        # Clean up
        try:
            os.remove(temp_file)
        except:
            pass
        
        return f"🖥️ Current Screen Analysis: {analysis}"
        
    except Exception as e:
        return f"❌ Screen analysis error: {str(e)}"

def find_ui_element(description):
    """Find UI element based on description"""
    return find_element_in_screenshot(description)

def get_element_map():
    """Get map of all UI elements on current screen"""
    return create_element_map()

def enhance_automation_with_vision(target):
    """Use computer vision to enhance automation accuracy"""
    return enhance_web_automation_with_vision(target)
