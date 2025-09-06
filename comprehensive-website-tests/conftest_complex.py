"""
Pytest configuration and fixtures for comprehensive test suite
============================================================
"""

import pytest
import logging
import os
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Playwright, Browser, Page
from utils.test_data import TestConfig
from utils.video_recorder import TestMediaCapture

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def pytest_configure(config):
    """Configure pytest with custom markers and setup"""
    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "chromium: Tests for Chromium browser")
    config.addinivalue_line("markers", "firefox: Tests for Firefox browser")
    config.addinivalue_line("markers", "webkit: Tests for WebKit browser")
    
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for different types of reports
    (reports_dir / "screenshots").mkdir(exist_ok=True)
    (reports_dir / "videos").mkdir(exist_ok=True)
    (reports_dir / "html").mkdir(exist_ok=True)

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run in headless mode (true/false)"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to use (chromium/firefox/webkit)"
    )
    parser.addoption(
        "--record-video",
        action="store",
        default="on",
        help="Enable video recording (on/off/retain-on-failure)"
    )
    parser.addoption(
        "--capture-screenshots",
        action="store", 
        default="true",
        help="Enable screenshot capture (true/false)"
    )

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    return TestConfig()

@pytest.fixture(scope="session")
def browser_type_name(request):
    """Get browser type from command line"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def is_headless(request):
    """Get headless mode from command line"""
    return request.config.getoption("--headless").lower() == "true"

@pytest.fixture(scope="session")
def enable_video(request):
    """Get video recording setting from command line"""
    return request.config.getoption("--record-video") != "off"

@pytest.fixture(scope="session")
def enable_screenshots(request):
    """Get screenshot setting from command line"""
    return request.config.getoption("--capture-screenshots").lower() == "true"

@pytest.fixture(scope="session")
def playwright():
    """Create Playwright instance"""
    with Playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser_context_args(enable_video):
    """Browser context arguments with video recording if enabled"""
    context_args = {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
    
    if enable_video:
        # Enable video recording
        context_args["record_video_dir"] = "reports/videos"
        context_args["record_video_size"] = {"width": 1280, "height": 720}
    
    return context_args

@pytest.fixture(scope="session")
def browser(playwright, browser_type_name, is_headless):
    """Create browser instance"""
    browser_type = getattr(playwright, browser_type_name)
    browser = browser_type.launch(
        headless=is_headless,
        slow_mo=100 if not is_headless else 0,  # Slow down actions when not headless
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--disable-default-apps",
            "--disable-extensions",
        ]
    )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    """Create browser context for each test"""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create page for each test"""
    page = context.new_page()
    
    # Set longer timeouts for stability
    page.set_default_timeout(30000)  # 30 seconds
    page.set_default_navigation_timeout(60000)  # 60 seconds
    
    yield page
    page.close()

@pytest.fixture(scope="function")
def media_capture(enable_video, enable_screenshots):
    """Create media capture instance for video and screenshots"""
    if enable_video or enable_screenshots:
        capture = TestMediaCapture()
        yield capture
        # Cleanup handled by the capture instance
    else:
        yield None

@pytest.fixture(autouse=True)
def test_setup_teardown(request, page, media_capture):
    """Setup and teardown for each test with media capture"""
    test_name = request.node.name
    test_start_time = datetime.now()
    
    logger.info(f"Starting test: {test_name}")
    
    # Start media capture if enabled
    artifacts = None
    if media_capture:
        try:
            artifacts = media_capture.start_test_capture(page, test_name)
        except Exception as e:
            logger.warning(f"Could not start media capture: {e}")
    
    # Take basic screenshot if media capture is not available
    if not media_capture:
        try:
            screenshots_dir = Path("reports/screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            start_screenshot = screenshots_dir / f"{test_name}_start.png"
            page.screenshot(path=str(start_screenshot))
            logger.info(f"Basic screenshot: {start_screenshot}")
        except Exception as e:
            logger.warning(f"Could not take basic screenshot: {e}")
    
    # Provide test info to the test function
    test_info = {
        'name': test_name,
        'start_time': test_start_time,
        'artifacts': artifacts,
        'media_capture': media_capture
    }
    
    # Store in request for access in tests
    request.test_info = test_info
    
    yield test_info
    
    # Teardown
    test_end_time = datetime.now()
    test_duration = (test_end_time - test_start_time).total_seconds()
    
    # Determine if test passed
    test_passed = not hasattr(request.node, 'rep_call') or not request.node.rep_call.failed
    
    # Finish media capture
    if media_capture:
        try:
            if test_passed:
                media_capture.finish_test_capture(page, test_name, success=True)
            else:
                media_capture.capture_error(page, test_name, "test_failure")
        except Exception as e:
            logger.warning(f"Error in media capture teardown: {e}")
    
    # Take basic end screenshot if media capture is not available
    if not media_capture:
        try:
            end_screenshot = screenshots_dir / f"{test_name}_end.png"
            page.screenshot(path=str(end_screenshot))
            logger.info(f"Basic end screenshot: {end_screenshot}")
        except Exception as e:
            logger.warning(f"Could not take basic end screenshot: {e}")
    
    logger.info(f"Finished test: {test_name} - {'PASSED' if test_passed else 'FAILED'} (Duration: {test_duration:.2f}s)")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for media capture"""
    outcome = yield
    rep = outcome.get_result()
    
    # Store the result in the item for access in teardown
    setattr(item, f"rep_{rep.when}", rep)
    
    # Take screenshot on failure
    if rep.when == "call" and rep.failed:
        # Try to access page and media capture from the test
        try:
            if hasattr(item, '_request') and hasattr(item._request, 'test_info') and 'page' in item.funcargs:
                test_info = item._request.test_info
                page = item.funcargs['page']
                
                if test_info.get('media_capture'):
                    test_info['media_capture'].capture_error(page, test_info['name'], "failure")
                else:
                    # Basic failure screenshot
                    screenshots_dir = Path("reports/screenshots")
                    screenshots_dir.mkdir(exist_ok=True)
                    failure_screenshot = screenshots_dir / f"{test_info['name']}_failure.png"
                    page.screenshot(path=str(failure_screenshot))
                    logger.info(f"Failure screenshot: {failure_screenshot}")
        except Exception as e:
            logger.warning(f"Could not capture failure screenshot: {e}")

# Custom assertion helpers
def assert_element_visible(page, selector, timeout=10000):
    """Assert that an element is visible within timeout"""
    try:
        page.wait_for_selector(selector, timeout=timeout, state="visible")
        return True
    except Exception as e:
        logger.error(f"Element {selector} not visible: {e}")
        return False

def assert_element_text(page, selector, expected_text, timeout=10000):
    """Assert that an element contains expected text"""
    try:
        element = page.wait_for_selector(selector, timeout=timeout)
        actual_text = element.text_content()
        assert expected_text in actual_text, f"Expected '{expected_text}' in '{actual_text}'"
        return True
    except Exception as e:
        logger.error(f"Element text assertion failed: {e}")
        return False

def assert_url_contains(page, expected_url_part):
    """Assert that current URL contains expected part"""
    current_url = page.url
    assert expected_url_part in current_url, f"Expected '{expected_url_part}' in URL '{current_url}'"

# Pytest plugins for enhanced reporting (disabled for now)
# pytest_plugins = [
#     "pytest_html",
#     "pytest_json_report",
# ]
