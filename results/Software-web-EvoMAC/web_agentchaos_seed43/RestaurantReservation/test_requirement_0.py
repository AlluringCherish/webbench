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
        # Test Task 1: Access root '/' and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check that the Dashboard page contains required elements by their IDs and content
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Restaurant Dashboard</title>', html, "Page title should be 'Restaurant Dashboard'")
        # Check container div with id 'dashboard-page'
        self.assertIn('id="dashboard-page"', html, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check welcome message h1 with id 'welcome-message' and username displayed
        self.assertIn('id="welcome-message"', html, "Welcome message h1 with id 'welcome-message' should be present")
        self.assertIn('john_diner', html, "Username 'john_diner' should be displayed in welcome message")
        # Check presence of all navigation buttons by their IDs
        button_ids = [
            'make-reservation-button',
            'view-menu-button',
            'back-to-dashboard',
            'my-reservations-button',
            'my-reviews-button',
            'waitlist-button',
            'profile-button'
        ]
        for btn_id in button_ids:
            self.assertIn(f'id="{btn_id}"', html, f"Button with id '{btn_id}' should be present on Dashboard page")
if __name__ == '__main__':
    unittest.main()