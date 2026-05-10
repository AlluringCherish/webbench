'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of:
- ID: dashboard-page (Div container)
- ID: featured-restaurants (Div container)
- ID: browse-restaurants-button (Button)
- ID: view-cart-button (Button)
- ID: active-orders-button (Button)
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class FoodDeliveryAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at root URL '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements with correct IDs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check for dashboard-page div
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "dashboard-page div not found")
        # Check for featured-restaurants div
        featured_div = soup.find(id='featured-restaurants')
        self.assertIsNotNone(featured_div, "featured-restaurants div not found")
        # Check for browse-restaurants-button button
        browse_button = soup.find(id='browse-restaurants-button')
        self.assertIsNotNone(browse_button, "browse-restaurants-button not found")
        self.assertEqual(browse_button.name, 'button')
        # Check for view-cart-button button
        cart_button = soup.find(id='view-cart-button')
        self.assertIsNotNone(cart_button, "view-cart-button not found")
        self.assertEqual(cart_button.name, 'button')
        # Check for active-orders-button button
        active_orders_button = soup.find(id='active-orders-button')
        self.assertIsNotNone(active_orders_button, "active-orders-button not found")
        self.assertEqual(active_orders_button.name, 'button')
    def test_basic_navigation_from_dashboard(self):
        # Test navigation buttons on dashboard lead to correct pages (status code 200)
        # browse-restaurants-button -> /restaurants
        response = self.client.get('/restaurants')
        self.assertEqual(response.status_code, 200)
        # view-cart-button -> /cart
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        # active-orders-button -> /orders
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()