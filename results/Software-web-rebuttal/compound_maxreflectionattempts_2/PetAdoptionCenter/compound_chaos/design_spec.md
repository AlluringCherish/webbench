# PetAdoptionCenter Web Application Design Specification

---

## 1. Flask Routes Specification (Backend Focus)

| Route Path                  | Function Name          | HTTP Method(s) | Rendered Template      | Context Variables Passed                                                       |
|-----------------------------|------------------------|----------------|------------------------|--------------------------------------------------------------------------------|
| `/`                         | home_redirect          | GET            | N/A                    | N/A                                                                            |
| `/dashboard`                | dashboard              | GET            | `dashboard.html`       | `featured_pets` (list of dict)                                                  |
| `/pets`                    | pet_listings           | GET, POST      | `pet_listings.html`    | `pets` (list of dict), `filter_species` (str), `search_query` (str)             |
| `/pet/<int:pet_id>`         | pet_details            | GET            | `pet_details.html`     | `pet` (dict), `is_favorite` (bool)                                             |
| `/pet/add`                  | add_pet                | GET, POST      | `add_pet.html`         | N/A                                                                            |
| `/application/new/<int:pet_id>` | new_application       | GET, POST      | `application.html`     | `pet` (dict)                                                                   |
| `/applications`             | my_applications        | GET            | `my_applications.html` | `applications` (list of dict), `filter_status` (str)                           |
| `/favorites`                | favorites              | GET            | `favorites.html`       | `favorite_pets` (list of dict)                                                 |
| `/messages`                 | messages               | GET, POST      | `messages.html`        | `messages` (list of dict)                                                      |
| `/profile`                  | profile                | GET, POST      | `profile.html`         | `user` (dict)                                                                  |
| `/admin`                   | admin_panel            | GET, POST      | `admin_panel.html`     | `pending_applications` (list of dict), `all_pets` (list of dict)               |

- Root route `/` redirects to `/dashboard`.
- Form submission routes use POST method.

---

## 2. HTML Template Specifications (Frontend Focus)

### 2.1 `templates/dashboard.html`
- **Page Title**: Pet Adoption Dashboard
- **Main `<h1>`**: Pet Adoption Dashboard
- **Element IDs & Types:**
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `browse-pets-button`: `{{ url_for('pet_listings') }}` (click navigates to `/pets`)
  - `back-to-dashboard`: reloads `/dashboard`
- **Context Variables:**
  - `featured_pets`: list of dicts, each pet dict:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `age` (str)
    - `photo_url` (str, optional)

---

### 2.2 `templates/pet_listings.html`
- **Page Title**: Available Pets
- **Main `<h1>`**: Available Pets
- **Element IDs & Types:**
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (select)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
  - Clicking pet card navigates to `{{ url_for('pet_details', pet_id=pet.pet_id) }}`
- **Context Variables:**
  - `pets`: list of dicts; each dict:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `age` (str)
    - `photo_url` (str, optional)
  - `filter_species`: str
  - `search_query`: str

---

### 2.3 `templates/pet_details.html`
- **Page Title**: Pet Details
- **Main `<h1>`**: `{{ pet.name }}`
- **Element IDs & Types:**
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- **Navigation Mappings:**
  - `adopt-button`: `{{ url_for('new_application', pet_id=pet.pet_id) }}`
  - `back-to-listings`: `{{ url_for('pet_listings') }}`
- **Context Variables:**
  - `pet`: dict with keys:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `breed` (str)
    - `age` (str)
    - `gender` (str)
    - `size` (str)
    - `description` (str)
    - `shelter_id` (int)
    - `status` (str)
    - `date_added` (str)
  - `is_favorite`: bool

---

### 2.4 `templates/add_pet.html`
- **Page Title**: Add New Pet
- **Main `<h1>`**: Add New Pet
- **Element IDs & Types:**
  - `add-pet-page` (div)
  - `pet-name-input` (input)
  - `pet-species-input` (select)
  - `pet-breed-input` (input)
  - `pet-age-input` (input)
  - `pet-gender-input` (select)
  - `pet-size-input` (select)
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:** None (empty form)

---

### 2.5 `templates/application.html`
- **Page Title**: Adoption Application
- **Main `<h1>`**: Adoption Application
- **Element IDs & Types:**
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (select)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- **Navigation Mappings:**
  - `back-to-pet`: `{{ url_for('pet_details', pet_id=pet.pet_id) }}`
- **Context Variables:**
  - `pet`: dict (same structure as in pet_details.html)

---

### 2.6 `templates/my_applications.html`
- **Page Title**: My Applications
- **Main `<h1>`**: My Applications
- **Element IDs & Types:**
  - `my-applications-page` (div)
  - `filter-status` (select)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `applications`: list of dicts, each with:
    - `application_id` (int)
    - `pet_name` (str)
    - `date_submitted` (str)
    - `status` (str)
  - `filter_status`: str

---

### 2.7 `templates/favorites.html`
- **Page Title**: My Favorites
- **Main `<h1>`**: My Favorites
- **Element IDs & Types:**
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `favorite_pets`: list of dicts with pet details

---

### 2.8 `templates/messages.html`
- **Page Title**: Messages
- **Main `<h1>`**: Messages
- **Element IDs & Types:**
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `messages`: list of dicts

---

### 2.9 `templates/profile.html`
- **Page Title**: My Profile
- **Main `<h1>`**: My Profile
- **Element IDs & Types:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `user`: dict with `username` (str), `email` (str), `phone` (str), `address` (str)

---

### 2.10 `templates/admin_panel.html`
- **Page Title**: Admin Panel
- **Main `<h1>`**: Admin Panel
- **Element IDs & Types:**
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- **Navigation Mappings:**
  - `back-to-dashboard`: `{{ url_for('dashboard') }}`
- **Context Variables:**
  - `pending_applications`: list of dicts
  - `all_pets`: list of dicts

---

## 3. Data File Schemas (Backend Focus)

### 3.1 `users.txt`
- **Format:**
  ```
  username|email|phone|address
  ```
- **Description:** Stores registered users' information.
- **Example Rows:**
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

---

### 3.2 `pets.txt`
- **Format:**
  ```
  pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
  ```
- **Description:** Stores details of pets available for adoption or in shelter.
- **Example Rows:**
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

---

### 3.3 `applications.txt`
- **Format:**
  ```
  application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
  ```
- **Description:** Stores adoption application data.
- **Example Rows:**
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

---

### 3.4 `favorites.txt`
- **Format:**
  ```
  username|pet_id|date_added
  ```
- **Description:** Tracks pets favorited by users.
- **Example Rows:**
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

---

### 3.5 `messages.txt`
- **Format:**
  ```
  message_id|sender_username|recipient_username|subject|content|timestamp|is_read
  ```
- **Description:** Stores messages between users and shelters.
- **Example Rows:**
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

---

### 3.6 `adoption_history.txt`
- **Format:**
  ```
  history_id|username|pet_id|pet_name|adoption_date|shelter_id
  ```
- **Description:** Records past adoptions.
- **Example Rows:**
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

---

### 3.7 `shelters.txt`
- **Format:**
  ```
  shelter_id|name|address|phone|email
  ```
- **Description:** Contains shelter information.
- **Example Rows:**
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

# End of Design Specification

This file fully describes the Flask routes, HTML templates, and backend data file schemas enabling independent backend and frontend development.