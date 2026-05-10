'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class FoodDeliveryAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test that the dashboard page has correct title
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Food Delivery Dashboard", "Dashboard page title should be 'Food Delivery Dashboard'")
    def test_dashboard_featured_restaurants_section(self):
        # Test presence of featured restaurants section and that it contains up to 3 restaurants
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_div = soup.find(id='featured-restaurants')
        self.assertIsNotNone(featured_div, "Dashboard should have a div with id 'featured-restaurants'")
        restaurant_cards = featured_div.find_all(class_='restaurant-card')
        self.assertLessEqual(len(restaurant_cards), 3, "Featured restaurants should be up to 3")
        # Check that each card contains name, cuisine, rating, and delivery time text
        for card in restaurant_cards:
            text = card.get_text()
            self.assertRegex(text, r'.+', "Featured restaurant card should contain text")
            self.assertRegex(text, r'Rating:', "Featured restaurant card should contain 'Rating:'")
            self.assertRegex(text, r'Delivery Time:', "Featured restaurant card should contain 'Delivery Time:'")
    def test_dashboard_popular_cuisines_section(self):
        # Test presence of popular cuisines section and that it contains up to 5 cuisines
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        popular_div = soup.find(id='popular-cuisines')
        self.assertIsNotNone(popular_div, "Dashboard should have a div with id 'popular-cuisines'")
        ul = popular_div.find('ul')
        self.assertIsNotNone(ul, "Popular cuisines section should contain a <ul> list")
        cuisines = ul.find_all('li')
        self.assertLessEqual(len(cuisines), 5, "Popular cuisines should be up to 5")
        for li in cuisines:
            self.assertTrue(li.get_text().strip(), "Cuisine list item should not be empty")
    def test_dashboard_navigation_buttons(self):
        # Test presence and correctness of navigation buttons with correct IDs and links
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        buttons = {
            'browse-restaurants-button': '/restaurants',
            'view-cart-button': '/cart',
            'active-orders-button': '/active_orders'
        }
        for btn_id, expected_href in buttons.items():
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Dashboard should have button with id '{btn_id}'")
            # The button uses onclick with location.href, extract href from onclick attribute
            onclick = btn.get('onclick', '')
            self.assertIn(expected_href, onclick, f"Button '{btn_id}' should navigate to '{expected_href}'")
if __name__ == '__main__':
    unittest.main()