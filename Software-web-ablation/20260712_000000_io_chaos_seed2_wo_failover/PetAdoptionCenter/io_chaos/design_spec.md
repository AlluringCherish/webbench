# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path               | Function Name            | HTTP Method | Template File           | Context Variables (Name: Type)                                                  |
|--------------------------|--------------------------|-------------|------------------------|---------------------------------------------------------------------------------|
| /                        | root_redirect            | GET         | None (Redirect)         | None                                                                            |
| /dashboard               | dashboard                | GET         | dashboard.html         | featured_pets: list of dict                                                     |
| /pets                    | pet_listings             | GET         | pet_listings.html      | pets: list of dict                                                              |
| /pets/<int:pet_id>       | pet_details              | GET         | pet_details.html       | pet: dict                                                                       |
| /add_pet                 | add_pet                  | GET, POST   | add_pet.html           | GET: None, POST: success_msg (str), error_msg (str) optional                     |
| /apply/<int:pet_id>      | adoption_application     | GET, POST   | adoption_application.html | GET: pet: dict, POST: success_msg (str), error_msg (str) optional               |
| /my_applications         | my_applications          | GET         | my_applications.html   | applications: list of dict                                                      |
| /favorites               | favorites                | GET         | favorites.html         | favorite_pets: list of dict                                                     |
| /messages                | messages                 | GET, POST   | messages.html          | GET: conversations: list of dict, POST: error_msg (str) optional                |
| /profile                 | profile                  | GET, POST   | profile.html           | GET: user_profile: dict, POST: success_msg (str), error_msg (str) optional       |
| /admin                   | admin_panel              | GET         | admin_panel.html       | pending_applications: list of dict, all_pets: list of dict                      |

### Details:

- The root route `/` redirects to `/dashboard`.
- `dashboard` route shows featured pets (limit 5), recent activities can be included as context.
- `pet_listings` provides all pets available with filtering handled frontend.
- `pet_details` delivers detailed info for a pet identified by `<int:pet_id>`.
- `add_pet` supports GET to show form and POST to accept form data for new pet entry.
- `adoption_application` supports GET to show form for the pet `<pet_id>`, POST to submit application.
- `my_applications` shows all applications submitted by the current user.
- `favorites` shows all user's favorite pets.
- `messages` allows viewing conversations and sending messages via POST.
- `profile` allows viewing and updating user profile.
- `admin_panel` allows admin to manage applications and pet data.


## Section 2: HTML Template Specifications (Frontend Focus)

---

### 1. Dashboard Page
- File: `templates/dashboard.html`
- Title: "Pet Adoption Dashboard"
- <h1> Title: "Pet Adoption Dashboard"
- Element IDs and Types:
  - `dashboard-page`: div
  - `featured-pets`: div
  - `browse-pets-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `browse-pets-button` -> url_for('pet_listings')
  - `back-to-dashboard` -> url_for('dashboard') (refreshes page)
- Context Variables:
  - `featured_pets`: list of dict, each dict includes pet info (pet_id: int, name: str, species: str, age: str, photo_url: str)

---

### 2. Pet Listings Page
- File: `templates/pet_listings.html`
- Title: "Available Pets"
- <h1> Title: "Available Pets"
- Element IDs:
  - `pet-listings-page`: div
  - `search-input`: input
  - `filter-species`: select (dropdown)
  - `pet-grid`: div
  - `back-to-dashboard`: button
- Navigation:
  - Clicking pet cards (dynamic) links to url_for('pet_details', pet_id=pet.pet_id)
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - `pets`: list of dict, each dict with keys: pet_id (int), name (str), species (str), age (str), photo_url (str), breed (str)

---

### 3. Pet Details Page
- File: `templates/pet_details.html`
- Title: "Pet Details"
- <h1> Title: pet.name (dynamic)
- Element IDs:
  - `pet-details-page`: div
  - `pet-name`: h1
  - `pet-species`: div
  - `pet-description`: div
  - `adopt-button`: button
  - `back-to-listings`: button
- Navigation:
  - `adopt-button` -> url_for('adoption_application', pet_id=pet.pet_id)
  - `back-to-listings` -> url_for('pet_listings')
- Context Variables:
  - `pet`: dict with keys: pet_id (int), name (str), species (str), breed (str), age (str), gender (str), size (str), description (str)

---

### 4. Add Pet Page
- File: `templates/add_pet.html`
- Title: "Add New Pet"
- <h1> Title: "Add New Pet"
- Element IDs:
  - `add-pet-page`: div
  - `pet-name-input`: input
  - `pet-species-input`: select
  - `pet-breed-input`: input
  - `pet-age-input`: input
  - `pet-gender-input`: select
  - `pet-size-input`: select
  - `pet-description-input`: textarea
  - `submit-pet-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - on GET: none
  - on POST: success_msg: str, error_msg: str (optional)

