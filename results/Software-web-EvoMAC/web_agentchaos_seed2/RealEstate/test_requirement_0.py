'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class RealEstateDashboardTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Task 1: Test if the dashboard page is accessible (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Task 2 & 3: Test if the page title is correct in the HTML content
        response = self.client.get('/')
        self.assertIn(b'<title>Real Estate Dashboard</title>', response.data, "Dashboard page title should be 'Real Estate Dashboard'")
    def test_dashboard_elements_presence(self):
        # Task 3: Test presence of required elements by their IDs in the dashboard page HTML
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check container div
        self.assertIn('id="dashboard-page"', html, "Dashboard container div with id 'dashboard-page' should be present")
        # Check featured properties container
        self.assertIn('id="featured-properties"', html, "Featured properties div with id 'featured-properties' should be present")
        # Check buttons for navigation
        self.assertIn('id="browse-properties-button"', html, "Button with id 'browse-properties-button' should be present")
        self.assertIn('id="my-inquiries-button"', html, "Button with id 'my-inquiries-button' should be present")
        self.assertIn('id="my-favorites-button"', html, "Button with id 'my-favorites-button' should be present")
    def test_dashboard_navigation_buttons_functionality(self):
        # Task 2: Test that navigation buttons link to correct pages (by checking href or form action)
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Since buttons might be <button> with JS or <a> tags, check for URLs in the page
        self.assertIn('/search', html, "Dashboard page should have navigation to property search page (/search)")
        self.assertIn('/my_inquiries', html, "Dashboard page should have navigation to inquiries page (/my_inquiries)")
        self.assertIn('/my_favorites', html, "Dashboard page should have navigation to favorites page (/my_favorites)")
if __name__ == '__main__':
    unittest.main()