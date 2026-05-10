'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist and have correct links.
Test the presence and correctness of key elements on the Dashboard page:
- ID: dashboard-page (Div container)
- ID: featured-restaurants (Div container with featured restaurants list)
- Buttons with IDs: browse-restaurants-button, view-cart-button, active-orders-button
'''
import unittest
from app import app
class FoodDeliveryDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the root URL '/' is accessible and returns 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for dashboard-page div container
        self.assertIn('id="dashboard-page"', html)
        # Check for featured-restaurants section
        self.assertIn('id="featured-restaurants"', html)
        # Check for navigation buttons with correct IDs and links
        self.assertIn('id="browse-restaurants-button"', html)
        self.assertIn('id="view-cart-button"', html)
        self.assertIn('id="active-orders-button"', html)
        # Check that buttons have correct href links (using url_for)
        self.assertIn('location.href=\'/restaurants\'', html)
        self.assertIn('location.href=\'/cart\'', html)
        self.assertIn('location.href=\'/orders\'', html)
    def test_featured_restaurants_listed(self):
        # Test that featured restaurants are listed (based on example data)
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Example featured restaurants from example data: Dragon House, La Bella Italia, Taj Mahal
        self.assertIn('Dragon House', html)
        self.assertIn('La Bella Italia', html)
        self.assertIn('Taj Mahal', html)
if __name__ == '__main__':
    unittest.main()