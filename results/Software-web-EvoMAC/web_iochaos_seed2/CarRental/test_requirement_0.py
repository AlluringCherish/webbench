'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of all specified elements as per the requirements.
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
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test that the page title is "Car Rental Dashboard"
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        self.assertEqual(title, "Car Rental Dashboard", "Dashboard page title should be 'Car Rental Dashboard'")
    def test_dashboard_main_container(self):
        # Test presence of main container div with id 'dashboard-page'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page should contain div with id 'dashboard-page'")
    def test_featured_vehicles_section(self):
        # Test presence of featured vehicles section with id 'featured-vehicles'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_div = soup.find('div', id='featured-vehicles')
        self.assertIsNotNone(featured_div, "Dashboard page should contain div with id 'featured-vehicles'")
        # Check that at least one vehicle card is present if example data is loaded
        vehicle_cards = featured_div.find_all('div', class_='vehicle-card')
        self.assertTrue(len(vehicle_cards) > 0, "Featured vehicles section should contain vehicle cards")
    def test_promotions_section(self):
        # Test presence of promotions section with id 'promotions-section'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        promo_div = soup.find('div', id='promotions-section')
        self.assertIsNotNone(promo_div, "Dashboard page should contain div with id 'promotions-section'")
        # Check that promotions list is present and has list items
        ul = promo_div.find('ul')
        self.assertIsNotNone(ul, "Promotions section should contain a list (ul)")
        li_items = ul.find_all('li') if ul else []
        self.assertTrue(len(li_items) > 0, "Promotions list should contain at least one promotion")
    def test_navigation_buttons_presence_and_ids(self):
        # Test presence of navigation buttons with correct IDs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        search_btn = soup.find('button', id='search-vehicles-button')
        reservations_btn = soup.find('button', id='my-reservations-button')
        self.assertIsNotNone(search_btn, "Dashboard should have button with id 'search-vehicles-button'")
        self.assertIsNotNone(reservations_btn, "Dashboard should have button with id 'my-reservations-button'")
    def test_navigation_buttons_functionality(self):
        # Test that navigation buttons link to correct pages by simulating clicks (checking href in onclick)
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        search_btn = soup.find('button', id='search-vehicles-button')
        reservations_btn = soup.find('button', id='my-reservations-button')
        self.assertIn('/vehicle_search', search_btn['onclick'], "Search Vehicles button should navigate to /vehicle_search")
        self.assertIn('/my_reservations', reservations_btn['onclick'], "My Reservations button should navigate to /my_reservations")
if __name__ == '__main__':
    unittest.main()