'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test basic navigation buttons on the Dashboard page.
'''
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import socket
import time
import requests
from bs4 import BeautifulSoup
# We will start a simple HTTP server serving the current directory on port 5000 for testing.
# This simulates the local server hosting the HTML files.
PORT = 5000
class TestLocalServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start HTTP server in a separate thread
        handler = SimpleHTTPRequestHandler
        cls.httpd = HTTPServer(('localhost', PORT), handler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        # Wait a moment for server to start
        time.sleep(1)
    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.server_thread.join()
    def test_access_dashboard_page(self):
        # Test if the dashboard page is accessible via http://localhost:5000/dashboard.html
        url = f'http://localhost:{PORT}/dashboard.html'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
        # Check that the page title is correct
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Bookstore Dashboard", "Dashboard page title is incorrect")
    def test_dashboard_navigation_buttons(self):
        # Test that the navigation buttons exist and have correct hrefs
        url = f'http://localhost:{PORT}/dashboard.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Browse Catalog button
        browse_button = soup.find('button', id='browse-catalog-button')
        self.assertIsNotNone(browse_button, "Browse Catalog button not found on Dashboard")
        self.assertIn("book_catalog.html", browse_button.get('onclick', ''), "Browse Catalog button does not navigate correctly")
        # View Cart button
        view_cart_button = soup.find('button', id='view-cart-button')
        self.assertIsNotNone(view_cart_button, "View Cart button not found on Dashboard")
        self.assertIn("cart.html", view_cart_button.get('onclick', ''), "View Cart button does not navigate correctly")
        # Order History button
        order_history_button = soup.find('button', id='order-history-button')
        self.assertIsNotNone(order_history_button, "Order History button not found on Dashboard")
        self.assertIn("order_history.html", order_history_button.get('onclick', ''), "Order History button does not navigate correctly")
if __name__ == '__main__':
    unittest.main()