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
        self.code_path = 'data'

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "featured-vehicles").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-vehicles-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-reservations-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "promotions-section").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-page").is_displayed())

    # ===== Vehicle Search Page Tests =====
    def test_search_page_elements(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "vehicle-type-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "date-range-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "vehicles-grid").is_displayed())

    def test_search_page_functionality(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))

        # Verify vehicles from data file are displayed
        with open(f'{self.code_path}/vehicles.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "vehicles.txt file is empty")
            if len(lines) > 0:
                first_vehicle = lines[0].strip().split('|')
                if len(first_vehicle) > 2:
                    expected_model = first_vehicle[2]  # model is at index 2
                    vehicles_grid = self.driver.find_element(By.ID, "vehicles-grid").text
                    self.assertIn(expected_model, vehicles_grid, f"Vehicle model '{expected_model}' not found in grid")

    # ===== Vehicle Details Page Tests =====
    def test_vehicle_details_page_elements(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "vehicle-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "vehicle-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "vehicle-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "vehicle-specs").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "daily-rate").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-now-button").is_displayed())

    def test_vehicle_details_page_functionality(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "vehicle-details-page")))

        # Verify vehicle details match data file
        with open(f'{self.code_path}/vehicles.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # vehicle_id = 1
                    expected_make = parts[1]
                    expected_model = parts[2]
                    expected_rate = parts[4]

                    vehicle_name = self.driver.find_element(By.ID, "vehicle-name").text
                    daily_rate = self.driver.find_element(By.ID, "daily-rate").text

                    self.assertIn(expected_make, vehicle_name, f"Expected make '{expected_make}' not found")
                    self.assertIn(expected_model, vehicle_name, f"Expected model '{expected_model}' not found")
                    self.assertIn(expected_rate, daily_rate, f"Expected rate '{expected_rate}' not found")
                    break

    # ===== Booking Page Tests =====
    def test_booking_page_elements(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "vehicle-details-page")))
        self.driver.find_element(By.ID, "book-now-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "booking-page")))
        self.assertTrue(self.driver.find_element(By.ID, "booking-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pickup-location").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "dropoff-location").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pickup-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "dropoff-date").is_displayed())

    def test_booking_page_functionality(self):
        self.driver.find_element(By.ID, "search-vehicles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-details-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "vehicle-details-page")))
        self.driver.find_element(By.ID, "book-now-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "booking-page")))
        self.driver.find_element(By.ID, "pickup-date").send_keys("02/15/2025")
        date_value = self.driver.find_element(By.ID, "pickup-date").get_attribute("value")
        self.assertIsNotNone(date_value)

    # ===== Insurance Options Page Tests =====
    def test_insurance_page_elements(self):
        self.driver.get("http://localhost:5000/insurance")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "insurance-page")))
        self.assertTrue(self.driver.find_element(By.ID, "insurance-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "insurance-options").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "insurance-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "insurance-price").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "confirm-booking-button").is_displayed())

    def test_insurance_page_functionality(self):
        self.driver.get("http://localhost:5000/insurance")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "insurance-page")))

        # Verify insurance options from data file are displayed
        with open(f'{self.code_path}/insurance.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "insurance.txt file is empty")
            if len(lines) > 0:
                first_insurance = lines[0].strip().split('|')
                if len(first_insurance) > 1:
                    expected_plan = first_insurance[1]  # plan_name is at index 1
                    insurance_options = self.driver.find_element(By.ID, "insurance-options").text
                    self.assertIn(expected_plan, insurance_options, f"Insurance plan '{expected_plan}' not found")

    # ===== Rental History Page Tests =====
    def test_history_page_elements(self):
        self.driver.get("http://localhost:5000/history")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "history-page")))
        self.assertTrue(self.driver.find_element(By.ID, "history-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rentals-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "status-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_history_page_functionality(self):
        self.driver.get("http://localhost:5000/history")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "history-page")))

        # Verify rentals from data file are displayed
        with open(f'{self.code_path}/rentals.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "rentals.txt file is empty")
            if len(lines) > 0:
                first_rental = lines[0].strip().split('|')
                if len(first_rental) > 5:
                    expected_location = first_rental[5]  # pickup_location is at index 5
                    rentals_table = self.driver.find_element(By.ID, "rentals-table").text
                    self.assertIn(expected_location, rentals_table, f"Rental location '{expected_location}' not found")

    # ===== Reservations Management Page Tests =====
    def test_reservations_page_elements(self):
        self.driver.find_element(By.ID, "my-reservations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reservations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "reservations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "reservations-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "sort-by-date-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_reservations_page_functionality(self):
        self.driver.find_element(By.ID, "my-reservations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reservations-page")))

        # Verify reservations from data file are displayed
        with open(f'{self.code_path}/reservations.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "reservations.txt file is empty")
            if len(lines) > 0:
                first_reservation = lines[0].strip().split('|')
                if len(first_reservation) > 4:
                    expected_status = first_reservation[4]  # status is at index 4
                    reservations_list = self.driver.find_element(By.ID, "reservations-list").text
                    self.assertIn(expected_status, reservations_list, f"Reservation status '{expected_status}' not found")

    # ===== Special Requests Page Tests =====
    def test_requests_page_elements(self):
        self.driver.get("http://localhost:5000/special-requests")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "requests-page")))
        self.assertTrue(self.driver.find_element(By.ID, "requests-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-reservation").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "special-notes").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-requests-button").is_displayed())

    def test_requests_page_functionality(self):
        self.driver.get("http://localhost:5000/special-requests")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "requests-page")))
        self.driver.find_element(By.ID, "special-notes").send_keys("Please add GPS")
        notes_text = self.driver.find_element(By.ID, "special-notes").get_attribute("value")
        self.assertEqual(notes_text, "Please add GPS")

    # ===== Locations Page Tests =====
    def test_locations_page_elements(self):
        self.driver.get("http://localhost:5000/locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "locations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "locations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "locations-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "hours-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-location-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_locations_page_functionality(self):
        self.driver.get("http://localhost:5000/locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "locations-page")))

        # Verify locations from data file are displayed
        with open(f'{self.code_path}/locations.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "locations.txt file is empty")
            if len(lines) > 0:
                first_location = lines[0].strip().split('|')
                if len(first_location) > 1:
                    expected_city = first_location[1]  # city is at index 1
                    locations_list = self.driver.find_element(By.ID, "locations-list").text
                    self.assertIn(expected_city, locations_list, f"Location city '{expected_city}' not found")


class TestCarRental:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('CarRental')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestCarRental(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
