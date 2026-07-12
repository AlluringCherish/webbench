# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                | Function Name          | HTTP Method(s) | Template File Rendered        | Context Variables (name:type)                                                                                                                    |
|---------------------------|------------------------|----------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| /                         | root_redirect          | GET            | Redirect to /dashboard        | None                                                                                                                                            |
| /dashboard                | dashboard              | GET            | dashboard.html                | featured_pets: List[Dict[str, Any]]  # List of up to 5 dictionaries representing pets with keys: id (int), name (str), species (str), age (str), photo_url (str)
|                           |                        |                |                               | recent_activities: List[str]  # List of strings describing recent activities                                                                       |
| /pets                     | pet_listings           | GET            | pet_listings.html             | pets: List[Dict[str, Any]]  # List of all pet dictionaries with keys: id (int), name (str), species (str), age (str), photo_url (str)               |
|                           |                        |                |                               | filters: Dict[str, List[str]]   # E.g., {'species': ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']}                                                |
| /pets                     | pet_listings_post      | POST           | Redirect or render pet_listings.html | search_query: str (request.form) - for searching pets by name
|                           |                        |                |                               | selected_species: str (request.form) - species filter                                                                                             |
| /pets/<int:pet_id>        | pet_details            | GET            | pet_details.html              | pet: Dict[str, Any]  # Details of the specific pet with keys: id (int), name (str), species (str), description (str), age (str), gender (str)       |
|                           |                        |                |                               | shelter: Dict[str, Any]  # Shelter info with keys: id (int), name (str), address (str), phone (str), email (str)                                   |
| /pets/<int:pet_id>/adopt  | adoption_application   | GET            | adoption_application.html     | pet: Dict[str, Any]  # Pet details including id (int), name (str)
|
| /pets/<int:pet_id>/adopt  | submit_adoption        | POST           | Redirect or render adoption_application.html | application_data: dict from form data: applicant_name (str), applicant_phone (str), housing_type (str), reason (str)                              |
| /add-pet                  | add_pet_page           | GET            | add_pet.html                  | None                                                                                                                                            |
| /add-pet                  | submit_pet             | POST           | Redirect or render add_pet.html | pet_data: dict from form inputs: name (str), species (str), breed (str), age (str), gender (str), size (str), description (str)                    |
| /applications             | my_applications        | GET            | my_applications.html          | applications: List[Dict[str, Any]]  # Applications by current user with keys: application_id (int), pet_name (str), date (str), status (str)         |
|                           |                        |                |                               | filter_status: str (optional query param)                                                                                                       |
| /favorites                | favorites_page         | GET            | favorites.html                | favorite_pets: List[Dict[str, Any]]  # List of pet dicts user marked as favorites                                                                 |
| /messages                 | messages_page          | GET            | messages.html                 | conversations: List[Dict[str, Any]]  # Conversations summaries
|
| /messages/send            | send_message           | POST           | Redirect or messages.html     | message_data: dict from form: recipient_username (str), subject (str), content (str)                                                             |
| /profile                  | user_profile           | GET            | profile.html                  | user_profile: Dict[str, str]  # username (str), email (str), phone (str), address (str)                                                           |
| /profile                  | update_profile         | POST           | Redirect or profile.html      | updated_profile_data from form: email (str)                                                                                                     |
| /admin                   | admin_panel            | GET            | admin_panel.html              | pending_applications: List[Dict[str, Any]]  # Pending applications with details
|                           |                        |                |                               | all_pets: List[Dict[str, Any]]  # List of all pets with full details                                                                             |


### Additional Route Details
- The root route `/` redirects to `/dashboard`.
- Form submission routes use POST method and redirect back or render the same page with messages.
- Routes include URL parameter `pet_id` for identifying pets where needed.


---

## Section 2: HTML Template Specifications (Frontend Focus)

Each template resides in the `templates/` directory.

---

### 1. templates/dashboard.html
- Page Title: Pet Adoption Dashboard
- <title> and <h1>: "Pet Adoption Dashboard"
- Element IDs and types:
  - dashboard-page (div)
  - featured-pets (div)
  - browse-pets-button (button)
  - back-to-dashboard (button)
- Navigation:
  - browse-pets-button navigates to `{{ url_for('pet_listings') }}`
  - back-to-dashboard triggers page refresh or redirects to `{{ url_for('dashboard') }}`
- Context Variables:
  - featured_pets: List of dicts with keys: id (int), name (str), species (str), age (str), photo_url (str)
  - recent_activities: List of strings

---

### 2. templates/pet_listings.html
- Page Title: Available Pets
- <title> and <h1>: "Available Pets"
- Element IDs and types:
  - pet-listings-page (div)
  - search-input (input, text)
  - filter-species (select/dropdown)
  - pet-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - pets: List of dicts with keys: id (int), name (str), species (str), age (str), photo_url (str)
  - filters: dict with 'species' key mapping to list of species options

---

