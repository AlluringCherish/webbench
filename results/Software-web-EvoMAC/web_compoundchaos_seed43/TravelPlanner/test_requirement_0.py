'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page (Dashboard) of the website loads correctly and basic navigation buttons exist.
'''
import unittest
from app import app
class TravelPlannerBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET request
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Test that the dashboard page contains key elements by their IDs
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for container div id
        self.assertIn('id="dashboard-page"', html, "Dashboard page container div should be present")
        # Check for featured destinations div
        self.assertIn('id="featured-destinations"', html, "Featured destinations div should be present")
        # Check for upcoming trips div
        self.assertIn('id="upcoming-trips"', html, "Upcoming trips div should be present")
        # Check for browse destinations button
        self.assertIn('id="browse-destinations-button"', html, "Browse destinations button should be present")
        # Check for plan itinerary button
        self.assertIn('id="plan-itinerary-button"', html, "Plan itinerary button should be present")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons exist and have correct types
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check buttons by id and type
        self.assertIn('<button id="browse-destinations-button"', html, "Browse destinations button should be a button element")
        self.assertIn('<button id="plan-itinerary-button"', html, "Plan itinerary button should be a button element")
if __name__ == '__main__':
    unittest.main()