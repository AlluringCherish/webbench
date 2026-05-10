'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains expected elements.
Test basic navigation buttons on the Dashboard page to ensure they link to correct URLs.
'''
import unittest
from main import app
class EventPlanningAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test that the dashboard page contains key elements and text
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Event Planning Dashboard</title>', html)
        # Check dashboard page container div
        self.assertIn('id="dashboard-page"', html)
        # Check featured events section
        self.assertIn('id="featured-events"', html)
        # Check featured venues section
        self.assertIn('id="featured-venues"', html)
        # Check navigation buttons by id and their href targets
        self.assertIn('id="browse-events-button"', html)
        self.assertIn('id="view-tickets-button"', html)
        self.assertIn('id="venues-button"', html)
        # Check that buttons have correct onclick URLs
        self.assertIn("location.href='/events'", html)
        self.assertIn("location.href='/bookings'", html)
        self.assertIn("location.href='/venues'", html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons lead to correct pages by requesting those URLs
        # Browse Events button leads to /events
        response_events = self.client.get('/events')
        self.assertEqual(response_events.status_code, 200)
        self.assertIn('id="events-page"', response_events.get_data(as_text=True) or '')
        # View Tickets button leads to /bookings
        response_bookings = self.client.get('/bookings')
        self.assertEqual(response_bookings.status_code, 200)
        self.assertIn('id="bookings-page"', response_bookings.get_data(as_text=True) or '')
        # Venues button leads to /venues
        response_venues = self.client.get('/venues')
        self.assertEqual(response_venues.status_code, 200)
        self.assertIn('id="venues-page"', response_venues.get_data(as_text=True) or '')
if __name__ == '__main__':
    unittest.main()