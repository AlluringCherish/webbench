'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page (/dashboard) including:
- Page container (id: dashboard-page)
- Welcome message with username (id: welcome-message)
- Quick stats section (id: quick-stats) with all expected statuses
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
    def test_index_redirects_to_dashboard(self):
        # Test that '/' redirects to '/dashboard'
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])
    def test_dashboard_page_loads(self):
        # Test that /dashboard loads successfully
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        # Check content type
        self.assertIn('text/html', response.content_type)
    def test_dashboard_page_elements(self):
        # Test presence of required elements on dashboard page
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check page container
        container = soup.find(id='dashboard-page')
        self.assertIsNotNone(container, "Dashboard page container not found")
        # Check welcome message with username
        welcome = soup.find(id='welcome-message')
        self.assertIsNotNone(welcome, "Welcome message element not found")
        self.assertIn('Welcome', welcome.text)
        # Check quick stats section and all statuses
        quick_stats = soup.find(id='quick-stats')
        self.assertIsNotNone(quick_stats, "Quick stats section not found")
        expected_statuses = ['Draft', 'Pending Review', 'Under Review', 'Approved', 'Published', 'Rejected', 'Archived']
        for status in expected_statuses:
            found = any(status in div.text for div in quick_stats.find_all('div'))
            self.assertTrue(found, f"Status '{status}' not found in quick stats")
        # Check Create Article button
        create_button = soup.find(id='create-article-button')
        self.assertIsNotNone(create_button, "Create Article button not found")
        self.assertEqual(create_button.name, 'button')
        self.assertIn('Create Article', create_button.text)
        # Check Recent activity feed
        recent_activity = soup.find(id='recent-activity')
        self.assertIsNotNone(recent_activity, "Recent activity feed not found")
        # Should have a heading Recent Activity
        heading = recent_activity.find('h3')
        self.assertIsNotNone(heading)
        self.assertIn('Recent Activity', heading.text)
        # Check that recent activity items have expected classes and structure if any
        activity_items = recent_activity.find_all(class_='activity-item')
        # It's acceptable if no recent activity, but if present check structure
        for item in activity_items:
            # Should contain either comment or approval type span
            comment_span = item.find(class_='activity-type-comment')
            approval_span = item.find(class_='activity-type-approval')
            self.assertTrue(comment_span or approval_span, "Activity item missing type span")
            # Should contain a timestamp span
            timestamp_span = item.find(class_='timestamp')
            self.assertIsNotNone(timestamp_span, "Activity item missing timestamp")
    def test_create_article_button_navigation(self):
        # Test that clicking Create Article button leads to /article/create page
        response = self.client.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        create_button = soup.find(id='create-article-button')
        self.assertIsNotNone(create_button)
        # The button uses onclick with location.href, extract URL
        onclick = create_button.get('onclick', '')
        self.assertIn('/article/create', onclick)
        # Test GET /article/create loads
        response_create = self.client.get('/article/create')
        self.assertEqual(response_create.status_code, 200)
        self.assertIn(b'Create New Article', response_create.data)
if __name__ == '__main__':
    unittest.main()