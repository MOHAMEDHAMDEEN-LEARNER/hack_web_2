"""
Test 06: Applicant Portal & Dashboard  
=====================================

This test module covers applicant portal functionality including:
- Applicant dashboard access
- Profile management
- Competition submissions
- Payment integration
- File uploads
- Status tracking
- Notifications
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.applicant
@pytest.mark.portal
@pytest.mark.ui
class TestApplicantPortal:
    """Test cases for applicant portal functionality"""
    
    def test_applicant_dashboard_access(self, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test applicant dashboard access and layout"""
        logger.info("🎯 Testing applicant dashboard access")
        
        # Try accessing applicant dashboard
        dashboard_urls = [
            "/applicant/dashboard",
            "/applicant",
            "/dashboard"
        ]
        
        dashboard_accessed = False
        for url in dashboard_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                
                # Check if we're on a dashboard or redirected to login
                if "login" in current_url:
                    logger.info(f"✅ Correctly redirected to login for: {url}")
                    continue
                elif "dashboard" in current_url or "applicant" in current_url:
                    dashboard_accessed = True
                    logger.info(f"✅ Dashboard accessed: {url}")
                    break
                else:
                    # Check page content for dashboard indicators
                    page_content = browser_helper.page.content().lower()
                    if "dashboard" in page_content or "welcome" in page_content:
                        dashboard_accessed = True
                        logger.info(f"✅ Dashboard content found: {url}")
                        break
            except Exception as e:
                logger.debug(f"Could not access {url}: {e}")
                continue
        
        if dashboard_accessed:
            # Check dashboard elements
            dashboard_elements = [
                "nav",
                ".dashboard",
                ".profile",
                ".competitions",
                ".submissions"
            ]
            
            for element in dashboard_elements:
                try:
                    if browser_helper.is_visible(element):
                        logger.info(f"✅ Dashboard element found: {element}")
                except:
                    continue
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_dashboard_access")
        
        logger.info("✅ Applicant dashboard access test completed")
    
    def test_applicant_profile_management(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test applicant profile management features"""
        logger.info("👤 Testing applicant profile management")
        
        # Navigate to profile page
        profile_urls = [
            "/applicant/profile",
            "/profile",
            "/applicant/dashboard"
        ]
        
        profile_found = False
        for url in profile_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for profile indicators
                profile_indicators = [
                    "form",
                    ".profile",
                    "input[name='name']",
                    "input[name='email']",
                    "text*='profile' i",
                    "text*='personal' i"
                ]
                
                for indicator in profile_indicators:
                    try:
                        if browser_helper.is_visible(indicator):
                            profile_found = True
                            logger.info(f"✅ Profile section found: {indicator}")
                            break
                    except:
                        continue
                
                if profile_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Could not access profile at {url}: {e}")
                continue
        
        if profile_found:
            # Test profile form fields
            profile_fields = [
                ("name", "John Doe Updated"),
                ("email", "updated@example.com"),
                ("phone", "9876543210"),
                ("college", "Updated University"),
                ("year", "3"),
                ("branch", "Updated Computer Science")
            ]
            
            for field_name, test_value in profile_fields:
                field_selectors = [
                    f"input[name='{field_name}']",
                    f"select[name='{field_name}']",
                    f"textarea[name='{field_name}']"
                ]
                
                field_found = False
                for selector in field_selectors:
                    try:
                        if browser_helper.is_visible(selector):
                            # Fill field with test value
                            element = browser_helper.page.query_selector(selector)
                            if element:
                                if element.get_attribute('type') == 'email':
                                    # Skip email field to avoid conflicts
                                    logger.info(f"ℹ️ Skipping email field to avoid conflicts")
                                    continue
                                    
                                browser_helper.fill_input(selector, test_value)
                                field_found = True
                                logger.info(f"✅ Profile field updated: {field_name}")
                                break
                    except Exception as e:
                        logger.debug(f"Could not fill {field_name}: {e}")
                        continue
                
                if not field_found:
                    logger.info(f"ℹ️ Profile field not found: {field_name}")
            
            # Look for save/update button
            save_selectors = [
                "button[type='submit']",
                "button:has-text('Save')",
                "button:has-text('Update')",
                ".btn-save"
            ]
            
            for selector in save_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        logger.info(f"✅ Save button found: {selector}")
                        # Note: Not clicking to avoid data modification
                        break
                except:
                    continue
        
        # Take screenshot
        browser_helper.take_screenshot("applicant_profile_management")
        
        if profile_found:
            logger.info("✅ Profile management features accessible")
        else:
            logger.info("ℹ️ Profile management not accessible (may require authentication)")
        
        logger.info("✅ Profile management test completed")
    
    def test_competition_listings(self, browser_helper: BrowserHelper):
        """Test competition listings in applicant portal"""
        logger.info("🏆 Testing competition listings")
        
        # Navigate to competitions
        competition_urls = [
            "/applicant/competitions",
            "/competitions",
            "/applicant/dashboard"
        ]
        
        competitions_found = False
        for url in competition_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for competition listings
                competition_indicators = [
                    ".competition",
                    ".competition-card",
                    "text*='competition' i",
                    "text*='hackathon' i",
                    "text*='contest' i"
                ]
                
                for indicator in competition_indicators:
                    try:
                        if browser_helper.is_visible(indicator):
                            competitions_found = True
                            logger.info(f"✅ Competition listings found: {indicator}")
                            break
                    except:
                        continue
                
                if competitions_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Could not access competitions at {url}: {e}")
                continue
        
        if competitions_found:
            # Check for competition details
            competition_details = [
                "title",
                "description",
                "deadline",
                "prize",
                "requirement",
                "registration",
                "submit"
            ]
            
            for detail in competition_details:
                try:
                    if browser_helper.is_visible(f"text*='{detail}' i"):
                        logger.info(f"✅ Competition detail found: {detail}")
                except:
                    continue
            
            # Look for action buttons
            action_buttons = [
                "button:has-text('Register')",
                "button:has-text('Submit')",
                "button:has-text('Apply')",
                "a:has-text('View Details')"
            ]
            
            for button in action_buttons:
                try:
                    if browser_helper.is_visible(button):
                        logger.info(f"✅ Action button found: {button}")
                except:
                    continue
        
        # Take screenshot
        browser_helper.take_screenshot("competition_listings")
        
        if competitions_found:
            logger.info("✅ Competition listings accessible")
        else:
            logger.info("ℹ️ Competition listings not found (may require authentication)")
        
        logger.info("✅ Competition listings test completed")
    
    def test_submission_workflow(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test competition submission workflow"""
        logger.info("📝 Testing submission workflow")
        
        # Navigate to submissions page
        submission_urls = [
            "/applicant/submissions",
            "/submissions",
            "/applicant/submit"
        ]
        
        submission_page_found = False
        for url in submission_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for submission form or page
                submission_indicators = [
                    "form",
                    ".submission",
                    ".submit-form",
                    "text*='submission' i",
                    "text*='submit' i",
                    "input[type='file']"
                ]
                
                for indicator in submission_indicators:
                    try:
                        if browser_helper.is_visible(indicator):
                            submission_page_found = True
                            logger.info(f"✅ Submission page found: {indicator}")
                            break
                    except:
                        continue
                
                if submission_page_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Could not access submissions at {url}: {e}")
                continue
        
        if submission_page_found:
            # Test submission form fields
            submission_fields = [
                "title",
                "description",
                "github",
                "demo",
                "video",
                "file"
            ]
            
            for field in submission_fields:
                field_selectors = [
                    f"input[name='{field}']",
                    f"textarea[name='{field}']",
                    f"input[placeholder*='{field}' i]"
                ]
                
                for selector in field_selectors:
                    try:
                        if browser_helper.is_visible(selector):
                            logger.info(f"✅ Submission field found: {field}")
                            break
                    except:
                        continue
            
            # Look for file upload functionality
            file_selectors = [
                "input[type='file']",
                ".file-upload",
                ".dropzone",
                "text*='upload' i"
            ]
            
            file_upload_found = False
            for selector in file_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        file_upload_found = True
                        logger.info(f"✅ File upload found: {selector}")
                        break
                except:
                    continue
            
            if file_upload_found:
                logger.info("✅ File upload functionality available")
            else:
                logger.info("ℹ️ File upload not found")
        
        # Take screenshot
        browser_helper.take_screenshot("submission_workflow")
        
        if submission_page_found:
            logger.info("✅ Submission workflow accessible")
        else:
            logger.info("ℹ️ Submission workflow not accessible (may require authentication)")
        
        logger.info("✅ Submission workflow test completed")
    
    def test_payment_integration(self, browser_helper: BrowserHelper):
        """Test payment integration functionality"""
        logger.info("💳 Testing payment integration")
        
        # Navigate to payment page
        payment_urls = [
            "/payment",
            "/applicant/payment",
            "/checkout"
        ]
        
        payment_page_found = False
        for url in payment_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for payment indicators
                payment_indicators = [
                    ".payment",
                    ".checkout",
                    "text*='payment' i",
                    "text*='pay' i",
                    "text*='amount' i",
                    "text*='₹' i"
                ]
                
                for indicator in payment_indicators:
                    try:
                        if browser_helper.is_visible(indicator):
                            payment_page_found = True
                            logger.info(f"✅ Payment page found: {indicator}")
                            break
                    except:
                        continue
                
                if payment_page_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Could not access payment at {url}: {e}")
                continue
        
        if payment_page_found:
            # Check for payment elements
            payment_elements = [
                "amount",
                "total",
                "fee",
                "pay now",
                "proceed"
            ]
            
            for element in payment_elements:
                try:
                    if browser_helper.is_visible(f"text*='{element}' i"):
                        logger.info(f"✅ Payment element found: {element}")
                except:
                    continue
            
            # Look for payment buttons
            payment_buttons = [
                "button:has-text('Pay')",
                "button:has-text('Proceed')",
                "button:has-text('Checkout')",
                ".pay-btn"
            ]
            
            for button in payment_buttons:
                try:
                    if browser_helper.is_visible(button):
                        logger.info(f"✅ Payment button found: {button}")
                        # Note: Not clicking to avoid actual payment
                        break
                except:
                    continue
        
        # Test payment status pages
        payment_status_urls = [
            "/payment/success",
            "/payment/failed",
            "/payment/cancelled"
        ]
        
        for status_url in payment_status_urls:
            try:
                browser_helper.navigate_to(status_url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                status_type = status_url.split('/')[-1]
                
                if status_type in current_url:
                    logger.info(f"✅ Payment {status_type} page accessible")
                    
                    # Take screenshot of status page
                    browser_helper.take_screenshot(f"payment_{status_type}_page")
                    
            except Exception as e:
                logger.debug(f"Could not access {status_url}: {e}")
                continue
        
        # Take main payment screenshot
        if payment_page_found:
            browser_helper.take_screenshot("payment_integration")
        
        if payment_page_found:
            logger.info("✅ Payment integration accessible")
        else:
            logger.info("ℹ️ Payment integration not accessible (may require authentication)")
        
        logger.info("✅ Payment integration test completed")

@pytest.mark.applicant
@pytest.mark.portal
@pytest.mark.api
class TestApplicantPortalAPI:
    """Test applicant portal API functionality"""
    
    def test_applicant_profile_api(self, api_helper):
        """Test applicant profile API endpoints"""
        logger.info("🔌 Testing applicant profile API")
        
        # Test getting profile (will likely fail without auth, which is expected)
        try:
            profile_result = api_helper.applicant.get_profile()
            if profile_result.get('success'):
                logger.info("✅ Profile API accessible")
            else:
                logger.info("ℹ️ Profile API requires authentication (expected)")
        except:
            logger.info("ℹ️ Profile API endpoint not accessible")
        
        # Test updating profile
        test_profile_data = {
            "name": "Test User",
            "college": "Test University",
            "year": "3",
            "branch": "Computer Science"
        }
        
        try:
            update_result = api_helper.applicant.update_profile(test_profile_data)
            if update_result.get('success'):
                logger.info("✅ Profile update API working")
            else:
                logger.info("ℹ️ Profile update requires authentication (expected)")
        except:
            logger.info("ℹ️ Profile update API endpoint not accessible")
        
        logger.info("✅ Applicant profile API test completed")
    
    def test_submissions_api(self, api_helper):
        """Test submissions API endpoints"""
        logger.info("📤 Testing submissions API")
        
        # Test getting submissions
        try:
            submissions_result = api_helper.applicant.get_submissions()
            if submissions_result.get('success'):
                logger.info("✅ Submissions API accessible")
            else:
                logger.info("ℹ️ Submissions API requires authentication (expected)")
        except:
            logger.info("ℹ️ Submissions API endpoint not accessible")
        
        # Test creating submission
        test_submission = {
            "title": "Test Submission",
            "description": "Test Description",
            "github_url": "https://github.com/test/repo",
            "demo_url": "https://demo.example.com"
        }
        
        try:
            create_result = api_helper.applicant.create_submission(test_submission)
            if create_result.get('success'):
                logger.info("✅ Submission creation API working")
            else:
                logger.info("ℹ️ Submission creation requires authentication (expected)")
        except:
            logger.info("ℹ️ Submission creation API endpoint not accessible")
        
        logger.info("✅ Submissions API test completed")

@pytest.mark.applicant
@pytest.mark.portal
@pytest.mark.integration
class TestApplicantPortalIntegration:
    """Integration tests for applicant portal"""
    
    def test_complete_applicant_journey(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test complete applicant user journey"""
        logger.info("🎭 Testing complete applicant journey")
        
        # Step 1: Registration (if not already done)
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Check if registration is available
        if browser_helper.is_visible("form"):
            test_data = TestDataGenerator.generate_applicant_data()
            test_data['email'] = f"journey_{int(__import__('time').time())}@example.com"
            
            try:
                form_helper.fill_registration_form(test_data, submit=True)
                browser_helper.wait_for_loading_to_complete()
                logger.info("✅ Registration step completed")
            except:
                logger.info("ℹ️ Registration step skipped (form filling failed)")
        
        # Take screenshot of registration
        browser_helper.take_screenshot("journey_registration")
        
        # Step 2: Try to access applicant portal
        browser_helper.navigate_to("/applicant/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        current_url = browser_helper.page.url
        
        # Step 3: Handle login redirect if needed
        if "login" in current_url:
            logger.info("ℹ️ Redirected to login (expected for new registration)")
            
            # Try login with test email
            login_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[name='identifier']"
            ]
            
            for selector in login_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        browser_helper.fill_input(selector, test_data.get('email', 'test@example.com'))
                        break
                except:
                    continue
            
            # Submit login
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
        
        # Take screenshot of login attempt
        browser_helper.take_screenshot("journey_login_attempt")
        
        # Step 4: Check what's accessible
        accessible_features = []
        
        # Test different portal sections
        portal_sections = [
            ("/applicant/dashboard", "Dashboard"),
            ("/applicant/profile", "Profile"),
            ("/applicant/competitions", "Competitions"),
            ("/applicant/submissions", "Submissions"),
            ("/payment", "Payment")
        ]
        
        for url, section_name in portal_sections:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                
                # Check if we reached the intended section
                if section_name.lower() in current_url.lower() or not "login" in current_url:
                    accessible_features.append(section_name)
                    logger.info(f"✅ {section_name} section accessible")
                    
                    # Take screenshot of accessible section
                    section_safe = section_name.lower().replace(' ', '_')
                    browser_helper.take_screenshot(f"journey_{section_safe}")
                else:
                    logger.info(f"ℹ️ {section_name} section redirects to login")
                    
            except Exception as e:
                logger.debug(f"Could not test {section_name}: {e}")
                continue
        
        # Step 5: Summary
        logger.info(f"🎯 Applicant journey summary:")
        logger.info(f"   - Accessible features: {len(accessible_features)}")
        logger.info(f"   - Features: {', '.join(accessible_features) if accessible_features else 'None (authentication required)'}")
        
        if accessible_features:
            logger.info("✅ Applicant portal has accessible features")
        else:
            logger.info("ℹ️ Applicant portal requires proper authentication")
        
        # Take final screenshot
        browser_helper.take_screenshot("journey_complete")
        
        logger.info("✅ Complete applicant journey test completed")
    
    def test_responsive_applicant_portal(self, browser_helper: BrowserHelper):
        """Test applicant portal responsive design"""
        logger.info("📱 Testing applicant portal responsiveness")
        
        # Test different viewport sizes
        viewports = [
            (375, 667, "mobile"),
            (768, 1024, "tablet"),
            (1280, 720, "desktop")
        ]
        
        for width, height, device_type in viewports:
            logger.info(f"🔍 Testing {device_type} view ({width}x{height})")
            
            # Set viewport
            browser_helper.page.set_viewport_size({"width": width, "height": height})
            
            # Navigate to applicant portal
            browser_helper.navigate_to("/applicant/dashboard")
            browser_helper.wait_for_loading_to_complete()
            
            # Check layout adaptation
            try:
                # Check if content fits viewport
                page_width = browser_helper.page.evaluate("document.body.scrollWidth")
                
                if page_width <= width * 1.1:  # Allow 10% margin
                    logger.info(f"✅ {device_type} layout fits viewport")
                else:
                    logger.warning(f"⚠️ {device_type} layout may overflow")
                
                # Check for mobile-specific elements
                if device_type == "mobile":
                    mobile_indicators = [
                        ".mobile-menu",
                        ".hamburger",
                        ".menu-toggle"
                    ]
                    
                    mobile_nav_found = False
                    for indicator in mobile_indicators:
                        try:
                            if browser_helper.is_visible(indicator):
                                mobile_nav_found = True
                                logger.info(f"✅ Mobile navigation found: {indicator}")
                                break
                        except:
                            continue
                    
                    if not mobile_nav_found:
                        logger.info("ℹ️ No specific mobile navigation detected")
                
            except Exception as e:
                logger.debug(f"Could not analyze {device_type} layout: {e}")
            
            # Take screenshot
            browser_helper.take_screenshot(f"portal_responsive_{device_type}")
        
        # Reset to desktop view
        browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
        
        logger.info("✅ Applicant portal responsiveness test completed")
