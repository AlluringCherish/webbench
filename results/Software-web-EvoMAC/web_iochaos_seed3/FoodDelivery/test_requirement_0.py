'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class FoodDeliveryBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test Task 2: Check page title in dashboard.html
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        self.assertEqual(title, "Food Delivery Dashboard", "Dashboard page title should be 'Food Delivery Dashboard'")
    def test_dashboard_featured_restaurants_section(self):
        # Test Task 3: Check presence of featured restaurants section and its elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_div = soup.find(id='featured-restaurants')
        self.assertIsNotNone(featured_div, "Dashboard should have a div with id 'featured-restaurants'")
        # Check that it contains a list of featured restaurants or a no data message
        ul = featured_div.find('ul')
        self.assertIsNotNone(ul, "'featured-restaurants' div should contain a ul element")
        # At least one li or the no featured restaurants message
        lis = ul.find_all('li')
        self.assertGreater(len(lis), 0, "'featured-restaurants' ul should have at least one li element")
    def test_dashboard_popular_cuisines_section(self):
        # Test Task 3: Check presence of popular cuisines section and its elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        cuisines_div = soup.find(id='popular-cuisines')
        self.assertIsNotNone(cuisines_div, "Dashboard should have a div with id 'popular-cuisines'")
        ul = cuisines_div.find('ul')
        self.assertIsNotNone(ul, "'popular-cuisines' div should contain a ul element")
        lis = ul.find_all('li')
        self.assertGreater(len(lis), 0, "'popular-cuisines' ul should have at least one li element")
    def test_dashboard_buttons_presence_and_links(self):
        # Test Task 3: Check presence of dashboard buttons and their correct links
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        buttons_div = soup.find(id='dashboard-buttons')
        self.assertIsNotNone(buttons_div, "Dashboard should have a div with id 'dashboard-buttons'")
        # Check buttons by id and their onclick links
        browse_btn = buttons_div.find('button', id='browse-restaurants-button')
        self.assertIsNotNone(browse_btn, "Dashboard should have a button with id 'browse-restaurants-button'")
        self.assertIn('/restaurants', browse_btn.get('onclick', ''), "Browse Restaurants button should link to /restaurants")
        cart_btn = buttons_div.find('button', id='view-cart-button')
        self.assertIsNotNone(cart_btn, "Dashboard should have a button with id 'view-cart-button'")
        self.assertIn('/cart', cart_btn.get('onclick', ''), "View Cart button should link to /cart")
        active_orders_btn = buttons_div.find('button', id='active-orders-button')
        self.assertIsNotNone(active_orders_btn, "Dashboard should have a button with id 'active-orders-button'")
        self.assertIn('/active_orders', active_orders_btn.get('onclick', ''), "Active Orders button should link to /active_orders")
if __name__ == '__main__':
    unittest.main()