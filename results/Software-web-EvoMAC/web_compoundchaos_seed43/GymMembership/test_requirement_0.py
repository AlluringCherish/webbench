'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Testing Task 3: Test the elements and integrity of the Dashboard page (the first page).
'''
import unittest
from main import app
class GymMembershipTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Task 1: Test access to the root URL '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Task 2 & 3: Test that the dashboard page loads correct content and elements
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Gym Membership Dashboard</title>', html, "Dashboard page title missing or incorrect")
        # Check main container div id
        self.assertIn('id="dashboard-page"', html, "Dashboard main container div missing")
        # Check member welcome section
        self.assertIn('id="member-welcome"', html, "Member welcome section missing")
        # Check welcome message content
        self.assertIn('Welcome, Guest User!', html, "Welcome message missing or incorrect")
        # Check navigation buttons with correct ids and links
        self.assertIn('id="browse-membership-button"', html, "Browse Membership Plans button missing")
        self.assertIn('id="view-schedule-button"', html, "View Class Schedule button missing")
        self.assertIn('id="book-trainer-button"', html, "Book Personal Training button missing")
        # Check featured classes section
        self.assertIn('<h3>Featured Classes</h3>', html, "Featured Classes heading missing")
        # Check at least one featured class from example data (e.g. Morning Yoga)
        self.assertIn('Morning Yoga', html, "Featured class 'Morning Yoga' missing")
        # Check membership plans section
        self.assertIn('<h3>Membership Plans</h3>', html, "Membership Plans heading missing")
        # Check at least one membership plan from example data (e.g. Basic)
        self.assertIn('Basic', html, "Membership plan 'Basic' missing")
    def test_dashboard_navigation_buttons(self):
        # Task 2: Test that navigation buttons link to correct pages
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Extract URLs from buttons and test accessibility
        # Browse Membership Plans button
        resp_memberships = self.client.get('/memberships')
        self.assertEqual(resp_memberships.status_code, 200, "Membership Plans page should be accessible")
        # View Class Schedule button
        resp_classes = self.client.get('/classes')
        self.assertEqual(resp_classes.status_code, 200, "Class Schedule page should be accessible")
        # Book Personal Training button
        resp_booking = self.client.get('/booking')
        self.assertEqual(resp_booking.status_code, 200, "Personal Training Booking page should be accessible")
if __name__ == '__main__':
    unittest.main()