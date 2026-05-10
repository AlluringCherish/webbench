'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist and have correct links.
'''
import unittest
from app import app
class TestJobBoardDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at root '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test that the dashboard page contains correct title
        response = self.client.get('/')
        self.assertIn(b'<title>Job Board Dashboard</title>', response.data)
    def test_dashboard_featured_jobs_section(self):
        # Test that the featured jobs section exists with correct id
        response = self.client.get('/')
        self.assertIn(b'id="featured-jobs"', response.data)
        self.assertIn(b'<h2>Featured Jobs</h2>', response.data)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons exist with correct ids and hrefs
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="browse-jobs-button"', html)
        self.assertIn("location.href='/jobs'", html)
        self.assertIn('id="my-applications-button"', html)
        self.assertIn("location.href='/applications'", html)
        self.assertIn('id="companies-button"', html)
        self.assertIn("location.href='/companies'", html)
if __name__ == '__main__':
    unittest.main()