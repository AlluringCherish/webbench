'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test that the page title is correct
        response = self.client.get('/')
        self.assertIn(b'<title>Smart Home Dashboard</title>', response.data)
    def test_dashboard_page_elements(self):
        # Test presence of main container div with id 'dashboard-page'
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="dashboard-page"', html)
        # Test presence of device summary div with id 'device-summary'
        self.assertIn('id="device-summary"', html)
        # Test presence of device counts spans with correct ids
        self.assertIn('id="total-devices"', html)
        self.assertIn('id="active-devices"', html)
        self.assertIn('id="offline-devices"', html)
        # Test presence of all navigation buttons with correct ids
        self.assertIn('id="device-list-button"', html)
        self.assertIn('id="add-device-button"', html)
        self.assertIn('id="automation-button"', html)
        self.assertIn('id="energy-button"', html)
        self.assertIn('id="activity-button"', html)
        # Test presence of room list div with id 'room-list'
        self.assertIn('id="room-list"', html)
    def test_dashboard_buttons_navigation(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check that device list button links to /devices
        self.assertIn("location.href='/devices'", html)
        # Check that add device button links to /devices/add
        self.assertIn("location.href='/devices/add'", html)
        # Check that automation rules button links to /automation
        self.assertIn("location.href='/automation'", html)
        # Check that energy report button links to /energy
        self.assertIn("location.href='/energy'", html)
        # Check that activity logs button links to /activity
        self.assertIn("location.href='/activity'", html)
if __name__ == '__main__':
    unittest.main()