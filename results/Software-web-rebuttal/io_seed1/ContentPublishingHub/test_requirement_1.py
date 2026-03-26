'''
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
'''
import unittest
from main import app
class ContentPublishingHubBasicNavigationTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_index_redirects_to_dashboard(self):
        # Access root URL and check redirect to /dashboard
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])
    def test_dashboard_page_loads(self):
        # Access /dashboard and check page loads with expected content
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check for presence of welcome message with username 'john'
        self.assertIn('Welcome, john!', html)
        # Check for quick stats section
        self.assertIn('Quick Stats', html)
        # Check for Create Article button
        self.assertIn('id="create-article-button"', html)
        # Check for Recent Activity section
        self.assertIn('Recent Activity', html)
    def test_create_article_navigation_link(self):
        # From dashboard page, check that Create Article button links to /article/create
        response = self.client.get('/dashboard')
        html = response.get_data(as_text=True)
        self.assertIn('href="/article/create"', html)
    def test_create_article_page_loads(self):
        # Access /article/create page and check it loads
        response = self.client.get('/article/create')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Create Article', html)  # Title or button text presence
    def test_my_articles_page_loads(self):
        # Access /articles/mine page and check it loads
        response = self.client.get('/articles/mine')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Articles', html)  # Basic check for articles listing
    def test_published_articles_page_loads(self):
        # Access /articles/published page and check it loads
        response = self.client.get('/articles/published')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Articles', html)  # Basic check for published articles listing
if __name__ == '__main__':
    unittest.main()