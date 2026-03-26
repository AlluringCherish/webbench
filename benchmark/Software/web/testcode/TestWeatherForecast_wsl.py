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
        self.assertTrue(self.driver.find_element(By.ID, "current-weather-summary").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-location-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-forecast-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-alerts-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "view-forecast-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "forecast-page")))
        self.assertTrue(self.driver.find_element(By.ID, "forecast-page").is_displayed())

    # ===== Current Weather Page Tests =====
    def test_current_weather_page_elements(self):
        self.driver.get("http://localhost:5000/current-weather")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "current-weather-page")))
        self.assertTrue(self.driver.find_element(By.ID, "current-weather-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "temperature-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "weather-condition").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "humidity-info").is_displayed())

    def test_current_weather_page_functionality(self):
        self.driver.get("http://localhost:5000/current-weather")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "current-weather-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/current_weather.txt', 'r') as f:
            weather_data = f.readlines()
        self.assertTrue(len(weather_data) > 0, "current_weather.txt is empty")
        temperature = self.driver.find_element(By.ID, "temperature-display").text
        self.assertTrue(len(temperature) > 0, "Temperature display is empty")

    # ===== Weekly Forecast Page Tests =====
    def test_forecast_page_elements(self):
        self.driver.find_element(By.ID, "view-forecast-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "forecast-page")))
        self.assertTrue(self.driver.find_element(By.ID, "forecast-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "forecast-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "forecast-list").is_displayed())

    def test_forecast_page_functionality(self):
        self.driver.find_element(By.ID, "view-forecast-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "forecast-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/forecasts.txt', 'r') as f:
            forecasts = f.readlines()
        self.assertTrue(len(forecasts) > 0, "forecasts.txt is empty")
        forecast_list = self.driver.find_element(By.ID, "forecast-list").text
        self.assertTrue(len(forecast_list) > 0, "Forecast list is empty")

    # ===== Location Search Page Tests =====
    def test_search_page_elements(self):
        self.driver.find_element(By.ID, "search-location-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-results").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "saved-locations-list").is_displayed())

    def test_search_page_functionality(self):
        self.driver.find_element(By.ID, "search-location-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/locations.txt', 'r') as f:
            locations = f.readlines()
        self.assertTrue(len(locations) > 0, "locations.txt is empty")
        first_location = locations[0].split('|')[1]
        search_input = self.driver.find_element(By.ID, "location-search-input")
        search_input.send_keys(first_location)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-results")))
        results = self.driver.find_element(By.ID, "search-results").text
        self.assertIn(first_location, results, f"Expected location '{first_location}' not found in search results")

    # ===== Weather Alerts Page Tests =====
    def test_alerts_page_elements(self):
        self.driver.find_element(By.ID, "view-alerts-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "alerts-page")))
        self.assertTrue(self.driver.find_element(By.ID, "alerts-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "alerts-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "severity-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-filter-alerts").is_displayed())

    def test_alerts_page_functionality(self):
        self.driver.find_element(By.ID, "view-alerts-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "alerts-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/alerts.txt', 'r') as f:
            alerts = f.readlines()
        alerts_list = self.driver.find_element(By.ID, "alerts-list").text
        if len(alerts) > 0:
            first_alert_type = alerts[0].split('|')[2]
            self.assertIn(first_alert_type, alerts_list, f"Expected alert type '{first_alert_type}' not found")

    # ===== Air Quality Page Tests =====
    def test_air_quality_page_elements(self):
        self.driver.get("http://localhost:5000/air-quality")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "air-quality-page")))
        self.assertTrue(self.driver.find_element(By.ID, "air-quality-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "aqi-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "aqi-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "pollution-details").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-aqi-filter").is_displayed())

    def test_air_quality_page_functionality(self):
        self.driver.get("http://localhost:5000/air-quality")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "air-quality-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/air_quality.txt', 'r') as f:
            aqi_data = f.readlines()
        self.assertTrue(len(aqi_data) > 0, "air_quality.txt is empty")
        aqi_value = self.driver.find_element(By.ID, "aqi-display").text
        self.assertTrue(len(aqi_value) > 0, "AQI display is empty")

    # ===== Saved Locations Page Tests =====
    def test_saved_locations_page_elements(self):
        self.driver.get("http://localhost:5000/saved-locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "saved-locations-page")))
        self.assertTrue(self.driver.find_element(By.ID, "saved-locations-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "locations-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-new-location-button").is_displayed())

    def test_saved_locations_page_functionality(self):
        self.driver.get("http://localhost:5000/saved-locations")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "saved-locations-page")))
        code_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(f'{code_path}/data/saved_locations.txt', 'r') as f:
            saved_locations = f.readlines()
        locations_table = self.driver.find_element(By.ID, "locations-table").text
        if len(saved_locations) > 0:
            first_saved_location = saved_locations[0].split('|')[3]
            self.assertIn(first_saved_location, locations_table, f"Expected location '{first_saved_location}' not found")

    # ===== Settings Page Tests =====
    def test_settings_page_elements(self):
        self.driver.get("http://localhost:5000/settings")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "settings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "settings-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "temperature-unit-select").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "default-location-select").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-settings-button").is_displayed())

    def test_settings_page_functionality(self):
        self.driver.get("http://localhost:5000/settings")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "settings-page")))
        select_element = Select(self.driver.find_element(By.ID, "temperature-unit-select"))
        select_element.select_by_value("Fahrenheit")
        selected_value = select_element.first_selected_option.get_attribute("value")
        self.assertEqual(selected_value, "Fahrenheit")


class TestWeatherForecast:
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
        result = {'total': 16, 'total_basic': 8, 'total_advanced': 8, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except:
            self.tear_down()

        if result['test_cases']['set_up'] != 1:
            self.tear_down()
            return result

        res = None
        if result['test_cases']['set_up'] == 1:
            try:
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except Exception as e:
                print(f"ERROR: {e}")
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('WeatherForecast')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestWeatherForecast(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
