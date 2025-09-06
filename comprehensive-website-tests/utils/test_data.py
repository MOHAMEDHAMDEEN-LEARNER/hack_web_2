"""
Test Configuration and Data
==========================
"""

import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class TestConfig:
    """Main test configuration"""
    
    # Base URLs
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:3001')
    API_BASE_URL = f"{BASE_URL}/api"
    
    # Browser Settings
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')  # chromium, firefox, webkit
    VIEWPORT_WIDTH = int(os.getenv('VIEWPORT_WIDTH', '1280'))
    VIEWPORT_HEIGHT = int(os.getenv('VIEWPORT_HEIGHT', '720'))
    
    # Test Timeouts
    DEFAULT_TIMEOUT = 30000  # 30 seconds
    NAVIGATION_TIMEOUT = 60000  # 60 seconds
    
    # Test Credentials
    ADMIN_CREDENTIALS = {
        'email': 'admin@test.com',
        'password': 'admin123'
    }
    
    # Test Data
    VALID_APPLICANT = {
        'name': 'Test Applicant',
        'email': 'testapplicant@example.com',
        'mobile': '9876543210',
        'studentId': 'STU001',
        'course': 'Computer Science',
        'yearOfGraduation': '2024',
        'collegeName': 'Test College',
        'linkedinProfile': 'https://linkedin.com/in/testuser'
    }
    
    # Report Settings
    REPORTS_DIR = 'reports'
    SCREENSHOTS_DIR = f'{REPORTS_DIR}/screenshots'
    VIDEOS_DIR = f'{REPORTS_DIR}/videos'
    LOGS_DIR = f'{REPORTS_DIR}/logs'

class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def generate_applicant_data(include_optional=True):
        """Generate realistic applicant data"""
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'mobile': fake.numerify('##########'),
            'studentId': fake.bothify('STU###??'),
            'course': fake.random_element([
                'Computer Science', 'Information Technology', 
                'Electronics Engineering', 'Mechanical Engineering',
                'Civil Engineering', 'Electrical Engineering'
            ]),
            'yearOfGraduation': str(fake.random_int(2024, 2027)),
            'collegeName': fake.company() + ' College'
        }
        
        if include_optional:
            data['linkedinProfile'] = f"https://linkedin.com/in/{fake.user_name()}"
        
        return data
    
    @staticmethod
    def generate_bulk_applicants(count=10):
        """Generate multiple applicant records"""
        return [TestDataGenerator.generate_applicant_data() for _ in range(count)]
    
    @staticmethod
    def generate_invalid_data():
        """Generate various invalid data scenarios"""
        return {
            'invalid_email': {
                'name': 'Test User',
                'email': 'invalid-email',
                'mobile': '9876543210',
                'studentId': 'STU001',
                'course': 'Computer Science',
                'yearOfGraduation': '2024',
                'collegeName': 'Test College'
            },
            'invalid_mobile': {
                'name': 'Test User',
                'email': 'test@example.com',
                'mobile': '123',  # Too short
                'studentId': 'STU001',
                'course': 'Computer Science',
                'yearOfGraduation': '2024',
                'collegeName': 'Test College'
            },
            'missing_required': {
                'name': '',  # Missing required field
                'email': 'test@example.com',
                'mobile': '9876543210',
                'studentId': '',  # Missing required field
                'course': 'Computer Science',
                'yearOfGraduation': '2024',
                'collegeName': 'Test College'
            },
            'special_characters': {
                'name': 'Test <script>alert("xss")</script>',
                'email': 'test+special@example.com',
                'mobile': '9876543210',
                'studentId': 'STU001!@#',
                'course': 'Computer Science & Engineering',
                'yearOfGraduation': '2024',
                'collegeName': "O'Neil College"
            }
        }

class CompetitionData:
    """Competition and stage related test data"""
    
    @staticmethod
    def get_sample_stages():
        """Sample competition stages"""
        return [
            {
                'name': 'Registration',
                'description': 'Initial registration phase',
                'startTime': datetime.now(),
                'endTime': datetime.now() + timedelta(days=7),
                'status': 'active'
            },
            {
                'name': 'Screening',
                'description': 'Application screening phase',
                'startTime': datetime.now() + timedelta(days=7),
                'endTime': datetime.now() + timedelta(days=14),
                'status': 'upcoming'
            },
            {
                'name': 'Final Presentation',
                'description': 'Final presentation phase',
                'startTime': datetime.now() + timedelta(days=14),
                'endTime': datetime.now() + timedelta(days=21),
                'status': 'upcoming'
            }
        ]
    
    @staticmethod
    def get_submission_data():
        """Sample submission data"""
        return {
            'githubUrl': 'https://github.com/testuser/hackathon-project',
            'description': 'This is a test project submission for the hackathon',
            'technologies': ['React', 'Node.js', 'PostgreSQL'],
            'documents': []  # File uploads would be handled separately
        }

