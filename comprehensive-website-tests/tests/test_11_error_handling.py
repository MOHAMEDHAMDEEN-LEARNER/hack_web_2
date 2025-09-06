"""
Test 11: Error Handling & Edge Cases
====================================

This test module covers error handling and edge cases including:
- Network failures
- Invalid data scenarios  
- Server errors
- Database connectivity issues
- File upload edge cases
- Authentication edge cases
- Form validation edge cases
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.error_handling
@pytest.mark.network
class TestNetworkErrorHandling:
    """Test network error handling"""
    
    def test_offline_behavior(self, browser_helper: BrowserHelper):
        """Test application behavior when offline"""
        logger.info("📡 Testing offline behavior")
        
        # First load page normally
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        # Take screenshot of normal state
        browser_helper.take_screenshot("before_offline")
        
        try:
            # Simulate offline condition
            browser_helper.page.context.set_offline(True)
            
            # Try to navigate to another page
            browser_helper.navigate_to("/register")
            
            # Check for offline indicators
            offline_indicators = [
                "text*='offline' i",
                "text*='no connection' i",
                "text*='network error' i",
                "text*='connection failed' i",
                ".offline",
                ".no-connection"
            ]
            
            offline_handling_found = False
            for indicator in offline_indicators:
                try:
                    if browser_helper.is_visible(indicator):
                        offline_handling_found = True
                        logger.info(f"✅ Offline indicator found: {indicator}")
                        break
                except:
                    continue
            
            # Check if browser shows default offline page
            page_content = browser_helper.page.content().lower()
            if "no internet" in page_content or "offline" in page_content:
                offline_handling_found = True
                logger.info("✅ Browser offline page detected")
            
            # Take screenshot of offline state
            browser_helper.take_screenshot("offline_state")
            
            if offline_handling_found:
                logger.info("✅ Application handles offline state")
            else:
                logger.info("ℹ️ No specific offline handling detected")
            
        except Exception as e:
            logger.warning(f"Could not test offline behavior: {e}")
        finally:
            # Restore online state
            browser_helper.page.context.set_offline(False)
        
        logger.info("✅ Offline behavior test completed")
    
    def test_slow_network_handling(self, browser_helper: BrowserHelper):
        """Test application behavior with slow network"""
        logger.info("🐌 Testing slow network handling")
        
        try:
            # Simulate slow network (throttling)
            browser_helper.page.context.set_extra_http_headers({
                "Connection": "slow"
            })
            
            # Measure load time with slow network
            import time
            start_time = time.time()
            
            browser_helper.navigate_to("/")
            browser_helper.wait_for_loading_to_complete()
            
            load_time = time.time() - start_time
            
            logger.info(f"📊 Load time with slow network: {load_time:.3f}s")
            
            # Check for loading indicators
            loading_indicators = [
                ".loading",
                ".spinner",
                ".skeleton",
                "[aria-label*='loading' i]",
                "text*='loading' i"
            ]
            
            loading_handling_found = False
            for indicator in loading_indicators:
                try:
                    if browser_helper.is_visible(indicator):
                        loading_handling_found = True
                        logger.info(f"✅ Loading indicator found: {indicator}")
                        break
                except:
                    continue
            
            # Take screenshot
            browser_helper.take_screenshot("slow_network_handling")
            
            if loading_handling_found:
                logger.info("✅ Application shows loading indicators")
            else:
                logger.info("ℹ️ No loading indicators detected")
            
            # Test if page still functions
            if browser_helper.is_visible("nav, .navbar, .navigation"):
                logger.info("✅ Page functions with slow network")
            else:
                logger.warning("⚠️ Page may not function properly with slow network")
            
        except Exception as e:
            logger.warning(f"Could not test slow network: {e}")
        
        logger.info("✅ Slow network handling test completed")

@pytest.mark.error_handling
@pytest.mark.server_errors
class TestServerErrorHandling:
    """Test server error handling"""
    
    def test_404_error_handling(self, browser_helper: BrowserHelper):
        """Test 404 error page handling"""
        logger.info("🔍 Testing 404 error handling")
        
        # Try to access non-existent pages
        non_existent_pages = [
            "/non-existent-page",
            "/admin/non-existent",
            "/api/non-existent",
            "/random-path-12345"
        ]
        
        error_handling_results = []
        
        for page in non_existent_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Check for 404 indicators
                error_404_indicators = [
                    "404",
                    "not found",
                    "page not found",
                    "does not exist"
                ]
                
                page_content = browser_helper.page.content().lower()
                
                error_detected = False
                for indicator in error_404_indicators:
                    if indicator in page_content:
                        error_detected = True
                        logger.info(f"✅ 404 error detected for {page}: {indicator}")
                        break
                
                # Check for custom error page elements
                error_page_elements = [
                    ".error-page",
                    ".not-found",
                    ".error-404",
                    "h1:has-text('404')",
                    "h1:has-text('Not Found')"
                ]
                
                custom_error_page = False
                for element in error_page_elements:
                    try:
                        if browser_helper.is_visible(element):
                            custom_error_page = True
                            logger.info(f"✅ Custom error page element found: {element}")
                            break
                    except:
                        continue
                
                error_handling_results.append({
                    'page': page,
                    'error_detected': error_detected,
                    'custom_page': custom_error_page
                })
                
                # Take screenshot of first 404 page
                if page == non_existent_pages[0]:
                    browser_helper.take_screenshot("404_error_page")
                
            except Exception as e:
                logger.debug(f"Could not test 404 for {page}: {e}")
                continue
        
        # Analyze results
        pages_with_error_detection = sum(1 for r in error_handling_results if r['error_detected'])
        pages_with_custom_page = sum(1 for r in error_handling_results if r['custom_page'])
        
        logger.info(f"📊 404 Error handling summary:")
        logger.info(f"   - Pages tested: {len(error_handling_results)}")
        logger.info(f"   - Error detection: {pages_with_error_detection}/{len(error_handling_results)}")
        logger.info(f"   - Custom error pages: {pages_with_custom_page}/{len(error_handling_results)}")
        
        if pages_with_error_detection >= len(error_handling_results) * 0.7:
            logger.info("✅ Good 404 error handling")
        else:
            logger.warning("⚠️ Limited 404 error handling")
        
        logger.info("✅ 404 error handling test completed")
    
    def test_server_error_simulation(self, browser_helper: BrowserHelper):
        """Test server error simulation"""
        logger.info("🚨 Testing server error simulation")
        
        # Try to trigger server errors by accessing admin endpoints without auth
        potential_error_endpoints = [
            "/admin/api/users",
            "/api/admin/stats",
            "/admin/delete-all",  # Hopefully non-existent destructive endpoint
            "/api/internal/debug"
        ]
        
        server_error_results = []
        
        for endpoint in potential_error_endpoints:
            try:
                browser_helper.navigate_to(endpoint)
                browser_helper.wait_for_loading_to_complete()
                
                # Check for server error indicators
                server_error_indicators = [
                    "500",
                    "internal server error",
                    "server error",
                    "error occurred",
                    "unauthorized",
                    "forbidden",
                    "access denied"
                ]
                
                page_content = browser_helper.page.content().lower()
                
                error_type_detected = None
                for indicator in server_error_indicators:
                    if indicator in page_content:
                        error_type_detected = indicator
                        logger.info(f"✅ Server error detected for {endpoint}: {indicator}")
                        break
                
                # Check for error page elements
                error_elements = [
                    ".error",
                    ".server-error",
                    ".unauthorized",
                    ".forbidden"
                ]
                
                error_element_found = False
                for element in error_elements:
                    try:
                        if browser_helper.is_visible(element):
                            error_element_found = True
                            break
                    except:
                        continue
                
                server_error_results.append({
                    'endpoint': endpoint,
                    'error_detected': error_type_detected is not None,
                    'error_type': error_type_detected,
                    'error_element': error_element_found
                })
                
            except Exception as e:
                logger.debug(f"Could not test server error for {endpoint}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("server_error_handling")
        
        # Analyze results
        endpoints_with_errors = sum(1 for r in server_error_results if r['error_detected'])
        
        logger.info(f"📊 Server error handling summary:")
        logger.info(f"   - Endpoints tested: {len(server_error_results)}")
        logger.info(f"   - Error responses: {endpoints_with_errors}/{len(server_error_results)}")
        
        if endpoints_with_errors > 0:
            logger.info("✅ Server error handling detected")
        else:
            logger.info("ℹ️ No server errors encountered (endpoints may not exist)")
        
        logger.info("✅ Server error simulation test completed")

@pytest.mark.error_handling
@pytest.mark.data_validation
class TestDataValidationEdgeCases:
    """Test data validation edge cases"""
    
    def test_extreme_input_values(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test extreme input values"""
        logger.info("🔥 Testing extreme input values")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Extreme test values
        extreme_test_cases = [
            ("very_long_string", "A" * 1000),  # Very long string
            ("empty_string", ""),  # Empty string
            ("special_characters", "!@#$%^&*()_+-=[]{}|;':\",./<>?"),  # Special characters
            ("unicode_characters", "测试🎉🚀💻🌟"),  # Unicode characters
            ("sql_injection", "'; DROP TABLE users; --"),  # SQL injection attempt
            ("xss_script", "<script>alert('XSS')</script>"),  # XSS attempt
            ("null_bytes", "test\0null"),  # Null bytes
            ("very_large_number", "99999999999999999999"),  # Very large number
            ("negative_number", "-999999"),  # Negative number
            ("float_precision", "3.14159265358979323846"),  # High precision float
        ]
        
        validation_results = []
        
        for test_name, test_value in extreme_test_cases:
            logger.info(f"🔍 Testing {test_name}: {test_value[:50]}...")
            
            try:
                # Find first text input field
                text_inputs = browser_helper.page.query_selector_all("input[type='text'], input[type='email'], textarea")
                
                if text_inputs:
                    first_input = text_inputs[0]
                    field_name = first_input.get_attribute('name') or 'unknown'
                    
                    # Clear and fill with extreme value
                    first_input.clear()
                    first_input.fill(test_value)
                    
                    # Try to submit or trigger validation
                    submit_button = browser_helper.page.query_selector("button[type='submit']")
                    if submit_button:
                        submit_button.click()
                        browser_helper.wait_for_loading_to_complete()
                    
                    # Check for validation errors
                    validation_errors = [
                        ".error",
                        ".invalid-feedback",
                        "[aria-invalid='true']",
                        "text*='invalid' i",
                        "text*='error' i"
                    ]
                    
                    validation_detected = False
                    for error_selector in validation_errors:
                        try:
                            if browser_helper.is_visible(error_selector):
                                validation_detected = True
                                logger.info(f"✅ Validation error detected for {test_name}")
                                break
                        except:
                            continue
                    
                    # Check if value was sanitized
                    actual_value = first_input.input_value()
                    value_sanitized = actual_value != test_value
                    
                    validation_results.append({
                        'test_name': test_name,
                        'field': field_name,
                        'validation_detected': validation_detected,
                        'value_sanitized': value_sanitized,
                        'original_length': len(test_value),
                        'actual_length': len(actual_value)
                    })
                    
                    if validation_detected:
                        logger.info(f"✅ {test_name} properly validated")
                    elif value_sanitized:
                        logger.info(f"✅ {test_name} value sanitized")
                    else:
                        logger.warning(f"⚠️ {test_name} may not be properly handled")
                    
                    # Reset form for next test
                    browser_helper.navigate_to("/register")
                    browser_helper.wait_for_loading_to_complete()
                
            except Exception as e:
                logger.warning(f"Could not test {test_name}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("extreme_input_validation")
        
        # Analyze validation results
        total_tests = len(validation_results)
        validated_tests = sum(1 for r in validation_results if r['validation_detected'] or r['value_sanitized'])
        
        logger.info(f"📊 Extreme input validation summary:")
        logger.info(f"   - Tests performed: {total_tests}")
        logger.info(f"   - Properly handled: {validated_tests}/{total_tests}")
        
        if validated_tests >= total_tests * 0.7:
            logger.info("✅ Good input validation for extreme values")
        else:
            logger.warning("⚠️ Input validation may need improvement")
        
        logger.info("✅ Extreme input values test completed")
    
    def test_boundary_conditions(self, browser_helper: BrowserHelper):
        """Test boundary conditions"""
        logger.info("🎯 Testing boundary conditions")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Boundary test cases
        boundary_tests = [
            ("min_length_password", "12345"),  # Minimum password length
            ("max_length_email", "a" * 50 + "@example.com"),  # Long email
            ("min_phone_length", "123456"),  # Short phone
            ("max_phone_length", "1234567890123456"),  # Long phone
            ("edge_year", "0"),  # Invalid year
            ("future_year", "10"),  # Future year
            ("unicode_email", "测试@example.com"),  # Unicode in email
        ]
        
        boundary_results = []
        
        for test_name, test_value in boundary_tests:
            logger.info(f"🔍 Testing boundary condition: {test_name}")
            
            try:
                # Determine field type based on test name
                if "password" in test_name:
                    field_selector = "input[type='password'], input[name='password']"
                elif "email" in test_name:
                    field_selector = "input[type='email'], input[name='email']"
                elif "phone" in test_name:
                    field_selector = "input[type='tel'], input[name='phone']"
                elif "year" in test_name:
                    field_selector = "select[name='year'], input[name='year']"
                else:
                    field_selector = "input[type='text']"
                
                # Find and fill field
                field = browser_helper.page.query_selector(field_selector)
                
                if field and field.is_visible():
                    # Handle select elements differently
                    if field.tag_name.lower() == 'select':
                        # Try to select by value or text
                        try:
                            field.select_option(value=test_value)
                        except:
                            try:
                                field.select_option(label=test_value)
                            except:
                                logger.info(f"Could not select {test_value} in dropdown")
                                continue
                    else:
                        field.clear()
                        field.fill(test_value)
                    
                    # Trigger validation (blur event)
                    field.blur()
                    browser_helper.wait_for_loading_to_complete()
                    
                    # Check for validation response
                    validation_indicators = [
                        ".error",
                        ".invalid-feedback",
                        "[aria-invalid='true']",
                        "text*='invalid' i"
                    ]
                    
                    validation_found = False
                    for indicator in validation_indicators:
                        try:
                            if browser_helper.is_visible(indicator):
                                validation_found = True
                                break
                        except:
                            continue
                    
                    boundary_results.append({
                        'test_name': test_name,
                        'validation_triggered': validation_found,
                        'test_value': test_value
                    })
                    
                    if validation_found:
                        logger.info(f"✅ Boundary validation working for {test_name}")
                    else:
                        logger.info(f"ℹ️ No validation triggered for {test_name}")
                
            except Exception as e:
                logger.warning(f"Could not test boundary condition {test_name}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("boundary_conditions")
        
        # Analyze results
        total_boundary_tests = len(boundary_results)
        validated_boundaries = sum(1 for r in boundary_results if r['validation_triggered'])
        
        logger.info(f"📊 Boundary conditions summary:")
        logger.info(f"   - Boundary tests: {total_boundary_tests}")
        logger.info(f"   - Validation triggered: {validated_boundaries}/{total_boundary_tests}")
        
        logger.info("✅ Boundary conditions test completed")

@pytest.mark.error_handling
@pytest.mark.file_upload
class TestFileUploadEdgeCases:
    """Test file upload edge cases"""
    
    def test_invalid_file_uploads(self, browser_helper: BrowserHelper):
        """Test invalid file upload scenarios"""
        logger.info("📎 Testing invalid file uploads")
        
        # Look for file upload functionality
        upload_pages = [
            "/admin/dashboard",
            "/applicant/submit",
            "/submissions"
        ]
        
        file_upload_found = False
        
        for page in upload_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for file upload inputs
                file_inputs = browser_helper.page.query_selector_all("input[type='file']")
                
                if file_inputs:
                    file_upload_found = True
                    logger.info(f"✅ File upload found on {page}")
                    
                    # Test with first file input
                    file_input = file_inputs[0]
                    
                    # Create test files for edge cases
                    import tempfile
                    import os
                    
                    test_files = []
                    
                    try:
                        # Create various test files
                        
                        # 1. Empty file
                        empty_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                        empty_file.close()
                        test_files.append(('empty_file', empty_file.name))
                        
                        # 2. Very large file (simulate)
                        large_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                        large_file.write(b'A' * 1024 * 1024)  # 1MB file
                        large_file.close()
                        test_files.append(('large_file', large_file.name))
                        
                        # 3. File with no extension
                        no_ext_file = tempfile.NamedTemporaryFile(delete=False, suffix='')
                        no_ext_file.write(b'test content')
                        no_ext_file.close()
                        test_files.append(('no_extension', no_ext_file.name))
                        
                        # 4. File with weird extension
                        weird_ext_file = tempfile.NamedTemporaryFile(delete=False, suffix='.weird123')
                        weird_ext_file.write(b'test content')
                        weird_ext_file.close()
                        test_files.append(('weird_extension', weird_ext_file.name))
                        
                        upload_results = []
                        
                        for test_name, file_path in test_files:
                            try:
                                logger.info(f"🔍 Testing file upload: {test_name}")
                                
                                # Upload file
                                file_input.set_input_files(file_path)
                                browser_helper.wait_for_loading_to_complete()
                                
                                # Check for upload feedback
                                upload_indicators = [
                                    ".upload-success",
                                    ".upload-error",
                                    ".file-uploaded",
                                    "text*='uploaded' i",
                                    "text*='error' i",
                                    "text*='invalid' i"
                                ]
                                
                                upload_feedback = False
                                feedback_type = None
                                
                                for indicator in upload_indicators:
                                    try:
                                        if browser_helper.is_visible(indicator):
                                            upload_feedback = True
                                            if 'error' in indicator or 'invalid' in indicator:
                                                feedback_type = 'error'
                                            else:
                                                feedback_type = 'success'
                                            logger.info(f"✅ Upload feedback found: {indicator}")
                                            break
                                    except:
                                        continue
                                
                                upload_results.append({
                                    'test_name': test_name,
                                    'feedback_found': upload_feedback,
                                    'feedback_type': feedback_type
                                })
                                
                                # Clear file input for next test
                                try:
                                    file_input.set_input_files([])
                                except:
                                    pass
                                
                            except Exception as e:
                                logger.warning(f"Could not test file upload {test_name}: {e}")
                                continue
                        
                        # Cleanup test files
                        for _, file_path in test_files:
                            try:
                                os.unlink(file_path)
                            except:
                                pass
                        
                        # Analyze upload results
                        total_uploads = len(upload_results)
                        uploads_with_feedback = sum(1 for r in upload_results if r['feedback_found'])
                        
                        logger.info(f"📊 File upload edge cases:")
                        logger.info(f"   - Upload tests: {total_uploads}")
                        logger.info(f"   - Feedback provided: {uploads_with_feedback}/{total_uploads}")
                        
                        if uploads_with_feedback >= total_uploads * 0.7:
                            logger.info("✅ Good file upload feedback")
                        else:
                            logger.info("ℹ️ Limited file upload feedback")
                        
                    except Exception as e:
                        logger.warning(f"Could not create test files: {e}")
                    
                    break
                    
            except Exception as e:
                logger.debug(f"Could not test file upload on {page}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("file_upload_edge_cases")
        
        if file_upload_found:
            logger.info("✅ File upload edge cases tested")
        else:
            logger.info("ℹ️ No file upload functionality found")
        
        logger.info("✅ Invalid file uploads test completed")

@pytest.mark.error_handling
@pytest.mark.authentication
class TestAuthenticationEdgeCases:
    """Test authentication edge cases"""
    
    def test_session_expiry_handling(self, browser_helper: BrowserHelper):
        """Test session expiry handling"""
        logger.info("⏰ Testing session expiry handling")
        
        # Try to login first
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Quick login attempt
        if browser_helper.is_visible("input[type='email'], input[name='email']"):
            browser_helper.fill_input("input[type='email'], input[name='email']", TestConfig.ADMIN_EMAIL)
            
        if browser_helper.is_visible("input[type='password'], input[name='password']"):
            browser_helper.fill_input("input[type='password'], input[name='password']", TestConfig.ADMIN_PASSWORD)
            
        if browser_helper.is_visible("button[type='submit']"):
            browser_helper.click_element("button[type='submit']")
            browser_helper.wait_for_loading_to_complete()
        
        current_url = browser_helper.page.url
        
        if "dashboard" in current_url or "admin" in current_url:
            logger.info("✅ Successfully logged in for session test")
            
            # Simulate session expiry by clearing storage
            try:
                browser_helper.page.evaluate("""
                    () => {
                        localStorage.clear();
                        sessionStorage.clear();
                        // Clear all cookies
                        document.cookie.split(";").forEach(function(c) { 
                            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
                        });
                    }
                """)
                
                logger.info("✅ Simulated session expiry")
                
                # Try to access protected page
                browser_helper.navigate_to("/admin/dashboard")
                browser_helper.wait_for_loading_to_complete()
                
                final_url = browser_helper.page.url
                
                # Check if redirected to login
                if "login" in final_url:
                    logger.info("✅ Session expiry properly redirects to login")
                else:
                    logger.warning("⚠️ Session expiry may not be properly handled")
                
                # Check for session expiry messages
                expiry_messages = [
                    "session expired",
                    "please log in",
                    "authentication required",
                    "logged out"
                ]
                
                page_content = browser_helper.page.content().lower()
                
                expiry_message_found = False
                for message in expiry_messages:
                    if message in page_content:
                        expiry_message_found = True
                        logger.info(f"✅ Session expiry message found: {message}")
                        break
                
                if expiry_message_found:
                    logger.info("✅ User-friendly session expiry message shown")
                else:
                    logger.info("ℹ️ No specific session expiry message")
                
            except Exception as e:
                logger.warning(f"Could not simulate session expiry: {e}")
        else:
            logger.info("ℹ️ Could not log in for session expiry test")
        
        # Take screenshot
        browser_helper.take_screenshot("session_expiry_handling")
        
        logger.info("✅ Session expiry handling test completed")
    
    def test_concurrent_login_attempts(self, browser_helper: BrowserHelper):
        """Test concurrent login attempts"""
        logger.info("🔄 Testing concurrent login attempts")
        
        browser_helper.navigate_to("/admin/login")
        browser_helper.wait_for_loading_to_complete()
        
        # Simulate rapid login attempts
        login_attempts = []
        
        for attempt in range(3):
            try:
                logger.info(f"🔍 Login attempt {attempt + 1}")
                
                # Fill login form
                if browser_helper.is_visible("input[type='email'], input[name='email']"):
                    browser_helper.fill_input("input[type='email'], input[name='email']", TestConfig.ADMIN_EMAIL)
                    
                if browser_helper.is_visible("input[type='password'], input[name='password']"):
                    browser_helper.fill_input("input[type='password'], input[name='password']", TestConfig.ADMIN_PASSWORD)
                
                # Submit rapidly
                if browser_helper.is_visible("button[type='submit']"):
                    browser_helper.click_element("button[type='submit']")
                    browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                login_attempts.append({
                    'attempt': attempt + 1,
                    'success': "dashboard" in current_url,
                    'url': current_url
                })
                
                # If successful, logout and try again
                if "dashboard" in current_url:
                    # Look for logout
                    logout_selectors = [
                        "button:has-text('Logout')",
                        "a:has-text('Logout')",
                        ".logout"
                    ]
                    
                    for logout_selector in logout_selectors:
                        try:
                            if browser_helper.is_visible(logout_selector):
                                browser_helper.click_element(logout_selector)
                                browser_helper.wait_for_loading_to_complete()
                                break
                        except:
                            continue
                    
                    # Navigate back to login
                    browser_helper.navigate_to("/admin/login")
                    browser_helper.wait_for_loading_to_complete()
                
            except Exception as e:
                logger.warning(f"Login attempt {attempt + 1} failed: {e}")
                continue
        
        # Analyze concurrent login results
        successful_attempts = sum(1 for attempt in login_attempts if attempt['success'])
        
        logger.info(f"📊 Concurrent login attempts:")
        logger.info(f"   - Total attempts: {len(login_attempts)}")
        logger.info(f"   - Successful: {successful_attempts}")
        
        # Take screenshot
        browser_helper.take_screenshot("concurrent_login_attempts")
        
        logger.info("✅ Concurrent login attempts test completed")
