'''
Testing Tasks:
1) Test whether the website can be accessed through local port 5000 (i.e., the root URL '/').
2) Test whether the first page (Dashboard) loads correctly with the welcome message showing the username.
3) Test whether basic navigation buttons on the Dashboard page exist and have correct IDs and text.
4) Test that the Dashboard page contains all required elements as per the requirements document.
'''
import unittest
from main import app
class TestRestaurantReservationDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_root_accessible(self):
        # Test Task 1: Access root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check content type is HTML
        self.assertIn('text/html', response.content_type)
    def test_dashboard_page_content(self):
        # Test Task 2 & 3: Check that dashboard page contains required elements and welcome message
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check presence of dashboard container div with id 'dashboard-page'
        self.assertIn('id="dashboard-page"', html)
        # Check presence of welcome message element with id 'welcome-message'
        self.assertIn('id="welcome-message"', html)
        # Since user is 'jane_food' with full_name 'Jane Foodie', check welcome message text contains 'Welcome, User' (default in HTML)
        # The actual username is set by frontend JS after API call, so here just check the placeholder text exists
        self.assertIn('Welcome, User', html)
        # Check presence of all required buttons with correct IDs and text
        buttons = {
            'make-reservation-button': 'Make Reservation',
            'view-menu-button': 'View Menu',
            'back-to-dashboard': 'Refresh',
            'my-reservations-button': 'My Reservations',
            'my-reviews-button': 'My Reviews',
            'waitlist-button': 'Waitlist',
            'profile-button': 'Profile'
        }
        for btn_id, btn_text in buttons.items():
            self.assertIn(f'id="{btn_id}"', html)
            self.assertIn(btn_text, html)
    def test_dashboard_navigation_buttons_have_onclick(self):
        # Test that buttons have correct onclick attributes for navigation
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check that each button has an onclick attribute with location.href set correctly
        expected_onclicks = {
            'make-reservation-button': "location.href='/make-reservation'",
            'view-menu-button': "location.href='/menu'",
            'back-to-dashboard': "location.href='/'",
            'my-reservations-button': "location.href='/my-reservations'",
            'my-reviews-button': "location.href='/my-reviews'",
            'waitlist-button': "location.href='/waitlist'",
            'profile-button': "location.href='/profile'"
        }
        for btn_id, onclick_val in expected_onclicks.items():
            self.assertIn(f'id="{btn_id}"', html)
            self.assertIn(f'onclick="{onclick_val}"', html)
if __name__ == '__main__':
    unittest.main()