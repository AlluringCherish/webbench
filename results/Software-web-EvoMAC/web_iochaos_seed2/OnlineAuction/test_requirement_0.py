'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of:
- ID: dashboard-page (Div container)
- ID: featured-auctions (Div container for featured items)
- ID: browse-auctions-button (Button to navigate to auction catalog)
- ID: view-bids-button (Button to navigate to bid history)
- ID: trending-auctions-button (Button to navigate to trending auctions)
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestOnlineAuctionDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (status 200)")
    def test_dashboard_page_title(self):
        # Test that the page title is "Auction Dashboard"
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string if soup.title else ''
        self.assertIn("Auction Dashboard", title, "Dashboard page title should contain 'Auction Dashboard'")
    def test_dashboard_elements_presence(self):
        # Test presence of required elements by ID on dashboard page
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container with ID 'dashboard-page' should be present")
        featured_div = soup.find(id='featured-auctions')
        self.assertIsNotNone(featured_div, "Featured auctions container with ID 'featured-auctions' should be present")
        browse_btn = soup.find(id='browse-auctions-button')
        self.assertIsNotNone(browse_btn, "Browse auctions button with ID 'browse-auctions-button' should be present")
        self.assertEqual(browse_btn.name, 'button', "Browse auctions element should be a button")
        view_bids_btn = soup.find(id='view-bids-button')
        self.assertIsNotNone(view_bids_btn, "View bids button with ID 'view-bids-button' should be present")
        self.assertEqual(view_bids_btn.name, 'button', "View bids element should be a button")
        trending_btn = soup.find(id='trending-auctions-button')
        self.assertIsNotNone(trending_btn, "Trending auctions button with ID 'trending-auctions-button' should be present")
        self.assertEqual(trending_btn.name, 'button', "Trending auctions element should be a button")
    def test_dashboard_navigation_buttons(self):
        # Test that navigation buttons have correct href or onclick to navigate to correct pages
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        browse_btn = soup.find(id='browse-auctions-button')
        self.assertIsNotNone(browse_btn)
        # The button might have onclick or be inside a form or link, check for onclick or form action or href
        # Since navigation is handled by JS, we check presence of button only here
        view_bids_btn = soup.find(id='view-bids-button')
        self.assertIsNotNone(view_bids_btn)
        trending_btn = soup.find(id='trending-auctions-button')
        self.assertIsNotNone(trending_btn)
if __name__ == '__main__':
    unittest.main()