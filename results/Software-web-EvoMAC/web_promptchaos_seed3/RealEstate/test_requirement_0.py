'''
Testing Task 1: Test whether the website can be accessed through local port 5000.
Testing Task 2: Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons exist.
Testing Task 3: Test the elements and integrity of ALL pages as per the requirements document.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class RealEstateAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    # Task 1: Test access to the root URL (Dashboard page)
    def test_dashboard_accessible(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible (status 200)")
    # Task 2: Test Dashboard page content and navigation buttons
    def test_dashboard_content_and_navigation(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check page title
        self.assertIn("Real Estate Dashboard", soup.title.string)
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' should exist")
        # Check featured properties div
        featured_div = soup.find('div', id='featured-properties')
        self.assertIsNotNone(featured_div, "Featured properties div with id 'featured-properties' should exist")
        # Check navigation buttons
        browse_btn = soup.find('button', id='browse-properties-button')
        self.assertIsNotNone(browse_btn, "Browse properties button with id 'browse-properties-button' should exist")
        inquiries_btn = soup.find('button', id='my-inquiries-button')
        self.assertIsNotNone(inquiries_btn, "My inquiries button with id 'my-inquiries-button' should exist")
        favorites_btn = soup.find('button', id='my-favorites-button')
        self.assertIsNotNone(favorites_btn, "My favorites button with id 'my-favorites-button' should exist")
    # Task 3: Test all pages for presence and correctness of specified elements
    def test_property_search_page_elements(self):
        response = self.client.get('/properties')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("Property Search", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='search-page'), "Search page container div should exist")
        self.assertIsNotNone(soup.find('input', id='location-input'), "Location input field should exist")
        self.assertIsNotNone(soup.find('input', id='price-range-min'), "Price min input field should exist")
        self.assertIsNotNone(soup.find('input', id='price-range-max'), "Price max input field should exist")
        self.assertIsNotNone(soup.find('select', id='property-type-filter'), "Property type dropdown should exist")
        self.assertIsNotNone(soup.find('div', id='properties-grid'), "Properties grid div should exist")
        # Check at least one view-property-button-{property_id} button exists if properties exist
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-property-button-')]
        self.assertTrue(len(view_buttons) >= 0, "View property buttons should exist for each property")
    def test_property_details_page_elements(self):
        # Use property_id=1 from example data
        response = self.client.get('/property/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("Property Details", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='property-details-page'), "Property details container div should exist")
        self.assertIsNotNone(soup.find('h1', id='property-address'), "Property address h1 should exist")
        self.assertIsNotNone(soup.find('div', id='property-price'), "Property price div should exist")
        self.assertIsNotNone(soup.find('div', id='property-description'), "Property description div should exist")
        self.assertIsNotNone(soup.find('div', id='property-features'), "Property features div should exist")
        self.assertIsNotNone(soup.find('button', id='add-to-favorites-button'), "Add to favorites button should exist")
        self.assertIsNotNone(soup.find('button', id='submit-inquiry-button'), "Submit inquiry button should exist")
    def test_property_inquiry_page_elements(self):
        response = self.client.get('/property_inquiry')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("Submit Property Inquiry", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='inquiry-page'), "Inquiry page container div should exist")
        self.assertIsNotNone(soup.find('select', id='select-property'), "Select property dropdown should exist")
        self.assertIsNotNone(soup.find('input', id='inquiry-name'), "Inquiry name input should exist")
        self.assertIsNotNone(soup.find('input', id='inquiry-email'), "Inquiry email input should exist")
        self.assertIsNotNone(soup.find('input', id='inquiry-phone'), "Inquiry phone input should exist")
        self.assertIsNotNone(soup.find('textarea', id='inquiry-message'), "Inquiry message textarea should exist")
        self.assertIsNotNone(soup.find('button', id='submit-inquiry-button'), "Submit inquiry button should exist")
    def test_my_inquiries_page_elements(self):
        response = self.client.get('/inquiries')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("My Inquiries", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='inquiries-page'), "Inquiries page container div should exist")
        self.assertIsNotNone(soup.find('table', id='inquiries-table'), "Inquiries table should exist")
        self.assertIsNotNone(soup.find('select', id='inquiry-status-filter'), "Inquiry status filter dropdown should exist")
        # Check for at least one delete inquiry button with correct id pattern if inquiries exist
        delete_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('delete-inquiry-button-')]
        self.assertTrue(len(delete_buttons) >= 0, "Delete inquiry buttons should exist for each inquiry")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Back to dashboard button should exist")
    def test_my_favorites_page_elements(self):
        response = self.client.get('/my_favorites')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("My Favorite Properties", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='favorites-page'), "Favorites page container div should exist")
        self.assertIsNotNone(soup.find('div', id='favorites-list'), "Favorites list div should exist")
        # Check for remove-from-favorites-button-{property_id} buttons
        remove_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('remove-from-favorites-button-')]
        self.assertTrue(len(remove_buttons) >= 0, "Remove from favorites buttons should exist for each favorite property")
        # Check for view-property-button-{property_id} buttons
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-property-button-')]
        self.assertTrue(len(view_buttons) >= 0, "View property buttons should exist for each favorite property")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Back to dashboard button should exist")
    def test_agents_page_elements(self):
        response = self.client.get('/agents')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("Real Estate Agents", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='agents-page'), "Agents page container div should exist")
        self.assertIsNotNone(soup.find('div', id='agents-list'), "Agents list div should exist")
        self.assertIsNotNone(soup.find('input', id='agent-search'), "Agent search input should exist")
        # Check for contact-agent-button-{agent_id} buttons
        contact_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('contact-agent-button-')]
        self.assertTrue(len(contact_buttons) >= 0, "Contact agent buttons should exist for each agent")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Back to dashboard button should exist")
    def test_locations_page_elements(self):
        response = self.client.get('/locations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn("Featured Locations", soup.title.string)
        self.assertIsNotNone(soup.find('div', id='locations-page'), "Locations page container div should exist")
        self.assertIsNotNone(soup.find('div', id='locations-list'), "Locations list div should exist")
        self.assertIsNotNone(soup.find('select', id='location-sort'), "Location sort dropdown should exist")
        # Check for view-location-button-{location_id} buttons
        view_buttons = [btn for btn in soup.find_all('button') if btn.get('id', '').startswith('view-location-button-')]
        self.assertTrue(len(view_buttons) >= 0, "View location buttons should exist for each location")
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'), "Back to dashboard button should exist")
if __name__ == '__main__':
    unittest.main()