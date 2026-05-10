'''
Test cases for MovieTicketing web application to verify:
- Task 1: The website can be accessed through local port 5000 (test dashboard page accessibility).
- Task 2: The first page (Dashboard) loads correctly and basic navigation buttons redirect properly.
- Task 3: Presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class MovieTicketingDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Task 1: Test if dashboard page is accessible (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Task 2 & 3: Test if dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page must contain div with id 'dashboard-page'")
        # Check featured movies div with id 'featured-movies'
        featured_div = soup.find('div', id='featured-movies')
        self.assertIsNotNone(featured_div, "Dashboard page must contain div with id 'featured-movies'")
        # Check buttons with correct ids
        browse_button = soup.find('button', id='browse-movies-button')
        self.assertIsNotNone(browse_button, "Dashboard page must contain button with id 'browse-movies-button'")
        view_bookings_button = soup.find('button', id='view-bookings-button')
        self.assertIsNotNone(view_bookings_button, "Dashboard page must contain button with id 'view-bookings-button'")
        showtimes_button = soup.find('button', id='showtimes-button')
        self.assertIsNotNone(showtimes_button, "Dashboard page must contain button with id 'showtimes-button'")
    def test_dashboard_navigation_buttons(self):
        # Task 2: Test navigation buttons redirect to correct pages
        # The buttons likely trigger navigation via client-side JS or form submission,
        # but we can test the /navigate/<page> route which is used for navigation.
        # Test navigation to catalog
        response = self.client.get('/navigate/catalog', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/catalog', response.headers['Location'])
        # Test navigation to bookings
        response = self.client.get('/navigate/bookings', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/bookings', response.headers['Location'])
        # Test navigation to showtimes
        response = self.client.get('/navigate/showtimes', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/showtimes', response.headers['Location'])
        # Test navigation to theaters
        response = self.client.get('/navigate/theaters', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/theaters/info', response.headers['Location'])
if __name__ == '__main__':
    unittest.main()