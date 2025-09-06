# Comprehensive Website Tests

This test suite provides comprehensive testing for the hackathon website using pytest and Playwright.

## 🚀 Quick Start

### Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

### Run All Tests
```bash
# Simple execution
python run_tests.py

# With browser UI visible
python run_tests.py --headed

# Verbose output
python run_tests.py --verbose
```

### Run Specific Tests
```bash
# Quick smoke tests
python run_tests.py --quick

# Specific test pattern
python run_tests.py --test "test_01*"
python run_tests.py --test "landing"

# Traditional pytest approach
pytest tests/test_01_landing_page.py -v
```

## 📋 Test Modules

| Module | Purpose | Coverage |
|--------|---------|----------|
| `test_01_landing_page.py` | Landing page functionality | Navigation, content, responsiveness |
| `test_02_registration.py` | Registration system | Form validation, data persistence |
| `test_03_admin_auth.py` | Admin authentication | Login, session management, security |
| `test_04_applicant_auth.py` | Applicant authentication | Login, registration, password reset |
| `test_05_admin_dashboard.py` | Admin dashboard | Management features, data display |
| `test_06_applicant_portal.py` | Applicant portal | Submissions, status tracking |
| `test_07_competition_management.py` | Competition features | Stages, rounds, judging |
| `test_08_api_endpoints.py` | API testing | REST endpoints, data validation |
| `test_09_ui_components.py` | UI components | Responsiveness, interactions |
| `test_10_performance.py` | Performance testing | Load times, memory usage |
| `test_11_error_handling.py` | Error scenarios | Edge cases, error recovery |

## 🛠 Test Structure

```
comprehensive-website-tests/
├── run_tests.py              # Main test runner
├── conftest.py              # Pytest configuration
├── requirements.txt         # Dependencies
├── tests/                   # Test modules
│   ├── test_01_landing_page.py
│   ├── test_02_registration.py
│   └── ...
├── utils/                   # Shared utilities
│   ├── test_data.py        # Test data and config
│   ├── browser_helper.py   # Browser automation
│   └── api_helper.py       # API testing utilities
└── reports/                # Generated reports
    ├── test_report.html
    └── comprehensive_test_summary.json
```

## 🎯 Test Categories

### Functional Tests
- ✅ User registration and authentication
- ✅ Admin dashboard functionality
- ✅ Applicant portal features
- ✅ Competition management
- ✅ Form validation and data handling

### Non-Functional Tests
- ⚡ Performance and load testing
- 📱 Responsive design validation
- 🛡️ Security and error handling
- 🔗 API endpoint testing

### Cross-Browser Testing
- 🌐 Chrome/Chromium
- 🦊 Firefox
- 🧭 Safari/WebKit

## ⚙️ Configuration

### Environment Variables
```bash
# Test configuration
export HEADLESS=true
export BROWSER=chromium
export BASE_URL=http://localhost:5173
export API_BASE_URL=http://localhost:3000

# Test data
export TEST_ADMIN_EMAIL=admin@test.com
export TEST_ADMIN_PASSWORD=testpass123
```

### Test Markers
Use pytest markers to run specific test categories:

```bash
# Run only smoke tests
pytest -m smoke

# Run only performance tests
pytest -m performance

# Skip slow tests
pytest -m "not slow"

# Run specific browser tests
pytest -m "chromium or firefox"
```

## 📊 Reporting

### Automatic Reports
- **HTML Report**: `reports/test_report.html` - Detailed test results
- **JSON Summary**: `reports/comprehensive_test_summary.json` - Machine-readable results
- **Screenshots**: Captured on test failures for debugging

### Custom Reporting
```bash
# Generate JUnit XML for CI/CD
pytest --junitxml=reports/junit.xml

# Generate coverage report
pytest --cov=../client/src --cov-report=html:reports/coverage

# Generate performance metrics
python run_tests.py --test "test_10*" --verbose
```

## 🚨 Troubleshooting

### Common Issues

**Browser Installation**
```bash
# Reinstall browsers
playwright install --force
```

**Port Conflicts**
```bash
# Check if services are running
netstat -an | grep :5173
netstat -an | grep :3000
```

**Permission Issues**
```bash
# Make run_tests.py executable
chmod +x run_tests.py
```

