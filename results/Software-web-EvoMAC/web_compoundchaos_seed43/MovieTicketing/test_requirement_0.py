'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist and link correctly.
Testing Task 3: Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Task 1: Test access to root URL '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Task 2 & 3: Test presence of required elements in the dashboard page HTML
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Movie Ticketing Dashboard</title>', html, "Page title should be 'Movie Ticketing Dashboard'")
        # Check container div with id 'dashboard-page'
        self.assertIn('id="dashboard-page"', html, "Dashboard container div with id 'dashboard-page' should be present")
        # Check featured movies container div with id 'featured-movies'
        self.assertIn('id="featured-movies"', html, "Featured movies div with id 'featured-movies' should be present")
        # Check buttons with correct ids and that they link to correct routes
        # browse-movies-button -> /catalog
        self.assertIn('id="browse-movies-button"', html, "Button with id 'browse-movies-button' should be present")
        self.assertIn('/catalog', html, "Browse movies button should link to /catalog")
        # view-bookings-button -> /booking_history
        self.assertIn('id="view-bookings-button"', html, "Button with id 'view-bookings-button' should be present")
        self.assertIn('/booking_history', html, "View bookings button should link to /booking_history")
        # showtimes-button -> /showtimes/<movie_id> (since no movie_id here, check at least the button exists)
        self.assertIn('id="showtimes-button"', html, "Button with id 'showtimes-button' should be present")
    def test_dashboard_navigation_buttons_functionality(self):
        # Task 2: Test that navigation buttons lead to correct pages (simulate clicking by requesting URLs)
        # /catalog page
        response_catalog = self.client.get('/catalog')
        self.assertEqual(response_catalog.status_code, 200, "Catalog page should be accessible")
        # /booking_history page
        response_booking_history = self.client.get('/booking_history')
        self.assertEqual(response_booking_history.status_code, 200, "Booking history page should be accessible")
        # Since showtimes requires movie_id, test with a valid movie_id from example data: '1'
        response_showtimes = self.client.get('/showtimes/1')
        self.assertEqual(response_showtimes.status_code, 200, "Showtimes page for movie_id=1 should be accessible")
if __name__ == '__main__':
    unittest.main()