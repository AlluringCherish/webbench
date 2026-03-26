# Design Specification for PetAdoptionCenter

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                     | Function Name       | HTTP Methods | Template File              | Context Variables (name: type)                                                                                  |
|--------------------------------|---------------------|--------------|----------------------------|-----------------------------------------------------------------------------------------------------------------|
| `/`                            | root_redirect       | GET          | N/A (redirect)              | None                                                                                                            |
| `/dashboard`                   | dashboard           | GET          | dashboard.html             | featured_pets: list[dict], recent_activities: list[str]                                                        |
| `/pets`                       | pet_listings        | GET          | pet_listings.html          | pets: list[dict], species_options: list[str], selected_species: str, search_query: str                          |
| `/pets/<int:pet_id>`          | pet_details         | GET          | pet_details.html           | pet: dict                                                                                                       |
| `/pets/add`                   | add_pet             | GET, POST    | add_pet.html               | species_options: list[str], gender_options: list[str], size_options: list[str] (GET)
|                              |                     |              |                            | submission_result: str (POST - success or error message)                                                      |
| `/applications/apply/<int:pet_id>` | adoption_application | GET, POST    | adoption_application.html  | pet: dict, submission_result: str (POST - success or error message)                                            |
| `/applications/my`            | my_applications     | GET          | my_applications.html       | applications: list[dict], status_options: list[str], selected_status: str                                       |
| `/favorites`                 | favorites           | GET          | favorites.html             | favorite_pets: list[dict]                                                                                        |
| `/messages`                  | messages            | GET, POST    | messages.html              | conversations: list[dict] (GET), submission_result: str (POST - success or error message)                       |
| `/profile`                   | user_profile        | GET, POST    | profile.html               | user_info: dict, submission_result: str (POST)                                                                  |
| `/admin`                     | admin_panel         | GET          | admin_panel.html           | pending_applications: list[dict], all_pets: list[dict]                                                         |
| `/admin/pets/edit/<int:pet_id>` | edit_pet             | GET, POST    | add_pet.html               | pet: dict (GET), submission_result: str (POST)                                                                 |
| `/admin/pets/delete/<int:pet_id>` | delete_pet           | POST         | N/A (redirect)              | None                                                                                                            |

### Notes on Routes:
- The root `/` route redirects to `/dashboard`.
- POST methods are used for submitting forms such as add pet, adoption application, profile updates, message sending, pet deletion.
- GET methods for displaying pages.

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Template File: `templates/dashboard.html`
- **Page Title:** Pet Adoption Dashboard
- **Page Header (<h1>):** Pet Adoption Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `browse-pets-button`: navigates to `{{ url_for('pet_listings') }}`
  - `back-to-dashboard`: reloads the dashboard page `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `featured_pets`: list of dictionaries, each dict contains pet details including at least `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)
  - `recent_activities`: list of strings representing recent activity descriptions

### 2. Template File: `templates/pet_listings.html`
- **Page Title:** Available Pets
- **Page Header (<h1>):** Available Pets
- **Element IDs:**
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (select dropdown)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
  - Each pet card in `pet-grid` links to pet details page using `{{ url_for('pet_details', pet_id=pet['pet_id']) }}`
- **Context Variables:**
  - `pets`: list of dictionaries, each with keys `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)
  - `species_options`: list of strings [`All`, `Dog`, `Cat`, `Bird`, `Rabbit`, `Other`]
  - `selected_species`: string (current selected species filter)
  - `search_query`: string (current search input)

### 3. Template File: `templates/pet_details.html`
- **Page Title:** Pet Details
- **Page Header (<h1>):** Pet Details
- **Element IDs:**
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- **Navigation Mappings:**
  - `adopt-button`: navigates to `{{ url_for('adoption_application', pet_id=pet['pet_id']) }}`
  - `back-to-listings`: navigates to `{{ url_for('pet_listings') }}`
- **Context Variables:**
  - `pet`: dictionary with at least keys: `pet_id` (int), `name` (str), `species` (str), `description` (str)

### 4. Template File: `templates/add_pet.html`
- **Page Title:** Add New Pet
- **Page Header (<h1>):** Add New Pet
- **Element IDs:**
  - `add-pet-page` (div)
  - `pet-name-input` (input)
  - `pet-species-input` (select dropdown)
  - `pet-breed-input` (input)
  - `pet-age-input` (input)
  - `pet-gender-input` (select dropdown)
  - `pet-size-input` (select dropdown)
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `species_options`: list of strings [`Dog`, `Cat`, `Bird`, `Rabbit`, `Other`]
  - `gender_options`: list of strings [`Male`, `Female`]
  - `size_options`: list of strings [`Small`, `Medium`, `Large`]
  - `submission_result`: string (optional, post submission success or error message)

### 5. Template File: `templates/adoption_application.html`
- **Page Title:** Adoption Application
- **Page Header (<h1>):** Adoption Application
- **Element IDs:**
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (select dropdown)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- **Navigation Mappings:**
  - `back-to-pet`: navigates to `{{ url_for('pet_details', pet_id=pet['pet_id']) }}`
- **Context Variables:**
  - `pet`: dictionary with at least keys: `pet_id` (int), `name` (str)
  - `submission_result`: string (optional, post submission success or error message)
  - `housing_options`: list of strings [`House`, `Apartment`, `Condo`, `Other`]

### 6. Template File: `templates/my_applications.html`
- **Page Title:** My Applications
- **Page Header (<h1>):** My Applications
- **Element IDs:**
  - `my-applications-page` (div)
  - `filter-status` (select dropdown)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
  - Actions in `applications-table` could include links/buttons to view application details or withdraw
- **Context Variables:**
  - `applications`: list of dictionaries with keys including `application_id` (int), `pet_name` (str), `date` (str), `status` (str)
  - `status_options`: list of strings [`All`, `Pending`, `Approved`, `Rejected`]
  - `selected_status`: string (current filter)

### 7. Template File: `templates/favorites.html`
- **Page Title:** My Favorites
- **Page Header (<h1>):** My Favorites
- **Element IDs:**
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
  - Each favorite pet card in `favorites-grid` links to pet details page `{{ url_for('pet_details', pet_id=pet['pet_id']) }}`
- **Context Variables:**
  - `favorite_pets`: list of dictionaries with keys `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)

