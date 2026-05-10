'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from app import app
class CarRentalDashboardTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title_and_elements(self):
        # Test Task 2 & 3: Check page title and presence of key elements on dashboard page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Car Rental Dashboard</title>', html, "Dashboard page title should be correct")
        # Check container div with id dashboard-page
        self.assertIn('id="dashboard-page"', html, "Dashboard page container div should be present")
        # Check featured vehicles section div
        self.assertIn('id="featured-vehicles"', html, "Featured vehicles section should be present")
        # Check promotions section div
        self.assertIn('id="promotions-section"', html, "Promotions section should be present")
        # Check search vehicles button with correct id
        self.assertIn('id="search-vehicles-button"', html, "Search Vehicles button should be present")
        # Check my reservations button with correct id
        self.assertIn('id="my-reservations-button"', html, "My Reservations button should be present")
        # Check that buttons have correct onclick navigation to expected routes
        self.assertIn("onclick=\"location.href='/vehicles'\"", html, "Search Vehicles button should navigate to /vehicles")
        self.assertIn("onclick=\"location.href='/reservations'\"", html, "My Reservations button should navigate to /reservations")
    def test_dashboard_featured_vehicles_content(self):
        # Test that featured vehicles are displayed if available vehicles exist in data
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Since example data has available vehicles, check that at least one vehicle make/model is shown
        # Example vehicles: Toyota Camry, Honda CR-V, BMW X5
        self.assertTrue(
            ('Toyota Camry' in html) or ('Honda CR-V' in html) or ('BMW X5' in html),
            "At least one featured vehicle should be displayed on dashboard"
        )
if __name__ == '__main__':
    unittest.main()