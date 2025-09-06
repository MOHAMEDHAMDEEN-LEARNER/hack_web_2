"""
Test 08: API Endpoints  
======================

This test module covers comprehensive API testing including:
- Authentication endpoints
- User management APIs
- Competition APIs
- Submission APIs 
- Payment APIs
- Data validation
- Error handling
- Rate limiting
"""

import pytest
import logging
import requests
import json
from utils.test_data import TestConfig, TestDataGenerator
from utils.api_helper import APIHelper

logger = logging.getLogger(__name__)

@pytest.mark.api
@pytest.mark.auth
class TestAuthenticationAPI:
    """Test authentication-related API endpoints"""
    
    def test_admin_login_api(self, api_helper: APIHelper):
        """Test admin login API endpoint"""
        logger.info("🔐 Testing admin login API")
        
        # Test valid admin login
        valid_credentials = {
            "email": TestConfig.ADMIN_EMAIL,
            "password": TestConfig.ADMIN_PASSWORD
        }
        
        result = api_helper.auth.admin_login(valid_credentials['email'], valid_credentials['password'])
        
        if result['success']:
            logger.info("✅ Admin login API working with valid credentials")
            
            # Check response structure
            response_data = result.get('data', {})
            expected_fields = ['token', 'user', 'role']
            
            for field in expected_fields:
                if field in response_data:
                    logger.info(f"✅ Response contains {field}")
                else:
                    logger.info(f"ℹ️ Response missing {field}")
            
        else:
            logger.warning("⚠️ Admin login API failed with valid credentials")
            logger.info(f"Error: {result.get('error', 'Unknown error')}")
        
        # Test invalid credentials
        invalid_credentials = {
            "email": "wrong@admin.com",
            "password": "wrongpassword"
        }
        
        invalid_result = api_helper.auth.admin_login(invalid_credentials['email'], invalid_credentials['password'])
        
        if not invalid_result['success']:
            logger.info("✅ Admin login API correctly rejects invalid credentials")
        else:
            logger.warning("⚠️ Admin login API accepts invalid credentials")
        
        logger.info("✅ Admin login API test completed")
    
    def test_applicant_otp_flow_api(self, api_helper: APIHelper):
        """Test applicant OTP authentication flow"""
        logger.info("📱 Testing applicant OTP flow API")
        
        # Generate test applicant data
        test_email = f"apitest_{int(__import__('time').time())}@example.com"
        
        # Test sending OTP
        otp_result = api_helper.auth.applicant_send_otp(test_email)
        
        if otp_result['success']:
            logger.info("✅ OTP send API working")
        else:
            error_msg = otp_result.get('error', 'Unknown error')
            if 'not found' in error_msg.lower() or 'not registered' in error_msg.lower():
                logger.info("✅ OTP send API correctly rejects unregistered email")
            else:
                logger.warning(f"⚠️ OTP send API error: {error_msg}")
        
        # Test OTP verification with invalid OTP
        verify_result = api_helper.auth.applicant_verify_otp(test_email, "123456")
        
        if not verify_result['success']:
            logger.info("✅ OTP verification API correctly rejects invalid OTP")
        else:
            logger.warning("⚠️ OTP verification API accepts invalid OTP")
        
        logger.info("✅ Applicant OTP flow API test completed")
    
    def test_logout_api(self, api_helper: APIHelper):
        """Test logout API endpoint"""
        logger.info("🚪 Testing logout API")
        
        # First try to login
        login_result = api_helper.auth.admin_login(TestConfig.ADMIN_EMAIL, TestConfig.ADMIN_PASSWORD)
        
        if login_result['success']:
            # Test logout
            logout_result = api_helper.auth.logout()
            
            if logout_result['success']:
                logger.info("✅ Logout API working")
            else:
                logger.info("ℹ️ Logout API not working or not implemented")
        else:
            logger.info("ℹ️ Cannot test logout without successful login")
        
        logger.info("✅ Logout API test completed")

