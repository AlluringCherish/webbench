'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class NewsPortalDashboardTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET request to '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test that the page title is "News Portal"
        response = self.client.get('/')
        self.assertIn(b'<title>News Portal</title>', response.data, "Dashboard page title should be 'News Portal'")
    def test_dashboard_elements_presence(self):
        # Test presence of main container div with id 'dashboard-page'
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="dashboard-page"', html, "Dashboard page should contain div with id 'dashboard-page'")
        # Test presence of featured articles section with id 'featured-articles'
        self.assertIn('id="featured-articles"', html, "Dashboard page should contain section with id 'featured-articles'")
        # Test presence of trending articles section with id 'trending-articles'
        self.assertIn('id="trending-articles"', html, "Dashboard page should contain section with id 'trending-articles'")
        # Test presence of navigation buttons with correct ids
        self.assertIn('id="browse-articles-button"', html, "Dashboard page should have button with id 'browse-articles-button'")
        self.assertIn('id="view-bookmarks-button"', html, "Dashboard page should have button with id 'view-bookmarks-button'")
        self.assertIn('id="trending-articles-button"', html, "Dashboard page should have button with id 'trending-articles-button'")
    def test_dashboard_navigation_buttons_functionality(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check that browse articles button links to /article_catalog
        self.assertIn("location.href='/article_catalog'", html, "Browse Articles button should navigate to /article_catalog")
        # Check that view bookmarks button links to /bookmarks
        self.assertIn("location.href='/bookmarks'", html, "View Bookmarks button should navigate to /bookmarks")
        # Check that trending articles button links to /trending_articles
        self.assertIn("location.href='/trending_articles'", html, "Trending Articles button should navigate to /trending_articles")
if __name__ == '__main__':
    unittest.main()