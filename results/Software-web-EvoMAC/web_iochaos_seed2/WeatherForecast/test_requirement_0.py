'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) can be accessed and loads correctly.
Test basic navigation buttons on the Dashboard page to ensure they link to correct pages.
'''
import unittest
from main import app
class WeatherForecastBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather Dashboard', response.data)
        # Check presence of current weather summary container
        self.assertIn(b'id="current-weather-summary"', response.data)
        # Check presence of navigation buttons by their IDs
        self.assertIn(b'id="search-location-button"', response.data)
        self.assertIn(b'id="view-forecast-button"', response.data)
        self.assertIn(b'id="view-alerts-button"', response.data)
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # The buttons use onclick with location.href, so check URLs in the HTML
        self.assertIn(b"location.href='/location_search'", response.data)
        self.assertIn(b"location.href='/weekly_forecast'", response.data)
        self.assertIn(b"location.href='/weather_alerts'", response.data)
if __name__ == '__main__':
    unittest.main()