'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation buttons work.
Test the presence and correctness of key elements on the Dashboard page:
- ID: dashboard-page (Div container)
- ID: featured-articles (Div container with featured articles)
- ID: browse-articles-button (Button to navigate to article catalog)
- ID: view-bookmarks-button (Button to navigate to bookmarks)
- ID: trending-articles-button (Button to navigate to trending articles)
Also verify that featured articles and trending articles are displayed based on example data.
'''
import unittest
from main import app
class TestDashboardPage(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET on '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_contains_required_elements(self):
        # Test that the dashboard page contains required elements by ID and content
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check for dashboard-page div container
        self.assertIn('id="dashboard-page"', html, "Dashboard page container div should be present")
        # Check for featured-articles section
        self.assertIn('id="featured-articles"', html, "Featured articles section should be present")
        # Check for browse-articles-button button
        self.assertIn('id="browse-articles-button"', html, "Browse articles button should be present")
        # Check for view-bookmarks-button button
        self.assertIn('id="view-bookmarks-button"', html, "View bookmarks button should be present")
        # Check for trending-articles-button button
        self.assertIn('id="trending-articles-button"', html, "Trending articles button should be present")
    def test_dashboard_featured_articles_displayed(self):
        # Test that featured articles are displayed with expected example data titles
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Example featured article titles from example data in requirements
        expected_titles = [
            "Breaking: New Technology Breakthrough",
            "Sports: Championship Victory",
            "Business: Market Trends Analysis"
        ]
        # At least one of the example titles should appear in featured articles section
        featured_section_start = html.find('id="featured-articles"')
        featured_section_end = html.find('</section>', featured_section_start)
        featured_section_html = html[featured_section_start:featured_section_end]
        found_any = any(title in featured_section_html for title in expected_titles)
        self.assertTrue(found_any, "At least one example featured article title should be displayed")
    def test_dashboard_trending_articles_displayed(self):
        # Test that trending articles (This Week) are displayed with expected example data titles
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Example trending article titles for 'This Week' period from example data
        expected_trending_titles = [
            "Breaking: New Technology Breakthrough",
            "Sports: Championship Victory"
        ]
        trending_section_start = html.find('id="trending-articles"')
        trending_section_end = html.find('</section>', trending_section_start)
        trending_section_html = html[trending_section_start:trending_section_end]
        found_any = any(title in trending_section_html for title in expected_trending_titles)
        self.assertTrue(found_any, "At least one example trending article title for 'This Week' should be displayed")
    def test_dashboard_navigation_buttons_functionality(self):
        # Test that navigation buttons have correct form actions and method GET
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        # Check browse articles button form action
        self.assertIn('form method="get" action="/catalog"', html, "Browse Articles button form should navigate to /catalog")
        # Check view bookmarks button form action
        self.assertIn('form method="get" action="/bookmarks"', html, "View Bookmarks button form should navigate to /bookmarks")
        # Check trending articles button form action
        self.assertIn('form method="get" action="/trending"', html, "Trending Articles button form should navigate to /trending")
if __name__ == '__main__':
    unittest.main()