'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of the required elements:
- ID: dashboard-page (Div container)
- ID: featured-books (Div container for featured books)
- ID: browse-catalog-button (Button to navigate to catalog)
- ID: view-cart-button (Button to navigate to cart)
- ID: bestsellers-button (Button to navigate to bestsellers)
Also verify that featured books and bestsellers are displayed with correct links.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the root URL '/' is accessible (port 5000 default)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_elements(self):
        # Test presence of required elements on dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "dashboard-page div not found")
        # Check featured-books div
        featured_div = dashboard_div.find('div', id='featured-books')
        self.assertIsNotNone(featured_div, "featured-books div not found")
        # Check buttons by id
        browse_button = dashboard_div.find('button', id='browse-catalog-button')
        self.assertIsNotNone(browse_button, "browse-catalog-button not found")
        view_cart_button = dashboard_div.find('button', id='view-cart-button')
        self.assertIsNotNone(view_cart_button, "view-cart-button not found")
        bestsellers_button = dashboard_div.find('button', id='bestsellers-button')
        self.assertIsNotNone(bestsellers_button, "bestsellers-button not found")
    def test_featured_books_displayed(self):
        # Test that featured books are displayed with correct structure and links
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        featured_div = soup.find('div', id='featured-books')
        self.assertIsNotNone(featured_div)
        book_list_items = featured_div.find_all('li')
        self.assertGreaterEqual(len(book_list_items), 1, "No featured books listed")
        for li in book_list_items:
            # Each li should contain strong tag for title
            strong = li.find('strong')
            self.assertIsNotNone(strong, "Featured book title missing")
            # Should contain author text
            self.assertIn('by', li.text)
            # Should contain price with $ sign
            self.assertIn('$', li.text)
            # Should have a link with id view-book-button-{book_id}
            link = li.find('a')
            self.assertIsNotNone(link, "View Details link missing in featured book")
            self.assertTrue(link['id'].startswith('view-book-button-'), "View Details link id incorrect")
    def test_navigation_buttons_functionality(self):
        # Test that navigation buttons have correct onclick URLs
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        dashboard_div = soup.find('div', id='dashboard-page')
        browse_button = dashboard_div.find('button', id='browse-catalog-button')
        self.assertIn('/catalog', browse_button['onclick'], "Browse Catalog button onclick incorrect")
        view_cart_button = dashboard_div.find('button', id='view-cart-button')
        self.assertIn('/cart', view_cart_button['onclick'], "View Cart button onclick incorrect")
        bestsellers_button = dashboard_div.find('button', id='bestsellers-button')
        self.assertIn('/bestsellers', bestsellers_button['onclick'], "Bestsellers button onclick incorrect")
if __name__ == '__main__':
    unittest.main()