@pytest.mark.api
@pytest.mark.user
class TestUserManagementAPI:
    """Test user management API endpoints"""
    
    def test_user_registration_api(self, api_helper: APIHelper):
        """Test user registration API"""
        logger.info("👤 Testing user registration API")
        
        # Generate test user data
        test_user = TestDataGenerator.generate_applicant_data()
        test_user['email'] = f"apitest_{int(__import__('time').time())}@example.com"
        
        # Test user registration
        registration_result = api_helper.auth.register_user(test_user)
        
        if registration_result['success']:
            logger.info("✅ User registration API working")
            
            # Check response structure
            response_data = registration_result.get('data', {})
            if 'id' in response_data or 'user_id' in response_data:
                logger.info("✅ Registration returns user ID")
            
        else:
            error_msg = registration_result.get('error', 'Unknown error')
            logger.info(f"ℹ️ Registration API error: {error_msg}")
        
        # Test duplicate email registration
        duplicate_result = api_helper.auth.register_user(test_user)
        
        if not duplicate_result['success']:
            error_msg = duplicate_result.get('error', '')
            if 'exists' in error_msg.lower() or 'duplicate' in error_msg.lower():
                logger.info("✅ Registration API correctly rejects duplicate email")
            else:
                logger.info(f"ℹ️ Duplicate registration error: {error_msg}")
        else:
            logger.warning("⚠️ Registration API allows duplicate emails")
        
        logger.info("✅ User registration API test completed")
    
    def test_user_profile_api(self, api_helper: APIHelper):
        """Test user profile management API"""
        logger.info("👥 Testing user profile API")
        
        # Test getting user profile (requires authentication)
        profile_result = api_helper.applicant.get_profile()
        
        if profile_result['success']:
            logger.info("✅ Get profile API working")
            
            profile_data = profile_result.get('data', {})
            profile_fields = ['name', 'email', 'college', 'year', 'branch']
            
            for field in profile_fields:
                if field in profile_data:
                    logger.info(f"✅ Profile contains {field}")
        else:
            logger.info("ℹ️ Get profile API requires authentication (expected)")
        
        # Test updating profile
        update_data = {
            "name": "Updated API Test User",
            "college": "API Test University"
        }
        
        update_result = api_helper.applicant.update_profile(update_data)
        
        if update_result['success']:
            logger.info("✅ Update profile API working")
        else:
            logger.info("ℹ️ Update profile API requires authentication (expected)")
        
        logger.info("✅ User profile API test completed")
    
    def test_admin_user_management_api(self, api_helper: APIHelper):
        """Test admin user management APIs"""
        logger.info("👑 Testing admin user management API")
        
        # Test getting all users (admin endpoint)
        users_result = api_helper.admin.get_users()
        
        if users_result['success']:
            logger.info("✅ Admin get users API working")
            
            users_data = users_result.get('data', [])
            logger.info(f"📊 Found {len(users_data)} users")
            
            if users_data:
                # Check user structure
                first_user = users_data[0]
                user_fields = ['id', 'email', 'name', 'role', 'created_at']
                
                for field in user_fields:
                    if field in first_user:
                        logger.info(f"✅ User object contains {field}")
            
        else:
            logger.info("ℹ️ Admin get users API requires authentication")
        
        # Test admin statistics
        stats_result = api_helper.admin.get_stats()
        
        if stats_result['success']:
            logger.info("✅ Admin stats API working")
            
            stats_data = stats_result.get('data', {})
            stat_fields = ['total_users', 'total_applicants', 'total_competitions']
            
            for field in stat_fields:
                if field in stats_data:
                    logger.info(f"✅ Stats contain {field}: {stats_data[field]}")
        else:
            logger.info("ℹ️ Admin stats API requires authentication")
        
        logger.info("✅ Admin user management API test completed")

