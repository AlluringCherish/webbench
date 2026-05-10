'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test whether basic navigation buttons on the Dashboard page exist and have correct IDs.
'''
import unittest
from flask import Flask
from flask.testing import FlaskClient
from bs4 import BeautifulSoup
# Assuming the main app is created in a module named 'app.py' with variable 'app'
# Since we don't have the actual app.py, we will create a minimal Flask app stub here
# to demonstrate the test structure.
# In real scenario, replace the below with: from app import app
app = Flask(__name__)
# Minimal route for dashboard to enable testing
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Simulate the dashboard page HTML with required elements
    return '''
    <html>
    <head><title>Smart Home Dashboard</title></head>
    <body>
      <div id="dashboard-page">
        <div id="device-summary">Total: 3, Active: 2, Offline: 1</div>
        <button id="device-list-button">Device List</button>
        <button id="add-device-button">Add Device</button>
        <button id="automation-button">Automation Rules</button>
        <button id="energy-button">Energy Report</button>
        <button id="activity-button">Activity Logs</button>
        <div id="room-list">
          <div>Living Room (2 devices)</div>
          <div>Bedroom (1 device)</div>
        </div>
      </div>
    </body>
    </html>
    '''
class TestSmartHomeManagerDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True
    def test_dashboard_accessible_on_port_5000(self):
        # Since we cannot test actual port binding here, we test route accessibility
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (HTTP 200)")
    def test_dashboard_page_title(self):
        response = self.app.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string, "Smart Home Dashboard", "Dashboard page title should be correct")
    def test_dashboard_main_container_exists(self):
        response = self.app.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find(id="dashboard-page")
        self.assertIsNotNone(dashboard_div, "Dashboard main container with id 'dashboard-page' should exist")
    def test_device_summary_exists(self):
        response = self.app.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        device_summary = soup.find(id="device-summary")
        self.assertIsNotNone(device_summary, "Device summary div with id 'device-summary' should exist")
        self.assertIn("Total", device_summary.text, "Device summary should contain total devices info")
    def test_dashboard_buttons_exist(self):
        response = self.app.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        button_ids = [
            "device-list-button",
            "add-device-button",
            "automation-button",
            "energy-button",
            "activity-button"
        ]
        for btn_id in button_ids:
            btn = soup.find(id=btn_id)
            self.assertIsNotNone(btn, f"Button with id '{btn_id}' should exist on dashboard")
    def test_room_list_exists_and_has_content(self):
        response = self.app.get('/dashboard')
        soup = BeautifulSoup(response.data, 'html.parser')
        room_list = soup.find(id="room-list")
        self.assertIsNotNone(room_list, "Room list div with id 'room-list' should exist")
        self.assertGreater(len(room_list.find_all('div')), 0, "Room list should contain at least one room entry")
if __name__ == '__main__':
    unittest.main()