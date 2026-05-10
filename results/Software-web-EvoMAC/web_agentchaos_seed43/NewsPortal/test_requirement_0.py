'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured articles, trending articles, and navigation buttons.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class NewsPortalTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check the dashboard page content and elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured articles div with id 'featured-articles'
        featured_div = soup.find('div', id='featured-articles')
        self.assertIsNotNone(featured_div, "Featured articles div with id 'featured-articles' should be present")
        # There should be at least one featured article displayed (based on example data)
        featured_articles = featured_div.find_all(class_='featured-article')
        self.assertGreaterEqual(len(featured_articles), 1, "At least one featured article should be displayed")
        # Check trending articles button with id 'trending-articles-button'
        trending_btn = soup.find('button', id='trending-articles-button')
        self.assertIsNotNone(trending_btn, "Trending articles button with id 'trending-articles-button' should be present")
        # Check browse articles button with id 'browse-articles-button'
        browse_btn = soup.find('button', id='browse-articles-button')
        self.assertIsNotNone(browse_btn, "Browse articles button with id 'browse-articles-button' should be present")
        # Check view bookmarks button with id 'view-bookmarks-button'
        bookmarks_btn = soup.find('button', id='view-bookmarks-button')
        self.assertIsNotNone(bookmarks_btn, "View bookmarks button with id 'view-bookmarks-button' should be present")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons on dashboard redirect correctly (simulate clicks by requesting URLs)
        # Browse Articles button should lead to /catalog
        response = self.client.get('/catalog')
        self.assertEqual(response.status_code, 200, "Article Catalog page should be accessible at /catalog")
        # Bookmarks button should lead to /bookmarks
        response = self.client.get('/bookmarks')
        self.assertEqual(response.status_code, 200, "Bookmarks page should be accessible at /bookmarks")
        # Trending Articles button should lead to /trending
        response = self.client.get('/trending')
        self.assertEqual(response.status_code, 200, "Trending Articles page should be accessible at /trending")
if __name__ == '__main__':
    unittest.main()