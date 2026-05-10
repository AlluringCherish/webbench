'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, including presence of featured properties, recent listings, and navigation buttons.
'''
import unittest
from main import app
class RealEstateAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_content(self):
        # Test that the dashboard page contains required elements and example data
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Real Estate Dashboard</title>', html)
        # Check dashboard container div
        self.assertIn('id="dashboard-page"', html)
        # Check featured properties section and at least one featured property from example data
        self.assertIn('id="featured-properties"', html)
        self.assertIn('123 Oak Street', html)  # From example data property 1
        self.assertIn('456 Park Avenue', html)  # From example data property 2
        # Check recent listings section and at least one recent listing from example data
        self.assertIn('id="recent-listings"', html)
        self.assertIn('789 Elm Road', html)  # From example data property 3
        # Check navigation buttons with correct IDs and links
        self.assertIn('id="browse-properties-button"', html)
        self.assertIn('id="my-inquiries-button"', html)
        self.assertIn('id="my-favorites-button"', html)
        # Check navigation buttons link to correct routes
        self.assertIn('href="/property_search"', html)
        self.assertIn('href="/my_inquiries"', html)
        self.assertIn('href="/my_favorites"', html)
    def test_basic_navigation_from_dashboard(self):
        # Test navigation buttons redirect correctly
        # Browse Properties button leads to property_search page
        response = self.client.get('/property_search')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Property Search</title>', response.get_data(as_text=True))
        # My Inquiries page accessible
        response = self.client.get('/my_inquiries')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>My Inquiries</title>', response.get_data(as_text=True))
        # My Favorites page accessible
        response = self.client.get('/my_favorites')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>My Favorite Properties</title>', response.get_data(as_text=True))
if __name__ == '__main__':
    unittest.main()