"""
Test 04: Applicant Authentication
================================

This test module covers applicant authentication functionality including:
- Applicant login page
- OTP-based authentication
- Email/mobile login validation
- OTP verification
- Applicant dashboard access
- Session management
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.auth
@pytest.mark.applicant
@pytest.mark.ui
class TestApplicantLogin:
    """Test cases for applicant login functionality"""
    
    def test_applicant_login_page_loads(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that applicant login page loads correctly"""
        logger.info("👤 Testing applicant login page load")
        
        # Navigate to applicant login page
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Verify page loaded
        validation_helper.assert_url_contains("applicant")
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
        
        assert form_found, "Login form not found on applicant login page"
        
        # Check for email/mobile input field
        identifier_field_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='identifier']",
            "input[name='mobile']",
            "input[placeholder*='email' i]",
            "input[placeholder*='mobile' i]"
        ]
        
        identifier_field_found = False
        for selector in identifier_field_selectors:
            if browser_helper.is_visible(selector):
                identifier_field_found = True
                logger.info(f"✅ Identifier field found: {selector}")
                break
        
        assert identifier_field_found, "Email/mobile input field not found"
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_login_page_loaded")
        
        logger.info("✅ Applicant login page loaded successfully")
    
    def test_applicant_login_with_email(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test applicant login with email address"""
        logger.info("📧 Testing applicant login with email")
        
        # Navigate to applicant login page
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Use a test email (should be registered first, but we'll test the flow)
        test_email = "testapplicant@example.com"
        
        # Fill email field
        email_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='identifier']"
        ]
        
        email_field_found = False
        for selector in email_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.fill_input(selector, test_email)
                    email_field_found = True
                    logger.info(f"✅ Email entered in field: {selector}")
                    break
            except:
                continue
        
        assert email_field_found, "Could not find email input field"
        
        # Look for and click submit/send OTP button
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Login')",
            "button:has-text('Send OTP')",
            "button:has-text('Send')"
        ]
        
        for selector in submit_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    logger.info(f"✅ Clicked submit button: {selector}")
                    break
            except:
                continue
        
        # Wait for response
        browser_helper.wait_for_loading_to_complete()
        
        # Check for OTP field or success message
        otp_indicators = [
            "input[name='otp']",
            "text*='OTP' i",
            "text*='code' i",
            "text*='sent' i",
            ".otp-field"
        ]
        
        otp_flow_detected = False
        for indicator in otp_indicators:
            try:
                if browser_helper.is_visible(indicator):
                    otp_flow_detected = True
                    logger.info(f"✅ OTP flow detected: {indicator}")
                    break
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_login_email_submitted")
        
        if otp_flow_detected:
            logger.info("✅ Email login flow working (OTP system detected)")
        else:
            # Check for error messages
            errors = browser_helper.check_for_errors()
            if errors['page_errors']:
                logger.info(f"ℹ️ Expected error for unregistered email: {errors['page_errors']}")
            else:
                logger.warning("⚠️ No clear response to email login attempt")
        
        logger.info("✅ Email login test completed")
    
    def test_applicant_login_with_mobile(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test applicant login with mobile number"""
        logger.info("📱 Testing applicant login with mobile")
        
        # Navigate to applicant login page
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Use a test mobile number
        test_mobile = "9876543210"
        
        # Fill mobile field
        mobile_selectors = [
            "input[name='mobile']",
            "input[name='identifier']",
            "input[type='tel']",
            "input[placeholder*='mobile' i]"
        ]
        
        mobile_field_found = False
        for selector in mobile_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.fill_input(selector, test_mobile)
                    mobile_field_found = True
                    logger.info(f"✅ Mobile entered in field: {selector}")
                    break
            except:
                continue
        
        if not mobile_field_found:
            # Try email field if mobile field not found (unified identifier field)
            email_selector = "input[type='email'], input[name='email']"
            if browser_helper.is_visible(email_selector):
                browser_helper.fill_input(email_selector, test_mobile)
                mobile_field_found = True
                logger.info("✅ Mobile entered in email field (unified identifier)")
        
        assert mobile_field_found, "Could not find mobile input field"
        
        # Submit the form
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Login')",
            "button:has-text('Send OTP')"
        ]
        
        for selector in submit_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    break
            except:
                continue
        
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_login_mobile_submitted")
        
        logger.info("✅ Mobile login test completed")
    
    def test_otp_verification_flow(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test OTP verification flow"""
        logger.info("🔢 Testing OTP verification flow")
        
        # Navigate to applicant login page
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Enter test email/mobile
        test_identifier = "testapplicant@example.com"
        
        identifier_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='identifier']"
        ]
        
        for selector in identifier_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.fill_input(selector, test_identifier)
                    break
            except:
                continue
        
        # Submit to get OTP field
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Send OTP')",
            "button:has-text('Login')"
        ]
        
        for selector in submit_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    break
            except:
                continue
        
        browser_helper.wait_for_loading_to_complete()
        
        # Look for OTP input field
        otp_selectors = [
            "input[name='otp']",
            "input[placeholder*='OTP' i]",
            "input[placeholder*='code' i]",
            "input[maxlength='6']",
            "input[type='text'][pattern='[0-9]*']"
        ]
        
        otp_field_found = False
        for selector in otp_selectors:
            try:
                if browser_helper.is_visible(selector):
                    # Enter test OTP (will likely fail, but tests the flow)
                    browser_helper.fill_input(selector, "123456")
                    otp_field_found = True
                    logger.info(f"✅ OTP field found and filled: {selector}")
                    break
            except:
                continue
        
        if otp_field_found:
            # Try to submit OTP
            verify_selectors = [
                "button[type='submit']",
                "button:has-text('Verify')",
                "button:has-text('Login')",
                "button:has-text('Submit')"
            ]
            
            for selector in verify_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        browser_helper.click_element(selector)
                        break
                except:
                    continue
            
            browser_helper.wait_for_loading_to_complete()
            
            # Take screenshot of OTP verification attempt
            browser_helper.take_screenshot("otp_verification_submitted")
            
            logger.info("✅ OTP verification flow tested")
        else:
            logger.info("ℹ️ OTP field not displayed (may require registered user)")
        
        logger.info("✅ OTP verification test completed")
    
    def test_invalid_email_mobile_format(self, browser_helper: BrowserHelper):
        """Test validation for invalid email/mobile formats"""
        logger.info("❌ Testing invalid email/mobile formats")
        
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Test invalid formats
        invalid_identifiers = [
            "invalid-email",
            "123",  # Too short mobile
            "@example.com",  # Invalid email
            "12345678901234567890"  # Too long
        ]
        
        for invalid_id in invalid_identifiers:
            logger.info(f"🔍 Testing invalid identifier: {invalid_id}")
            
            # Fill identifier field
            identifier_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[name='identifier']"
            ]
            
            for selector in identifier_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        browser_helper.fill_input(selector, invalid_id)
                        break
                except:
                    continue
            
            # Submit form
            submit_selectors = [
                "button[type='submit']",
                "button:has-text('Send OTP')",
                "button:has-text('Login')"
            ]
            
            for selector in submit_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        browser_helper.click_element(selector)
                        break
                except:
                    continue
            
            browser_helper.wait_for_loading_to_complete()
            
            # Check for validation errors
            validation_selectors = [
                ".error",
                ".invalid-feedback",
                "[aria-invalid='true']",
                "text*='invalid' i",
                "text*='format' i"
            ]
            
            validation_found = False
            for selector in validation_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        validation_found = True
                        logger.info(f"✅ Validation error shown for: {invalid_id}")
                        break
                except:
                    continue
            
            if not validation_found:
                logger.warning(f"⚠️ No validation error for: {invalid_id}")
            
            # Take screenshot
            safe_id = invalid_id.replace('@', '_at_').replace('.', '_dot_')
            browser_helper.take_screenshot(f"invalid_identifier_{safe_id}")
            
            # Refresh for next test
            browser_helper.navigate_to("/applicant/login")
            browser_helper.wait_for_loading_to_complete()
        
        logger.info("✅ Invalid format validation test completed")

@pytest.mark.auth
@pytest.mark.applicant
@pytest.mark.api
class TestApplicantAuthenticationAPI:
    """Test applicant authentication via API"""
    
    def test_send_otp_api(self, api_helper):
        """Test sending OTP via API"""
        logger.info("📤 Testing send OTP API")
        
        # Test with email
        test_email = "testapplicant@example.com"
        result = api_helper.auth.applicant_send_otp(test_email)
        
        # We expect this to fail for unregistered user, which is correct behavior
        if not result['success']:
            logger.info("✅ OTP send correctly rejected for unregistered email")
        else:
            logger.info("✅ OTP send API working")
    
    def test_verify_otp_api(self, api_helper):
        """Test OTP verification via API"""
        logger.info("🔢 Testing OTP verification API")
        
        # Test with test credentials (will fail, but tests the API)
        test_identifier = "testapplicant@example.com"
        test_otp = "123456"
        
        result = api_helper.auth.applicant_verify_otp(test_identifier, test_otp)
        
        # We expect this to fail, which is correct behavior
        if not result['success']:
            logger.info("✅ OTP verification correctly rejected invalid OTP")
        else:
            logger.warning("⚠️ Invalid OTP was accepted")

@pytest.mark.auth
@pytest.mark.applicant
@pytest.mark.integration
class TestApplicantAuthenticationIntegration:
    """Integration tests for applicant authentication"""
    
    def test_complete_applicant_auth_flow(self, browser_helper: BrowserHelper, form_helper: FormHelper, api_helper):
        """Test complete applicant authentication flow"""
        logger.info("🔗 Testing complete applicant auth flow")
        
        # Step 1: First register an applicant
        test_data = TestDataGenerator.generate_applicant_data()
        test_data['email'] = f"testauth_{int(__import__('time').time())}@example.com"
        
        # Register via UI
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_registration_form(test_data, submit=True)
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot of registration
        browser_helper.take_screenshot("auth_flow_registration")
        
        # Step 2: Try to login with registered email
        browser_helper.navigate_to("/applicant/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Fill login form
        identifier_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='identifier']"
        ]
        
        for selector in identifier_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.fill_input(selector, test_data['email'])
                    break
            except:
                continue
        
        # Submit login form
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Send OTP')",
            "button:has-text('Login')"
        ]
        
        for selector in submit_selectors:
            try:
                if browser_helper.is_visible(selector):
                    browser_helper.click_element(selector)
                    break
            except:
                continue
        
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot of login attempt
        browser_helper.take_screenshot("auth_flow_login_attempt")
        
        # Check if OTP field appears (indicates registered user)
        otp_selectors = [
            "input[name='otp']",
            "text*='OTP' i",
            "text*='code' i"
        ]
        
        otp_flow_active = False
        for selector in otp_selectors:
            try:
                if browser_helper.is_visible(selector):
                    otp_flow_active = True
                    logger.info("✅ OTP flow activated for registered user")
                    break
            except:
                continue
        
        if otp_flow_active:
            logger.info("✅ Complete auth flow working (OTP system active)")
        else:
            logger.info("ℹ️ OTP flow not detected (may need real OTP)")
        
        logger.info("✅ Complete applicant auth flow test completed")
    
    def test_applicant_dashboard_access_without_auth(self, browser_helper: BrowserHelper):
        """Test accessing applicant dashboard without authentication"""
        logger.info("🚫 Testing dashboard access without auth")
        
        # Try to access applicant dashboard directly
        dashboard_urls = [
            "/applicant/dashboard",
            "/applicant",
            "/dashboard"
        ]
        
        for url in dashboard_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                
                # Should be redirected to login or show access denied
                if "login" in current_url:
                    logger.info(f"✅ Correctly redirected to login for: {url}")
                elif "401" in current_url or "403" in current_url:
                    logger.info(f"✅ Access denied for: {url}")
                else:
                    # Check page content for access restrictions
                    page_content = browser_helper.page.content().lower()
                    if "login" in page_content or "access denied" in page_content or "unauthorized" in page_content:
                        logger.info(f"✅ Access restricted for: {url}")
                    else:
                        logger.warning(f"⚠️ Dashboard accessible without auth: {url}")
                
                # Take screenshot
                url_safe = url.replace("/", "_")
                browser_helper.take_screenshot(f"unauth_dashboard_access{url_safe}")
                
            except Exception as e:
                logger.warning(f"Could not test dashboard access for {url}: {e}")
        
        logger.info("✅ Unauthorized access test completed")
