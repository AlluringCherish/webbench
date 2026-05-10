'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence and correctness of:
- Page container (id: dashboard-page)
- Welcome message with username (id: welcome-message)
- Quick stats section (id: quick-stats)
- Create Article button (id: create-article-button)
- Recent activity feed (id: recent-activity)
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class ContentPublishingHubDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_server_running_and_dashboard_accessible(self):
        # Test if the root redirects to /dashboard and /dashboard loads successfully
        response_root = self.client.get('/')
        self.assertEqual(response_root.status_code, 302)
        self.assertIn('/dashboard', response_root.location)
        response_dashboard = self.client.get('/dashboard')
        self.assertEqual(response_dashboard.status_code, 200)
        self.assertIn(b'ContentPublishingHub Dashboard', response_dashboard.data)
    def test_dashboard_page_elements(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page container
        page_container = soup.find(id='dashboard-page')
        self.assertIsNotNone(page_container, "Dashboard page container with id 'dashboard-page' not found")
        # Check welcome message
        welcome_message = soup.find(id='welcome-message')
        self.assertIsNotNone(welcome_message, "Welcome message with id 'welcome-message' not found")
        self.assertIn('Welcome,', welcome_message.text)
        # Check quick stats section
        quick_stats = soup.find(id='quick-stats')
        self.assertIsNotNone(quick_stats, "Quick stats section with id 'quick-stats' not found")
        # Check that it contains the expected stats labels
        stats_text = quick_stats.get_text()
        self.assertIn('Total Articles', stats_text)
        self.assertIn('Published Articles', stats_text)
        self.assertIn('Drafts', stats_text)
        self.assertIn('Pending Review', stats_text)
        # Check Create Article button
        create_article_button = soup.find(id='create-article-button')
        self.assertIsNotNone(create_article_button, "Create Article button with id 'create-article-button' not found")
        self.assertEqual(create_article_button.name, 'a')
        self.assertIn('/article/create', create_article_button['href'])
        # Check recent activity feed
        recent_activity = soup.find(id='recent-activity')
        self.assertIsNotNone(recent_activity, "Recent activity feed with id 'recent-activity' not found")
        # It should contain either a list or a message "No recent activity."
        ul = recent_activity.find('ul')
        p = recent_activity.find('p')
        self.assertTrue(ul is not None or (p is not None and 'No recent activity' in p.text))
if __name__ == '__main__':
    unittest.main()