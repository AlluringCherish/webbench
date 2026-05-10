'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of the Dashboard page by verifying the presence and correctness of the specified elements as per the requirements document.
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
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check that dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check welcome section div with id 'member-welcome'
        member_welcome_div = dashboard_div.find('div', id='member-welcome')
        self.assertIsNotNone(member_welcome_div, "Member welcome div with id 'member-welcome' should be present")
        # Check that welcome message contains expected text snippet
        self.assertIn("Welcome", member_welcome_div.get_text(), "Welcome message should contain 'Welcome'")
        # Check featured classes section
        featured_classes_div = dashboard_div.find('div', id='featured-classes')
        self.assertIsNotNone(featured_classes_div, "Featured classes div with id 'featured-classes' should be present")
        # It should contain a ul with li elements or a message if no classes
        ul = featured_classes_div.find('ul')
        if ul:
            lis = ul.find_all('li')
            self.assertTrue(len(lis) > 0, "Featured classes list should have at least one class listed")
            # Check that each li contains class name and schedule info
            for li in lis:
                text = li.get_text()
                self.assertRegex(text, r".+\s-\s.+\sat\s.+\s\(\d+\smins\)", "Each featured class should show name, day, time and duration")
        else:
            # If no ul, check for no classes message
            no_classes_msg = featured_classes_div.find('p')
            self.assertIsNotNone(no_classes_msg, "If no classes, a message paragraph should be present")
        # Check dashboard buttons container
        buttons_div = dashboard_div.find('div', id='dashboard-buttons')
        self.assertIsNotNone(buttons_div, "Dashboard buttons container div with id 'dashboard-buttons' should be present")
        # Check presence of buttons with correct ids and their onclick attributes
        browse_btn = buttons_div.find('button', id='browse-membership-button')
        self.assertIsNotNone(browse_btn, "Button with id 'browse-membership-button' should be present")
        self.assertIn('/membership_plans', browse_btn.get('onclick', ''), "Browse Membership Plans button should navigate to /membership_plans")
        schedule_btn = buttons_div.find('button', id='view-schedule-button')
        self.assertIsNotNone(schedule_btn, "Button with id 'view-schedule-button' should be present")
        self.assertIn('/class_schedule', schedule_btn.get('onclick', ''), "View Class Schedule button should navigate to /class_schedule")
        book_trainer_btn = buttons_div.find('button', id='book-trainer-button')
        self.assertIsNotNone(book_trainer_btn, "Button with id 'book-trainer-button' should be present")
        self.assertIn('/pt_booking', book_trainer_btn.get('onclick', ''), "Book Personal Training button should navigate to /pt_booking")
if __name__ == '__main__':
    unittest.main()