'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
'''
import unittest
from main import create_app
class TestJobBoardInitialPage(unittest.TestCase):
    def setUp(self):
        # Create test client for the Flask app
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page title is correct in the HTML
        self.assertIn(b'Job Board Dashboard', response.data)
        self.assertIn(b'id="dashboard-page"', response.data)
    def test_dashboard_featured_jobs_section(self):
        # Check that the featured jobs container is present
        response = self.client.get('/')
        self.assertIn(b'id="featured-jobs"', response.data)
        # Check that navigation buttons exist with correct IDs
        self.assertIn(b'id="browse-jobs-button"', response.data)
        self.assertIn(b'id="my-applications-button"', response.data)
        self.assertIn(b'id="companies-button"', response.data)
    def test_dashboard_navigation_buttons_redirect(self):
        # Test that clicking navigation buttons redirects to correct pages
        # Since we cannot click buttons in unittest, test the routes they redirect to
        # Browse Jobs button redirects to /listings/
        response = self.client.get('/browse-jobs', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/listings/', response.headers['Location'])
        # My Applications button redirects to /applications/
        response = self.client.get('/my-applications', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/applications/', response.headers['Location'])
        # Companies button redirects to /companies/
        response = self.client.get('/companies', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/companies/', response.headers['Location'])
if __name__ == '__main__':
    unittest.main()