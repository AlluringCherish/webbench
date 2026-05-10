'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence and correctness of all specified elements as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class VirtualMuseumDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_title(self):
        # Test Task 2: Check page title in HTML
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('title')
        self.assertIsNotNone(title, "Page should have a <title> element")
        self.assertEqual(title.text.strip(), "Museum Dashboard", "Page title should be 'Museum Dashboard'")
    def test_dashboard_elements_presence(self):
        # Test Task 3: Check presence of all specified elements on Dashboard page
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page should contain a div with id 'dashboard-page'")
        # Check exhibition summary div with id 'exhibition-summary'
        exhibition_summary = soup.find('div', id='exhibition-summary')
        self.assertIsNotNone(exhibition_summary, "Dashboard page should contain a div with id 'exhibition-summary'")
        # Check buttons with specified ids
        button_ids = [
            'artifact-catalog-button',
            'exhibitions-button',
            'visitor-tickets-button',
            'virtual-events-button',
            'audio-guides-button'
        ]
        for btn_id in button_ids:
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Dashboard page should contain a button with id '{btn_id}'")
    def test_dashboard_exhibition_summary_content(self):
        # Test Task 3: Check that exhibition summary shows total and active exhibitions counts as integers
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        exhibition_summary = soup.find('div', id='exhibition-summary')
        self.assertIsNotNone(exhibition_summary, "Exhibition summary div should be present")
        # The summary text should contain numbers for total exhibitions and active exhibitions
        text = exhibition_summary.get_text(strip=True)
        import re
        numbers = re.findall(r'\d+', text)
        self.assertTrue(len(numbers) >= 2, "Exhibition summary should contain at least two numbers (total and active exhibitions)")
        # Check that numbers are integers and non-negative
        for num in numbers:
            self.assertTrue(num.isdigit(), "Exhibition summary numbers should be digits")
            self.assertGreaterEqual(int(num), 0, "Exhibition summary numbers should be non-negative")
if __name__ == '__main__':
    unittest.main()