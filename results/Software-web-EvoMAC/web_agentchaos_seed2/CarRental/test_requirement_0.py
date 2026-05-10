'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence and correctness of all specified elements as per requirements.
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
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check page title and main elements presence and correctness
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page title
        self.assertEqual(soup.title.string.strip(), "Car Rental Dashboard", "Page title should be 'Car Rental Dashboard'")
        # Check main container div with id dashboard-page
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured vehicles section
        featured_section = dashboard_div.find('section', id='featured-vehicles')
        self.assertIsNotNone(featured_section, "Featured vehicles section with id 'featured-vehicles' should be present")
        # There should be at least one featured vehicle card or a no vehicles message
        vehicle_cards = featured_section.find_all('div', class_='vehicle-card')
        no_vehicles_msg = featured_section.find('p')
        self.assertTrue(len(vehicle_cards) > 0 or (no_vehicles_msg and "No featured vehicles available." in no_vehicles_msg.text),
                        "Featured vehicles section should contain vehicle cards or a no vehicles message")
        # Check promotions section
        promotions_section = dashboard_div.find('section', id='promotions-section')
        self.assertIsNotNone(promotions_section, "Promotions section with id 'promotions-section' should be present")
        promo_list = promotions_section.find('ul')
        self.assertIsNotNone(promo_list, "Promotions section should contain a list of promotions")
        promo_items = promo_list.find_all('li')
        self.assertGreaterEqual(len(promo_items), 1, "There should be at least one promotion listed")
        # Check navigation buttons presence and correct ids
        nav = dashboard_div.find('nav')
        self.assertIsNotNone(nav, "Navigation element should be present")
        search_btn = nav.find('button', id='search-vehicles-button')
        self.assertIsNotNone(search_btn, "Button with id 'search-vehicles-button' should be present")
        reservations_btn = nav.find('button', id='my-reservations-button')
        self.assertIsNotNone(reservations_btn, "Button with id 'my-reservations-button' should be present")
        # Check other navigation buttons by text
        nav_buttons_text = [btn.text.strip() for btn in nav.find_all('button')]
        expected_buttons = ['Search Vehicles', 'My Reservations', 'Rental History', 'Special Requests', 'Locations']
        for btn_text in expected_buttons:
            self.assertIn(btn_text, nav_buttons_text, f"Navigation button '{btn_text}' should be present")
    def test_dashboard_navigation_links(self):
        # Test that navigation buttons link to correct routes
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        nav = soup.find('nav')
        self.assertIsNotNone(nav)
        # Check that buttons with ids have correct onclick URLs
        search_btn = nav.find('button', id='search-vehicles-button')
        self.assertIsNotNone(search_btn)
        self.assertIn('/vehicle_search', search_btn.get('onclick', ''), "Search Vehicles button should link to /vehicle_search")
        reservations_btn = nav.find('button', id='my-reservations-button')
        self.assertIsNotNone(reservations_btn)
        self.assertIn('/reservations', reservations_btn.get('onclick', ''), "My Reservations button should link to /reservations")
        # Check other buttons by onclick attribute
        buttons = nav.find_all('button')
        expected_routes = {
            'Rental History': '/rental_history',
            'Special Requests': '/special_requests',
            'Locations': '/locations'
        }
        for btn in buttons:
            text = btn.text.strip()
            if text in expected_routes:
                self.assertIn(expected_routes[text], btn.get('onclick', ''), f"Button '{text}' should link to {expected_routes[text]}")
if __name__ == '__main__':
    unittest.main()