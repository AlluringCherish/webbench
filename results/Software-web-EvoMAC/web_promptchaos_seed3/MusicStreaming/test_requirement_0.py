'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page by verifying the presence and correctness of the following elements:
- ID: dashboard-page (Div container)
- ID: featured-songs (Div container for featured songs)
- ID: browse-songs-button (Button to navigate to song catalog)
- ID: my-playlists-button (Button to navigate to playlists)
- ID: trending-artists-button (Button to navigate to trending artists)
Also test that clicking navigation buttons leads to the expected pages.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class MusicStreamingDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status 200")
    def test_dashboard_elements_presence(self):
        # Test that required elements exist in the dashboard page HTML
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured-songs div
        featured_songs_div = soup.find('div', id='featured-songs')
        self.assertIsNotNone(featured_songs_div, "Featured songs div with id 'featured-songs' should be present")
        # Check browse-songs-button button
        browse_songs_btn = soup.find('button', id='browse-songs-button')
        self.assertIsNotNone(browse_songs_btn, "Browse songs button with id 'browse-songs-button' should be present")
        # Check my-playlists-button button
        my_playlists_btn = soup.find('button', id='my-playlists-button')
        self.assertIsNotNone(my_playlists_btn, "My playlists button with id 'my-playlists-button' should be present")
        # Check trending-artists-button button
        trending_artists_btn = soup.find('button', id='trending-artists-button')
        self.assertIsNotNone(trending_artists_btn, "Trending artists button with id 'trending-artists-button' should be present")
    def test_navigation_buttons(self):
        # Test that navigation buttons redirect to expected pages
        # Since buttons use JS to redirect, we test the target pages directly
        # Browse songs page
        response_songs = self.client.get('/songs')
        self.assertEqual(response_songs.status_code, 200, "Song Catalog page should be accessible")
        # Playlists page
        response_playlists = self.client.get('/playlists')
        self.assertEqual(response_playlists.status_code, 200, "Playlists page should be accessible")
        # Trending artists redirect to dashboard (button redirects to '/')
        response_trending = self.client.get('/')
        self.assertEqual(response_trending.status_code, 200, "Trending artists redirect to dashboard page")
if __name__ == '__main__':
    unittest.main()