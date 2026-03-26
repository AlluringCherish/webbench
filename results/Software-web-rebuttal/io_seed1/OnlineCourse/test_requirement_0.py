'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page (Dashboard) of the website loads correctly and basic navigation works based on example data.
Testing Task 3: Test the elements and integrity of the Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineCourseTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        # To test dashboard, user must be logged in.
        # We will simulate login by setting session cookie via test client.
        # Flask test client does not allow direct session manipulation,
        # so we perform login via POST to /login with a valid username from example data.
        self.login_username = 'john'  # from example users.txt
        response = self.client.post('/login', data={'username': self.login_username}, follow_redirects=True)
        self.assertIn(b'Logged in as', response.data)
    def tearDown(self):
        self.ctx.pop()
    def test_server_accessibility(self):
        # Test Task 1: Access root URL '/' which is dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Test Task 2 & 3: Check dashboard page content and elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Parse HTML content
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check for div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check for h1 with id 'welcome-message' containing user's full name
        welcome_h1 = dashboard_div.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_h1, "Welcome message h1 with id 'welcome-message' should be present")
        self.assertIn(self.login_username.capitalize(), welcome_h1.text, "Welcome message should contain user's name")
        # Check for div with id 'enrolled-courses'
        enrolled_div = dashboard_div.find('div', id='enrolled-courses')
        self.assertIsNotNone(enrolled_div, "Div with id 'enrolled-courses' should be present")
        # Check that enrolled courses are listed or message shown
        # Since user 'john' is enrolled in courses per example data, expect list
        ul = enrolled_div.find('ul')
        p = enrolled_div.find('p')
        self.assertTrue(ul or p, "Either a list of enrolled courses or a message should be present")
        # Check for buttons with ids 'browse-courses-button' and 'my-courses-button'
        browse_button = dashboard_div.find('button', id='browse-courses-button')
        my_courses_button = dashboard_div.find('button', id='my-courses-button')
        self.assertIsNotNone(browse_button, "Button with id 'browse-courses-button' should be present")
        self.assertIsNotNone(my_courses_button, "Button with id 'my-courses-button' should be present")
        # Check buttons have correct onclick attributes (navigation)
        self.assertIn('/course_catalog', browse_button.get('onclick', ''), "Browse Courses button should navigate to course catalog")
        self.assertIn('/my_courses', my_courses_button.get('onclick', ''), "My Courses button should navigate to my courses page")
    def test_navigation_from_dashboard(self):
        # Test navigation buttons from dashboard page
        # Browse Courses button navigation
        response = self.client.get('/course_catalog')
        self.assertEqual(response.status_code, 200, "Course Catalog page should be accessible")
        # My Courses button navigation
        response = self.client.get('/my_courses')
        self.assertEqual(response.status_code, 200, "My Courses page should be accessible")
if __name__ == '__main__':
    unittest.main()