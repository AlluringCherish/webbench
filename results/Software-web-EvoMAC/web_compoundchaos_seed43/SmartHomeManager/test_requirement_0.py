'''
Test cases for SmartHomeManager web application to verify:
- Task 1: Website accessibility on local port 5000 and loading of the Dashboard page.
- Task 2: Dashboard page loads correctly with example data and basic navigation buttons present.
- Task 3: Presence and correctness of specified elements on all seven pages as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class SmartHomeManagerTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    # Task 1: Test website accessibility on local port 5000 (simulated by test client)
    def test_dashboard_accessible(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (status 200)")
    # Task 2: Test dashboard page loads correctly with example data and navigation buttons
    def test_dashboard_page_elements(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' must be present")
        # Check device summary div
        device_summary = soup.find(id='device-summary')
        self.assertIsNotNone(device_summary, "Device summary div with id 'device-summary' must be present")
        # Check navigation buttons by id
        nav_button_ids = [
            'device-list-button',
            'add-device-button',
            'automation-button',
            'energy-button',
            'activity-button'
        ]
        for btn_id in nav_button_ids:
            btn = soup.find(id=btn_id)
            self.assertIsNotNone(btn, f"Navigation button with id '{btn_id}' must be present on dashboard")
        # Check room list div
        room_list = soup.find(id='room-list')
        self.assertIsNotNone(room_list, "Room list div with id 'room-list' must be present on dashboard")
    # Task 3: Test presence and correctness of elements on all pages
    def test_device_list_page_elements(self):
        response = self.client.get('/device_list')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        device_list_page = soup.find(id='device-list-page')
        self.assertIsNotNone(device_list_page, "Device list page container div with id 'device-list-page' must be present")
        device_table = soup.find(id='device-table')
        self.assertIsNotNone(device_table, "Device table with id 'device-table' must be present")
        back_btn = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button with id 'back-to-dashboard' must be present")
        # Check at least one control-device-button-{device_id} if devices exist
        # Since example data is loaded, check for any button with id starting with 'control-device-button-'
        control_buttons = soup.find_all('button')
        found_control_button = any(btn.get('id', '').startswith('control-device-button-') for btn in control_buttons)
        self.assertTrue(found_control_button or len(control_buttons) == 0,
                        "At least one control device button with id starting 'control-device-button-' should be present if devices exist")
    def test_add_device_page_elements(self):
        response = self.client.get('/add_device')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        add_device_page = soup.find(id='add-device-page')
        self.assertIsNotNone(add_device_page, "Add device page container div with id 'add-device-page' must be present")
        device_name_input = soup.find(id='device-name')
        self.assertIsNotNone(device_name_input, "Input field with id 'device-name' must be present")
        device_type_dropdown = soup.find(id='device-type')
        self.assertIsNotNone(device_type_dropdown, "Dropdown with id 'device-type' must be present")
        device_room_dropdown = soup.find(id='device-room')
        self.assertIsNotNone(device_room_dropdown, "Dropdown with id 'device-room' must be present")
        submit_button = soup.find(id='submit-device-button')
        self.assertIsNotNone(submit_button, "Submit button with id 'submit-device-button' must be present")
        back_button = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_button, "Back to dashboard button with id 'back-to-dashboard' must be present")
    def test_device_control_page_elements(self):
        # To test device control page, we need a valid device_id from example data
        # From example data, device_id=1 exists
        response = self.client.get('/device_control/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        device_control_page = soup.find(id='device-control-page')
        self.assertIsNotNone(device_control_page, "Device control page container div with id 'device-control-page' must be present")
        device_name_display = soup.find(id='device-name-display')
        self.assertIsNotNone(device_name_display, "Device name display with id 'device-name-display' must be present")
        device_status_display = soup.find(id='device-status-display')
        self.assertIsNotNone(device_status_display, "Device status display with id 'device-status-display' must be present")
        power_toggle = soup.find(id='power-toggle')
        self.assertIsNotNone(power_toggle, "Power toggle button with id 'power-toggle' must be present")
        save_settings_button = soup.find(id='save-settings-button')
        self.assertIsNotNone(save_settings_button, "Save settings button with id 'save-settings-button' must be present")
        back_to_devices = soup.find(id='back-to-devices')
        self.assertIsNotNone(back_to_devices, "Back to device list button with id 'back-to-devices' must be present")
    def test_automation_rules_page_elements(self):
        response = self.client.get('/automation_rules')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        automation_page = soup.find(id='automation-page')
        self.assertIsNotNone(automation_page, "Automation rules page container div with id 'automation-page' must be present")
        rules_table = soup.find(id='rules-table')
        self.assertIsNotNone(rules_table, "Rules table with id 'rules-table' must be present")
        rule_name_input = soup.find(id='rule-name')
        self.assertIsNotNone(rule_name_input, "Input field with id 'rule-name' must be present")
        trigger_type_dropdown = soup.find(id='trigger-type')
        self.assertIsNotNone(trigger_type_dropdown, "Dropdown with id 'trigger-type' must be present")
        trigger_value_input = soup.find(id='trigger-value')
        self.assertIsNotNone(trigger_value_input, "Input field with id 'trigger-value' must be present")
        action_device_dropdown = soup.find(id='action-device')
        self.assertIsNotNone(action_device_dropdown, "Dropdown with id 'action-device' must be present")
        action_type_dropdown = soup.find(id='action-type')
        self.assertIsNotNone(action_type_dropdown, "Dropdown with id 'action-type' must be present")
        add_rule_button = soup.find(id='add-rule-button')
        self.assertIsNotNone(add_rule_button, "Add rule button with id 'add-rule-button' must be present")
        back_to_dashboard = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_to_dashboard, "Back to dashboard button with id 'back-to-dashboard' must be present")
    def test_energy_report_page_elements(self):
        response = self.client.get('/energy_report')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        energy_page = soup.find(id='energy-page')
        self.assertIsNotNone(energy_page, "Energy report page container div with id 'energy-page' must be present")
        energy_summary = soup.find(id='energy-summary')
        self.assertIsNotNone(energy_summary, "Energy summary div with id 'energy-summary' must be present")
        energy_table = soup.find(id='energy-table')
        self.assertIsNotNone(energy_table, "Energy table with id 'energy-table' must be present")
        date_filter_input = soup.find(id='date-filter')
        self.assertIsNotNone(date_filter_input, "Date filter input with id 'date-filter' must be present")
        apply_filter_button = soup.find(id='apply-filter-button')
        self.assertIsNotNone(apply_filter_button, "Apply filter button with id 'apply-filter-button' must be present")
        back_to_dashboard = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_to_dashboard, "Back to dashboard button with id 'back-to-dashboard' must be present")
    def test_activity_logs_page_elements(self):
        response = self.client.get('/activity_logs')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        activity_page = soup.find(id='activity-page')
        self.assertIsNotNone(activity_page, "Activity logs page container div with id 'activity-page' must be present")
        activity_table = soup.find(id='activity-table')
        self.assertIsNotNone(activity_table, "Activity table with id 'activity-table' must be present")
        search_activity_input = soup.find(id='search-activity')
        self.assertIsNotNone(search_activity_input, "Search activity input with id 'search-activity' must be present")
        apply_search_button = soup.find(id='apply-search-button')
        self.assertIsNotNone(apply_search_button, "Apply search button with id 'apply-search-button' must be present")
        back_to_dashboard = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_to_dashboard, "Back to dashboard button with id 'back-to-dashboard' must be present")
if __name__ == '__main__':
    unittest.main()