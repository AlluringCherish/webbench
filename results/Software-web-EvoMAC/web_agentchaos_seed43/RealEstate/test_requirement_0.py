'''
Test cases for RealEstate web application to verify:
- Task 1: Website accessibility on local port 5000 (Dashboard page)
- Task 2: Dashboard page loads correctly with featured properties, recent listings, and navigation buttons
- Task 3: Presence and correctness of all specified elements on the Dashboard page as per requirements
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class RealEstateDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_website_accessibility(self):
        # Task 1: Test if the website is accessible on local port 5000 (root route '/')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Task 2 & 3: Test if Dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check page title
        title = soup.find('title')
        self.assertIsNotNone(title, "Page should have a <title> element")
        self.assertEqual(title.text.strip(), "Real Estate Dashboard", "Page title should be 'Real Estate Dashboard'")
        # Check featured properties section and id
        featured_section = dashboard_div.find('section', id='featured-properties')
        self.assertIsNotNone(featured_section, "Featured properties section with id 'featured-properties' should be present")
        featured_heading = featured_section.find('h2')
        self.assertIsNotNone(featured_heading)
        self.assertEqual(featured_heading.text.strip(), "Featured Properties")
        # Check recent listings section and id
        recent_section = dashboard_div.find('section', id='recent-listings')
        self.assertIsNotNone(recent_section, "Recent listings section with id 'recent-listings' should be present")
        recent_heading = recent_section.find('h2')
        self.assertIsNotNone(recent_heading)
        self.assertEqual(recent_heading.text.strip(), "Recent Listings")
        # Check navigation buttons container and buttons with correct ids
        nav = dashboard_div.find('nav', id='dashboard-navigation')
        self.assertIsNotNone(nav, "Navigation container with id 'dashboard-navigation' should be present")
        browse_button = nav.find('button', id='browse-properties-button')
        self.assertIsNotNone(browse_button, "Button with id 'browse-properties-button' should be present")
        self.assertIn('Browse Properties', browse_button.text)
        inquiries_button = nav.find('button', id='my-inquiries-button')
        self.assertIsNotNone(inquiries_button, "Button with id 'my-inquiries-button' should be present")
        self.assertIn('My Inquiries', inquiries_button.text)
        favorites_button = nav.find('button', id='my-favorites-button')
        self.assertIsNotNone(favorites_button, "Button with id 'my-favorites-button' should be present")
        self.assertIn('My Favorites', favorites_button.text)
        # Check that featured properties and recent listings contain property cards with required info and buttons
        for section in [featured_section, recent_section]:
            property_cards = section.find_all('div', class_='property-card')
            # Property cards may be empty if no data, but if present check structure
            for card in property_cards:
                # Check for address in h3
                address = card.find('h3')
                self.assertIsNotNone(address, "Property card should have an h3 with address")
                self.assertTrue(address.text.strip() != '', "Property address should not be empty")
                # Check for location paragraph
                location_p = card.find('p', text=lambda t: t and 'Location:' in t)
                self.assertIsNotNone(location_p, "Property card should have a paragraph with location info")
                # Check for price paragraph
                price_p = card.find('p', text=lambda t: t and 'Price:' in t)
                self.assertIsNotNone(price_p, "Property card should have a paragraph with price info")
                # Check for beds and baths paragraph
                beds_baths_p = card.find('p', text=lambda t: t and 'Beds:' in t and 'Baths:' in t)
                self.assertIsNotNone(beds_baths_p, "Property card should have a paragraph with beds and baths info")
                # Check for form with button to view details with correct id pattern
                form = card.find('form')
                self.assertIsNotNone(form, "Property card should have a form for view details button")
                button = form.find('button')
                self.assertIsNotNone(button, "Form should contain a button")
                self.assertTrue(button.has_attr('id'), "View details button should have an id")
                self.assertTrue(button['id'].startswith('view-property-button-'), "View details button id should start with 'view-property-button-'")
if __name__ == '__main__':
    unittest.main()