'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page of the website.
'''
import unittest
from main import app
class VirtualMuseumTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if the dashboard page is accessible via GET request to '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test if the dashboard page contains required elements and correct data
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Museum Dashboard</title>', html)
        # Check container div id
        self.assertIn('id="dashboard-page"', html)
        # Check exhibition summary div and its content placeholders
        self.assertIn('id="exhibition-summary"', html)
        self.assertIn('Total Exhibitions:', html)
        self.assertIn('Active Exhibitions:', html)
        # Check presence of navigation buttons with correct ids and labels
        self.assertIn('id="artifact-catalog-button"', html)
        self.assertIn('Artifact Catalog', html)
        self.assertIn('id="exhibitions-button"', html)
        self.assertIn('Exhibitions', html)
        self.assertIn('id="visitor-tickets-button"', html)
        self.assertIn('Visitor Tickets', html)
        self.assertIn('id="virtual-events-button"', html)
        self.assertIn('Virtual Events', html)
        self.assertIn('id="audio-guides-button"', html)
        self.assertIn('Audio Guides', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct routes
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check that buttons have correct onclick URLs
        self.assertIn("onclick=\"location.href='/artifact_catalog'\"", html)
        self.assertIn("onclick=\"location.href='/exhibitions'\"", html)
        self.assertIn("onclick=\"location.href='/visitor_tickets'\"", html)
        self.assertIn("onclick=\"location.href='/virtual_events'\"", html)
        self.assertIn("onclick=\"location.href='/audio_guides'\"", html)
if __name__ == '__main__':
    unittest.main()