---

### 5. Adoption Application Page
- File: `templates/adoption_application.html`
- Title: "Adoption Application"
- <h1> Title: "Adoption Application"
- Element IDs:
  - `application-page`: div
  - `applicant-name`: input
  - `applicant-phone`: input
  - `housing-type`: select
  - `reason`: textarea
  - `submit-application-button`: button
  - `back-to-pet`: button
- Navigation:
  - `back-to-pet` -> url_for('pet_details', pet_id=pet.pet_id)
- Context Variables:
  - on GET: pet: dict
  - on POST: success_msg: str, error_msg: str optional

---

### 6. My Applications Page
- File: `templates/my_applications.html`
- Title: "My Applications"
- <h1> Title: "My Applications"
- Element IDs:
  - `my-applications-page`: div
  - `filter-status`: select
  - `applications-table`: table
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - applications: list of dict, each dict includes: application_id (int), pet_name (str), date_submitted (str), status (str)

---

### 7. Favorites Page
- File: `templates/favorites.html`
- Title: "My Favorites"
- <h1> Title: "My Favorites"
- Element IDs:
  - `favorites-page`: div
  - `favorites-grid`: div
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - favorite_pets: list of dict (pet_id, name, species, photo_url)

---

### 8. Messages Page
- File: `templates/messages.html`
- Title: "Messages"
- <h1> Title: "Messages"
- Element IDs:
  - `messages-page`: div
  - `conversation-list`: div
  - `message-input`: textarea
  - `send-message-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - conversations: list of dict, each with sender_username (str), recipient_username (str), subject (str), content (str), timestamp (str), is_read (bool)

---

### 9. User Profile Page
- File: `templates/profile.html`
- Title: "My Profile"
- <h1> Title: "My Profile"
- Element IDs:
  - `profile-page`: div
  - `profile-username`: div
  - `profile-email`: input
  - `update-profile-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - user_profile: dict (username: str, email: str)

---

### 10. Admin Panel Page
- File: `templates/admin_panel.html`
- Title: "Admin Panel"
- <h1> Title: "Admin Panel"
- Element IDs:
  - `admin-panel-page`: div
  - `pending-applications`: div
  - `all-pets-list`: div
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` -> url_for('dashboard')
- Context Variables:
  - pending_applications: list of dict (application_id, applicant_name, pet_name, date_submitted, status)
  - all_pets: list of dict (pet_id, name, species, status)


## Section 3: Data File Schemas (Backend Focus)

---

### 1. users.txt
- Filename: `users.txt`
- Fields (pipe-delimited):
  - username (str)
  - email (str)
  - phone (str)
  - address (str)
- Example Data:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

---

### 2. pets.txt
- Filename: `pets.txt`
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
  - status (str) [Available, Pending, Adopted]
  - date_added (str, YYYY-MM-DD)
- Example Data:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

---

### 3. applications.txt
- Filename: `applications.txt`
- Fields (pipe-delimited):
  - application_id (int)
  - username (str)
  - pet_id (int)
  - applicant_name (str)
  - phone (str)
  - address (str)
  - housing_type (str)
  - has_yard (str) [Yes, No]
  - other_pets (str)
  - experience (str)
  - reason (str)
  - status (str) [Pending, Approved, Rejected]
  - date_submitted (str, YYYY-MM-DD)
- Example Data:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

---

### 4. favorites.txt
- Filename: `favorites.txt`
- Fields (pipe-delimited):
  - username (str)
  - pet_id (int)
  - date_added (str, YYYY-MM-DD)
- Example Data:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

---

### 5. messages.txt
- Filename: `messages.txt`
- Fields (pipe-delimited):
  - message_id (int)
  - sender_username (str)
  - recipient_username (str)
  - subject (str)
  - content (str)
  - timestamp (str, YYYY-MM-DD HH:MM:SS)
  - is_read (str) [true, false]
- Example Data:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

---

### 6. adoption_history.txt
- Filename: `adoption_history.txt`
- Fields (pipe-delimited):
  - history_id (int)
  - username (str)
  - pet_id (int)
  - pet_name (str)
  - adoption_date (str, YYYY-MM-DD)
  - shelter_id (int)
- Example Data:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

---

### 7. shelters.txt
- Filename: `shelters.txt`
- Fields (pipe-delimited):
  - shelter_id (int)
  - name (str)
  - address (str)
  - phone (str)
  - email (str)
- Example Data:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

*End of Design Specification for PetAdoptionCenter.*
