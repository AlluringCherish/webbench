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
        self.assertTrue(self.driver.find_element(By.ID, "featured-properties").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-properties-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-inquiries-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-favorites-button").is_displayed())

    def test_dashboard_page_functionality(self):
        # Verify featured properties are displayed
        with open('data/properties.txt', 'r') as f:
            properties = f.readlines()
        featured = self.driver.find_element(By.ID, "featured-properties").text
        if len(properties) > 0:
            self.assertTrue(len(featured) > 0)
        self.driver.find_element(By.ID, "browse-properties-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-page").is_displayed())

    # ===== Property Search Page Tests =====
    def test_search_page_elements(self):
        self.driver.find_element(By.ID, "browse-properties-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "price-range-min").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "price-range-max").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "property-type-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "properties-grid").is_displayed())

    def test_search_page_functionality(self):
        self.driver.find_element(By.ID, "browse-properties-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        # Verify properties from properties.txt are displayed
        with open('data/properties.txt', 'r') as f:
            properties = f.readlines()
        self.assertTrue(len(properties) > 0, "properties.txt is empty")
        first_property = properties[0].strip().split('|')
        expected_address = first_property[1]
        properties_grid = self.driver.find_element(By.ID, "properties-grid").text
        self.assertIn(expected_address, properties_grid)

    # ===== Property Details Page Tests =====
    def test_property_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-properties-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-property-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "property-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "property-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "property-address").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "property-price").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "property-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "property-features").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-to-favorites-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-inquiry-button").is_displayed())

    def test_property_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-properties-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.driver.find_element(By.ID, "view-property-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "property-details-page")))
        # Verify property details match properties.txt
        with open('data/properties.txt', 'r') as f:
            properties = f.readlines()
        first_property = properties[0].strip().split('|')
        expected_address = first_property[1]
        expected_price = first_property[3]
        address = self.driver.find_element(By.ID, "property-address").text
        price = self.driver.find_element(By.ID, "property-price").text
        self.assertEqual(address, expected_address)
        self.assertIn(expected_price, price)

    # ===== Property Inquiry Page Tests =====
    def test_inquiry_page_elements(self):
        self.driver.get("http://localhost:5000/inquiry")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inquiry-page")))
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-property").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-phone").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-inquiry-button").is_displayed())

    def test_inquiry_page_functionality(self):
        self.driver.get("http://localhost:5000/inquiry")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inquiry-page")))
        # Verify property selection dropdown has properties
        with open('data/properties.txt', 'r') as f:
            properties = f.readlines()
        if len(properties) > 0:
            select = Select(self.driver.find_element(By.ID, "select-property"))
            self.assertTrue(len(select.options) > 0)
        self.driver.find_element(By.ID, "inquiry-name").send_keys("Test User")
        self.driver.find_element(By.ID, "inquiry-email").send_keys("test@email.com")
        name = self.driver.find_element(By.ID, "inquiry-name").get_attribute("value")
        self.assertEqual(name, "Test User")

    # ===== My Inquiries Page Tests =====
    def test_inquiries_page_elements(self):
        self.driver.find_element(By.ID, "my-inquiries-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inquiries-page")))
        self.assertTrue(self.driver.find_element(By.ID, "inquiries-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiries-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "inquiry-status-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_inquiries_page_functionality(self):
        self.driver.find_element(By.ID, "my-inquiries-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inquiries-page")))
        # Verify inquiries from inquiries.txt are displayed
        with open('data/inquiries.txt', 'r') as f:
            inquiries = f.readlines()
        inquiries_table = self.driver.find_element(By.ID, "inquiries-table").text
        if len(inquiries) > 0:
            first_inquiry = inquiries[0].strip().split('|')
            customer_name = first_inquiry[2]
            self.assertIn(customer_name, inquiries_table)
        else:
            self.assertIsNotNone(inquiries_table)

    # ===== My Favorites Page Tests =====
    def test_favorites_page_elements(self):
        self.driver.find_element(By.ID, "my-favorites-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "favorites-page")))
        self.assertTrue(self.driver.find_element(By.ID, "favorites-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "favorites-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_favorites_page_functionality(self):
        self.driver.find_element(By.ID, "my-favorites-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "favorites-page")))
        # Verify favorites from favorites.txt are displayed
        with open('data/favorites.txt', 'r') as f:
            favorites = f.readlines()
        favorites_list = self.driver.find_element(By.ID, "favorites-list").text
        if len(favorites) > 0:
            # Get property details from first favorite
            first_fav = favorites[0].strip().split('|')
            property_id = first_fav[1]
            with open('data/properties.txt', 'r') as f:
                properties = f.readlines()
            for prop in properties:
                if prop.startswith(f"{property_id}|"):
                    address = prop.strip().split('|')[1]
                    self.assertIn(address, favorites_list)
                    break
        else:
            self.assertIsNotNone(favorites_list)

    # ===== Agent Directory Page Tests =====
    def test_agents_page_elements(self):
        self.driver.get("http://localhost:5000/agents")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "agents-page")))
        self.assertTrue(self.driver.find_element(By.ID, "agents-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "agents-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "agent-search").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_agents_page_functionality(self):
        self.driver.get("http://localhost:5000/agents")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "agents-page")))
        # Verify agents from agents.txt are displayed
        with open('data/agents.txt', 'r') as f:
            agents = f.readlines()
        self.assertTrue(len(agents) > 0, "agents.txt is empty")
        first_agent = agents[0].strip().split('|')
        agent_name = first_agent[1]
        agents_list = self.driver.find_element(By.ID, "agents-list").text
        self.assertIn(agent_name, agents_list)

    # ===== Locations Page Tests =====
    def test_locations_page_elements(self):
        self.driver.get("http://localhost:5000/locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "locations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "locations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "locations-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-sort").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_locations_page_functionality(self):
        self.driver.get("http://localhost:5000/locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "locations-page")))
        # Verify locations from locations.txt are displayed
        with open('data/locations.txt', 'r') as f:
            locations = f.readlines()
        self.assertTrue(len(locations) > 0, "locations.txt is empty")
        first_location = locations[0].strip().split('|')
        location_name = first_location[1]
        locations_list = self.driver.find_element(By.ID, "locations-list").text
        self.assertIn(location_name, locations_list)


class TestRealEstate:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('RealEstate')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestRealEstate(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