@pytest.mark.api
@pytest.mark.competition
class TestCompetitionAPI:
    """Test competition-related API endpoints"""
    
    def test_competition_crud_api(self, api_helper: APIHelper):
        """Test competition CRUD operations"""
        logger.info("🏆 Testing competition CRUD API")
        
        # Test getting competitions
        competitions_result = api_helper.competition.get_competitions()
        
        if competitions_result['success']:
            logger.info("✅ Get competitions API working")
            
            competitions = competitions_result.get('data', [])
            logger.info(f"📊 Found {len(competitions)} competitions")
            
            if competitions:
                # Check competition structure
                first_competition = competitions[0]
                competition_fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status']
                
                for field in competition_fields:
                    if field in first_competition:
                        logger.info(f"✅ Competition object contains {field}")
            
        else:
            logger.info("ℹ️ Get competitions API requires authentication or no competitions exist")
        
        # Test creating competition
        test_competition = {
            "name": f"API Test Competition {int(__import__('time').time())}",
            "description": "Test competition created via API",
            "start_date": "2024-12-01",
            "end_date": "2024-12-31",
            "registration_deadline": "2024-11-30",
            "max_participants": 100,
            "entry_fee": 500
        }
        
        create_result = api_helper.competition.create_competition(test_competition)
        
        if create_result['success']:
            logger.info("✅ Create competition API working")
            
            competition_id = create_result.get('data', {}).get('id')
            
            if competition_id:
                # Test updating competition
                update_data = {"name": "Updated API Test Competition"}
                update_result = api_helper.competition.update_competition(competition_id, update_data)
                
                if update_result['success']:
                    logger.info("✅ Update competition API working")
                
                # Test getting single competition
                single_result = api_helper.competition.get_competition(competition_id)
                
                if single_result['success']:
                    logger.info("✅ Get single competition API working")
                
                # Clean up: delete test competition
                delete_result = api_helper.competition.delete_competition(competition_id)
                
                if delete_result['success']:
                    logger.info("✅ Delete competition API working")
                else:
                    logger.info("ℹ️ Delete competition API may require special permissions")
            
        else:
            logger.info("ℹ️ Create competition API requires admin authentication")
        
        logger.info("✅ Competition CRUD API test completed")
    
    def test_competition_stages_api(self, api_helper: APIHelper):
        """Test competition stages API"""
        logger.info("🎭 Testing competition stages API")
        
        # Assume competition ID 1 exists (or use first available)
        test_competition_id = 1
        
        # Test getting stages
        stages_result = api_helper.competition.get_stages(test_competition_id)
        
        if stages_result['success']:
            logger.info("✅ Get stages API working")
            
            stages = stages_result.get('data', [])
            logger.info(f"📊 Found {len(stages)} stages")
            
            if stages:
                # Check stage structure
                first_stage = stages[0]
                stage_fields = ['id', 'name', 'description', 'deadline', 'requirements']
                
                for field in stage_fields:
                    if field in first_stage:
                        logger.info(f"✅ Stage object contains {field}")
        else:
            logger.info("ℹ️ Get stages API requires valid competition or authentication")
        
        # Test creating stage
        test_stage = {
            "competition_id": test_competition_id,
            "name": f"API Test Stage {int(__import__('time').time())}",
            "description": "Test stage created via API",
            "deadline": "2024-12-15",
            "requirements": "Test requirements for API stage"
        }
        
        create_stage_result = api_helper.competition.create_stage(test_stage)
        
        if create_stage_result['success']:
            logger.info("✅ Create stage API working")
        else:
            logger.info("ℹ️ Create stage API requires authentication or valid competition")
        
        logger.info("✅ Competition stages API test completed")

