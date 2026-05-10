'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of all specified elements as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineLibraryTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.username = 'john_reader'  # From example data
        # Log in before tests that require login
        with self.client:
            response = self.client.post('/login', data={'username': self.username}, follow_redirects=True)
            self.assertIn(b'Welcome, john_reader!', response.data)
    def tearDown(self):
        # Log out after tests
        with self.client:
            self.client.get('/logout', follow_redirects=True)
    def test_access_dashboard_page(self):
        # Access the dashboard page '/'
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            # Check page title
            self.assertIn(b'<title>Library Dashboard</title>', response.data)
            # Parse HTML to check elements
            soup = BeautifulSoup(response.data, 'html.parser')
            dashboard_div = soup.find(id='dashboard-page')
            self.assertIsNotNone(dashboard_div, "Dashboard container div not found")
            welcome_message = soup.find(id='welcome-message')
            self.assertIsNotNone(welcome_message, "Welcome message element not found")
            self.assertIn(self.username, welcome_message.text)
            browse_button = soup.find(id='browse-books-button')
            self.assertIsNotNone(browse_button, "Browse Books button not found")
            my_borrows_button = soup.find(id='my-borrows-button')
            self.assertIsNotNone(my_borrows_button, "My Borrowings button not found")
            # Check featured books grid
            book_grid = soup.find(id='book-grid')
            self.assertIsNotNone(book_grid, "Book grid container not found")
            # Check that featured books are displayed (based on example data, at least one available book)
            book_cards = book_grid.find_all(class_='book-card')
            self.assertGreaterEqual(len(book_cards), 1, "No featured book cards found")
    def test_navigation_from_dashboard(self):
        # Test navigation buttons on dashboard page
        with self.client:
            # Browse Books button leads to /catalog
            response = self.client.get('/catalog')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<title>Book Catalog</title>', response.data)
            # My Borrowings button leads to /my_borrowings
            response = self.client.get('/my_borrowings')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<title>My Borrowings</title>', response.data)
    def test_dashboard_featured_books_elements(self):
        # Check each featured book card elements on dashboard page
        with self.client:
            response = self.client.get('/')
            soup = BeautifulSoup(response.data, 'html.parser')
            book_cards = soup.select('#book-grid .book-card')
            for card in book_cards:
                # Check for book cover image
                img = card.find('img')
                self.assertIsNotNone(img, "Book cover image missing in book card")
                self.assertTrue(img.has_attr('src'), "Book cover image src attribute missing")
                # Check for book title h3
                title = card.find('h3')
                self.assertIsNotNone(title, "Book title missing in book card")
                self.assertTrue(len(title.text.strip()) > 0, "Book title is empty")
                # Check for author paragraph
                author_p = card.find('p', string=lambda text: text and text.startswith('by '))
                self.assertIsNotNone(author_p, "Book author paragraph missing or incorrect")
                # Check for status paragraph
                status_p = card.find('p', string=lambda text: text and text.startswith('Status:'))
                self.assertIsNotNone(status_p, "Book status paragraph missing or incorrect")
                # Check for rating paragraph
                rating_p = card.find('p', string=lambda text: text and text.startswith('Rating:'))
                self.assertIsNotNone(rating_p, "Book rating paragraph missing or incorrect")
                # Check for view details button with correct id
                button = card.find('button')
                self.assertIsNotNone(button, "View Details button missing in book card")
                self.assertTrue(button.has_attr('id'), "View Details button missing id attribute")
                self.assertTrue(button['id'].startswith('view-book-button-'), "View Details button id incorrect")
if __name__ == '__main__':
    unittest.main()