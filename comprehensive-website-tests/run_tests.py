#!/usr/bin/env python3
"""
Comprehensive Test Runner for Hackathon Website
===============================================

This script runs all test modules and generates comprehensive reports.
"""

import sys
import os
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class TestRunner:
    """Comprehensive test runner"""
    
    def __init__(self):
        self.project_root = project_root
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Test modules in execution order
        self.test_modules = [
            ("test_01_landing_page.py", "Landing Page Tests"),
            ("test_02_registration.py", "Registration System Tests"),
            ("test_03_admin_auth.py", "Admin Authentication Tests"),
            ("test_04_applicant_auth.py", "Applicant Authentication Tests"),
            ("test_05_admin_dashboard.py", "Admin Dashboard Tests"),
            ("test_06_applicant_portal.py", "Applicant Portal Tests"),
            ("test_07_competition_management.py", "Competition Management Tests"),
            ("test_08_api_endpoints.py", "API Endpoints Tests"),
            ("test_09_ui_components.py", "UI Components Tests"),
            ("test_10_performance.py", "Performance Tests"),
            ("test_11_error_handling.py", "Error Handling Tests")
        ]
        
        self.test_results = {}
    
    def run_all_tests(self, headless=True, verbose=False):
        """Run all test modules"""
        print("🚀 Starting Comprehensive Test Suite")
        print("=" * 50)
        
        start_time = time.time()
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        
        # Test execution arguments
        pytest_args = [
            "python3", "-m", "pytest",
            "-v" if verbose else "",
            "--tb=short",
            f"--headless={headless}",
            "--html=reports/test_report.html",
            "--self-contained-html",
            "--json-report",
            "--json-report-file=reports/test_results.json"
        ]
        
        # Remove empty arguments
        pytest_args = [arg for arg in pytest_args if arg]
        
        for test_file, test_description in self.test_modules:
            print(f"\n📋 Running: {test_description}")
            print(f"   File: {test_file}")
            print("-" * 40)
            
            module_start_time = time.time()
            
            # Run individual test module
            cmd = pytest_args + [f"tests/{test_file}"]
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per module
                )
                
                module_end_time = time.time()
                module_duration = module_end_time - module_start_time
                
                # Parse pytest output for results
                output_lines = result.stdout.split('\n')
                
                passed = 0
                failed = 0
                skipped = 0
                
                for line in output_lines:
                    if 'passed' in line and 'failed' in line:
                        # Parse summary line like "5 passed, 2 failed, 1 skipped"
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == 'passed' and i > 0:
                                try:
                                    passed = int(parts[i-1])
                                except:
                                    pass
                            elif part == 'failed' and i > 0:
                                try:
                                    failed = int(parts[i-1])
                                except:
                                    pass
                            elif part == 'skipped' and i > 0:
                                try:
                                    skipped = int(parts[i-1])
                                except:
                                    pass
                
                self.test_results[test_file] = {
                    'description': test_description,
                    'passed': passed,
                    'failed': failed,
                    'skipped': skipped,
                    'duration': module_duration,
                    'return_code': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
                total_passed += passed
                total_failed += failed
                total_skipped += skipped
                
                # Status output
                if result.returncode == 0:
                    print(f"✅ {test_description}: PASSED")
                else:
                    print(f"❌ {test_description}: FAILED")
                
                print(f"   📊 Results: {passed} passed, {failed} failed, {skipped} skipped")
                print(f"   ⏱️  Duration: {module_duration:.2f}s")
                
                if verbose and result.stderr:
                    print(f"   ⚠️  Stderr: {result.stderr[:200]}...")
                
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_description}: TIMEOUT (5 minutes)")
                self.test_results[test_file] = {
                    'description': test_description,
                    'passed': 0,
                    'failed': 1,
                    'skipped': 0,
                    'duration': 300,
                    'return_code': -1,
                    'error': 'Timeout after 5 minutes'
                }
                total_failed += 1
                
            except Exception as e:
                print(f"💥 {test_description}: ERROR - {str(e)}")
                self.test_results[test_file] = {
                    'description': test_description,
                    'passed': 0,
                    'failed': 1,
                    'skipped': 0,
                    'duration': 0,
                    'return_code': -1,
                    'error': str(e)
                }
                total_failed += 1
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Generate summary report
        self.generate_summary_report(total_passed, total_failed, total_skipped, total_duration)
        
        return total_failed == 0
    
    def run_specific_tests(self, test_pattern, headless=True):
        """Run specific tests matching pattern"""
        print(f"🎯 Running specific tests: {test_pattern}")
        
        cmd = [
            "python3", "-m", "pytest",
            "-v",
            f"--headless={headless}",
            "--html=reports/specific_test_report.html",
            "--self-contained-html",
            f"tests/{test_pattern}"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                timeout=600  # 10 minute timeout
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏰ Test execution timed out")
            return False
        except Exception as e:
            print(f"💥 Error running specific tests: {e}")
            return False
    
    def generate_summary_report(self, total_passed, total_failed, total_skipped, total_duration):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 50)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 50)
        
        # Console summary
        print(f"⏱️  Total Duration: {total_duration:.2f} seconds")
        print(f"📋 Test Modules: {len(self.test_modules)}")
        print(f"✅ Total Passed: {total_passed}")
        print(f"❌ Total Failed: {total_failed}")
        print(f"⏭️  Total Skipped: {total_skipped}")
        print(f"📈 Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "No tests completed")
        
        # Detailed module results
        print("\n📋 MODULE RESULTS:")
        print("-" * 50)
        
        for test_file, result in self.test_results.items():
            status = "✅ PASS" if result['return_code'] == 0 else "❌ FAIL"
            print(f"{status} {result['description']}")
            print(f"     📊 {result['passed']} passed, {result['failed']} failed, {result['skipped']} skipped")
            print(f"     ⏱️  {result['duration']:.2f}s")
            if 'error' in result:
                print(f"     💥 {result['error']}")
            print()
        
        # Generate JSON report
        json_report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_duration': total_duration,
                'total_modules': len(self.test_modules),
                'total_passed': total_passed,
                'total_failed': total_failed,
                'total_skipped': total_skipped,
                'success_rate': (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
            },
            'modules': self.test_results
        }
        
        json_report_path = self.reports_dir / "comprehensive_test_summary.json"
        with open(json_report_path, 'w') as f:
            json.dump(json_report, f, indent=2)
        
        print(f"📄 Detailed JSON report saved: {json_report_path}")
        print(f"📄 HTML report available: {self.reports_dir}/test_report.html")
        
        # Quick recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 30)
        
        if total_failed == 0:
            print("🎉 All tests passed! Your application is working excellently.")
        elif total_failed <= 3:
            print("⚠️  Few test failures detected. Check the detailed reports for specific issues.")
        else:
            print("🚨 Multiple test failures detected. Priority fixes needed.")
        
        failed_modules = [test_file for test_file, result in self.test_results.items() if result['return_code'] != 0]
        if failed_modules:
            print(f"🔍 Focus on these modules: {', '.join(failed_modules)}")
        
        if total_duration > 300:  # 5 minutes
            print("⚡ Consider optimizing performance - tests took longer than expected.")
        
        print("\n" + "=" * 50)

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Test Runner for Hackathon Website")
    parser.add_argument("--headless", action="store_true", default=True, help="Run tests in headless mode")
    parser.add_argument("--headed", action="store_true", help="Run tests with browser UI visible")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--test", "-t", help="Run specific test pattern (e.g., 'test_01*' or 'landing')")
    parser.add_argument("--quick", "-q", action="store_true", help="Run quick smoke tests only")
    
    args = parser.parse_args()
    
    # Determine headless mode
    headless = not args.headed if args.headed else args.headless
    
    runner = TestRunner()
    
    try:
        if args.test:
            # Run specific tests
            success = runner.run_specific_tests(args.test, headless=headless)
        elif args.quick:
            # Run quick smoke tests
            print("🚀 Running Quick Smoke Tests")
            success = runner.run_specific_tests("test_01* or test_02* or test_03*", headless=headless)
        else:
            # Run all tests
            success = runner.run_all_tests(headless=headless, verbose=args.verbose)
        
        if success:
            print("\n🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️  Some tests failed. Check the reports for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
