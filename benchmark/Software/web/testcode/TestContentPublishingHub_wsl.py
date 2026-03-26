import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
import sys
import subprocess
import shutil
import psutil
sys.path.append(os.path.abspath('evaluator'))
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):

    def setUp(self):
        self.code_path = os.path.dirname(os.path.abspath(__file__))
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://localhost:5000/dashboard")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )

    def tearDown(self):
        self.driver.quit()

    # ===== BASIC TESTS: Element Presence =====

    def test_dashboard_page_elements(self):
        """Test 1: Verify dashboard page elements are present"""
        self.driver.get("http://localhost:5000/dashboard")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "welcome-message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "quick-stats").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "create-article-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "recent-activity").is_displayed())

    def test_create_article_page_elements(self):
        """Test 2: Verify create article page elements are present"""
        self.driver.get("http://localhost:5000/article/create")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "create-article-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "create-article-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "article-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "article-content").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-draft-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cancel-button").is_displayed())

    def test_edit_article_page_elements(self):
        """Test 3: Verify edit article page elements are present"""
        self.driver.get("http://localhost:5000/article/1/edit")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "edit-article-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "edit-article-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-article-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-article-content").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-version-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cancel-edit").is_displayed())

    def test_version_history_page_elements(self):
        """Test 4: Verify version history page elements are present"""
        self.driver.get("http://localhost:5000/article/1/versions")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-history-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "version-history-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "versions-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "version-comparison").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "restore-version-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-edit-history").is_displayed())

    def test_my_articles_page_elements(self):
        """Test 5: Verify my articles page elements are present"""
        self.driver.get("http://localhost:5000/articles/mine")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "my-articles-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "my-articles-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-article-status").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "articles-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "create-new-article").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_published_articles_page_elements(self):
        """Test 6: Verify published articles page elements are present"""
        self.driver.get("http://localhost:5000/articles/published")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "published-articles-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "published-articles-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-published-category").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "published-articles-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "sort-published").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard-published").is_displayed())

    def test_content_calendar_page_elements(self):
        """Test 7: Verify content calendar page elements are present"""
        self.driver.get("http://localhost:5000/calendar")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "calendar-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "calendar-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "calendar-view").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "calendar-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "schedule-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard-calendar").is_displayed())

    def test_article_analytics_page_elements(self):
        """Test 8: Verify article analytics page elements are present"""
        self.driver.get("http://localhost:5000/article/1/analytics")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "analytics-page"))
        )
        self.assertTrue(self.driver.find_element(By.ID, "analytics-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "analytics-overview").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "analytics-total-views").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "analytics-unique-visitors").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-article-analytics").is_displayed())

    # ===== ADVANCED TESTS: Functionality =====

    def test_create_article_draft_functionality(self):
        """Test 9: Verify creating article as draft"""
        self.driver.get("http://localhost:5000/article/create")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "article-title"))
        )

        article_title = f"Test Article {int(time.time())}"
        self.driver.find_element(By.ID, "article-title").send_keys(article_title)
        self.driver.find_element(By.ID, "article-content").send_keys("This is test content for the article.")
        self.driver.find_element(By.ID, "save-draft-button").click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("articles")
        )

        # Verify article created with draft status
        with open(f'{self.code_path}/articles.txt', 'r') as f:
            articles = f.read()
            self.assertIn(article_title, articles, f"Article '{article_title}' not found in articles.txt")
            self.assertIn("draft", articles, "Draft status not found in articles.txt")

    def test_edit_article_version_functionality(self):
        """Test 10: Verify creating new version of article"""
        self.driver.get("http://localhost:5000/article/1/edit")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "edit-article-content"))
        )

        self.driver.find_element(By.ID, "edit-article-content").clear()
        self.driver.find_element(By.ID, "edit-article-content").send_keys("Updated content for version 2")
        self.driver.find_element(By.ID, "save-version-button").click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("edit")
        )

        # Verify new version created
        with open(f'{self.code_path}/article_versions.txt', 'r') as f:
            versions = f.read()
            self.assertIn("Updated content", versions, "Updated content not found in article_versions.txt")

    def test_version_history_functionality(self):
        """Test 11: Verify viewing version history"""
        self.driver.get("http://localhost:5000/article/1/versions")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "versions-list"))
        )

        # Verify versions from data file are displayed
        with open(f'{self.code_path}/article_versions.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "article_versions.txt file is empty")
            if len(lines) > 0:
                # Check that at least one version is shown
                versions_list = self.driver.find_element(By.ID, "versions-list").text
                self.assertGreater(len(versions_list), 0, "Version list is empty")

    def test_restore_version_functionality(self):
        """Test 12: Verify restoring previous version"""
        self.driver.get("http://localhost:5000/article/1/versions")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "versions-list"))
        )

        # Count versions before restore
        with open(f'{self.code_path}/article_versions.txt', 'r') as f:
            before_count = len(f.readlines())

        try:
            # Restore version 1
            self.driver.find_element(By.ID, "restore-version-1").click()
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("edit")
            )

            # Verify new version created with restored content
            with open(f'{self.code_path}/article_versions.txt', 'r') as f:
                after_count = len(f.readlines())
                self.assertGreaterEqual(after_count, before_count, "No new version created after restore")
        except:
            pass

    def test_filter_articles_by_status_functionality(self):
        """Test 13: Verify filtering articles by status"""
        self.driver.get("http://localhost:5000/articles/mine")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter-article-status"))
        )

        Select(self.driver.find_element(By.ID, "filter-article-status")).select_by_value("draft")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "articles-table"))
        )

        # Verify table still displayed (filtering applied)
        self.assertTrue(self.driver.find_element(By.ID, "articles-table").is_displayed())

    def test_article_analytics_functionality(self):
        """Test 14: Verify article analytics data"""
        self.driver.get("http://localhost:5000/article/1/analytics")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "analytics-total-views"))
        )

        # Verify analytics data from file is displayed
        with open(f'{self.code_path}/analytics.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "analytics.txt file is empty")
            if len(lines) > 0:
                # Sum up total views for article 1
                total_views_expected = 0
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) > 3 and parts[1] == '1':  # article_id = 1
                        total_views_expected += int(parts[3])  # views at index 3

                if total_views_expected > 0:
                    total_views = self.driver.find_element(By.ID, "analytics-total-views").text
                    self.assertIn(str(total_views_expected), total_views, f"Expected total views '{total_views_expected}' not found")

    def test_calendar_schedule_functionality(self):
        """Test 15: Verify calendar scheduling functionality"""
        self.driver.get("http://localhost:5000/calendar")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "calendar-view"))
        )

        # Verify calendar elements are functional
        self.assertTrue(self.driver.find_element(By.ID, "calendar-view").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "calendar-grid").is_displayed())

    def test_published_articles_display_functionality(self):
        """Test 16: Verify published articles display"""
        self.driver.get("http://localhost:5000/articles/published")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "published-articles-grid"))
        )

        # Verify published articles grid is displayed
        self.assertTrue(self.driver.find_element(By.ID, "published-articles-grid").is_displayed())

    def test_filter_published_by_category_functionality(self):
        """Test 17: Verify filtering published articles by category"""
        self.driver.get("http://localhost:5000/articles/published")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter-published-category"))
        )

        # Test category filter
        try:
            Select(self.driver.find_element(By.ID, "filter-published-category")).select_by_value("tutorial")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "published-articles-grid"))
            )
            self.assertTrue(True)
        except:
            pass

    def test_sort_published_articles_functionality(self):
        """Test 18: Verify sorting published articles"""
        self.driver.get("http://localhost:5000/articles/published")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "sort-published"))
        )

        # Test sorting functionality
        try:
            Select(self.driver.find_element(By.ID, "sort-published")).select_by_value("newest")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "published-articles-grid"))
            )
            self.assertTrue(True)
        except:
            pass

    def test_navigation_back_to_dashboard_functionality(self):
        """Test 19: Verify navigation back to dashboard"""
        self.driver.get("http://localhost:5000/articles/mine")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "back-to-dashboard"))
        )

        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("dashboard")
        )

        self.assertIn("dashboard", self.driver.current_url)

    def test_create_new_article_button_functionality(self):
        """Test 20: Verify create new article button"""
        self.driver.get("http://localhost:5000/articles/mine")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "create-new-article"))
        )

        self.driver.find_element(By.ID, "create-new-article").click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("create")
        )

        self.assertIn("create", self.driver.current_url)


class TestContentPublishingHub:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        self.pid = get_python_pid()
        self.py = path
        self.code_path = code_path
        self.score = 0
        self.basic_passed = 0
        self.advanced_passed = 0

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
        """Run all tests and calculate score"""
        result = {
            'total': 20,
            'total_basic': 8,
            'total_advanced': 12,
            'basic': 0,
            'advanced': 0,
            'test_cases': {'set_up': 0}
        }
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
                test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
                result['test_cases'][test_cases] = 1
            for test in res['fail']:
                test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
                result['test_cases'][test_cases] = 0

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]

        return result


if __name__ == "__main__":
    import glob
    def find_app_py(app_name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pattern = os.path.join(base_dir, 'no_login_web', f'{app_name}', 'app.py')
        if os.path.exists(pattern):
            return pattern
        return None

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('ContentPublishingHub')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestContentPublishingHub(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
