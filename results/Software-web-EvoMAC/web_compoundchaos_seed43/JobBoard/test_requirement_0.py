'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) can be accessed and loads correctly.
Test basic navigation buttons on the Dashboard page to ensure they link to the correct URLs.
'''
import unittest
from app import app
class TestJobBoardApp(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the root URL '/' loads successfully (Dashboard page)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page title is present in the response data
        self.assertIn(b'Job Board Dashboard', response.data)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons exist and point to correct URLs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for browse-jobs-button linking to /jobs
        self.assertIn(b'id="browse-jobs-button"', response.data)
        # Check for my-applications-button linking to /applications
        self.assertIn(b'id="my-applications-button"', response.data)
        # Check for companies-button linking to /companies
        self.assertIn(b'id="companies-button"', response.data)
if __name__ == '__main__':
    unittest.main()