'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and contains the main elements.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from app import app
class FoodDeliveryAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_content(self):
        # Test that the dashboard page contains key elements as per requirements
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for dashboard page container div
        self.assertIn('id="dashboard-page"', html)
        # Check for featured restaurants section
        self.assertIn('id="featured-restaurants"', html)
        # Check for popular cuisines section
        self.assertIn('Popular Cuisines', html)
        # Check for navigation buttons with correct IDs
        self.assertIn('id="browse-restaurants-button"', html)
        self.assertIn('id="view-cart-button"', html)
        self.assertIn('id="active-orders-button"', html)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct pages
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # The buttons use onclick with location.href, check URLs
        self.assertIn("location.href='/restaurants'", html)
        self.assertIn("location.href='/cart'", html)
        self.assertIn("location.href='/active_orders'", html)
if __name__ == '__main__':
    unittest.main()