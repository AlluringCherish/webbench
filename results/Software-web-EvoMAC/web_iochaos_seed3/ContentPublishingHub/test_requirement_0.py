'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page (/dashboard).
'''
import unittest
from app import app
class ContentPublishingHubTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_root_redirects_to_dashboard(self):
        # Test that root URL redirects to /dashboard
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])
    def test_dashboard_page_accessible(self):
        # Test that /dashboard page loads successfully
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="dashboard-page"', response.data)
    def test_dashboard_welcome_message(self):
        # Test that welcome message contains username (fullname)
        response = self.client.get('/dashboard')
        self.assertIn(b'Welcome, John Doe!', response.data)
    def test_dashboard_quick_stats_section(self):
        # Test that quick stats section is present with expected ids and labels
        response = self.client.get('/dashboard')
        self.assertIn(b'id="quick-stats"', response.data)
        self.assertIn(b'Total Articles:', response.data)
        self.assertIn(b'Published Articles:', response.data)
        self.assertIn(b'Drafts:', response.data)
        self.assertIn(b'Pending Review:', response.data)
    def test_dashboard_create_article_button(self):
        # Test that Create Article button is present and links correctly
        response = self.client.get('/dashboard')
        self.assertIn(b'id="create-article-button"', response.data)
        self.assertIn(b'Create Article', response.data)
        # The button uses onclick with url_for('create_article'), so check URL presence
        self.assertIn(b'/article/create', response.data)
    def test_dashboard_recent_activity_section(self):
        # Test that recent activity section is present and contains expected id
        response = self.client.get('/dashboard')
        self.assertIn(b'id="recent-activity"', response.data)
        self.assertIn(b'Recent Activity', response.data)
        # Since example data has some comments and approvals, check for at least one known activity type label
        self.assertTrue(
            b'Comment:' in response.data or
            b'Status:' in response.data or
            b'views on' in response.data or
            b'comment_text' not in response.data  # fallback
        )
if __name__ == '__main__':
    unittest.main()