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

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "featured-destinations").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "upcoming-trips").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-destinations-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "plan-itinerary-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-destinations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destinations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "destinations-page").is_displayed())

    # ===== Destinations Page Tests =====
    def test_destinations_page_elements(self):
        self.driver.find_element(By.ID, "browse-destinations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destinations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "destinations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-destination").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "region-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "destinations-grid").is_displayed())

    def test_destinations_page_functionality(self):
        self.driver.find_element(By.ID, "browse-destinations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destinations-page")))
        with open(f'{self.code_path}/data/destinations.txt', 'r') as f:
            destinations = f.readlines()
        self.assertTrue(len(destinations) > 0, "No destinations found in destinations.txt")
        destinations_grid = self.driver.find_element(By.ID, "destinations-grid").text
        first_dest_name = destinations[0].split('|')[1]
        self.assertIn(first_dest_name, destinations_grid, f"Expected destination '{first_dest_name}' not found")

    # ===== Destination Details Page Tests =====
    def test_destination_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-destinations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destinations-page")))
        self.driver.find_element(By.ID, "view-destination-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destination-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "destination-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "destination-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "destination-country").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "destination-description").is_displayed())

    def test_destination_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-destinations-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destinations-page")))
        with open(f'{self.code_path}/data/destinations.txt', 'r') as f:
            destinations = f.readlines()
        expected_name = destinations[0].split('|')[1]
        expected_country = destinations[0].split('|')[2]
        self.driver.find_element(By.ID, "view-destination-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "destination-details-page")))
        name = self.driver.find_element(By.ID, "destination-name").text
        country = self.driver.find_element(By.ID, "destination-country").text
        self.assertIn(expected_name, name, f"Expected destination name '{expected_name}' not found")
        self.assertIn(expected_country, country, f"Expected country '{expected_country}' not found")

    # ===== Itinerary Planning Page Tests =====
    def test_itinerary_page_elements(self):
        self.driver.find_element(By.ID, "plan-itinerary-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "itinerary-page")))
        self.assertTrue(self.driver.find_element(By.ID, "itinerary-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "itinerary-name-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "start-date-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "end-date-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-activity-button").is_displayed())

    def test_itinerary_page_functionality(self):
        self.driver.find_element(By.ID, "plan-itinerary-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "itinerary-page")))
        with open(f'{self.code_path}/data/itineraries.txt', 'r') as f:
            itineraries = f.readlines()
        itinerary_list = self.driver.find_element(By.ID, "itinerary-list").text
        if len(itineraries) > 0:
            first_itinerary_name = itineraries[0].split('|')[1]
            self.assertIn(first_itinerary_name, itinerary_list, f"Expected itinerary '{first_itinerary_name}' not found")

    # ===== Accommodations Page Tests =====
    def test_accommodations_page_elements(self):
        self.driver.get("http://localhost:5000/accommodations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "accommodations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "accommodations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "destination-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "check-in-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "check-out-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "price-filter").is_displayed())

    def test_accommodations_page_functionality(self):
        self.driver.get("http://localhost:5000/accommodations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "accommodations-page")))
        with open(f'{self.code_path}/data/hotels.txt', 'r') as f:
            hotels = f.readlines()
        self.assertTrue(len(hotels) > 0, "No hotels found in hotels.txt")
        hotels_list = self.driver.find_element(By.ID, "hotels-list").text
        first_hotel_name = hotels[0].split('|')[1]
        self.assertIn(first_hotel_name, hotels_list, f"Expected hotel '{first_hotel_name}' not found")

    # ===== Transportation Page Tests =====
    def test_transportation_page_elements(self):
        self.driver.get("http://localhost:5000/transportation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "transportation-page")))
        self.assertTrue(self.driver.find_element(By.ID, "transportation-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "departure-city").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "arrival-city").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "departure-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "flight-class-filter").is_displayed())

    def test_transportation_page_functionality(self):
        self.driver.get("http://localhost:5000/transportation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "transportation-page")))
        with open(f'{self.code_path}/data/flights.txt', 'r') as f:
            flights = f.readlines()
        self.assertTrue(len(flights) > 0, "No flights found in flights.txt")
        available_flights = self.driver.find_element(By.ID, "available-flights").text
        first_airline = flights[0].split('|')[1]
        self.assertIn(first_airline, available_flights, f"Expected airline '{first_airline}' not found")

    # ===== Travel Packages Page Tests =====
    def test_packages_page_elements(self):
        self.driver.get("http://localhost:5000/packages")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "packages-page")))
        self.assertTrue(self.driver.find_element(By.ID, "packages-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "packages-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "duration-filter").is_displayed())

    def test_packages_page_functionality(self):
        self.driver.get("http://localhost:5000/packages")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "packages-page")))
        with open(f'{self.code_path}/data/packages.txt', 'r') as f:
            packages = f.readlines()
        self.assertTrue(len(packages) > 0, "No packages found in packages.txt")
        packages_grid = self.driver.find_element(By.ID, "packages-grid").text
        first_package_name = packages[0].split('|')[1]
        self.assertIn(first_package_name, packages_grid, f"Expected package '{first_package_name}' not found")

    # ===== Trip Management Page Tests =====
    def test_trips_page_elements(self):
        self.driver.get("http://localhost:5000/trips")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trips-page")))
        self.assertTrue(self.driver.find_element(By.ID, "trips-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trips-table").is_displayed())

    def test_trips_page_functionality(self):
        self.driver.get("http://localhost:5000/trips")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trips-page")))
        with open(f'{self.code_path}/data/trips.txt', 'r') as f:
            trips = f.readlines()
        trips_table = self.driver.find_element(By.ID, "trips-table").text
        if len(trips) > 0:
            first_trip_name = trips[0].split('|')[1]
            self.assertIn(first_trip_name, trips_table, f"Expected trip '{first_trip_name}' not found")

    # ===== Booking Confirmation Page Tests =====
    def test_confirmation_page_elements(self):
        self.driver.get("http://localhost:5000/confirmation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-page")))
        self.assertTrue(self.driver.find_element(By.ID, "confirmation-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "confirmation-number").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "booking-details").is_displayed())

    def test_confirmation_page_functionality(self):
        self.driver.get("http://localhost:5000/confirmation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-page")))
        with open(f'{self.code_path}/data/bookings.txt', 'r') as f:
            bookings = f.readlines()
        confirmation_number = self.driver.find_element(By.ID, "confirmation-number").text
        self.assertTrue(len(confirmation_number) > 0, "Confirmation number is empty")
        if len(bookings) > 0:
            expected_conf_number = bookings[0].split('|')[5]
            self.assertIn(expected_conf_number, confirmation_number, f"Expected confirmation '{expected_conf_number}' not found")

    # ===== Travel Recommendations Page Tests =====
    def test_recommendations_page_elements(self):
        self.driver.get("http://localhost:5000/recommendations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "recommendations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "recommendations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-destinations").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "recommendation-season-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "budget-filter").is_displayed())

    def test_recommendations_page_functionality(self):
        self.driver.get("http://localhost:5000/recommendations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "recommendations-page")))
        with open(f'{self.code_path}/data/destinations.txt', 'r') as f:
            destinations = f.readlines()
        trending = self.driver.find_element(By.ID, "trending-destinations").text
        self.assertTrue(len(trending) > 0, "Trending destinations section is empty")
        if len(destinations) > 0:
            first_dest = destinations[0].split('|')[1]
            self.assertIn(first_dest, trending, f"Expected destination '{first_dest}' not found in trending")


class TestTravelPlanner:
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
        self.time = time

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
        result = {'total': 20, 'total_basic': 10, 'total_advanced': 10, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('TravelPlanner')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestTravelPlanner(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
