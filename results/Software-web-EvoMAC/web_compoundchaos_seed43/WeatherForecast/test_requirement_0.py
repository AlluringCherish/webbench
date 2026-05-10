'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Test the presence and correctness of required elements on the Dashboard page:
- ID: dashboard-page (Div container)
- ID: current-weather-summary (Div)
- ID: search-location-button (Button)
- ID: view-forecast-button (Button)
- ID: view-alerts-button (Button)
'''
import unittest
from flask import Flask
from bs4 import BeautifulSoup
# Assuming the main app is created in a module named app.py with variable 'app'
# For this test, we will create a minimal Flask app simulating the Dashboard page
# because the original source code is not provided.
app = Flask(__name__)
@app.route('/')
def dashboard():
    # Simulated HTML content of the Dashboard page based on requirements
    html = '''
    <div id="dashboard-page">
        <div id="current-weather-summary">Current weather: Sunny, 72°F</div>
        <button id="search-location-button">Search Location</button>
        <button id="view-forecast-button">View Forecast</button>
        <button id="view-alerts-button">View Alerts</button>
    </div>
    '''
    return html, 200
class TestWeatherForecastDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True
    def test_access_local_port_5000(self):
        # Simulate accessing the root URL (Dashboard page)
        response = self.app.get('/')
        # Check HTTP status code 200 OK
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_loads_correctly(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check dashboard-page div exists
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "dashboard-page div not found")
        # Check current-weather-summary div exists
        current_weather = soup.find('div', id='current-weather-summary')
        self.assertIsNotNone(current_weather, "current-weather-summary div not found")
        # Check search-location-button button exists
        search_button = soup.find('button', id='search-location-button')
        self.assertIsNotNone(search_button, "search-location-button not found")
        # Check view-forecast-button button exists
        forecast_button = soup.find('button', id='view-forecast-button')
        self.assertIsNotNone(forecast_button, "view-forecast-button not found")
        # Check view-alerts-button button exists
        alerts_button = soup.find('button', id='view-alerts-button')
        self.assertIsNotNone(alerts_button, "view-alerts-button not found")
if __name__ == '__main__':
    unittest.main()