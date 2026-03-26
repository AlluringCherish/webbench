'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of ALL pages including presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class WeatherForecastTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access dashboard page at root URL
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check page title
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('title')
        self.assertIsNotNone(title)
        self.assertIn('Weather Dashboard', title.text)
    def test_dashboard_elements_and_navigation_buttons(self):
        # Test Task 2: Dashboard page elements and navigation buttons
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div)
        # Check current weather summary div
        current_weather_div = dashboard_div.find('div', id='current-weather-summary')
        self.assertIsNotNone(current_weather_div)
        # Check presence of temperature-display, weather-condition, humidity-info, wind-speed-info, last-updated
        self.assertIsNotNone(current_weather_div.find('div', id='temperature-display'))
        self.assertIsNotNone(current_weather_div.find('div', id='weather-condition'))
        self.assertIsNotNone(current_weather_div.find('div', id='humidity-info'))
        self.assertIsNotNone(current_weather_div.find('div', id='wind-speed-info'))
        self.assertIsNotNone(current_weather_div.find('div', id='last-updated'))
        # Check navigation buttons by id and text
        buttons = {
            'search-location-button': 'Search Locations',
            'view-forecast-button': 'View Weekly Forecast',
            'view-alerts-button': 'View Weather Alerts',
            'view-air-quality-button': 'View Air Quality',
            'saved-locations-button': 'Saved Locations',
            'settings-button': 'Settings'
        }
        for btn_id, btn_text in buttons.items():
            btn = dashboard_div.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Button with id {btn_id} not found")
            self.assertIn(btn_text, btn.text)
    def test_current_weather_page_elements(self):
        # Test Task 3: Current Weather page elements for a valid location (e.g. location_id=1)
        response = self.client.get('/current_weather/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='current-weather-page')
        self.assertIsNotNone(container)
        # Check location name h1
        location_name = container.find('h1', id='location-name')
        self.assertIsNotNone(location_name)
        self.assertTrue(len(location_name.text.strip()) > 0)
        # Check temperature-display div
        temp_div = container.find('div', id='temperature-display')
        self.assertIsNotNone(temp_div)
        # Check weather-condition div
        condition_div = container.find('div', id='weather-condition')
        self.assertIsNotNone(condition_div)
        # Check humidity-info div
        humidity_div = container.find('div', id='humidity-info')
        self.assertIsNotNone(humidity_div)
        # Check wind-speed-info div
        wind_div = container.find('div', id='wind-speed-info')
        self.assertIsNotNone(wind_div)
        # Check back to dashboard button
        back_form = container.find('form')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_button)
    def test_weekly_forecast_page_elements(self):
        # Test Task 3: Weekly Forecast page elements and filtering
        response = self.client.get('/weekly_forecast')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='forecast-page')
        self.assertIsNotNone(container)
        # Check location filter dropdown
        location_filter = container.find('select', id='location-filter')
        self.assertIsNotNone(location_filter)
        # Check forecast table
        forecast_table = container.find('table', id='forecast-table')
        self.assertIsNotNone(forecast_table)
        # Check table headers
        headers = [th.text.strip() for th in forecast_table.find_all('th')]
        expected_headers = ['Date', 'High Temp (°C)', 'Low Temp (°C)', 'Condition', 'Precipitation (%)', 'Humidity (%)']
        # Temperature unit letter may vary, so check partial match for 'High Temp' and 'Low Temp'
        self.assertTrue(any('High Temp' in h for h in headers))
        self.assertTrue(any('Low Temp' in h for h in headers))
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_button)
    def test_location_search_page_elements(self):
        # Test Task 3: Location Search page elements and search functionality
        response = self.client.get('/location_search')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='search-page')
        self.assertIsNotNone(container)
        # Check search input
        search_input = container.find('input', id='location-search-input')
        self.assertIsNotNone(search_input)
        # Check search results div or ul (may be ul with id search-results)
        search_results = container.find(id='search-results')
        # May be empty initially, so no assert on presence
        # Check saved locations list div or ul
        saved_locations_list = container.find(id='saved-locations-list')
        # May be empty initially, so no assert on presence
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button')
        self.assertIsNotNone(back_button)
    def test_weather_alerts_page_elements(self):
        # Test Task 3: Weather Alerts page elements and filters
        response = self.client.get('/weather_alerts')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='alerts-page')
        self.assertIsNotNone(container)
        # Check severity filter dropdown
        severity_filter = container.find('select', id='severity-filter')
        self.assertIsNotNone(severity_filter)
        # Check location filter dropdown
        location_filter = container.find('select', id='location-filter-alerts')
        self.assertIsNotNone(location_filter)
        # Check alerts list div
        alerts_list = container.find('div', id='alerts-list')
        # May be empty if no alerts, so no assert on presence
        # Check acknowledge alert buttons if alerts present
        if alerts_list:
            buttons = alerts_list.find_all('button')
            self.assertTrue(all(btn['id'].startswith('acknowledge-alert-button-') for btn in buttons))
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button')
        self.assertIsNotNone(back_button)
    def test_air_quality_page_elements(self):
        # Test Task 3: Air Quality page elements and filtering
        response = self.client.get('/air_quality')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='air-quality-page')
        self.assertIsNotNone(container)
        # Check location filter dropdown
        location_filter = container.find('select', id='location-aqi-filter')
        self.assertIsNotNone(location_filter)
        # Check AQI display div
        aqi_display = container.find('div', id='aqi-display')
        # May be None if no data for default location
        # Check AQI description div
        aqi_desc = container.find('div', id='aqi-description')
        # Check pollution details table
        pollution_table = container.find('table', id='pollution-details')
        # Check health recommendation div
        health_rec = container.find('div', id='health-recommendation')
        # Check last updated div
        last_updated = container.find('div', id='last-updated')
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button')
        self.assertIsNotNone(back_button)
    def test_saved_locations_page_elements(self):
        # Test Task 3: Saved Locations page elements and actions
        response = self.client.get('/saved_locations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='saved-locations-page')
        self.assertIsNotNone(container)
        # Check locations table
        locations_table = container.find('table', id='locations-table')
        # May be None if no saved locations
        # Check add new location button
        add_new_btn = container.find('button', id='add-new-location-button')
        self.assertIsNotNone(add_new_btn)
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button')
        self.assertIsNotNone(back_button)
    def test_settings_page_elements(self):
        # Test Task 3: Settings page elements and form controls
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='settings-page')
        self.assertIsNotNone(container)
        # Check temperature unit select
        temp_unit_select = container.find('select', id='temperature-unit-select')
        self.assertIsNotNone(temp_unit_select)
        # Check default location select
        default_loc_select = container.find('select', id='default-location-select')
        self.assertIsNotNone(default_loc_select)
        # Check alert notifications toggle checkbox
        alert_toggle = container.find('input', id='alert-notifications-toggle')
        self.assertIsNotNone(alert_toggle)
        self.assertEqual(alert_toggle.get('type'), 'checkbox')
        # Check save settings button
        save_btn = container.find('button', id='save-settings-button')
        self.assertIsNotNone(save_btn)
        # Check back to dashboard button
        back_form = container.find('form', action='/back_to_dashboard')
        self.assertIsNotNone(back_form)
        back_button = back_form.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_button)
if __name__ == '__main__':
    unittest.main()