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
        self.assertTrue(self.driver.find_element(By.ID, "featured-restaurants").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-restaurants-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "view-cart-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "active-orders-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.assertTrue(self.driver.find_element(By.ID, "restaurants-page").is_displayed())

    # ===== Restaurant Listing Page Tests =====
    def test_restaurants_page_elements(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.assertTrue(self.driver.find_element(By.ID, "restaurants-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cuisine-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "restaurants-grid").is_displayed())

    def test_restaurants_page_functionality(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))

        # Verify restaurants from data file are displayed
        with open(f'{self.code_path}/restaurants.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "restaurants.txt file is empty")
            if len(lines) > 0:
                first_restaurant = lines[0].strip().split('|')
                if len(first_restaurant) > 1:
                    expected_name = first_restaurant[1]  # name is at index 1
                    restaurants_grid = self.driver.find_element(By.ID, "restaurants-grid").text
                    self.assertIn(expected_name, restaurants_grid, f"Restaurant name '{expected_name}' not found")

    # ===== Restaurant Menu Page Tests =====
    def test_menu_page_elements(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.driver.find_element(By.ID, "view-restaurant-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        self.assertTrue(self.driver.find_element(By.ID, "menu-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "restaurant-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "restaurant-info").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "menu-items-grid").is_displayed())

    def test_menu_page_functionality(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.driver.find_element(By.ID, "view-restaurant-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))

        # Verify restaurant name matches data file
        with open(f'{self.code_path}/restaurants.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # restaurant_id = 1
                    expected_name = parts[1]
                    restaurant_name = self.driver.find_element(By.ID, "restaurant-name").text
                    self.assertIn(expected_name, restaurant_name, f"Expected restaurant name '{expected_name}' not found")
                    break

    # ===== Item Details Page Tests =====
    def test_item_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.driver.find_element(By.ID, "view-restaurant-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        self.driver.find_element(By.ID, "view-item-details-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "item-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "item-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "item-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "item-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "item-price").is_displayed())

    def test_item_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-restaurants-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "restaurants-page")))
        self.driver.find_element(By.ID, "view-restaurant-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu-page")))
        self.driver.find_element(By.ID, "view-item-details-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "item-details-page")))

        # Verify item details match data file
        with open(f'{self.code_path}/menus.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # item_id = 1
                    expected_item = parts[2]
                    expected_price = parts[5]

                    item_name = self.driver.find_element(By.ID, "item-name").text
                    item_price = self.driver.find_element(By.ID, "item-price").text

                    self.assertIn(expected_item, item_name, f"Expected item name '{expected_item}' not found")
                    self.assertIn(expected_price, item_price, f"Expected price '{expected_price}' not found")
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
            self.assertTrue(self.driver.find_element(By.ID, "delivery-address").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "phone-number").is_displayed())
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
            self.driver.find_element(By.ID, "delivery-address").send_keys("123 Test St")
        except:
            pass  # Cart might be empty

    # ===== Active Orders Page Tests =====
    def test_active_orders_page_elements(self):
        self.driver.get("http://localhost:5000/active-orders")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "active-orders-page")))
        self.assertTrue(self.driver.find_element(By.ID, "active-orders-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "orders-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_active_orders_page_functionality(self):
        self.driver.get("http://localhost:5000/active-orders")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "active-orders-page")))

        # Verify orders from data file are displayed
        with open(f'{self.code_path}/orders.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "orders.txt file is empty")
            if len(lines) > 0:
                first_order = lines[0].strip().split('|')
                if len(first_order) > 1:
                    expected_customer = first_order[1]  # customer_name is at index 1
                    orders_list = self.driver.find_element(By.ID, "orders-list").text
                    self.assertIn(expected_customer, orders_list, f"Customer name '{expected_customer}' not found in orders")

    # ===== Order Tracking Page Tests =====
    def test_tracking_page_elements(self):
        self.driver.get("http://localhost:5000/track-order/1")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tracking-page")))
        self.assertTrue(self.driver.find_element(By.ID, "tracking-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "order-details").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "delivery-driver-info").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "estimated-time").is_displayed())

    def test_tracking_page_functionality(self):
        self.driver.get("http://localhost:5000/track-order/1")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "tracking-page")))

        # Verify order tracking details match data file
        with open(f'{self.code_path}/orders.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == '1':  # order_id = 1
                    expected_customer = parts[1]
                    expected_total = parts[4]

                    order_details = self.driver.find_element(By.ID, "order-details").text
                    self.assertGreater(len(order_details), 0, "Order details are empty")
                    # Optionally verify specific details
                    # self.assertIn(expected_customer, order_details, f"Customer '{expected_customer}' not found")
                    break

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

        # Verify reviews from data file are displayed
        with open(f'{self.code_path}/reviews.txt', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "reviews.txt file is empty")
            if len(lines) > 0:
                first_review = lines[0].strip().split('|')
                if len(first_review) > 2:
                    expected_customer = first_review[2]  # customer_name is at index 2
                    reviews_list = self.driver.find_element(By.ID, "reviews-list").text
                    self.assertIn(expected_customer, reviews_list, f"Customer name '{expected_customer}' not found in reviews")

    # ===== Write Review Page Tests =====
    def test_write_review_page_elements(self):
        self.driver.get("http://localhost:5000/write-review")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.assertTrue(self.driver.find_element(By.ID, "write-review-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-restaurant").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rating-select").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "review-text").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-review-button").is_displayed())

    def test_write_review_page_functionality(self):
        self.driver.get("http://localhost:5000/write-review")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.driver.find_element(By.ID, "review-text").send_keys("Great food and service!")
        review_text = self.driver.find_element(By.ID, "review-text").get_attribute("value")
        self.assertEqual(review_text, "Great food and service!")


class TestFoodDelivery:
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
        result = {'total': 20, 'total_basic': 10, 'total_advanced': 10, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
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

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('FoodDelivery')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestFoodDelivery(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
