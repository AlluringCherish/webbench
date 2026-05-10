'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains the required elements.
Test basic navigation buttons on the Dashboard page to ensure they link to the correct routes.
'''
import unittest
from main import app
class RestaurantReservationBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page title is correct
        self.assertIn(b'<title>Restaurant Dashboard</title>', response.data)
        # Check that welcome message container exists
        self.assertIn(b'id="welcome-message"', response.data)
        # Check presence of navigation buttons by their IDs
        nav_button_ids = [
            b'id="make-reservation-button"',
            b'id="view-menu-button"',
            b'id="back-to-dashboard"',
            b'id="my-reservations-button"',
            b'id="my-reviews-button"',
            b'id="waitlist-button"',
            b'id="profile-button"'
        ]
        for btn_id in nav_button_ids:
            self.assertIn(btn_id, response.data)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons on dashboard lead to correct pages
        # We test the GET requests for the URLs linked by buttons
        urls = [
            '/make_reservation',
            '/menu',
            '/back_to_dashboard',
            '/my_reservations',
            '/my_reviews',
            '/waitlist',
            '/profile'
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertIn(resp.status_code, [200, 302], f"URL {url} did not respond with 200 or 302")
if __name__ == '__main__':
    unittest.main()