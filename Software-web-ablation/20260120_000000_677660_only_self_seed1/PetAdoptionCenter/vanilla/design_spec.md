# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                | Function Name          | HTTP Method | Template File Rendered      | Context Variables (name: type)                                                                                         |
|---------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`        | GET         | None (Redirect to /dashboard) | None                                                                                                                   |
| `/dashboard`              | `dashboard`            | GET         | `dashboard.html`             | featured_pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str))                                    |
| `/pets`                   | `pet_listings`         | GET         | `pet_listings.html`          | pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str, optional for frontend))      |
| `/pets`                   | `pet_listings_filter`  | POST        | `pet_listings.html`          | pets: list of dicts (as above)                                                                                         |
| `/pets/<int:pet_id>`      | `pet_details`          | GET         | `pet_details.html`           | pet: dict (`pet_id`(int), `name`(str), `species`(str), `description`(str))                                              |
| `/pets/add`               | `add_pet`              | GET         | `add_pet.html`               | None                                                                                                                   |
| `/pets/add`               | `submit_new_pet`       | POST        | `add_pet.html`               | success_message: str, or error_message: str                                                                            |
| `/applications/adopt/<int:pet_id>` | `adoption_application_form` | GET         | `application.html`           | pet_id: int                                                                                                            |
| `/applications/adopt/<int:pet_id>` | `submit_adoption_application` | POST        | `application.html`           | success_message: str, or error_message: str                                                                            |
| `/applications/my`        | `my_applications`      | GET         | `my_applications.html`       | applications: list of dicts (`application_id`(int), `pet_name`(str), `date_submitted`(str), `status`(str))                |
| `/favorites`              | `favorites`            | GET         | `favorites.html`             | favorite_pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str))                                    |
| `/messages`               | `messages`             | GET         | `messages.html`              | conversations: list of dicts (`conversation_id`(int), `participants`(list of str), `last_message`(str))                     |
| `/messages/send`          | `send_message`         | POST        | `messages.html`              | success_message: str, or error_message: str                                                                            |
| `/profile`                | `user_profile`         | GET         | `profile.html`               | username: str, email: str                                                                                              |
| `/profile`                | `update_profile`       | POST        | `profile.html`               | success_message: str, or error_message: str                                                                            |
| `/admin`                  | `admin_panel`          | GET         | `admin_panel.html`           | pending_applications: list of dicts (`application_id`(int), `applicant_name`(str), `pet_name`(str)),
|                           |                        |             |                             | all_pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `status`(str))                                     |

### Details and Notes:
- The root route `/` redirects to `/dashboard`.
- For form submissions (e.g., adding a pet, submitting an application, sending messages, profile updates), POST method is used.
- Context variables are typed precisely.
- For routes returning lists (pets, applications, messages), each item in the list is a dictionary defined with exact keys and types.
- For pet listings and favorites, `photo_url` is optional for frontend display if images are supported (not specified but allowed for UI).

---

## Section 2: HTML Template Specifications (Frontend Focus)

| Template File Path        | Page Title              | Element IDs and Types                                                                                                 | Navigation Mappings                                                                                                    | Context Variables Available                                                                                   |
|---------------------------|-------------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `templates/dashboard.html` | Pet Adoption Dashboard  | `dashboard-page`(div), `featured-pets`(div), `browse-pets-button`(button), `back-to-dashboard`(button)              | `browse-pets-button` -> `url_for('pet_listings')`
`back-to-dashboard` -> refresh current page                       | featured_pets: list of dict (pet_id:int, name:str, species:str, age:str)                                       |
| `templates/pet_listings.html` | Available Pets          | `pet-listings-page`(div), `search-input`(input), `filter-species`(dropdown), `pet-grid`(div), `back-to-dashboard`(button) | `back-to-dashboard` -> `url_for('dashboard')`
Pet cards in `pet-grid` link to `url_for('pet_details', pet_id=pet.pet_id)` | pets: list of dict (pet_id:int, name:str, species:str, age:str)                                              |
| `templates/pet_details.html` | Pet Details              | `pet-details-page`(div), `pet-name`(h1), `pet-species`(div), `pet-description`(div), `adopt-button`(button), `back-to-listings`(button) | `adopt-button` -> `url_for('adoption_application_form', pet_id=pet.pet_id)`
`back-to-listings` -> `url_for('pet_listings')` | pet: dict (pet_id:int, name:str, species:str, description:str)                                               |
| `templates/add_pet.html`     | Add New Pet              | `add-pet-page`(div), `pet-name-input`(input), `pet-species-input`(dropdown), `pet-breed-input`(input), `pet-age-input`(input), `pet-gender-input`(dropdown), `pet-size-input`(dropdown), `pet-description-input`(textarea), `submit-pet-button`(button), `back-to-dashboard`(button) | `back-to-dashboard` -> `url_for('dashboard')`                                                                  | None                                                                                                          |
| `templates/application.html` | Adoption Application     | `application-page`(div), `applicant-name`(input), `applicant-phone`(input), `housing-type`(dropdown), `reason`(textarea), `submit-application-button`(button), `back-to-pet`(button) | `back-to-pet` -> `url_for('pet_details', pet_id=pet_id)`                                                       | pet_id: int                                                                                                   |
| `templates/my_applications.html` | My Applications        | `my-applications-page`(div), `filter-status`(dropdown), `applications-table`(table), `back-to-dashboard`(button)       | `back-to-dashboard` -> `url_for('dashboard')`                                                                   | applications: list of dict (application_id:int, pet_name:str, date_submitted:str, status:str)                  |
| `templates/favorites.html`    | My Favorites             | `favorites-page`(div), `favorites-grid`(div), `back-to-dashboard`(button)                                           | `back-to-dashboard` -> `url_for('dashboard')`
Pet cards link to `url_for('pet_details', pet_id=pet.pet_id)`      | favorite_pets: list of dict (pet_id:int, name:str, species:str, age:str)                                      |
| `templates/messages.html`     | Messages                 | `messages-page`(div), `conversation-list`(div), `message-input`(textarea), `send-message-button`(button), `back-to-dashboard`(button) | `back-to-dashboard` -> `url_for('dashboard')`                                                                   | conversations: list of dict (conversation_id:int, participants:list of str, last_message:str)                  |
| `templates/profile.html`      | My Profile               | `profile-page`(div), `profile-username`(div), `profile-email`(input), `update-profile-button`(button), `back-to-dashboard`(button) | `back-to-dashboard` -> `url_for('dashboard')`                                                                   | username: str, email: str                                                                                      |
| `templates/admin_panel.html`  | Admin Panel              | `admin-panel-page`(div), `pending-applications`(div), `all-pets-list`(div), `back-to-dashboard`(button)               | `back-to-dashboard` -> `url_for('dashboard')`                                                                   | pending_applications: list of dict (application_id:int, applicant_name:str, pet_name:str), all_pets: list of dict (pet_id:int, name:str, species:str, status:str) |

---

## Section 3: Data File Schemas (Backend Focus)

### 1. User Data
- **Filename**: `users.txt`
- **Fields (pipe-delimited)**: `username|email|phone|address`
- **Description**: Stores basic user data including contact info and address.
- **Example**:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pet Data
- **Filename**: `pets.txt`
- **Fields (pipe-delimited)**: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- **Description**: Holds all pet details including adoption status and shelter association.
- **Example**:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- **Filename**: `applications.txt`
- **Fields (pipe-delimited)**: `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- **Description**: Records adoption applications with applicant details and application status.
- **Example**:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- **Filename**: `favorites.txt`
- **Fields (pipe-delimited)**: `username|pet_id|date_added`
- **Description**: Keeps track of pets favorited by users.
- **Example**:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- **Filename**: `messages.txt`
- **Fields (pipe-delimited)**: `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- **Description**: Stores messages between users and shelters; `is_read` is boolean serialized as `true` or `false`.
- **Example**:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- **Filename**: `adoption_history.txt`
- **Fields (pipe-delimited)**: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- **Description**: Historical record of successful pet adoptions.
- **Example**:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- **Filename**: `shelters.txt`
- **Fields (pipe-delimited)**: `shelter_id|name|address|phone|email`
- **Description**: Information about shelters housing pets.
- **Example**:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This design specification enables independent parallel development:
- Backend developers implement Flask routes and handle data strictly per Sections 1 and 3.
- Frontend developers create HTML templates based strictly on Section 2 requirements.
- No cross-dependencies or assumptions outside this spec are necessary.

All IDs, route names, context variable names, and data schema formats are explicitly stated to ensure exact coherence between backend and frontend.

---
