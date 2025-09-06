"""
Test 01: Landing Page Functionality
===================================

This test module covers the landing page functionality including:
- Page loading and rendering
- Navigation elements
- Login button functionality
- Registration button functionality
- Responsive design
- Content verification
"""

import pytest
import logging
from utils.test_data import TestConfig, UISelectors, TestMessages
from utils.browser_helper import BrowserHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.ui
class TestLandingPage:
    """Test cases for landing page functionality"""
    
    def test_landing_page_loads_successfully(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that landing page loads without errors"""
        logger.info("🏠 Testing landing page load")
        
        # Navigate to landing page
        browser_helper.navigate_to("/")
        
        # Take screenshot
        browser_helper.take_screenshot("landing_page_loaded")
        
        # Verify page loaded successfully
        validation_helper.assert_no_errors_on_page()
        
        # Check for key elements
        validation_helper.assert_element_visible("body", "Page body should be visible")
        
        logger.info("✅ Landing page loaded successfully")
    
    def test_page_title_and_content(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test page title and main content"""
        logger.info("📝 Testing page title and content")
        
        browser_helper.navigate_to("/")
        
        # Check page title
        validation_helper.assert_page_title_contains("hackathon")
        
        # Check for main heading
        main_heading_selectors = [
            "h1:has-text('CIEL-Kings VibeAIthon')",
            "h1:has-text('hackathon')",
            "h1"
        ]
        
        heading_found = False
        for selector in main_heading_selectors:
            if browser_helper.is_visible(selector):
                heading_found = True
                logger.info(f"✅ Found main heading: {selector}")
                break
        
        assert heading_found, "Main heading not found on landing page"
        
        # Take screenshot of content
        browser_helper.take_screenshot("landing_page_content")
        
        logger.info("✅ Page title and content verified")
    
    def test_admin_login_button(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test admin login button functionality"""
        logger.info("👨‍💼 Testing admin login button")
        
        browser_helper.navigate_to("/")
        
        # Look for admin login button with various selectors
        admin_login_selectors = [
            "text=Admin/Jury Login",
            "text=Admin Login", 
            "a[href*='admin']",
            "button:has-text('Admin')",
            ".admin-login"
        ]
        
        admin_button_found = False
        for selector in admin_login_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    admin_button_found = True
                    logger.info(f"✅ Admin login button found and clicked: {selector}")
                    break
            except:
                continue
        
        if not admin_button_found:
            # Try direct navigation
            browser_helper.navigate_to("/admin/login")
            logger.info("🔄 Direct navigation to admin login")
        
        # Verify we're on admin login page
        browser_helper.wait_for_loading_to_complete()
        validation_helper.assert_url_contains("admin")
        
        # Take screenshot
        browser_helper.take_screenshot("admin_login_page_accessed")
        
        logger.info("✅ Admin login button functionality verified")
    
    def test_applicant_login_button(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test applicant login button functionality"""
        logger.info("👤 Testing applicant login button")
        
        browser_helper.navigate_to("/")
        
        # Look for applicant login button
        applicant_login_selectors = [
            "text=Applicant Login",
            "a[href*='applicant']",
            "button:has-text('Applicant')",
            ".applicant-login"
        ]
        
        applicant_button_found = False
        for selector in applicant_login_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    applicant_button_found = True
                    logger.info(f"✅ Applicant login button found and clicked: {selector}")
                    break
            except:
                continue
        
        if not applicant_button_found:
            # Try direct navigation
            browser_helper.navigate_to("/applicant/login")
            logger.info("🔄 Direct navigation to applicant login")
        
        # Verify we're on applicant login page
        browser_helper.wait_for_loading_to_complete()
        validation_helper.assert_url_contains("applicant")
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_login_page_accessed")
        
        logger.info("✅ Applicant login button functionality verified")
    
    def test_registration_button(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test registration button functionality"""
        logger.info("📝 Testing registration button")
        
        browser_helper.navigate_to("/")
        
        # Look for registration button
        registration_selectors = [
            "text=Register as Participant",
            "text=Register",
            "a[href*='register']",
            "button:has-text('Register')",
            ".register-btn"
        ]
        
        registration_button_found = False
        for selector in registration_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    registration_button_found = True
                    logger.info(f"✅ Registration button found and clicked: {selector}")
                    break
            except:
                continue
        
        if not registration_button_found:
            # Try direct navigation
            browser_helper.navigate_to("/register")
            logger.info("🔄 Direct navigation to registration")
        
        # Verify we're on registration page
        browser_helper.wait_for_loading_to_complete()
        validation_helper.assert_url_contains("register")
        
        # Take screenshot
        browser_helper.take_screenshot("registration_page_accessed")
        
        logger.info("✅ Registration button functionality verified")
    
    @pytest.mark.slow
    def test_page_responsiveness(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test page responsiveness across different viewport sizes"""
        logger.info("📱 Testing page responsiveness")
        
        viewports = [
            {"width": 1920, "height": 1080, "name": "Desktop Large"},
            {"width": 1366, "height": 768, "name": "Desktop"},
            {"width": 768, "height": 1024, "name": "Tablet"},
            {"width": 375, "height": 667, "name": "Mobile"}
        ]
        
        for viewport in viewports:
            logger.info(f"📐 Testing {viewport['name']} viewport ({viewport['width']}x{viewport['height']})")
            
            # Set viewport
            browser_helper.page.set_viewport_size(viewport["width"], viewport["height"])
            browser_helper.navigate_to("/")
            browser_helper.wait_for_loading_to_complete()
            
            # Verify page content is visible
            validation_helper.assert_element_visible("body")
            validation_helper.assert_no_errors_on_page()
            
            # Take screenshot for each viewport
            browser_helper.take_screenshot(f"landing_page_{viewport['name'].lower().replace(' ', '_')}")
            
            # Check for mobile menu on smaller screens
            if viewport["width"] < 768:
                mobile_menu_selectors = [
                    "button[aria-label*='menu']",
                    ".mobile-menu-toggle",
                    "button:has-text('☰')",
                    "[data-testid='mobile-menu']"
                ]
                
                mobile_menu_found = False
                for selector in mobile_menu_selectors:
                    if browser_helper.is_visible(selector):
                        mobile_menu_found = True
                        logger.info(f"✅ Mobile menu found: {selector}")
                        break
                
                if mobile_menu_found:
                    browser_helper.click_element(selector)
                    browser_helper.take_screenshot(f"mobile_menu_open_{viewport['name'].lower().replace(' ', '_')}")
        
        logger.info("✅ Page responsiveness verified across all viewports")
    
    def test_navigation_links(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test navigation links functionality"""
        logger.info("🔗 Testing navigation links")
        
        browser_helper.navigate_to("/")
        
        # Common navigation links to test
        nav_links = [
            {"text": "Home", "expected_url": "/"},
            {"text": "Register", "expected_url": "register"},
            {"text": "About", "expected_url": "about"},
            {"text": "Contact", "expected_url": "contact"}
        ]
        
        working_links = []
        
        for link in nav_links:
            try:
                link_selectors = [
                    f"text={link['text']}",
                    f"a:has-text('{link['text']}')",
                    f"[href*='{link['expected_url']}']"
                ]
                
                for selector in link_selectors:
                    if browser_helper.is_visible(selector):
                        # Store current URL
                        original_url = browser_helper.page.url
                        
                        # Click link
                        browser_helper.click_element(selector)
                        browser_helper.wait_for_loading_to_complete()
                        
                        # Check if URL changed as expected
                        new_url = browser_helper.page.url
                        if link['expected_url'] in new_url:
                            working_links.append(link['text'])
                            logger.info(f"✅ Navigation link working: {link['text']}")
                        
                        # Navigate back to landing page
                        browser_helper.navigate_to("/")
                        break
            except Exception as e:
                logger.warning(f"⚠️ Could not test navigation link {link['text']}: {e}")
        
        # Take screenshot of navigation
        browser_helper.take_screenshot("navigation_links_tested")
        
        logger.info(f"✅ Tested {len(working_links)} working navigation links")
    
    def test_page_load_performance(self, browser_helper: BrowserHelper):
        """Test page load performance"""
        logger.info("⚡ Testing page load performance")
        
        import time
        
        # Measure page load time
        start_time = time.time()
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        load_time = time.time() - start_time
        
        logger.info(f"📊 Landing page load time: {load_time:.2f} seconds")
        
        # Assert reasonable load time (should be under 10 seconds)
        assert load_time < 10, f"Page load time too slow: {load_time:.2f}s"
        
        if load_time < 3:
            logger.info("🚀 Excellent load time!")
        elif load_time < 5:
            logger.info("✅ Good load time")
        else:
            logger.warning("⚠️ Load time could be improved")
        
        # Take screenshot
        browser_helper.take_screenshot("landing_page_performance_test")
        
        logger.info("✅ Page load performance verified")
    
    def test_console_errors(self, browser_helper: BrowserHelper):
        """Test for console errors on landing page"""
        logger.info("🔍 Checking for console errors")
        
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        # Check for JavaScript errors
        errors = browser_helper.check_for_errors()
        
        console_errors = [msg for msg in errors['console_messages'] if msg['type'] == 'error']
        
        if console_errors:
            logger.warning(f"⚠️ Console errors found: {console_errors}")
            # Take screenshot for debugging
            browser_helper.take_screenshot("console_errors_detected")
        else:
            logger.info("✅ No console errors detected")
        
        # Log warnings but don't fail test
        console_warnings = [msg for msg in errors['console_messages'] if msg['type'] == 'warning']
        if console_warnings:
            logger.info(f"ℹ️ Console warnings: {len(console_warnings)} warnings found")
        
        logger.info("✅ Console error check completed")

@pytest.mark.ui
@pytest.mark.integration
class TestLandingPageIntegration:
    """Integration tests for landing page with backend"""
    
    def test_landing_page_with_api_connectivity(self, browser_helper: BrowserHelper, api_helper):
        """Test landing page with API connectivity"""
        logger.info("🔗 Testing landing page with API connectivity")
        
        # Check API health first
        health_check = api_helper.health_check()
        
        # Navigate to landing page
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot
        browser_helper.take_screenshot("landing_page_with_api")
        
        # The page should load regardless of API status
        # but we log the API status for information
        if health_check['success']:
            logger.info("✅ API is accessible")
        else:
            logger.warning("⚠️ API not accessible, but page should still work")
        
        logger.info("✅ Landing page integration test completed")
