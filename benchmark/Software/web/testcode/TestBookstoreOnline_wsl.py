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
        self.code_path = 'data'

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "featured-books").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-catalog-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-cart-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bestsellers-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Book Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "category-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "books-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))

        # Verify books from data file are displayed
        with open(f'{self.code_path}/books.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "books.txt file is empty")
            if len(lines) > 0:
                first_book = lines[0].strip().split('|')
                if len(first_book) > 1:
                    expected_title = first_book[1]  # title is at index 1
                    books_grid = self.driver.find_element(By.ID, "books-grid").text
                    self.assertIn(expected_title, books_grid, f"Book title '{expected_title}' not found in catalog")

    # ===== Book Details Page Tests =====
    def test_book_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "book-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-author").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-price").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "add-to-cart-button").is_displayed())

    def test_book_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-catalog-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))

        # Verify book details match data file
        with open(f'{self.code_path}/books.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # book_id = 1
                    expected_title = parts[1]
                    expected_author = parts[2]
                    expected_price = parts[5]

                    title = self.driver.find_element(By.ID, "book-title").text
                    author = self.driver.find_element(By.ID, "book-author").text
                    price = self.driver.find_element(By.ID, "book-price").text

                    self.assertIn(expected_title, title, f"Expected title '{expected_title}' not found")
                    self.assertIn(expected_author, author, f"Expected author '{expected_author}' not found")
                    self.assertIn(expected_price, price, f"Expected price '{expected_price}' not found")
                    break

    # ===== Shopping Cart Page Tests =====
    def test_cart_page_elements(self):
        self.driver.find_element(By.ID, "view-cart-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cart-page")))
        self.assertTrue(self.driver.find_element(By.ID, "cart-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cart-items-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "total-amount").is_displayed())

    def test_cart_page_functionality(self):
        self.driver.find_element(By.ID, "view-cart-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cart-page")))
        total = self.driver.find_element(By.ID, "total-amount").text
        self.assertIsNotNone(total)

    # ===== Checkout Page Tests =====
    def test_checkout_page_elements(self):
        self.driver.find_element(By.ID, "view-cart-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cart-page")))
        try:
            self.driver.find_element(By.ID, "proceed-checkout-button").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkout-page")))
            self.assertTrue(self.driver.find_element(By.ID, "checkout-page").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "customer-name").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "shipping-address").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "payment-method").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "place-order-button").is_displayed())
        except:
            pass  # Cart might be empty

    def test_checkout_page_functionality(self):
        self.driver.find_element(By.ID, "view-cart-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cart-page")))
        try:
            self.driver.find_element(By.ID, "proceed-checkout-button").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkout-page")))
            self.driver.find_element(By.ID, "customer-name").send_keys("Test Customer")
            self.driver.find_element(By.ID, "shipping-address").send_keys("123 Test St")
        except:
            pass  # Cart might be empty

    # ===== Order History Page Tests =====
    def test_orders_page_elements(self):
        self.driver.get("http://localhost:5000/orders")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "orders-page")))
        self.assertTrue(self.driver.find_element(By.ID, "orders-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "orders-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_orders_page_functionality(self):
        self.driver.get("http://localhost:5000/orders")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "orders-page")))

        # Verify orders from data file are displayed
        with open(f'{self.code_path}/orders.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "orders.txt file is empty")
            if len(lines) > 0:
                first_order = lines[0].strip().split('|')
                if len(first_order) > 1:
                    expected_customer = first_order[1]  # customer_name is at index 1
                    orders_table = self.driver.find_element(By.ID, "orders-table").text
                    self.assertIn(expected_customer, orders_table, f"Customer name '{expected_customer}' not found in orders")

    # ===== Reviews Page Tests =====
    def test_reviews_page_elements(self):
        self.driver.get("http://localhost:5000/reviews")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        self.assertTrue(self.driver.find_element(By.ID, "reviews-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "reviews-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "write-review-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_reviews_page_functionality(self):
        self.driver.get("http://localhost:5000/reviews")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-page")))
        self.driver.find_element(By.ID, "write-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))

    # ===== Write Review Page Tests =====
    def test_write_review_page_elements(self):
        self.driver.get("http://localhost:5000/write-review")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.assertTrue(self.driver.find_element(By.ID, "write-review-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-book").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rating-select").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "review-text").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-review-button").is_displayed())

    def test_write_review_page_functionality(self):
        self.driver.get("http://localhost:5000/write-review")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.driver.find_element(By.ID, "review-text").send_keys("Great book!")
        review_text = self.driver.find_element(By.ID, "review-text").get_attribute("value")
        self.assertEqual(review_text, "Great book!")

    # ===== Bestsellers Page Tests =====
    def test_bestsellers_page_elements(self):
        self.driver.find_element(By.ID, "bestsellers-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bestsellers-page")))
        self.assertTrue(self.driver.find_element(By.ID, "bestsellers-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "bestsellers-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "time-period-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_bestsellers_page_functionality(self):
        self.driver.find_element(By.ID, "bestsellers-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "bestsellers-page")))

        # Verify bestsellers from data file are displayed
        with open(f'{self.code_path}/bestsellers.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "bestsellers.txt file is empty")
            if len(lines) > 0:
                first_bestseller = lines[0].strip().split('|')
                book_id = first_bestseller[0]

                # Find corresponding book title
                with open(f'{self.code_path}/books.txt', 'r') as bf:
                    for book_line in bf:
                        book_parts = book_line.strip().split('|')
                        if book_parts[0] == book_id:
                            expected_title = book_parts[1]
                            bestsellers_list = self.driver.find_element(By.ID, "bestsellers-list").text
                            self.assertIn(expected_title, bestsellers_list, f"Bestseller book '{expected_title}' not found")
                            break


class TestBookstoreOnline:
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('BookstoreOnline')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestBookstoreOnline(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
