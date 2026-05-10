'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) can be accessed and loads correctly.
Test basic navigation buttons on the Dashboard page to ensure they link to the correct pages.
'''
import unittest
from main import app
class MusicStreamingAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Music Streaming Dashboard', response.data)
    def test_root_redirects_to_dashboard(self):
        # Test that root URL '/' loads the dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Music Streaming Dashboard', response.data)
    def test_dashboard_elements(self):
        # Test presence of key elements on dashboard page
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        # Check container div
        self.assertIn('id="dashboard-page"', html)
        # Check featured songs div
        self.assertIn('id="featured-songs"', html)
        # Check navigation buttons by id
        self.assertIn('id="browse-songs-button"', html)
        self.assertIn('id="my-playlists-button"', html)
        self.assertIn('id="trending-artists-button"', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct pages
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        # Check that browse songs button links to /songs
        self.assertIn('id="browse-songs-button"', html)
        self.assertIn('/songs', html)
        # Check that my playlists button links to /playlists
        self.assertIn('id="my-playlists-button"', html)
        self.assertIn('/playlists', html)
        # Check that trending artists button links to /artists
        self.assertIn('id="trending-artists-button"', html)
        self.assertIn('/artists', html)
if __name__ == '__main__':
    unittest.main()