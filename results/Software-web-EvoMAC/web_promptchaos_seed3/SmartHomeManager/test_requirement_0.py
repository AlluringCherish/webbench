'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of the required elements:
- ID: dashboard-page (Div container)
- ID: device-summary (Div showing total devices, active devices, offline devices)
- Buttons with IDs: device-list-button, add-device-button, automation-button, energy-button, activity-button
- ID: room-list (Div listing all rooms with device counts)
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class SmartHomeManagerTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET on '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
    def test_dashboard_content_elements(self):
        # Test that the dashboard page contains all required elements with correct IDs and content
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' not found")
        # Check device-summary div and its content
        device_summary = dashboard_div.find('div', id='device-summary')
        self.assertIsNotNone(device_summary, "Device summary div with id 'device-summary' not found")
        # Check that it contains Total Devices, Active Devices, Offline Devices text
        summary_text = device_summary.get_text()
        self.assertIn("Total Devices:", summary_text, "Total Devices count not found in device-summary")
        self.assertIn("Active Devices:", summary_text, "Active Devices count not found in device-summary")
        self.assertIn("Offline Devices:", summary_text, "Offline Devices count not found in device-summary")
        # Check buttons by ID and their hrefs
        button_ids = [
            'device-list-button',
            'add-device-button',
            'automation-button',
            'energy-button',
            'activity-button'
        ]
        for btn_id in button_ids:
            btn = dashboard_div.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Button with id '{btn_id}' not found on dashboard")
            # Check that button has an onclick attribute with url_for link
            onclick = btn.get('onclick', '')
            self.assertTrue(onclick.startswith("location.href="), f"Button '{btn_id}' does not have correct onclick navigation")
        # Check room-list div and that it lists rooms with device counts
        room_list_div = dashboard_div.find('div', id='room-list')
        self.assertIsNotNone(room_list_div, "Room list div with id 'room-list' not found")
        # It should contain an <h2> with text 'Rooms'
        h2 = room_list_div.find('h2')
        self.assertIsNotNone(h2, "Room list section missing <h2> header")
        self.assertEqual(h2.text.strip(), "Rooms", "Room list <h2> header text is not 'Rooms'")
        # It should contain either a <ul> with <li> items or a <p> with 'No rooms found.'
        ul = room_list_div.find('ul')
        p = room_list_div.find('p')
        self.assertTrue(ul is not None or (p is not None and 'No rooms found' in p.text), "Room list does not contain a list or 'No rooms found' message")
    def test_dashboard_navigation_buttons(self):
        # Test that clicking navigation buttons leads to correct pages (simulate by checking URLs)
        # Since we cannot click buttons in unittest, we check the URLs in onclick attributes
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        nav_map = {
            'device-list-button': '/devices',
            'add-device-button': '/add_device',
            'automation-button': '/automation',
            'energy-button': '/energy',
            'activity-button': '/activity'
        }
        for btn_id, expected_path in nav_map.items():
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Button '{btn_id}' not found for navigation test")
            onclick = btn.get('onclick', '')
            # Extract URL from onclick string: location.href='URL'
            import re
            match = re.search(r"location\.href='([^']+)'", onclick)
            self.assertIsNotNone(match, f"Button '{btn_id}' onclick does not contain a URL")
            url = match.group(1)
            self.assertEqual(url, expected_path, f"Button '{btn_id}' onclick URL '{url}' does not match expected '{expected_path}'")
if __name__ == '__main__':
    unittest.main()