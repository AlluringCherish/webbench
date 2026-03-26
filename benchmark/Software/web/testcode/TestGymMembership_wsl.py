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
    @classmethod
    def setUpClass(cls):
        """Set up code path for data file access."""
        cls.code_path = 'data'

    def setUp(self):
        """Set up the Selenium WebDriver before each test (WSL headless mode)."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        prefs = {"profile.password_manager_leak_detection": False}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "member-welcome").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-membership-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-schedule-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-trainer-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-membership-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "membership-page")))
        self.assertTrue(self.driver.find_element(By.ID, "membership-page").is_displayed())

    # ===== Membership Plans Page Tests =====
    def test_membership_page_elements(self):
        self.driver.find_element(By.ID, "browse-membership-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "membership-page")))
        self.assertTrue(self.driver.find_element(By.ID, "membership-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plan-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plans-grid").is_displayed())

    def test_membership_page_functionality(self):
        self.driver.find_element(By.ID, "browse-membership-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "membership-page")))
        plans_grid = self.driver.find_element(By.ID, "plans-grid").text
        # Verify data from memberships.txt is displayed
        with open(f'{self.code_path}/memberships.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "memberships.txt is empty")
            # Check first plan name appears in grid
            first_plan = lines[0].split('|')
            plan_name = first_plan[1]
            self.assertIn(plan_name, plans_grid)

    # ===== Plan Details Page Tests =====
    def test_plan_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-membership-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "membership-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "plan-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "plan-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plan-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plan-price").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plan-features").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "enroll-plan-button").is_displayed())

    def test_plan_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-membership-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "membership-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "plan-details-page")))
        # Verify plan details match data file
        with open(f'{self.code_path}/memberships.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "memberships.txt is empty")
            expected_data = first_line.split('|')
            expected_title = expected_data[1]
            expected_price = expected_data[2]
            title = self.driver.find_element(By.ID, "plan-title").text
            price = self.driver.find_element(By.ID, "plan-price").text
            self.assertIn(expected_title, title)
            self.assertIn(expected_price, price)

    # ===== Class Schedule Page Tests =====
    def test_schedule_page_elements(self):
        self.driver.find_element(By.ID, "view-schedule-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "schedule-page")))
        self.assertTrue(self.driver.find_element(By.ID, "schedule-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedule-search").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedule-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "classes-grid").is_displayed())

    def test_schedule_page_functionality(self):
        self.driver.find_element(By.ID, "view-schedule-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "schedule-page")))
        classes_grid = self.driver.find_element(By.ID, "classes-grid").text
        # Verify classes from data file are displayed
        with open(f'{self.code_path}/classes.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "classes.txt is empty")
            first_class = lines[0].split('|')
            class_name = first_class[1]
            self.assertIn(class_name, classes_grid)

    # ===== Trainer Profiles Page Tests =====
    def test_trainers_page_elements(self):
        self.driver.get("http://localhost:5000/trainers")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainers-page")))
        self.assertTrue(self.driver.find_element(By.ID, "trainers-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trainer-search").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "specialty-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trainers-grid").is_displayed())

    def test_trainers_page_functionality(self):
        self.driver.get("http://localhost:5000/trainers")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainers-page")))
        trainers_grid = self.driver.find_element(By.ID, "trainers-grid").text
        # Verify trainers from data file are displayed
        with open(f'{self.code_path}/trainers.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "trainers.txt is empty")
            first_trainer = lines[0].split('|')
            trainer_name = first_trainer[1]
            self.assertIn(trainer_name, trainers_grid)

    # ===== Trainer Detail Page Tests =====
    def test_trainer_detail_page_elements(self):
        self.driver.get("http://localhost:5000/trainers")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainers-page")))
        self.driver.find_element(By.ID, "view-trainer-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainer-detail-page")))
        self.assertTrue(self.driver.find_element(By.ID, "trainer-detail-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trainer-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trainer-bio").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trainer-certifications").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-session-button").is_displayed())

    def test_trainer_detail_page_functionality(self):
        self.driver.get("http://localhost:5000/trainers")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainers-page")))
        self.driver.find_element(By.ID, "view-trainer-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trainer-detail-page")))
        # Verify trainer details match data file
        with open(f'{self.code_path}/trainers.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "trainers.txt is empty")
            expected_data = first_line.split('|')
            expected_name = expected_data[1]
            name = self.driver.find_element(By.ID, "trainer-name").text
            self.assertIn(expected_name, name)

    # ===== PT Booking Page Tests =====
    def test_booking_page_elements(self):
        self.driver.find_element(By.ID, "book-trainer-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "booking-page")))
        self.assertTrue(self.driver.find_element(By.ID, "booking-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-trainer").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "session-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "session-time").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "session-duration").is_displayed())

    def test_booking_page_functionality(self):
        self.driver.find_element(By.ID, "book-trainer-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "booking-page")))
        # Verify trainer dropdown has options from data file
        with open(f'{self.code_path}/trainers.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "trainers.txt is empty")
        trainer_dropdown = Select(self.driver.find_element(By.ID, "select-trainer"))
        options = trainer_dropdown.options
        self.assertGreater(len(options), 0, "Trainer dropdown has no options")

    # ===== Workout Records Page Tests =====
    def test_workouts_page_elements(self):
        self.driver.get("http://localhost:5000/workouts")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "workouts-page")))
        self.assertTrue(self.driver.find_element(By.ID, "workouts-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "workouts-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-by-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_workouts_page_functionality(self):
        self.driver.get("http://localhost:5000/workouts")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "workouts-page")))
        workouts_table = self.driver.find_element(By.ID, "workouts-table").text
        # Verify workouts from data file are displayed
        with open(f'{self.code_path}/workouts.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_workout = lines[0].split('|')
                workout_type = first_workout[2]
                self.assertIn(workout_type, workouts_table)

    # ===== Log Workout Page Tests =====
    def test_log_workout_page_elements(self):
        self.driver.get("http://localhost:5000/log-workout")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "log-workout-page")))
        self.assertTrue(self.driver.find_element(By.ID, "log-workout-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "workout-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "workout-duration").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "calories-burned").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "workout-notes").is_displayed())

    def test_log_workout_page_functionality(self):
        self.driver.get("http://localhost:5000/log-workout")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "log-workout-page")))
        self.driver.find_element(By.ID, "workout-notes").send_keys("Great workout session!")
        workout_notes = self.driver.find_element(By.ID, "workout-notes").get_attribute("value")
        self.assertEqual(workout_notes, "Great workout session!")


class TestGymMembership:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')
        self.pid = get_python_pid()
        self.py = path
        self.code_path = code_path

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
        result = {'total': 18, 'total_basic': 9, 'total_advanced': 9, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
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
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 1
            for test in res['fail']:
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 0

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
        pattern = os.path.join(base_dir, 'no_login_web', f'{app_name}', 'app.py')
        if os.path.exists(pattern):
            return pattern
        return None

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('GymMembership')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestGymMembership(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
