'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence and correctness of:
- ID: dashboard-page (Div container)
- ID: featured-vehicles (Div container with featured vehicle cards)
- ID: search-vehicles-button (Button to navigate to vehicle search page)
- ID: my-reservations-button (Button to navigate to reservations page)
- ID: promotions-section (Div container with current promotions)
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class CarRentalDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the root URL '/' is accessible (simulating local port 5000)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements with correct IDs and content
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured-vehicles div
        featured_div = dashboard_div.find('section', id='featured-vehicles')
        self.assertIsNotNone(featured_div, "Featured vehicles section with id 'featured-vehicles' should be present")
        # Check that featured vehicles are displayed (based on example data, at least one vehicle)
        vehicle_cards = featured_div.find_all('div', class_='vehicle-card')
        self.assertTrue(len(vehicle_cards) > 0, "There should be at least one featured vehicle card displayed")
        # Check each vehicle card has a button with correct id pattern and link
        for card in vehicle_cards:
            button = card.find('button')
            self.assertIsNotNone(button, "Each vehicle card should have a 'View Details' button")
            self.assertTrue(button['id'].startswith('view-details-button-'), "Button id should start with 'view-details-button-'")
            # Check the button is inside an <a> tag with href to vehicle details page
            parent_a = button.find_parent('a')
            self.assertIsNotNone(parent_a, "Button should be wrapped in an <a> tag linking to vehicle details")
        # Check promotions-section div
        promotions_div = dashboard_div.find('section', id='promotions-section')
        self.assertIsNotNone(promotions_div, "Promotions section with id 'promotions-section' should be present")
        # Check that promotions are listed
        promotions_list = promotions_div.find('ul')
        self.assertIsNotNone(promotions_list, "Promotions section should contain a list of promotions")
        promotions_items = promotions_list.find_all('li')
        self.assertTrue(len(promotions_items) > 0, "There should be at least one promotion listed")
        # Check navigation buttons
        search_button = dashboard_div.find('button', id='search-vehicles-button')
        self.assertIsNotNone(search_button, "Search Vehicles button with id 'search-vehicles-button' should be present")
        self.assertIn('/search-vehicles', search_button.get('onclick', ''), "Search Vehicles button should navigate to /search-vehicles")
        reservations_button = dashboard_div.find('button', id='my-reservations-button')
        self.assertIsNotNone(reservations_button, "My Reservations button with id 'my-reservations-button' should be present")
        self.assertIn('/my-reservations', reservations_button.get('onclick', ''), "My Reservations button should navigate to /my-reservations")
if __name__ == '__main__':
    unittest.main()