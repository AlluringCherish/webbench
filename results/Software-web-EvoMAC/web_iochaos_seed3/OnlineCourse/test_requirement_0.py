'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of ALL pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineCourseTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible_and_elements(self):
        # Test root '/' route accessible and loads Dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page container div id
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div missing")
        # Check welcome message h1 id and content includes 'Welcome'
        welcome_h1 = soup.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_h1, "Welcome message h1 missing")
        self.assertIn('Welcome', welcome_h1.text)
        # Check enrolled courses div id
        enrolled_div = soup.find('div', id='enrolled-courses')
        self.assertIsNotNone(enrolled_div, "Enrolled courses div missing")
        # Check buttons for browsing and my courses
        browse_btn = soup.find('button', id='browse-courses-button')
        self.assertIsNotNone(browse_btn, "Browse courses button missing")
        my_courses_btn = soup.find('button', id='my-courses-button')
        self.assertIsNotNone(my_courses_btn, "My courses button missing")
    def test_02_navigation_to_course_catalog(self):
        # Navigate from dashboard to course catalog page
        response = self.client.get('/catalog')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check catalog page container div id
        catalog_div = soup.find('div', id='catalog-page')
        self.assertIsNotNone(catalog_div, "Catalog page container div missing")
        # Check search input field id
        search_input = soup.find('input', id='search-input')
        self.assertIsNotNone(search_input, "Search input missing")
        # Check course grid div id
        course_grid = soup.find('div', id='course-grid')
        self.assertIsNotNone(course_grid, "Course grid div missing")
        # Check back to dashboard button
        back_btn = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button missing")
    def test_03_navigation_to_course_details(self):
        # Use example course_id '1' from example data
        response = self.client.get('/course/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check course details page container div id
        details_div = soup.find('div', id='course-details-page')
        self.assertIsNotNone(details_div, "Course details page container div missing")
        # Check course title h1 id
        course_title = soup.find('h1', id='course-title')
        self.assertIsNotNone(course_title, "Course title h1 missing")
        self.assertTrue(len(course_title.text.strip()) > 0, "Course title is empty")
        # Check course description div id
        course_desc = soup.find('div', id='course-description')
        self.assertIsNotNone(course_desc, "Course description div missing")
        # Check enroll button presence or disabled state
        enroll_btn = soup.find('button', id='enroll-button')
        self.assertIsNotNone(enroll_btn, "Enroll button missing")
        # Check back to catalog button
        back_btn = soup.find('button', id='back-to-catalog')
        self.assertIsNotNone(back_btn, "Back to catalog button missing")
    def test_04_navigation_to_my_courses(self):
        response = self.client.get('/my-courses')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check my courses page container div id
        my_courses_div = soup.find('div', id='my-courses-page')
        self.assertIsNotNone(my_courses_div, "My courses page container div missing")
        # Check courses list div id
        courses_list = soup.find('div', id='courses-list')
        self.assertIsNotNone(courses_list, "Courses list div missing")
        # Check back to dashboard button
        back_btn = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button missing")
    def test_05_navigation_to_course_learning(self):
        # Use course_id '1' which user 'john' is enrolled in example data
        response = self.client.get('/learning/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check learning page container div id
        learning_div = soup.find('div', id='learning-page')
        self.assertIsNotNone(learning_div, "Learning page container div missing")
        # Check lessons list div id
        lessons_list = soup.find('div', id='lessons-list')
        self.assertIsNotNone(lessons_list, "Lessons list div missing")
        # Check lesson content div id
        lesson_content = soup.find('div', id='lesson-content')
        self.assertIsNotNone(lesson_content, "Lesson content div missing")
        # Check mark complete button presence or course completed message
        mark_btn = soup.find('button', id='mark-complete-button')
        course_completed_msg = learning_div.find(string="Course Completed!")
        self.assertTrue(mark_btn is not None or course_completed_msg is not None,
                        "Neither mark complete button nor course completed message found")
        # Check back to my courses button
        back_btn = soup.find('button', id='back-to-my-courses')
        self.assertIsNotNone(back_btn, "Back to my courses button missing")
    def test_06_navigation_to_my_assignments(self):
        response = self.client.get('/assignments')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check assignments page container div id
        assignments_div = soup.find('div', id='assignments-page')
        self.assertIsNotNone(assignments_div, "Assignments page container div missing")
        # Check assignments table id
        assignments_table = soup.find('table', id='assignments-table')
        self.assertIsNotNone(assignments_table, "Assignments table missing")
        # Check back to dashboard button
        back_btn = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button missing")
    def test_07_navigation_to_submit_assignment_get(self):
        # Use assignment_id '1' from example data
        response = self.client.get('/assignments/submit/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check submit page container div id
        submit_div = soup.find('div', id='submit-page')
        self.assertIsNotNone(submit_div, "Submit assignment page container div missing")
        # Check assignment info div id
        assignment_info = soup.find('div', id='assignment-info')
        self.assertIsNotNone(assignment_info, "Assignment info div missing")
        # Check submission textarea id
        submission_textarea = soup.find('textarea', id='submission-text')
        self.assertIsNotNone(submission_textarea, "Submission textarea missing")
        # Check submit button id
        submit_btn = soup.find('button', id='submit-button')
        self.assertIsNotNone(submit_btn, "Submit button missing")
        # Check back to assignments button
        back_btn = soup.find('button', id='back-to-assignments')
        self.assertIsNotNone(back_btn, "Back to assignments button missing")
    def test_08_navigation_to_certificates(self):
        response = self.client.get('/certificates')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check certificates page container div id
        certs_div = soup.find('div', id='certificates-page')
        self.assertIsNotNone(certs_div, "Certificates page container div missing")
        # Check certificates grid div id
        certs_grid = soup.find('div', id='certificates-grid')
        self.assertIsNotNone(certs_grid, "Certificates grid div missing")
        # Check back to dashboard button
        back_btn = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button missing")
    def test_09_navigation_to_user_profile_get(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check profile page container div id
        profile_div = soup.find('div', id='profile-page')
        self.assertIsNotNone(profile_div, "Profile page container div missing")
        # Check email input id
        email_input = soup.find('input', id='profile-email')
        self.assertIsNotNone(email_input, "Profile email input missing")
        # Check fullname input id
        fullname_input = soup.find('input', id='profile-fullname')
        self.assertIsNotNone(fullname_input, "Profile fullname input missing")
        # Check update profile button id
        update_btn = soup.find('button', id='update-profile-button')
        self.assertIsNotNone(update_btn, "Update profile button missing")
        # Check back to dashboard button
        back_btn = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to dashboard button missing")
    def test_10_404_error_page(self):
        # Access a non-existent page to trigger 404
        response = self.client.get('/nonexistentpage')
        self.assertEqual(response.status_code, 404)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check that 404.html template is rendered by looking for a container div
        # Since 404.html is not provided, just check page has some content
        self.assertTrue(len(html) > 0, "404 page content missing")
if __name__ == '__main__':
    unittest.main()