'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page (Dashboard) of the website loads correctly and basic navigation buttons exist.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per the requirements document.
'''
import unittest
from main import app
class TravelPlannerDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_website_accessible(self):
        # Test if the root URL '/' is accessible (Task 1)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_loads_correctly(self):
        # Test if the Dashboard page loads and contains expected elements (Task 2 & 3)
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Travel Planner Dashboard</title>', html, "Dashboard page title missing or incorrect")
        # Check container div with id 'dashboard-page'
        self.assertIn('id="dashboard-page"', html, "Dashboard container div with id 'dashboard-page' missing")
        # Check featured destinations div
        self.assertIn('id="featured-destinations"', html, "Featured destinations div missing")
        # Check upcoming trips div
        self.assertIn('id="upcoming-trips"', html, "Upcoming trips div missing")
        # Check browse destinations button
        self.assertIn('id="browse-destinations-button"', html, "Browse destinations button missing")
        # Check plan itinerary button
        self.assertIn('id="plan-itinerary-button"', html, "Plan itinerary button missing")
    def test_navigation_buttons_functionality(self):
        # Test that navigation buttons link to correct pages (basic navigation)
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check browse destinations button links to /destinations
        self.assertIn('id="browse-destinations-button"', html)
        self.assertIn('href="/destinations"', html, "Browse destinations button should link to /destinations")
        # Check plan itinerary button links to /itinerary
        self.assertIn('id="plan-itinerary-button"', html)
        self.assertIn('href="/itinerary"', html, "Plan itinerary button should link to /itinerary")
if __name__ == '__main__':
    unittest.main()