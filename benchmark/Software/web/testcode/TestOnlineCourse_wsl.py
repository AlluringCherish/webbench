import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_test import CustomTestRunner
from utils_win import get_python_pid


class TestCase(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        prefs = {"profile.password_manager_leak_detection": False}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))

    def tearDown(self):
        self.driver.quit()

    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "welcome-message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-courses-button").is_displayed())

    def test_dashboard_page_functionality(self):
        welcome = self.driver.find_element(By.ID, "welcome-message").text
        self.assertTrue(len(welcome) > 0)
        # Verify enrolled courses are displayed
        enrolled_courses = self.driver.find_element(By.ID, "enrolled-courses").text
        with open('data/enrollments.txt', 'r') as f:
            enrollments = f.readlines()
        if len(enrollments) > 0:
            self.assertTrue(len(enrolled_courses) > 0)

    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "course-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        # Verify courses from courses.txt are displayed
        with open('data/courses.txt', 'r') as f:
            courses_data = f.readlines()
        self.assertTrue(len(courses_data) > 0, "courses.txt is empty")
        first_course = courses_data[0].strip().split('|')
        course_title = first_course[1]
        courses = self.driver.find_element(By.ID, "course-grid").text
        self.assertIn(course_title, courses)

    def test_course_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-course-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "course-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "course-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "enroll-button").is_displayed())

    def test_course_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-course-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "course-details-page")))
        # Verify course title matches data
        with open('data/courses.txt', 'r') as f:
            courses = f.readlines()
        first_course = courses[0].strip().split('|')
        expected_title = first_course[1]
        title = self.driver.find_element(By.ID, "course-title").text
        self.assertEqual(title, expected_title)

    def test_my_courses_page_elements(self):
        self.driver.find_element(By.ID, "my-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-courses-page")))
        self.assertTrue(self.driver.find_element(By.ID, "courses-list").is_displayed())

    def test_my_courses_page_functionality(self):
        self.driver.find_element(By.ID, "my-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-courses-page")))
        # Verify enrolled courses match enrollments.txt
        with open('data/enrollments.txt', 'r') as f:
            enrollments = f.readlines()
        courses_list = self.driver.find_element(By.ID, "courses-list").text
        if len(enrollments) > 0:
            # Get first enrollment's course
            first_enrollment = enrollments[0].strip().split('|')
            course_id = first_enrollment[2]
            with open('data/courses.txt', 'r') as f:
                courses = f.readlines()
            for course in courses:
                if course.startswith(f"{course_id}|"):
                    course_title = course.strip().split('|')[1]
                    self.assertIn(course_title, courses_list)
                    break
        else:
            self.assertIsNotNone(courses_list)

    def test_learning_page_elements(self):
        self.driver.find_element(By.ID, "my-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-courses-page")))
        self.driver.find_element(By.ID, "continue-learning-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "learning-page")))
        self.assertTrue(self.driver.find_element(By.ID, "lessons-list").is_displayed())

    def test_learning_page_functionality(self):
        self.driver.find_element(By.ID, "my-courses-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-courses-page")))
        self.driver.find_element(By.ID, "continue-learning-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "learning-page")))
        lessons = self.driver.find_element(By.ID, "lessons-list").text
        self.assertTrue(len(lessons) > 0)
        # Verify lesson content is displayed
        lesson_content = self.driver.find_element(By.ID, "lesson-content").text
        self.assertTrue(len(lesson_content) > 0)

    def test_assignments_page_elements(self):
        self.driver.get("http://localhost:5000/assignments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "assignments-page")))
        self.assertTrue(self.driver.find_element(By.ID, "assignments-table").is_displayed())

    def test_assignments_page_functionality(self):
        self.driver.get("http://localhost:5000/assignments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "assignments-page")))
        # Verify assignments from assignments.txt are displayed
        with open('data/assignments.txt', 'r') as f:
            assignments = f.readlines()
        if len(assignments) > 0:
            first_assignment = assignments[0].strip().split('|')
            assignment_title = first_assignment[2]
            table = self.driver.find_element(By.ID, "assignments-table").text
            self.assertIn(assignment_title, table)
        else:
            table = self.driver.find_element(By.ID, "assignments-table").text
            self.assertIsNotNone(table)

    def test_submit_page_elements(self):
        self.driver.get("http://localhost:5000/assignments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "assignments-page")))
        self.driver.find_element(By.ID, "submit-assignment-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "submit-page")))
        self.assertTrue(self.driver.find_element(By.ID, "submission-text").is_displayed())

    def test_submit_page_functionality(self):
        self.driver.get("http://localhost:5000/assignments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "assignments-page")))
        self.driver.find_element(By.ID, "submit-assignment-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "submit-page")))
        # Count submissions before
        with open('data/submissions.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "submission-text").send_keys("My submission")
        self.driver.find_element(By.ID, "submit-button").click()
        time.sleep(1)
        # Verify submission was added
        with open('data/submissions.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count)

    def test_certificates_page_elements(self):
        self.driver.get("http://localhost:5000/certificates")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "certificates-page")))
        self.assertTrue(self.driver.find_element(By.ID, "certificates-grid").is_displayed())

    def test_certificates_page_functionality(self):
        self.driver.get("http://localhost:5000/certificates")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "certificates-page")))
        # Verify certificates from certificates.txt are displayed
        with open('data/certificates.txt', 'r') as f:
            certificates = f.readlines()
        certs_grid = self.driver.find_element(By.ID, "certificates-grid").text
        if len(certificates) > 0:
            # Verify certificate course appears in grid
            first_cert = certificates[0].strip().split('|')
            course_id = first_cert[2]
            with open('data/courses.txt', 'r') as f:
                courses = f.readlines()
            for course in courses:
                if course.startswith(f"{course_id}|"):
                    course_title = course.strip().split('|')[1]
                    self.assertIn(course_title, certs_grid)
                    break
        else:
            self.assertIsNotNone(certs_grid)

    def test_profile_page_elements(self):
        self.driver.get("http://localhost:5000/profile")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        self.assertTrue(self.driver.find_element(By.ID, "profile-email").is_displayed())

    def test_profile_page_functionality(self):
        self.driver.get("http://localhost:5000/profile")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        # Verify email from users.txt
        with open('data/users.txt', 'r') as f:
            users = f.readlines()
        if len(users) > 0:
            first_user = users[0].strip().split('|')
            expected_email = first_user[1]
            email = self.driver.find_element(By.ID, "profile-email").get_attribute("value")
            self.assertEqual(email, expected_email)
        else:
            email = self.driver.find_element(By.ID, "profile-email").get_attribute("value")
            self.assertIsNotNone(email)


class TestOnlineCourse:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')
        self.checker = checker
        self.time = time
        self.py = path
        self.pid = get_python_pid()

    def test_set_up(self):
        try:
            self.process = subprocess.Popen(['python', self.py])
            time.sleep(2)
            return 1
        except:
            return 0

    def tear_down(self):
        if os.path.exists('data'):
            shutil.rmtree('data')
        self.process.terminate()

    def main(self):
        result = {
            'total': 18,
            'total_basic': 9,
            'total_advanced': 9,
            'basic': 0,
            'advanced': 0,
            'test_cases': {'set_up': 0}
        }
        res = None

        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except Exception as e:
            print(f"ERROR during setup: {e}")
            self.tear_down()
            return result

        if result['test_cases']['set_up'] == 1:
            try:
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except Exception as e:
                print(f"ERROR during test execution: {e}")
                self.tear_down()
                return result
        else:
            print("Setup failed, skipping tests")
            self.tear_down()
            return result

        self.tear_down()

        if res is not None:
            for test in res['succ']:
                test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
                result['test_cases'][test_cases] = 1
            for test in res['fail']:
                test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
                result['test_cases'][test_cases] = 0

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]
        return result


if __name__ == '__main__':
    import glob

    def find_app_py(app_name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pattern = os.path.join(base_dir, f'{app_name}_*')
        matching_dirs = glob.glob(pattern)
        if not matching_dirs:
            return None
        matching_dirs.sort(key=os.path.getmtime, reverse=True)
        for dir_path in matching_dirs:
            app_py_path = os.path.join(dir_path, 'app.py')
            if os.path.exists(app_py_path):
                return app_py_path
        return None

    if len(sys.argv) > 1:
        py = sys.argv[1]
    else:
        py = find_app_py('OnlineCourse')
        if py is None:
            print("ERROR: Could not find app.py")
            sys.exit(1)

    test = TestOnlineCourse(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
