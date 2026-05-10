'''
Testing Task 1 and Task 2:
- Test whether the website can be accessed through local port 5000 (Flask default).
- Test whether the first page (Dashboard) loads correctly.
- Test basic navigation buttons on the Dashboard page:
  - Browse Songs button navigates to /songs
  - My Playlists button navigates to /playlists
  - Trending Artists button navigates to /artists
- Test presence of featured songs and trending artists sections with example data.
'''
import unittest
from main import app
class MusicStreamingBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test that dashboard page contains expected elements and example data
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Music Streaming Dashboard</title>', html)
        # Check presence of featured songs section
        self.assertIn('id="featured-songs"', html)
        self.assertIn('<h2>Featured Songs</h2>', html)
        # Check presence of trending artists section
        self.assertIn('id="trending-artists"', html)
        self.assertIn('<h2>Trending Artists</h2>', html)
        # Check presence of navigation buttons with correct IDs and labels
        self.assertIn('id="browse-songs-button"', html)
        self.assertIn('Browse Songs', html)
        self.assertIn('id="my-playlists-button"', html)
        self.assertIn('My Playlists', html)
        self.assertIn('id="trending-artists-button"', html)
        self.assertIn('Trending Artists', html)
        # Check that example featured songs from example data appear (e.g. "Bohemian Rhapsody")
        self.assertIn('Bohemian Rhapsody', html)
        self.assertIn('Queen', html)
        # Check that example trending artists from example data appear (e.g. "Queen", "The Weeknd", "Ed Sheeran")
        self.assertIn('Queen', html)
        self.assertIn('The Weeknd', html)
        self.assertIn('Ed Sheeran', html)
    def test_navigation_buttons(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check Browse Songs button link
        self.assertIn("onclick=\"location.href='/songs'\"", html)
        # Check My Playlists button link
        self.assertIn("onclick=\"location.href='/playlists'\"", html)
        # Check Trending Artists button link
        self.assertIn("onclick=\"location.href='/artists'\"", html)
if __name__ == '__main__':
    unittest.main()