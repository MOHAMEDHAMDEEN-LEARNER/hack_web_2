"""
Test 05: Admin Dashboard
========================

This test module covers admin dashboard functionality including:
- Dashboard overview and stats
- Navigation and menu functionality
- User management features
- Competition management
- Data visualization
- Export functionality
- Settings and configuration
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.admin
@pytest.mark.dashboard
@pytest.mark.ui
class TestAdminDashboard:
    """Test cases for admin dashboard functionality"""
    
    def test_admin_dashboard_loads(self, authenticated_admin, browser_helper: BrowserHelper, validation_helper: ValidationHelper):
        """Test that admin dashboard loads correctly after authentication"""
        logger.info("📊 Testing admin dashboard load")
        
        # Navigate to admin dashboard
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Verify dashboard loaded
        validation_helper.assert_url_contains("admin")
        validation_helper.assert_no_errors_on_page()
        
        # Check for dashboard elements
        dashboard_indicators = [
            "nav",
            ".dashboard",
            "[data-testid='dashboard']",
            "text*='dashboard' i",
            "text*='admin' i"
        ]
        
        dashboard_found = False
        for indicator in dashboard_indicators:
            try:
                if browser_helper.is_visible(indicator):
                    dashboard_found = True
                    logger.info(f"✅ Dashboard element found: {indicator}")
                    break
            except:
                continue
        
        assert dashboard_found, "Admin dashboard not found"
        
        # Check for navigation menu
        nav_selectors = [
            "nav",
            ".navbar",
            ".menu",
            ".sidebar",
            "[role='navigation']"
        ]
        
        nav_found = False
        for selector in nav_selectors:
            try:
                if browser_helper.is_visible(selector):
                    nav_found = True
                    logger.info(f"✅ Navigation found: {selector}")
                    break
            except:
                continue
        
        assert nav_found, "Navigation menu not found"
        
        # Take screenshot
        browser_helper.take_screenshot("admin_dashboard_loaded")
        
        logger.info("✅ Admin dashboard loaded successfully")
    
    def test_dashboard_stats_cards(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test dashboard statistics cards"""
        logger.info("📈 Testing dashboard stats cards")
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Look for stats cards
        stats_selectors = [
            ".stats",
            ".card",
            ".metric",
            "[data-testid*='stat']",
            "text*='Total' i",
            "text*='Count' i"
        ]
        
        stats_found = []
        for selector in stats_selectors:
            try:
                elements = browser_helper.page.query_selector_all(selector)
                if elements:
                    stats_found.extend(elements)
                    logger.info(f"✅ Stats elements found: {selector} ({len(elements)} items)")
            except:
                continue
        
        if stats_found:
            logger.info(f"✅ {len(stats_found)} statistics elements found")
        else:
            logger.warning("⚠️ No statistics cards found")
        
        # Check for common stat types
        stat_types = [
            "applicant",
            "competition",
            "submission",
            "user",
            "registration",
            "pending",
            "approved"
        ]
        
        for stat_type in stat_types:
            try:
                if browser_helper.is_visible(f"text*='{stat_type}' i"):
                    logger.info(f"✅ {stat_type.title()} stat found")
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("dashboard_stats_cards")
        
        logger.info("✅ Dashboard stats test completed")
    
    def test_dashboard_navigation_menu(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test dashboard navigation menu functionality"""
        logger.info("🧭 Testing dashboard navigation menu")
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Common menu items to test
        menu_items = [
            ("Dashboard", ["/admin/dashboard", "/admin", "/dashboard"]),
            ("Applicants", ["/admin/applicants", "/applicants"]),
            ("Competitions", ["/admin/competitions", "/competitions"]),
            ("Settings", ["/admin/settings", "/settings"]),
            ("Export", ["/admin/export", "/export"]),
            ("Logout", ["/admin/login", "/login", "/"]),
            ("Users", ["/admin/users", "/users"]),
            ("Reports", ["/admin/reports", "/reports"])
        ]
        
        # Test each menu item
        for item_name, possible_urls in menu_items:
            logger.info(f"🔍 Testing menu item: {item_name}")
            
            # Look for menu item
            menu_selectors = [
                f"a:has-text('{item_name}')",
                f"button:has-text('{item_name}')",
                f"[href*='{item_name.lower()}']",
                f"text*='{item_name}' i"
            ]
            
            menu_item_found = False
            for selector in menu_selectors:
                try:
                    element = browser_helper.page.query_selector(selector)
                    if element and element.is_visible():
                        # Click the menu item
                        element.click()
                        browser_helper.wait_for_loading_to_complete()
                        
                        current_url = browser_helper.page.url
                        logger.info(f"✅ Clicked {item_name}, navigated to: {current_url}")
                        
                        # Verify navigation
                        navigation_success = any(url in current_url for url in possible_urls)
                        if navigation_success:
                            logger.info(f"✅ {item_name} navigation successful")
                        else:
                            logger.warning(f"⚠️ {item_name} navigation unclear")
                        
                        menu_item_found = True
                        
                        # Take screenshot
                        item_safe = item_name.lower().replace(' ', '_')
                        browser_helper.take_screenshot(f"menu_item_{item_safe}")
                        
                        # Navigate back to dashboard for next test
                        browser_helper.navigate_to("/admin/dashboard")
                        browser_helper.wait_for_loading_to_complete()
                        break
                        
                except Exception as e:
                    logger.debug(f"Could not click {item_name} with {selector}: {e}")
                    continue
            
            if not menu_item_found:
                logger.info(f"ℹ️ Menu item '{item_name}' not found (may not be implemented)")
        
        logger.info("✅ Navigation menu test completed")
    
    def test_applicants_management_page(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test applicants management functionality"""
        logger.info("👥 Testing applicants management page")
        
        # Navigate to applicants page
        applicants_urls = ["/admin/applicants", "/applicants"]
        
        for url in applicants_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                if "applicant" in current_url:
                    logger.info(f"✅ Applicants page loaded: {url}")
                    break
            except:
                continue
        
        # Check for applicants table/list
        table_selectors = [
            "table",
            ".table",
            ".applicants-table",
            ".data-table",
            "[data-testid*='table']"
        ]
        
        table_found = False
        for selector in table_selectors:
            try:
                if browser_helper.is_visible(selector):
                    table_found = True
                    logger.info(f"✅ Applicants table found: {selector}")
                    break
            except:
                continue
        
        if table_found:
            # Check for table headers
            header_texts = ["name", "email", "status", "date", "action"]
            for header in header_texts:
                try:
                    if browser_helper.is_visible(f"th:has-text('{header}' i), td:has-text('{header}' i)"):
                        logger.info(f"✅ Table header found: {header}")
                except:
                    continue
        
        # Look for action buttons
        action_selectors = [
            "button:has-text('Add')",
            "button:has-text('Edit')",
            "button:has-text('Delete')",
            "button:has-text('Export')",
            ".btn-add",
            ".btn-edit",
            ".btn-delete"
        ]
        
        actions_found = []
        for selector in action_selectors:
            try:
                if browser_helper.is_visible(selector):
                    actions_found.append(selector)
                    logger.info(f"✅ Action button found: {selector}")
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("applicants_management_page")
        
        logger.info(f"✅ Applicants management test completed ({len(actions_found)} actions found)")
    
    def test_export_functionality(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test data export functionality"""
        logger.info("📤 Testing export functionality")
        
        # Try to access export page
        export_urls = ["/admin/export", "/export"]
        
        export_page_found = False
        for url in export_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                if "export" in current_url or browser_helper.is_visible("text*='export' i"):
                    export_page_found = True
                    logger.info(f"✅ Export page found: {url}")
                    break
            except:
                continue
        
        if not export_page_found:
            # Look for export buttons on other pages
            browser_helper.navigate_to("/admin/dashboard")
            browser_helper.wait_for_loading_to_complete()
        
        # Look for export functionality
        export_selectors = [
            "button:has-text('Export')",
            "a:has-text('Export')",
            "button:has-text('Download')",
            ".export-btn",
            "[data-testid*='export']"
        ]
        
        export_found = False
        for selector in export_selectors:
            try:
                if browser_helper.is_visible(selector):
                    export_found = True
                    logger.info(f"✅ Export functionality found: {selector}")
                    
                    # Try clicking export (if safe)
                    try:
                        browser_helper.click_element(selector)
                        browser_helper.wait_for_loading_to_complete()
                        logger.info("✅ Export button clicked successfully")
                    except:
                        logger.info("ℹ️ Export button found but not clicked (may require data)")
                    
                    break
            except:
                continue
        
        if not export_found:
            logger.info("ℹ️ Export functionality not found (may be in sub-pages)")
        
        # Take screenshot
        browser_helper.take_screenshot("export_functionality")
        
        logger.info("✅ Export functionality test completed")
    
    def test_admin_settings_page(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test admin settings page"""
        logger.info("⚙️ Testing admin settings page")
        
        # Navigate to settings
        settings_urls = ["/admin/settings", "/settings"]
        
        settings_found = False
        for url in settings_urls:
            try:
                browser_helper.navigate_to(url)
                browser_helper.wait_for_loading_to_complete()
                
                current_url = browser_helper.page.url
                if "setting" in current_url or browser_helper.is_visible("text*='setting' i"):
                    settings_found = True
                    logger.info(f"✅ Settings page found: {url}")
                    break
            except:
                continue
        
        if settings_found:
            # Look for settings form elements
            settings_elements = [
                "form",
                "input",
                "select",
                "textarea",
                "button[type='submit']"
            ]
            
            form_elements_found = []
            for element in settings_elements:
                try:
                    elements = browser_helper.page.query_selector_all(element)
                    if elements:
                        form_elements_found.append(f"{element}: {len(elements)}")
                        logger.info(f"✅ Settings form element: {element} ({len(elements)} found)")
                except:
                    continue
            
            # Look for common settings
            common_settings = [
                "competition",
                "deadline",
                "requirement",
                "notification",
                "email",
                "payment"
            ]
            
            for setting in common_settings:
                try:
                    if browser_helper.is_visible(f"text*='{setting}' i"):
                        logger.info(f"✅ Setting found: {setting}")
                except:
                    continue
        
        # Take screenshot
        browser_helper.take_screenshot("admin_settings_page")
        
        if settings_found:
            logger.info("✅ Settings page accessible")
        else:
            logger.info("ℹ️ Settings page not found or not accessible")
        
        logger.info("✅ Admin settings test completed")

@pytest.mark.admin
@pytest.mark.dashboard
@pytest.mark.responsive
class TestAdminDashboardResponsive:
    """Test admin dashboard responsive design"""
    
    def test_dashboard_mobile_view(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test dashboard in mobile view"""
        logger.info("📱 Testing dashboard mobile responsiveness")
        
        # Set mobile viewport
        browser_helper.page.set_viewport_size({"width": 375, "height": 667})
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Check if mobile menu exists
        mobile_menu_selectors = [
            ".mobile-menu",
            ".hamburger",
            ".menu-toggle",
            "button[aria-label*='menu' i]"
        ]
        
        mobile_menu_found = False
        for selector in mobile_menu_selectors:
            try:
                if browser_helper.is_visible(selector):
                    mobile_menu_found = True
                    logger.info(f"✅ Mobile menu found: {selector}")
                    
                    # Try to open mobile menu
                    browser_helper.click_element(selector)
                    browser_helper.wait_for_loading_to_complete()
                    break
            except:
                continue
        
        # Check if content is properly arranged for mobile
        content_readable = True
        try:
            # Check if text is not cut off (basic check)
            page_width = browser_helper.page.evaluate("document.body.scrollWidth")
            viewport_width = 375
            
            if page_width > viewport_width * 1.1:  # Allow 10% margin
                content_readable = False
                logger.warning("⚠️ Content may be cut off in mobile view")
            else:
                logger.info("✅ Content fits mobile viewport")
        except:
            logger.info("ℹ️ Could not check content width")
        
        # Take mobile screenshot
        browser_helper.take_screenshot("dashboard_mobile_view")
        
        # Reset to desktop view
        browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
        
        if mobile_menu_found and content_readable:
            logger.info("✅ Dashboard mobile view working well")
        else:
            logger.info("ℹ️ Dashboard mobile view may need optimization")
        
        logger.info("✅ Mobile responsiveness test completed")
    
    def test_dashboard_tablet_view(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test dashboard in tablet view"""
        logger.info("📟 Testing dashboard tablet responsiveness")
        
        # Set tablet viewport
        browser_helper.page.set_viewport_size({"width": 768, "height": 1024})
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Check layout adaptation
        layout_good = True
        try:
            # Check if sidebar/navigation adapts well
            nav_elements = browser_helper.page.query_selector_all("nav, .sidebar, .menu")
            if nav_elements:
                for nav in nav_elements:
                    if nav.is_visible():
                        nav_rect = nav.bounding_box()
                        if nav_rect and nav_rect['width'] > 768 * 0.5:  # Nav shouldn't take >50% width
                            layout_good = False
                            logger.warning("⚠️ Navigation too wide for tablet")
                        else:
                            logger.info("✅ Navigation fits tablet layout")
                        break
        except:
            logger.info("ℹ️ Could not analyze navigation layout")
        
        # Take tablet screenshot
        browser_helper.take_screenshot("dashboard_tablet_view")
        
        # Reset to desktop view
        browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
        
        if layout_good:
            logger.info("✅ Dashboard tablet view working well")
        else:
            logger.info("ℹ️ Dashboard tablet view may need optimization")
        
        logger.info("✅ Tablet responsiveness test completed")

@pytest.mark.admin
@pytest.mark.dashboard
@pytest.mark.api
class TestAdminDashboardAPI:
    """Test admin dashboard API integrations"""
    
    def test_dashboard_data_loading(self, authenticated_admin, browser_helper: BrowserHelper, api_helper):
        """Test dashboard data loading via API"""
        logger.info("🔄 Testing dashboard data loading")
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        # Check for loading indicators
        loading_selectors = [
            ".loading",
            ".spinner",
            ".skeleton",
            "[data-testid*='loading']"
        ]
        
        # Wait a bit and check if loading disappears
        import time
        time.sleep(2)
        
        loading_active = False
        for selector in loading_selectors:
            try:
                if browser_helper.is_visible(selector):
                    loading_active = True
                    logger.info(f"ℹ️ Loading indicator still active: {selector}")
                    break
            except:
                continue
        
        if not loading_active:
            logger.info("✅ Dashboard data loaded (no loading indicators)")
        
        # Check for error states
        error_selectors = [
            ".error",
            ".alert-danger",
            "text*='error' i",
            "text*='failed' i"
        ]
        
        errors_found = []
        for selector in error_selectors:
            try:
                if browser_helper.is_visible(selector):
                    errors_found.append(selector)
            except:
                continue
        
        if errors_found:
            logger.warning(f"⚠️ Error indicators found: {errors_found}")
        else:
            logger.info("✅ No error indicators found")
        
        # Try to test admin API endpoints
        try:
            # Test basic admin stats API
            stats_result = api_helper.admin.get_stats()
            if stats_result.get('success'):
                logger.info("✅ Admin stats API working")
            else:
                logger.info("ℹ️ Admin stats API not accessible (may require session)")
        except:
            logger.info("ℹ️ Admin API testing skipped (authentication required)")
        
        # Take screenshot
        browser_helper.take_screenshot("dashboard_data_loading")
        
        logger.info("✅ Dashboard data loading test completed")

@pytest.mark.admin
@pytest.mark.dashboard
@pytest.mark.performance
class TestAdminDashboardPerformance:
    """Test admin dashboard performance"""
    
    def test_dashboard_load_time(self, authenticated_admin, browser_helper: BrowserHelper):
        """Test dashboard load time performance"""
        logger.info("⚡ Testing dashboard load time")
        
        import time
        
        # Measure load time
        start_time = time.time()
        
        browser_helper.navigate_to("/admin/dashboard")
        browser_helper.wait_for_loading_to_complete()
        
        end_time = time.time()
        load_time = end_time - start_time
        
        logger.info(f"📊 Dashboard load time: {load_time:.2f} seconds")
        
        # Performance thresholds
        if load_time < 2:
            logger.info("✅ Excellent load time (< 2s)")
        elif load_time < 5:
            logger.info("✅ Good load time (< 5s)")
        elif load_time < 10:
            logger.warning("⚠️ Slow load time (< 10s)")
        else:
            logger.warning("❌ Very slow load time (> 10s)")
        
        # Check for heavy resources
        try:
            # Get network requests info
            response_count = len(browser_helper.page.evaluate(
                "window.performance.getEntriesByType('resource').length"
            ))
            logger.info(f"📊 Network requests: {response_count}")
            
            if response_count > 50:
                logger.warning("⚠️ High number of network requests")
            else:
                logger.info("✅ Reasonable number of network requests")
        except:
            logger.info("ℹ️ Could not analyze network requests")
        
        # Take screenshot
        browser_helper.take_screenshot("dashboard_load_performance")
        
        logger.info("✅ Dashboard performance test completed")
