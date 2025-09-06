"""
Video Recording and Visual Testing Utilities
=============================================

This module provides comprehensive video recording and screenshot
capabilities for browser tests to capture execution for debugging.
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page

logger = logging.getLogger(__name__)

class VideoRecorder:
    """Handle video recording for test execution using Playwright's built-in video recording"""
    
    def __init__(self, output_dir: str = "reports/videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.recording_path = None
        self.start_time = None
    
    def start_recording(self, page: Page, test_name: str = None):
        """Start video recording for a page"""
        if test_name is None:
            test_name = f"test_{int(time.time())}"
        
        # Clean test name for filename
        clean_name = "".join(c for c in test_name if c.isalnum() or c in "_-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.recording_path = self.output_dir / f"{clean_name}_{timestamp}.webm"
        
        try:
            self.start_time = time.time()
            logger.info(f"Started video recording: {self.recording_path}")
            
        except Exception as e:
            logger.warning(f"Could not start video recording: {e}")
            self.recording_path = None
    
    def stop_recording(self, page: Page, save_path: str = None):
        """Stop video recording and save file"""
        if self.recording_path is None:
            return None
        
        try:
            # Get video path from page context
            video_path = None
            if hasattr(page.context, 'video_path'):
                video_path = page.context.video_path()
            elif hasattr(page, 'video') and page.video:
                video_path = page.video.path()
            
            if video_path and os.path.exists(video_path):
                # Move to our desired location
                final_path = save_path or self.recording_path
                final_path.parent.mkdir(parents=True, exist_ok=True)
                
                import shutil
                shutil.move(video_path, final_path)
                
                duration = time.time() - self.start_time if self.start_time else 0
                logger.info(f"Video recording saved: {final_path} (Duration: {duration:.1f}s)")
                
                return str(final_path)
            else:
                logger.warning("Video recording failed - no video file found")
                return None
                
        except Exception as e:
            logger.error(f"Error saving video recording: {e}")
            return None
        finally:
            self.recording_path = None
            self.start_time = None
            fps,
            (self.width, self.height)
        )
        
        logger.info(f"Started video recording: {self.video_path}")
    
    def capture_frame(self):
        """Capture current frame"""
        if not self.is_recording or not self.page:
            return
        
        try:
            # Take screenshot as bytes
            screenshot_bytes = self.page.screenshot()
            
            # Convert to OpenCV format
            image = Image.open(io.BytesIO(screenshot_bytes))
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Write frame to video
            if self.video_writer:
                self.video_writer.write(frame)
            
        except Exception as e:
            logger.warning(f"Failed to capture frame: {e}")
    
    def stop_recording(self):
        """Stop video recording"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        logger.info(f"Video recording saved: {self.video_path}")
        return str(self.video_path)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_recording()

class ScreenshotComparator:
    """Compare screenshots for visual regression testing"""
    
    def __init__(self):
        self.config = TestConfig()
        self.baseline_dir = Path(self.config.SCREENSHOTS_DIR) / "baseline"
        self.comparison_dir = Path(self.config.SCREENSHOTS_DIR) / "comparison"
        self.diff_dir = Path(self.config.SCREENSHOTS_DIR) / "diff"
        
        # Create directories
        for dir_path in [self.baseline_dir, self.comparison_dir, self.diff_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_baseline(self, page: Page, name: str):
        """Save a baseline screenshot"""
        filepath = self.baseline_dir / f"{name}.png"
        page.screenshot(path=str(filepath), full_page=True)
        logger.info(f"Baseline screenshot saved: {filepath}")
        return str(filepath)
    
    def compare_with_baseline(self, page: Page, name: str, threshold: float = 0.95):
        """Compare current page with baseline screenshot"""
        baseline_path = self.baseline_dir / f"{name}.png"
        
        if not baseline_path.exists():
            logger.warning(f"No baseline found for {name}, creating new baseline")
            return self.save_baseline(page, name)
        
        # Take current screenshot
        current_path = self.comparison_dir / f"{name}_current.png"
        page.screenshot(path=str(current_path), full_page=True)
        
        # Compare images
        similarity = self._calculate_similarity(baseline_path, current_path)
        
        result = {
            'name': name,
            'similarity': similarity,
            'passed': similarity >= threshold,
            'baseline_path': str(baseline_path),
            'current_path': str(current_path),
            'threshold': threshold
        }
        
        if not result['passed']:
            # Generate diff image
            diff_path = self._generate_diff_image(baseline_path, current_path, name)
            result['diff_path'] = diff_path
            logger.warning(f"Visual regression detected for {name}: {similarity:.2%} similarity")
        else:
            logger.info(f"Visual comparison passed for {name}: {similarity:.2%} similarity")
        
        return result
    
    def _calculate_similarity(self, img1_path: Path, img2_path: Path) -> float:
        """Calculate similarity between two images"""
        try:
            from skimage.metrics import structural_similarity as ssim
            import numpy as np
            
            # Load images
            img1 = cv2.imread(str(img1_path), cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(str(img2_path), cv2.IMREAD_GRAYSCALE)
            
            # Resize images to same size if needed
            if img1.shape != img2.shape:
                height = min(img1.shape[0], img2.shape[0])
                width = min(img1.shape[1], img2.shape[1])
                img1 = cv2.resize(img1, (width, height))
                img2 = cv2.resize(img2, (width, height))
            
            # Calculate SSIM
            similarity, _ = ssim(img1, img2, full=True)
            return float(similarity)
            
        except ImportError:
            # Fallback to simple pixel comparison
            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)
            
            # Resize to same size
            size = (min(img1.width, img2.width), min(img1.height, img2.height))
            img1 = img1.resize(size)
            img2 = img2.resize(size)
            
            # Convert to numpy arrays
            arr1 = np.array(img1)
            arr2 = np.array(img2)
            
            # Calculate pixel-wise similarity
            diff = np.abs(arr1 - arr2)
            similarity = 1 - (diff.mean() / 255)
            
            return float(similarity)
    
    def _generate_diff_image(self, baseline_path: Path, current_path: Path, name: str) -> str:
        """Generate difference image highlighting changes"""
        try:
            # Load images
            img1 = cv2.imread(str(baseline_path))
            img2 = cv2.imread(str(current_path))
            
            # Resize to same size
            height = min(img1.shape[0], img2.shape[0])
            width = min(img1.shape[1], img2.shape[1])
            img1 = cv2.resize(img1, (width, height))
            img2 = cv2.resize(img2, (width, height))
            
            # Calculate difference
            diff = cv2.absdiff(img1, img2)
            
            # Threshold to highlight significant differences
            _, thresh = cv2.threshold(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY), 30, 255, cv2.THRESH_BINARY)
            
            # Create colored diff image
            diff_colored = img2.copy()
            diff_colored[thresh == 255] = [0, 0, 255]  # Red for differences
            
            # Save diff image
            diff_path = self.diff_dir / f"{name}_diff.png"
            cv2.imwrite(str(diff_path), diff_colored)
            
            return str(diff_path)
            
        except Exception as e:
            logger.error(f"Failed to generate diff image: {e}")
            return None

class TestAnnotator:
    """Add annotations to screenshots for better documentation"""
    
    @staticmethod
    def annotate_screenshot(image_path: str, annotations: list, output_path: str = None):
        """Add annotations to a screenshot"""
        if not output_path:
            output_path = image_path.replace('.png', '_annotated.png')
        
        try:
            # Load image
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Add annotations
            for annotation in annotations:
                x, y = annotation.get('position', (10, 10))
                text = annotation.get('text', '')
                color = annotation.get('color', 'red')
                
                # Draw text with background
                text_bbox = draw.textbbox((x, y), text, font=font)
                draw.rectangle(text_bbox, fill='white', outline=color)
                draw.text((x, y), text, fill=color, font=font)
                
                # Draw arrow if target position is specified
                if 'target' in annotation:
                    target_x, target_y = annotation['target']
                    draw.line([(x, y), (target_x, target_y)], fill=color, width=2)
                    # Draw arrow head
                    arrow_size = 5
                    draw.polygon([
                        (target_x, target_y),
                        (target_x - arrow_size, target_y - arrow_size),
                        (target_x - arrow_size, target_y + arrow_size)
                    ], fill=color)
            
            # Save annotated image
            image.save(output_path)
            logger.info(f"Annotated screenshot saved: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to annotate screenshot: {e}")
            return image_path

class VisualTestReporter:
    """Generate visual test reports with screenshots and videos"""
    
    def __init__(self):
        self.config = TestConfig()
        self.test_results = []
        self.screenshots = []
        self.videos = []
    
    def add_test_result(self, test_name: str, status: str, screenshot_path: str = None, 
                       video_path: str = None, error_message: str = None):
        """Add test result to report"""
        result = {
            'name': test_name,
            'status': status,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'screenshot': screenshot_path,
            'video': video_path,
            'error': error_message
        }
        
        self.test_results.append(result)
        
        if screenshot_path:
            self.screenshots.append(screenshot_path)
        
        if video_path:
            self.videos.append(video_path)
    
    def generate_html_report(self, output_path: str = None):
        """Generate comprehensive HTML report"""
        if not output_path:
            output_path = Path(self.config.REPORTS_DIR) / "visual_test_report.html"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hackathon Website Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background: #2563eb; color: white; padding: 20px; border-radius: 5px; }
                .summary { background: #f8fafc; padding: 15px; margin: 20px 0; border-radius: 5px; }
                .test-result { border: 1px solid #e2e8f0; margin: 10px 0; padding: 15px; border-radius: 5px; }
                .test-passed { border-left: 5px solid #10b981; }
                .test-failed { border-left: 5px solid #ef4444; }
                .test-skipped { border-left: 5px solid #f59e0b; }
                .screenshot { max-width: 400px; margin: 10px 0; border: 1px solid #e2e8f0; }
                .video { margin: 10px 0; }
                .error { background: #fef2f2; color: #dc2626; padding: 10px; border-radius: 3px; margin: 5px 0; }
                .stats { display: flex; gap: 20px; }
                .stat-item { text-align: center; }
                .stat-number { font-size: 2em; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏆 Hackathon Website Test Report</h1>
                <p>Comprehensive test results with visual documentation</p>
            </div>
            
            <div class="summary">
                <h2>Test Summary</h2>
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number" style="color: #10b981;">{passed_count}</div>
                        <div>Passed</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" style="color: #ef4444;">{failed_count}</div>
                        <div>Failed</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" style="color: #f59e0b;">{skipped_count}</div>
                        <div>Skipped</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" style="color: #2563eb;">{total_count}</div>
                        <div>Total</div>
                    </div>
                </div>
                <p><strong>Success Rate:</strong> {success_rate}%</p>
                <p><strong>Generated:</strong> {timestamp}</p>
            </div>
            
            <div class="test-results">
                <h2>Test Results</h2>
                {test_results_html}
            </div>
        </body>
        </html>
        """
        
        # Calculate statistics
        passed_count = sum(1 for r in self.test_results if r['status'] == 'passed')
        failed_count = sum(1 for r in self.test_results if r['status'] == 'failed')
        skipped_count = sum(1 for r in self.test_results if r['status'] == 'skipped')
        total_count = len(self.test_results)
        success_rate = (passed_count / total_count * 100) if total_count > 0 else 0
        
        # Generate test results HTML
        test_results_html = ""
        for result in self.test_results:
            status_class = f"test-{result['status']}"
            
            result_html = f"""
            <div class="test-result {status_class}">
                <h3>{result['name']}</h3>
                <p><strong>Status:</strong> {result['status'].upper()}</p>
                <p><strong>Time:</strong> {result['timestamp']}</p>
                
                {f'<div class="error">{result["error"]}</div>' if result.get('error') else ''}
                
                {f'<img src="{result["screenshot"]}" class="screenshot" alt="Screenshot">' if result.get('screenshot') else ''}
                
                {f'<video controls class="video" width="400"><source src="{result["video"]}" type="video/mp4"></video>' if result.get('video') else ''}
            </div>
            """
            test_results_html += result_html
        
        # Generate final HTML
        html_content = html_template.format(
            passed_count=passed_count,
            failed_count=failed_count,
            skipped_count=skipped_count,
            total_count=total_count,
            success_rate=f"{success_rate:.1f}",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            test_results_html=test_results_html
        )
        
        # Save report
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Visual test report generated: {output_path}")
        return str(output_path)

# Import required modules for image processing
try:
    import numpy as np
    import io
except ImportError:
    logger.warning("NumPy or other optional dependencies not available for advanced image processing")

# Export classes
__all__ = ['VideoRecorder', 'ScreenshotComparator', 'TestAnnotator', 'VisualTestReporter']
