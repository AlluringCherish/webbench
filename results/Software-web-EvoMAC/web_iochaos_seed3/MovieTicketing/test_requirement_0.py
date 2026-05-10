'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
'''
import unittest
from main import app
class TestMovieTicketingDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test that the dashboard page contains expected elements
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Movie Ticketing Dashboard</title>', html)
        # Check dashboard page container
        self.assertIn('id="dashboard-page"', html)
        # Check featured movies section
        self.assertIn('id="featured-movies"', html)
        # Check upcoming releases section
        self.assertIn('id="upcoming-releases"', html)
        # Check navigation buttons by id
        self.assertIn('id="browse-movies-button"', html)
        self.assertIn('id="view-bookings-button"', html)
        self.assertIn('id="showtimes-button"', html)
    def test_navigation_buttons_functionality(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Browse Movies button should link to /catalog
        self.assertIn('onclick="location.href=\'/catalog\'"', html)
        # View Bookings button should link to /bookings
        self.assertIn('onclick="location.href=\'/bookings\'"', html)
        # Showtimes button should link to /showtimes/<movie_id> (movie_id=1 or featured movie)
        # We check for pattern /showtimes/ in the button onclick
        self.assertIn('onclick="location.href=\'/showtimes/', html)
if __name__ == '__main__':
    unittest.main()