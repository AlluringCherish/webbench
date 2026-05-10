'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains the required elements.
Test basic navigation buttons on the Dashboard page to ensure they link to the correct routes.
'''
import unittest
from main import app
class TestRestaurantReservation(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access root '/' and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test Task 2: Check that dashboard page contains required elements
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Restaurant Dashboard</title>', html)
        # Check welcome message id
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
    def test_dashboard_navigation_links(self):
        # Test Task 2: Check that navigation buttons link to correct routes
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Buttons should be present and have correct form or href attributes
        # Since buttons may use form or JS, check for presence of expected URLs in html
        self.assertIn('/make_reservation', html)
        self.assertIn('/menu', html)
        self.assertIn('/my_reservations', html)
        self.assertIn('/my_reviews', html)
        self.assertIn('/waitlist', html)
        self.assertIn('/profile', html)
if __name__ == '__main__':
    unittest.main()