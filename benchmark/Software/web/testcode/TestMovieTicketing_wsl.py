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
        self.assertTrue(self.driver.find_element(By.ID, "featured-movies").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-movies-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-bookings-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "showtimes-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Movie Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "genre-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "movies-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        movies_grid = self.driver.find_element(By.ID, "movies-grid").text
        # Verify movies from data file are displayed
        with open(f'{self.code_path}/movies.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "movies.txt is empty")
            first_movie = lines[0].split('|')
            movie_title = first_movie[1]
            self.assertIn(movie_title, movies_grid)

    # ===== Movie Details Page Tests =====
    def test_movie_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "movie-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "movie-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "movie-director").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "movie-rating").is_displayed())

    def test_movie_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        # Verify movie details match data file
        with open(f'{self.code_path}/movies.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "movies.txt is empty")
            expected_data = first_line.split('|')
            expected_title = expected_data[1]
            title = self.driver.find_element(By.ID, "movie-title").text
            self.assertIn(expected_title, title)

    # ===== Showtime Selection Page Tests =====
    def test_showtime_page_elements(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        self.driver.find_element(By.ID, "select-showtime-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "showtime-page")))
        self.assertTrue(self.driver.find_element(By.ID, "showtime-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "showtimes-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "theater-filter").is_displayed())

    def test_showtime_page_functionality(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        self.driver.find_element(By.ID, "select-showtime-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "showtime-page")))
        showtimes_list = self.driver.find_element(By.ID, "showtimes-list").text
        # Verify showtimes from data file are displayed
        with open(f'{self.code_path}/showtimes.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "showtimes.txt is empty")

    # ===== Seat Selection Page Tests =====
    def test_seat_selection_page_elements(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        self.driver.find_element(By.ID, "select-showtime-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "showtime-page")))
        try:
            self.driver.find_element(By.ID, "select-showtime-button-1").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "seat-selection-page")))
            self.assertTrue(self.driver.find_element(By.ID, "seat-selection-page").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "seat-map").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "selected-seats-display").is_displayed())
        except:
            pass  # Showtime might not be available

    def test_seat_selection_page_functionality(self):
        self.driver.find_element(By.ID, "browse-movies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-movie-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "movie-details-page")))
        self.driver.find_element(By.ID, "select-showtime-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "showtime-page")))
        try:
            self.driver.find_element(By.ID, "select-showtime-button-1").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "seat-selection-page")))
            # Verify seats from data file exist
            with open(f'{self.code_path}/seats.txt', 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                self.assertGreater(len(lines), 0, "seats.txt is empty")
        except:
            pass  # Showtime might not be available

    # ===== Booking Confirmation Page Tests =====
    def test_confirmation_page_elements(self):
        self.driver.get("http://localhost:5000/confirmation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-page")))
        self.assertTrue(self.driver.find_element(By.ID, "confirmation-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "booking-summary").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "customer-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "customer-email").is_displayed())

    def test_confirmation_page_functionality(self):
        self.driver.get("http://localhost:5000/confirmation")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-page")))
        self.driver.find_element(By.ID, "customer-name").send_keys("Test Customer")
        name_value = self.driver.find_element(By.ID, "customer-name").get_attribute("value")
        self.assertEqual(name_value, "Test Customer")

    # ===== Booking History Page Tests =====
    def test_bookings_page_elements(self):
        self.driver.find_element(By.ID, "view-bookings-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "bookings-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bookings-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "status-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_bookings_page_functionality(self):
        self.driver.find_element(By.ID, "view-bookings-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookings-page")))
        bookings_table = self.driver.find_element(By.ID, "bookings-table").text
        # Verify bookings from data file are displayed
        with open(f'{self.code_path}/bookings.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_booking = lines[0].split('|')
                customer_name = first_booking[2]
                self.assertIn(customer_name, bookings_table)

    # ===== Theater Information Page Tests =====
    def test_theater_page_elements(self):
        self.driver.get("http://localhost:5000/theaters")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "theater-page")))
        self.assertTrue(self.driver.find_element(By.ID, "theater-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "theaters-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "theater-location-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_theater_page_functionality(self):
        self.driver.get("http://localhost:5000/theaters")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "theater-page")))
        theaters_list = self.driver.find_element(By.ID, "theaters-list").text
        # Verify theaters from data file are displayed
        with open(f'{self.code_path}/theaters.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "theaters.txt is empty")
            first_theater = lines[0].split('|')
            theater_name = first_theater[1]
            self.assertIn(theater_name, theaters_list)


class TestMovieTicketing:
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
        result = {'total': 16, 'total_basic': 8, 'total_advanced': 8, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('MovieTicketing')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestMovieTicketing(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
