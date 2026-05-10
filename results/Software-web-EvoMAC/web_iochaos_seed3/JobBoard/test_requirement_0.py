'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page as the first page.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class JobBoardBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements as per requirements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check section with id 'featured-jobs'
        featured_jobs_section = dashboard_div.find('section', id='featured-jobs')
        self.assertIsNotNone(featured_jobs_section, "Featured jobs section with id 'featured-jobs' should be present")
        # Check that featured jobs are displayed (at most 3)
        job_cards = featured_jobs_section.find_all('div', class_='job-card')
        self.assertLessEqual(len(job_cards), 3, "There should be at most 3 featured job cards displayed")
        # For each job card, check presence of title, company, location, salary, and view details button
        for job_card in job_cards:
            # Job title h3
            title = job_card.find('h3')
            self.assertIsNotNone(title, "Job card should have a job title in <h3>")
            # Company name div with strong label
            company_div = job_card.find('div', string=lambda text: text and 'Company:' in text)
            self.assertIsNotNone(company_div, "Job card should display company name")
            # Location div with strong label
            location_div = job_card.find('div', string=lambda text: text and 'Location:' in text)
            self.assertIsNotNone(location_div, "Job card should display location")
            # Salary div with strong label
            salary_div = job_card.find('div', string=lambda text: text and 'Salary:' in text)
            self.assertIsNotNone(salary_div, "Job card should display salary range")
            # View Details button with id pattern 'view-job-button-{job_id}'
            form = job_card.find('form')
            self.assertIsNotNone(form, "Job card should have a form for view details button")
            button = form.find('button')
            self.assertIsNotNone(button, "View Details button should be present in job card")
            self.assertTrue(button['id'].startswith('view-job-button-'), "View Details button id should start with 'view-job-button-'")
        # Check navigation buttons with correct ids and that they link to correct URLs
        browse_jobs_button = soup.find('button', id='browse-jobs-button')
        self.assertIsNotNone(browse_jobs_button, "Browse Jobs button with id 'browse-jobs-button' should be present")
        self.assertIn('/jobs', browse_jobs_button.get('onclick', ''), "Browse Jobs button should navigate to /jobs")
        my_applications_button = soup.find('button', id='my-applications-button')
        self.assertIsNotNone(my_applications_button, "My Applications button with id 'my-applications-button' should be present")
        self.assertIn('/applications', my_applications_button.get('onclick', ''), "My Applications button should navigate to /applications")
        companies_button = soup.find('button', id='companies-button')
        self.assertIsNotNone(companies_button, "Companies button with id 'companies-button' should be present")
        self.assertIn('/companies', companies_button.get('onclick', ''), "Companies button should navigate to /companies")
if __name__ == '__main__':
    unittest.main()