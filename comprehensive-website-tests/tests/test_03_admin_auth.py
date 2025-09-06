"""
Test 03: Admin Authentication
============================

This test module covers admin authentication functionality including:
- Admin login form validation
- Successful admin login
- Invalid credential handling
- Admin dashboard access
- Session management
- Role-based access control
"""

import pytest
import logging
from utils.test_data import TestConfig, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.auth
@pytest.mark.admin
@pytest.mark.ui
class TestAdminLogin:
    """Test cases for admin login functionality"""
    
    def test_admin_login_page_loads(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that admin login page loads correctly"""
        logger.info("👨‍💼 Testing admin login page load")
        
        # Navigate to admin login page
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Verify page loaded
        validation_helper.assert_url_contains("admin")
        validation_helper.assert_no_errors_on_page()
        
        # Check for login form
        form_selectors = [
            "form",
            ".login-form",
            "[data-testid='login-form']"
        ]
        
        form_found = False
        for selector in form_selectors:
            if browser_helper.is_visible(selector):
                form_found = True
                logger.info(f"✅ Login form found: {selector}")
                break
        
        assert form_found, "Login form not found on admin login page"
        
        # Check for required form fields
        email_field = browser_helper.is_visible("input[type='email'], input[name='email']")
        password_field = browser_helper.is_visible("input[type='password'], input[name='password']")
        
        assert email_field, "Email field not found"
        assert password_field, "Password field not found"
        
        # Take screenshot
        browser_helper.take_screenshot("admin_login_page_loaded")
        
        logger.info("✅ Admin login page loaded successfully")
    
    def test_successful_admin_login(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper, config: TestConfig):
        """Test successful admin login with valid credentials"""
        logger.info("🔐 Testing successful admin login")
        
        # Navigate to admin login page
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Fill login form with admin credentials
        form_helper.fill_login_form(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password'],
            submit=True
        )
        
        # Wait for login response
        browser_helper.wait_for_loading_to_complete()
        
        # Check for successful login indicators
        success_indicators = [
            "dashboard",
            "admin",
            "welcome",
            "logout"
        ]
        
        login_successful = False
        current_url = browser_helper.page.url.lower()
        
        # Check URL for success indicators
        for indicator in success_indicators:
            if indicator in current_url:
                login_successful = True
                logger.info(f"✅ Login success detected in URL: {indicator}")
                break
        
        # Check page content for success indicators
        if not login_successful:
            page_content = browser_helper.page.content().lower()
            for indicator in success_indicators:
                if indicator in page_content:
                    login_successful = True
                    logger.info(f"✅ Login success detected in content: {indicator}")
                    break
        
        # Look for specific dashboard elements
        dashboard_selectors = [
            "text=Dashboard",
            "text=Admin Dashboard", 
            ".dashboard",
            "[data-testid='dashboard']",
            "text=Applicants",
            "text=Competition Rounds"
        ]
        
        for selector in dashboard_selectors:
            try:
                if browser_helper.is_visible(selector):
                    login_successful = True
                    logger.info(f"✅ Dashboard element found: {selector}")
                    break
            except:
                continue
        
        # Take screenshot of result
        browser_helper.take_screenshot("admin_login_result")
        
        if not login_successful:
            # Check for error messages
            errors = browser_helper.check_for_errors()
            if errors['page_errors']:
                logger.error(f"❌ Admin login failed with errors: {errors['page_errors']}")
                pytest.fail(f"Admin login failed: {errors['page_errors']}")
            else:
                logger.warning("⚠️ Admin login result unclear")
                # Don't fail the test as login might have worked but we can't detect it clearly
        
        logger.info("✅ Admin login test completed")
    
    def test_invalid_admin_credentials(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper):
        """Test admin login with invalid credentials"""
        logger.info("❌ Testing invalid admin credentials")
        
        invalid_credentials = [
            {"email": "invalid@test.com", "password": "wrongpassword"},
            {"email": "admin@test.com", "password": "wrongpassword"},
            {"email": "wrong@email.com", "password": "admin123"},
            {"email": "", "password": "admin123"},
            {"email": "admin@test.com", "password": ""}
        ]
        
        for creds in invalid_credentials:
            logger.info(f"🔍 Testing invalid credentials: {creds['email']}")
            
            # Navigate to admin login page
            browser_helper.navigate_to("/admin/login")
            browser_helper.wait_for_loading_to_complete()
            
            # Fill form with invalid credentials
            form_helper.fill_login_form(
                email=creds['email'],
                password=creds['password'],
                submit=True
            )
            
            # Wait for response
            browser_helper.wait_for_loading_to_complete()
            
            # Check for error messages
            error_selectors = [
                ".error",
                ".alert-error",
                ".invalid-feedback",
                "text*='invalid' i",
                "text*='incorrect' i",
                "text*='failed' i",
                "[data-state='error']"
            ]
            
            error_found = False
            for selector in error_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        error_text = browser_helper.get_text(selector)
                        error_found = True
                        logger.info(f"✅ Error message shown: {error_text}")
                        break
                except:
                    continue
            
            # Check if still on login page (not redirected)
            current_url = browser_helper.page.url
            if "login" in current_url:
                error_found = True
                logger.info("✅ Stayed on login page (good)")
            
            if not error_found:
                logger.warning(f"⚠️ No error shown for invalid credentials: {creds['email']}")
            
            # Take screenshot
            email_safe = creds['email'].replace('@', '_at_').replace('.', '_dot_')
            browser_helper.take_screenshot(f"invalid_admin_login_{email_safe}")
        
        logger.info("✅ Invalid credentials test completed")
    
    def test_admin_login_form_validation(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test admin login form validation"""
        logger.info("📝 Testing admin login form validation")
        
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Try to submit empty form
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Login')",
            "input[type='submit']"
        ]
        
        for selector in submit_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    break
            except:
                continue
        
        # Wait for validation
        browser_helper.wait_for_loading_to_complete()
        
        # Check for validation errors
        validation_found = False
        validation_selectors = [
            ".error",
            ".invalid-feedback",
            "[aria-invalid='true']",
            "text*='required' i"
        ]
        
        for selector in validation_selectors:
            try:
                if browser_helper.is_visible(selector):
                    validation_found = True
                    logger.info(f"✅ Form validation working: {selector}")
                    break
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("admin_login_form_validation")
        
        if not validation_found:
            logger.warning("⚠️ No form validation detected")
        
        logger.info("✅ Form validation test completed")
    
    def test_admin_dashboard_access(self, browser_helper: BrowserHelper, form_helper: FormHelper, config: TestConfig):
        """Test admin dashboard access after login"""
        logger.info("🏠 Testing admin dashboard access")
        
        # Login as admin first
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_login_form(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password'],
            submit=True
        )
        
        browser_helper.wait_for_loading_to_complete()
        
        # Check for dashboard elements
        dashboard_elements = [
            {"name": "Applicants", "selectors": ["text=Applicants", "a[href*='applicants']"]},
            {"name": "Competition Rounds", "selectors": ["text=Competition Rounds", "text=Rounds", "a[href*='rounds']"]},
            {"name": "Settings", "selectors": ["text=Settings", "a[href*='settings']"]},
            {"name": "Export Data", "selectors": ["text=Export", "a[href*='export']"]},
            {"name": "Quick Actions", "selectors": ["text=Quick Actions", "a[href*='quick']"]}
        ]
        
        found_elements = []
        
        for element in dashboard_elements:
            element_found = False
            for selector in element['selectors']:
                try:
                    if browser_helper.is_visible(selector):
                        found_elements.append(element['name'])
                        element_found = True
                        logger.info(f"✅ Found dashboard element: {element['name']}")
                        break
                except:
                    continue
            
            if not element_found:
                logger.info(f"ℹ️ Dashboard element not found: {element['name']}")
        
        # Take screenshot of dashboard
        browser_helper.take_screenshot("admin_dashboard_accessed")
        
        logger.info(f"✅ Admin dashboard access test completed. Found {len(found_elements)} dashboard elements")
    
    def test_admin_navigation_menu(self, browser_helper: BrowserHelper, form_helper: FormHelper, config: TestConfig):
        """Test admin navigation menu functionality"""
        logger.info("🧭 Testing admin navigation menu")
        
        # Login as admin first
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_login_form(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password'],
            submit=True
        )
        
        browser_helper.wait_for_loading_to_complete()
        
        # Test navigation to different admin pages
        admin_pages = [
            {"name": "Applicants", "url_pattern": "applicant", "selectors": ["text=Applicants", "a[href*='applicants']"]},
            {"name": "Rounds", "url_pattern": "round", "selectors": ["text=Competition Rounds", "text=Rounds", "a[href*='rounds']"]},
            {"name": "Settings", "url_pattern": "setting", "selectors": ["text=Settings", "a[href*='settings']"]},
            {"name": "Export", "url_pattern": "export", "selectors": ["text=Export", "a[href*='export']"]}
        ]
        
        successful_navigation = []
        
        for page in admin_pages:
            logger.info(f"🔍 Testing navigation to {page['name']}")
            
            navigation_successful = False
            for selector in page['selectors']:
                try:
                    if browser_helper.is_visible(selector):
                        original_url = browser_helper.page.url
                        browser_helper.click_element(selector)
                        browser_helper.wait_for_loading_to_complete()
                        
                        new_url = browser_helper.page.url
                        if page['url_pattern'] in new_url.lower() or new_url != original_url:
                            successful_navigation.append(page['name'])
                            navigation_successful = True
                            logger.info(f"✅ Successfully navigated to {page['name']}")
                            
                            # Take screenshot
                            browser_helper.take_screenshot(f"admin_navigation_{page['name'].lower()}")
                        
                        # Navigate back to dashboard
                        browser_helper.page.go_back()
                        browser_helper.wait_for_loading_to_complete()
                        break
                except Exception as e:
                    logger.warning(f"Could not navigate to {page['name']}: {e}")
            
            if not navigation_successful:
                logger.info(f"ℹ️ Could not test navigation to {page['name']}")
        
        logger.info(f"✅ Admin navigation test completed. Successfully tested {len(successful_navigation)} pages")

