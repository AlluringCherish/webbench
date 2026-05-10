'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of ALL pages, verifying presence and correctness of required elements on each page.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class GymMembershipTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access dashboard page at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gym Membership Dashboard', response.data)
    def test_02_dashboard_elements(self):
        # Test Task 2 & 3: Dashboard page elements and navigation buttons
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div id
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div)
        # Check member welcome div
        member_welcome = soup.find('div', id='member-welcome')
        self.assertIsNotNone(member_welcome)
        self.assertTrue(len(member_welcome.text.strip()) > 0)
        # Check navigation buttons by id and their hrefs
        browse_btn = soup.find('button', id='browse-membership-button')
        self.assertIsNotNone(browse_btn)
        self.assertIn('Browse Membership Plans', browse_btn.text)
        view_schedule_btn = soup.find('button', id='view-schedule-button')
        self.assertIsNotNone(view_schedule_btn)
        self.assertIn('View Class Schedule', view_schedule_btn.text)
        book_trainer_btn = soup.find('button', id='book-trainer-button')
        self.assertIsNotNone(book_trainer_btn)
        self.assertIn('Book Personal Training', book_trainer_btn.text)
        # Check featured classes section
        featured_classes = dashboard_div.find_all('div', class_='class-card')
        self.assertTrue(len(featured_classes) > 0)
        # Check each featured class has required info
        for cls_card in featured_classes:
            self.assertIsNotNone(cls_card.find('h3'))
            self.assertIsNotNone(cls_card.find(text=lambda t: 'Day:' in t))
            self.assertIsNotNone(cls_card.find(text=lambda t: 'Time:' in t))
            self.assertIsNotNone(cls_card.find(text=lambda t: 'Duration:' in t))
            self.assertIsNotNone(cls_card.find(text=lambda t: 'Capacity:' in t))
            self.assertIsNotNone(cls_card.find(text=lambda t: 'Trainer:' in t))
        # Check nav links at bottom
        nav = soup.find('nav')
        self.assertIsNotNone(nav)
        expected_links = {
            'Membership Plans': '/membership-plans',
            'Class Schedule': '/class-schedule',
            'Trainer Profiles': '/trainer-profiles',
            'Book Personal Training': '/pt-booking',
            'My Workout Records': '/workout-records',
            'Log Workout': '/log-workout'
        }
        for text, href in expected_links.items():
            link = nav.find('a', string=text)
            self.assertIsNotNone(link)
            self.assertTrue(link['href'].endswith(href))
    def test_03_membership_plans_page(self):
        # Test membership plans page loads and elements present
        response = self.client.get('/membership-plans')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='membership-page')
        self.assertIsNotNone(container)
        plan_filter = soup.find('select', id='plan-filter')
        self.assertIsNotNone(plan_filter)
        plans_grid = soup.find('div', id='plans-grid')
        self.assertIsNotNone(plans_grid)
        # Check at least one plan card with view details button
        plan_cards = plans_grid.find_all(class_='plan-card')
        self.assertTrue(len(plan_cards) > 0)
        for card in plan_cards:
            self.assertIsNotNone(card.find('h3'))
            self.assertIsNotNone(card.find(class_='plan-price'))
            self.assertIsNotNone(card.find(class_='plan-features'))
            # Check view details button with correct id pattern
            btn = card.find('button', id=lambda x: x and x.startswith('view-details-button-'))
            self.assertIsNotNone(btn)
        back_btn = container.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn)
    def test_04_plan_details_page(self):
        # Test plan details page for plan_id=1 (Basic)
        response = self.client.get('/plan-details/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='plan-details-page')
        self.assertIsNotNone(container)
        plan_title = container.find('h1', id='plan-title')
        self.assertIsNotNone(plan_title)
        self.assertTrue(len(plan_title.text.strip()) > 0)
        plan_price = container.find('div', id='plan-price')
        self.assertIsNotNone(plan_price)
        self.assertTrue(len(plan_price.text.strip()) > 0)
        plan_features = container.find('div', id='plan-features')
        self.assertIsNotNone(plan_features)
        self.assertTrue(len(plan_features.text.strip()) > 0)
        enroll_btn = container.find('button', id='enroll-plan-button')
        self.assertIsNotNone(enroll_btn)
        plan_reviews = container.find('div', id='plan-reviews')
        self.assertIsNotNone(plan_reviews)
    def test_05_class_schedule_page(self):
        response = self.client.get('/class-schedule')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='schedule-page')
        self.assertIsNotNone(container)
        search_input = container.find('input', id='schedule-search')
        self.assertIsNotNone(search_input)
        filter_dropdown = container.find('select', id='schedule-filter')
        self.assertIsNotNone(filter_dropdown)
        classes_grid = container.find('div', id='classes-grid')
        self.assertIsNotNone(classes_grid)
        class_cards = classes_grid.find_all(class_='class-card')
        self.assertTrue(len(class_cards) > 0)
        for card in class_cards:
            self.assertIsNotNone(card.find('h3'))
            self.assertIsNotNone(card.find(class_='class-info'))
            enroll_btn = card.find('button', id=lambda x: x and x.startswith('enroll-class-button-'))
            self.assertIsNotNone(enroll_btn)
    def test_06_trainer_profiles_page(self):
        response = self.client.get('/trainer-profiles')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='trainers-page')
        self.assertIsNotNone(container)
        search_input = container.find('input', id='trainer-search')
        self.assertIsNotNone(search_input)
        specialty_filter = container.find('select', id='specialty-filter')
        self.assertIsNotNone(specialty_filter)
        trainers_grid = container.find('div', id='trainers-grid')
        self.assertIsNotNone(trainers_grid)
        trainer_cards = trainers_grid.find_all(class_='trainer-card')
        self.assertTrue(len(trainer_cards) > 0)
        for card in trainer_cards:
            self.assertIsNotNone(card.find(class_='trainer-name'))
            self.assertIsNotNone(card.find(class_='trainer-expertise'))
            btn = card.find('button', id=lambda x: x and x.startswith('view-trainer-button-'))
            self.assertIsNotNone(btn)
    def test_07_trainer_detail_page(self):
        response = self.client.get('/trainer-detail/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='trainer-detail-page')
        self.assertIsNotNone(container)
        trainer_name = container.find('h1', id='trainer-name')
        self.assertIsNotNone(trainer_name)
        self.assertTrue(len(trainer_name.text.strip()) > 0)
        bio = container.find('div', id='trainer-bio')
        self.assertIsNotNone(bio)
        certs = container.find('div', id='trainer-certifications')
        self.assertIsNotNone(certs)
        book_btn = container.find('button', id='book-session-button')
        self.assertIsNotNone(book_btn)
        reviews = container.find('div', id='trainer-reviews')
        self.assertIsNotNone(reviews)
    def test_08_pt_booking_page_get(self):
        response = self.client.get('/pt-booking')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='booking-page')
        self.assertIsNotNone(container)
        select_trainer = container.find('select', id='select-trainer')
        self.assertIsNotNone(select_trainer)
        session_date = container.find('input', id='session-date')
        self.assertIsNotNone(session_date)
        session_time = container.find('select', id='session-time')
        self.assertIsNotNone(session_time)
        session_duration = container.find('select', id='session-duration')
        self.assertIsNotNone(session_duration)
        confirm_btn = container.find('button', id='confirm-booking-button')
        self.assertIsNotNone(confirm_btn)
    def test_09_workout_records_page(self):
        response = self.client.get('/workout-records')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='workouts-page')
        self.assertIsNotNone(container)
        workouts_table = container.find('table', id='workouts-table')
        self.assertIsNotNone(workouts_table)
        filter_dropdown = container.find('select', id='filter-by-type')
        self.assertIsNotNone(filter_dropdown)
        log_workout_btn = container.find('button', id='log-workout-button')
        self.assertIsNotNone(log_workout_btn)
    def test_10_log_workout_page_get(self):
        response = self.client.get('/log-workout')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='log-workout-page')
        self.assertIsNotNone(container)
        workout_type = container.find('select', id='workout-type')
        self.assertIsNotNone(workout_type)
        workout_duration = container.find('input', id='workout-duration')
        self.assertIsNotNone(workout_duration)
        calories_burned = container.find('input', id='calories-burned')
        self.assertIsNotNone(calories_burned)
        workout_notes = container.find('textarea', id='workout-notes')
        self.assertIsNotNone(workout_notes)
        workout_date = container.find('input', id='workout-date')
        self.assertIsNotNone(workout_date)
        submit_btn = container.find('button', id='submit-workout-button')
        self.assertIsNotNone(submit_btn)
if __name__ == '__main__':
    unittest.main()