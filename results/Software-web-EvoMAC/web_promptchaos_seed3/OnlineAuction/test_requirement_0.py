'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class TestOnlineAuctionDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Task 2: Check page title is "Auction Dashboard"
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        self.assertEqual(title, "Auction Dashboard", "Dashboard page title should be 'Auction Dashboard'")
    def test_dashboard_main_div_present(self):
        # Task 3: Check presence of main container div with id 'dashboard-page'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page must contain div with id 'dashboard-page'")
    def test_featured_auctions_section(self):
        # Task 3: Check presence of featured auctions section with id 'featured-auctions'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find('section', id='featured-auctions')
        self.assertIsNotNone(featured_section, "Dashboard page must contain section with id 'featured-auctions'")
    def test_trending_auctions_section(self):
        # Task 3: Check presence of trending auctions section with id 'trending-auctions-section'
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        trending_section = soup.find('section', id='trending-auctions-section')
        self.assertIsNotNone(trending_section, "Dashboard page must contain section with id 'trending-auctions-section'")
    def test_navigation_buttons_presence_and_links(self):
        # Task 3: Check presence of navigation buttons with correct ids and hrefs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        nav = soup.find('nav', id='dashboard-navigation')
        self.assertIsNotNone(nav, "Dashboard page must contain nav with id 'dashboard-navigation'")
        # Define expected buttons and their target endpoints
        expected_buttons = {
            'browse-auctions-button': '/catalog',
            'view-bids-button': '/bid_history',
            'trending-auctions-button': '/trending',
            'categories-button': '/categories',
            'winners-button': '/winners',
            'status-button': '/status'
        }
        for btn_id, target_url in expected_buttons.items():
            button = nav.find('button', id=btn_id)
            self.assertIsNotNone(button, f"Navigation button with id '{btn_id}' must be present")
            # Check onclick attribute contains correct URL
            onclick = button.get('onclick', '')
            self.assertIn(target_url, onclick, f"Button '{btn_id}' should navigate to '{target_url}'")
    def test_featured_auction_cards_elements(self):
        # Task 3: Check each featured auction card has image, title, current bid, end time, and view details button
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find('section', id='featured-auctions')
        if featured_section:
            cards = featured_section.find_all('div', class_='auction-card')
            for card in cards:
                # Image with class auction-image
                img = card.find('img', class_='auction-image')
                self.assertIsNotNone(img, "Featured auction card must have an image with class 'auction-image'")
                # Title h3
                title = card.find('h3')
                self.assertIsNotNone(title, "Featured auction card must have a title in <h3>")
                self.assertTrue(title.text.strip(), "Featured auction card title must not be empty")
                # Current bid paragraph
                current_bid_p = card.find('p', string=lambda text: text and 'Current Bid:' in text)
                self.assertIsNotNone(current_bid_p, "Featured auction card must display current bid")
                # End time paragraph
                end_time_p = card.find('p', string=lambda text: text and 'Ends:' in text)
                self.assertIsNotNone(end_time_p, "Featured auction card must display end time")
                # View details button with correct id
                auction_id = card.get('id', '').replace('featured-auction-', '')
                view_button = card.find('button', id=f'view-auction-button-{auction_id}')
                self.assertIsNotNone(view_button, "Featured auction card must have a 'View Details' button with correct id")
    def test_trending_auction_cards_elements(self):
        # Task 3: Check each trending auction card has rank, title, current bid, bid count, and view details button
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        trending_section = soup.find('section', id='trending-auctions-section')
        if trending_section:
            cards = trending_section.find_all('div', class_='trending-auction-card')
            for card in cards:
                # Rank span with class trending-rank
                rank_span = card.find('span', class_='trending-rank')
                self.assertIsNotNone(rank_span, "Trending auction card must have a rank span with class 'trending-rank'")
                self.assertTrue(rank_span.text.strip().startswith('#'), "Trending rank should start with '#'")
                # Title h3
                title = card.find('h3')
                self.assertIsNotNone(title, "Trending auction card must have a title in <h3>")
                self.assertTrue(title.text.strip(), "Trending auction card title must not be empty")
                # Current bid paragraph
                current_bid_p = card.find('p', string=lambda text: text and 'Current Bid:' in text)
                self.assertIsNotNone(current_bid_p, "Trending auction card must display current bid")
                # Bid count paragraph
                bid_count_p = card.find('p', string=lambda text: text and 'Bid Count:' in text)
                self.assertIsNotNone(bid_count_p, "Trending auction card must display bid count")
                # View details button with correct id
                auction_id = card.get('id', '').replace('trending-auction-', '')
                view_button = card.find('button', id=f'view-auction-button-{auction_id}')
                self.assertIsNotNone(view_button, "Trending auction card must have a 'View Details' button with correct id")
if __name__ == '__main__':
    unittest.main()