'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) can be accessed and loads correctly.
Test basic navigation from Dashboard to Course Catalog and My Courses pages.
Verify presence of key elements on Dashboard page as per requirements.
'''
import unittest
from main import app
class OnlineCourseBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test root '/' route returns 200 and contains expected elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Learning Dashboard</title>', html)
        # Check presence of dashboard-page div
        self.assertIn('id="dashboard-page"', html)
        # Check presence of welcome-message h1
        self.assertIn('id="welcome-message"', html)
        # Check presence of enrolled-courses div
        self.assertIn('id="enrolled-courses"', html)
        # Check presence of browse-courses-button button
        self.assertIn('id="browse-courses-button"', html)
        # Check presence of my-courses-button button
        self.assertIn('id="my-courses-button"', html)
    def test_navigation_to_catalog(self):
        # From dashboard, simulate clicking browse-courses-button by requesting /catalog
        response = self.client.get('/catalog')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Available Courses</title>', html)
        # Check presence of catalog-page div
        self.assertIn('id="catalog-page"', html)
        # Check presence of search-input input
        self.assertIn('id="search-input"', html)
        # Check presence of course-grid div
        self.assertIn('id="course-grid"', html)
        # Check presence of back-to-dashboard button
        self.assertIn('id="back-to-dashboard"', html)
    def test_navigation_to_my_courses(self):
        # From dashboard, simulate clicking my-courses-button by requesting /my-courses
        response = self.client.get('/my-courses')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>My Courses</title>', html)
        # Check presence of my-courses-page div
        self.assertIn('id="my-courses-page"', html)
        # Check presence of courses-list div
        self.assertIn('id="courses-list"', html)
        # Check presence of back-to-dashboard button
        self.assertIn('id="back-to-dashboard"', html)
if __name__ == '__main__':
    unittest.main()