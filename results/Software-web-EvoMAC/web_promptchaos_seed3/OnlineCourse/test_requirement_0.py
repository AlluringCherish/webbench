'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page (Dashboard) of the website loads correctly and basic navigation buttons work.
Testing Task 3: Test the elements and integrity of the Dashboard page as per requirements:
- ID: dashboard-page (Div container)
- ID: welcome-message (H1 with user's name)
- ID: enrolled-courses (Div showing enrolled courses)
- ID: browse-courses-button (Button to navigate to course catalog)
- ID: my-courses-button (Button to navigate to my courses page)
'''
import unittest
from main import app
class TestOnlineCourseDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_server_running_and_dashboard_accessible(self):
        # Test that the server responds on '/' (dashboard) with status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Access dashboard page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for dashboard-page div
        self.assertIn('id="dashboard-page"', html, "Dashboard page should contain div with id 'dashboard-page'")
        # Check for welcome-message h1
        self.assertIn('id="welcome-message"', html, "Dashboard page should contain h1 with id 'welcome-message'")
        # Check that welcome message contains the default user fullname "John Student"
        self.assertIn('Welcome, John Student!', html, "Welcome message should display the user's full name")
        # Check for enrolled-courses div
        self.assertIn('id="enrolled-courses"', html, "Dashboard page should contain div with id 'enrolled-courses'")
        # Check for browse-courses-button button
        self.assertIn('id="browse-courses-button"', html, "Dashboard page should contain button with id 'browse-courses-button'")
        # Check for my-courses-button button
        self.assertIn('id="my-courses-button"', html, "Dashboard page should contain button with id 'my-courses-button'")
    def test_dashboard_navigation_buttons(self):
        # Access dashboard page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check that browse-courses-button navigates to /catalog
        self.assertIn("location.href='/catalog'", html, "Browse Courses button should navigate to /catalog")
        # Check that my-courses-button navigates to /my-courses
        self.assertIn("location.href='/my-courses'", html, "My Courses button should navigate to /my-courses")
if __name__ == '__main__':
    unittest.main()