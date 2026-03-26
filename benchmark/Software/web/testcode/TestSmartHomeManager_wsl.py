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
        self.assertTrue(self.driver.find_element(By.ID, "device-summary").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-list-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-device-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "automation-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "energy-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "activity-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "room-list").is_displayed())

    def test_dashboard_page_functionality(self):
        device_summary = self.driver.find_element(By.ID, "device-summary").text
        self.assertTrue(len(device_summary) > 0)
        self.driver.find_element(By.ID, "device-list-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        self.assertIn("My Devices", self.driver.title)

    # ===== Device List Page Tests =====
    def test_device_list_page_elements(self):
        self.driver.find_element(By.ID, "device-list-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        self.assertTrue(self.driver.find_element(By.ID, "device-list-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_device_list_page_functionality(self):
        self.driver.find_element(By.ID, "device-list-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        with open('data/devices.txt', 'r') as f:
            devices = [d for d in f.readlines() if d.startswith("john_doe|")]
        device_table = self.driver.find_element(By.ID, "device-table").text
        for device in devices:
            device_name = device.split("|")[2]
            self.assertIn(device_name, device_table)

    # ===== Add Device Page Tests =====
    def test_add_device_page_elements(self):
        self.driver.find_element(By.ID, "add-device-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-device-page")))
        self.assertTrue(self.driver.find_element(By.ID, "add-device-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-room").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-device-button").is_displayed())

    def test_add_device_page_functionality(self):
        self.driver.find_element(By.ID, "add-device-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-device-page")))
        device_name = f"Test Device {int(time.time())}"
        self.driver.find_element(By.ID, "device-name").send_keys(device_name)
        Select(self.driver.find_element(By.ID, "device-type")).select_by_visible_text("Light")
        Select(self.driver.find_element(By.ID, "device-room")).select_by_visible_text("Living Room")
        self.driver.find_element(By.ID, "submit-device-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        with open('data/devices.txt', 'r') as f:
            self.assertIn(device_name, f.read())

    # ===== Device Control Page Tests =====
    def test_device_control_page_elements(self):
        self.driver.find_element(By.ID, "device-list-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        self.driver.find_element(By.ID, "control-device-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-control-page")))
        self.assertTrue(self.driver.find_element(By.ID, "device-control-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-name-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "device-status-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "power-toggle").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-settings-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-devices").is_displayed())

    def test_device_control_page_functionality(self):
        self.driver.find_element(By.ID, "device-list-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        self.driver.find_element(By.ID, "control-device-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-control-page")))
        device_name = self.driver.find_element(By.ID, "device-name-display").text
        self.assertTrue(len(device_name) > 0)
        self.driver.find_element(By.ID, "power-toggle").click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "back-to-devices")))
        self.driver.find_element(By.ID, "back-to-devices").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "device-list-page")))
        self.assertIn("My Devices", self.driver.title)

    # ===== Automation Rules Page Tests =====
    def test_automation_page_elements(self):
        self.driver.find_element(By.ID, "automation-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "automation-page")))
        self.assertTrue(self.driver.find_element(By.ID, "automation-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rules-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rule-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trigger-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trigger-value").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "action-device").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "action-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-rule-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_automation_page_functionality(self):
        self.driver.find_element(By.ID, "automation-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "automation-page")))
        with open('data/automation_rules.txt', 'r') as f:
            rules = [r for r in f.readlines() if r.startswith("john_doe|")]
        self.assertTrue(len(rules) > 0, "No automation rules found for john_doe")
        rules_table = self.driver.find_element(By.ID, "rules-table").text
        first_rule_name = rules[0].split("|")[2]
        self.assertIn(first_rule_name, rules_table, f"Expected rule '{first_rule_name}' not found in table")

    # ===== Energy Report Page Tests =====
    def test_energy_page_elements(self):
        self.driver.find_element(By.ID, "energy-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "energy-page")))
        self.assertTrue(self.driver.find_element(By.ID, "energy-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "energy-summary").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "energy-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "date-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-filter-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_energy_page_functionality(self):
        self.driver.find_element(By.ID, "energy-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "energy-page")))
        energy_summary = self.driver.find_element(By.ID, "energy-summary").text
        self.assertTrue(len(energy_summary) > 0)
        with open('data/energy_logs.txt', 'r') as f:
            logs = f.readlines()
        self.assertTrue(len(logs) > 0)

    # ===== Activity Logs Page Tests =====
    def test_activity_page_elements(self):
        self.driver.find_element(By.ID, "activity-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "activity-page")))
        self.assertTrue(self.driver.find_element(By.ID, "activity-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "activity-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-activity").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-search-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_activity_page_functionality(self):
        self.driver.find_element(By.ID, "activity-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "activity-page")))
        with open('data/activity_logs.txt', 'r') as f:
            logs = [l for l in f.readlines() if l.startswith("john_doe|")]
        self.assertTrue(len(logs) > 0, "No activity logs found for john_doe")
        activity_table = self.driver.find_element(By.ID, "activity-table").text
        first_log_action = logs[0].split("|")[3]
        self.assertIn(first_log_action, activity_table, f"Expected action '{first_log_action}' not found in activity table")


class TestSmartHomeManager:
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
        print(f"Searching for SmartHomeManager app.py...")
        py = find_app_py('SmartHomeManager')
        if py is None:
            print("=" * 70)
            print("ERROR: Could not find app.py")
            print(f"Searched for: SmartHomeManager_*/app.py")
            print("=" * 70)
            sys.exit(1)
        print(f"Found: {py}")

    if not os.path.exists(py):
        print(f"ERROR: File not found: {py}")
        sys.exit(1)

    test = TestSmartHomeManager(None, py)
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
    print(f"Total: {result['basic'] + result['advanced']}/{result['total']}")
