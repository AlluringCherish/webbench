'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured books and navigation buttons.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class TestBookstoreOnlineDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at root '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_title(self):
        # Test that the page title is correct
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('title')
        self.assertIsNotNone(title)
        self.assertEqual(title.text.strip(), 'Bookstore Dashboard')
    def test_dashboard_featured_books_section(self):
        # Test that the featured books section exists and contains expected elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find(id='featured-books')
        self.assertIsNotNone(featured_section)
        # Check that at least one featured book card is present or the no books message
        book_cards = featured_section.find_all(class_='book-card')
        no_books_msg = featured_section.find('p')
        self.assertTrue(len(book_cards) > 0 or (no_books_msg and 'No featured books' in no_books_msg.text))
    def test_dashboard_navigation_buttons(self):
        # Test presence and correctness of navigation buttons with correct IDs and links
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        nav = soup.find(id='navigation-buttons')
        self.assertIsNotNone(nav)
        # Check buttons by ID and their onclick links
        browse_btn = nav.find('button', id='browse-catalog-button')
        self.assertIsNotNone(browse_btn)
        self.assertIn('/catalog', browse_btn['onclick'])
        cart_btn = nav.find('button', id='view-cart-button')
        self.assertIsNotNone(cart_btn)
        self.assertIn('/cart', cart_btn['onclick'])
        bestsellers_btn = nav.find('button', id='bestsellers-button')
        self.assertIsNotNone(bestsellers_btn)
        self.assertIn('/bestsellers', bestsellers_btn['onclick'])
    def test_dashboard_page_container(self):
        # Test that the main container div with id 'dashboard-page' exists
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='dashboard-page')
        self.assertIsNotNone(container)
if __name__ == '__main__':
    unittest.main()