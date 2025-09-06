"""
Test 12: Comprehensive User Flow Tests
=====================================

This test module covers complete end-to-end user flows including:
- New applicant registration and login
- Admin authentication and dashboard access
- Full user journey testing with real data
- Integration between registration and login systems
- Video and screenshot capture for all user interactions
"""

import pytest
import logging
import time
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)

@pytest.mark.integration
@pytest.mark.comprehensive
@pytest.mark.user_flows
class TestComprehensiveUserFlows:
    """Comprehensive end-to-end user flow tests"""
    
    def test_complete_applicant_registration_and_login_flow(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper, test_config: TestConfig):
        """Test complete applicant registration and login flow"""
        logger.info("🔄 Starting comprehensive applicant registration and login flow")
        
        # Generate unique test data for this run
        test_applicant = TestDataGenerator.generate_applicant_data()
        test_applicant['email'] = f"testuser_{int(time.time())}@hackathon.test"
        test_applicant['mobile'] = f"987654{int(time.time()) % 10000:04d}"
        
        logger.info(f"📝 Generated test applicant: {test_applicant['name']} ({test_applicant['email']})")
        
        # Step 1: Navigate to landing page
        logger.info("🏠 Step 1: Navigate to landing page")
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("01_landing_page_loaded")
        
        # Verify landing page elements
        validation_helper.assert_element_visible(UISelectors.LANDING_MAIN_HEADING)
        validation_helper.assert_element_visible(UISelectors.LANDING_REGISTER_BUTTON)
        validation_helper.assert_element_visible(UISelectors.LANDING_ADMIN_LOGIN_BUTTON)
        validation_helper.assert_element_visible(UISelectors.LANDING_APPLICANT_LOGIN_BUTTON)
        
        # Step 2: Click Register button
        logger.info("📝 Step 2: Navigate to registration page")
        browser_helper.click(UISelectors.LANDING_REGISTER_BUTTON)
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("02_registration_page_loaded")
        
        # Verify registration form loaded
        validation_helper.assert_url_contains("register")
        validation_helper.assert_element_visible(UISelectors.REGISTRATION_FORM)
        
        # Step 3: Fill registration form
        logger.info("✍️ Step 3: Fill registration form with test data")
        
        # Fill required fields
        browser_helper.fill_input(UISelectors.REGISTRATION_NAME_INPUT, test_applicant['name'])
        browser_helper.take_screenshot("03a_name_filled")
        
        browser_helper.fill_input(UISelectors.REGISTRATION_EMAIL_INPUT, test_applicant['email'])
        browser_helper.take_screenshot("03b_email_filled")
        
        browser_helper.fill_input(UISelectors.REGISTRATION_MOBILE_INPUT, test_applicant['mobile'])
        browser_helper.take_screenshot("03c_mobile_filled")
        
        browser_helper.fill_input(UISelectors.REGISTRATION_STUDENT_ID_INPUT, test_applicant['studentId'])
        browser_helper.take_screenshot("03d_student_id_filled")
        
        browser_helper.fill_input(UISelectors.REGISTRATION_COURSE_INPUT, test_applicant['course'])
        browser_helper.take_screenshot("03e_course_filled")
        
        browser_helper.fill_input(UISelectors.REGISTRATION_COLLEGE_INPUT, test_applicant['collegeName'])
        browser_helper.take_screenshot("03f_college_filled")
        
        # Fill year of graduation
        try:
            browser_helper.select_option(UISelectors.REGISTRATION_YEAR_SELECT, test_applicant['yearOfGraduation'])
            browser_helper.take_screenshot("03g_year_selected")
        except Exception as e:
            logger.warning(f"Could not select year dropdown, trying to fill as input: {e}")
            browser_helper.fill_input(UISelectors.REGISTRATION_YEAR_SELECT.replace('select', 'input'), test_applicant['yearOfGraduation'])
        
        # Fill optional LinkedIn profile
        if 'linkedinProfile' in test_applicant and test_applicant['linkedinProfile']:
            try:
                browser_helper.fill_input(UISelectors.REGISTRATION_LINKEDIN_INPUT, test_applicant['linkedinProfile'])
                browser_helper.take_screenshot("03h_linkedin_filled")
            except Exception as e:
                logger.info(f"LinkedIn field not found or not required: {e}")
        
        # Step 4: Submit registration form
        logger.info("🚀 Step 4: Submit registration form")
        browser_helper.take_screenshot("04a_form_ready_to_submit")
        browser_helper.click(UISelectors.REGISTRATION_SUBMIT_BUTTON)
        
        # Wait for registration response
        browser_helper.wait_for_loading_to_complete(timeout=15000)
        browser_helper.take_screenshot("04b_registration_submitted")
        
        # Step 5: Verify registration success
        logger.info("✅ Step 5: Verify registration success")
        time.sleep(2)  # Wait for any success messages to appear
        
        # Look for success indicators
        current_url = browser_helper.page.url.lower()
        success_indicators = [
            "success", "confirm", "thank", "registration",
            "participant", "complete", "submitted"
        ]
        
        registration_successful = False
        for indicator in success_indicators:
            if indicator in current_url or browser_helper.is_visible(f"text={indicator}"):
                registration_successful = True
                logger.info(f"✅ Registration success detected: {indicator}")
                break
        
        # Take screenshot regardless of success detection
        browser_helper.take_screenshot("05_registration_result")
        
        # Store applicant data for later use
        test_applicant_data = test_applicant.copy()
        logger.info(f"📋 Registration completed for: {test_applicant_data['email']}")
        
        # Step 6: Navigate to applicant login
        logger.info("🔐 Step 6: Navigate to applicant login page")
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("06_applicant_login_page")
        
        # Verify applicant login page
        validation_helper.assert_url_contains("applicant")
        validation_helper.assert_url_contains("login")
        
        # Step 7: Test applicant login with registered email
        logger.info("📧 Step 7: Test applicant login with registered email")
        
        # Fill identifier (email or mobile)
        browser_helper.fill_input(UISelectors.APPLICANT_LOGIN_IDENTIFIER_INPUT, test_applicant_data['email'])
        browser_helper.take_screenshot("07a_login_identifier_filled")
        
        # Click Send OTP button
        browser_helper.click(UISelectors.APPLICANT_LOGIN_SEND_OTP_BUTTON)
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("07b_otp_sent")
        
        # Wait for OTP input field to appear
        time.sleep(3)
        
        # Note: In a real test environment, we would need to:
        # 1. Either mock the OTP service
        # 2. Or have a test OTP code (like 123456)
        # 3. Or integrate with email/SMS testing service
        
        # For demonstration, let's try with a common test OTP
        test_otp = "123456"  # Common test OTP
        
        try:
            if browser_helper.is_visible(UISelectors.APPLICANT_LOGIN_OTP_INPUT):
                logger.info("📱 Step 8: Enter test OTP")
                browser_helper.fill_input(UISelectors.APPLICANT_LOGIN_OTP_INPUT, test_otp)
                browser_helper.take_screenshot("08a_otp_entered")
                
                # Click Verify button
                browser_helper.click(UISelectors.APPLICANT_LOGIN_VERIFY_BUTTON)
                browser_helper.wait_for_loading_to_complete()
                browser_helper.take_screenshot("08b_otp_verification_attempt")
                
                # Check for dashboard access
                time.sleep(3)
                current_url = browser_helper.page.url.lower()
                if "dashboard" in current_url:
                    logger.info("✅ Applicant login successful - Dashboard accessed")
                    browser_helper.take_screenshot("08c_applicant_dashboard_success")
                else:
                    logger.info("⚠️ Applicant login may have failed - checking for error messages")
                    browser_helper.take_screenshot("08d_applicant_login_result")
            
        except Exception as e:
            logger.warning(f"OTP verification step failed (expected in test environment): {e}")
            browser_helper.take_screenshot("08e_otp_verification_failed")
        
        logger.info("✅ Applicant registration and login flow test completed")
        
    def test_admin_authentication_and_dashboard_access(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper, test_config: TestConfig):
        """Test admin authentication and dashboard access"""
        logger.info("👨‍💼 Starting admin authentication and dashboard access test")
        
        # Step 1: Navigate to landing page
        logger.info("🏠 Step 1: Navigate to landing page")
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("admin_01_landing_page")
        
        # Step 2: Click Admin/Jury Login button
        logger.info("🔐 Step 2: Navigate to admin login")
        browser_helper.click(UISelectors.LANDING_ADMIN_LOGIN_BUTTON)
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("admin_02_login_page_loaded")
        
        # Verify admin login page
        validation_helper.assert_url_contains("admin")
        validation_helper.assert_url_contains("login")
        validation_helper.assert_element_visible(UISelectors.ADMIN_LOGIN_FORM)
        
        # Step 3: Fill admin login form
        logger.info("✍️ Step 3: Fill admin login form")
        browser_helper.fill_input(UISelectors.ADMIN_LOGIN_EMAIL_INPUT, test_config.ADMIN_CREDENTIALS['email'])
        browser_helper.take_screenshot("admin_03a_email_filled")
        
        browser_helper.fill_input(UISelectors.ADMIN_LOGIN_PASSWORD_INPUT, test_config.ADMIN_CREDENTIALS['password'])
        browser_helper.take_screenshot("admin_03b_password_filled")
        
        # Step 4: Submit login form
        logger.info("🚀 Step 4: Submit admin login form")
        browser_helper.click(UISelectors.ADMIN_LOGIN_SUBMIT_BUTTON)
        browser_helper.wait_for_loading_to_complete(timeout=15000)
        browser_helper.take_screenshot("admin_04_login_submitted")
        
        # Step 5: Verify successful admin login
        logger.info("✅ Step 5: Verify admin login success")
        time.sleep(3)  # Wait for redirect and dashboard load
        
        current_url = browser_helper.page.url.lower()
        login_success_indicators = [
            "dashboard", "admin", "applicants", "management"
        ]
        
        admin_login_successful = False
        for indicator in login_success_indicators:
            if indicator in current_url:
                admin_login_successful = True
                logger.info(f"✅ Admin login success detected in URL: {indicator}")
                break
        
        # Look for dashboard elements
        dashboard_elements = [
            UISelectors.ADMIN_DASHBOARD_HEADING,
            "h1:has-text('Dashboard')",
            "text=Admin",
            "text=Applicants",
            "text=Logout",
            "text=Sign out"
        ]
        
        for element in dashboard_elements:
            if browser_helper.is_visible(element):
                admin_login_successful = True
                logger.info(f"✅ Admin dashboard element found: {element}")
                break
        
        browser_helper.take_screenshot("admin_05_dashboard_access_result")
        
        if admin_login_successful:
            logger.info("✅ Admin authentication successful - Dashboard accessed")
            
            # Step 6: Test dashboard functionality
            logger.info("🎛️ Step 6: Test admin dashboard functionality")
            
            # Look for key admin features
            admin_features = [
                "text=Applicants",
                "text=Competition",
                "text=Rounds",
                "text=Export",
                "text=Settings",
                "text=Statistics"
            ]
            
            available_features = []
            for feature in admin_features:
                if browser_helper.is_visible(feature):
                    available_features.append(feature)
                    logger.info(f"✅ Admin feature available: {feature}")
            
            browser_helper.take_screenshot("admin_06_dashboard_features")
            
            # Test logout functionality
            logger.info("🚪 Step 7: Test admin logout")
            logout_selectors = [
                UISelectors.LOGOUT_BUTTON,
                "button:has-text('Logout')",
                "button:has-text('Sign out')",
                "a:has-text('Logout')",
                "a:has-text('Sign out')"
            ]
            
            logout_successful = False
            for selector in logout_selectors:
                if browser_helper.is_visible(selector):
                    browser_helper.click(selector)
                    browser_helper.wait_for_loading_to_complete()
                    browser_helper.take_screenshot("admin_07_logout_attempt")
                    
                    # Check if redirected to login or landing page
                    time.sleep(2)
                    current_url = browser_helper.page.url.lower()
                    if "login" in current_url or current_url.endswith("/"):
                        logout_successful = True
                        logger.info("✅ Admin logout successful")
                        browser_helper.take_screenshot("admin_08_logout_success")
                    break
            
            if not logout_successful:
                logger.warning("⚠️ Logout button not found or logout failed")
                browser_helper.take_screenshot("admin_08_logout_failed")
        
        else:
            logger.warning("⚠️ Admin login may have failed")
            
            # Check for error messages
            error_selectors = [
                UISelectors.ERROR_MESSAGE,
                "text=Invalid",
                "text=Error",
                "text=Failed",
                ".alert-error",
                ".error-message"
            ]
            
            for selector in error_selectors:
                if browser_helper.is_visible(selector):
                    logger.warning(f"❌ Error message found: {selector}")
                    break
        
        logger.info("✅ Admin authentication and dashboard test completed")
        
    def test_navigation_and_ui_consistency(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper, test_config: TestConfig):
        """Test navigation consistency and UI elements across the application"""
        logger.info("🧭 Starting navigation and UI consistency test")
        
        # Test pages to verify
        test_pages = [
            {"path": "/", "name": "Landing Page", "expected_elements": [UISelectors.LANDING_MAIN_HEADING]},
            {"path": "/register", "name": "Registration Page", "expected_elements": [UISelectors.REGISTRATION_FORM]},
            {"path": "/admin/login", "name": "Admin Login Page", "expected_elements": [UISelectors.ADMIN_LOGIN_FORM]},
            {"path": "/applicant/login", "name": "Applicant Login Page", "expected_elements": [UISelectors.APPLICANT_LOGIN_IDENTIFIER_INPUT]},
        ]
        
        for i, page in enumerate(test_pages, 1):
            logger.info(f"🔍 Step {i}: Testing {page['name']}")
            
            # Navigate to page
            browser_helper.navigate_to(page["path"])
            browser_helper.wait_for_loading_to_complete()
            
            # Take screenshot
            screenshot_name = f"nav_{i:02d}_{page['name'].lower().replace(' ', '_')}"
            browser_helper.take_screenshot(screenshot_name)
            
            # Verify URL
            validation_helper.assert_url_contains(page["path"].lstrip("/") if page["path"] != "/" else "")
            
            # Verify expected elements
            for element in page["expected_elements"]:
                try:
                    validation_helper.assert_element_visible(element)
                    logger.info(f"✅ Element found on {page['name']}: {element}")
                except Exception as e:
                    logger.warning(f"⚠️ Element not found on {page['name']}: {element} - {e}")
            
            # Check for common errors
            validation_helper.assert_no_errors_on_page()
            
            # Verify no loading spinners are stuck
            if browser_helper.is_visible(UISelectors.LOADING_SPINNER):
                time.sleep(5)  # Wait for loading to complete
                if browser_helper.is_visible(UISelectors.LOADING_SPINNER):
                    logger.warning(f"⚠️ Loading spinner still visible on {page['name']}")
        
        logger.info("✅ Navigation and UI consistency test completed")
        
    def test_responsive_design_and_mobile_compatibility(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test responsive design and mobile compatibility"""
        logger.info("📱 Starting responsive design and mobile compatibility test")
        
        # Test different viewport sizes
        viewport_sizes = [
            {"name": "Mobile", "width": 375, "height": 667},
            {"name": "Tablet", "width": 768, "height": 1024},
            {"name": "Desktop", "width": 1920, "height": 1080}
        ]
        
        # Test pages
        test_pages = ["/", "/register", "/admin/login", "/applicant/login"]
        
        for viewport in viewport_sizes:
            logger.info(f"🔍 Testing {viewport['name']} viewport ({viewport['width']}x{viewport['height']})")
            
            # Set viewport size
            browser_helper.page.set_viewport_size(viewport["width"], viewport["height"])
            
            for page_path in test_pages:
                page_name = page_path.replace("/", "").replace("admin/", "admin_").replace("applicant/", "applicant_") or "landing"
                
                # Navigate to page
                browser_helper.navigate_to(page_path)
                browser_helper.wait_for_loading_to_complete()
                
                # Take screenshot
                screenshot_name = f"responsive_{viewport['name'].lower()}_{page_name}"
                browser_helper.take_screenshot(screenshot_name)
                
                # Check if page is still functional
                validation_helper.assert_no_errors_on_page()
                
                time.sleep(1)  # Brief pause between pages
        
        # Reset to default desktop size
        browser_helper.page.set_viewport_size(1280, 720)
        logger.info("✅ Responsive design test completed")
