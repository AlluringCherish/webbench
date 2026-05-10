'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website loads correctly and basic navigation works.
Testing Task 3: Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineLibraryTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_root_redirects_to_dashboard(self):
        # Test Task 1 and part of Task 2: Access root '/' and check redirect to /dashboard
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard', response.headers['Location'])
    def test_dashboard_page_loads(self):
        # Test Task 2: Access /dashboard and check status code and page title
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page title
        self.assertIn('Library Dashboard', soup.title.string)
        # Check presence of dashboard container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div)
        # Check presence of welcome message h1 with id 'welcome-message' and contains username
        welcome_h1 = soup.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_h1)
        self.assertIn('john_reader', welcome_h1.text)
        # Check presence of browse books button with id 'browse-books-button'
        browse_button = soup.find('button', id='browse-books-button')
        self.assertIsNotNone(browse_button)
        # Check presence of my borrows button with id 'my-borrows-button'
        my_borrows_button = soup.find('button', id='my-borrows-button')
        self.assertIsNotNone(my_borrows_button)
        # Check presence of featured books (at least one featured book card)
        # Featured books are passed to template, so check if any book info is rendered
        # We expect some text from featured books in the dashboard div
        self.assertTrue(len(dashboard_div.text.strip()) > 0)
if __name__ == '__main__':
    unittest.main()