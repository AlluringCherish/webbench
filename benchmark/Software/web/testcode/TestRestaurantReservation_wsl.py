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
        self.assertTrue(self.driver.find_element(By.ID, "make-reservation-button").is_displayed())

    def test_dashboard_page_functionality(self):
        welcome = self.driver.find_element(By.ID, "welcome-message").text
        self.assertTrue(len(welcome) > 0, "Welcome message is empty")

    def test_menu_page_elements(self):
        self.driver.find_element(By.ID, "view-menu-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        self.assertTrue(self.driver.find_element(By.ID, "menu-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_menu_page_functionality(self):
        self.driver.find_element(By.ID, "view-menu-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/menu.txt', 'r') as f:
            menu_items = f.readlines()
        self.assertTrue(len(menu_items) > 0, "menu.txt is empty")
        menu_grid = self.driver.find_element(By.ID, "menu-grid").text
        first_dish_name = menu_items[0].split('|')[1]
        self.assertIn(first_dish_name, menu_grid, f"Expected dish '{first_dish_name}' not found in menu grid")

    def test_dish_details_page_elements(self):
        self.driver.find_element(By.ID, "view-menu-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        self.driver.find_element(By.ID, "view-dish-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dish-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "dish-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "dish-price").is_displayed())

    def test_dish_details_page_functionality(self):
        self.driver.find_element(By.ID, "view-menu-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/menu.txt', 'r') as f:
            menu_items = f.readlines()
        expected_dish_name = menu_items[0].split('|')[1]
        expected_dish_price = menu_items[0].split('|')[3]
        self.driver.find_element(By.ID, "view-dish-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dish-details-page")))
        dish_name = self.driver.find_element(By.ID, "dish-name").text
        dish_price = self.driver.find_element(By.ID, "dish-price").text
        self.assertIn(expected_dish_name, dish_name, f"Expected dish name '{expected_dish_name}' not found")
        self.assertIn(expected_dish_price, dish_price, f"Expected price '{expected_dish_price}' not found")

    def test_reservation_page_elements(self):
        self.driver.find_element(By.ID, "make-reservation-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reservation-page")))
        self.assertTrue(self.driver.find_element(By.ID, "guest-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "party-size").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "reservation-date").is_displayed())

    def test_reservation_page_functionality(self):
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/reservations.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "make-reservation-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reservation-page")))
        test_guest_name = f"TestGuest{int(time.time())}"
        self.driver.find_element(By.ID, "guest-name").send_keys(test_guest_name)
        self.driver.find_element(By.ID, "reservation-date").send_keys("2025-12-01")
        Select(self.driver.find_element(By.ID, "party-size")).select_by_value("4")
        self.driver.find_element(By.ID, "submit-reservation-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        time.sleep(0.5)
        with open(f'{code_path}/data/reservations.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count, "Reservation was not added to file")

    def test_my_reservations_page_elements(self):
        self.driver.find_element(By.ID, "my-reservations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-reservations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "reservations-table").is_displayed())

    def test_my_reservations_page_functionality(self):
        self.driver.find_element(By.ID, "my-reservations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-reservations-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/reservations.txt', 'r') as f:
            reservations = f.readlines()
        self.assertTrue(len(reservations) > 0, "No reservations found in reservations.txt")
        table = self.driver.find_element(By.ID, "reservations-table").text
        first_guest_name = reservations[0].split('|')[2]
        self.assertIn(first_guest_name, table, f"Expected guest name '{first_guest_name}' not found in table")

    def test_waitlist_page_elements(self):
        self.driver.find_element(By.ID, "waitlist-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "waitlist-page")))
        self.assertTrue(self.driver.find_element(By.ID, "waitlist-party-size").is_displayed())

    def test_waitlist_page_functionality(self):
        self.driver.find_element(By.ID, "waitlist-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "waitlist-page")))
        Select(self.driver.find_element(By.ID, "waitlist-party-size")).select_by_value("2")
        self.driver.find_element(By.ID, "join-waitlist-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "user-position")))

    def test_reviews_page_elements(self):
        self.driver.find_element(By.ID, "my-reviews-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        self.assertTrue(self.driver.find_element(By.ID, "reviews-list").is_displayed())

    def test_reviews_page_functionality(self):
        self.driver.find_element(By.ID, "my-reviews-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/reviews.txt', 'r') as f:
            reviews_data = f.readlines()
        reviews = self.driver.find_element(By.ID, "reviews-list").text
        if len(reviews_data) > 0:
            first_review_text = reviews_data[0].split('|')[4]
            self.assertIn(first_review_text, reviews, f"Expected review text '{first_review_text}' not found")

    def test_write_review_page_elements(self):
        self.driver.find_element(By.ID, "my-reviews-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        self.driver.find_element(By.ID, "write-new-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.assertTrue(self.driver.find_element(By.ID, "select-dish").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rating-input").is_displayed())

    def test_write_review_page_functionality(self):
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/reviews.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "my-reviews-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        self.driver.find_element(By.ID, "write-new-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        Select(self.driver.find_element(By.ID, "select-dish")).select_by_index(1)
        Select(self.driver.find_element(By.ID, "rating-input")).select_by_value("5")
        test_review = f"Great food! TestReview{int(time.time())}"
        self.driver.find_element(By.ID, "review-text").send_keys(test_review)
        self.driver.find_element(By.ID, "submit-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        time.sleep(0.5)
        with open(f'{code_path}/data/reviews.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count, "Review was not added to file")

    def test_profile_page_elements(self):
        self.driver.find_element(By.ID, "profile-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        self.assertTrue(self.driver.find_element(By.ID, "profile-username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "profile-email").is_displayed())

    def test_profile_page_functionality(self):
        self.driver.find_element(By.ID, "profile-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/users.txt', 'r') as f:
            users = f.readlines()
        self.assertTrue(len(users) > 0, "No users found in users.txt")
        expected_username = users[0].split('|')[0]
        username = self.driver.find_element(By.ID, "profile-username").text
        self.assertIn(expected_username, username, f"Expected username '{expected_username}' not found")


class TestRestaurantReservation:
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
        print(f"Searching for RestaurantReservation app.py...")
        py = find_app_py('RestaurantReservation')
        if py is None:
            print("=" * 70)
            print("ERROR: Could not find app.py")
            print("=" * 70)
            sys.exit(1)
        print(f"Found: {py}")

    if not os.path.exists(py):
        print(f"ERROR: File not found: {py}")
        sys.exit(1)

    test = TestRestaurantReservation(None, py)
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
    print(f"Total: {result['basic'] + result['advanced']}/{result['total']}")
