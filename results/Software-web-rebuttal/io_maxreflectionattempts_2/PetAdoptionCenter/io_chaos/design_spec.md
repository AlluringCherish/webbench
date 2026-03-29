# PetAdoptionCenter Flask Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path             | Function Name          | HTTP Method | Template Rendered            | Context Variables Passed (name: type)                        |
|------------------------|------------------------|-------------|-----------------------------|--------------------------------------------------------------|
| /                      | root_redirect          | GET         | None (Redirect to /dashboard) | None                                                         |
| /dashboard             | dashboard_page         | GET         | dashboard.html              | featured_pets: list of dict                                    |
| /pets                  | pet_listings_page      | GET         | pet_listings.html           | pets: list of dict                                            |
| /search_pets           | search_pets            | POST        | pet_listings.html           | pets: list of dict (filtered based on search/filter)          |
| /pets/<int:pet_id>     | pet_details_page       | GET         | pet_details.html            | pet: dict                                                    |
| /add_pet               | add_pet_page           | GET         | add_pet.html                | None                                                         |
| /submit_pet            | submit_pet             | POST        | redirect to /pets           | None                                                         |
| /apply_adoption/<int:pet_id> | adoption_application_page | GET         | adoption_application.html   | pet: dict                                                    |
| /submit_application/<int:pet_id> | submit_application  | POST        | redirect to /my_applications | None                                                         |
| /my_applications       | my_applications_page   | GET         | my_applications.html        | applications: list of dict                                    |
| /filter_applications    | filter_applications    | POST        | my_applications.html        | applications: list of dict (filtered by status)                |
| /favorites             | favorites_page         | GET         | favorites.html              | favorites: list of dict                                      |
| /messages              | messages_page          | GET         | messages.html               | conversations: list of dict                                   |
| /send_message          | send_message           | POST        | redirect to /messages       | None                                                         |
| /profile               | user_profile_page      | GET         | profile.html                | user_info: dict                                             |
| /update_profile        | update_profile         | POST        | redirect to /profile        | None                                                         |
| /admin_panel           | admin_panel_page       | GET         | admin_panel.html            | pending_applications: list of dict, all_pets: list of dict    |
| /edit_pet/<int:pet_id> | edit_pet_page          | GET         | add_pet.html (for editing)  | pet: dict                                                    |
| /delete_pet/<int:pet_id> | delete_pet            | POST        | redirect to /admin_panel    | None                                                         |

### Notes on Backend Routes:
- The root `/` route redirects to `/dashboard`.
- Routes that process forms use POST method (`/submit_pet`, `/submit_application/<int:pet_id>`, `/send_message`, `/update_profile`, `/delete_pet`, `/search_pets`, `/filter_applications`).
- Context variables for templates are typed exactly as follows:
  - `list of dict` = List where each element is a dictionary representing a record (e.g., pets, applications).
  - `dict` = Single dictionary for one item (e.g., a pet, user info).
- Redirects happen after POST submissions to prevent form resubmission.

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. templates/dashboard.html
- Page Title (<title> and <h1>): "Pet Adoption Dashboard"
- Element IDs:
  - dashboard-page (div)
  - featured-pets (div)
  - browse-pets-button (button)
  - back-to-dashboard (button)
- Navigation:
  - browse-pets-button: `url_for('pet_listings_page')`
  - back-to-dashboard: reload current page (dashboard)
- Context Variables:
  - featured_pets: list of dict with keys - pet_id (int), name (str), species (str), age (str), photo_url (str)

### 2. templates/pet_listings.html
- Page Title: "Available Pets"
- Element IDs:
  - pet-listings-page (div)
  - search-input (input)
  - filter-species (select/dropdown)
  - pet-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
  - Each pet card in pet-grid should link to pet details using pet_id via `url_for('pet_details_page', pet_id=pet.pet_id)`
- Context Variables:
  - pets: list of dict with keys - pet_id (int), name (str), species (str), age (str), photo_url (str)

### 3. templates/pet_details.html
- Page Title: "Pet Details"
- Element IDs:
  - pet-details-page (div)
  - pet-name (h1)
  - pet-species (div)
  - pet-description (div)
  - adopt-button (button)
  - back-to-listings (button)
- Navigation:
  - adopt-button: `url_for('adoption_application_page', pet_id=pet.pet_id)`
  - back-to-listings: `url_for('pet_listings_page')`
