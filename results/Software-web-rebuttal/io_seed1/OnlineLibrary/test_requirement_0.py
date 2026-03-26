'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page of the website.
'''
import unittest
from main import app
class OnlineLibraryDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2: Check that the dashboard page contains welcome message and navigation buttons
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check welcome message with username 'john_reader'
        self.assertIn('Welcome, john_reader!', html, "Dashboard should display welcome message with username")
        # Check presence of browse books button
        self.assertIn('id="browse-books-button"', html, "Dashboard should have browse books button")
        # Check presence of my borrowings button
        self.assertIn('id="my-borrows-button"', html, "Dashboard should have my borrowings button")
        # Check presence of featured books container
        self.assertIn('id="featured-books-grid"', html, "Dashboard should display featured books grid")
        # Check that featured books include at least one book with status Available
        self.assertIn('Status: Available', html, "Featured books should include books with status Available")
    def test_dashboard_navigation_buttons(self):
        # Test Task 2: Check that navigation buttons link to correct pages
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # The buttons are forms with action URLs, check those URLs exist
        self.assertIn('/book_catalog', html, "Browse Books button should link to /book_catalog")
        self.assertIn('/my_borrowings', html, "My Borrowings button should link to /my_borrowings")
if __name__ == '__main__':
    unittest.main()