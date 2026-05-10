'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from main import app
class NewsPortalBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page title is correct
        self.assertIn(b'<title>News Portal</title>', response.data)
        # Check that the dashboard container div is present
        self.assertIn(b'id="dashboard-page"', response.data)
    def test_dashboard_featured_articles_section(self):
        # Check that featured articles section exists
        response = self.client.get('/')
        self.assertIn(b'id="featured-articles"', response.data)
        self.assertIn(b'<h2>Featured Articles</h2>', response.data)
    def test_dashboard_trending_articles_section(self):
        # Check that trending articles section exists
        response = self.client.get('/')
        self.assertIn(b'id="trending-articles"', response.data)
        self.assertIn(b'<h2>Trending News</h2>', response.data)
    def test_dashboard_navigation_buttons(self):
        # Check presence and href of navigation buttons on dashboard
        response = self.client.get('/')
        # Buttons with correct IDs
        self.assertIn(b'id="browse-articles-button"', response.data)
        self.assertIn(b'id="view-bookmarks-button"', response.data)
        self.assertIn(b'id="trending-articles-button"', response.data)
        # Buttons should have onclick attributes with correct URLs
        self.assertIn(b"onclick=\"location.href='/articles'\"", response.data)
        self.assertIn(b"onclick=\"location.href='/bookmarks'\"", response.data)
        self.assertIn(b"onclick=\"location.href='/trending'\"", response.data)
if __name__ == '__main__':
    unittest.main()