- Context Variables:
  - pet: dict with fields - pet_id (int), name (str), species (str), breed (str), age (str), gender (str), size (str), description (str), status (str)

### 4. templates/add_pet.html
- Page Title: "Add New Pet"
- Element IDs:
  - add-pet-page (div)
  - pet-name-input (input)
  - pet-species-input (select/dropdown)
  - pet-breed-input (input)
  - pet-age-input (input)
  - pet-gender-input (select/dropdown)
  - pet-size-input (select/dropdown)
  - pet-description-input (textarea)
  - submit-pet-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - When editing also get pet: dict with above pet fields
  - Species options: Dog, Cat, Bird, Rabbit, Other
  - Gender options: Male, Female
  - Size options: Small, Medium, Large

### 5. templates/adoption_application.html
- Page Title: "Adoption Application"
- Element IDs:
  - application-page (div)
  - applicant-name (input)
  - applicant-phone (input)
  - housing-type (select/dropdown)
  - reason (textarea)
  - submit-application-button (button)
  - back-to-pet (button)
- Navigation:
  - back-to-pet: `url_for('pet_details_page', pet_id=pet.pet_id)`
- Context Variables:
  - pet: dict with fields - pet_id (int), name (str)
  - Housing type options: House, Apartment, Condo, Other

### 6. templates/my_applications.html
- Page Title: "My Applications"
- Element IDs:
  - my-applications-page (div)
  - filter-status (select/dropdown)
  - applications-table (table)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - applications: list of dict with keys - application_id (int), pet_name (str), date_submitted (str), status (str)

### 7. templates/favorites.html
- Page Title: "My Favorites"
- Element IDs:
  - favorites-page (div)
  - favorites-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - favorites: list of dict with keys - pet_id (int), name (str), species (str), age (str), photo_url (str)

### 8. templates/messages.html
- Page Title: "Messages"
- Element IDs:
  - messages-page (div)
  - conversation-list (div)
  - message-input (textarea)
  - send-message-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - conversations: list of dict with keys - conversation_id (int), other_party_username (str), last_message_preview (str), last_message_timestamp (str)

### 9. templates/profile.html
- Page Title: "My Profile"
- Element IDs:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - user_info: dict with keys - username (str), email (str)

### 10. templates/admin_panel.html
- Page Title: "Admin Panel"
- Element IDs:
  - admin-panel-page (div)
  - pending-applications (div)
  - all-pets-list (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - pending_applications: list of dict with keys - application_id (int), applicant_name (str), pet_name (str), date_submitted (str), status (str)
  - all_pets: list of dict with keys - pet_id (int), name (str), species (str), status (str)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Fields (pipe-delimited):
  - username (str)
  - email (str)
  - phone (str)
  - address (str)
- Example Rows:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- Fields (pipe-delimited):
  - pet_id (int)
  - name (str)
  - species (str)
  - breed (str)
  - age (str)
  - gender (str)
  - size (str)
  - description (str)
  - shelter_id (int)
  - status (str)  # e.g., Available, Pending
  - date_added (str)  # Format: YYYY-MM-DD
- Example Rows:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- Fields (pipe-delimited):
  - application_id (int)
  - username (str)
  - pet_id (int)
  - applicant_name (str)
  - phone (str)
  - address (str)
  - housing_type (str)
  - has_yard (str)  # Yes/No
  - other_pets (str)
  - experience (str)
  - reason (str)
  - status (str)  # Pending, Approved, Rejected
  - date_submitted (str)  # Format: YYYY-MM-DD
- Example Rows:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- Fields (pipe-delimited):
  - username (str)
  - pet_id (int)
  - date_added (str)  # Format: YYYY-MM-DD
- Example Rows:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- Fields (pipe-delimited):
  - message_id (int)
  - sender_username (str)
  - recipient_username (str)
  - subject (str)
  - content (str)
  - timestamp (str)  # Format: YYYY-MM-DD HH:MM:SS
  - is_read (str)  # "true" or "false"
- Example Rows:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- Fields (pipe-delimited):
  - history_id (int)
  - username (str)
  - pet_id (int)
  - pet_name (str)
  - adoption_date (str)  # Format: YYYY-MM-DD
  - shelter_id (int)
- Example Rows:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- Fields (pipe-delimited):
  - shelter_id (int)
  - name (str)
  - address (str)
  - phone (str)
  - email (str)
- Example Rows:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This completes the comprehensive design specification covering the Flask routes, HTML templates, and data schemas for backend and frontend developers to work independently and in parallel.