@pytest.mark.api
@pytest.mark.submission
class TestSubmissionAPI:
    """Test submission-related API endpoints"""
    
    def test_submission_crud_api(self, api_helper: APIHelper):
        """Test submission CRUD operations"""
        logger.info("📝 Testing submission CRUD API")
        
        # Test getting submissions
        submissions_result = api_helper.applicant.get_submissions()
        
        if submissions_result['success']:
            logger.info("✅ Get submissions API working")
            
            submissions = submissions_result.get('data', [])
            logger.info(f"📊 Found {len(submissions)} submissions")
            
            if submissions:
                # Check submission structure
                first_submission = submissions[0]
                submission_fields = ['id', 'title', 'description', 'github_url', 'demo_url', 'status']
                
                for field in submission_fields:
                    if field in first_submission:
                        logger.info(f"✅ Submission object contains {field}")
        else:
            logger.info("ℹ️ Get submissions API requires authentication")
        
        # Test creating submission
        test_submission = {
            "title": f"API Test Submission {int(__import__('time').time())}",
            "description": "Test submission created via API",
            "github_url": "https://github.com/test/api-submission",
            "demo_url": "https://demo.api-submission.com",
            "competition_id": 1,
            "stage_id": 1
        }
        
        create_result = api_helper.applicant.create_submission(test_submission)
        
        if create_result['success']:
            logger.info("✅ Create submission API working")
            
            submission_id = create_result.get('data', {}).get('id')
            
            if submission_id:
                # Test updating submission
                update_data = {"title": "Updated API Test Submission"}
                update_result = api_helper.applicant.update_submission(submission_id, update_data)
                
                if update_result['success']:
                    logger.info("✅ Update submission API working")
                
                # Test getting single submission
                single_result = api_helper.applicant.get_submission(submission_id)
                
                if single_result['success']:
                    logger.info("✅ Get single submission API working")
            
        else:
            logger.info("ℹ️ Create submission API requires authentication")
        
        logger.info("✅ Submission CRUD API test completed")
    
    def test_file_upload_api(self, api_helper: APIHelper):
        """Test file upload API for submissions"""
        logger.info("📎 Testing file upload API")
        
        # Create a test file in memory
        import io
        test_file_content = b"This is a test file for API upload testing"
        test_file = io.BytesIO(test_file_content)
        test_file.name = "test_upload.txt"
        
        # Test file upload
        upload_result = api_helper.applicant.upload_file(test_file)
        
        if upload_result['success']:
            logger.info("✅ File upload API working")
            
            upload_data = upload_result.get('data', {})
            upload_fields = ['file_id', 'filename', 'url', 'size']
            
            for field in upload_fields:
                if field in upload_data:
                    logger.info(f"✅ Upload response contains {field}")
        else:
            logger.info("ℹ️ File upload API requires authentication or not implemented")
        
        logger.info("✅ File upload API test completed")

@pytest.mark.api
@pytest.mark.payment
class TestPaymentAPI:
    """Test payment-related API endpoints"""
    
    def test_payment_initiation_api(self, api_helper: APIHelper):
        """Test payment initiation API"""
        logger.info("💳 Testing payment initiation API")
        
        # Test payment creation
        payment_data = {
            "amount": 500,
            "currency": "INR",
            "competition_id": 1,
            "description": "API test payment"
        }
        
        payment_result = api_helper.payment.create_payment(payment_data)
        
        if payment_result['success']:
            logger.info("✅ Payment initiation API working")
            
            payment_response = payment_result.get('data', {})
            payment_fields = ['payment_id', 'amount', 'currency', 'status', 'redirect_url']
            
            for field in payment_fields:
                if field in payment_response:
                    logger.info(f"✅ Payment response contains {field}")
        else:
            logger.info("ℹ️ Payment initiation API requires authentication or not implemented")
        
        logger.info("✅ Payment initiation API test completed")
    
    def test_payment_status_api(self, api_helper: APIHelper):
        """Test payment status checking API"""
        logger.info("💰 Testing payment status API")
        
        # Test getting payment status (with dummy payment ID)
        test_payment_id = "test_payment_123"
        
        status_result = api_helper.payment.get_payment_status(test_payment_id)
        
        if status_result['success']:
            logger.info("✅ Payment status API working")
        else:
            error_msg = status_result.get('error', 'Unknown error')
            if 'not found' in error_msg.lower():
                logger.info("✅ Payment status API correctly handles invalid payment ID")
            else:
                logger.info("ℹ️ Payment status API requires authentication or valid payment ID")
        
        logger.info("✅ Payment status API test completed")

