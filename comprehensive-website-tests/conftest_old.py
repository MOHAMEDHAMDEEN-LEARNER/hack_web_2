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
        artifacts = media_capture.start_test_capture(page, test_name)
    
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
    test_passed = not request.node.rep_call.failed if hasattr(request.node, 'rep_call') else True
    
    # Finish media capture
    if media_capture:
        try:
            if test_passed:
                media_capture.finish_test_capture(page, test_name, success=True)
            else:
                media_capture.capture_error(page, test_name, "test_failure")
        except Exception as e:
            logger.warning(f"Error in media capture teardown: {e}")
    
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
            if hasattr(item, '_request') and hasattr(item._request, 'test_info'):
                test_info = item._request.test_info
                if test_info.get('media_capture') and 'page' in item.funcargs:
                    page = item.funcargs['page']
                    test_info['media_capture'].capture_error(page, test_info['name'], "failure")
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

# Pytest plugins for enhanced reporting
pytest_plugins = [
    "pytest_html",
    "pytest_json_report",
]

import pytest
import logging
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.test_data import TestConfig
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper
from utils.api_helper import ComprehensiveAPIHelper
from utils.video_recorder import TestMediaCapture

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/logs/test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

@pytest.fixture(scope="session")
def config():
    """Test configuration fixture"""
    return TestConfig()

@pytest.fixture(scope="session")
def api_helper():
    """API helper fixture"""
    return ComprehensiveAPIHelper()

@pytest.fixture(scope="session")
def visual_reporter():
    """Visual test reporter fixture"""
    return VisualTestReporter()

@pytest.fixture(scope="session")
def playwright_instance():
    """Playwright instance fixture"""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    """Browser fixture"""
    browser = playwright_instance.chromium.launch(
        headless=config.HEADLESS,
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    yield browser
    browser.close()

@pytest.fixture
def context(browser, config):
    """Browser context fixture"""
    context = browser.new_context(
        viewport={'width': config.VIEWPORT_WIDTH, 'height': config.VIEWPORT_HEIGHT},
        record_video_dir='reports/videos' if not config.HEADLESS else None
    )
    yield context
    context.close()

@pytest.fixture  
def page(context):
    """Page fixture"""
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def browser_helper(page, context):
    """Browser helper fixture"""
    return BrowserHelper(page, context)

@pytest.fixture
def form_helper(browser_helper):
    """Form helper fixture"""
    return FormHelper(browser_helper)

@pytest.fixture
def validation_helper(browser_helper):
    """Validation helper fixture"""
    return ValidationHelper(browser_helper)

@pytest.fixture
def video_recorder(request):
    """Video recorder fixture"""
    test_name = request.node.name
    recorder = VideoRecorder(test_name)
    yield recorder
    recorder.stop_recording()

@pytest.fixture(autouse=True)
def setup_test_environment(browser_helper, visual_reporter, request):
    """Setup test environment for each test"""
    test_name = request.node.name
    
    # Take initial screenshot
    try:
        browser_helper.navigate_to("/")
        screenshot_path = browser_helper.take_screenshot(f"{test_name}_start")
    except:
        screenshot_path = None
    
    yield
    
    # Take final screenshot and record test result
    try:
        final_screenshot = browser_helper.take_screenshot(f"{test_name}_end")
        status = "passed" if not hasattr(request.node, 'rep_call') or request.node.rep_call.passed else "failed"
        error_message = str(request.node.rep_call.longrepr) if hasattr(request.node, 'rep_call') and request.node.rep_call.failed else None
        
        visual_reporter.add_test_result(
            test_name=test_name,
            status=status,
            screenshot_path=final_screenshot,
            error_message=error_message
        )
    except:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results for reporting"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def pytest_sessionfinish(session, exitstatus):
    """Generate final report after all tests complete"""
    try:
        # Get visual reporter from any test that used it
        for item in session.items:
            if hasattr(item, '_request'):
                try:
                    visual_reporter = item._request.getfixturevalue('visual_reporter')
                    report_path = visual_reporter.generate_html_report()
                    print(f"\n📊 Test report generated: {report_path}")
                    break
                except:
                    pass
    except:
        pass

# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    # Create report directories
    report_dirs = ['reports', 'reports/screenshots', 'reports/videos', 'reports/logs']
    for dir_path in report_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Add custom markers
    config.addinivalue_line(
        "markers", "auth: mark test as authentication related"
    )
    config.addinivalue_line(
        "markers", "registration: mark test as registration related"
    )
    config.addinivalue_line(
        "markers", "admin: mark test as admin functionality"
    )
    config.addinivalue_line(
        "markers", "applicant: mark test as applicant functionality"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI/frontend related"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API/backend related"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance related"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

# Custom pytest command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--video",
        action="store_true", 
        default=False,
        help="Record videos during test execution"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:3001",
        help="Base URL for testing"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use for testing"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Update config based on command line options
    if config.getoption("--headless"):
        TestConfig.HEADLESS = True
    
    if config.getoption("--base-url"):
        TestConfig.BASE_URL = config.getoption("--base-url")
    
    if config.getoption("--browser"):
        TestConfig.BROWSER_TYPE = config.getoption("--browser")
