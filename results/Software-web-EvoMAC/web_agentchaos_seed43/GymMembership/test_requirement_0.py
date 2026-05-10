'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of specified elements:
- ID: dashboard-page (Div container)
- ID: member-welcome (Div welcome section)
- ID: browse-membership-button (Button to membership plans)
- ID: view-schedule-button (Button to class schedule)
- ID: book-trainer-button (Button to personal training booking)
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class GymMembershipDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status 200")
    def test_dashboard_page_elements(self):
        # Test presence of required elements on dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check for dashboard-page div
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container with id 'dashboard-page' should be present")
        # Check for member-welcome div
        member_welcome = soup.find(id='member-welcome')
        self.assertIsNotNone(member_welcome, "Member welcome section with id 'member-welcome' should be present")
        # Check for browse-membership-button button
        browse_membership_btn = soup.find(id='browse-membership-button')
        self.assertIsNotNone(browse_membership_btn, "Button with id 'browse-membership-button' should be present")
        # Check for view-schedule-button button
        view_schedule_btn = soup.find(id='view-schedule-button')
        self.assertIsNotNone(view_schedule_btn, "Button with id 'view-schedule-button' should be present")
        # Check for book-trainer-button button
        book_trainer_btn = soup.find(id='book-trainer-button')
        self.assertIsNotNone(book_trainer_btn, "Button with id 'book-trainer-button' should be present")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        browse_btn = soup.find(id='browse-membership-button')
        self.assertIsNotNone(browse_btn)
        # The button might be a form submit or a link, check href or form action or onclick attribute
        # We accept href or onclick or form action containing '/membership-plans'
        href = browse_btn.get('href')
        onclick = browse_btn.get('onclick')
        self.assertTrue(
            (href and '/membership-plans' in href) or
            (onclick and '/membership-plans' in onclick),
            "Browse membership button should navigate to '/membership-plans' page"
        )
        schedule_btn = soup.find(id='view-schedule-button')
        self.assertIsNotNone(schedule_btn)
        href = schedule_btn.get('href')
        onclick = schedule_btn.get('onclick')
        self.assertTrue(
            (href and '/class-schedule' in href) or
            (onclick and '/class-schedule' in onclick),
            "View schedule button should navigate to '/class-schedule' page"
        )
        book_btn = soup.find(id='book-trainer-button')
        self.assertIsNotNone(book_btn)
        href = book_btn.get('href')
        onclick = book_btn.get('onclick')
        self.assertTrue(
            (href and '/pt-booking' in href) or
            (onclick and '/pt-booking' in onclick),
            "Book trainer button should navigate to '/pt-booking' page"
        )
if __name__ == '__main__':
    unittest.main()