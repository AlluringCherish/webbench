# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

### 1. Root Route
- **Path:** `/`
- **Function:** `root_redirect`
- **HTTP Methods:** GET
- **Template:** None (redirects to `/dashboard`)
- **Context Variables:** None

### 2. Dashboard
- **Path:** `/dashboard`
- **Function:** `dashboard`
- **HTTP Methods:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_pets` (list of dict): Featured pets, each dict with keys: `pet_id` (int), `name` (str), `species` (str), `breed` (str), `age` (str), `gender` (str), `size` (str), `description` (str)
  - `recent_activities` (list of dict): Recent actions or updates

### 3. Pet Listings
- **Path:** `/pets`
- **Function:** `pets_listing`
- **HTTP Methods:** GET, POST
- **Template:** `pets.html`
- **Context Variables:**
  - `pets` (list of dict): Available pets with keys as in featured_pets plus `status` (str), `date_added` (str)
  - `filter_species` (str): Current species filter
  - `search_text` (str): Current search input
- **POST Form Fields:**
  - `search_input` (str)
  - `filter_species` (str)

### 4. Pet Details
- **Path:** `/pets/<int:pet_id>`
- **Function:** `pet_details`
- **HTTP Methods:** GET
- **Template:** `pet_details.html`
- **Context Variables:**
  - `pet` (dict): Detailed pet data

### 5. Add Pet (Admin Only)
- **Path:** `/add-pet`
- **Function:** `add_pet`
- **HTTP Methods:** GET, POST
- **Template:** `add_pet.html`
- **Context Variables:** None (GET)
- **POST Form Fields:**
  - `pet_name` (str)
  - `pet_species` (str)
  - `pet_breed` (str)
  - `pet_age` (str)
  - `pet_gender` (str)
  - `pet_size` (str)
  - `pet_description` (str)

### 6. Adoption Application
- **Path:** `/apply/<int:pet_id>`
- **Function:** `submit_adoption_application`
- **HTTP Methods:** GET, POST
- **Template:** `application.html`
- **Context Variables:**
  - `pet` (dict)
- **POST Form Fields:**
  - `applicant_name` (str)
  - `applicant_phone` (str)
  - `housing_type` (str)
  - `reason` (str)

### 7. My Applications
- **Path:** `/my-applications`
- **Function:** `my_applications`
- **HTTP Methods:** GET
- **Template:** `my_applications.html`
- **Context Variables:**
  - `applications` (list of dict)
  - `filter_status` (str)

### 8. Favorites
- **Path:** `/favorites`
- **Function:** `favorites`
- **HTTP Methods:** GET
- **Template:** `favorites.html`
- **Context Variables:**
  - `favorites` (list of dict)

### 9. Messages
- **Path:** `/messages`
- **Function:** `messages`
- **HTTP Methods:** GET, POST
- **Template:** `messages.html`
- **Context Variables:**
  - `conversations` (list of dict)
- **POST Form Fields:**
  - `message_input` (str)
  - `recipient_username` (str)
  - `subject` (str)

### 10. User Profile
- **Path:** `/profile`
- **Function:** `profile`
- **HTTP Methods:** GET, POST
- **Template:** `profile.html`
- **Context Variables:**
  - `user` (dict)
- **POST Form Fields:**
  - `email` (str)

### 11. Admin Panel
- **Path:** `/admin`
- **Function:** `admin_panel`
- **HTTP Methods:** GET
- **Template:** `admin_panel.html`
- **Context Variables:**
  - `pending_applications` (list of dict)
  - `all_pets` (list of dict)

---

## Section 2: HTML Template Specifications (Frontend Focus)

### Template: `dashboard.html`
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Pet Adoption Dashboard`
- **H1:** `Dashboard`
- **Element IDs:**
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button) [navigates to `url_for('pets_listing')`]
  - `back-to-dashboard` (button) [refreshes dashboard]
- **Context Variables:** `featured_pets`, `recent_activities`

### Template: `pets.html`
- **File Path:** `templates/pets.html`
- **Page Title:** `Available Pets`
- **H1:** `Available Pets`
- **Element IDs:**
  - `pet-listings-page` (div)
  - `search-input` (input text)
  - `filter-species` (dropdown with options: All, Dog, Cat, Bird, Rabbit, Other)
  - `pet-grid` (div) showing pet cards
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `pets`, `filter_species`, `search_text`

### Template: `pet_details.html`
- **File Path:** `templates/pet_details.html`
- **Page Title:** `Pet Details`
- **H1:** `{{ pet.name }}`
- **Element IDs:**
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button) [navigates to `url_for('submit_adoption_application', pet_id=pet.pet_id)`]
  - `back-to-listings` (button) [navigates to `url_for('pets_listing')`]
- **Context Variables:** `pet`

### Template: `add_pet.html`
- **File Path:** `templates/add_pet.html`
- **Page Title:** `Add New Pet`
- **H1:** `Add New Pet`
- **Element IDs:**
  - `add-pet-page` (div)
  - `pet-name-input` (input text)
  - `pet-species-input` (dropdown)
  - `pet-breed-input` (input text)
  - `pet-age-input` (input text)
  - `pet-gender-input` (dropdown)
  - `pet-size-input` (dropdown)
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** None

