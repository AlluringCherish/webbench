'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page (Dashboard) loads correctly and basic navigation buttons work.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class TravelPlannerDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2 & 3: Check page title and presence of key elements on Dashboard page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Travel Planner Dashboard</title>', html, "Dashboard page title should be correct")
        # Check container div id
        self.assertIn('id="dashboard-page"', html, "Dashboard container div should be present")
        # Check featured destinations section and id
        self.assertIn('id="featured-destinations"', html, "Featured destinations section should be present")
        # Check upcoming trips section and id
        self.assertIn('id="upcoming-trips"', html, "Upcoming trips section should be present")
        # Check browse destinations button and id
        self.assertIn('id="browse-destinations-button"', html, "Browse destinations button should be present")
        # Check plan itinerary button and id
        self.assertIn('id="plan-itinerary-button"', html, "Plan itinerary button should be present")
    def test_dashboard_navigation_buttons(self):
        # Test Task 2: Check that navigation buttons link to correct pages
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check browse destinations button onclick link
        self.assertIn("location.href='/destinations'", html, "Browse destinations button should link to /destinations")
        # Check plan itinerary button onclick link
        self.assertIn("location.href='/itinerary'", html, "Plan itinerary button should link to /itinerary")
if __name__ == '__main__':
    unittest.main()