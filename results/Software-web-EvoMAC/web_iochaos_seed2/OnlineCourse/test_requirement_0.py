'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation works.
Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineCourseBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check the Dashboard page elements and content
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' should be present")
        # Check welcome message h1 with id 'welcome-message'
        welcome_h1 = dashboard_div.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_h1, "Welcome message h1 with id 'welcome-message' should be present")
        self.assertIn("Welcome,", welcome_h1.text, "Welcome message should contain 'Welcome,'")
        # Check enrolled courses div with id 'enrolled-courses'
        enrolled_div = dashboard_div.find('div', id='enrolled-courses')
        self.assertIsNotNone(enrolled_div, "Enrolled courses div with id 'enrolled-courses' should be present")
        # Check buttons: browse-courses-button and my-courses-button
        browse_button = dashboard_div.find('button', id='browse-courses-button')
        self.assertIsNotNone(browse_button, "Button with id 'browse-courses-button' should be present")
        self.assertEqual(browse_button.text.strip(), "Browse Courses", "Browse Courses button text should be correct")
        my_courses_button = dashboard_div.find('button', id='my-courses-button')
        self.assertIsNotNone(my_courses_button, "Button with id 'my-courses-button' should be present")
        self.assertEqual(my_courses_button.text.strip(), "My Courses", "My Courses button text should be correct")
    def test_dashboard_enrolled_courses_list(self):
        # Test that enrolled courses list is present and correctly formatted if user has enrollments
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        enrolled_div = soup.find('div', id='enrolled-courses')
        # The example data has user 'john' enrolled in courses 1 and 2, so list should be present
        ul = enrolled_div.find('ul')
        self.assertIsNotNone(ul, "Enrolled courses list (ul) should be present when user has enrollments")
        # Check that each li contains course title, progress and status
        lis = ul.find_all('li')
        self.assertGreater(len(lis), 0, "There should be at least one enrolled course listed")
        for li in lis:
            text = li.get_text()
            self.assertRegex(text, r'Progress: \d+%', "Each enrolled course should show progress percentage")
            self.assertRegex(text, r'Status: (In Progress|Completed)', "Each enrolled course should show status")
if __name__ == '__main__':
    unittest.main()