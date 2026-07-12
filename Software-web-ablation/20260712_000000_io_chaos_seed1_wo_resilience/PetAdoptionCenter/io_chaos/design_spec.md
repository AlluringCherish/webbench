# PetAdoptionCenter Design Specifications

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                  | Function Name             | HTTP Method(s) | Template Rendered           | Context Variables (names and types)                                          |
|-----------------------------|---------------------------|----------------|-----------------------------|-------------------------------------------------------------------------------|
| /                            | root_redirect             | GET            | Redirects to `/dashboard`    | None                                                                          |
| /dashboard                   | dashboard                 | GET            | dashboard.html              | featured_pets (list of dict), recent_activities (list of dict, optional)      |
| /pets                       | pet_listings              | GET            | pet_listings.html           | pets (list of dict), species_filter (str)                                    |
| /pets/<int:pet_id>          | pet_details               | GET            | pet_details.html            | pet (dict)                                                                    |
| /pets/add                   | add_pet                   | GET, POST      | add_pet.html                | On GET: None; On POST: form submission handling                               |
| /applications/apply/<int:pet_id> | adoption_application  | GET, POST      | adoption_application.html   | On GET: pet (dict); On POST: form submission handling                         |
| /applications/my            | my_applications           | GET            | my_applications.html        | applications (list of dict), status_filter (str)                             |
| /favorites                  | favorites                 | GET            | favorites.html              | favorites (list of dict)                                                      |
| /messages                   | messages                  | GET, POST      | messages.html               | conversations (list of dict), messages (list of dict)                        |
| /profile                    | user_profile              | GET, POST      | profile.html                | user_profile (dict)                                                           |
| /admin                     | admin_panel               | GET            | admin_panel.html            | pending_applications (list of dict), all_pets (list of dict)                 |

### Notes on Context Variables:
- `featured_pets`: List of dicts representing pet objects with keys matching pet data fields.
- `pets`: List of dicts of available pets filtered as per query parameters.
- `species_filter`: String value representing selected species filter.
- `pet`: Dict with a pet's full fields.
- `applications`: List of dicts with adoption application details.
- `status_filter`: String, filter for application status.
- `favorites`: List of dicts representing pets favorited by the user.
- `conversations`: List of dicts representing message threads.
- `messages`: List of dicts representing messages in selected conversation.
- `user_profile`: Dict with user details: username, email, etc.
- `pending_applications`: List of dicts representing adoption applications with status "Pending".
- `all_pets`: List of dicts representing all pets, regardless of status.

### Route Details with Additional Backend Functionality:

- `/` (root): Redirects to `/dashboard`.

- `/dashboard`:
  - Renders dashboard.html with featured pets (max 5) and any recent activities.

- `/pets` (Pet Listings):
  - Supports query parameters for filtering species and search term.
  - Passes filtered pets list and species_filter string.

- `/pets/<int:pet_id>` (Pet Details):
  - Shows details of selected pet.

- `/pets/add` (Add Pet):
  - GET renders form.
  - POST processes form submission to add pet; redirects to dashboard or pet listings.

- `/applications/apply/<int:pet_id>` (Adoption Application):
  - GET renders adoption form for specific pet.
  - POST processes adoption application.

- `/applications/my` (My Applications):
  - Shows user's applications.
  - Supports filtering by application status.

- `/favorites` (My Favorites):
  - Shows pets user saved.

- `/messages` (Messages):
  - GET shows user's conversations.
  - POST submits new message.

- `/profile` (User Profile):
  - GET shows profile.
  - POST updates user info.

- `/admin` (Admin Panel):
  - Shows pending applications and all pets.


---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File path: `templates/dashboard.html`
- Page title and <h1>: `Pet Adoption Dashboard`
- Element IDs and types:
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button) - navigates to pet listings via `url_for('pet_listings')`
  - `back-to-dashboard` (button) - refreshes current page
- Context variables:
  - `featured_pets`: list of dicts with pet details
  - `recent_activities`: list of dicts (optional, if implemented)

### 2. Pet Listings Page
- File path: `templates/pet_listings.html`
- Page title and <h1>: `Available Pets`
- Element IDs and types:
  - `pet-listings-page` (div)
  - `search-input` (input type="text")
  - `filter-species` (select dropdown) - options: All, Dog, Cat, Bird, Rabbit, Other
  - `pet-grid` (div) - container for pet cards
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Navigation:
  - Pet cards link to pet details page with URL: `url_for('pet_details', pet_id=pet['pet_id'])`
- Context variables:
  - `pets`: list of dicts with pet data
  - `species_filter`: str

### 3. Pet Details Page
- File path: `templates/pet_details.html`
- Page title and <h1>: `Pet Details`
- Element IDs and types:
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button) - navigates to adoption application page using `url_for('adoption_application', pet_id=pet['pet_id'])`
  - `back-to-listings` (button) - navigates to pet listings via `url_for('pet_listings')`
- Context variables:
  - `pet`: dict with full pet details

### 4. Add Pet Page
- File path: `templates/add_pet.html`
- Page title and <h1>: `Add New Pet`
- Element IDs and types:
  - `add-pet-page` (div)
  - `pet-name-input` (input text)
  - `pet-species-input` (select dropdown) - Dog, Cat, Bird, Rabbit, Other
  - `pet-breed-input` (input text)
  - `pet-age-input` (input text)
  - `pet-gender-input` (select dropdown) - Male, Female
  - `pet-size-input` (select dropdown) - Small, Medium, Large
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button) - submits form, POST to `/pets/add`
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - None on GET
  - On errors (optional) form data and validation messages

