'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test whether basic navigation buttons on the Dashboard page work and lead to the correct pages.
Test the presence and correctness of key elements on the Dashboard page:
- ID: dashboard-page
- ID: featured-songs
- ID: browse-songs-button
- ID: my-playlists-button
- ID: trending-artists-button
'''
import unittest
from threading import Thread
import time
import requests
from bs4 import BeautifulSoup
# Assuming the main app is in a file named app.py and the Flask app instance is named 'app'
# We import the app here to run it in a separate thread for testing
try:
    from app import app
except ImportError:
    # If app.py or app instance is not found, fail the tests gracefully
    app = None
class TestMusicStreamingApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if app is None:
            raise unittest.SkipTest("Flask app instance not found. Skipping tests.")
        # Start the Flask app in a separate thread
        cls.server_thread = Thread(target=app.run, kwargs={'port':5000, 'debug':False, 'use_reloader':False})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        # Wait a bit for the server to start
        time.sleep(1)
    @classmethod
    def tearDownClass(cls):
        # Flask does not provide a direct way to stop the server programmatically.
        # Since the thread is daemon, it will exit when tests finish.
        pass
    def test_access_dashboard_page(self):
        """Test that the dashboard page is accessible at http://localhost:5000/"""
        url = "http://localhost:5000/"
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            self.fail("Could not connect to the server at port 5000.")
        self.assertEqual(response.status_code, 200, "Dashboard page did not return status 200.")
    def test_dashboard_page_elements(self):
        """Test presence of key elements on the dashboard page"""
        url = "http://localhost:5000/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Check container div
        dashboard_div = soup.find(id="dashboard-page")
        self.assertIsNotNone(dashboard_div, "dashboard-page div not found.")
        # Check featured songs div
        featured_songs = soup.find(id="featured-songs")
        self.assertIsNotNone(featured_songs, "featured-songs div not found.")
        # Check browse songs button
        browse_button = soup.find(id="browse-songs-button")
        self.assertIsNotNone(browse_button, "browse-songs-button not found.")
        self.assertEqual(browse_button.name, "button", "browse-songs-button is not a button element.")
        # Check my playlists button
        playlists_button = soup.find(id="my-playlists-button")
        self.assertIsNotNone(playlists_button, "my-playlists-button not found.")
        self.assertEqual(playlists_button.name, "button", "my-playlists-button is not a button element.")
        # Check trending artists button
        trending_button = soup.find(id="trending-artists-button")
        self.assertIsNotNone(trending_button, "trending-artists-button not found.")
        self.assertEqual(trending_button.name, "button", "trending-artists-button is not a button element.")
    def test_basic_navigation_from_dashboard(self):
        """Test that navigation buttons on dashboard lead to correct pages"""
        base_url = "http://localhost:5000"
        # Mapping of button IDs to expected page titles and URL paths
        navigation_tests = {
            "browse-songs-button": {
                "expected_title": "Song Catalog",
                "expected_path": "/songs"
            },
            "my-playlists-button": {
                "expected_title": "My Playlists",
                "expected_path": "/playlists"
            },
            "trending-artists-button": {
                "expected_title": "Artist Profiles",
                "expected_path": "/artists"
            }
        }
        # Get dashboard page content
        response = requests.get(base_url + "/")
        self.assertEqual(response.status_code, 200, "Dashboard page not accessible for navigation test.")
        soup = BeautifulSoup(response.text, 'html.parser')
        for button_id, info in navigation_tests.items():
            button = soup.find(id=button_id)
            self.assertIsNotNone(button, f"Button {button_id} not found on dashboard page.")
            # We expect the button to have an onclick or be inside a form or link that navigates
            # Since we cannot click buttons in requests, we simulate by requesting the expected path
            nav_response = requests.get(base_url + info["expected_path"])
            self.assertEqual(nav_response.status_code, 200, f"Navigation to {info['expected_path']} failed.")
            nav_soup = BeautifulSoup(nav_response.text, 'html.parser')
            # Check page title
            page_title = nav_soup.find('title')
            self.assertIsNotNone(page_title, f"Page title not found on {info['expected_path']}.")
            self.assertIn(info["expected_title"], page_title.text, f"Page title does not match on {info['expected_path']}.")
if __name__ == '__main__':
    unittest.main()