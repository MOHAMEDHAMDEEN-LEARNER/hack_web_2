"""
Video Recording and Screenshot Utilities for Test Suite
=======================================================

This module provides video recording and screenshot capabilities
for browser tests using Playwright's built-in functionality.
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoRecorder:
    """Handle video recording for test execution using Playwright's built-in video recording"""
    
    def __init__(self, output_dir: str = "reports/videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.recording_path = None
        self.start_time = None
    
    def start_recording(self, page, test_name: str = None):
        """Start video recording for a page"""
        if test_name is None:
            test_name = f"test_{int(time.time())}"
        
        # Clean test name for filename
        clean_name = "".join(c for c in test_name if c.isalnum() or c in "_-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.recording_path = self.output_dir / f"{clean_name}_{timestamp}.webm"
        self.start_time = time.time()
        
        logger.info(f"Video recording prepared: {self.recording_path}")
    
    def stop_recording(self, page, save_path: str = None):
        """Stop video recording and save file"""
        if self.recording_path is None:
            return None
        
        try:
            # Try to get video from page context
            video_path = None
            
            # Check if page has video recording capability
            if hasattr(page, 'video') and page.video:
                try:
                    video_path = page.video.path()
                except:
                    pass
            
            # Alternative: check context for video
            if not video_path and hasattr(page, 'context'):
                try:
                    # For browser context with video recording enabled
                    if hasattr(page.context, '_video_dir'):
                        video_files = list(Path(page.context._video_dir).glob("*.webm"))
                        if video_files:
                            video_path = str(video_files[-1])  # Get latest video
                except:
                    pass
            
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
                logger.info("Video recording not available - check if video recording is enabled in browser context")
                return None
                
        except Exception as e:
            logger.error(f"Error saving video recording: {e}")
            return None
        finally:
            self.recording_path = None
            self.start_time = None

class ScreenshotManager:
    """Manage screenshot capture during tests"""
    
    def __init__(self, output_dir: str = "reports/screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(self, page, name: str = None, full_page: bool = True):
        """Take a screenshot of the current page"""
        if name is None:
            name = f"screenshot_{int(time.time())}"
        
        # Clean name for filename
        clean_name = "".join(c for c in name if c.isalnum() or c in "_-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        screenshot_path = self.output_dir / f"{clean_name}_{timestamp}.png"
        
        try:
            page.screenshot(
                path=str(screenshot_path),
                full_page=full_page
            )
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    def take_element_screenshot(self, page, selector: str, name: str = None):
        """Take a screenshot of a specific element"""
        if name is None:
            name = f"element_{selector.replace('#', '').replace('.', '').replace(' ', '_')}"
        
        clean_name = "".join(c for c in name if c.isalnum() or c in "_-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        screenshot_path = self.output_dir / f"{clean_name}_{timestamp}.png"
        
        try:
            element = page.locator(selector).first
            if element.is_visible():
                element.screenshot(path=str(screenshot_path))
                logger.info(f"Element screenshot saved: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning(f"Element {selector} not visible for screenshot")
                return None
                
        except Exception as e:
            logger.error(f"Error taking element screenshot: {e}")
            return None

class TestMediaCapture:
    """Combined video and screenshot capture for tests"""
    
    def __init__(self, base_output_dir: str = "reports"):
        self.base_dir = Path(base_output_dir)
        self.video_recorder = VideoRecorder(str(self.base_dir / "videos"))
        self.screenshot_manager = ScreenshotManager(str(self.base_dir / "screenshots"))
        self.test_artifacts = {}
    
    def start_test_capture(self, page, test_name: str):
        """Start capturing video and take initial screenshot"""
        artifacts = {
            'test_name': test_name,
            'start_time': datetime.now(),
            'video_path': None,
            'screenshots': [],
            'start_screenshot': None
        }
        
        # Start video recording
        self.video_recorder.start_recording(page, test_name)
        
        # Take initial screenshot
        start_screenshot = self.screenshot_manager.take_screenshot(
            page, f"{test_name}_start"
        )
        artifacts['start_screenshot'] = start_screenshot
        
        self.test_artifacts[test_name] = artifacts
        logger.info(f"Started media capture for test: {test_name}")
        
        return artifacts
    
    def capture_step(self, page, test_name: str, step_name: str):
        """Capture screenshot for a specific test step"""
        if test_name not in self.test_artifacts:
            logger.warning(f"No media capture started for test: {test_name}")
            return None
        
        screenshot_path = self.screenshot_manager.take_screenshot(
            page, f"{test_name}_{step_name}"
        )
        
        if screenshot_path:
            self.test_artifacts[test_name]['screenshots'].append({
                'step': step_name,
                'path': screenshot_path,
                'timestamp': datetime.now()
            })
        
        return screenshot_path
    
    def capture_error(self, page, test_name: str, error_info: str = "error"):
        """Capture screenshot and video when test fails"""
        if test_name not in self.test_artifacts:
            logger.warning(f"No media capture started for test: {test_name}")
            return {}
        
        # Take error screenshot
        error_screenshot = self.screenshot_manager.take_screenshot(
            page, f"{test_name}_error_{error_info}"
        )
        
        # Stop video recording
        video_path = self.video_recorder.stop_recording(page)
        
        artifacts = self.test_artifacts[test_name]
        artifacts['error_screenshot'] = error_screenshot
        artifacts['video_path'] = video_path
        artifacts['end_time'] = datetime.now()
        
        logger.info(f"Captured error media for test: {test_name}")
        
        return {
            'error_screenshot': error_screenshot,
            'video_path': video_path
        }
    
    def finish_test_capture(self, page, test_name: str, success: bool = True):
        """Finish capturing and save final artifacts"""
        if test_name not in self.test_artifacts:
            logger.warning(f"No media capture started for test: {test_name}")
            return {}
        
        # Take final screenshot
        final_screenshot = self.screenshot_manager.take_screenshot(
            page, f"{test_name}_final"
        )
        
        # Stop video recording
        video_path = self.video_recorder.stop_recording(page)
        
        artifacts = self.test_artifacts[test_name]
        artifacts['final_screenshot'] = final_screenshot
        artifacts['video_path'] = video_path
        artifacts['end_time'] = datetime.now()
        artifacts['success'] = success
        
        if final_screenshot:
            artifacts['screenshots'].append({
                'step': 'final',
                'path': final_screenshot,
                'timestamp': datetime.now()
            })
        
        duration = (artifacts['end_time'] - artifacts['start_time']).total_seconds()
        artifacts['duration'] = duration
        
        logger.info(f"Finished media capture for test: {test_name} (Duration: {duration:.1f}s)")
        
        return artifacts
    
    def get_test_artifacts(self, test_name: str = None):
        """Get artifacts for a specific test or all tests"""
        if test_name:
            return self.test_artifacts.get(test_name, {})
        return self.test_artifacts
    
    def cleanup_old_artifacts(self, days_old: int = 7):
        """Clean up old video and screenshot files"""
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        cleaned_count = 0
        
        # Clean videos
        for video_file in self.video_recorder.output_dir.glob("*.webm"):
            if video_file.stat().st_mtime < cutoff_time:
                video_file.unlink()
                cleaned_count += 1
        
        # Clean screenshots
        for screenshot_file in self.screenshot_manager.output_dir.glob("*.png"):
            if screenshot_file.stat().st_mtime < cutoff_time:
                screenshot_file.unlink()
                cleaned_count += 1
        
        logger.info(f"Cleaned up {cleaned_count} old media files")
        return cleaned_count
