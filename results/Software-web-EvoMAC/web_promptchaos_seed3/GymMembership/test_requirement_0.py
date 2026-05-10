'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, including presence of required elements:
- ID: dashboard-page (Div container)
- ID: member-welcome (Div welcome section)
- ID: browse-membership-button (Button to membership plans)
- ID: view-schedule-button (Button to class schedule)
- ID: book-trainer-button (Button to personal training booking)
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
        # Test that the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements with correct IDs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check for dashboard-page div
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' not found")
        # Check for member-welcome div
        member_welcome_div = soup.find(id='member-welcome')
        self.assertIsNotNone(member_welcome_div, "Member welcome div with id 'member-welcome' not found")
        # Check for browse-membership-button button
        browse_membership_button = soup.find(id='browse-membership-button')
        self.assertIsNotNone(browse_membership_button, "Button with id 'browse-membership-button' not found")
        self.assertEqual(browse_membership_button.name, 'button', "'browse-membership-button' is not a button element")
        # Check for view-schedule-button button
        view_schedule_button = soup.find(id='view-schedule-button')
        self.assertIsNotNone(view_schedule_button, "Button with id 'view-schedule-button' not found")
        self.assertEqual(view_schedule_button.name, 'button', "'view-schedule-button' is not a button element")
        # Check for book-trainer-button button
        book_trainer_button = soup.find(id='book-trainer-button')
        self.assertIsNotNone(book_trainer_button, "Button with id 'book-trainer-button' not found")
        self.assertEqual(book_trainer_button.name, 'button', "'book-trainer-button' is not a button element")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct pages
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Buttons might be <button> with onclick or <a> tags, check href or onclick attribute
        # Check browse-membership-button navigates to /memberships
        browse_button = soup.find(id='browse-membership-button')
        self.assertIsNotNone(browse_button, "browse-membership-button not found")
        # Check if button is inside a form or has onclick or is a link
        # We accept either <button onclick="location.href='...'"> or <a> with id
        href = None
        if browse_button.name == 'button':
            onclick = browse_button.get('onclick', '')
            self.assertIn('/memberships', onclick, "browse-membership-button does not navigate to /memberships")
        elif browse_button.name == 'a':
            href = browse_button.get('href', '')
            self.assertIn('/memberships', href, "browse-membership-button link does not point to /memberships")
        # Check view-schedule-button navigates to /classes
        schedule_button = soup.find(id='view-schedule-button')
        self.assertIsNotNone(schedule_button, "view-schedule-button not found")
        if schedule_button.name == 'button':
            onclick = schedule_button.get('onclick', '')
            self.assertIn('/classes', onclick, "view-schedule-button does not navigate to /classes")
        elif schedule_button.name == 'a':
            href = schedule_button.get('href', '')
            self.assertIn('/classes', href, "view-schedule-button link does not point to /classes")
        # Check book-trainer-button navigates to /book_training
        book_button = soup.find(id='book-trainer-button')
        self.assertIsNotNone(book_button, "book-trainer-button not found")
        if book_button.name == 'button':
            onclick = book_button.get('onclick', '')
            self.assertIn('/book_training', onclick, "book-trainer-button does not navigate to /book_training")
        elif book_button.name == 'a':
            href = book_button.get('href', '')
            self.assertIn('/book_training', href, "book-trainer-button link does not point to /book_training")
if __name__ == '__main__':
    unittest.main()