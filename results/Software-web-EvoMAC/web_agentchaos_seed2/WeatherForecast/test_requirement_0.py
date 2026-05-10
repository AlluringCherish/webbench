'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page of the website.
'''
import unittest
from main import app
class WeatherForecastBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2 & 3: Check that dashboard page contains required elements and example data
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Weather Dashboard</title>', html)
        # Check dashboard page container div
        self.assertIn('id="dashboard-page"', html)
        # Check current weather summary container
        self.assertIn('id="current-weather-summary"', html)
        # Check navigation buttons by their IDs
        self.assertIn('id="search-location-button"', html)
        self.assertIn('id="view-forecast-button"', html)
        self.assertIn('id="view-alerts-button"', html)
        self.assertIn('id="air-quality-button"', html)
        self.assertIn('id="saved-locations-button"', html)
        self.assertIn('id="settings-button"', html)
        # Check that example location names from example data appear in saved locations or current weather
        # Example locations: New York, London, Tokyo
        self.assertTrue(
            ('New York' in html) or ('London' in html) or ('Tokyo' in html),
            "At least one example location name should appear on dashboard"
        )
        # Check that temperature, condition, humidity, wind speed fields appear if current weather summary exists
        if 'No current weather data available.' not in html:
            self.assertRegex(html, r'Temperature:\s*\d+')
            self.assertRegex(html, r'Condition:\s*\w+')
            self.assertRegex(html, r'Humidity:\s*\d+%')
            self.assertRegex(html, r'Wind Speed:\s*\d+')
    def test_dashboard_navigation_buttons_functionality(self):
        # Test that navigation buttons URLs are correct in the HTML
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check that buttons have correct onclick URLs
        self.assertIn("onclick=\"location.href='/location_search'\"", html)
        self.assertIn("onclick=\"location.href='/weekly_forecast'\"", html)
        self.assertIn("onclick=\"location.href='/weather_alerts'\"", html)
        self.assertIn("onclick=\"location.href='/air_quality'\"", html)
        self.assertIn("onclick=\"location.href='/saved_locations'\"", html)
        self.assertIn("onclick=\"location.href='/settings'\"", html)
if __name__ == '__main__':
    unittest.main()