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
    code_path = None

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
        self.assertTrue(self.driver.find_element(By.ID, "featured-auctions").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-auctions-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-bids-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-auctions-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Auction Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "auctions-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        # Read auctions data and verify actual content
        with open('data/auctions.txt', 'r') as f:
            auctions = f.readlines()
        self.assertTrue(len(auctions) > 0, "auctions.txt is empty")
        first_auction = auctions[0].strip().split('|')
        expected_item_name = first_auction[1]
        auctions_grid = self.driver.find_element(By.ID, "auctions-grid").text
        self.assertIn(expected_item_name, auctions_grid)

    # ===== Auction Details Page Tests =====
    def test_auction_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-auction-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "auction-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "auction-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "auction-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "auction-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "current-bid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "place-bid-button").is_displayed())

    def test_auction_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-auction-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "auction-details-page")))
        # Verify title matches data file
        with open('data/auctions.txt', 'r') as f:
            auctions = f.readlines()
        first_auction = auctions[0].strip().split('|')
        expected_title = first_auction[1]
        title = self.driver.find_element(By.ID, "auction-title").text
        self.assertEqual(title, expected_title)

    # ===== Place Bid Page Tests =====
    def test_place_bid_page_elements(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-auction-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "auction-details-page")))
        self.driver.find_element(By.ID, "place-bid-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "place-bid-page")))
        self.assertTrue(self.driver.find_element(By.ID, "place-bid-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bidder-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bid-amount").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "auction-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-bid-button").is_displayed())

    def test_place_bid_page_functionality(self):
        self.driver.find_element(By.ID, "browse-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-auction-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "auction-details-page")))
        self.driver.find_element(By.ID, "place-bid-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "place-bid-page")))
        # Count bids before
        with open('data/bids.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "bidder-name").send_keys("Test Bidder")
        self.driver.find_element(By.ID, "bid-amount").send_keys("100.00")
        self.driver.find_element(By.ID, "submit-bid-button").click()
        time.sleep(1)
        # Verify bid was added
        with open('data/bids.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count)

    # ===== Bid History Page Tests =====
    def test_bid_history_page_elements(self):
        self.driver.get("http://localhost:5000/bid-history")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bid-history-page")))
        self.assertTrue(self.driver.find_element(By.ID, "bid-history-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bids-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_bid_history_page_functionality(self):
        self.driver.get("http://localhost:5000/bid-history")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bid-history-page")))
        # Verify bid history shows data from bids.txt
        with open('data/bids.txt', 'r') as f:
            bids = f.readlines()
        self.assertTrue(len(bids) > 0, "bids.txt is empty")
        first_bid = bids[0].strip().split('|')
        bidder_name = first_bid[2]
        bids_table = self.driver.find_element(By.ID, "bids-table").text
        self.assertIn(bidder_name, bids_table)

    # ===== Auction Categories Page Tests =====
    def test_categories_page_elements(self):
        self.driver.get("http://localhost:5000/categories")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "categories-page")))
        self.assertTrue(self.driver.find_element(By.ID, "categories-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "categories-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_categories_page_functionality(self):
        self.driver.get("http://localhost:5000/categories")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "categories-page")))
        # Verify categories match categories.txt
        with open('data/categories.txt', 'r') as f:
            categories = f.readlines()
        self.assertTrue(len(categories) > 0, "categories.txt is empty")
        first_category = categories[0].strip().split('|')
        category_name = first_category[1]
        categories_list = self.driver.find_element(By.ID, "categories-list").text
        self.assertIn(category_name, categories_list)

    # ===== Winners Page Tests =====
    def test_winners_page_elements(self):
        self.driver.get("http://localhost:5000/winners")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "winners-page")))
        self.assertTrue(self.driver.find_element(By.ID, "winners-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "winners-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_winners_page_functionality(self):
        self.driver.get("http://localhost:5000/winners")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "winners-page")))
        # Verify winners match winners.txt
        with open('data/winners.txt', 'r') as f:
            winners = f.readlines()
        if len(winners) > 0:
            first_winner = winners[0].strip().split('|')
            winner_name = first_winner[3]
            winners_list = self.driver.find_element(By.ID, "winners-list").text
            self.assertIn(winner_name, winners_list)
        else:
            winners_list = self.driver.find_element(By.ID, "winners-list").text
            self.assertIsNotNone(winners_list)

    # ===== Trending Auctions Page Tests =====
    def test_trending_page_elements(self):
        self.driver.find_element(By.ID, "trending-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trending-page")))
        self.assertTrue(self.driver.find_element(By.ID, "trending-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "time-range-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_trending_page_functionality(self):
        self.driver.find_element(By.ID, "trending-auctions-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "trending-page")))
        # Verify trending list shows data from trending.txt
        with open('data/trending.txt', 'r') as f:
            trending = f.readlines()
        self.assertTrue(len(trending) > 0, "trending.txt is empty")
        first_trending = trending[0].strip().split('|')
        item_name = first_trending[1]
        trending_list = self.driver.find_element(By.ID, "trending-list").text
        self.assertIn(item_name, trending_list)

    # ===== Auction Status Page Tests =====
    def test_status_page_elements(self):
        self.driver.get("http://localhost:5000/status")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "status-page")))
        self.assertTrue(self.driver.find_element(By.ID, "status-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "status-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "status-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_status_page_functionality(self):
        self.driver.get("http://localhost:5000/status")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "status-page")))
        # Verify status table shows auctions with their status
        with open('data/auctions.txt', 'r') as f:
            auctions = f.readlines()
        self.assertTrue(len(auctions) > 0, "auctions.txt is empty")
        first_auction = auctions[0].strip().split('|')
        status = first_auction[7]
        status_table = self.driver.find_element(By.ID, "status-table").text
        self.assertIn(status, status_table)


class TestOnlineAuction:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('OnlineAuction')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestOnlineAuction(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