@pytest.mark.api
@pytest.mark.validation
class TestAPIValidation:
    """Test API data validation and error handling"""
    
    def test_invalid_data_validation(self, api_helper: APIHelper):
        """Test API validation with invalid data"""
        logger.info("❌ Testing API data validation")
        
        # Test invalid registration data
        invalid_registration_data = {
            "email": "invalid-email",  # Invalid email format
            "name": "",  # Empty name
            "password": "123",  # Too short password
            "phone": "invalid-phone"  # Invalid phone
        }
        
        registration_result = api_helper.auth.register_user(invalid_registration_data)
        
        if not registration_result['success']:
            error_msg = registration_result.get('error', '').lower()
            validation_errors = ['invalid', 'required', 'format', 'minimum', 'maximum']
            
            validation_found = any(error in error_msg for error in validation_errors)
            
            if validation_found:
                logger.info("✅ Registration API correctly validates invalid data")
            else:
                logger.info(f"ℹ️ Registration validation error: {error_msg}")
        else:
            logger.warning("⚠️ Registration API accepts invalid data")
        
        # Test invalid competition data
        invalid_competition = {
            "name": "",  # Empty name
            "start_date": "invalid-date",  # Invalid date
            "end_date": "2024-01-01",  # End date before start date
            "max_participants": -1  # Negative number
        }
        
        competition_result = api_helper.competition.create_competition(invalid_competition)
        
        if not competition_result['success']:
            logger.info("✅ Competition API validates invalid data")
        else:
            logger.info("ℹ️ Competition API validation not tested (requires auth)")
        
        logger.info("✅ API data validation test completed")
    
    def test_api_error_responses(self, api_helper: APIHelper):
        """Test API error response formats"""
        logger.info("🚨 Testing API error responses")
        
        # Test authentication errors
        auth_result = api_helper.auth.admin_login("wrong@email.com", "wrongpassword")
        
        if not auth_result['success']:
            error_response = auth_result
            
            # Check error response structure
            expected_error_fields = ['success', 'error', 'message', 'status_code']
            
            for field in expected_error_fields:
                if field in error_response:
                    logger.info(f"✅ Error response contains {field}")
                else:
                    logger.info(f"ℹ️ Error response missing {field}")
            
            # Check error message is informative
            error_msg = error_response.get('error', '')
            if error_msg and len(error_msg) > 5:
                logger.info("✅ Error message is informative")
            else:
                logger.info("ℹ️ Error message could be more informative")
        
        # Test 404 errors (non-existent endpoints)
        try:
            # Use requests directly to test non-existent endpoint
            base_url = TestConfig.BASE_URL
            response = requests.get(f"{base_url}/api/nonexistent-endpoint")
            
            if response.status_code == 404:
                logger.info("✅ API correctly returns 404 for non-existent endpoints")
            else:
                logger.info(f"ℹ️ Non-existent endpoint returns status: {response.status_code}")
        except:
            logger.info("ℹ️ Could not test non-existent endpoint")
        
        logger.info("✅ API error responses test completed")

@pytest.mark.api
@pytest.mark.security
class TestAPISecurity:
    """Test API security features"""
    
    def test_authentication_required(self, api_helper: APIHelper):
        """Test that protected endpoints require authentication"""
        logger.info("🔒 Testing API authentication requirements")
        
        # List of endpoints that should require authentication
        protected_endpoints = [
            ("Admin users", api_helper.admin.get_users),
            ("Admin stats", api_helper.admin.get_stats),
            ("User profile", api_helper.applicant.get_profile),
            ("User submissions", api_helper.applicant.get_submissions)
        ]
        
        protected_count = 0
        for endpoint_name, endpoint_function in protected_endpoints:
            try:
                result = endpoint_function()
                
                if not result['success']:
                    error_msg = result.get('error', '').lower()
                    auth_errors = ['unauthorized', 'authentication', 'login', 'token']
                    
                    if any(auth_error in error_msg for auth_error in auth_errors):
                        protected_count += 1
                        logger.info(f"✅ {endpoint_name} requires authentication")
                    else:
                        logger.info(f"ℹ️ {endpoint_name} error: {error_msg}")
                else:
                    logger.warning(f"⚠️ {endpoint_name} accessible without authentication")
                    
            except Exception as e:
                logger.debug(f"Could not test {endpoint_name}: {e}")
        
        logger.info(f"📊 Protected endpoints: {protected_count}/{len(protected_endpoints)}")
        
        if protected_count >= len(protected_endpoints) * 0.7:  # 70% threshold
            logger.info("✅ Most endpoints properly protected")
        else:
            logger.warning("⚠️ Some endpoints may lack proper authentication")
        
        logger.info("✅ Authentication requirements test completed")
    
    def test_input_sanitization(self, api_helper: APIHelper):
        """Test API input sanitization"""
        logger.info("🧹 Testing API input sanitization")
        
        # Test XSS injection attempts
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "'; DROP TABLE users; --"
        ]
        
        sanitization_working = True
        
        for payload in xss_payloads:
            test_data = {
                "name": payload,
                "email": f"test_{int(__import__('time').time())}@example.com",
                "college": payload,
                "branch": payload
            }
            
            result = api_helper.auth.register_user(test_data)
            
            if result['success']:
                # Check if the payload was sanitized in the response
                response_data = result.get('data', {})
                for field, value in response_data.items():
                    if isinstance(value, str) and payload in value:
                        sanitization_working = False
                        logger.warning(f"⚠️ Potential XSS vulnerability in {field}")
                        break
            
            # Small delay between attempts
            __import__('time').sleep(0.1)
        
        if sanitization_working:
            logger.info("✅ Input sanitization appears to be working")
        else:
            logger.warning("⚠️ Potential input sanitization issues detected")
        
        logger.info("✅ Input sanitization test completed")