class UISelectors:
    """Common UI selectors for the hackathon website"""
    
    # Landing Page Selectors
    LANDING_ADMIN_LOGIN_BUTTON = "text=Admin/Jury Login"
    LANDING_APPLICANT_LOGIN_BUTTON = "text=Applicant Login"  
    LANDING_REGISTER_BUTTON = "text=Register as Participant"
    LANDING_MAIN_HEADING = "h1:has-text('CIEL-Kings VibeAIthon')"
    
    # Registration Form Selectors
    REGISTRATION_FORM = "form"
    REGISTRATION_NAME_INPUT = "input[name='name']"
    REGISTRATION_EMAIL_INPUT = "input[name='email']"
    REGISTRATION_MOBILE_INPUT = "input[name='mobile']"
    REGISTRATION_STUDENT_ID_INPUT = "input[name='studentId']"
    REGISTRATION_COURSE_INPUT = "input[name='course']"
    REGISTRATION_YEAR_SELECT = "select[name='yearOfGraduation']"
    REGISTRATION_COLLEGE_INPUT = "input[name='collegeName']"
    REGISTRATION_LINKEDIN_INPUT = "input[name='linkedinProfile']"
    REGISTRATION_SUBMIT_BUTTON = "button[type='submit']"
    
    # Admin Login Selectors
    ADMIN_LOGIN_EMAIL_INPUT = "input[name='email'], input[type='email']"
    ADMIN_LOGIN_PASSWORD_INPUT = "input[name='password'], input[type='password']"
    ADMIN_LOGIN_SUBMIT_BUTTON = "button[type='submit']"
    ADMIN_LOGIN_FORM = "form"
    
    # Applicant Login Selectors
    APPLICANT_LOGIN_IDENTIFIER_INPUT = "input[name='identifier'], input[placeholder*='email'], input[placeholder*='mobile']"
    APPLICANT_LOGIN_SEND_OTP_BUTTON = "button:has-text('Send OTP')"
    APPLICANT_LOGIN_OTP_INPUT = "input[name='otp'], input[placeholder*='OTP']"
    APPLICANT_LOGIN_VERIFY_BUTTON = "button:has-text('Verify')"
    
    # Dashboard Selectors
    ADMIN_DASHBOARD_HEADING = "h1:has-text('Admin Dashboard')"
    APPLICANT_DASHBOARD_HEADING = "h1:has-text('Applicant Dashboard')"
    LOGOUT_BUTTON = "button:has-text('Logout'), button:has-text('Sign out')"
    
    # Common UI Elements
    LOADING_SPINNER = ".animate-spin"
    ERROR_MESSAGE = ".error, .text-red-500, .text-destructive"
    SUCCESS_MESSAGE = ".success, .text-green-500"
    MODAL = ".modal, [role='dialog']"
    TOAST_MESSAGE = ".toast, .notification"

class TestMessages:
    """Expected messages and text content"""
    
    # Success Messages
    REGISTRATION_SUCCESS = [
        "Registration successful",
        "Successfully registered",
        "Thank you for registering"
    ]
    
    LOGIN_SUCCESS = [
        "Login successful",
        "Welcome",
        "Dashboard"
    ]
    
    # Error Messages
    INVALID_CREDENTIALS = [
        "Invalid credentials",
        "Login failed",
        "Authentication failed"
    ]
    
    VALIDATION_ERRORS = [
        "required",
        "invalid",
        "must be",
        "should be"
    ]
    
    # Navigation Labels
    DASHBOARD_TITLE = [
        "Dashboard",
        "Admin Dashboard",
        "Applicant Dashboard"
    ]

# Export all classes for easy importing
__all__ = [
    'TestConfig',
    'TestDataGenerator', 
    'CompetitionData',
    'UISelectors',
    'TestMessages'
]
