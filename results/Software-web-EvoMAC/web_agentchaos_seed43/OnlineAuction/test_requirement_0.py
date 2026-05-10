'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of all pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineAuctionTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_02_dashboard_elements(self):
        # Test Task 2 & 3: Dashboard page elements and content
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div with id dashboard-page
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "dashboard-page div not found")
        # Check featured auctions div
        featured_div = soup.find(id='featured-auctions')
        self.assertIsNotNone(featured_div, "featured-auctions div not found")
        # Check buttons for navigation
        browse_btn = soup.find(id='browse-auctions-button')
        self.assertIsNotNone(browse_btn, "browse-auctions-button not found")
        view_bids_btn = soup.find(id='view-bids-button')
        self.assertIsNotNone(view_bids_btn, "view-bids-button not found")
        trending_btn = soup.find(id='trending-auctions-button')
        self.assertIsNotNone(trending_btn, "trending-auctions-button not found")
    def test_03_auction_catalog_page_elements(self):
        # Test Auction Catalog page elements presence
        response = self.client.get('/auction-catalog')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='catalog-page'), "catalog-page div not found")
        self.assertIsNotNone(soup.find(id='search-input'), "search-input not found")
        self.assertIsNotNone(soup.find(id='category-filter'), "category-filter dropdown not found")
        self.assertIsNotNone(soup.find(id='auctions-grid'), "auctions-grid div not found")
        # Check at least one view-auction-button-{auction_id} button exists
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-auction-button-')]
        self.assertTrue(len(view_buttons) > 0, "No view-auction-button-{auction_id} buttons found")
    def test_04_auction_details_page_elements(self):
        # Use example auction_id=1 from example data
        response = self.client.get('/auction-details/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='auction-details-page'), "auction-details-page div not found")
        self.assertIsNotNone(soup.find(id='auction-title'), "auction-title not found")
        self.assertIsNotNone(soup.find(id='auction-description'), "auction-description not found")
        self.assertIsNotNone(soup.find(id='current-bid'), "current-bid not found")
        self.assertIsNotNone(soup.find(id='place-bid-button'), "place-bid-button not found")
        self.assertIsNotNone(soup.find(id='bid-history'), "bid-history div not found")
    def test_05_place_bid_page_elements(self):
        # GET request to place bid page for auction_id=1
        response = self.client.get('/place-bid/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='place-bid-page'), "place-bid-page div not found")
        self.assertIsNotNone(soup.find(id='bidder-name'), "bidder-name input not found")
        self.assertIsNotNone(soup.find(id='bid-amount'), "bid-amount input not found")
        self.assertIsNotNone(soup.find(id='auction-name'), "auction-name div not found")
        self.assertIsNotNone(soup.find(id='minimum-bid'), "minimum-bid div not found")
        self.assertIsNotNone(soup.find(id='submit-bid-button'), "submit-bid-button not found")
    def test_06_bid_history_page_elements(self):
        response = self.client.get('/bid-history')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='bid-history-page'), "bid-history-page div not found")
        self.assertIsNotNone(soup.find(id='bids-table'), "bids-table not found")
        self.assertIsNotNone(soup.find(id='filter-by-auction'), "filter-by-auction dropdown not found")
        self.assertIsNotNone(soup.find(id='sort-by-amount'), "sort-by-amount button not found")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "back-to-dashboard button not found")
    def test_07_auction_categories_page_elements(self):
        response = self.client.get('/auction-categories')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='categories-page'), "categories-page div not found")
        self.assertIsNotNone(soup.find(id='categories-list'), "categories-list div not found")
        # Check at least one category-card-{category_id} div exists
        category_cards = [div for div in soup.find_all('div') if div.get('id', '').startswith('category-card-')]
        self.assertTrue(len(category_cards) > 0, "No category-card-{category_id} divs found")
        # Check at least one view-category-button-{category_id} button exists
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-category-button-')]
        self.assertTrue(len(view_buttons) > 0, "No view-category-button-{category_id} buttons found")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "back-to-dashboard button not found")
    def test_08_winners_page_elements(self):
        response = self.client.get('/winners')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='winners-page'), "winners-page div not found")
        self.assertIsNotNone(soup.find(id='winners-list'), "winners-list div not found")
        # Check at least one winner-card-{auction_id} div exists
        winner_cards = [div for div in soup.find_all('div') if div.get('id', '').startswith('winner-card-')]
        self.assertTrue(len(winner_cards) > 0, "No winner-card-{auction_id} divs found")
        self.assertIsNotNone(soup.find(id='filter-by-winner'), "filter-by-winner input not found")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "back-to-dashboard button not found")
    def test_09_trending_auctions_page_elements(self):
        response = self.client.get('/trending-auctions')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='trending-page'), "trending-page div not found")
        self.assertIsNotNone(soup.find(id='trending-list'), "trending-list div not found")
        self.assertIsNotNone(soup.find(id='time-range-filter'), "time-range-filter dropdown not found")
        # Check at least one view-auction-button-{auction_id} button exists
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-auction-button-')]
        self.assertTrue(len(view_buttons) > 0, "No view-auction-button-{auction_id} buttons found")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "back-to-dashboard button not found")
    def test_10_auction_status_page_elements(self):
        response = self.client.get('/auction-status')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='status-page'), "status-page div not found")
        self.assertIsNotNone(soup.find(id='status-filter'), "status-filter dropdown not found")
        self.assertIsNotNone(soup.find(id='status-table'), "status-table not found")
        self.assertIsNotNone(soup.find(id='refresh-status-button'), "refresh-status-button not found")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "back-to-dashboard button not found")
if __name__ == '__main__':
    unittest.main()