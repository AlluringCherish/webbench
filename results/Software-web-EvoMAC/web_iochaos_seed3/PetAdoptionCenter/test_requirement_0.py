'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains expected elements.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from main import app
class TestPetAdoptionCenterDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (status 200)")
    def test_dashboard_content(self):
        # Test that the dashboard page contains key elements:
        # - Page title "Pet Adoption Dashboard"
        # - Featured pets section with id "featured-pets"
        # - Recent activities section with id "recent-activities"
        # - Buttons with ids "browse-pets-button" and "back-to-dashboard"
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertIn('<title>Pet Adoption Dashboard</title>', html, "Page title should be 'Pet Adoption Dashboard'")
        self.assertIn('id="featured-pets"', html, "Dashboard should contain featured pets section with id 'featured-pets'")
        self.assertIn('id="recent-activities"', html, "Dashboard should contain recent activities section with id 'recent-activities'")
        self.assertIn('id="browse-pets-button"', html, "Dashboard should have a button with id 'browse-pets-button'")
        self.assertIn('id="back-to-dashboard"', html, "Dashboard should have a button with id 'back-to-dashboard'")
    def test_navigation_buttons(self):
        # Test that the buttons have correct href or onclick attributes for navigation
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # The browse-pets-button should navigate to /pets
        self.assertIn("id=\"browse-pets-button\"", html)
        self.assertIn("location.href='", html)
        self.assertIn("/pets", html)
        # The back-to-dashboard button should refresh the page (reload)
        self.assertIn("id=\"back-to-dashboard\"", html)
        self.assertIn("location.reload()", html)
if __name__ == '__main__':
    unittest.main()