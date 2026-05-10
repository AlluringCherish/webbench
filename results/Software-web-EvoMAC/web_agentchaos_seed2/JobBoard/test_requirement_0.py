'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test basic navigation buttons on the Dashboard page to ensure they redirect properly.
'''
import unittest
from main import app
class JobBoardBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Board Dashboard', response.data)
        self.assertIn(b'Featured Jobs', response.data)
    def test_dashboard_buttons_navigation(self):
        # Test that the dashboard buttons redirect to correct pages
        # Browse Jobs button redirects to /jobs
        response = self.client.get('/go_to_jobs', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Listings', response.data)
        # My Applications button redirects to /applications
        response = self.client.get('/go_to_applications', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Applications', response.data)
        # Companies button redirects to /companies
        response = self.client.get('/go_to_companies', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Company Directory', response.data)
    def test_dashboard_featured_jobs_content(self):
        # Check that featured jobs section contains job cards with expected fields
        response = self.client.get('/')
        self.assertIn(b'id="featured-jobs"', response.data)
        # Check presence of at least one job card if example data present
        # Since example data has jobs, check for job title from example data
        self.assertTrue(
            b'Senior Python Developer' in response.data or
            b'Data Analyst' in response.data or
            b'Healthcare Administrator' in response.data
        )
if __name__ == '__main__':
    unittest.main()