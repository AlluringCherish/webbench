'''
Testing Task 1, 2, 3:
- Test whether the website can be accessed through local port 5000 (root URL).
- Test whether the first page (Dashboard) loads correctly with example data.
- Test basic navigation buttons on the Dashboard page.
- Test presence and correctness of specified elements on the Dashboard page.
'''
import unittest
from main import app
class TestOnlineCourseDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
    def tearDown(self):
        self.ctx.pop()
    def login(self, username='john'):
        # Mock login by setting session cookie via login route
        return self.client.post('/login', data=dict(username=username, password='any'), follow_redirects=True)
    def test_01_access_root_redirects_to_login_if_not_logged_in(self):
        # Access root '/' without login should redirect to login page
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])
    def test_02_login_and_access_dashboard(self):
        # Login and access dashboard page
        login_response = self.login('john')
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Welcome, John Student!', login_response.data)
        dashboard_response = self.client.get('/')
        self.assertEqual(dashboard_response.status_code, 200)
        # Check presence of dashboard page container div
        self.assertIn(b'id="dashboard-page"', dashboard_response.data)
        # Check presence of welcome message with user's full name
        self.assertIn(b'id="welcome-message"', dashboard_response.data)
        self.assertIn(b'John Student', dashboard_response.data)
        # Check presence of enrolled courses container
        self.assertIn(b'id="enrolled-courses"', dashboard_response.data)
        # Check presence of browse courses button
        self.assertIn(b'id="browse-courses-button"', dashboard_response.data)
        # Check presence of my courses button
        self.assertIn(b'id="my-courses-button"', dashboard_response.data)
    def test_03_dashboard_navigation_buttons(self):
        # Login first
        self.login('john')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # The buttons should be present and have correct form or link
        # Since buttons are in HTML, check their presence by id and type
        html = response.data.decode('utf-8')
        self.assertIn('id="browse-courses-button"', html)
        self.assertIn('id="my-courses-button"', html)
    def test_04_dashboard_enrolled_courses_content(self):
        # Login as john who has enrollments in example data
        self.login('john')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        # Check that enrolled courses titles from example data appear
        self.assertIn('Python Programming', html)
        self.assertIn('Web Development', html)
        # Check progress percentages appear (75 and 25 from example data)
        self.assertIn('75', html)
        self.assertIn('25', html)
if __name__ == '__main__':
    unittest.main()