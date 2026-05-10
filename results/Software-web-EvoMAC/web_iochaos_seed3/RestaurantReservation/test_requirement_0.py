'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of all specified elements as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestRestaurantReservationDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title_and_welcome_message(self):
        # Test Task 2: Check page title and welcome message presence
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check page title
        self.assertEqual(soup.title.string, "Restaurant Dashboard", "Page title should be 'Restaurant Dashboard'")
        # Check welcome message element
        welcome = soup.find(id="welcome-message")
        self.assertIsNotNone(welcome, "Welcome message element with id 'welcome-message' should be present")
        self.assertTrue(welcome.text.strip().startswith("Welcome"), "Welcome message should start with 'Welcome'")
    def test_dashboard_buttons_presence_and_links(self):
        # Test Task 3: Check presence of all required buttons and their links
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Button IDs and expected href targets
        buttons = {
            "make-reservation-button": "/make_reservation",
            "view-menu-button": "/menu",
            "my-reservations-button": "/my_reservations",
            "my-reviews-button": "/my_reviews",
            "waitlist-button": "/waitlist",
            "profile-button": "/profile",
            "back-to-dashboard": "/"
        }
        for btn_id, expected_path in buttons.items():
            btn = soup.find(id=btn_id)
            self.assertIsNotNone(btn, f"Button with id '{btn_id}' should be present")
            # The button uses onclick with location.href, check the attribute
            onclick = btn.get('onclick', '')
            self.assertIn(expected_path, onclick, f"Button '{btn_id}' should navigate to '{expected_path}'")
    def test_featured_dishes_section(self):
        # Test Task 3: Check featured dishes section presence and content correctness
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find('div', class_='featured-dishes')
        self.assertIsNotNone(featured_section, "Featured dishes section should be present")
        dish_cards = featured_section.find_all('div', class_='dish-card')
        # According to example data, there should be up to 3 featured dishes
        self.assertTrue(1 <= len(dish_cards) <= 3, "There should be between 1 and 3 featured dishes displayed")
        for card in dish_cards:
            # Check dish name
            dish_name = card.find(class_='dish-name')
            self.assertIsNotNone(dish_name, "Each dish card should have a dish name element")
            self.assertTrue(len(dish_name.text.strip()) > 0, "Dish name should not be empty")
            # Check dish description
            dish_desc = card.find(class_='dish-description')
            self.assertIsNotNone(dish_desc, "Each dish card should have a dish description element")
            # Check dish price
            dish_price = card.find(class_='dish-price')
            self.assertIsNotNone(dish_price, "Each dish card should have a dish price element")
            self.assertTrue(dish_price.text.strip().startswith('$'), "Dish price should start with '$'")
            # Check view details button with correct id pattern
            view_btn = card.find('button', id=lambda x: x and x.startswith('view-dish-button-'))
            self.assertIsNotNone(view_btn, "Each dish card should have a 'View Details' button with correct id")
    def test_upcoming_reservations_section(self):
        # Test Task 3: Check upcoming reservations table or no reservations message
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check if table exists
        table = soup.find('table', class_='upcoming-reservations')
        no_reservations_msg = soup.find('p', class_='no-reservations')
        # At least one of them should be present
        self.assertTrue(table is not None or no_reservations_msg is not None,
                        "Either upcoming reservations table or no reservations message should be present")
        if table:
            # Check table headers
            headers = [th.text.strip() for th in table.find_all('th')]
            expected_headers = ['Date', 'Time', 'Party Size', 'Special Requests']
            self.assertEqual(headers, expected_headers, "Upcoming reservations table headers should match expected")
            # Check rows have correct number of columns
            rows = table.find_all('tbody')[0].find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                self.assertEqual(len(cols), 4, "Each reservation row should have 4 columns")
if __name__ == '__main__':
    unittest.main()