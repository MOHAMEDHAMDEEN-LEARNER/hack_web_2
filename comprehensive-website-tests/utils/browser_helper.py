"""
Browser Helper Utilities
========================
"""

import os
import time
import logging
from pathlib import Path
from playwright.sync_api import Page, BrowserContext, expect
from .test_data import TestConfig, UISelectors

logger = logging.getLogger(__name__)

class BrowserHelper:
    """Browser automation helper functions"""
    
    def __init__(self, page: Page, context: BrowserContext):
        self.page = page
        self.context = context
        self.config = TestConfig()
        
        # Set default timeout
        page.set_default_timeout(self.config.DEFAULT_TIMEOUT)
        
        # Create report directories
        self._create_report_dirs()
    
    def _create_report_dirs(self):
        """Create necessary report directories"""
        dirs = [
            self.config.REPORTS_DIR,
            self.config.SCREENSHOTS_DIR,
            self.config.VIDEOS_DIR,
            self.config.LOGS_DIR
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def navigate_to(self, path: str = "/", wait_for_load: bool = True):
        """Navigate to a specific path"""
        url = f"{self.config.BASE_URL}{path}"
        logger.info(f"Navigating to: {url}")
        
        self.page.goto(url)
        
        if wait_for_load:
            self.page.wait_for_load_state("networkidle")
    
    def take_screenshot(self, name: str, full_page: bool = True):
        """Take a screenshot with automatic naming"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = Path(self.config.SCREENSHOTS_DIR) / filename
        
        self.page.screenshot(path=str(filepath), full_page=full_page)
        logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    
    def wait_for_element(self, selector: str, timeout: int = None):
        """Wait for element to be visible"""
        timeout = timeout or self.config.DEFAULT_TIMEOUT
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def click(self, selector: str, timeout: int = None):
        """Click an element with wait"""
        element = self.wait_for_element(selector, timeout)
        element.click()
        logger.info(f"Clicked element: {selector}")
    
    def is_visible(self, selector: str, timeout: int = 1000):
        """Check if element is visible without throwing exception"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except:
            return False
    
    def wait_for_loading_to_complete(self, timeout: int = 30000):
        """Wait for page loading to complete"""
        try:
            # Wait for network idle
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            
            # Wait for any loading spinners to disappear
            spinner_selectors = [".animate-spin", ".loading", ".spinner", "[data-loading]"]
            for spinner in spinner_selectors:
                if self.is_visible(spinner, timeout=1000):
                    self.page.wait_for_selector(spinner, state="hidden", timeout=10000)
            
            logger.info("Page loading completed")
        except Exception as e:
            logger.warning(f"Loading wait timed out or failed: {e}")
    
    def scroll_to_element(self, selector: str):
        """Scroll element into view"""
        element = self.wait_for_element(selector)
        element.scroll_into_view_if_needed()
        logger.info(f"Scrolled to element: {selector}")
    
    def select_option(self, selector: str, value: str):
        """Select an option from dropdown"""
        element = self.wait_for_element(selector)
        element.select_option(value)
        logger.info(f"Selected option {value} in {selector}")
    
    def fill_input(self, selector: str, value: str, clear_first: bool = True):
        """Fill an input field"""
        element = self.wait_for_element(selector)
        
        if clear_first:
            element.fill("")  # Clear existing content
        
        element.fill(value)
        logger.info(f"Filled input {selector} with: {value}")
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        element = self.wait_for_element(selector)
        return element.text_content()
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            element = self.page.locator(selector)
            return element.is_visible()
        except:
            return False
    
    def wait_for_text(self, text: str, timeout: int = None):
        """Wait for specific text to appear on page"""
        timeout = timeout or self.config.DEFAULT_TIMEOUT
        self.page.wait_for_selector(f"text={text}", timeout=timeout)
    
    def wait_for_url_change(self, expected_url: str = None, timeout: int = None):
        """Wait for URL to change"""
        timeout = timeout or self.config.DEFAULT_TIMEOUT
        
        if expected_url:
            self.page.wait_for_url(expected_url, timeout=timeout)
        else:
            # Wait for any URL change
            current_url = self.page.url
            start_time = time.time()
            
            while time.time() - start_time < timeout / 1000:
                if self.page.url != current_url:
                    break
                time.sleep(0.1)
    
    def check_for_errors(self):
        """Check for JavaScript errors or console warnings"""
        # Get console messages
        console_messages = []
        
        def handle_console(msg):
            console_messages.append({
                'type': msg.type,
                'text': msg.text,
                'location': msg.location
            })
        
        self.page.on('console', handle_console)
        
        # Check for error messages on page
        error_selectors = [
            UISelectors.ERROR_MESSAGE,
            ".error",
            "[role='alert']",
            ".alert-danger"
        ]
        
        errors = []
        for selector in error_selectors:
            try:
                elements = self.page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        errors.append(element.text_content())
            except:
                pass
        
        return {
            'console_messages': console_messages,
            'page_errors': errors
        }
    
    def wait_for_loading_to_complete(self, timeout: int = None):
        """Wait for loading indicators to disappear"""
        timeout = timeout or self.config.DEFAULT_TIMEOUT
        
        loading_selectors = [
            UISelectors.LOADING_SPINNER,
            ".loading",
            ".spinner",
            "[data-loading='true']"
        ]
        
        for selector in loading_selectors:
            try:
                # Wait for loading to appear first (if it does)
                self.page.wait_for_selector(selector, timeout=2000, state="visible")
                # Then wait for it to disappear
                self.page.wait_for_selector(selector, timeout=timeout, state="hidden")
            except:
                # Loading indicator might not appear, which is fine
                pass

class FormHelper:
    """Helper for form interactions"""
    
    def __init__(self, browser_helper: BrowserHelper):
        self.browser = browser_helper
        self.page = browser_helper.page
    
    def fill_registration_form(self, data: dict, submit: bool = True):
        """Fill the registration form with provided data"""
        logger.info("Filling registration form")
        
        # Fill basic information
        if 'name' in data:
            self.browser.fill_input(UISelectors.NAME_INPUT, data['name'])
        
        if 'email' in data:
            self.browser.fill_input(UISelectors.EMAIL_INPUT, data['email'])
        
        if 'mobile' in data:
            self.browser.fill_input(UISelectors.MOBILE_INPUT, data['mobile'])
        
        if 'studentId' in data:
            self.browser.fill_input(UISelectors.STUDENT_ID_INPUT, data['studentId'])
        
        if 'course' in data:
            self.browser.fill_input(UISelectors.COURSE_INPUT, data['course'])
        
        if 'yearOfGraduation' in data:
            # Try both input and select field
            try:
                self.browser.select_option(UISelectors.YEAR_SELECT, data['yearOfGraduation'])
            except:
                self.browser.fill_input("input[name='yearOfGraduation']", data['yearOfGraduation'])
        
        if 'collegeName' in data:
            self.browser.fill_input(UISelectors.COLLEGE_INPUT, data['collegeName'])
        
        if 'linkedinProfile' in data:
            self.browser.fill_input(UISelectors.LINKEDIN_INPUT, data['linkedinProfile'])
        
        # Take screenshot of filled form
        self.browser.take_screenshot("registration_form_filled")
        
        if submit:
            self.browser.click_element(UISelectors.SUBMIT_BUTTON)
            logger.info("Submitted registration form")
    
    def fill_login_form(self, email: str, password: str, submit: bool = True):
        """Fill login form"""
        logger.info(f"Filling login form for: {email}")
        
        self.browser.fill_input(UISelectors.EMAIL_INPUT, email)
        self.browser.fill_input(UISelectors.PASSWORD_INPUT, password)
        
        if submit:
            self.browser.click_element(UISelectors.SUBMIT_BUTTON)
            logger.info("Submitted login form")
    
    def fill_otp_field(self, otp: str, submit: bool = True):
        """Fill OTP field"""
        logger.info("Filling OTP field")
        
        # Try different OTP input selectors
        otp_selectors = [
            "input[name='otp']",
            "input[placeholder*='OTP' i]",
            "input[aria-label*='otp' i]",
            "input[type='text'][maxlength='6']"
        ]
        
        for selector in otp_selectors:
            try:
                self.browser.fill_input(selector, otp)
                break
            except:
                continue
        
        if submit:
            self.browser.click_element(UISelectors.SUBMIT_BUTTON)

class ValidationHelper:
    """Helper for validation and assertions"""
    
    def __init__(self, browser_helper: BrowserHelper):
        self.browser = browser_helper
        self.page = browser_helper.page
    
    def assert_page_title_contains(self, text: str):
        """Assert page title contains specific text"""
        title = self.page.title()
        assert text.lower() in title.lower(), f"Page title '{title}' does not contain '{text}'"
    
    def assert_url_contains(self, path: str):
        """Assert current URL contains specific path"""
        current_url = self.page.url
        assert path in current_url, f"URL '{current_url}' does not contain '{path}'"
    
    def assert_element_visible(self, selector: str, message: str = None):
        """Assert element is visible"""
        message = message or f"Element '{selector}' should be visible"
        assert self.browser.is_visible(selector), message
    
    def assert_element_not_visible(self, selector: str, message: str = None):
        """Assert element is not visible"""
        message = message or f"Element '{selector}' should not be visible"
        assert not self.browser.is_visible(selector), message
    
    def assert_text_present(self, text: str, message: str = None):
        """Assert text is present on page"""
        message = message or f"Text '{text}' should be present on page"
        page_content = self.page.content()
        assert text in page_content, message
    
    def assert_no_errors_on_page(self):
        """Assert no error messages are displayed"""
        errors = self.browser.check_for_errors()
        
        # Check for page errors
        if errors['page_errors']:
            raise AssertionError(f"Error messages found on page: {errors['page_errors']}")
        
        # Check for console errors (excluding warnings)
        console_errors = [msg for msg in errors['console_messages'] if msg['type'] == 'error']
        if console_errors:
            raise AssertionError(f"Console errors found: {console_errors}")
    
    def assert_form_validation_error(self, expected_fields: list = None):
        """Assert form validation errors are shown"""
        error_found = False
        
        # Check for general error messages
        if self.browser.is_visible(UISelectors.ERROR_MESSAGE):
            error_found = True
        
        # Check for field-specific errors
        if expected_fields:
            for field in expected_fields:
                field_error_selector = f"input[name='{field}'] + .error, input[name='{field}'][aria-invalid='true']"
                if self.browser.is_visible(field_error_selector):
                    error_found = True
        
        assert error_found, "Expected form validation errors but none were found"
    
    def assert_success_message(self, expected_messages: list = None):
        """Assert success message is displayed"""
        success_found = False
        
        # Check for success indicators
        if self.browser.is_visible(UISelectors.SUCCESS_MESSAGE):
            success_found = True
        
        # Check for specific success messages
        if expected_messages:
            page_content = self.page.content().lower()
            for message in expected_messages:
                if message.lower() in page_content:
                    success_found = True
                    break
        
        assert success_found, f"Expected success message not found. Expected one of: {expected_messages}"

# Export main classes
__all__ = ['BrowserHelper', 'FormHelper', 'ValidationHelper']
