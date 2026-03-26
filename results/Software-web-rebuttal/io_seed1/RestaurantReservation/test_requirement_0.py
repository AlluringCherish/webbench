'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of all specified elements as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root page '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2 & 3: Check that dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' should be present")
        # Check welcome message h1 with id 'welcome-message' and contains username text
        welcome_h1 = dashboard_div.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_h1, "Welcome message h1 with id 'welcome-message' should be present")
        self.assertIn('Welcome,', welcome_h1.text, "Welcome message should contain 'Welcome,'")
        self.assertTrue(len(welcome_h1.text.strip()) > 8, "Welcome message should display username after 'Welcome,'")
        # Check featured dishes section and dish cards with buttons
        featured_section = dashboard_div.find('section', id='featured-dishes')
        self.assertIsNotNone(featured_section, "Featured dishes section with id 'featured-dishes' should be present")
        featured_grid = featured_section.find('div', id='featured-dishes-grid')
        self.assertIsNotNone(featured_grid, "Featured dishes grid div with id 'featured-dishes-grid' should be present")
        dish_cards = featured_grid.find_all('div', class_='dish-card')
        self.assertGreaterEqual(len(dish_cards), 1, "At least one featured dish card should be present")
        for card in dish_cards:
            # Each card should have a button with id 'view-dish-button-{dish_id}'
            button = card.find('button')
            self.assertIsNotNone(button, "Each dish card should have a 'View Details' button")
            self.assertTrue(button.has_attr('id'), "Button should have an id attribute")
            self.assertTrue(button['id'].startswith('view-dish-button-'), "Button id should start with 'view-dish-button-'")
        # Check upcoming reservations section
        upcoming_section = dashboard_div.find('section', id='upcoming-reservations')
        self.assertIsNotNone(upcoming_section, "Upcoming reservations section with id 'upcoming-reservations' should be present")
        # It should contain either a table or a paragraph "No upcoming reservations."
        table = upcoming_section.find('table')
        no_reservations_p = upcoming_section.find('p')
        self.assertTrue(table is not None or (no_reservations_p is not None and "No upcoming reservations." in no_reservations_p.text),
                        "Upcoming reservations section should contain a table or a 'No upcoming reservations.' message")
        # Check navigation buttons section and all required buttons by id
        nav_section = dashboard_div.find('section', id='navigation-buttons')
        self.assertIsNotNone(nav_section, "Navigation buttons section with id 'navigation-buttons' should be present")
        expected_button_ids = [
            'make-reservation-button',
            'view-menu-button',
            'back-to-dashboard',
            'my-reservations-button',
            'my-reviews-button',
            'waitlist-button',
            'profile-button'
        ]
        found_button_ids = [btn['id'] for btn in nav_section.find_all('button') if btn.has_attr('id')]
        for btn_id in expected_button_ids:
            self.assertIn(btn_id, found_button_ids, f"Navigation button with id '{btn_id}' should be present")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons lead to correct pages (only test GET requests)
        # We test the URLs behind the buttons by simulating GET requests to their endpoints
        routes = {
            'make_reservation': '/make_reservation',
            'menu': '/menu',
            'back_to_dashboard': '/back_to_dashboard',
            'my_reservations': '/my_reservations',
            'my_reviews': '/my_reviews',
            'waitlist': '/waitlist',
            'profile': '/profile'
        }
        for route_name, url in routes.items():
            response = self.client.get(url)
            # back_to_dashboard redirects to dashboard, so allow 302 or 200
            if route_name == 'back_to_dashboard':
                self.assertIn(response.status_code, (200, 302), f"Route {url} should be accessible")
            else:
                self.assertEqual(response.status_code, 200, f"Route {url} should be accessible")
if __name__ == '__main__':
    unittest.main()