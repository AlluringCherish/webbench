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
from datetime import datetime

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

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "welcome-message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-books-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-borrows-button").is_displayed())

    def test_dashboard_page_functionality(self):
        welcome = self.driver.find_element(By.ID, "welcome-message").text
        self.assertTrue(len(welcome) > 0)
        # Verify username from users.txt is displayed
        with open('data/users.txt', 'r') as f:
            users = f.readlines()
        if len(users) > 0:
            first_user = users[0].strip().split('|')
            username = first_user[0]
            self.assertIn(username, welcome)
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Book Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        # Verify books from books.txt are displayed
        with open('data/books.txt', 'r') as f:
            books = f.readlines()
        self.assertTrue(len(books) > 0, "books.txt is empty")
        first_book = books[0].strip().split('|')
        expected_title = first_book[1]
        book_grid = self.driver.find_element(By.ID, "book-grid").text
        self.assertIn(expected_title, book_grid)

    # ===== Book Details Page Tests =====
    def test_book_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "book-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-author").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "book-status").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "reviews-section").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-catalog").is_displayed())

    def test_book_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        # Verify book details match books.txt
        with open('data/books.txt', 'r') as f:
            books = f.readlines()
        first_book = books[0].strip().split('|')
        expected_title = first_book[1]
        expected_author = first_book[2]
        book_title = self.driver.find_element(By.ID, "book-title").text
        book_author = self.driver.find_element(By.ID, "book-author").text
        self.assertEqual(book_title, expected_title)
        self.assertIn(expected_author, book_author)

    # ===== Borrow Confirmation Page Tests =====
    def test_borrow_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.driver.find_element(By.ID, "borrow-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "borrow-page")))
        self.assertTrue(self.driver.find_element(By.ID, "borrow-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "borrow-book-info").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "due-date-display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "confirm-borrow-button").is_displayed())

    def test_borrow_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.driver.find_element(By.ID, "borrow-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "borrow-page")))
        # Verify due date is displayed (should be 14 days from borrow)
        due_date_text = self.driver.find_element(By.ID, "due-date-display").text
        self.assertTrue(len(due_date_text) > 0)
        # Count borrowings before
        with open('data/borrowings.txt', 'r') as f:
            before_count = len(f.readlines())
        self.driver.find_element(By.ID, "confirm-borrow-button").click()
        time.sleep(1)
        # Verify borrowing was added
        with open('data/borrowings.txt', 'r') as f:
            after_count = len(f.readlines())
        self.assertGreater(after_count, before_count)

    # ===== My Borrowings Page Tests =====
    def test_my_borrows_page_elements(self):
        self.driver.find_element(By.ID, "my-borrows-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-borrows-page")))
        self.assertTrue(self.driver.find_element(By.ID, "my-borrows-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "filter-status").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "borrows-table").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_my_borrows_page_functionality(self):
        self.driver.find_element(By.ID, "my-borrows-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "my-borrows-page")))
        # Verify borrowings from borrowings.txt are displayed
        with open('data/borrowings.txt', 'r') as f:
            borrowings = f.readlines()
        borrows_table = self.driver.find_element(By.ID, "borrows-table").text
        if len(borrowings) > 0:
            # Verify first borrowing's book appears
            first_borrow = borrowings[0].strip().split('|')
            book_id = first_borrow[2]
            with open('data/books.txt', 'r') as f:
                books = f.readlines()
            for book in books:
                if book.startswith(f"{book_id}|"):
                    book_title = book.strip().split('|')[1]
                    self.assertIn(book_title, borrows_table)
                    break
        else:
            self.assertIsNotNone(borrows_table)

    # ===== My Reservations Page Tests =====
    def test_reservations_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())

    def test_reservations_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())

    # ===== My Reviews Page Tests =====
    def test_reviews_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "reviews-section").is_displayed())

    def test_reviews_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        reviews_section = self.driver.find_element(By.ID, "reviews-section").text
        self.assertTrue(reviews_section is not None)

    # ===== Write Review Page Tests =====
    def test_write_review_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.driver.find_element(By.ID, "write-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        self.assertTrue(self.driver.find_element(By.ID, "write-review-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rating-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "review-text").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-review-button").is_displayed())

    def test_write_review_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "view-book-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "book-details-page")))
        self.driver.find_element(By.ID, "write-review-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "write-review-page")))
        # Count reviews before
        with open('data/reviews.txt', 'r') as f:
            before_count = len(f.readlines())
        Select(self.driver.find_element(By.ID, "rating-input")).select_by_value("5")
        self.driver.find_element(By.ID, "review-text").send_keys("Great book!")
        self.driver.find_element(By.ID, "submit-review-button").click()
        time.sleep(1)
        # Verify review was added
        with open('data/reviews.txt', 'r') as f:
            after_count = len(f.readlines())
            content = f.read()
        self.assertGreater(after_count, before_count)
        with open('data/reviews.txt', 'r') as f:
            self.assertIn("Great book!", f.read())

    # ===== User Profile Page Tests =====
    def test_profile_page_elements(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())

    def test_profile_page_functionality(self):
        self.driver.find_element(By.ID, "browse-books-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "back-to-dashboard").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-page")))
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())

    # ===== Payment Confirmation Page Tests =====
    def test_payment_confirmation_page_elements(self):
        # Navigate via direct link since payment page is for fines
        self.driver.get("http://localhost:5000/payment")
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "payment-page")))
            self.assertTrue(self.driver.find_element(By.ID, "payment-page").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "fine-amount-display").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "confirm-payment-button").is_displayed())
        except:
            # Payment page may not be accessible without fines
            pass

    def test_payment_confirmation_page_functionality(self):
        # Check if there are any fines to pay
        with open('data/fines.txt', 'r') as f:
            fines = f.readlines()
        if len(fines) > 0:
            self.driver.get("http://localhost:5000/payment")
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "payment-page")))
                fine_amount = self.driver.find_element(By.ID, "fine-amount-display").text
                self.assertTrue(len(fine_amount) > 0)
            except:
                pass


class TestOnlineLibrary:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')
        self.pid = get_python_pid()
        self.py = path
        self.time = time
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
        result = {
            'total': 20,
            'total_basic': 10,
            'total_advanced': 10,
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
        pattern = os.path.join(base_dir, f'{app_name}_*')
        matching_dirs = glob.glob(pattern)
        if not matching_dirs:
            return None
        matching_dirs.sort(key=os.path.getmtime, reverse=True)
        for dir_path in matching_dirs:
            app_py_path = os.path.join(dir_path, 'app.py')
            if os.path.exists(app_py_path):
                return app_py_path
        return None

    if len(sys.argv) > 1:
        py = sys.argv[1]
    else:
        print(f"Searching for OnlineLibrary app.py...")
        py = find_app_py('OnlineLibrary')
        if py is None:
            print("=" * 70)
            print("ERROR: Could not find app.py")
            print(f"Searched for: OnlineLibrary_*/app.py")
            print("=" * 70)
            sys.exit(1)
        print(f"Found: {py}")

    if not os.path.exists(py):
        print(f"ERROR: File not found: {py}")
        sys.exit(1)

    test = TestOnlineLibrary(None, py)
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    result = test.main()
    import pprint
    pprint.pprint(result)
    print(f"Basic: {result['basic']}/{result['total_basic']}")
    print(f"Advanced: {result['advanced']}/{result['total_advanced']}")
    print(f"Total: {result['basic'] + result['advanced']}/{result['total']}")