### 5. Adoption Application Page
- File path: `templates/adoption_application.html`
- Page title and <h1>: `Adoption Application`
- Element IDs and types:
  - `application-page` (div)
  - `applicant-name` (input text)
  - `applicant-phone` (input text)
  - `housing-type` (select dropdown) - House, Apartment, Condo, Other
  - `reason` (textarea)
  - `submit-application-button` (button) - submits form, POST to `/applications/apply/<pet_id>`
  - `back-to-pet` (button) - navigates back to pet details via `url_for('pet_details', pet_id=pet['pet_id'])`
- Context variables:
  - `pet`: dict with pet details

### 6. My Applications Page
- File path: `templates/my_applications.html`
- Page title and <h1>: `My Applications`
- Element IDs and types:
  - `my-applications-page` (div)
  - `filter-status` (select dropdown) - All, Pending, Approved, Rejected
  - `applications-table` (table) - columns: Pet Name, Date, Status, Actions
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - `applications`: list of dicts with application details
  - `status_filter`: str

### 7. Favorites Page
- File path: `templates/favorites.html`
- Page title and <h1>: `My Favorites`
- Element IDs and types:
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - `favorites`: list of dicts with favorite pets

### 8. Messages Page
- File path: `templates/messages.html`
- Page title and <h1>: `Messages`
- Element IDs and types:
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button) - submits message, POST to `/messages`
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - `conversations`: list of dicts
  - `messages`: list of dicts

### 9. User Profile Page
- File path: `templates/profile.html`
- Page title and <h1>: `My Profile`
- Element IDs and types:
  - `profile-page` (div)
  - `profile-username` (div) - displays username, non-editable
  - `profile-email` (input text)
  - `update-profile-button` (button) - submits profile changes, POST to `/profile`
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - `user_profile`: dict with username, email, phone, address

### 10. Admin Panel Page
- File path: `templates/admin_panel.html`
- Page title and <h1>: `Admin Panel`
- Element IDs and types:
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button) - navigates to dashboard via `url_for('dashboard')`
- Context variables:
  - `pending_applications`: list of dicts
  - `all_pets`: list of dicts

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: `users.txt`
- Fields (pipe `|` delimited):
  - `username` (str) - unique user identifier
  - `email` (str) - user's email address
  - `phone` (str) - user phone number
  - `address` (str) - user mailing address
- Example data rows:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- Filename: `pets.txt`
- Fields (pipe `|` delimited):
  - `pet_id` (int) - unique pet identifier
  - `name` (str) - pet's name
  - `species` (str) - species (Dog, Cat, Bird, Rabbit, Other)
  - `breed` (str) - breed name
  - `age` (str) - age description (e.g., "3 years")
  - `gender` (str) - Male or Female
  - `size` (str) - Small, Medium, Large
  - `description` (str) - detailed description
  - `shelter_id` (int) - shelter identifier
  - `status` (str) - adoption status (Available, Pending, Adopted)
  - `date_added` (str) - ISO date string YYYY-MM-DD
- Example data rows:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- Filename: `applications.txt`
- Fields (pipe `|` delimited):
  - `application_id` (int) - unique application identifier
  - `username` (str) - applicant's username
  - `pet_id` (int) - pet identifier
  - `applicant_name` (str) - full name of applicant
  - `phone` (str) - phone number
  - `address` (str) - mailing address
  - `housing_type` (str) - housing description
  - `has_yard` (str) - Yes or No
  - `other_pets` (str) - description of other pets
  - `experience` (str) - pet experience description
  - `reason` (str) - reason for adoption
  - `status` (str) - application status (Pending, Approved, Rejected)
  - `date_submitted` (str) - ISO date YYYY-MM-DD
- Example data rows:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- Filename: `favorites.txt`
- Fields (pipe `|` delimited):
  - `username` (str) - user who favorited
  - `pet_id` (int) - pet identifier
  - `date_added` (str) - ISO date YYYY-MM-DD
- Example data rows:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- Filename: `messages.txt`
- Fields (pipe `|` delimited):
  - `message_id` (int) - unique message identifier
  - `sender_username` (str) - sender username
  - `recipient_username` (str) - recipient username
  - `subject` (str) - message subject
  - `content` (str) - message content body
  - `timestamp` (str) - datetime YYYY-MM-DD HH:MM:SS
  - `is_read` (str) - "true" or "false" indicating read status
- Example data rows:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- Filename: `adoption_history.txt`
- Fields (pipe `|` delimited):
  - `history_id` (int) - unique adoption history record ID
  - `username` (str) - adopter's username
  - `pet_id` (int) - pet ID
  - `pet_name` (str) - pet name
  - `adoption_date` (str) - ISO date YYYY-MM-DD
  - `shelter_id` (int) - shelter ID
- Example data rows:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- Filename: `shelters.txt`
- Fields (pipe `|` delimited):
  - `shelter_id` (int) - unique shelter identifier
  - `name` (str) - shelter name
  - `address` (str) - shelter address
  - `phone` (str) - shelter phone number
  - `email` (str) - shelter email
- Example data rows:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This specification enables backend and frontend developers to work independently, given complete and precise definitions of routes, templates, and data structures.

For any dynamic navigation in templates, use Flask's `url_for` with exact function names stated in Section 1 and include dynamic parameters accordingly with Jinja2 syntax (e.g., `{{ pet.pet_id }}`).

All context variable names, template IDs, element types, and data fields must be strictly adhered to for full system integration.
