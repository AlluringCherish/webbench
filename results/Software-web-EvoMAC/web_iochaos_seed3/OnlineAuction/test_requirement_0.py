'''
Testing Task 1, 2, 3:
- Test whether the website can be accessed through local port 5000 (root route '/').
- Test whether the first page (Dashboard) loads correctly with required elements.
- Test basic navigation buttons on Dashboard page.
- Test presence and correctness of specified elements on Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestOnlineAuctionDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_root_route_accessible(self):
        # Test that root route '/' is accessible and returns 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Root route '/' should be accessible and return status 200")
    def test_dashboard_page_title(self):
        # Test that the page title is "Auction Dashboard"
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Auction Dashboard", "Dashboard page title should be 'Auction Dashboard'")
    def test_dashboard_page_main_div(self):
        # Test presence of main container div with id 'dashboard-page'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page should contain div with id 'dashboard-page'")
    def test_featured_auctions_section(self):
        # Test presence of featured auctions section with id 'featured-auctions'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find('section', id='featured-auctions')
        self.assertIsNotNone(featured_section, "Dashboard page should contain section with id 'featured-auctions'")
        # If featured auctions exist, check for auction cards and required elements
        auction_cards = featured_section.find_all('div', class_='auction-card')
        # We do not know if example data is present, so if cards exist, check their structure
        for card in auction_cards:
            img = card.find('img')
            self.assertIsNotNone(img, "Each featured auction card should have an image")
            self.assertTrue(img.has_attr('src'), "Image should have src attribute")
            h3 = card.find('h3')
            self.assertIsNotNone(h3, "Each featured auction card should have a title in h3")
            current_bid_p = card.find('p', text=lambda t: t and 'Current Bid:' in t)
            self.assertIsNotNone(current_bid_p, "Each featured auction card should display current bid")
            ends_p = card.find('p', text=lambda t: t and 'Ends:' in t)
            self.assertIsNotNone(ends_p, "Each featured auction card should display end time")
            view_button = card.find('button', id=lambda x: x and x.startswith('view-auction-button-'))
            self.assertIsNotNone(view_button, "Each featured auction card should have a 'View Details' button with correct id")
    def test_trending_auctions_section(self):
        # Test presence of trending auctions section with id 'trending-auctions'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        trending_section = soup.find('section', id='trending-auctions')
        self.assertIsNotNone(trending_section, "Dashboard page should contain section with id 'trending-auctions'")
        # If trending auctions exist, check for list items and required elements
        list_items = trending_section.find_all('li')
        for li in list_items:
            # Check for rank, item name, current bid, bid count text presence
            text = li.get_text()
            self.assertIn('#', text, "Trending auction list item should contain rank")
            self.assertIn('Current Bid:', text, "Trending auction list item should contain current bid")
            self.assertIn('Bids:', text, "Trending auction list item should contain bid count")
            # Check for view details button with correct id
            view_button = li.find('button', id=lambda x: x and x.startswith('view-auction-button-'))
            self.assertIsNotNone(view_button, "Trending auction list item should have a 'View Details' button with correct id")
    def test_dashboard_navigation_buttons(self):
        # Test presence and functionality of navigation buttons on dashboard
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        nav = soup.find('nav', class_='dashboard-navigation')
        self.assertIsNotNone(nav, "Dashboard page should have a navigation section with class 'dashboard-navigation'")
        browse_btn = nav.find('button', id='browse-auctions-button')
        self.assertIsNotNone(browse_btn, "Dashboard should have 'Browse Auctions' button with id 'browse-auctions-button'")
        self.assertIn("Browse Auctions", browse_btn.text)
        view_bids_btn = nav.find('button', id='view-bids-button')
        self.assertIsNotNone(view_bids_btn, "Dashboard should have 'View Bid History' button with id 'view-bids-button'")
        self.assertIn("View Bid History", view_bids_btn.text)
        trending_btn = nav.find('button', id='trending-auctions-button')
        self.assertIsNotNone(trending_btn, "Dashboard should have 'Trending Auctions' button with id 'trending-auctions-button'")
        self.assertIn("Trending Auctions", trending_btn.text)
    def test_navigation_buttons_redirect(self):
        # Test that navigation buttons link to correct URLs by simulating clicks (GET requests)
        # Browse Auctions button -> /catalog
        response = self.client.get('/catalog')
        self.assertEqual(response.status_code, 200, "Browse Auctions page should be accessible at /catalog")
        # View Bid History button -> /bid_history
        response = self.client.get('/bid_history')
        self.assertEqual(response.status_code, 200, "Bid History page should be accessible at /bid_history")
        # Trending Auctions button -> /trending
        response = self.client.get('/trending')
        self.assertEqual(response.status_code, 200, "Trending Auctions page should be accessible at /trending")
if __name__ == '__main__':
    unittest.main()