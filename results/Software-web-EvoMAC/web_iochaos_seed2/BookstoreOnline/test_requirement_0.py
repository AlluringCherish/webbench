'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured books, bestsellers, and navigation buttons.
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
        # Test if the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test if the page title is correct
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Bookstore Dashboard", "Dashboard page title should be 'Bookstore Dashboard'")
    def test_dashboard_featured_books_section(self):
        # Test presence of featured books section and at least one featured book from example data
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find(id="featured-books")
        self.assertIsNotNone(featured_section, "Featured books section should be present")
        book_cards = featured_section.find_all(class_="book-card")
        self.assertGreaterEqual(len(book_cards), 1, "There should be at least one featured book displayed")
        # Check that each book card has title, author, price, and view button
        for card in book_cards:
            self.assertTrue(card.get("data-title"), "Book card should have data-title attribute")
            self.assertTrue(card.get("data-author"), "Book card should have data-author attribute")
            self.assertTrue(card.get("data-isbn"), "Book card should have data-isbn attribute")
            self.assertTrue(card.get("data-category"), "Book card should have data-category attribute")
            self.assertIsNotNone(card.find("h3"), "Book card should have a title element (h3)")
            self.assertIsNotNone(card.find("button", id=lambda x: x and x.startswith("view-book-button-")), "Book card should have a view details button")
    def test_dashboard_bestsellers_section(self):
        # Test presence of bestsellers section and that it lists bestsellers with rank, title, author, sales count, and view button
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        bestsellers_section = soup.find(id="bestsellers-list")
        self.assertIsNotNone(bestsellers_section, "Bestsellers section should be present")
        ol = bestsellers_section.find("ol")
        self.assertIsNotNone(ol, "Bestsellers list should be an ordered list")
        items = ol.find_all("li")
        self.assertGreaterEqual(len(items), 1, "There should be at least one bestseller listed")
        for li in items:
            rank_span = li.find(class_="rank")
            title_span = li.find(class_="title")
            author_span = li.find(class_="author")
            sales_span = li.find(class_="sales-count")
            view_button = li.find("button", id=lambda x: x and x.startswith("view-book-button-"))
            self.assertIsNotNone(rank_span, "Bestseller item should have rank span")
            self.assertIsNotNone(title_span, "Bestseller item should have title span")
            self.assertIsNotNone(author_span, "Bestseller item should have author span")
            self.assertIsNotNone(sales_span, "Bestseller item should have sales count span")
            self.assertIsNotNone(view_button, "Bestseller item should have view details button")
    def test_dashboard_navigation_buttons(self):
        # Test presence and correctness of navigation buttons on dashboard
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        browse_btn = soup.find("button", id="browse-catalog-button")
        cart_btn = soup.find("button", id="view-cart-button")
        bestsellers_btn = soup.find("button", id="bestsellers-button")
        self.assertIsNotNone(browse_btn, "Browse Catalog button should be present")
        self.assertIsNotNone(cart_btn, "View Cart button should be present")
        self.assertIsNotNone(bestsellers_btn, "Bestsellers button should be present")
        self.assertEqual(browse_btn.text.strip(), "Browse Catalog", "Browse Catalog button text should be correct")
        self.assertEqual(cart_btn.text.strip(), "View Cart", "View Cart button text should be correct")
        self.assertEqual(bestsellers_btn.text.strip(), "Bestsellers", "Bestsellers button text should be correct")
if __name__ == '__main__':
    unittest.main()