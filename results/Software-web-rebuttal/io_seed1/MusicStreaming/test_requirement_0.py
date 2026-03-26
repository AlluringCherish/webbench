'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from main import app
class MusicStreamingBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Music Streaming Dashboard', response.data)
    def test_dashboard_elements(self):
        # Test presence of key elements on dashboard page
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check container div id
        self.assertIn('id="dashboard-page"', html)
        # Check featured songs section
        self.assertIn('id="featured-songs"', html)
        self.assertIn('<h2>Featured Songs</h2>', html)
        # Check trending artists section
        self.assertIn('id="trending-artists"', html)
        self.assertIn('<h2>Trending Artists</h2>', html)
        # Check navigation buttons with correct ids
        self.assertIn('id="browse-songs-button"', html)
        self.assertIn('id="my-playlists-button"', html)
        self.assertIn('id="trending-artists-button"', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct pages
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Browse Songs button link
        self.assertIn("location.href='/songs'", html)
        # My Playlists button link
        self.assertIn("location.href='/playlists'", html)
        # Trending Artists button link
        self.assertIn("location.href='/artists'", html)
if __name__ == '__main__':
    unittest.main()