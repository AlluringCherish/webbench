'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence and correctness of specified elements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class GymMembershipTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content_and_navigation_buttons(self):
        # Test Task 2 & 3: Check dashboard page content and navigation buttons
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' should be present")
        # Check welcome section div with id 'member-welcome'
        welcome_div = dashboard_div.find('div', id='member-welcome')
        self.assertIsNotNone(welcome_div, "Welcome section div with id 'member-welcome' should be present")
        self.assertIn("Welcome to GymMembership", welcome_div.text, "Welcome message should be present in member-welcome div")
        # Check featured class section
        featured_class_div = dashboard_div.find('div', id='featured-classes')
        self.assertIsNotNone(featured_class_div, "Featured classes div with id 'featured-classes' should be present")
        # It should contain either a featured class or a no class message
        self.assertTrue(featured_class_div.find('strong') or "No featured class available." in featured_class_div.text)
        # Check featured trainer section
        featured_trainer_div = dashboard_div.find('div', id='featured-trainers')
        self.assertIsNotNone(featured_trainer_div, "Featured trainers div with id 'featured-trainers' should be present")
        # It should contain either a featured trainer or a no trainer message
        self.assertTrue(featured_trainer_div.find('strong') or "No featured trainer available." in featured_trainer_div.text)
        # Check navigation buttons with correct ids and hrefs
        nav_div = dashboard_div.find('div', id='dashboard-navigation')
        self.assertIsNotNone(nav_div, "Dashboard navigation div with id 'dashboard-navigation' should be present")
        browse_btn = nav_div.find('button', id='browse-membership-button')
        self.assertIsNotNone(browse_btn, "Button with id 'browse-membership-button' should be present")
        self.assertIn("Browse Membership Plans", browse_btn.text)
        view_schedule_btn = nav_div.find('button', id='view-schedule-button')
        self.assertIsNotNone(view_schedule_btn, "Button with id 'view-schedule-button' should be present")
        self.assertIn("View Class Schedule", view_schedule_btn.text)
        book_trainer_btn = nav_div.find('button', id='book-trainer-button')
        self.assertIsNotNone(book_trainer_btn, "Button with id 'book-trainer-button' should be present")
        self.assertIn("Book Personal Training", book_trainer_btn.text)
    def test_dashboard_navigation_buttons_functionality(self):
        # Test that navigation buttons URLs correspond to backend routes
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        nav_div = soup.find('div', id='dashboard-navigation')
        # Extract onclick attributes and verify URLs
        browse_btn = nav_div.find('button', id='browse-membership-button')
        self.assertIn('/memberships', browse_btn['onclick'], "Browse Membership Plans button should navigate to /memberships")
        view_schedule_btn = nav_div.find('button', id='view-schedule-button')
        self.assertIn('/schedule', view_schedule_btn['onclick'], "View Class Schedule button should navigate to /schedule")
        book_trainer_btn = nav_div.find('button', id='book-trainer-button')
        self.assertIn('/booking', book_trainer_btn['onclick'], "Book Personal Training button should navigate to /booking")
if __name__ == '__main__':
    unittest.main()