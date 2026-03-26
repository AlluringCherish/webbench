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
from datetime import datetime

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
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-summary").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "artifact-catalog-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibitions-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "visitor-tickets-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "virtual-events-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "audio-guides-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.driver.find_element(By.ID, "artifact-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "artifact-catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "artifact-catalog-page").is_displayed())

    # ===== Artifact Catalog Page Tests =====
    def test_artifact_catalog_page_elements(self):
        self.driver.find_element(By.ID, "artifact-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "artifact-catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "artifact-catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "artifact-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-artifact").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-artifact-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_artifact_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "artifact-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "artifact-catalog-page")))
        with open(f'{self.code_path}/data/artifacts.txt', 'r') as f:
            artifacts = f.readlines()
        self.assertTrue(len(artifacts) > 0, "artifacts.txt is empty")
        artifact_table = self.driver.find_element(By.ID, "artifact-table").text
        first_artifact = artifacts[0].split("|")[1]
        self.assertIn(first_artifact, artifact_table, f"Expected artifact '{first_artifact}' not found in table")

    # ===== Exhibitions Page Tests =====
    def test_exhibitions_page_elements(self):
        self.driver.find_element(By.ID, "exhibitions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibitions-page")))
        self.assertTrue(self.driver.find_element(By.ID, "exhibitions-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-exhibition-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-exhibition-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-exhibition-button-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_exhibitions_page_functionality(self):
        self.driver.find_element(By.ID, "exhibitions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibitions-page")))
        with open(f'{self.code_path}/data/exhibitions.txt', 'r') as f:
            exhibitions = f.readlines()
        self.assertTrue(len(exhibitions) > 0, "exhibitions.txt is empty")
        exhibition_list = self.driver.find_element(By.ID, "exhibition-list").text
        first_exhibition = exhibitions[0].split("|")[1]
        self.assertIn(first_exhibition, exhibition_list, f"Expected exhibition '{first_exhibition}' not found in list")

    # ===== Exhibition Details Page Tests =====
    def test_exhibition_details_page_elements(self):
        self.driver.find_element(By.ID, "exhibitions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibitions-page")))
        self.driver.find_element(By.ID, "view-exhibition-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibition-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-dates").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "exhibition-artifacts").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-exhibitions").is_displayed())

    def test_exhibition_details_page_functionality(self):
        self.driver.find_element(By.ID, "exhibitions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibitions-page")))
        with open(f'{self.code_path}/data/exhibitions.txt', 'r') as f:
            exhibitions = f.readlines()
        expected_title = exhibitions[0].split("|")[1]
        self.driver.find_element(By.ID, "view-exhibition-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibition-details-page")))
        exhibition_title = self.driver.find_element(By.ID, "exhibition-title").text
        self.assertIn(expected_title, exhibition_title, f"Expected title '{expected_title}' not found")
        self.driver.find_element(By.ID, "back-to-exhibitions").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exhibitions-page")))

    # ===== Visitor Tickets Page Tests =====
    def test_visitor_tickets_page_elements(self):
        self.driver.find_element(By.ID, "visitor-tickets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "visitor-tickets-page")))
        self.assertTrue(self.driver.find_element(By.ID, "visitor-tickets-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "ticket-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "number-of-tickets").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "purchase-ticket-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-tickets-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_visitor_tickets_page_functionality(self):
        self.driver.find_element(By.ID, "visitor-tickets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "visitor-tickets-page")))
        with open(f'{self.code_path}/data/tickets.txt', 'r') as f:
            before_count = len(f.readlines())
        Select(self.driver.find_element(By.ID, "ticket-type")).select_by_visible_text("Standard")
        self.driver.find_element(By.ID, "number-of-tickets").send_keys("2")
        self.driver.find_element(By.ID, "purchase-ticket-button").click()
        time.sleep(1)
        with open(f'{self.code_path}/data/tickets.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count, "Ticket was not added to tickets.txt")

    # ===== Virtual Events Page Tests =====
    def test_virtual_events_page_elements(self):
        self.driver.find_element(By.ID, "virtual-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "virtual-events-page")))
        self.assertTrue(self.driver.find_element(By.ID, "virtual-events-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "event-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register-event-button-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cancel-registration-button-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_virtual_events_page_functionality(self):
        self.driver.find_element(By.ID, "virtual-events-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "virtual-events-page")))
        with open(f'{self.code_path}/data/events.txt', 'r') as f:
            events = f.readlines()
        self.assertTrue(len(events) > 0, "events.txt is empty")
        event_list = self.driver.find_element(By.ID, "event-list").text
        first_event = events[0].split("|")[1]
        self.assertIn(first_event, event_list, f"Expected event '{first_event}' not found in list")

    # ===== Audio Guides Page Tests =====
    def test_audio_guides_page_elements(self):
        self.driver.find_element(By.ID, "audio-guides-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "audio-guides-page")))
        self.assertTrue(self.driver.find_element(By.ID, "audio-guides-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "audio-guide-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-language").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-language-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "play-guide-button-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_audio_guides_page_functionality(self):
        self.driver.find_element(By.ID, "audio-guides-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "audio-guides-page")))
        with open(f'{self.code_path}/data/audioguides.txt', 'r') as f:
            guides = f.readlines()
        self.assertTrue(len(guides) > 0, "audioguides.txt is empty")
        guide_list = self.driver.find_element(By.ID, "audio-guide-list").text
        first_guide = guides[0].split("|")[2]
        self.assertIn(first_guide, guide_list, f"Expected audio guide '{first_guide}' not found in list")


class TestVirtualMuseum:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        TestCase.code_path = code_path  # Set code_path for TestCase to read data
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
            'total': 14,
            'total_basic': 7,
            'total_advanced': 7,
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
        print(f"Searching for VirtualMuseum app.py...")
        py = find_app_py('VirtualMuseum')
        if py is None:
            print("=" * 70)
            print("ERROR: Could not find app.py")
            print(f"Searched for: VirtualMuseum_*/app.py")
            print("=" * 70)
            sys.exit(1)
        print(f"Found: {py}")

    if not os.path.exists(py):
        print(f"ERROR: File not found: {py}")
        sys.exit(1)

    test = TestVirtualMuseum(None, py)
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
    print(f"Total: {result['basic'] + result['advanced']}/{result['total']}")
