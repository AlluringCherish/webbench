'''
Test whether the website can be accessed through local port 5000.
Specifically, test that the Dashboard page ("/") loads successfully with HTTP 200 status code.
'''
import unittest
from app import app
class TestDashboardAccess(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_page_accessible(self):
        # Access the dashboard page
        response = self.client.get('/')
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Optionally check that some expected content is in the response data
        self.assertIn(b'Pet Adoption Dashboard', response.data)
if __name__ == '__main__':
    unittest.main()