'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of the following elements:
- ID: dashboard-page (Div container)
- ID: featured-articles (Div container with featured articles)
- ID: browse-articles-button (Button to navigate to article catalog page)
- ID: view-bookmarks-button (Button to navigate to bookmarks page)
- ID: trending-articles-button (Button to navigate to trending articles page)
- ID: trending-articles (Div container with trending articles)
Also verify that featured articles and trending articles are displayed with correct titles and metadata.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestNewsPortalDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_contains_required_elements(self):
        # Test that dashboard page contains required elements by ID
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured-articles div
        featured_div = soup.find('div', id='featured-articles')
        self.assertIsNotNone(featured_div, "Featured articles div with id 'featured-articles' should be present")
        # Check buttons by id
        browse_btn = soup.find('button', id='browse-articles-button')
        self.assertIsNotNone(browse_btn, "Browse Articles button with id 'browse-articles-button' should be present")
        self.assertIn('Browse Articles', browse_btn.text)
        bookmarks_btn = soup.find('button', id='view-bookmarks-button')
        self.assertIsNotNone(bookmarks_btn, "View Bookmarks button with id 'view-bookmarks-button' should be present")
        self.assertIn('View Bookmarks', bookmarks_btn.text)
        trending_btn = soup.find('button', id='trending-articles-button')
        self.assertIsNotNone(trending_btn, "Trending Articles button with id 'trending-articles-button' should be present")
        self.assertIn('Trending Articles', trending_btn.text)
        # Check trending-articles div
        trending_div = soup.find('div', id='trending-articles')
        self.assertIsNotNone(trending_div, "Trending articles div with id 'trending-articles' should be present")
    def test_featured_articles_content(self):
        # Test that featured articles are displayed with title, author, date, and views
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_div = soup.find('div', id='featured-articles')
        self.assertIsNotNone(featured_div)
        article_cards = featured_div.find_all('div', class_='article-card')
        self.assertGreaterEqual(len(article_cards), 1, "There should be at least one featured article displayed")
        for card in article_cards:
            title = card.find('div', class_='article-title')
            self.assertIsNotNone(title, "Featured article should have a title element")
            self.assertTrue(title.text.strip(), "Featured article title should not be empty")
            meta = card.find('div', class_='article-meta')
            self.assertIsNotNone(meta, "Featured article should have meta information")
            self.assertRegex(meta.text, r'By .+ \| \d{4}-\d{2}-\d{2} \| Views: \d+', "Featured article meta should contain author, date, and views")
    def test_trending_articles_content(self):
        # Test that trending articles are displayed with rank, title, category, and view count
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        trending_div = soup.find('div', id='trending-articles')
        self.assertIsNotNone(trending_div)
        article_cards = trending_div.find_all('div', class_='article-card')
        self.assertGreaterEqual(len(article_cards), 0, "Trending articles section should be present (may be empty)")
        for card in article_cards:
            title = card.find('div', class_='article-title')
            self.assertIsNotNone(title, "Trending article should have a title element")
            self.assertTrue(title.text.strip(), "Trending article title should not be empty")
            # Title includes rank number and article title, e.g. "1. Breaking: New Technology Breakthrough"
            self.assertRegex(title.text.strip(), r'^\d+\.\s.+')
            meta = card.find('div', class_='article-meta')
            self.assertIsNotNone(meta, "Trending article should have meta information")
            self.assertRegex(meta.text, r'Category: .+ \| Views: \d+', "Trending article meta should contain category and views")
    def test_navigation_buttons_functionality(self):
        # Test that navigation buttons have correct hrefs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        browse_btn = soup.find('button', id='browse-articles-button')
        self.assertIsNotNone(browse_btn)
        self.assertIn("location.href", browse_btn.get('onclick', ''), "Browse Articles button should have onclick navigation")
        bookmarks_btn = soup.find('button', id='view-bookmarks-button')
        self.assertIsNotNone(bookmarks_btn)
        self.assertIn("location.href", bookmarks_btn.get('onclick', ''), "View Bookmarks button should have onclick navigation")
        trending_btn = soup.find('button', id='trending-articles-button')
        self.assertIsNotNone(trending_btn)
        self.assertIn("location.href", trending_btn.get('onclick', ''), "Trending Articles button should have onclick navigation")
if __name__ == '__main__':
    unittest.main()