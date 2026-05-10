'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if root URL '/' is accessible (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test if dashboard page contains expected elements and text
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title in HTML (should contain "Restaurant Dashboard")
        self.assertIn('Restaurant Dashboard', html)
        # Check welcome message element id
        self.assertIn('id="welcome-message"', html)
        # Check presence of navigation buttons by id
        self.assertIn('id="make-reservation-button"', html)
        self.assertIn('id="view-menu-button"', html)
        self.assertIn('id="back-to-dashboard"', html)
        self.assertIn('id="my-reservations-button"', html)
        self.assertIn('id="my-reviews-button"', html)
        self.assertIn('id="waitlist-button"', html)
        self.assertIn('id="profile-button"', html)
        # Check container div id
        self.assertIn('id="dashboard-page"', html)
if __name__ == '__main__':
    unittest.main()