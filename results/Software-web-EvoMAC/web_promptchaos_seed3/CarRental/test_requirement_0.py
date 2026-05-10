'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of the following elements:
- ID: dashboard-page (Div container)
- ID: featured-vehicles (Div container for featured vehicles)
- ID: search-vehicles-button (Button to navigate to vehicle search page)
- ID: my-reservations-button (Button to navigate to reservations page)
- ID: promotions-section (Div container for current promotions)
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class CarRentalDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully.")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements with correct IDs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully.")
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check dashboard-page div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container with id 'dashboard-page' not found.")
        # Check featured-vehicles div
        featured_div = soup.find('div', id='featured-vehicles')
        self.assertIsNotNone(featured_div, "Featured vehicles container with id 'featured-vehicles' not found.")
        # Check search-vehicles-button button
        search_button = soup.find('button', id='search-vehicles-button')
        self.assertIsNotNone(search_button, "Search vehicles button with id 'search-vehicles-button' not found.")
        self.assertIn('Search Vehicles', search_button.text, "Search vehicles button text incorrect.")
        # Check my-reservations-button button
        reservations_button = soup.find('button', id='my-reservations-button')
        self.assertIsNotNone(reservations_button, "My reservations button with id 'my-reservations-button' not found.")
        self.assertIn('My Reservations', reservations_button.text, "My reservations button text incorrect.")
        # Check promotions-section div
        promotions_div = soup.find('div', id='promotions-section')
        self.assertIsNotNone(promotions_div, "Promotions section with id 'promotions-section' not found.")
    def test_dashboard_featured_vehicles_content(self):
        # Test that featured vehicles are displayed correctly with required sub-elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully.")
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        featured_div = soup.find('div', id='featured-vehicles')
        self.assertIsNotNone(featured_div, "Featured vehicles container not found.")
        vehicle_cards = featured_div.find_all('div', class_='vehicle-card')
        self.assertTrue(len(vehicle_cards) > 0, "No vehicle cards found in featured vehicles.")
        for card in vehicle_cards:
            # Check vehicle-image div
            image_div = card.find('div', class_='vehicle-image')
            self.assertIsNotNone(image_div, "Vehicle image div missing in vehicle card.")
            # Check vehicle-name div
            name_div = card.find('div', class_='vehicle-name')
            self.assertIsNotNone(name_div, "Vehicle name div missing in vehicle card.")
            self.assertTrue(len(name_div.text.strip()) > 0, "Vehicle name is empty.")
            # Check vehicle-type div
            type_div = card.find('div', class_='vehicle-type')
            self.assertIsNotNone(type_div, "Vehicle type div missing in vehicle card.")
            self.assertTrue(len(type_div.text.strip()) > 0, "Vehicle type is empty.")
            # Check vehicle-rate div
            rate_div = card.find('div', class_='vehicle-rate')
            self.assertIsNotNone(rate_div, "Vehicle rate div missing in vehicle card.")
            self.assertRegex(rate_div.text.strip(), r'^\$\d+(\.\d{2})? per day$', "Vehicle rate format incorrect.")
            # Check view-details-link anchor
            details_link = card.find('a', class_='view-details-link')
            self.assertIsNotNone(details_link, "View details link missing in vehicle card.")
            self.assertTrue(details_link.has_attr('href'), "View details link missing href attribute.")
            self.assertTrue(details_link['href'].startswith('/vehicle/'), "View details link href incorrect.")
    def test_dashboard_navigation_buttons(self):
        # Test that clicking navigation buttons leads to correct pages (simulate GET requests)
        # Search Vehicles button leads to /search
        response_search = self.client.get('/search')
        self.assertEqual(response_search.status_code, 200, "Vehicle Search page did not load successfully.")
        # My Reservations button leads to /reservations
        response_reservations = self.client.get('/reservations')
        self.assertEqual(response_reservations.status_code, 200, "Reservations page did not load successfully.")
if __name__ == '__main__':
    unittest.main()