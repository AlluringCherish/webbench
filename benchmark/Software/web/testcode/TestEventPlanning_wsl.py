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
        self.assertTrue(self.driver.find_element(By.ID, "featured-events").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-events-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-tickets-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "venues-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "events-page")))
        self.assertTrue(self.driver.find_element(By.ID, "events-page").is_displayed())

    # ===== Events Listing Page Tests =====
    def test_events_page_elements(self):
        self.driver.find_element(By.ID, "browse-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "events-page")))
        self.assertTrue(self.driver.find_element(By.ID, "events-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-category-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "events-grid").is_displayed())

    def test_events_page_functionality(self):
        self.driver.find_element(By.ID, "browse-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "events-page")))

        # Verify events from data file are displayed
        with open(f'{self.code_path}/events.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "events.txt file is empty")
            if len(lines) > 0:
                first_event = lines[0].strip().split('|')
                if len(first_event) > 1:
                    expected_event_name = first_event[1]  # event_name is at index 1
                    events_grid = self.driver.find_element(By.ID, "events-grid").text
                    self.assertIn(expected_event_name, events_grid, f"Event name '{expected_event_name}' not found in grid")

    # ===== Event Details Page Tests =====
    def test_event_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "events-page")))
        self.driver.find_element(By.ID, "view-event-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "event-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "event-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-location").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-ticket-button").is_displayed())

    def test_event_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "events-page")))
        self.driver.find_element(By.ID, "view-event-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "event-details-page")))

        # Verify event details match data file
        with open(f'{self.code_path}/events.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # event_id = 1
                    expected_name = parts[1]
                    expected_date = parts[3]
                    expected_location = parts[5]

                    title = self.driver.find_element(By.ID, "event-title").text
                    date = self.driver.find_element(By.ID, "event-date").text
                    location = self.driver.find_element(By.ID, "event-location").text

                    self.assertIn(expected_name, title, f"Expected event name '{expected_name}' not found")
                    self.assertIn(expected_date, date, f"Expected date '{expected_date}' not found")
                    self.assertIn(expected_location, location, f"Expected location '{expected_location}' not found")
                    break

    # ===== Ticket Booking Page Tests =====
    def test_ticket_booking_page_elements(self):
        self.driver.find_element(By.ID, "view-tickets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ticket-booking-page")))
        self.assertTrue(self.driver.find_element(By.ID, "ticket-booking-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-event-dropdown").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "ticket-quantity-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "ticket-type-select").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-now-button").is_displayed())

    def test_ticket_booking_page_functionality(self):
        self.driver.find_element(By.ID, "view-tickets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ticket-booking-page")))
        self.driver.find_element(By.ID, "ticket-quantity-input").send_keys("2")
        quantity = self.driver.find_element(By.ID, "ticket-quantity-input").get_attribute("value")
        self.assertEqual(quantity, "2")

    # ===== Participants Management Page Tests =====
    def test_participants_page_elements(self):
        self.driver.get("http://localhost:5000/participants")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "participants-page")))
        self.assertTrue(self.driver.find_element(By.ID, "participants-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "participants-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-participant-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-participant-input").is_displayed())

    def test_participants_page_functionality(self):
        self.driver.get("http://localhost:5000/participants")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "participants-page")))

        # Verify participants from data file are displayed
        with open(f'{self.code_path}/participants.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "participants.txt file is empty")
            if len(lines) > 0:
                first_participant = lines[0].strip().split('|')
                if len(first_participant) > 2:
                    expected_name = first_participant[2]  # name is at index 2
                    participants_table = self.driver.find_element(By.ID, "participants-table").text
                    self.assertIn(expected_name, participants_table, f"Participant name '{expected_name}' not found")

    # ===== Venue Information Page Tests =====
    def test_venues_page_elements(self):
        self.driver.find_element(By.ID, "venues-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "venues-page")))
        self.assertTrue(self.driver.find_element(By.ID, "venues-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "venues-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "venue-search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "venue-capacity-filter").is_displayed())

    def test_venues_page_functionality(self):
        self.driver.find_element(By.ID, "venues-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "venues-page")))

        # Verify venues from data file are displayed
        with open(f'{self.code_path}/venues.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "venues.txt file is empty")
            if len(lines) > 0:
                first_venue = lines[0].strip().split('|')
                if len(first_venue) > 1:
                    expected_venue_name = first_venue[1]  # venue_name is at index 1
                    venues_grid = self.driver.find_element(By.ID, "venues-grid").text
                    self.assertIn(expected_venue_name, venues_grid, f"Venue name '{expected_venue_name}' not found")

    # ===== Event Schedules Page Tests =====
    def test_schedules_page_elements(self):
        self.driver.get("http://localhost:5000/schedules")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "schedules-page")))
        self.assertTrue(self.driver.find_element(By.ID, "schedules-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedules-timeline").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedule-filter-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedule-filter-event").is_displayed())

    def test_schedules_page_functionality(self):
        self.driver.get("http://localhost:5000/schedules")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "schedules-page")))

        # Verify schedules from data file are displayed
        with open(f'{self.code_path}/schedules.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "schedules.txt file is empty")
            if len(lines) > 0:
                first_schedule = lines[0].strip().split('|')
                if len(first_schedule) > 2:
                    expected_session = first_schedule[2]  # session_title is at index 2
                    timeline = self.driver.find_element(By.ID, "schedules-timeline").text
                    self.assertIn(expected_session, timeline, f"Session title '{expected_session}' not found")

    # ===== Bookings Summary Page Tests =====
    def test_bookings_page_elements(self):
        self.driver.get("http://localhost:5000/bookings")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "bookings-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bookings-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "booking-search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_bookings_page_functionality(self):
        self.driver.get("http://localhost:5000/bookings")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookings-page")))

        # Verify bookings from data file are displayed
        with open(f'{self.code_path}/bookings.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "bookings.txt file is empty")
            if len(lines) > 0:
                first_booking = lines[0].strip().split('|')
                if len(first_booking) > 2:
                    expected_customer = first_booking[2]  # customer_name is at index 2
                    bookings_table = self.driver.find_element(By.ID, "bookings-table").text
                    self.assertIn(expected_customer, bookings_table, f"Customer name '{expected_customer}' not found")


class TestEventPlanning:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('EventPlanning')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestEventPlanning(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
