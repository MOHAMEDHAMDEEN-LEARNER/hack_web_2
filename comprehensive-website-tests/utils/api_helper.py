"""
API Testing Helper Utilities
============================
"""

import requests
import logging
import json
from typing import Dict, Any, Optional
from .test_data import TestConfig

logger = logging.getLogger(__name__)

class APIHelper:
    """Helper for API testing and interactions"""
    
    def __init__(self):
        self.config = TestConfig()
        self.base_url = self.config.API_BASE_URL
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get(self, endpoint: str, params: Dict = None, headers: Dict = None) -> requests.Response:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        
        if headers:
            self.session.headers.update(headers)
        
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params)
        
        logger.info(f"Response: {response.status_code} - {response.reason}")
        return response
    
    def post(self, endpoint: str, data: Dict = None, headers: Dict = None) -> requests.Response:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        
        if headers:
            self.session.headers.update(headers)
        
        logger.info(f"POST {url}")
        if data:
            logger.debug(f"Data: {json.dumps(data, indent=2)}")
        
        response = self.session.post(url, json=data)
        
        logger.info(f"Response: {response.status_code} - {response.reason}")
        return response
    
    def put(self, endpoint: str, data: Dict = None, headers: Dict = None) -> requests.Response:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        
        if headers:
            self.session.headers.update(headers)
        
        logger.info(f"PUT {url}")
        response = self.session.put(url, json=data)
        
        logger.info(f"Response: {response.status_code} - {response.reason}")
        return response
    
    def delete(self, endpoint: str, headers: Dict = None) -> requests.Response:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        
        if headers:
            self.session.headers.update(headers)
        
        logger.info(f"DELETE {url}")
        response = self.session.delete(url)
        
        logger.info(f"Response: {response.status_code} - {response.reason}")
        return response
    
    def set_auth_token(self, token: str):
        """Set authorization token for subsequent requests"""
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
        logger.info("Authorization token set")
    
    def clear_auth(self):
        """Clear authorization headers"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        logger.info("Authorization cleared")

class AuthAPIHelper:
    """Helper for authentication-related API calls"""
    
    def __init__(self, api_helper: APIHelper):
        self.api = api_helper
        self.config = TestConfig()
    
    def admin_login(self, email: str = None, password: str = None) -> Dict:
        """Login as admin and return session info"""
        credentials = {
            'email': email or self.config.ADMIN_CREDENTIALS['email'],
            'password': password or self.config.ADMIN_CREDENTIALS['password']
        }
        
        response = self.api.post('/auth/login', credentials)
        
        if response.status_code == 200:
            data = response.json()
            logger.info("Admin login successful")
            return {
                'success': True,
                'user': data.get('user'),
                'session': response.cookies
            }
        else:
            logger.error(f"Admin login failed: {response.text}")
            return {
                'success': False,
                'error': response.text
            }
    
    def applicant_send_otp(self, identifier: str) -> Dict:
        """Send OTP for applicant login"""
        data = {'identifier': identifier}
        response = self.api.post('/applicant/send-otp', data)
        
        if response.status_code == 200:
            logger.info(f"OTP sent to {identifier}")
            return {'success': True, 'data': response.json()}
        else:
            logger.error(f"Failed to send OTP: {response.text}")
            return {'success': False, 'error': response.text}
    
    def applicant_verify_otp(self, identifier: str, otp: str) -> Dict:
        """Verify OTP and login applicant"""
        data = {
            'identifier': identifier,
            'otp': otp
        }
        response = self.api.post('/applicant/verify-otp', data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Set auth token for subsequent requests
                self.api.set_auth_token(data['sessionToken'])
                logger.info("Applicant login successful")
                return {
                    'success': True,
                    'token': data['sessionToken'],
                    'applicant': data['applicant']
                }
        
        logger.error(f"OTP verification failed: {response.text}")
        return {'success': False, 'error': response.text}
    
    def logout(self) -> Dict:
        """Logout current user"""
        response = self.api.post('/auth/logout')
        self.api.clear_auth()
        
        return {
            'success': response.status_code in [200, 302],
            'status_code': response.status_code
        }

class RegistrationAPIHelper:
    """Helper for registration-related API calls"""
    
    def __init__(self, api_helper: APIHelper):
        self.api = api_helper
    
    def register_applicant(self, applicant_data: Dict) -> Dict:
        """Register a new applicant"""
        response = self.api.post('/register', applicant_data)
        
        if response.status_code in [200, 201]:
            data = response.json()
            logger.info(f"Applicant registered: {applicant_data['email']}")
            return {
                'success': True,
                'data': data,
                'registration_id': data.get('registrationId')
            }
        else:
            logger.error(f"Registration failed: {response.text}")
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }
    
    def confirm_participation(self, confirmation_code: str) -> Dict:
        """Confirm participation with code"""
        data = {'code': confirmation_code}
        response = self.api.post('/confirm-participation', data)
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }

class AdminAPIHelper:
    """Helper for admin-specific API calls"""
    
    def __init__(self, api_helper: APIHelper):
        self.api = api_helper
    
    def get_applicants(self, page: int = 1, limit: int = 10, filters: Dict = None) -> Dict:
        """Get list of applicants"""
        params = {
            'page': page,
            'limit': limit
        }
        
        if filters:
            params.update(filters)
        
        response = self.api.get('/applicants', params)
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        else:
            return {
                'success': False,
                'error': response.text
            }
    
    def create_applicant(self, applicant_data: Dict) -> Dict:
        """Create applicant as admin"""
        response = self.api.post('/applicants', applicant_data)
        
        return {
            'success': response.status_code in [200, 201],
            'data': response.json() if response.status_code in [200, 201] else None,
            'error': response.text if response.status_code not in [200, 201] else None
        }
    
    def update_applicant(self, applicant_id: str, updates: Dict) -> Dict:
        """Update applicant information"""
        response = self.api.put(f'/applicants/{applicant_id}', updates)
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def delete_applicant(self, applicant_id: str) -> Dict:
        """Delete an applicant"""
        response = self.api.delete(f'/applicants/{applicant_id}')
        
        return {
            'success': response.status_code == 200,
            'message': response.json().get('message') if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def get_dashboard_stats(self) -> Dict:
        """Get admin dashboard statistics"""
        response = self.api.get('/dashboard/stats')
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def export_applicants(self, filters: Dict = None) -> Dict:
        """Export applicants data"""
        data = filters or {}
        response = self.api.post('/admin/export-applicants', data)
        
        return {
            'success': response.status_code == 200,
            'content': response.content if response.status_code == 200 else None,
            'content_type': response.headers.get('content-type'),
            'error': response.text if response.status_code != 200 else None
        }
    
    def clear_all_applicants(self) -> Dict:
        """Clear all applicant data"""
        response = self.api.delete('/admin/clear-applicants')
        
        return {
            'success': response.status_code == 200,
            'message': response.json().get('message') if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }

class CompetitionAPIHelper:
    """Helper for competition management API calls"""
    
    def __init__(self, api_helper: APIHelper):
        self.api = api_helper
    
    def get_rounds(self) -> Dict:
        """Get competition rounds"""
        response = self.api.get('/rounds')
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def create_round(self, round_data: Dict) -> Dict:
        """Create a new competition round"""
        response = self.api.post('/rounds', round_data)
        
        return {
            'success': response.status_code in [200, 201],
            'data': response.json() if response.status_code in [200, 201] else None,
            'error': response.text if response.status_code not in [200, 201] else None
        }
    
    def update_round(self, round_id: str, updates: Dict) -> Dict:
        """Update competition round"""
        response = self.api.put(f'/rounds/{round_id}', updates)
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }

class ApplicantAPIHelper:
    """Helper for applicant portal API calls"""
    
    def __init__(self, api_helper: APIHelper):
        self.api = api_helper
    
    def get_dashboard(self) -> Dict:
        """Get applicant dashboard data"""
        response = self.api.get('/applicant/dashboard')
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def submit_stage(self, stage_id: str, submission_data: Dict) -> Dict:
        """Submit for a competition stage"""
        data = {
            'stageId': stage_id,
            **submission_data
        }
        response = self.api.post('/applicant/submit-stage', data)
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def get_submissions(self) -> Dict:
        """Get applicant's submissions"""
        response = self.api.get('/applicant/submissions')
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }
    
    def confirm_participation(self) -> Dict:
        """Confirm participation in competition"""
        response = self.api.post('/applicant/confirm-participation')
        
        return {
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }

# Comprehensive API test helper that combines all helpers
class ComprehensiveAPIHelper:
    """Main API helper that provides access to all API functionality"""
    
    def __init__(self):
        self.api = APIHelper()
        self.auth = AuthAPIHelper(self.api)
        self.registration = RegistrationAPIHelper(self.api)
        self.admin = AdminAPIHelper(self.api)
        self.competition = CompetitionAPIHelper(self.api)
        self.applicant = ApplicantAPIHelper(self.api)
    
    def health_check(self) -> Dict:
        """Check if API is accessible"""
        try:
            response = self.api.get('/health')
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Export all classes
__all__ = [
    'APIHelper',
    'AuthAPIHelper', 
    'RegistrationAPIHelper',
    'AdminAPIHelper',
    'CompetitionAPIHelper',
    'ApplicantAPIHelper',
    'ComprehensiveAPIHelper'
]
