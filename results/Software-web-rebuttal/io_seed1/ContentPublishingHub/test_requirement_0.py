'''
Test whether the website can be accessed through local port 5000.
Specifically, test that the first page ("/") redirects to the dashboard page ("/dashboard")
and that the dashboard page loads successfully with status code 200.
'''
import unittest
from main import app
class TestWebsiteAccess(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_root_redirects_to_dashboard(self):
        # Access the root URL and check for redirect to /dashboard
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])
    def test_dashboard_accessible(self):
        # Access the dashboard page and check for status code 200
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        # Check that the response contains expected content (e.g. welcome message)
        self.assertIn(b'ContentPublishingHub Dashboard', response.data)
        self.assertIn(b'Welcome, john!', response.data)
if __name__ == '__main__':
    unittest.main()