### Debug Mode
```bash
# Run with debugging
pytest --pdb --pdbcls=IPython.terminal.debugger:Pdb

# Run with browser devtools
pytest --headed --slowmo=1000
```

## 🔧 Advanced Usage

### Parallel Execution
```bash
# Run tests in parallel
pytest -n auto --dist loadscope
```

### Custom Test Data
```bash
# Use custom test data file
pytest --test-data-file=custom_data.json
```

### Integration with CI/CD
```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    python run_tests.py --headless
    
- name: Upload Reports
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: reports/
```

## 📝 Writing New Tests

### Test Template
```python
import pytest
from utils.browser_helper import BrowserHelper
from utils.test_data import TestConfig

class TestNewFeature:
    """Test new feature functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.browser = BrowserHelper(page)
        self.config = TestConfig()
    
    @pytest.mark.smoke
    def test_basic_functionality(self):
        """Test basic feature functionality"""
        # Test implementation
        pass
    
    @pytest.mark.regression
    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        # Test implementation
        pass
```

### Best Practices
- 🏷️ Use descriptive test names and docstrings
- 🧪 Include both positive and negative test cases
- 📸 Take screenshots on failures for debugging
- ⏱️ Set appropriate timeouts for async operations
- 🔄 Clean up test data between tests
- 📊 Use appropriate pytest markers for categorization

## 📞 Support

For issues with the test suite:
1. Check the troubleshooting section above
2. Review test logs in `reports/` directory
3. Run individual test modules to isolate issues
4. Use `--verbose` flag for detailed output

## 🤝 Contributing

When adding new tests:
1. Follow the existing code structure
2. Add appropriate pytest markers
3. Include docstrings and comments
4. Test both success and failure scenarios
5. Update this README if adding new test categories
- Video recording of test runs
- HTML report generation
- Detailed test documentation

Features Tested:
===============

🔐 Authentication System:
- Admin login (admin@test.com / admin123)
- Applicant OTP-based login
- Session management
- Role-based access control

📝 Registration System:
- Complete form validation
- Duplicate email detection
- Registration confirmation
- Participation confirmation

👨‍💼 Admin Dashboard:
- Applicant management
- Competition round setup
- Bulk operations
- Data export/import
- System settings

👤 Applicant Portal:
- Dashboard access
- Stage submissions
- Progress tracking
- File uploads

🎯 Competition Management:
- Multi-stage competitions
- Submission deadlines
- Progress tracking
- Jury evaluation

🎨 UI/UX Testing:
- Responsive design
- Form interactions
- Navigation flows
- Error states
- Loading states

📊 Reporting:
- HTML test reports
- Screenshots for each test
- Video recordings
- Performance metrics
- Error logs

Installation:
============
pip install -r requirements.txt
playwright install

Usage:
======
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --category auth
python run_tests.py --category registration
python run_tests.py --category admin
python run_tests.py --category applicant

# Run with video recording
python run_tests.py --video

# Run in headless mode
python run_tests.py --headless

# Generate detailed report
python run_tests.py --report

Requirements:
============
- Python 3.8+
- Playwright for browser automation
- pytest for test framework
- Requests for API testing
- PIL/OpenCV for image processing
- Website running on localhost:3001 or 3002

Test Structure:
==============
tests/
├── test_01_landing_page.py       # Landing page tests
├── test_02_registration.py       # Registration flow tests
├── test_03_admin_auth.py         # Admin authentication tests
├── test_04_applicant_auth.py     # Applicant authentication tests
├── test_05_admin_dashboard.py    # Admin dashboard tests
├── test_06_applicant_portal.py   # Applicant portal tests
├── test_07_competition_mgmt.py   # Competition management tests
├── test_08_api_endpoints.py      # API testing
├── test_09_ui_components.py      # UI component tests
├── test_10_responsive_design.py  # Responsive design tests
├── test_11_performance.py        # Performance tests
├── test_12_error_handling.py     # Error handling tests
└── test_13_integration.py        # End-to-end integration tests

utils/
├── browser_helper.py             # Browser automation utilities
├── api_helper.py                 # API testing utilities
├── test_data.py                  # Test data and fixtures
├── report_generator.py           # Custom report generation
└── video_recorder.py             # Video recording utilities

reports/
├── html_report.html              # Main test report
├── screenshots/                  # Test screenshots
├── videos/                       # Test recordings
└── logs/                        # Test logs
"""
