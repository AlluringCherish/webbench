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
        self.assertTrue(self.driver.find_element(By.ID, "featured-pets").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-pets-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_dashboard_page_functionality(self):
        # Verify featured pets are displayed from pets.txt
        with open('data/pets.txt', 'r') as f:
            pets = [p for p in f.readlines() if "Available" in p]
        featured_pets = self.driver.find_element(By.ID, "featured-pets").text
        if len(pets) > 0:
            # Verify at least one pet name appears
            first_pet = pets[0].strip().split('|')
            pet_name = first_pet[1]
            self.assertIn(pet_name, featured_pets)
        else:
            self.assertIsNotNone(featured_pets)
        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )

    # ===== Pet Listings Page Tests =====
    def test_pet_listings_page_elements(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "pet-listings-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-species").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_pet_listings_page_functionality(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        with open('data/pets.txt', 'r') as f:
            pets = [p for p in f.readlines() if "Available" in p]
        pet_grid = self.driver.find_element(By.ID, "pet-grid").text
        for pet in pets[:3]:
            pet_name = pet.split("|")[1]
            self.assertIn(pet_name, pet_grid)

    # ===== Pet Details Page Tests =====
    def test_pet_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        self.driver.find_element(By.ID, "view-details-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "pet-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-species").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "adopt-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-listings").is_displayed())

    def test_pet_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        self.driver.find_element(By.ID, "view-details-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-details-page")))
        pet_name = self.driver.find_element(By.ID, "pet-name").text
        self.assertTrue(len(pet_name) > 0)
        with open('data/pets.txt', 'r') as f:
            pets_data = f.read()
        self.assertIn(pet_name, pets_data)

    # ===== Add Pet Page Tests =====
    def test_add_pet_page_elements(self):
        self.driver.find_element(By.ID, "add-pet-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-pet-page")))
        self.assertTrue(self.driver.find_element(By.ID, "add-pet-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-name-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-species-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-breed-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-age-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-gender-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pet-description-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-pet-button").is_displayed())

    def test_add_pet_page_functionality(self):
        self.driver.find_element(By.ID, "add-pet-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-pet-page")))
        # Count pets before
        with open('data/pets.txt', 'r') as f:
            before_count = len(f.readlines())
        pet_name = f"Test Pet {int(time.time())}"
        self.driver.find_element(By.ID, "pet-name-input").send_keys(pet_name)
        Select(self.driver.find_element(By.ID, "pet-species-input")).select_by_visible_text("Dog")
        self.driver.find_element(By.ID, "pet-breed-input").send_keys("Golden Retriever")
        self.driver.find_element(By.ID, "pet-age-input").send_keys("3 years")
        Select(self.driver.find_element(By.ID, "pet-gender-input")).select_by_visible_text("Male")
        Select(self.driver.find_element(By.ID, "pet-size-input")).select_by_visible_text("Medium")
        self.driver.find_element(By.ID, "pet-description-input").send_keys("Friendly and playful dog")
        self.driver.find_element(By.ID, "submit-pet-button").click()
        time.sleep(1)
        # Verify pet was added
        with open('data/pets.txt', 'r') as f:
            after_count = len(f.readlines())
            content = f.read()
        self.assertGreater(after_count, before_count)
        with open('data/pets.txt', 'r') as f:
            self.assertIn(pet_name, f.read())

    # ===== Adoption Application Page Tests =====
    def test_application_page_elements(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        self.driver.find_element(By.ID, "view-details-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-details-page")))
        self.driver.find_element(By.ID, "adopt-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "application-page")))
        self.assertTrue(self.driver.find_element(By.ID, "application-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applicant-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "housing-type").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "reason").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-application-button").is_displayed())

    def test_application_page_functionality(self):
        self.driver.find_element(By.ID, "browse-pets-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-listings-page")))
        self.driver.find_element(By.ID, "view-details-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pet-details-page")))
        self.driver.find_element(By.ID, "adopt-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "application-page")))
        # Count applications before
        with open('data/applications.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "applicant-name").clear()
        self.driver.find_element(By.ID, "applicant-name").send_keys("John Doe")
        self.driver.find_element(By.ID, "applicant-phone").clear()
        self.driver.find_element(By.ID, "applicant-phone").send_keys("555-1234")
        Select(self.driver.find_element(By.ID, "housing-type")).select_by_visible_text("House")
        self.driver.find_element(By.ID, "reason").send_keys("I love pets!")
        self.driver.find_element(By.ID, "submit-application-button").click()
        time.sleep(1)
        # Verify application was added
        with open('data/applications.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count)

    # ===== My Applications Page Tests =====
    def test_my_applications_page_elements(self):
        self.driver.find_element(By.ID, "my-applications-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-applications-page")))
        self.assertTrue(self.driver.find_element(By.ID, "my-applications-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-status").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applications-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_my_applications_page_functionality(self):
        self.driver.find_element(By.ID, "my-applications-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-applications-page")))
        with open('data/applications.txt', 'r') as f:
            user_apps = [a for a in f.readlines() if "john_doe" in a]
        if user_apps:
            apps_table = self.driver.find_element(By.ID, "applications-table").text
            self.assertTrue(len(apps_table) > 0)

    # ===== Favorites Page Tests =====
    def test_favorites_page_elements(self):
        self.driver.find_element(By.ID, "favorites-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "favorites-page")))
        self.assertTrue(self.driver.find_element(By.ID, "favorites-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "favorites-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_favorites_page_functionality(self):
        self.driver.find_element(By.ID, "favorites-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "favorites-page")))
        with open('data/favorites.txt', 'r') as f:
            user_favs = [fav for fav in f.readlines() if fav.startswith("john_doe|")]
        favorites_grid = self.driver.find_element(By.ID, "favorites-grid").text
        self.assertTrue(favorites_grid is not None)

    # ===== Messages Page Tests =====
    def test_messages_page_elements(self):
        self.driver.find_element(By.ID, "messages-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "messages-page")))
        self.assertTrue(self.driver.find_element(By.ID, "messages-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "conversation-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "message-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "send-message-button").is_displayed())

    def test_messages_page_functionality(self):
        self.driver.find_element(By.ID, "messages-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "messages-page")))
        # Count messages before
        with open('data/messages.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "message-input").send_keys("Test message")
        self.driver.find_element(By.ID, "send-message-button").click()
        time.sleep(1)
        # Verify message was added
        with open('data/messages.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count)
        with open('data/messages.txt', 'r') as f:
            self.assertIn("Test message", f.read())

    # ===== User Profile Page Tests =====
    def test_profile_page_elements(self):
        self.driver.find_element(By.ID, "profile-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        self.assertTrue(self.driver.find_element(By.ID, "profile-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "profile-username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "profile-email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "update-profile-button").is_displayed())

    def test_profile_page_functionality(self):
        self.driver.find_element(By.ID, "profile-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-page")))
        username_display = self.driver.find_element(By.ID, "profile-username").text
        self.assertIn("john_doe", username_display)

    # ===== Admin Panel Page Tests =====
    def test_admin_panel_page_elements(self):
        self.driver.find_element(By.ID, "admin-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "admin-panel-page")))
        self.assertTrue(self.driver.find_element(By.ID, "admin-panel-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pending-applications").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "all-pets-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_admin_panel_page_functionality(self):
        self.driver.find_element(By.ID, "admin-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "admin-panel-page")))
        with open('data/applications.txt', 'r') as f:
            pending = [a for a in f.readlines() if "Pending" in a]
        pending_display = self.driver.find_element(By.ID, "pending-applications").text
        self.assertTrue(pending_display is not None)


class TestPetAdoptionCenter:
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
            'total': 20,
            'total_basic': 10,
            'total_advanced': 10,
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
        print(f"Searching for PetAdoptionCenter app.py...")
        py = find_app_py('PetAdoptionCenter')
        if py is None:
            print("=" * 70)
            print("ERROR: Could not find app.py")
            print(f"Searched for: PetAdoptionCenter_*/app.py")
            print("=" * 70)
            sys.exit(1)
        print(f"Found: {py}")

    if not os.path.exists(py):
        print(f"ERROR: File not found: {py}")
        sys.exit(1)

    test = TestPetAdoptionCenter(None, py)
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
    print(f"Total: {result['basic'] + result['advanced']}/{result['total']}")
