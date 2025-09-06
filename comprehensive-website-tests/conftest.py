"""
Pytest configuration and fixtures for comprehensive test suite
============================================================
"""

import pytest
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Playwright, Browser, Page
from utils.test_data import TestConfig
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper
from utils.api_helper import APIHelper

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
    
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for different types of reports
    (reports_dir / "screenshots").mkdir(exist_ok=True)
    (reports_dir / "videos").mkdir(exist_ok=True)
    (reports_dir / "html").mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration"""
    return TestConfig()

@pytest.fixture
def config(test_config):
    """Alias for test_config for easier access"""
    return test_config

@pytest.fixture
def browser_helper(page, context):
    """Provide browser helper"""
    return BrowserHelper(page, context)

@pytest.fixture  
def form_helper(browser_helper):
    """Provide form helper"""
    return FormHelper(browser_helper)

@pytest.fixture
def validation_helper(browser_helper):
    """Provide validation helper"""
    return ValidationHelper(browser_helper)

@pytest.fixture
def api_helper():
    """Provide API helper"""
    return APIHelper()

@pytest.fixture(autouse=True)
def test_setup_teardown(request, page):
    """Setup and teardown for each test with screenshot capture"""
    test_name = request.node.name
    test_start_time = datetime.now()
    
    logger.info(f"Starting test: {test_name}")
    
    # Take screenshot at start of test
    try:
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        start_screenshot = screenshots_dir / f"{test_name}_start.png"
        page.screenshot(path=str(start_screenshot))
        logger.info(f"Start screenshot: {start_screenshot}")
    except Exception as e:
        logger.warning(f"Could not take start screenshot: {e}")
    
    yield
    
    # Teardown
    test_end_time = datetime.now()
    test_duration = (test_end_time - test_start_time).total_seconds()
    
    # Take screenshot at end of test
    try:
        end_screenshot = screenshots_dir / f"{test_name}_end.png"
        page.screenshot(path=str(end_screenshot))
        logger.info(f"End screenshot: {end_screenshot}")
    except Exception as e:
        logger.warning(f"Could not take end screenshot: {e}")
    
    logger.info(f"Finished test: {test_name} (Duration: {test_duration:.2f}s)")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting"""
    outcome = yield
    rep = outcome.get_result()
    
    # Take screenshot on failure
    if rep.when == "call" and rep.failed:
        try:
            # Access the page fixture
            if 'page' in item.funcargs:
                page = item.funcargs['page']
                screenshots_dir = Path("reports/screenshots")
                screenshots_dir.mkdir(exist_ok=True)
                
                failure_screenshot = screenshots_dir / f"{item.name}_failure.png"
                page.screenshot(path=str(failure_screenshot))
                logger.info(f"Failure screenshot: {failure_screenshot}")
        except Exception as e:
            logger.warning(f"Could not take failure screenshot: {e}")

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