### Template: `application.html`
- **File Path:** `templates/application.html`
- **Page Title:** `Adoption Application`
- **H1:** `Adoption Application`
- **Element IDs:**
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (dropdown)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button) [navigates to `url_for('pet_details', pet_id=pet.pet_id)`]
- **Context Variables:** `pet`

### Template: `my_applications.html`
- **File Path:** `templates/my_applications.html`
- **Page Title:** `My Applications`
- **H1:** `My Applications`
- **Element IDs:**
  - `my-applications-page` (div)
  - `filter-status` (dropdown with options: All, Pending, Approved, Rejected)
  - `applications-table` (table)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `applications`, `filter_status`

### Template: `favorites.html`
- **File Path:** `templates/favorites.html`
- **Page Title:** `My Favorites`
- **H1:** `Favorites`
- **Element IDs:**
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `favorites`

### Template: `messages.html`
- **File Path:** `templates/messages.html`
- **Page Title:** `Messages`
- **H1:** `Messages`
- **Element IDs:**
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `conversations`

### Template: `profile.html`
- **File Path:** `templates/profile.html`
- **Page Title:** `My Profile`
- **H1:** `My Profile`
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `user`

### Template: `admin_panel.html`
- **File Path:** `templates/admin_panel.html`
- **Page Title:** `Admin Panel`
- **H1:** `Admin Panel`
- **Element IDs:**
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button) [navigates to `url_for('dashboard')`]
- **Context Variables:** `pending_applications`, `all_pets`

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- **File Path:** `data/users.txt`
- **Fields:**
  `username|email|phone|address`
- **Field Descriptions:**
  - `username` (str): Unique user identifier
  - `email` (str): Email address
  - `phone` (str): Phone number
  - `address` (str): Mailing address
- **Example Rows:**
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- **File Path:** `data/pets.txt`
- **Fields:**
  `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- **Field Descriptions:**
  - `pet_id` (int): Unique pet ID
  - `name` (str): Pet name
  - `species` (str): Species (Dog, Cat, Bird, Rabbit, Other)
  - `breed` (str): Breed
  - `age` (str): Age with unit (e.g., "3 years")
  - `gender` (str): Male or Female
  - `size` (str): Small, Medium, or Large
  - `description` (str): Detailed description
  - `shelter_id` (int): Shelter identifier
  - `status` (str): Availability status (Available, Pending, Adopted)
  - `date_added` (str): Date added (YYYY-MM-DD)
- **Example Rows:**
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- **File Path:** `data/applications.txt`
- **Fields:**
  `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- **Field Descriptions:**
  - `application_id` (int): Unique application ID
  - `username` (str): Applicant's username
  - `pet_id` (int): Target pet ID
  - `applicant_name` (str): Applicant's full name
  - `phone` (str): Contact phone
  - `address` (str): Applicant's address
  - `housing_type` (str): Housing type
  - `has_yard` (str): "Yes" or "No"
  - `other_pets` (str): Description of other pets
  - `experience` (str): Pet experience
  - `reason` (str): Reason for applying
  - `status` (str): Application status (Pending, Approved, Rejected)
  - `date_submitted` (str): Date submitted (YYYY-MM-DD)
- **Example Rows:**
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- **File Path:** `data/favorites.txt`
- **Fields:**
  `username|pet_id|date_added`
- **Field Descriptions:**
  - `username` (str): User's username
  - `pet_id` (int): Pet favorited
  - `date_added` (str): Date when favorited
- **Example Rows:**
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- **File Path:** `data/messages.txt`
- **Fields:**
  `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- **Field Descriptions:**
  - `message_id` (int): Unique message ID
  - `sender_username` (str): Sender username
  - `recipient_username` (str): Recipient username
  - `subject` (str): Message subject
  - `content` (str): Message body
  - `timestamp` (str): Date and time (YYYY-MM-DD HH:MM:SS)
  - `is_read` (bool): true/false
- **Example Rows:**
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- **File Path:** `data/adoption_history.txt`
- **Fields:**
  `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- **Field Descriptions:**
  - `history_id` (int): Unique ID
  - `username` (str): Adopter username
  - `pet_id` (int): Pet ID
  - `pet_name` (str): Pet name
  - `adoption_date` (str): Date adopted
  - `shelter_id` (int): Shelter ID
- **Example Rows:**
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- **File Path:** `data/shelters.txt`
- **Fields:**
  `shelter_id|name|address|phone|email`
- **Field Descriptions:**
  - `shelter_id` (int): Unique shelter ID
  - `name` (str): Shelter name
  - `address` (str): Shelter address
  - `phone` (str): Contact phone
  - `email` (str): Contact email
- **Example Rows:**
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

End of Design Specification.

This document defines comprehensive backend routes, frontend templates, and data schemas to allow fully independent development of the PetAdoptionCenter application.
