'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from main import app
class MovieTicketingBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Ticketing Dashboard', response.data)
    def test_dashboard_featured_movies_section(self):
        # Check that featured movies section exists in the dashboard page
        response = self.client.get('/')
        self.assertIn(b'id="featured-movies"', response.data)
        self.assertIn(b'Featured Movies', response.data)
    def test_dashboard_upcoming_releases_section(self):
        # Check that upcoming releases section exists in the dashboard page
        response = self.client.get('/')
        self.assertIn(b'id="upcoming-releases"', response.data)
        self.assertIn(b'Upcoming Releases', response.data)
    def test_dashboard_navigation_buttons(self):
        # Check presence and functionality of navigation buttons on dashboard
        response = self.client.get('/')
        self.assertIn(b'id="browse-movies-button"', response.data)
        self.assertIn(b'id="view-bookings-button"', response.data)
        self.assertIn(b'id="showtimes-button"', response.data)
        # Test navigation to movie catalog via button route
        response = self.client.get('/navigate_to_catalog', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Catalog', response.data)
        # Test navigation to booking history via button route
        response = self.client.get('/navigate_to_bookings', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Booking History', response.data)
        # Test navigation to showtimes via button route (redirects to movie catalog)
        response = self.client.get('/navigate_to_showtimes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Catalog', response.data)
    def test_back_to_dashboard_route(self):
        # Test that back_to_dashboard route redirects to dashboard page
        response = self.client.get('/back_to_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Ticketing Dashboard', response.data)
if __name__ == '__main__':
    unittest.main()