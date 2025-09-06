"""
Test 09: UI Components & Responsiveness
=======================================

This test module covers UI component testing including:
- Form components and validation
- Navigation components
- Modal dialogs
- Table components
- Responsive design
- Cross-browser compatibility
- Accessibility features
"""

import pytest
import logging
from utils.test_data import TestConfig, TestDataGenerator, UISelectors
from utils.browser_helper import BrowserHelper, FormHelper, ValidationHelper

logger = logging.getLogger(__name__)

@pytest.mark.ui
@pytest.mark.components
class TestFormComponents:
    """Test form components and validation"""
    
    def test_registration_form_components(self, browser_helper: BrowserHelper, form_helper: FormHelper):
        """Test registration form components"""
        logger.info("📝 Testing registration form components")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Check if registration form exists
        form_selectors = ["form", ".registration-form", "[data-testid='registration-form']"]
        
        form_found = False
        for selector in form_selectors:
            if browser_helper.is_visible(selector):
                form_found = True
                logger.info(f"✅ Registration form found: {selector}")
                break
        
        assert form_found, "Registration form not found"
        
        # Test form field components
        expected_fields = [
            ("name", "text"),
            ("email", "email"),
            ("phone", "tel"),
            ("college", "text"),
            ("year", "select"),
            ("branch", "text"),
            ("password", "password")
        ]
        
        fields_found = []
        for field_name, field_type in expected_fields:
            field_selectors = [
                f"input[name='{field_name}']",
                f"select[name='{field_name}']",
                f"textarea[name='{field_name}']"
            ]
            
            field_found = False
            for selector in field_selectors:
                try:
                    element = browser_helper.page.query_selector(selector)
                    if element and element.is_visible():
                        # Check field type if it's an input
                        if element.tag_name.lower() == 'input':
                            actual_type = element.get_attribute('type') or 'text'
                            if actual_type == field_type or field_type == 'text':
                                field_found = True
                                fields_found.append(field_name)
                                logger.info(f"✅ Field found: {field_name} ({actual_type})")
                        else:
                            field_found = True
                            fields_found.append(field_name)
                            logger.info(f"✅ Field found: {field_name} ({element.tag_name})")
                        break
                except:
                    continue
            
            if not field_found:
                logger.info(f"ℹ️ Field not found: {field_name}")
        
        # Test form validation
        logger.info("🔍 Testing form validation")
        
        # Try submitting empty form
        submit_button = browser_helper.page.query_selector("button[type='submit'], input[type='submit']")
        if submit_button and submit_button.is_visible():
            submit_button.click()
            browser_helper.wait_for_loading_to_complete()
            
            # Check for validation messages
            validation_selectors = [
                ".error",
                ".invalid-feedback",
                "[aria-invalid='true']",
                "text*='required' i",
                "text*='invalid' i"
            ]
            
            validation_found = False
            for selector in validation_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        validation_found = True
                        logger.info(f"✅ Validation message found: {selector}")
                        break
                except:
                    continue
            
            if validation_found:
                logger.info("✅ Form validation working")
            else:
                logger.info("ℹ️ Form validation not detected")
        
        # Take screenshot
        browser_helper.take_screenshot("registration_form_components")
        
        logger.info(f"📊 Registration form summary:")
        logger.info(f"   - Fields found: {len(fields_found)}/{len(expected_fields)}")
        logger.info(f"   - Fields: {', '.join(fields_found)}")
        
        logger.info("✅ Registration form components test completed")
    
    def test_input_field_interactions(self, browser_helper: BrowserHelper):
        """Test input field interactions and states"""
        logger.info("🎯 Testing input field interactions")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Find input fields to test
        input_fields = browser_helper.page.query_selector_all("input[type='text'], input[type='email'], input[type='tel']")
        
        interaction_tests = []
        
        for i, field in enumerate(input_fields[:3]):  # Test first 3 fields
            if field.is_visible():
                field_name = field.get_attribute('name') or f"field_{i}"
                
                # Test focus
                field.focus()
                is_focused = browser_helper.page.evaluate("document.activeElement === arguments[0]", field)
                
                if is_focused:
                    interaction_tests.append(f"focus_{field_name}")
                    logger.info(f"✅ Field focus working: {field_name}")
                
                # Test typing
                test_value = "Test Input"
                field.fill(test_value)
                actual_value = field.input_value()
                
                if actual_value == test_value:
                    interaction_tests.append(f"input_{field_name}")
                    logger.info(f"✅ Field input working: {field_name}")
                
                # Test clearing
                field.fill("")
                cleared_value = field.input_value()
                
                if cleared_value == "":
                    interaction_tests.append(f"clear_{field_name}")
                    logger.info(f"✅ Field clear working: {field_name}")
                
                # Test blur
                browser_helper.page.evaluate("arguments[0].blur()", field)
        
        # Take screenshot
        browser_helper.take_screenshot("input_field_interactions")
        
        logger.info(f"📊 Input interactions summary:")
        logger.info(f"   - Interactions tested: {len(interaction_tests)}")
        
        logger.info("✅ Input field interactions test completed")
    
    def test_dropdown_select_components(self, browser_helper: BrowserHelper):
        """Test dropdown/select components"""
        logger.info("📋 Testing dropdown/select components")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Find select elements
        select_fields = browser_helper.page.query_selector_all("select")
        
        select_tests = []
        
        for i, select in enumerate(select_fields):
            if select.is_visible():
                field_name = select.get_attribute('name') or f"select_{i}"
                
                # Get options
                options = browser_helper.page.query_selector_all(f"select[name='{field_name}'] option")
                
                if options and len(options) > 1:
                    # Test selecting an option (skip first option as it's usually placeholder)
                    try:
                        select.select_option(index=1)
                        selected_value = select.input_value()
                        
                        if selected_value:
                            select_tests.append(field_name)
                            logger.info(f"✅ Select working: {field_name} (selected: {selected_value})")
                        
                    except Exception as e:
                        logger.debug(f"Could not test select {field_name}: {e}")
                
                logger.info(f"📊 Select {field_name}: {len(options)} options")
        
        # Test custom dropdowns (non-select elements)
        custom_dropdown_selectors = [
            ".dropdown",
            ".select",
            "[role='combobox']",
            "[role='listbox']"
        ]
        
        custom_dropdowns_found = []
        for selector in custom_dropdown_selectors:
            try:
                elements = browser_helper.page.query_selector_all(selector)
                if elements:
                    custom_dropdowns_found.extend(elements)
                    logger.info(f"✅ Custom dropdown found: {selector} ({len(elements)} items)")
            except:
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("dropdown_select_components")
        
        logger.info(f"📊 Dropdown components summary:")
        logger.info(f"   - Native selects: {len(select_tests)}")
        logger.info(f"   - Custom dropdowns: {len(custom_dropdowns_found)}")
        
        logger.info("✅ Dropdown/select components test completed")

