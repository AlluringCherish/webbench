'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
'''
import unittest
from main import app
class RealEstateAppBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test GET request to root URL '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test that dashboard page contains key elements and buttons
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Real Estate Dashboard</title>', html)
        # Check container div id
        self.assertIn('id="dashboard-page"', html)
        # Check featured properties section
        self.assertIn('id="featured-properties"', html)
        # Check recent listings section
        self.assertIn('id="recent-listings"', html)
        # Check navigation buttons by id
        self.assertIn('id="browse-properties-button"', html)
        self.assertIn('id="my-inquiries-button"', html)
        self.assertIn('id="my-favorites-button"', html)
if __name__ == '__main__':
    unittest.main()