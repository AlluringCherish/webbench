'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class VirtualMuseumDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (status 200)")
    def test_dashboard_page_title(self):
        # Test if the page title is correct in the dashboard page HTML
        response = self.client.get('/')
        self.assertIn(b'<title>Museum Dashboard</title>', response.data, "Dashboard page title should be 'Museum Dashboard'")
    def test_dashboard_elements_presence(self):
        # Test presence of all required elements by their IDs in the dashboard page HTML
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check container div
        self.assertIn('id="dashboard-page"', html, "Dashboard container div with id 'dashboard-page' should be present")
        # Check exhibition summary div
        self.assertIn('id="exhibition-summary"', html, "Exhibition summary div with id 'exhibition-summary' should be present")
        # Check navigation buttons by id
        expected_buttons = [
            'artifact-catalog-button',
            'exhibitions-button',
            'visitor-tickets-button',
            'virtual-events-button',
            'audio-guides-button'
        ]
        for btn_id in expected_buttons:
            self.assertIn(f'id="{btn_id}"', html, f"Button with id '{btn_id}' should be present on dashboard")
    def test_dashboard_exhibition_counts_displayed(self):
        # Test that total exhibitions and active exhibitions counts are displayed in the exhibition-summary div
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # We expect some text or numbers inside the exhibition-summary div
        start_index = html.find('id="exhibition-summary"')
        self.assertNotEqual(start_index, -1, "Exhibition summary div should be present")
        # Extract a snippet around exhibition-summary div to check for numbers
        snippet = html[start_index:start_index+500].lower()
        # Check for presence of numbers (at least one digit)
        import re
        self.assertRegex(snippet, r'\d+', "Exhibition summary should display numeric counts")
if __name__ == '__main__':
    unittest.main()