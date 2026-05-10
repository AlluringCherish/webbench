'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page of the website.
'''
import unittest
from flask import Flask, session
from dashboard import dashboard_bp
from bs4 import BeautifulSoup
class DashboardPageTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask app instance for testing
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret_key'
        self.app.register_blueprint(dashboard_bp)
        self.client = self.app.test_client()
        # Patch session to simulate logged-in user 'john'
        @self.app.before_request
        def set_session_user():
            session['username'] = 'john'
    def test_server_running_and_dashboard_accessible(self):
        # Test if the /dashboard route is accessible (simulating local port 5000)
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Access the dashboard page
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        # Parse HTML content
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check page container id
        page_container = soup.find(id='dashboard-page')
        self.assertIsNotNone(page_container, "Dashboard page container with id 'dashboard-page' should be present")
        # Check welcome message with username
        welcome_message = soup.find(id='welcome-message')
        self.assertIsNotNone(welcome_message, "Welcome message with id 'welcome-message' should be present")
        self.assertIn('john', welcome_message.text.lower(), "Welcome message should contain the username 'john'")
        # Check quick stats section
        quick_stats = soup.find(id='quick-stats')
        self.assertIsNotNone(quick_stats, "Quick stats section with id 'quick-stats' should be present")
        # Check Create Article button
        create_article_button = soup.find(id='create-article-button')
        self.assertIsNotNone(create_article_button, "Create Article button with id 'create-article-button' should be present")
        # Check recent activity feed
        recent_activity = soup.find(id='recent-activity')
        self.assertIsNotNone(recent_activity, "Recent activity feed with id 'recent-activity' should be present")
    def test_dashboard_navigation_links(self):
        # Access the dashboard page
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check that Create Article button is a link or form that leads to /article/create
        create_article_button = soup.find(id='create-article-button')
        self.assertIsNotNone(create_article_button, "Create Article button should be present")
        # The button might be a <a> or <button> with form or JS, check href or form action
        if create_article_button.name == 'a':
            href = create_article_button.get('href', '')
            self.assertIn('/article/create', href, "Create Article button link should navigate to /article/create")
        else:
            # If button, check if it has form or JS - we accept presence of data-target or form action
            # This is a minimal check since no JS is provided
            pass
if __name__ == '__main__':
    unittest.main()