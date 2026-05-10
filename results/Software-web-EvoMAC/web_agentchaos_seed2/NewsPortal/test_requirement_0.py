'''
Testing Task 1, 2, and 3:
- Test whether the website can be accessed through local port 5000 (Dashboard page).
- Test whether the first page (Dashboard) loads correctly with featured articles, trending articles, and navigation buttons.
- Test basic navigation from Dashboard to Article Catalog, Bookmarks, and Trending pages.
- Test presence and correctness of key elements on Dashboard page:
  - Div with id "dashboard-page"
  - Section with id "featured-articles" containing featured articles
  - Section with id "trending-articles" containing trending articles
  - Buttons with ids "browse-articles-button", "view-bookmarks-button", "trending-articles-button"
'''
import unittest
from main import app
class NewsPortalDashboardTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_contains_required_elements(self):
        # Test that dashboard page contains required elements by checking HTML content
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for dashboard-page div
        self.assertIn('id="dashboard-page"', html)
        # Check for featured-articles section
        self.assertIn('id="featured-articles"', html)
        self.assertIn('<h2>Featured Articles</h2>', html)
        # Check for trending-articles section
        self.assertIn('id="trending-articles"', html)
        self.assertIn('<h2>Trending News</h2>', html)
        # Check for navigation buttons with correct ids
        self.assertIn('id="browse-articles-button"', html)
        self.assertIn('id="view-bookmarks-button"', html)
        self.assertIn('id="trending-articles-button"', html)
    def test_dashboard_featured_articles_links(self):
        # Test that featured articles have links to article details page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # The example data has article_id=1,2,3; check that links to /article/1 etc exist
        self.assertIn('/article/1', html)
        self.assertIn('/article/2', html)
        self.assertIn('/article/3', html)
    def test_navigation_buttons_redirect(self):
        # Test that navigation buttons on dashboard redirect to correct pages
        # Since buttons use onclick with location.href, simulate GET requests to those pages
        # Article Catalog page
        response = self.client.get('/articles')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="catalog-page"', response.get_data(as_text=True))
        # Bookmarks page
        response = self.client.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="bookmarks-page"', response.get_data(as_text=True))
        # Trending Articles page
        response = self.client.get('/trending')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="trending-page"', response.get_data(as_text=True))
if __name__ == '__main__':
    unittest.main()