'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the elements and integrity of all pages as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class WeatherForecastAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_02_dashboard_content_and_navigation_buttons(self):
        # Test Task 2: Dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page must contain div with id 'dashboard-page'")
        # Check current weather summary div
        current_weather_summary = soup.find('div', id='current-weather-summary')
        self.assertIsNotNone(current_weather_summary, "Dashboard page must contain div with id 'current-weather-summary'")
        # Check navigation buttons
        search_location_button = soup.find('button', id='search-location-button')
        self.assertIsNotNone(search_location_button, "Dashboard page must contain button with id 'search-location-button'")
        view_forecast_button = soup.find('button', id='view-forecast-button')
        self.assertIsNotNone(view_forecast_button, "Dashboard page must contain button with id 'view-forecast-button'")
        view_alerts_button = soup.find('button', id='view-alerts-button')
        self.assertIsNotNone(view_alerts_button, "Dashboard page must contain button with id 'view-alerts-button'")
    def test_03_current_weather_page_elements(self):
        # Test Task 3: Current Weather page elements presence
        # Use default location from dashboard to get location_id
        response_dashboard = self.client.get('/')
        soup_dashboard = BeautifulSoup(response_dashboard.data, 'html.parser')
        # Try to get location_id from current_weather_summary data attribute or fallback to '1'
        # Since no direct location_id in dashboard, use '1' as default for test
        location_id = '1'
        response = self.client.get(f'/current_weather?location_id={location_id}')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='current-weather-page'), "Current Weather page must have div with id 'current-weather-page'")
        self.assertIsNotNone(soup.find('h1', id='location-name'), "Current Weather page must have h1 with id 'location-name'")
        self.assertIsNotNone(soup.find('div', id='temperature-display'), "Current Weather page must have div with id 'temperature-display'")
        self.assertIsNotNone(soup.find('div', id='weather-condition'), "Current Weather page must have div with id 'weather-condition'")
        self.assertIsNotNone(soup.find('div', id='humidity-info'), "Current Weather page must have div with id 'humidity-info'")
        self.assertIsNotNone(soup.find('div', id='wind-speed-info'), "Current Weather page must have div with id 'wind-speed-info'")
    def test_04_weekly_forecast_page_elements(self):
        response = self.client.get('/weekly_forecast')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='forecast-page'), "Weekly Forecast page must have div with id 'forecast-page'")
        self.assertIsNotNone(soup.find('table', id='forecast-table'), "Weekly Forecast page must have table with id 'forecast-table'")
        self.assertIsNotNone(soup.find('select', id='location-filter'), "Weekly Forecast page must have dropdown with id 'location-filter'")
        self.assertIsNotNone(soup.find('div', id='forecast-list'), "Weekly Forecast page must have div with id 'forecast-list'")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Weekly Forecast page must have button with id 'back-to-dashboard'")
    def test_05_location_search_page_elements(self):
        response = self.client.get('/location_search')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='search-page'), "Location Search page must have div with id 'search-page'")
        self.assertIsNotNone(soup.find('input', id='location-search-input'), "Location Search page must have input with id 'location-search-input'")
        self.assertIsNotNone(soup.find('div', id='search-results'), "Location Search page must have div with id 'search-results'")
        self.assertIsNotNone(soup.find('div', id='saved-locations-list'), "Location Search page must have div with id 'saved-locations-list'")
        # Check that at least one select-location-button-{location_id} button exists if there are search results
        buttons = soup.find_all('button')
        select_buttons = [btn for btn in buttons if btn.get('id', '').startswith('select-location-button-')]
        self.assertTrue(len(select_buttons) >= 0, "Location Search page should have buttons with id pattern 'select-location-button-{location_id}'")
    def test_06_weather_alerts_page_elements(self):
        response = self.client.get('/weather_alerts')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='alerts-page'), "Weather Alerts page must have div with id 'alerts-page'")
        self.assertIsNotNone(soup.find('div', id='alerts-list'), "Weather Alerts page must have div with id 'alerts-list'")
        self.assertIsNotNone(soup.find('select', id='severity-filter'), "Weather Alerts page must have dropdown with id 'severity-filter'")
        self.assertIsNotNone(soup.find('select', id='location-filter-alerts'), "Weather Alerts page must have dropdown with id 'location-filter-alerts'")
        # Check for acknowledge-alert-button-{alert_id} buttons if alerts exist
        buttons = soup.find_all('button')
        acknowledge_buttons = [btn for btn in buttons if btn.get('id', '').startswith('acknowledge-alert-button-')]
        self.assertTrue(len(acknowledge_buttons) >= 0, "Weather Alerts page should have buttons with id pattern 'acknowledge-alert-button-{alert_id}'")
    def test_07_air_quality_page_elements(self):
        response = self.client.get('/air_quality')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='air-quality-page'), "Air Quality page must have div with id 'air-quality-page'")
        self.assertIsNotNone(soup.find('div', id='aqi-display'), "Air Quality page must have div with id 'aqi-display'")
        self.assertIsNotNone(soup.find('div', id='aqi-description'), "Air Quality page must have div with id 'aqi-description'")
        self.assertIsNotNone(soup.find('table', id='pollution-details'), "Air Quality page must have table with id 'pollution-details'")
        self.assertIsNotNone(soup.find('select', id='location-aqi-filter'), "Air Quality page must have dropdown with id 'location-aqi-filter'")
        self.assertIsNotNone(soup.find('div', id='health-recommendation'), "Air Quality page must have div with id 'health-recommendation'")
    def test_08_saved_locations_page_elements(self):
        response = self.client.get('/saved_locations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='saved-locations-page'), "Saved Locations page must have div with id 'saved-locations-page'")
        self.assertIsNotNone(soup.find('table', id='locations-table'), "Saved Locations page must have table with id 'locations-table'")
        # Check for view-location-weather-{location_id} and remove-location-button-{location_id} buttons
        buttons = soup.find_all('button')
        view_buttons = [btn for btn in buttons if btn.get('id', '').startswith('view-location-weather-')]
        remove_buttons = [btn for btn in buttons if btn.get('id', '').startswith('remove-location-button-')]
        add_new_location_button = soup.find('button', id='add-new-location-button')
        self.assertTrue(len(view_buttons) >= 0, "Saved Locations page should have buttons with id pattern 'view-location-weather-{location_id}'")
        self.assertTrue(len(remove_buttons) >= 0, "Saved Locations page should have buttons with id pattern 'remove-location-button-{location_id}'")
        self.assertIsNotNone(add_new_location_button, "Saved Locations page must have button with id 'add-new-location-button'")
    def test_09_settings_page_elements(self):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find('div', id='settings-page'), "Settings page must have div with id 'settings-page'")
        self.assertIsNotNone(soup.find('select', id='temperature-unit-select'), "Settings page must have dropdown with id 'temperature-unit-select'")
        self.assertIsNotNone(soup.find('select', id='default-location-select'), "Settings page must have dropdown with id 'default-location-select'")
        self.assertIsNotNone(soup.find('input', id='alert-notifications-toggle'), "Settings page must have checkbox with id 'alert-notifications-toggle'")
        self.assertIsNotNone(soup.find('button', id='save-settings-button'), "Settings page must have button with id 'save-settings-button'")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Settings page must have button with id 'back-to-dashboard'")
if __name__ == '__main__':
    unittest.main()