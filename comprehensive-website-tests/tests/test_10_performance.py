"""
Test 10: Performance & Load Testing
===================================

This test module covers performance testing including:
- Page load times
- Resource loading
- Memory usage
- Network performance
- Database query performance
- Load testing
- Stress testing
"""

import pytest
import logging
import time
import threading
from utils.test_data import TestConfig
from utils.browser_helper import BrowserHelper

logger = logging.getLogger(__name__)

@pytest.mark.performance
@pytest.mark.load_time
class TestPageLoadPerformance:
    """Test page load performance"""
    
    def test_landing_page_load_time(self, browser_helper: BrowserHelper):
        """Test landing page load time"""
        logger.info("⚡ Testing landing page load time")
        
        # Measure load time
        start_time = time.time()
        
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        end_time = time.time()
        load_time = end_time - start_time
        
        logger.info(f"📊 Landing page load time: {load_time:.3f}s")
        
        # Performance thresholds
        if load_time < 1:
            logger.info("✅ Excellent load time (< 1s)")
        elif load_time < 2:
            logger.info("✅ Very good load time (< 2s)")
        elif load_time < 3:
            logger.info("✅ Good load time (< 3s)")
        elif load_time < 5:
            logger.warning("⚠️ Acceptable load time (< 5s)")
        else:
            logger.warning("❌ Slow load time (> 5s)")
        
        # Take screenshot
        browser_helper.take_screenshot("landing_page_load_performance")
        
        assert load_time < 10, f"Landing page load time too slow: {load_time:.3f}s"
        
        logger.info("✅ Landing page load time test completed")
    
    def test_admin_dashboard_load_time(self, browser_helper: BrowserHelper):
        """Test admin dashboard load time"""
        logger.info("📊 Testing admin dashboard load time")
        
        # First login as admin
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
        
        # Measure dashboard load time
        start_time = time.time()
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        end_time = time.time()
        load_time = end_time - start_time
        
        logger.info(f"📊 Admin dashboard load time: {load_time:.3f}s")
        
        # Performance thresholds (dashboard can be slower due to data loading)
        if load_time < 2:
            logger.info("✅ Excellent dashboard load time (< 2s)")
        elif load_time < 4:
            logger.info("✅ Good dashboard load time (< 4s)")
        elif load_time < 8:
            logger.warning("⚠️ Acceptable dashboard load time (< 8s)")
        else:
            logger.warning("❌ Slow dashboard load time (> 8s)")
        
        # Take screenshot
        browser_helper.take_screenshot("admin_dashboard_load_performance")
        
        logger.info("✅ Admin dashboard load time test completed")
    
    def test_resource_loading_performance(self, browser_helper: BrowserHelper):
        """Test resource loading performance"""
        logger.info("📦 Testing resource loading performance")
        
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        try:
            # Get performance metrics
            performance_metrics = browser_helper.page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    const resources = performance.getEntriesByType('resource');
                    
                    return {
                        navigation: {
                            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                            totalTime: navigation.loadEventEnd - navigation.fetchStart
                        },
                        resources: {
                            count: resources.length,
                            totalSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                            slowResources: resources.filter(r => r.duration > 1000).length
                        }
                    };
                }
            """)
            
            nav_metrics = performance_metrics['navigation']
            resource_metrics = performance_metrics['resources']
            
            logger.info(f"📊 Navigation metrics:")
            logger.info(f"   - DOM Content Loaded: {nav_metrics['domContentLoaded']:.3f}ms")
            logger.info(f"   - Load Complete: {nav_metrics['loadComplete']:.3f}ms")
            logger.info(f"   - Total Time: {nav_metrics['totalTime']:.3f}ms")
            
            logger.info(f"📊 Resource metrics:")
            logger.info(f"   - Resource count: {resource_metrics['count']}")
            logger.info(f"   - Total size: {resource_metrics['totalSize'] / 1024:.1f} KB")
            logger.info(f"   - Slow resources (>1s): {resource_metrics['slowResources']}")
            
            # Performance analysis
            if resource_metrics['count'] > 100:
                logger.warning("⚠️ High number of resources may impact performance")
            else:
                logger.info("✅ Resource count reasonable")
            
            if resource_metrics['totalSize'] > 5 * 1024 * 1024:  # 5MB
                logger.warning("⚠️ High total resource size")
            else:
                logger.info("✅ Resource size reasonable")
            
            if resource_metrics['slowResources'] > 5:
                logger.warning("⚠️ Multiple slow-loading resources detected")
            else:
                logger.info("✅ Resource loading performance good")
            
        except Exception as e:
            logger.warning(f"Could not gather performance metrics: {e}")
        
        # Take screenshot
        browser_helper.take_screenshot("resource_loading_performance")
        
        logger.info("✅ Resource loading performance test completed")

@pytest.mark.performance
@pytest.mark.memory
class TestMemoryUsage:
    """Test memory usage"""
    
    def test_memory_usage_during_navigation(self, browser_helper: BrowserHelper):
        """Test memory usage during navigation"""
        logger.info("🧠 Testing memory usage during navigation")
        
        # Pages to navigate through
        test_pages = [
            "/",
            "/register", 
            "/admin/login",
            "/admin/dashboard",
            "/admin/applicants"
        ]
        
        memory_measurements = []
        
        for i, page in enumerate(test_pages):
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Wait a bit for page to settle
                time.sleep(1)
                
                # Get memory info (if available)
                try:
                    memory_info = browser_helper.page.evaluate("""
                        () => {
                            if (performance.memory) {
                                return {
                                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                                    totalJSHeapSize: performance.memory.totalJSHeapSize,
                                    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                                };
                            }
                            return null;
                        }
                    """)
                    
                    if memory_info:
                        memory_measurements.append({
                            'page': page,
                            'step': i,
                            'used_heap': memory_info['usedJSHeapSize'],
                            'total_heap': memory_info['totalJSHeapSize']
                        })
                        
                        used_mb = memory_info['usedJSHeapSize'] / (1024 * 1024)
                        total_mb = memory_info['totalJSHeapSize'] / (1024 * 1024)
                        
                        logger.info(f"📊 {page} memory: {used_mb:.1f}MB used, {total_mb:.1f}MB total")
                        
                except Exception as e:
                    logger.debug(f"Could not get memory info for {page}: {e}")
                    
            except Exception as e:
                logger.debug(f"Could not test memory for {page}: {e}")
                continue
        
        # Analyze memory trends
        if len(memory_measurements) >= 3:
            first_measurement = memory_measurements[0]['used_heap']
            last_measurement = memory_measurements[-1]['used_heap']
            
            memory_increase = last_measurement - first_measurement
            memory_increase_mb = memory_increase / (1024 * 1024)
            
            logger.info(f"📊 Memory usage analysis:")
            logger.info(f"   - Initial: {first_measurement / (1024 * 1024):.1f}MB")
            logger.info(f"   - Final: {last_measurement / (1024 * 1024):.1f}MB")
            logger.info(f"   - Increase: {memory_increase_mb:.1f}MB")
            
            if memory_increase_mb < 10:
                logger.info("✅ Low memory increase during navigation")
            elif memory_increase_mb < 50:
                logger.info("✅ Moderate memory increase")
            else:
                logger.warning("⚠️ High memory increase - possible memory leak")
        
        # Take screenshot
        browser_helper.take_screenshot("memory_usage_navigation")
        
        logger.info("✅ Memory usage test completed")

@pytest.mark.performance
@pytest.mark.network
class TestNetworkPerformance:
    """Test network performance"""
    
    def test_network_request_performance(self, browser_helper: BrowserHelper):
        """Test network request performance"""
        logger.info("🌐 Testing network request performance")
        
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        try:
            # Get network timing information
            network_metrics = browser_helper.page.evaluate("""
                () => {
                    const resources = performance.getEntriesByType('resource');
                    
                    const metrics = {
                        totalRequests: resources.length,
                        fastRequests: 0,
                        slowRequests: 0,
                        failedRequests: 0,
                        averageResponseTime: 0,
                        requestsByType: {}
                    };
                    
                    let totalResponseTime = 0;
                    
                    resources.forEach(resource => {
                        const responseTime = resource.responseEnd - resource.responseStart;
                        totalResponseTime += responseTime;
                        
                        // Categorize by speed
                        if (responseTime < 100) metrics.fastRequests++;
                        else if (responseTime > 2000) metrics.slowRequests++;
                        
                        // Check for failed requests (approximate)
                        if (resource.transferSize === 0 && resource.duration > 0) {
                            metrics.failedRequests++;
                        }
                        
                        // Categorize by type
                        const url = new URL(resource.name);
                        const extension = url.pathname.split('.').pop() || 'unknown';
                        metrics.requestsByType[extension] = (metrics.requestsByType[extension] || 0) + 1;
                    });
                    
                    metrics.averageResponseTime = totalResponseTime / resources.length;
                    
                    return metrics;
                }
            """)
            
            logger.info(f"📊 Network performance metrics:")
            logger.info(f"   - Total requests: {network_metrics['totalRequests']}")
            logger.info(f"   - Fast requests (<100ms): {network_metrics['fastRequests']}")
            logger.info(f"   - Slow requests (>2s): {network_metrics['slowRequests']}")
            logger.info(f"   - Failed requests: {network_metrics['failedRequests']}")
            logger.info(f"   - Average response time: {network_metrics['averageResponseTime']:.1f}ms")
            
            # Request type breakdown
            logger.info(f"📊 Requests by type:")
            for req_type, count in network_metrics['requestsByType'].items():
                logger.info(f"   - {req_type}: {count}")
            
            # Performance analysis
            total_requests = network_metrics['totalRequests']
            if total_requests > 0:
                fast_ratio = network_metrics['fastRequests'] / total_requests
                slow_ratio = network_metrics['slowRequests'] / total_requests
                failed_ratio = network_metrics['failedRequests'] / total_requests
                
                if fast_ratio > 0.7:
                    logger.info("✅ Good network performance (70%+ fast requests)")
                elif fast_ratio > 0.5:
                    logger.info("✅ Acceptable network performance")
                else:
                    logger.warning("⚠️ Poor network performance")
                
                if slow_ratio > 0.1:
                    logger.warning("⚠️ Too many slow requests")
                
                if failed_ratio > 0.05:
                    logger.warning("⚠️ High request failure rate")
                else:
                    logger.info("✅ Low request failure rate")
            
        except Exception as e:
            logger.warning(f"Could not analyze network performance: {e}")
        
        # Take screenshot
        browser_helper.take_screenshot("network_performance")
        
        logger.info("✅ Network performance test completed")

@pytest.mark.performance
@pytest.mark.load
class TestLoadTesting:
    """Test application under load"""
    
    def test_concurrent_page_loads(self, browser_helper: BrowserHelper):
        """Test concurrent page loads"""
        logger.info("🔄 Testing concurrent page loads")
        
        # Test with multiple concurrent browser sessions
        def load_page_worker(worker_id):
            """Worker function to load pages"""
            try:
                from playwright.sync_api import sync_playwright
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    start_time = time.time()
                    
                    # Load multiple pages
                    test_pages = ["/", "/register", "/admin/login"]
                    
                    for test_page in test_pages:
                        page.goto(f"{TestConfig.BASE_URL}{test_page}")
                        page.wait_for_load_state("networkidle")
                        time.sleep(0.5)  # Small delay between pages
                    
                    end_time = time.time()
                    browser.close()
                    
                    return {
                        'worker_id': worker_id,
                        'success': True,
                        'total_time': end_time - start_time,
                        'pages_loaded': len(test_pages)
                    }
                    
            except Exception as e:
                return {
                    'worker_id': worker_id,
                    'success': False,
                    'error': str(e),
                    'total_time': None,
                    'pages_loaded': 0
                }
        
        # Run concurrent workers
        num_workers = 3  # Moderate load test
        threads = []
        results = []
        
        def thread_wrapper(worker_id):
            result = load_page_worker(worker_id)
            results.append(result)
        
        start_time = time.time()
        
        # Start all workers
        for i in range(num_workers):
            thread = threading.Thread(target=thread_wrapper, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all workers to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_test_time = end_time - start_time
        
        # Analyze results
        successful_workers = [r for r in results if r['success']]
        failed_workers = [r for r in results if not r['success']]
        
        if successful_workers:
            avg_worker_time = sum(r['total_time'] for r in successful_workers) / len(successful_workers)
            total_pages_loaded = sum(r['pages_loaded'] for r in successful_workers)
        else:
            avg_worker_time = 0
            total_pages_loaded = 0
        
        logger.info(f"📊 Concurrent load test results:")
        logger.info(f"   - Workers: {num_workers}")
        logger.info(f"   - Successful workers: {len(successful_workers)}")
        logger.info(f"   - Failed workers: {len(failed_workers)}")
        logger.info(f"   - Total test time: {total_test_time:.3f}s")
        logger.info(f"   - Average worker time: {avg_worker_time:.3f}s")
        logger.info(f"   - Total pages loaded: {total_pages_loaded}")
        
        # Log failures
        for failed_worker in failed_workers:
            logger.warning(f"⚠️ Worker {failed_worker['worker_id']} failed: {failed_worker['error']}")
        
        # Performance assessment
        success_rate = len(successful_workers) / num_workers
        
        if success_rate >= 1.0:
            logger.info("✅ Excellent load handling (100% success)")
        elif success_rate >= 0.8:
            logger.info("✅ Good load handling (80%+ success)")
        else:
            logger.warning("⚠️ Poor load handling")
        
        # Take screenshot of main page after load test
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        browser_helper.take_screenshot("concurrent_load_test_result")
        
        logger.info("✅ Concurrent page loads test completed")
    
    def test_form_submission_load(self, browser_helper: BrowserHelper):
        """Test form submission under load"""
        logger.info("📝 Testing form submission load")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Test multiple rapid form submissions
        if browser_helper.is_visible("form"):
            submission_results = []
            
            for i in range(3):  # Test 3 rapid submissions
                try:
                    start_time = time.time()
                    
                    # Fill form with unique data
                    test_data = {
                        'name': f"Load Test User {i}",
                        'email': f"loadtest{i}_{int(time.time())}@example.com",
                        'phone': f"98765432{i:02d}",
                        'college': f"Load Test University {i}",
                        'year': "3",
                        'branch': "Computer Science"
                    }
                    
                    # Fill form fields
                    for field, value in test_data.items():
                        field_selectors = [
                            f"input[name='{field}']",
                            f"select[name='{field}']"
                        ]
                        
                        for selector in field_selectors:
                            try:
                                if browser_helper.is_visible(selector):
                                    element = browser_helper.page.query_selector(selector)
                                    if element.tag_name.lower() == 'select':
                                        if field == 'year':
                                            element.select_option(value=value)
                                    else:
                                        element.fill(value)
                                    break
                            except:
                                continue
                    
                    # Submit form
                    submit_button = browser_helper.page.query_selector("button[type='submit']")
                    if submit_button:
                        submit_button.click()
                        browser_helper.wait_for_loading_to_complete()
                    
                    end_time = time.time()
                    submission_time = end_time - start_time
                    
                    submission_results.append({
                        'submission': i + 1,
                        'success': True,
                        'time': submission_time
                    })
                    
                    logger.info(f"✅ Form submission {i+1}: {submission_time:.3f}s")
                    
                    # Navigate back to registration for next test
                    if i < 2:  # Don't navigate after last submission
                        browser_helper.navigate_to("/register")
                        browser_helper.wait_for_loading_to_complete()
                        time.sleep(0.5)  # Small delay between submissions
                    
                except Exception as e:
                    submission_results.append({
                        'submission': i + 1,
                        'success': False,
                        'error': str(e),
                        'time': None
                    })
                    logger.warning(f"⚠️ Form submission {i+1} failed: {e}")
            
            # Analyze submission performance
            successful_submissions = [r for r in submission_results if r['success']]
            
            if successful_submissions:
                avg_submission_time = sum(r['time'] for r in successful_submissions) / len(successful_submissions)
                logger.info(f"📊 Form submission load test:")
                logger.info(f"   - Successful submissions: {len(successful_submissions)}/3")
                logger.info(f"   - Average submission time: {avg_submission_time:.3f}s")
                
                if avg_submission_time < 2:
                    logger.info("✅ Good form submission performance")
                elif avg_submission_time < 5:
                    logger.info("✅ Acceptable form submission performance")
                else:
                    logger.warning("⚠️ Slow form submission performance")
            else:
                logger.warning("⚠️ No successful form submissions")
        
        # Take screenshot
        browser_helper.take_screenshot("form_submission_load_test")
        
        logger.info("✅ Form submission load test completed")

@pytest.mark.performance
@pytest.mark.stress
class TestStressTesting:
    """Test application under stress conditions"""
    
    def test_browser_stress(self, browser_helper: BrowserHelper):
        """Test browser under stress conditions"""
        logger.info("🔥 Testing browser stress conditions")
        
        stress_results = []
        
        # Test 1: Rapid navigation
        logger.info("🔍 Testing rapid navigation")
        
        rapid_nav_pages = ["/", "/register", "/admin/login", "/"]
        
        start_time = time.time()
        
        for i, page in enumerate(rapid_nav_pages * 2):  # Do it twice
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                if i % 2 == 0:  # Every other navigation, take a screenshot
                    browser_helper.take_screenshot(f"stress_rapid_nav_{i}")
                
            except Exception as e:
                logger.warning(f"Rapid navigation failed at step {i}: {e}")
                break
        
        rapid_nav_time = time.time() - start_time
        stress_results.append(('rapid_navigation', rapid_nav_time, rapid_nav_time < 30))
        
        logger.info(f"📊 Rapid navigation: {rapid_nav_time:.3f}s")
        
        # Test 2: Multiple window/tab simulation
        logger.info("🔍 Testing multiple tab simulation")
        
        try:
            # Open multiple pages in sequence (simulating tabs)
            tab_pages = ["/", "/register", "/admin/login"]
            tab_start_time = time.time()
            
            for page in tab_pages:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Simulate some interaction
                if browser_helper.is_visible("input"):
                    first_input = browser_helper.page.query_selector("input")
                    if first_input:
                        first_input.focus()
                        first_input.type("stress test")
                        first_input.clear()
            
            tab_test_time = time.time() - tab_start_time
            stress_results.append(('multiple_tabs', tab_test_time, tab_test_time < 20))
            
            logger.info(f"📊 Multiple tab simulation: {tab_test_time:.3f}s")
            
        except Exception as e:
            logger.warning(f"Multiple tab test failed: {e}")
            stress_results.append(('multiple_tabs', None, False))
        
        # Test 3: Heavy form interaction
        logger.info("🔍 Testing heavy form interaction")
        
        try:
            browser_helper.navigate_to("/register")
            browser_helper.wait_for_loading_to_complete()
            
            form_stress_start = time.time()
            
            # Rapid form filling and clearing
            for cycle in range(5):
                input_fields = browser_helper.page.query_selector_all("input[type='text'], input[type='email']")
                
                for field in input_fields[:3]:  # Test first 3 fields
                    if field.is_visible():
                        field.fill(f"stress test {cycle}")
                        field.clear()
                        field.fill(f"final value {cycle}")
            
            form_stress_time = time.time() - form_stress_start
            stress_results.append(('form_interaction', form_stress_time, form_stress_time < 10))
            
            logger.info(f"📊 Heavy form interaction: {form_stress_time:.3f}s")
            
        except Exception as e:
            logger.warning(f"Form stress test failed: {e}")
            stress_results.append(('form_interaction', None, False))
        
        # Analyze stress test results
        logger.info(f"📊 Stress test summary:")
        
        passed_tests = 0
        total_tests = len(stress_results)
        
        for test_name, test_time, passed in stress_results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            time_str = f"{test_time:.3f}s" if test_time else "N/A"
            logger.info(f"   - {test_name}: {status} ({time_str})")
            
            if passed:
                passed_tests += 1
        
        stress_score = passed_tests / total_tests if total_tests > 0 else 0
        
        if stress_score >= 0.8:
            logger.info("✅ Excellent stress test performance")
        elif stress_score >= 0.6:
            logger.info("✅ Good stress test performance")
        else:
            logger.warning("⚠️ Poor stress test performance")
        
        # Take final screenshot
        browser_helper.take_screenshot("stress_test_complete")
        
        logger.info("✅ Browser stress test completed")
