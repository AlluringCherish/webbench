'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the presence and correctness of all specified elements on the Dashboard page as per requirements.
'''
import unittest
from main import app
class TestOnlineAuctionDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_website_accessible(self):
        # Test Task 1: Access root URL and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title_and_elements(self):
        # Test Task 2 and 3: Check page title and presence of required elements in HTML
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check page title
        self.assertIn('<title>Auction Dashboard</title>', html, "Dashboard page title should be 'Auction Dashboard'")
        # Check container div with id 'dashboard-page'
        self.assertIn('id="dashboard-page"', html, "Dashboard page should contain div with id 'dashboard-page'")
        # Check featured auctions container div
        self.assertIn('id="featured-auctions"', html, "Dashboard page should contain div with id 'featured-auctions'")
        # Check buttons for navigation with correct ids
        self.assertIn('id="browse-auctions-button"', html, "Dashboard page should have button with id 'browse-auctions-button'")
        self.assertIn('id="view-bids-button"', html, "Dashboard page should have button with id 'view-bids-button'")
        self.assertIn('id="trending-auctions-button"', html, "Dashboard page should have button with id 'trending-auctions-button'")
    def test_dashboard_navigation_buttons_functionality(self):
        # Test Task 2: Check that navigation buttons link to correct URLs
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check that browse auctions button links to /catalog
        self.assertIn('id="browse-auctions-button"', html)
        self.assertIn('/catalog', html, "Browse Auctions button should link to /catalog")
        # Check that view bids button links to /bid_history
        self.assertIn('id="view-bids-button"', html)
        self.assertIn('/bid_history', html, "View Bids button should link to /bid_history")
        # Check that trending auctions button links to /trending
        self.assertIn('id="trending-auctions-button"', html)
        self.assertIn('/trending', html, "Trending Auctions button should link to /trending")
if __name__ == '__main__':
    unittest.main()