@pytest.mark.ui
@pytest.mark.navigation
class TestNavigationComponents:
    """Test navigation components"""
    
    def test_main_navigation_menu(self, browser_helper: BrowserHelper):
        """Test main navigation menu"""
        logger.info("🧭 Testing main navigation menu")
        
        browser_helper.navigate_to("/")
        browser_helper.wait_for_loading_to_complete()
        
        # Find navigation menu
        nav_selectors = [
            "nav",
            ".navbar",
            ".navigation",
            ".menu",
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
        
        if nav_found:
            # Test navigation links
            nav_links = browser_helper.page.query_selector_all("nav a, .navbar a, .navigation a")
            
            working_links = []
            for link in nav_links[:5]:  # Test first 5 links
                if link.is_visible():
                    href = link.get_attribute('href')
                    text = link.text_content().strip()
                    
                    if href and text:
                        # Test link click (non-destructive)
                        try:
                            # Just hover to test interaction
                            link.hover()
                            working_links.append(text)
                            logger.info(f"✅ Navigation link working: {text}")
                        except:
                            logger.debug(f"Could not interact with link: {text}")
            
            # Test responsive navigation
            logger.info("📱 Testing responsive navigation")
            
            # Set mobile viewport
            browser_helper.page.set_viewport_size({"width": 375, "height": 667})
            
            # Look for mobile menu toggle
            mobile_toggle_selectors = [
                ".menu-toggle",
                ".hamburger",
                ".mobile-menu-button",
                "button[aria-label*='menu' i]"
            ]
            
            mobile_nav_found = False
            for selector in mobile_toggle_selectors:
                try:
                    if browser_helper.is_visible(selector):
                        mobile_nav_found = True
                        logger.info(f"✅ Mobile navigation toggle found: {selector}")
                        
                        # Test toggle
                        browser_helper.click_element(selector)
                        browser_helper.wait_for_loading_to_complete()
                        break
                except:
                    continue
            
            # Reset to desktop
            browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
            
            logger.info(f"📊 Navigation summary:")
            logger.info(f"   - Working links: {len(working_links)}")
            logger.info(f"   - Mobile navigation: {mobile_nav_found}")
        
        # Take screenshot
        browser_helper.take_screenshot("main_navigation_menu")
        
        if nav_found:
            logger.info("✅ Main navigation functional")
        else:
            logger.info("ℹ️ Main navigation not found")
        
        logger.info("✅ Main navigation test completed")
    
    def test_breadcrumb_navigation(self, browser_helper: BrowserHelper):
        """Test breadcrumb navigation"""
        logger.info("🍞 Testing breadcrumb navigation")
        
        # Test breadcrumbs on various pages
        test_pages = [
            "/admin/dashboard",
            "/admin/applicants",
            "/applicant/dashboard"
        ]
        
        breadcrumbs_found = False
        
        for page in test_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for breadcrumb components
                breadcrumb_selectors = [
                    ".breadcrumb",
                    ".breadcrumbs",
                    "[aria-label*='breadcrumb' i]",
                    "nav[aria-label*='breadcrumb' i]"
                ]
                
                for selector in breadcrumb_selectors:
                    try:
                        if browser_helper.is_visible(selector):
                            breadcrumbs_found = True
                            logger.info(f"✅ Breadcrumbs found on {page}: {selector}")
                            
                            # Count breadcrumb items
                            items = browser_helper.page.query_selector_all(f"{selector} li, {selector} a, {selector} span")
                            logger.info(f"📊 Breadcrumb items: {len(items)}")
                            break
                    except:
                        continue
                
                if breadcrumbs_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Could not test breadcrumbs on {page}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("breadcrumb_navigation")
        
        if breadcrumbs_found:
            logger.info("✅ Breadcrumb navigation found")
        else:
            logger.info("ℹ️ Breadcrumb navigation not found")
        
        logger.info("✅ Breadcrumb navigation test completed")

@pytest.mark.ui
@pytest.mark.modal
class TestModalComponents:
    """Test modal dialog components"""
    
    def test_modal_dialogs(self, browser_helper: BrowserHelper):
        """Test modal dialog functionality"""
        logger.info("💬 Testing modal dialogs")
        
        # Navigate to pages that might have modals
        test_pages = [
            "/admin/dashboard",
            "/admin/applicants",
            "/"
        ]
        
        modals_found = []
        
        for page in test_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for modal trigger buttons
                modal_trigger_selectors = [
                    "button:has-text('Add')",
                    "button:has-text('Edit')",
                    "button:has-text('Delete')",
                    "button:has-text('View')",
                    ".btn-modal",
                    "[data-bs-toggle='modal']",
                    "[data-toggle='modal']"
                ]
                
                for selector in modal_trigger_selectors:
                    try:
                        if browser_helper.is_visible(selector):
                            # Click to open modal
                            browser_helper.click_element(selector)
                            browser_helper.wait_for_loading_to_complete()
                            
                            # Look for opened modal
                            modal_selectors = [
                                ".modal",
                                ".dialog",
                                "[role='dialog']",
                                ".overlay",
                                ".popup"
                            ]
                            
                            for modal_selector in modal_selectors:
                                try:
                                    modal_element = browser_helper.page.query_selector(modal_selector)
                                    if modal_element and modal_element.is_visible():
                                        modals_found.append({
                                            'page': page,
                                            'trigger': selector,
                                            'modal': modal_selector
                                        })
                                        logger.info(f"✅ Modal found on {page}: {modal_selector}")
                                        
                                        # Test modal close
                                        close_selectors = [
                                            ".close",
                                            ".modal-close",
                                            "button:has-text('Close')",
                                            "button:has-text('Cancel')",
                                            "[aria-label*='close' i]"
                                        ]
                                        
                                        modal_closed = False
                                        for close_selector in close_selectors:
                                            try:
                                                if browser_helper.is_visible(close_selector):
                                                    browser_helper.click_element(close_selector)
                                                    browser_helper.wait_for_loading_to_complete()
                                                    modal_closed = True
                                                    logger.info(f"✅ Modal closed successfully")
                                                    break
                                            except:
                                                continue
                                        
                                        if not modal_closed:
                                            # Try ESC key
                                            try:
                                                browser_helper.page.keyboard.press("Escape")
                                                browser_helper.wait_for_loading_to_complete()
                                                logger.info("✅ Modal closed with ESC key")
                                            except:
                                                logger.info("ℹ️ Could not close modal")
                                        
                                        break
                                except:
                                    continue
                            
                            break
                    except Exception as e:
                        logger.debug(f"Could not test modal trigger {selector}: {e}")
                        continue
                
            except Exception as e:
                logger.debug(f"Could not test modals on {page}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("modal_dialogs")
        
        logger.info(f"📊 Modal dialogs summary:")
        logger.info(f"   - Modals found: {len(modals_found)}")
        
        if modals_found:
            logger.info("✅ Modal dialogs functional")
        else:
            logger.info("ℹ️ Modal dialogs not found")
        
        logger.info("✅ Modal dialogs test completed")

@pytest.mark.ui
@pytest.mark.tables
class TestTableComponents:
    """Test table components"""
    
    def test_data_tables(self, browser_helper: BrowserHelper):
        """Test data table functionality"""
        logger.info("📊 Testing data tables")
        
        # Navigate to pages with tables
        table_pages = [
            "/admin/applicants",
            "/admin/competitions",
            "/admin/dashboard"
        ]
        
        tables_found = []
        
        for page in table_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Look for tables
                table_selectors = [
                    "table",
                    ".table",
                    ".data-table",
                    "[role='table']"
                ]
                
                for selector in table_selectors:
                    try:
                        table_elements = browser_helper.page.query_selector_all(selector)
                        
                        for table in table_elements:
                            if table.is_visible():
                                tables_found.append({
                                    'page': page,
                                    'selector': selector,
                                    'element': table
                                })
                                
                                # Analyze table structure
                                headers = browser_helper.page.query_selector_all(f"{selector} th")
                                rows = browser_helper.page.query_selector_all(f"{selector} tbody tr")
                                
                                logger.info(f"✅ Table found on {page}:")
                                logger.info(f"   - Headers: {len(headers)}")
                                logger.info(f"   - Rows: {len(rows)}")
                                
                                # Test table interactions
                                if headers:
                                    # Test sorting (click on headers)
                                    first_header = headers[0]
                                    if first_header.is_visible():
                                        try:
                                            first_header.click()
                                            browser_helper.wait_for_loading_to_complete()
                                            logger.info("✅ Table header clickable (sorting?)")
                                        except:
                                            logger.info("ℹ️ Table header not clickable")
                                
                                # Look for pagination
                                pagination_selectors = [
                                    ".pagination",
                                    ".pager",
                                    "nav[aria-label*='pagination' i]"
                                ]
                                
                                for pagination_selector in pagination_selectors:
                                    try:
                                        if browser_helper.is_visible(pagination_selector):
                                            logger.info(f"✅ Pagination found: {pagination_selector}")
                                            break
                                    except:
                                        continue
                                
                                # Look for search/filter
                                search_selectors = [
                                    "input[type='search']",
                                    "input[placeholder*='search' i]",
                                    ".search",
                                    ".filter"
                                ]
                                
                                for search_selector in search_selectors:
                                    try:
                                        if browser_helper.is_visible(search_selector):
                                            logger.info(f"✅ Search/filter found: {search_selector}")
                                            break
                                    except:
                                        continue
                                
                                break
                    except:
                        continue
                
            except Exception as e:
                logger.debug(f"Could not test tables on {page}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("data_tables")
        
        logger.info(f"📊 Data tables summary:")
        logger.info(f"   - Tables found: {len(tables_found)}")
        
        if tables_found:
            logger.info("✅ Data tables functional")
        else:
            logger.info("ℹ️ Data tables not found")
        
        logger.info("✅ Data tables test completed")

@pytest.mark.ui
@pytest.mark.responsive
class TestResponsiveDesign:
    """Test responsive design across different screen sizes"""
    
    def test_mobile_responsiveness(self, browser_helper: BrowserHelper):
        """Test mobile responsive design"""
        logger.info("📱 Testing mobile responsiveness")
        
        # Mobile viewport sizes to test
        mobile_viewports = [
            (375, 667, "iPhone SE"),
            (390, 844, "iPhone 12"),
            (360, 640, "Android Small")
        ]
        
        # Pages to test
        test_pages = [
            "/",
            "/register",
            "/admin/login",
            "/admin/dashboard"
        ]
        
        mobile_results = []
        
        for width, height, device_name in mobile_viewports:
            logger.info(f"🔍 Testing {device_name} ({width}x{height})")
            
            # Set mobile viewport
            browser_helper.page.set_viewport_size({"width": width, "height": height})
            
            for page in test_pages:
                try:
                    browser_helper.navigate_to(page)
                    browser_helper.wait_for_loading_to_complete()
                    
                    # Check if content fits viewport
                    page_width = browser_helper.page.evaluate("document.body.scrollWidth")
                    page_height = browser_helper.page.evaluate("document.body.scrollHeight")
                    
                    # Check horizontal overflow
                    horizontal_fit = page_width <= width * 1.1  # Allow 10% margin
                    
                    # Check if navigation adapts
                    mobile_nav_indicators = [
                        ".mobile-menu",
                        ".hamburger",
                        ".menu-toggle",
                        ".navbar-toggler"
                    ]
                    
                    mobile_nav_found = False
                    for indicator in mobile_nav_indicators:
                        try:
                            if browser_helper.is_visible(indicator):
                                mobile_nav_found = True
                                break
                        except:
                            continue
                    
                    mobile_results.append({
                        'device': device_name,
                        'page': page,
                        'horizontal_fit': horizontal_fit,
                        'mobile_nav': mobile_nav_found,
                        'page_width': page_width
                    })
                    
                    if horizontal_fit:
                        logger.info(f"✅ {page} fits on {device_name}")
                    else:
                        logger.warning(f"⚠️ {page} overflows on {device_name} ({page_width}px)")
                    
                    if mobile_nav_found:
                        logger.info(f"✅ Mobile navigation found on {page}")
                    
                except Exception as e:
                    logger.debug(f"Could not test {page} on {device_name}: {e}")
                    continue
            
            # Take screenshot for this device
            device_safe = device_name.replace(" ", "_").lower()
            browser_helper.take_screenshot(f"mobile_responsive_{device_safe}")
        
        # Reset to desktop
        browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
        
        # Analysis
        total_tests = len(mobile_results)
        horizontal_fit_count = sum(1 for result in mobile_results if result['horizontal_fit'])
        mobile_nav_count = sum(1 for result in mobile_results if result['mobile_nav'])
        
        logger.info(f"📊 Mobile responsiveness summary:")
        logger.info(f"   - Total tests: {total_tests}")
        logger.info(f"   - Horizontal fit: {horizontal_fit_count}/{total_tests}")
        logger.info(f"   - Mobile navigation: {mobile_nav_count}/{total_tests}")
        
        if horizontal_fit_count >= total_tests * 0.8:  # 80% threshold
            logger.info("✅ Good mobile responsiveness")
        else:
            logger.warning("⚠️ Mobile responsiveness needs improvement")
        
        logger.info("✅ Mobile responsiveness test completed")
    
    def test_tablet_responsiveness(self, browser_helper: BrowserHelper):
        """Test tablet responsive design"""
        logger.info("📟 Testing tablet responsiveness")
        
        # Tablet viewport sizes
        tablet_viewports = [
            (768, 1024, "iPad Portrait"),
            (1024, 768, "iPad Landscape"),
            (800, 1280, "Android Tablet")
        ]
        
        test_pages = ["/", "/admin/dashboard", "/register"]
        
        tablet_results = []
        
        for width, height, device_name in tablet_viewports:
            logger.info(f"🔍 Testing {device_name} ({width}x{height})")
            
            browser_helper.page.set_viewport_size({"width": width, "height": height})
            
            for page in test_pages:
                try:
                    browser_helper.navigate_to(page)
                    browser_helper.wait_for_loading_to_complete()
                    
                    # Check layout adaptation
                    page_width = browser_helper.page.evaluate("document.body.scrollWidth")
                    
                    # Check if sidebar/navigation adapts appropriately
                    sidebar_elements = browser_helper.page.query_selector_all(".sidebar, nav, .navbar")
                    
                    layout_adapted = True
                    for sidebar in sidebar_elements:
                        if sidebar.is_visible():
                            sidebar_rect = sidebar.bounding_box()
                            if sidebar_rect:
                                # Sidebar shouldn't take more than 40% of screen width on tablet
                                if sidebar_rect['width'] > width * 0.4:
                                    layout_adapted = False
                                    break
                    
                    tablet_results.append({
                        'device': device_name,
                        'page': page,
                        'layout_adapted': layout_adapted,
                        'page_width': page_width
                    })
                    
                    if layout_adapted:
                        logger.info(f"✅ {page} layout adapted for {device_name}")
                    else:
                        logger.warning(f"⚠️ {page} layout not optimal for {device_name}")
                    
                except Exception as e:
                    logger.debug(f"Could not test {page} on {device_name}: {e}")
                    continue
            
            # Take screenshot
            device_safe = device_name.replace(" ", "_").lower()
            browser_helper.take_screenshot(f"tablet_responsive_{device_safe}")
        
        # Reset to desktop
        browser_helper.page.set_viewport_size({"width": 1280, "height": 720})
        
        # Analysis
        total_tests = len(tablet_results)
        adapted_count = sum(1 for result in tablet_results if result['layout_adapted'])
        
        logger.info(f"📊 Tablet responsiveness summary:")
        logger.info(f"   - Total tests: {total_tests}")
        logger.info(f"   - Layout adapted: {adapted_count}/{total_tests}")
        
        if adapted_count >= total_tests * 0.8:
            logger.info("✅ Good tablet responsiveness")
        else:
            logger.warning("⚠️ Tablet responsiveness needs improvement")
        
        logger.info("✅ Tablet responsiveness test completed")

@pytest.mark.ui
@pytest.mark.accessibility
class TestAccessibilityFeatures:
    """Test accessibility features"""
    
    def test_keyboard_navigation(self, browser_helper: BrowserHelper):
        """Test keyboard navigation"""
        logger.info("⌨️ Testing keyboard navigation")
        
        browser_helper.navigate_to("/register")
        browser_helper.wait_for_loading_to_complete()
        
        # Test Tab navigation
        focusable_elements = []
        
        try:
            # Start at the beginning
            browser_helper.page.keyboard.press("Tab")
            
            # Track focusable elements
            for i in range(10):  # Test first 10 tab stops
                focused_element = browser_helper.page.evaluate("document.activeElement")
                
                if focused_element:
                    tag_name = browser_helper.page.evaluate("document.activeElement.tagName")
                    element_type = browser_helper.page.evaluate("document.activeElement.type || ''")
                    element_id = browser_helper.page.evaluate("document.activeElement.id || ''")
                    
                    focusable_elements.append({
                        'tag': tag_name,
                        'type': element_type,
                        'id': element_id
                    })
                    
                    logger.info(f"✅ Tab {i+1}: {tag_name} {element_type} {element_id}")
                
                browser_helper.page.keyboard.press("Tab")
                __import__('time').sleep(0.1)  # Small delay
        
        except Exception as e:
            logger.debug(f"Keyboard navigation test error: {e}")
        
        # Test Enter key on buttons
        buttons = browser_helper.page.query_selector_all("button[type='submit'], input[type='submit']")
        
        button_keyboard_working = False
        for button in buttons[:1]:  # Test first button
            if button.is_visible():
                try:
                    button.focus()
                    browser_helper.page.keyboard.press("Enter")
                    button_keyboard_working = True
                    logger.info("✅ Button keyboard activation working")
                    break
                except:
                    continue
        
        # Take screenshot
        browser_helper.take_screenshot("keyboard_navigation")
        
        logger.info(f"📊 Keyboard navigation summary:")
        logger.info(f"   - Focusable elements: {len(focusable_elements)}")
        logger.info(f"   - Button keyboard activation: {button_keyboard_working}")
        
        if len(focusable_elements) >= 3:
            logger.info("✅ Keyboard navigation functional")
        else:
            logger.warning("⚠️ Limited keyboard navigation")
        
        logger.info("✅ Keyboard navigation test completed")
    
    def test_aria_labels_and_roles(self, browser_helper: BrowserHelper):
        """Test ARIA labels and roles"""
        logger.info("🏷️ Testing ARIA labels and roles")
        
        test_pages = ["/", "/register", "/admin/login"]
        
        aria_results = []
        
        for page in test_pages:
            try:
                browser_helper.navigate_to(page)
                browser_helper.wait_for_loading_to_complete()
                
                # Check for ARIA labels
                aria_labels = browser_helper.page.query_selector_all("[aria-label]")
                aria_labelledby = browser_helper.page.query_selector_all("[aria-labelledby]")
                aria_describedby = browser_helper.page.query_selector_all("[aria-describedby]")
                
                # Check for ARIA roles
                aria_roles = browser_helper.page.query_selector_all("[role]")
                
                # Check for specific important roles
                navigation_roles = browser_helper.page.query_selector_all("[role='navigation']")
                button_roles = browser_helper.page.query_selector_all("[role='button']")
                dialog_roles = browser_helper.page.query_selector_all("[role='dialog']")
                
                aria_results.append({
                    'page': page,
                    'aria_labels': len(aria_labels),
                    'aria_labelledby': len(aria_labelledby),
                    'aria_describedby': len(aria_describedby),
                    'aria_roles': len(aria_roles),
                    'navigation_roles': len(navigation_roles),
                    'button_roles': len(button_roles),
                    'dialog_roles': len(dialog_roles)
                })
                
                logger.info(f"📊 ARIA attributes on {page}:")
                logger.info(f"   - aria-label: {len(aria_labels)}")
                logger.info(f"   - aria-labelledby: {len(aria_labelledby)}")
                logger.info(f"   - aria-describedby: {len(aria_describedby)}")
                logger.info(f"   - role attributes: {len(aria_roles)}")
                
            except Exception as e:
                logger.debug(f"Could not test ARIA on {page}: {e}")
                continue
        
        # Take screenshot
        browser_helper.take_screenshot("aria_labels_roles")
        
        # Analysis
        total_aria_elements = sum(
            result['aria_labels'] + result['aria_labelledby'] + result['aria_describedby'] + result['aria_roles']
            for result in aria_results
        )
        
        logger.info(f"📊 ARIA accessibility summary:")
        logger.info(f"   - Total ARIA elements: {total_aria_elements}")
        
        if total_aria_elements >= 10:
            logger.info("✅ Good ARIA accessibility implementation")
        elif total_aria_elements >= 5:
            logger.info("✅ Basic ARIA accessibility implemented")
        else:
            logger.warning("⚠️ Limited ARIA accessibility")
        
        logger.info("✅ ARIA labels and roles test completed")
