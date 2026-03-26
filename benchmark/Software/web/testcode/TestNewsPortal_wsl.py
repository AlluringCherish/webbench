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
        self.assertTrue(self.driver.find_element(By.ID, "featured-articles").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-articles-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-bookmarks-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-articles-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Article Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "articles-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        articles_grid = self.driver.find_element(By.ID, "articles-grid").text
        # Verify articles from data file are displayed
        with open(f'{self.code_path}/articles.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "articles.txt is empty")
            first_article = lines[0].split('|')
            article_title = first_article[1]
            self.assertIn(article_title, articles_grid)

    # ===== Article Details Page Tests =====
    def test_article_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-article-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "article-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "article-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "article-author").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "article-date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bookmark-button").is_displayed())

    def test_article_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-article-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-details-page")))
        # Verify article details match data file
        with open(f'{self.code_path}/articles.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "articles.txt is empty")
            expected_data = first_line.split('|')
            expected_title = expected_data[1]
            title = self.driver.find_element(By.ID, "article-title").text
            self.assertIn(expected_title, title)

    # ===== Bookmarks Page Tests =====
    def test_bookmarks_page_elements(self):
        self.driver.find_element(By.ID, "view-bookmarks-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookmarks-page")))
        self.assertTrue(self.driver.find_element(By.ID, "bookmarks-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bookmarks-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_bookmarks_page_functionality(self):
        self.driver.find_element(By.ID, "view-bookmarks-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bookmarks-page")))
        bookmarks_list = self.driver.find_element(By.ID, "bookmarks-list").text
        # Verify bookmarks from data file are displayed
        with open(f'{self.code_path}/bookmarks.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_bookmark = lines[0].split('|')
                article_title = first_bookmark[2]
                self.assertIn(article_title, bookmarks_list)

    # ===== Comments Page Tests =====
    def test_comments_page_elements(self):
        self.driver.get("http://localhost:5000/comments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "comments-page")))
        self.assertTrue(self.driver.find_element(By.ID, "comments-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "comments-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "write-comment-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_comments_page_functionality(self):
        self.driver.get("http://localhost:5000/comments")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "comments-page")))
        self.driver.find_element(By.ID, "write-comment-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-comment-page")))

    # ===== Write Comment Page Tests =====
    def test_write_comment_page_elements(self):
        self.driver.get("http://localhost:5000/write-comment")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-comment-page")))
        self.assertTrue(self.driver.find_element(By.ID, "write-comment-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-article").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "commenter-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "comment-text").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-comment-button").is_displayed())

    def test_write_comment_page_functionality(self):
        self.driver.get("http://localhost:5000/write-comment")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-comment-page")))
        self.driver.find_element(By.ID, "comment-text").send_keys("Great article!")
        comment_text = self.driver.find_element(By.ID, "comment-text").get_attribute("value")
        self.assertEqual(comment_text, "Great article!")

    # ===== Trending Articles Page Tests =====
    def test_trending_page_elements(self):
        self.driver.find_element(By.ID, "trending-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trending-page")))
        self.assertTrue(self.driver.find_element(By.ID, "trending-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "time-period-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_trending_page_functionality(self):
        self.driver.find_element(By.ID, "trending-articles-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trending-page")))
        trending_list = self.driver.find_element(By.ID, "trending-list").text
        # Verify trending articles from data file are displayed
        with open(f'{self.code_path}/trending.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "trending.txt is empty")
            first_trending = lines[0].split('|')
            article_title = first_trending[1]
            self.assertIn(article_title, trending_list)

    # ===== Category Page Tests =====
    def test_category_page_elements(self):
        self.driver.get("http://localhost:5000/category/1")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "category-page")))
        self.assertTrue(self.driver.find_element(By.ID, "category-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-articles").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_category_page_functionality(self):
        self.driver.get("http://localhost:5000/category/1")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "category-page")))
        category_title = self.driver.find_element(By.ID, "category-title").text
        # Verify category matches data file
        with open(f'{self.code_path}/categories.txt', 'r') as f:
            first_line = f.readline().strip()
            if len(first_line) > 0:
                expected_data = first_line.split('|')
                expected_category = expected_data[1]
                self.assertIn(expected_category, category_title)

    # ===== Search Results Page Tests =====
    def test_search_results_page_elements(self):
        self.driver.get("http://localhost:5000/search?q=technology")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-results-page")))
        self.assertTrue(self.driver.find_element(By.ID, "search-results-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-query-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_search_results_page_functionality(self):
        self.driver.get("http://localhost:5000/search?q=technology")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-results-page")))
        query_display = self.driver.find_element(By.ID, "search-query-display").text
        self.assertIsNotNone(query_display)


class TestNewsPortal:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('NewsPortal')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestNewsPortal(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
