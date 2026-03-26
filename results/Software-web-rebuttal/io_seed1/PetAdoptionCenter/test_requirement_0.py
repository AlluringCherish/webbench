'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of ALL pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class PetAdoptionCenterTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access dashboard page at root '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pet Adoption Dashboard', response.data)
    def test_02_dashboard_elements(self):
        # Test Task 2 & 3: Check dashboard page elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container missing")
        featured_pets = soup.find(id='featured-pets')
        self.assertIsNotNone(featured_pets, "Featured pets section missing")
        browse_button = soup.find(id='browse-pets-button')
        self.assertIsNotNone(browse_button, "Browse pets button missing")
        back_button = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_button, "Back to dashboard button missing")
    def test_03_pet_listings_page_elements(self):
        # Test Pet Listings page elements and navigation
        response = self.client.get('/pet_listings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='pet-listings-page')
        self.assertIsNotNone(container, "Pet listings page container missing")
        search_input = soup.find(id='search-input')
        self.assertIsNotNone(search_input, "Search input missing")
        filter_species = soup.find(id='filter-species')
        self.assertIsNotNone(filter_species, "Filter species dropdown missing")
        pet_grid = soup.find(id='pet-grid')
        self.assertIsNotNone(pet_grid, "Pet grid missing")
        back_button = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_button, "Back to dashboard button missing")
    def test_04_pet_details_page_elements(self):
        # Test Pet Details page elements for a known pet_id (1)
        response = self.client.get('/pet_details/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='pet-details-page')
        self.assertIsNotNone(container, "Pet details page container missing")
        pet_name = soup.find(id='pet-name')
        self.assertIsNotNone(pet_name, "Pet name element missing")
        pet_species = soup.find(id='pet-species')
        self.assertIsNotNone(pet_species, "Pet species element missing")
        pet_description = soup.find(id='pet-description')
        self.assertIsNotNone(pet_description, "Pet description element missing")
        adopt_button = soup.find(id='adopt-button')
        self.assertIsNotNone(adopt_button, "Adopt button missing")
        back_button = soup.find(id='back-to-listings')
        self.assertIsNotNone(back_button, "Back to listings button missing")
    def test_05_add_pet_page_elements(self):
        # Test Add Pet page elements (requires admin login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'admin_user'
        response = self.client.get('/add_pet')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='add-pet-page')
        self.assertIsNotNone(container, "Add pet page container missing")
        self.assertIsNotNone(soup.find(id='pet-name-input'), "Pet name input missing")
        self.assertIsNotNone(soup.find(id='pet-species-input'), "Pet species dropdown missing")
        self.assertIsNotNone(soup.find(id='pet-breed-input'), "Pet breed input missing")
        self.assertIsNotNone(soup.find(id='pet-age-input'), "Pet age input missing")
        self.assertIsNotNone(soup.find(id='pet-gender-input'), "Pet gender dropdown missing")
        self.assertIsNotNone(soup.find(id='pet-size-input'), "Pet size dropdown missing")
        self.assertIsNotNone(soup.find(id='pet-description-input'), "Pet description textarea missing")
        self.assertIsNotNone(soup.find(id='submit-pet-button'), "Submit pet button missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
    def test_06_adoption_application_page_elements(self):
        # Test Adoption Application page elements (requires login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'john_doe'
        response = self.client.get('/adoption_application/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='application-page')
        self.assertIsNotNone(container, "Application page container missing")
        self.assertIsNotNone(soup.find(id='applicant-name'), "Applicant name input missing")
        self.assertIsNotNone(soup.find(id='applicant-phone'), "Applicant phone input missing")
        self.assertIsNotNone(soup.find(id='housing-type'), "Housing type dropdown missing")
        self.assertIsNotNone(soup.find(id='reason'), "Reason textarea missing")
        self.assertIsNotNone(soup.find(id='submit-application-button'), "Submit application button missing")
        self.assertIsNotNone(soup.find(id='back-to-pet'), "Back to pet button missing")
    def test_07_my_applications_page_elements(self):
        # Test My Applications page elements (requires login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'john_doe'
        response = self.client.get('/my_applications')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='my-applications-page')
        self.assertIsNotNone(container, "My applications page container missing")
        self.assertIsNotNone(soup.find(id='filter-status'), "Filter status dropdown missing")
        self.assertIsNotNone(soup.find(id='applications-table'), "Applications table missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
    def test_08_favorites_page_elements(self):
        # Test Favorites page elements (requires login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'john_doe'
        response = self.client.get('/favorites')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='favorites-page')
        self.assertIsNotNone(container, "Favorites page container missing")
        self.assertIsNotNone(soup.find(id='favorites-grid'), "Favorites grid missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
    def test_09_messages_page_elements(self):
        # Test Messages page elements (requires login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'john_doe'
        response = self.client.get('/messages')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='messages-page')
        self.assertIsNotNone(container, "Messages page container missing")
        self.assertIsNotNone(soup.find(id='conversation-list'), "Conversation list missing")
        self.assertIsNotNone(soup.find(id='message-input'), "Message input textarea missing")
        self.assertIsNotNone(soup.find(id='send-message-button'), "Send message button missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
    def test_10_user_profile_page_elements(self):
        # Test User Profile page elements (requires login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'john_doe'
        response = self.client.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='profile-page')
        self.assertIsNotNone(container, "Profile page container missing")
        self.assertIsNotNone(soup.find(id='profile-username'), "Profile username display missing")
        self.assertIsNotNone(soup.find(id='profile-email'), "Profile email input missing")
        self.assertIsNotNone(soup.find(id='update-profile-button'), "Update profile button missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
    def test_11_admin_panel_page_elements(self):
        # Test Admin Panel page elements (requires admin login)
        with self.client.session_transaction() as sess:
            sess['username'] = 'admin_user'
        response = self.client.get('/admin_panel')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find(id='admin-panel-page')
        self.assertIsNotNone(container, "Admin panel page container missing")
        self.assertIsNotNone(soup.find(id='pending-applications'), "Pending applications list missing")
        self.assertIsNotNone(soup.find(id='all-pets-list'), "All pets list missing")
        self.assertIsNotNone(soup.find(id='back-to-dashboard'), "Back to dashboard button missing")
if __name__ == '__main__':
    unittest.main()