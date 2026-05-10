'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from app import app
class CarRentalDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access root '/' and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2 & 3: Check page title and key elements presence in Dashboard page
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Car Rental Dashboard</title>', html, "Dashboard page title should be correct")
        # Check container div id
        self.assertIn('id="dashboard-page"', html, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured vehicles section
        self.assertIn('id="featured-vehicles"', html, "Featured vehicles section with id 'featured-vehicles' should be present")
        # Check promotions section
        self.assertIn('id="promotions-section"', html, "Promotions section with id 'promotions-section' should be present")
        # Check buttons for navigation
        self.assertIn('id="search-vehicles-button"', html, "Button with id 'search-vehicles-button' should be present")
        self.assertIn('id="my-reservations-button"', html, "Button with id 'my-reservations-button' should be present")
        # Check that featured vehicles are displayed (based on example data, Toyota Camry, Honda CR-V, BMW X5)
        self.assertIn('Toyota Camry', html, "Featured vehicle 'Toyota Camry' should be displayed")
        self.assertIn('Honda CR-V', html, "Featured vehicle 'Honda CR-V' should be displayed")
        self.assertIn('BMW X5', html, "Featured vehicle 'BMW X5' should be displayed")
        # Check that promotions text is present
        self.assertIn('10% off for rentals over 7 days!', html, "Promotion text should be present")
        self.assertIn('Free GPS with every SUV rental!', html, "Promotion text should be present")
        self.assertIn('Weekend special: Luxury cars at 20% discount!', html, "Promotion text should be present")
    def test_dashboard_navigation_links(self):
        # Test that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check link to vehicle search page
        self.assertIn('href="/search"', html, "Search Vehicles button should link to /search")
        # Check link to reservations page
        self.assertIn('href="/reservations"', html, "My Reservations button should link to /reservations")
if __name__ == '__main__':
    unittest.main()