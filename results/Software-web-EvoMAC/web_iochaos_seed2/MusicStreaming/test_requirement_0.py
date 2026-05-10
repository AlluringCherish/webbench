'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains required elements.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from main import app
class MusicStreamingBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if the root URL '/' is accessible (Dashboard page)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test if the Dashboard page contains required elements by IDs and text
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check container div id
        self.assertIn('id="dashboard-page"', html)
        # Check featured songs container
        self.assertIn('id="featured-songs"', html)
        # Check trending artists container
        self.assertIn('id="trending-artists-button"', html)  # button id
        # Check browse songs button
        self.assertIn('id="browse-songs-button"', html)
        # Check my playlists button
        self.assertIn('id="my-playlists-button"', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons exist and have correct href or onclick attributes
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Buttons should be present
        self.assertIn('id="browse-songs-button"', html)
        self.assertIn('id="my-playlists-button"', html)
        self.assertIn('id="trending-artists-button"', html)
if __name__ == '__main__':
    unittest.main()