### 8. Template File: `templates/messages.html`
- **Page Title:** Messages
- **Page Header (<h1>):** Messages
- **Element IDs:**
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `conversations`: list of dictionaries, each conversation includes `recipient_username` (str), `last_message` (str), `unread_count` (int)
  - `submission_result`: string (post message send result)

### 9. Template File: `templates/profile.html`
- **Page Title:** My Profile
- **Page Header (<h1>):** My Profile
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `user_info`: dictionary with keys `username` (str), `email` (str)
  - `submission_result`: string (optional, success or error message for profile update)

### 10. Template File: `templates/admin_panel.html`
- **Page Title:** Admin Panel
- **Page Header (<h1>):** Admin Panel
- **Element IDs:**
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: navigates to `{{ url_for('dashboard') }}`
  - Pending application items link to view or manage applications
  - Pets list includes edit and delete buttons:
    - Edit button links to `{{ url_for('edit_pet', pet_id=pet['pet_id']) }}`
    - Delete button triggers POST to `{{ url_for('delete_pet', pet_id=pet['pet_id']) }}`
- **Context Variables:**
  - `pending_applications`: list of dictionaries with keys including `application_id` (int), `pet_name` (str), `applicant_name` (str), `date_submitted` (str)
  - `all_pets`: list of dictionaries with keys `pet_id` (int), `name` (str), `species` (str), `status` (str)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. User Data
- **Filename:** `users.txt`
- **Field Order:**
  1. username (str) - Unique username
  2. email (str) - User's email address
  3. phone (str) - Phone number
  4. address (str) - User's postal address
- **Example Data Rows:**
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pet Data
- **Filename:** `pets.txt`
- **Field Order:**
  1. pet_id (int) - Unique pet identifier
  2. name (str) - Pet's name
  3. species (str) - Pet species (Dog, Cat, Bird, Rabbit, Other)
  4. breed (str) - Pet breed
  5. age (str) - Age description (e.g., "3 years")
  6. gender (str) - Gender (Male, Female)
  7. size (str) - Size (Small, Medium, Large)
  8. description (str) - Detailed description
  9. shelter_id (int) - Identifier for shelter
  10. status (str) - Adoption status (Available, Pending, Adopted)
  11. date_added (str) - Date added in YYYY-MM-DD format
- **Example Data Rows:**
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- **Filename:** `applications.txt`
- **Field Order:**
  1. application_id (int) - Unique application identifier
  2. username (str) - Username of applicant
  3. pet_id (int) - Pet identifier
  4. applicant_name (str) - Applicant full name
  5. phone (str) - Applicant phone number
  6. address (str) - Applicant address
  7. housing_type (str) - Housing type (House, Apartment, Condo, Other)
  8. has_yard (str) - "Yes" or "No" indicating yard availability
  9. other_pets (str) - Description of other pets owned
  10. experience (str) - Experience with pets
  11. reason (str) - Reason for adopting
  12. status (str) - Status of application (Pending, Approved, Rejected)
  13. date_submitted (str) - Date in YYYY-MM-DD format
- **Example Data Rows:**
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- **Filename:** `favorites.txt`
- **Field Order:**
  1. username (str) - Username
  2. pet_id (int) - Pet identifier
  3. date_added (str) - Date added in YYYY-MM-DD format
- **Example Data Rows:**
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- **Filename:** `messages.txt`
- **Field Order:**
  1. message_id (int) - Unique message identifier
  2. sender_username (str) - Sender username
  3. recipient_username (str) - Recipient username
  4. subject (str) - Message subject
  5. content (str) - Message body content
  6. timestamp (str) - Timestamp in `YYYY-MM-DD HH:MM:SS` format
  7. is_read (bool as str) - "true" or "false" indicating if message was read
- **Example Data Rows:**
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- **Filename:** `adoption_history.txt`
- **Field Order:**
  1. history_id (int) - Unique history entry identifier
  2. username (str) - Username of adopter
  3. pet_id (int) - Pet identifier
  4. pet_name (str) - Pet name
  5. adoption_date (str) - Adoption date in YYYY-MM-DD
  6. shelter_id (int) - Shelter identifier
- **Example Data Rows:**
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- **Filename:** `shelters.txt`
- **Field Order:**
  1. shelter_id (int) - Unique shelter identifier
  2. name (str) - Shelter name
  3. address (str) - Shelter address
  4. phone (str) - Shelter phone number
  5. email (str) - Shelter email
- **Example Data Rows:**
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

End of Design Specification Document.
