'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
Testing Task 3: Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestSmartHomeManagerDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test Task 2: Check page title is "Smart Home Dashboard"
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Smart Home Dashboard", "Dashboard page title should be 'Smart Home Dashboard'")
    def test_dashboard_device_summary_elements(self):
        # Test Task 3: Check device-summary div and its contents
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        device_summary = soup.find(id='device-summary')
        self.assertIsNotNone(device_summary, "Dashboard must have a div with id 'device-summary'")
        # Check that it contains total devices, active devices, offline devices counts
        texts = device_summary.stripped_strings
        texts = list(texts)
        self.assertTrue(any("Total Devices:" in t for t in texts), "Device summary must show 'Total Devices'")
        self.assertTrue(any("Active Devices:" in t for t in texts), "Device summary must show 'Active Devices'")
        self.assertTrue(any("Offline Devices:" in t for t in texts), "Device summary must show 'Offline Devices'")
    def test_dashboard_navigation_buttons(self):
        # Test Task 3: Check presence and correctness of navigation buttons with correct IDs and hrefs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        nav_buttons = {
            'device-list-button': '/devices',
            'add-device-button': '/devices/add',
            'automation-button': '/automation',
            'energy-button': '/energy',
            'activity-button': '/activity'
        }
        for btn_id, expected_path in nav_buttons.items():
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Button with id '{btn_id}' must be present on dashboard")
            # The button uses onclick with location.href, check the URL
            onclick = btn.get('onclick', '')
            self.assertIn(expected_path, onclick, f"Button '{btn_id}' should navigate to '{expected_path}'")
    def test_dashboard_room_list(self):
        # Test Task 3: Check room-list div and that it contains a list of rooms with device counts
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        room_list_div = soup.find(id='room-list')
        self.assertIsNotNone(room_list_div, "Dashboard must have a div with id 'room-list'")
        # Check for <ul> inside room-list
        ul = room_list_div.find('ul')
        self.assertIsNotNone(ul, "'room-list' div must contain a <ul> element")
        # Check that at least one <li> exists (based on example data, john_doe has rooms)
        lis = ul.find_all('li')
        self.assertGreater(len(lis), 0, "'room-list' ul must contain at least one <li> element")
        # Check format of each li text: "<Room Name>: <count> device(s)"
        for li in lis:
            text = li.get_text(strip=True)
            self.assertRegex(text, r'^[\w\s]+: \d+ device(s)?$', f"Room list item '{text}' must match expected format")
if __name__ == '__main__':
    unittest.main()