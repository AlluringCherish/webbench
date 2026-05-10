'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of the required elements:
- ID: dashboard-page (Div container)
- ID: featured-articles (Div container for featured articles)
- Buttons with IDs: browse-articles-button, view-bookmarks-button, trending-articles-button
- Presence of featured articles and trending articles with correct data display and links
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class NewsPortalDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements and data
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check dashboard-page div exists
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should exist")
        # Check featured-articles div exists
        featured_div = soup.find('div', id='featured-articles')
        self.assertIsNotNone(featured_div, "Featured articles div with id 'featured-articles' should exist")
        # Check buttons exist with correct IDs
        browse_btn = soup.find('button', id='browse-articles-button')
        self.assertIsNotNone(browse_btn, "Button with id 'browse-articles-button' should exist")
        bookmarks_btn = soup.find('button', id='view-bookmarks-button')
        self.assertIsNotNone(bookmarks_btn, "Button with id 'view-bookmarks-button' should exist")
        trending_btn = soup.find('button', id='trending-articles-button')
        self.assertIsNotNone(trending_btn, "Button with id 'trending-articles-button' should exist")
        # Check featured articles content: at least one featured article card with title, author, date, views, and link
        featured_articles = featured_div.find_all('div', class_='featured-article')
        self.assertGreaterEqual(len(featured_articles), 1, "There should be at least one featured article displayed")
        for article_div in featured_articles:
            # Title
            title_div = article_div.find('div', class_='article-title')
            self.assertIsNotNone(title_div, "Featured article should have a title div")
            self.assertTrue(len(title_div.text.strip()) > 0, "Featured article title should not be empty")
            # Meta info (author, date, views)
            meta_div = article_div.find('div', class_='article-meta')
            self.assertIsNotNone(meta_div, "Featured article should have meta info div")
            self.assertIn('By', meta_div.text, "Meta info should contain author info")
            self.assertIn('Views:', meta_div.text, "Meta info should contain views info")
            # Read More link
            read_more_link = article_div.find('a', class_='view-article-link')
            self.assertIsNotNone(read_more_link, "Featured article should have a 'Read More' link")
            href = read_more_link.get('href', '')
            self.assertTrue(href.startswith('/article/'), "Read More link href should start with '/article/'")
        # Check trending articles div and content
        trending_div = soup.find('div', id='trending-articles')
        self.assertIsNotNone(trending_div, "Trending articles div with id 'trending-articles' should exist")
        trending_articles = trending_div.find_all('div', class_='trending-article')
        # Trending articles may be empty if no data, but example data exists, so expect at least one
        self.assertGreaterEqual(len(trending_articles), 1, "There should be at least one trending article displayed")
        for idx, t_article_div in enumerate(trending_articles, start=1):
            # Rank span
            rank_span = t_article_div.find('span', class_='rank')
            self.assertIsNotNone(rank_span, "Trending article should have a rank span")
            self.assertIn(str(idx), rank_span.text, "Rank span should contain correct rank number")
            # Article title span
            title_span = t_article_div.find('span', class_='article-title')
            self.assertIsNotNone(title_span, "Trending article should have a title span")
            self.assertTrue(len(title_span.text.strip()) > 0, "Trending article title should not be empty")
            # Category span
            category_span = t_article_div.find('span', class_='category')
            self.assertIsNotNone(category_span, "Trending article should have a category span")
            self.assertTrue(len(category_span.text.strip()) > 0, "Trending article category should not be empty")
            # Views span
            views_span = t_article_div.find('span', class_='views')
            self.assertIsNotNone(views_span, "Trending article should have a views span")
            self.assertIn('views', views_span.text, "Views span should contain the word 'views'")
            # Read More link
            read_more_link = t_article_div.find('a', class_='view-article-link')
            self.assertIsNotNone(read_more_link, "Trending article should have a 'Read More' link")
            href = read_more_link.get('href', '')
            self.assertTrue(href.startswith('/article/'), "Trending article 'Read More' link href should start with '/article/'")
    def test_dashboard_navigation_buttons(self):
        # Test that the dashboard buttons navigate correctly via POST requests
        # Browse Articles button
        response = self.client.post('/go_to_catalog', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/catalog', response.headers['Location'])
        # View Bookmarks button
        response = self.client.post('/go_to_bookmarks', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/bookmarks', response.headers['Location'])
        # Trending Articles button
        response = self.client.post('/go_to_trending', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/trending', response.headers['Location'])
if __name__ == '__main__':
    unittest.main()