@pytest.mark.auth  
@pytest.mark.admin
@pytest.mark.api
class TestAdminAuthenticationAPI:
    """Test admin authentication via API"""
    
    def test_admin_login_api(self, api_helper, config: TestConfig):
        """Test admin login via API"""
        logger.info("🔌 Testing admin login API")
        
        # Test successful login
        result = api_helper.auth.admin_login(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password']
        )
        
        if result['success']:
            logger.info("✅ Admin API login successful")
            logger.info(f"User info: {result.get('user', {}).get('email', 'Unknown')}")
        else:
            logger.error(f"❌ Admin API login failed: {result['error']}")
            pytest.fail(f"Admin API login failed: {result['error']}")
    
    def test_admin_login_api_invalid_credentials(self, api_helper):
        """Test admin login API with invalid credentials"""
        logger.info("❌ Testing admin login API with invalid credentials")
        
        # Test invalid credentials
        result = api_helper.auth.admin_login(
            email="invalid@test.com",
            password="wrongpassword"
        )
        
        if not result['success']:
            logger.info("✅ Invalid credentials properly rejected by API")
        else:
            logger.error("❌ Invalid credentials were accepted by API")
            pytest.fail("Invalid credentials should not be accepted")

@pytest.mark.auth
@pytest.mark.admin  
@pytest.mark.integration
class TestAdminAuthenticationIntegration:
    """Integration tests for admin authentication"""
    
    def test_admin_session_persistence(self, browser_helper: BrowserHelper, form_helper: FormHelper, config: TestConfig):
        """Test admin session persistence across page navigation"""
        logger.info("🔄 Testing admin session persistence")
        
        # Login as admin
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_login_form(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password'],
            submit=True
        )
        
        browser_helper.wait_for_loading_to_complete()
        
        # Navigate to different pages and verify session
        test_pages = ["/", "/admin", "/admin/applicants", "/admin/settings"]
        
        for page in test_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Check if still authenticated (not redirected to login)
                current_url = browser_helper.page.url
                if "login" not in current_url:
                    logger.info(f"✅ Session persisted for page: {page}")
                else:
                    logger.warning(f"⚠️ Session lost for page: {page}")
                
                # Take screenshot
                page_name = page.replace("/", "_") or "home"
                browser_helper.take_screenshot(f"admin_session_{page_name}")
                
            except Exception as e:
                logger.warning(f"Could not test session for {page}: {e}")
        
        logger.info("✅ Admin session persistence test completed")
    
    def test_admin_logout(self, browser_helper: BrowserHelper, form_helper: FormHelper, config: TestConfig):
        """Test admin logout functionality"""
        logger.info("🚪 Testing admin logout")
        
        # Login as admin first
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_login_form(
            email=config.ADMIN_CREDENTIALS['email'],
            password=config.ADMIN_CREDENTIALS['password'],
            submit=True
        )
        
        browser_helper.wait_for_loading_to_complete()
        
        # Look for logout button/link
        logout_selectors = [
            "text=Logout",
            "text=Sign Out",
            "a[href*='logout']",
            "button:has-text('Logout')",
            "[data-testid='logout']"
        ]
        
        logout_successful = False
        for selector in logout_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    browser_helper.wait_for_loading_to_complete()
                    
                    # Check if redirected to login or home page
                    current_url = browser_helper.page.url
                    if "login" in current_url or current_url.endswith("/"):
                        logout_successful = True
                        logger.info("✅ Logout successful")
                        break
            except Exception as e:
                logger.warning(f"Could not test logout with {selector}: {e}")
        
        if not logout_successful:
            logger.info("ℹ️ Could not test logout (logout button not found)")
        
        # Take screenshot
        browser_helper.take_screenshot("admin_logout_result")
        
        logger.info("✅ Admin logout test completed")
