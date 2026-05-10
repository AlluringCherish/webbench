'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Test the presence of key elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the root URL '/' is accessible and returns 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test that the page title contains "Event Planning Dashboard"
        response = self.client.get('/')
        self.assertIn(b'Event Planning Dashboard', response.data)
    def test_dashboard_elements_presence(self):
        # Test presence of key elements by their IDs in the HTML response
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check container div for dashboard page
        self.assertIn('id="dashboard-page"', html)
        # Check featured events div
        self.assertIn('id="featured-events"', html)
        # Check navigation buttons by their IDs
        self.assertIn('id="browse-events-button"', html)
        self.assertIn('id="view-tickets-button"', html)
        self.assertIn('id="venues-button"', html)
    def test_navigation_buttons_functionality(self):
        # Check that navigation buttons link to correct pages (href or form action)
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Since buttons might be <button> with JS or <a> tags, check for expected URLs in HTML
        self.assertIn('/events', html)
        self.assertIn('/book-tickets', html)
        self.assertIn('/venues', html)
if __name__ == '__main__':
    unittest.main()