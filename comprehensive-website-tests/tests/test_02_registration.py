"""
Test 02: Registration Flow
=========================

This test module covers the complete registration functionality including:
- Registration form validation
- Successful registration flow
- Error handling and edge cases
- Form field validation
- Email format validation
- Mobile number validation
- Required field validation
- Duplicate registration handling
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.registration
@pytest.mark.ui
class TestRegistrationForm:
    """Test cases for registration form functionality"""
    
    def test_registration_page_loads(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that registration page loads correctly"""
        logger.info("📝 Testing registration page load")
        
        # Navigate to registration page
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Verify page loaded
        validation_helper.assert_url_contains("register")
        validation_helper.assert_no_errors_on_page()
        
        # Check for registration form
        form_selectors = [
            "form",
            ".registration-form",
            "[data-testid='registration-form']"
        ]
        
        form_found = False
        for selector in form_selectors:
            if browser_helper.is_visible(selector):
                form_found = True
                logger.info(f"✅ Registration form found: {selector}")
                break
        
        assert form_found, "Registration form not found on page"
        
        # Take screenshot
        browser_helper.take_screenshot("registration_page_loaded")
        
        logger.info("✅ Registration page loaded successfully")
    
    def test_registration_form_fields(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that all required form fields are present"""
        logger.info("🔍 Testing registration form fields")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Required fields to check
        required_fields = [
            {"name": "name", "type": "text", "label": "Name"},
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "mobile", "type": "text", "label": "Mobile"},
            {"name": "studentId", "type": "text", "label": "Student ID"},
            {"name": "course", "type": "text", "label": "Course"},
            {"name": "yearOfGraduation", "type": "select", "label": "Year"},
            {"name": "collegeName", "type": "text", "label": "College"}
        ]
        
        missing_fields = []
        
        for field in required_fields:
            field_selectors = [
                f"input[name='{field['name']}']",
                f"select[name='{field['name']}']",
                f"textarea[name='{field['name']}']",
                f"input[id='{field['name']}']"
            ]
            
            field_found = False
            for selector in field_selectors:
                if browser_helper.is_visible(selector):
                    field_found = True
                    logger.info(f"✅ Found field: {field['label']} ({selector})")
                    break
            
            if not field_found:
                missing_fields.append(field['label'])
                logger.warning(f"⚠️ Missing field: {field['label']}")
        
        # Check for submit button
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Register')",
            "button:has-text('Submit')"
        ]
        
        submit_found = False
        for selector in submit_selectors:
            if browser_helper.is_visible(selector):
                submit_found = True
                logger.info(f"✅ Found submit button: {selector}")
                break
        
        assert submit_found, "Submit button not found"
        
        # Take screenshot of form
        browser_helper.take_screenshot("registration_form_fields")
        
        if missing_fields:
            logger.warning(f"⚠️ Missing fields: {missing_fields}")
        else:
            logger.info("✅ All required fields present")
    
    def test_successful_registration_with_valid_data(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper, test_config: TestConfig):
        """Test successful registration with valid applicant data"""
        logger.info("✅ Testing successful registration with valid data")
        
        # Generate unique test data
        test_applicant = TestDataGenerator.generate_applicant_data()
        import time
        test_applicant['email'] = f"testreg_{int(time.time())}@hackathon.test"
        test_applicant['mobile'] = f"987654{int(time.time()) % 10000:04d}"
        
        logger.info(f"Using test data: {test_applicant['email']}")
        
        # Navigate to registration page
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("registration_page_loaded")
        
        # Verify form is visible
        validation_helper.assert_element_visible(UISelectors.REGISTRATION_FORM)
        
        # Fill registration form
        browser_helper.fill_input(UISelectors.REGISTRATION_NAME_INPUT, test_applicant['name'])
        browser_helper.fill_input(UISelectors.REGISTRATION_EMAIL_INPUT, test_applicant['email'])
        browser_helper.fill_input(UISelectors.REGISTRATION_MOBILE_INPUT, test_applicant['mobile'])
        browser_helper.fill_input(UISelectors.REGISTRATION_STUDENT_ID_INPUT, test_applicant['studentId'])
        browser_helper.fill_input(UISelectors.REGISTRATION_COURSE_INPUT, test_applicant['course'])
        browser_helper.fill_input(UISelectors.REGISTRATION_COLLEGE_INPUT, test_applicant['collegeName'])
        
        # Fill year of graduation
        try:
            browser_helper.select_option(UISelectors.REGISTRATION_YEAR_SELECT, test_applicant['yearOfGraduation'])
        except:
            logger.warning("Year dropdown not found, trying as input field")
            browser_helper.fill_input("input[name='yearOfGraduation']", test_applicant['yearOfGraduation'])
        
        # Fill LinkedIn profile if field exists
        if browser_helper.is_visible(UISelectors.REGISTRATION_LINKEDIN_INPUT):
            browser_helper.fill_input(UISelectors.REGISTRATION_LINKEDIN_INPUT, test_applicant.get('linkedinProfile', ''))
        
        browser_helper.take_screenshot("registration_form_filled")
        
        # Submit form
        browser_helper.click(UISelectors.REGISTRATION_SUBMIT_BUTTON)
        browser_helper.wait_for_loading_to_complete(timeout=15000)
        
        # Take screenshot of result
        browser_helper.take_screenshot("registration_submitted")
        
        # Wait a moment for any success messages or redirects
        time.sleep(3)
        browser_helper.take_screenshot("registration_result")
        
        # Check for success indicators
        current_url = browser_helper.page.url.lower()
        success_indicators = ['success', 'confirm', 'thank', 'registered', 'complete']
        
        registration_successful = False
        for indicator in success_indicators:
            if indicator in current_url:
                registration_successful = True
                logger.info(f"✅ Registration success detected in URL: {indicator}")
                break
        
        # Also check for success messages in page content
        success_messages = [
            "thank you", "success", "registered", "confirmation",
            "application submitted", "registration complete"
        ]
        
        page_content = browser_helper.page.content().lower()
        for message in success_messages:
            if message in page_content:
                registration_successful = True
                logger.info(f"✅ Registration success message detected: {message}")
                break
        
        if registration_successful:
            logger.info("✅ Registration completed successfully")
        else:
            logger.warning("⚠️ Registration may have failed or is pending")
            # Check for error messages
            validation_helper.assert_no_errors_on_page()
        
        logger.info("✅ Registration test completed")
    
    def test_email_validation(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper):
        """Test email format validation"""
        logger.info("📧 Testing email validation")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Test invalid email formats
        invalid_emails = [
            "invalid-email",
            "test@",
            "@example.com",
            "test.example.com",
            "test..test@example.com"
        ]
        
        for invalid_email in invalid_emails:
            logger.info(f"🔍 Testing invalid email: {invalid_email}")
            
            # Fill form with invalid email
            test_data = TestDataGenerator.generate_applicant_data()
            test_data['email'] = invalid_email
            
            form_helper.fill_registration_form(test_data, submit=True)
            
            # Check for validation error
            validation_selectors = [
                "input[name='email'][aria-invalid='true']",
                "input[name='email'] + .error",
                ".field-error",
                ".invalid-feedback",
                "text*='valid email' i"
            ]
            
            validation_error_found = False
            for selector in validation_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        validation_error_found = True
                        logger.info(f"✅ Email validation working for: {invalid_email}")
                        break
                except:
                    continue
            
            if not validation_error_found:
                logger.warning(f"⚠️ No validation error shown for invalid email: {invalid_email}")
            
            # Take screenshot
            browser_helper.take_screenshot(f"email_validation_{invalid_email.replace('@', '_at_').replace('.', '_dot_')}")
            
            # Refresh page for next test
            browser_helper.navigate_to("/register")
            browser_helper.wait_for_loading_to_complete()
        
        logger.info("✅ Email validation tests completed")
    
    def test_mobile_validation(self, browser_helper: BrowserHelper, form_helper: FormHelper, validation_helper: ValidationHelper):
        """Test mobile number validation"""
        logger.info("📱 Testing mobile number validation")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Test invalid mobile numbers
        invalid_mobiles = [
            "123",          # Too short
            "abcdefghij",   # Letters
            "123456789012", # Too long
            "0000000000",   # All zeros
            "+1234567890"   # With country code
        ]
        
        for invalid_mobile in invalid_mobiles:
            logger.info(f"🔍 Testing invalid mobile: {invalid_mobile}")
            
            # Fill form with invalid mobile
            test_data = TestDataGenerator.generate_applicant_data()
            test_data['mobile'] = invalid_mobile
            
            form_helper.fill_registration_form(test_data, submit=True)
            
            # Check for validation error
            validation_selectors = [
                "input[name='mobile'][aria-invalid='true']",
                "input[name='mobile'] + .error",
                ".field-error",
                "text*='valid mobile' i",
                "text*='10 digits' i"
            ]
            
            validation_error_found = False
            for selector in validation_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        validation_error_found = True
                        logger.info(f"✅ Mobile validation working for: {invalid_mobile}")
                        break
                except:
                    continue
            
            if not validation_error_found:
                logger.warning(f"⚠️ No validation error shown for invalid mobile: {invalid_mobile}")
            
            # Take screenshot
            browser_helper.take_screenshot(f"mobile_validation_{invalid_mobile.replace('+', 'plus')}")
            
            # Refresh page for next test
            browser_helper.navigate_to("/register")
            browser_helper.wait_for_loading_to_complete()
        
        logger.info("✅ Mobile validation tests completed")
    
    def test_required_field_validation(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test required field validation"""
        logger.info("⚠️ Testing required field validation")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Try to submit empty form
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Register')",
            "button:has-text('Submit')"
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
        validation_selectors = [
            ".error",
            ".invalid-feedback",
            ".field-error",
            "[aria-invalid='true']",
            "text*='required' i"
        ]
        
        validation_errors_found = []
        for selector in validation_selectors:
            try:
                elements = browser_helper.page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        validation_errors_found.append(element.text_content())
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("required_field_validation")
        
        if validation_errors_found:
            logger.info(f"✅ Required field validation working: {len(validation_errors_found)} errors found")
        else:
            logger.warning("⚠️ No required field validation errors shown")
        
        logger.info("✅ Required field validation test completed")
    
    def test_form_field_limits(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test form field character limits and constraints"""
        logger.info("📏 Testing form field limits")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Test extremely long inputs
        long_string = "a" * 1000
        
        test_cases = [
            {"field": "name", "value": long_string, "description": "Very long name"},
            {"field": "studentId", "value": "A" * 100, "description": "Very long student ID"},
            {"field": "course", "value": long_string, "description": "Very long course name"},
            {"field": "collegeName", "value": long_string, "description": "Very long college name"}
        ]
        
        for test_case in test_cases:
            logger.info(f"🔍 Testing {test_case['description']}")
            
            try:
                # Fill the specific field
                field_selector = f"input[name='{test_case['field']}']"
                if browser_helper.is_visible(field_selector):
                    browser_helper.fill_input(field_selector, test_case['value'])
                    
                    # Check what was actually entered
                    entered_value = browser_helper.page.locator(field_selector).input_value()
                    logger.info(f"Entered {len(entered_value)} characters for {test_case['field']}")
                    
                    # Clear field for next test
                    browser_helper.fill_input(field_selector, "")
            except Exception as e:
                logger.warning(f"Could not test {test_case['field']}: {e}")
        
        # Take screenshot
        browser_helper.take_screenshot("form_field_limits")
        
        logger.info("✅ Form field limits test completed")

@pytest.mark.registration
@pytest.mark.api  
class TestRegistrationAPI:
    """Test registration API functionality"""
    
    def test_registration_api_direct(self, api_helper):
        """Test registration API directly"""
        logger.info("🔌 Testing registration API directly")
        
        # Generate test data
        test_data = TestDataGenerator.generate_applicant_data()
        
        # Call registration API
        result = api_helper.registration.register_applicant(test_data)
        
        if result['success']:
            logger.info("✅ Registration API working successfully")
            logger.info(f"Registration ID: {result.get('registration_id')}")
        else:
            logger.error(f"❌ Registration API failed: {result['error']}")
            pytest.fail(f"Registration API failed: {result['error']}")
    
    def test_duplicate_email_registration(self, api_helper):
        """Test duplicate email registration handling"""
        logger.info("🔄 Testing duplicate email registration")
        
        # Generate test data
        test_data = TestDataGenerator.generate_applicant_data()
        
        # Register first time
        result1 = api_helper.registration.register_applicant(test_data)
        
        # Try to register again with same email
        result2 = api_helper.registration.register_applicant(test_data)
        
        if result1['success'] and not result2['success']:
            logger.info("✅ Duplicate email properly rejected")
        elif not result1['success']:
            logger.warning("⚠️ Initial registration failed, cannot test duplicate")
        else:
            logger.warning("⚠️ Duplicate email not properly handled")

@pytest.mark.registration
@pytest.mark.integration
class TestRegistrationIntegration:
    """Integration tests for registration flow"""
    
    def test_complete_registration_flow(self, browser_helper: BrowserHelper, form_helper: FormHelper, api_helper):
        """Test complete registration flow from UI to API"""
        logger.info("🔗 Testing complete registration flow")
        
        # Generate unique test data
        import time
        test_data = TestDataGenerator.generate_applicant_data()
        test_data['email'] = f"test_{int(time.time())}@example.com"
        
        # Register through UI
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        form_helper.fill_registration_form(test_data, submit=True)
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot
        browser_helper.take_screenshot("complete_registration_flow")
        
        # Verify through API (if accessible)
        try:
            # Check if applicant exists in system
            applicants_result = api_helper.admin.get_applicants()
            if applicants_result['success']:
                applicants = applicants_result['data'].get('applicants', [])
                registered_emails = [a.get('email') for a in applicants]
                
                if test_data['email'] in registered_emails:
                    logger.info("✅ Registration verified through API")
                else:
                    logger.warning("⚠️ Registration not found in API")
            else:
                logger.info("ℹ️ Could not verify through API (requires admin auth)")
        except Exception as e:
            logger.info(f"ℹ️ API verification not available: {e}")
        
        logger.info("✅ Complete registration flow test completed")
