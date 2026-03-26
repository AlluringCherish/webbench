'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
Testing Task 3: Test the presence and correctness of specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineAuctionDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_server_running_and_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check that the Dashboard page contains required elements and buttons
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured auctions div with id 'featured-auctions'
        featured_div = soup.find('div', id='featured-auctions')
        self.assertIsNotNone(featured_div, "Featured auctions div with id 'featured-auctions' should be present")
        # Check buttons with correct ids
        browse_button = soup.find('button', id='browse-auctions-button')
        self.assertIsNotNone(browse_button, "Button with id 'browse-auctions-button' should be present")
        view_bids_button = soup.find('button', id='view-bids-button')
        self.assertIsNotNone(view_bids_button, "Button with id 'view-bids-button' should be present")
        trending_button = soup.find('button', id='trending-auctions-button')
        self.assertIsNotNone(trending_button, "Button with id 'trending-auctions-button' should be present")
    def test_dashboard_navigation_buttons(self):
        # Test Task 2: Check that navigation buttons link to correct URLs via JS or href
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Buttons may not have href but JS handles navigation, so check button presence and id only
        # We can simulate clicking by checking URLs in JS or by testing routes separately
        # Test that /catalog route is accessible
        catalog_resp = self.client.get('/catalog')
        self.assertEqual(catalog_resp.status_code, 200, "Catalog page should be accessible")
        # Test that /bid_history route is accessible
        bid_history_resp = self.client.get('/bid_history')
        self.assertEqual(bid_history_resp.status_code, 200, "Bid History page should be accessible")
        # Test that /trending route is accessible
        trending_resp = self.client.get('/trending')
        self.assertEqual(trending_resp.status_code, 200, "Trending Auctions page should be accessible")
if __name__ == '__main__':
    unittest.main()