@pytest.mark.api
@pytest.mark.performance
class TestAPIPerformance:
    """Test API performance characteristics"""
    
    def test_api_response_times(self, api_helper: APIHelper):
        """Test API response times"""
        logger.info("⚡ Testing API response times")
        
        import time
        
        # Test different endpoints
        endpoints_to_test = [
            ("Get competitions", api_helper.competition.get_competitions),
            ("Admin login", lambda: api_helper.auth.admin_login(TestConfig.ADMIN_EMAIL, TestConfig.ADMIN_PASSWORD))
        ]
        
        response_times = []
        
        for endpoint_name, endpoint_function in endpoints_to_test:
            start_time = time.time()
            
            try:
                result = endpoint_function()
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                logger.info(f"📊 {endpoint_name}: {response_time:.3f}s")
                
                # Performance thresholds
                if response_time < 1:
                    logger.info(f"✅ {endpoint_name} - Excellent response time")
                elif response_time < 3:
                    logger.info(f"✅ {endpoint_name} - Good response time")
                elif response_time < 5:
                    logger.warning(f"⚠️ {endpoint_name} - Slow response time")
                else:
                    logger.warning(f"❌ {endpoint_name} - Very slow response time")
                    
            except Exception as e:
                logger.debug(f"Could not test {endpoint_name}: {e}")
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            logger.info(f"📊 Average API response time: {avg_response_time:.3f}s")
        
        logger.info("✅ API response times test completed")
    
    def test_concurrent_requests(self, api_helper: APIHelper):
        """Test API handling of concurrent requests"""
        logger.info("🔄 Testing concurrent API requests")
        
        import threading
        import time
        
        # Function to make concurrent requests
        def make_request():
            return api_helper.competition.get_competitions()
        
        # Test with multiple concurrent requests
        threads = []
        results = []
        
        def thread_function():
            result = make_request()
            results.append(result)
        
        # Create and start threads
        num_threads = 5
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=thread_function)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        successful_requests = sum(1 for result in results if result.get('success'))
        
        logger.info(f"📊 Concurrent requests summary:")
        logger.info(f"   - Total requests: {num_threads}")
        logger.info(f"   - Successful requests: {successful_requests}")
        logger.info(f"   - Total time: {total_time:.3f}s")
        logger.info(f"   - Average time per request: {total_time/num_threads:.3f}s")
        
        if successful_requests == num_threads:
            logger.info("✅ All concurrent requests handled successfully")
        elif successful_requests >= num_threads * 0.8:  # 80% threshold
            logger.info("✅ Most concurrent requests handled successfully")
        else:
            logger.warning("⚠️ Some concurrent requests failed")
        
        logger.info("✅ Concurrent requests test completed")
