import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_test import CustomTestRunner
from utils_win import get_python_pid


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up code path for data file access."""
        cls.code_path = 'data'

    def setUp(self):
        """Set up the Selenium WebDriver before each test (WSL headless mode)."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        prefs = {"profile.password_manager_leak_detection": False}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "featured-jobs").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-jobs-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-applications-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "companies-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "listings-page").is_displayed())

    # ===== Job Listings Page Tests =====
    def test_listings_page_elements(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.assertTrue(self.driver.find_element(By.ID, "listings-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "location-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "jobs-grid").is_displayed())

    def test_listings_page_functionality(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        jobs_grid = self.driver.find_element(By.ID, "jobs-grid").text
        # Verify jobs from data file are displayed
        with open(f'{self.code_path}/jobs.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "jobs.txt is empty")
            first_job = lines[0].split('|')
            job_title = first_job[1]
            self.assertIn(job_title, jobs_grid)

    # ===== Job Details Page Tests =====
    def test_job_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.driver.find_element(By.ID, "view-job-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "job-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "job-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "job-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "company-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "job-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-now-button").is_displayed())

    def test_job_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.driver.find_element(By.ID, "view-job-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "job-details-page")))
        # Verify job details match data file
        with open(f'{self.code_path}/jobs.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "jobs.txt is empty")
            expected_data = first_line.split('|')
            expected_title = expected_data[1]
            title = self.driver.find_element(By.ID, "job-title").text
            self.assertIn(expected_title, title)

    # ===== Application Form Page Tests =====
    def test_application_form_page_elements(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.driver.find_element(By.ID, "view-job-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "job-details-page")))
        self.driver.find_element(By.ID, "apply-now-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "application-form-page")))
        self.assertTrue(self.driver.find_element(By.ID, "application-form-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applicant-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applicant-email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cover-letter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-application-button").is_displayed())

    def test_application_form_page_functionality(self):
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listings-page")))
        self.driver.find_element(By.ID, "view-job-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "job-details-page")))
        self.driver.find_element(By.ID, "apply-now-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "application-form-page")))
        self.driver.find_element(By.ID, "applicant-name").send_keys("Test Applicant")
        name = self.driver.find_element(By.ID, "applicant-name").get_attribute("value")
        self.assertEqual(name, "Test Applicant")

    # ===== Application Tracking Page Tests =====
    def test_tracking_page_elements(self):
        self.driver.find_element(By.ID, "my-applications-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tracking-page")))
        self.assertTrue(self.driver.find_element(By.ID, "tracking-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applications-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "status-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_tracking_page_functionality(self):
        self.driver.find_element(By.ID, "my-applications-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tracking-page")))
        applications_table = self.driver.find_element(By.ID, "applications-table").text
        # Verify applications from data file are displayed
        with open(f'{self.code_path}/applications.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_application = lines[0].split('|')
                applicant_name = first_application[2]
                self.assertIn(applicant_name, applications_table)

    # ===== Companies Directory Page Tests =====
    def test_companies_page_elements(self):
        self.driver.find_element(By.ID, "companies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "companies-page")))
        self.assertTrue(self.driver.find_element(By.ID, "companies-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "companies-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-company-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_companies_page_functionality(self):
        self.driver.find_element(By.ID, "companies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "companies-page")))
        companies_list = self.driver.find_element(By.ID, "companies-list").text
        # Verify companies from data file are displayed
        with open(f'{self.code_path}/companies.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "companies.txt is empty")
            first_company = lines[0].split('|')
            company_name = first_company[1]
            self.assertIn(company_name, companies_list)

    # ===== Company Profile Page Tests =====
    def test_company_profile_page_elements(self):
        self.driver.find_element(By.ID, "companies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "companies-page")))
        self.driver.find_element(By.ID, "view-company-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "company-profile-page")))
        self.assertTrue(self.driver.find_element(By.ID, "company-profile-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "company-info").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "company-jobs").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-companies").is_displayed())

    def test_company_profile_page_functionality(self):
        self.driver.find_element(By.ID, "companies-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "companies-page")))
        self.driver.find_element(By.ID, "view-company-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "company-profile-page")))
        # Verify company info matches data file
        with open(f'{self.code_path}/companies.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "companies.txt is empty")
            expected_data = first_line.split('|')
            expected_name = expected_data[1]
            company_info = self.driver.find_element(By.ID, "company-info").text
            self.assertIn(expected_name, company_info)

    # ===== Resume Management Page Tests =====
    def test_resume_page_elements(self):
        self.driver.get("http://localhost:5000/resumes")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "resume-page")))
        self.assertTrue(self.driver.find_element(By.ID, "resume-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "resumes-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "upload-resume-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_resume_page_functionality(self):
        self.driver.get("http://localhost:5000/resumes")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "resume-page")))
        resumes_list = self.driver.find_element(By.ID, "resumes-list").text
        # Verify resumes from data file are displayed
        with open(f'{self.code_path}/resumes.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_resume = lines[0].split('|')
                applicant_name = first_resume[1]
                self.assertIn(applicant_name, resumes_list)

    # ===== Search Results Page Tests =====
    def test_search_results_page_elements(self):
        self.driver.get("http://localhost:5000/search?q=developer")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-results-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-results-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-query-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "results-tabs").is_displayed())

    def test_search_results_page_functionality(self):
        self.driver.get("http://localhost:5000/search?q=developer")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-results-page")))
        query_display = self.driver.find_element(By.ID, "search-query-display").text
        self.assertIsNotNone(query_display)


class TestJobBoard:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')
        self.pid = get_python_pid()
        self.py = path
        self.code_path = code_path

    def test_set_up(self):
        try:
            self.process = subprocess.Popen(['python', self.py])
            time.sleep(2)
            return 1
        except:
            return 0

    def tear_down(self):
        if os.path.exists('data'):
            shutil.rmtree('data')
        self.process.terminate()

    def main(self):
        result = {'total': 18, 'total_basic': 9, 'total_advanced': 9, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
        res = None

        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except Exception as e:
            print(f"ERROR during setup: {e}")
            self.tear_down()
            return result

        if result['test_cases']['set_up'] == 1:
            try:
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except Exception as e:
                print(f"ERROR during test execution: {e}")
                self.tear_down()
                return result
        else:
            print("Setup failed, skipping tests")
            self.tear_down()
            return result

        self.tear_down()

        if res is not None:
            for test in res['succ']:
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 1
            for test in res['fail']:
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 0

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]
        return result


if __name__ == '__main__':
    import glob
    def find_app_py(app_name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pattern = os.path.join(base_dir, 'no_login_web', f'{app_name}', 'app.py')
        if os.path.exists(pattern):
            return pattern
        return None

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('JobBoard')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestJobBoard(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
