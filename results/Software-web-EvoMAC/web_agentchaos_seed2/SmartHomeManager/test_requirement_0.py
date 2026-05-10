'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Test the presence and correctness of all specified elements on the Dashboard page as per the requirements.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains all required elements with correct IDs and content
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page container div with id dashboard-page
        self.assertIn('id="dashboard-page"', html)
        # Check page title in h1
        self.assertIn('<h1>Smart Home Dashboard</h1>', html)
        # Check device summary div and its children
        self.assertIn('id="device-summary"', html)
        self.assertIn('<h3>Total Devices</h3>', html)
        self.assertIn('<h3>Active Devices</h3>', html)
        self.assertIn('<h3>Offline Devices</h3>', html)
        # Check navigation buttons with correct IDs
        self.assertIn('id="device-list-button"', html)
        self.assertIn('id="add-device-button"', html)
        self.assertIn('id="automation-button"', html)
        self.assertIn('id="energy-button"', html)
        self.assertIn('id="activity-button"', html)
        # Check room list container
        self.assertIn('id="room-list"', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct routes
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check hrefs for buttons (using onclick location.href)
        self.assertIn("location.href='/devices'", html)
        self.assertIn("location.href='/devices/add'", html)
        self.assertIn("location.href='/automation'", html)
        self.assertIn("location.href='/energy'", html)
        self.assertIn("location.href='/activity'", html)
if __name__ == '__main__':
    unittest.main()