'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured books, bestsellers, and navigation buttons.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class BookstoreOnlineTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Test Task 2 & 3: Check that dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id dashboard-page
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured books section and at least one featured book card
        featured_section = dashboard_div.find('section', id='featured-books')
        self.assertIsNotNone(featured_section, "Featured books section with id 'featured-books' should be present")
        book_cards = featured_section.find_all('div', class_='book-card')
        self.assertGreaterEqual(len(book_cards), 1, "There should be at least one featured book card")
        # Check each featured book card has title, author, price, and view details button with correct id
        for card in book_cards:
            title = card.find('h3')
            self.assertIsNotNone(title)
            author_p = card.find('p', string=lambda text: text and 'Author:' in text)
            self.assertIsNotNone(author_p)
            price_p = card.find('p', string=lambda text: text and 'Price:' in text)
            self.assertIsNotNone(price_p)
            button = card.find('button', id=lambda x: x and x.startswith('view-book-button-'))
            self.assertIsNotNone(button)
        # Check bestsellers section and at least one bestseller item
        bestsellers_section = dashboard_div.find('section', id='bestsellers-section')
        self.assertIsNotNone(bestsellers_section, "Bestsellers section with id 'bestsellers-section' should be present")
        bestseller_items = bestsellers_section.find_all('div', class_='bestseller-item')
        self.assertGreaterEqual(len(bestseller_items), 1, "There should be at least one bestseller item")
        # Check each bestseller item has rank, title, author, sales count, and view details button with correct id
        for item in bestseller_items:
            text = item.get_text()
            self.assertIn('Sales:', text)
            button = item.find('button', id=lambda x: x and x.startswith('view-book-button-'))
            self.assertIsNotNone(button)
        # Check navigation buttons with correct ids and hrefs
        nav = dashboard_div.find('nav', class_='dashboard-nav')
        self.assertIsNotNone(nav, "Dashboard navigation with class 'dashboard-nav' should be present")
        browse_button = nav.find('button', id='browse-catalog-button')
        self.assertIsNotNone(browse_button)
        view_cart_button = nav.find('button', id='view-cart-button')
        self.assertIsNotNone(view_cart_button)
        bestsellers_button = nav.find('button', id='bestsellers-button')
        self.assertIsNotNone(bestsellers_button)
        # Check that buttons have onclick attributes with correct URLs
        self.assertIn('/catalog', browse_button.get('onclick', ''), "Browse Catalog button should navigate to /catalog")
        self.assertIn('/cart', view_cart_button.get('onclick', ''), "View Cart button should navigate to /cart")
        self.assertIn('/bestsellers', bestsellers_button.get('onclick', ''), "Bestsellers button should navigate to /bestsellers")
if __name__ == '__main__':
    unittest.main()