### 3. templates/pet_details.html
- Page Title: Pet Details
- <title> and <h1>: "Pet Details"
- Element IDs and types:
  - pet-details-page (div)
  - pet-name (h1)
  - pet-species (div)
  - pet-description (div)
  - adopt-button (button)
  - back-to-listings (button)
- Navigation:
  - adopt-button navigates to `{{ url_for('adoption_application', pet_id=pet.id) }}`
  - back-to-listings navigates to `{{ url_for('pet_listings') }}`
- Context Variables:
  - pet: dict with id (int), name (str), species (str), description (str), age (str), gender (str)
  - shelter: dict with id (int), name (str), address (str), phone (str), email (str)

---

### 4. templates/add_pet.html
- Page Title: Add New Pet
- <title> and <h1>: "Add New Pet"
- Element IDs and types:
  - add-pet-page (div)
  - pet-name-input (input, text)
  - pet-species-input (select/dropdown)
  - pet-breed-input (input, text)
  - pet-age-input (input, text)
  - pet-gender-input (select/dropdown)
  - pet-size-input (select/dropdown)
  - pet-description-input (textarea)
  - submit-pet-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - None

---

### 5. templates/adoption_application.html
- Page Title: Adoption Application
- <title> and <h1>: "Adoption Application"
- Element IDs and types:
  - application-page (div)
  - applicant-name (input, text)
  - applicant-phone (input, text)
  - housing-type (select/dropdown)
  - reason (textarea)
  - submit-application-button (button)
  - back-to-pet (button)
- Navigation:
  - back-to-pet navigates to `{{ url_for('pet_details', pet_id=pet.id) }}`
- Context Variables:
  - pet: dict with id (int), name (str)

---

### 6. templates/my_applications.html
- Page Title: My Applications
- <title> and <h1>: "My Applications"
- Element IDs and types:
  - my-applications-page (div)
  - filter-status (select/dropdown)
  - applications-table (table)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - applications: List of dicts with keys: application_id (int), pet_name (str), date (str), status (str)

---

### 7. templates/favorites.html
- Page Title: My Favorites
- <title> and <h1>: "My Favorites"
- Element IDs and types:
  - favorites-page (div)
  - favorites-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - favorite_pets: List of pet dicts with keys: id (int), name (str), species (str), age (str), photo_url (str)

---

### 8. templates/messages.html
- Page Title: Messages
- <title> and <h1>: "Messages"
- Element IDs and types:
  - messages-page (div)
  - conversation-list (div)
  - message-input (textarea)
  - send-message-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - conversations: List of dicts with conversation details including last message, interlocutor

---

### 9. templates/profile.html
- Page Title: My Profile
- <title> and <h1>: "My Profile"
- Element IDs and types:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input, text)
  - update-profile-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - user_profile: dict with username (str), email (str), phone (str), address (str)

---

### 10. templates/admin_panel.html
- Page Title: Admin Panel
- <title> and <h1>: "Admin Panel"
- Element IDs and types:
  - admin-panel-page (div)
  - pending-applications (div)
  - all-pets-list (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard navigates to `{{ url_for('dashboard') }}`
- Context Variables:
  - pending_applications: List of application dicts (id, pet_name, applicant_name, date, status)
  - all_pets: List of all pet dicts with full details

---

## Section 3: Data File Schemas (Backend Focus)

All data files are located in the `data/` directory.

### 1. users.txt
- Fields (pipe-delimited):
  - username (str) | email (str) | phone (str) | address (str)
- Description: Stores user contact information
- Example Rows:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- Fields (pipe-delimited):
  - pet_id (int) | name (str) | species (str) | breed (str) | age (str) | gender (str) | size (str) | description (str) | shelter_id (int) | status (str) | date_added (str: YYYY-MM-DD)
- Description: Stores pet adoption listing details
- Example Rows:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- Fields (pipe-delimited):
  - application_id (int) | username (str) | pet_id (int) | applicant_name (str) | phone (str) | address (str) | housing_type (str) | has_yard (str: Yes/No) | other_pets (str) | experience (str) | reason (str) | status (str) | date_submitted (str: YYYY-MM-DD)
- Description: Stores adoption application details
- Example Rows:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- Fields (pipe-delimited):
  - username (str) | pet_id (int) | date_added (str: YYYY-MM-DD)
- Description: Stores users' favorite pets
- Example Rows:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- Fields (pipe-delimited):
  - message_id (int) | sender_username (str) | recipient_username (str) | subject (str) | content (str) | timestamp (str: YYYY-MM-DD HH:MM:SS) | is_read (bool as 'true'/'false')
- Description: Stores messages between users and shelters/admins
- Example Rows:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- Fields (pipe-delimited):
  - history_id (int) | username (str) | pet_id (int) | pet_name (str) | adoption_date (str: YYYY-MM-DD) | shelter_id (int)
- Description: Stores records of completed adoptions
- Example Rows:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- Fields (pipe-delimited):
  - shelter_id (int) | name (str) | address (str) | phone (str) | email (str)
- Description: Stores shelter information
- Example Rows:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

**End of Design Specification**
