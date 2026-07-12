# PetAdoptionCenter Design Specifications

---

## Section 1: Flask Routes Specification (Backend Focus)

### Route: `/`
- **Function Name:** root_redirect
- **HTTP Method:** GET
- **Description:** Redirects to the dashboard page.
- **Template:** N/A (redirect only)
- **Context Variables:** None

---

### Route: `/dashboard`
- **Function Name:** dashboard
- **HTTP Method:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_pets` (list of dict): List of up to 5 pet objects with keys:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `age` (str)
    - `photo_url` (str, optional)
  - `recent_activities` (list of str) - Optional (if recent activities shown)

---

### Route: `/pets`
- **Function Name:** pet_listings
- **HTTP Method:** GET
- **Template:** `pet_listings.html`
- **Context Variables:**
  - `pets` (list of dict): List of all available pets with keys:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `breed` (str)
    - `age` (str)
    - `gender` (str)
    - `size` (str)
    - `description` (str)
    - `status` (str)
  - `filter_species` (str) - currently applied species filter value
  - `search_query` (str) - current search input value

---

### Route: `/pets/<int:pet_id>`
- **Function Name:** pet_details
- **HTTP Method:** GET
- **Template:** `pet_details.html`
- **Context Variables:**
  - `pet` (dict): Detailed pet object with keys:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `breed` (str)
    - `age` (str)
    - `gender` (str)
    - `size` (str)
    - `description` (str)
    - `status` (str)
    - `shelter_id` (int)

---

### Route: `/pets/add`
- **Function Name:** add_pet
- **HTTP Method:** GET
- **Template:** `add_pet.html`
- **Context Variables:** None

---

### Route: `/pets/add` (form submission)
- **Function Name:** submit_new_pet
- **HTTP Method:** POST
- **Template:** Redirects to `/dashboard` after submission
- **Context Variables:** N/A

- **Form Fields:**
  - `pet_name` (str)
  - `pet_species` (str)
  - `pet_breed` (str)
  - `pet_age` (str)
  - `pet_gender` (str)
  - `pet_size` (str)
  - `pet_description` (str)

---

### Route: `/applications/new/<int:pet_id>`
- **Function Name:** adoption_application_page
- **HTTP Method:** GET
- **Template:** `adoption_application.html`
- **Context Variables:**
  - `pet_id` (int)
  - `pet_name` (str)

---

### Route: `/applications/new/<int:pet_id>` (form submission)
- **Function Name:** submit_adoption_application
- **HTTP Method:** POST
- **Template:** Redirect to `/pets/<pet_id>` after submission
- **Context Variables:** N/A

- **Form Fields:**
  - `applicant_name` (str)
  - `applicant_phone` (str)
  - `housing_type` (str)
  - `reason` (str)

---

### Route: `/applications`
- **Function Name:** my_applications
- **HTTP Method:** GET
- **Template:** `my_applications.html`
- **Context Variables:**
  - `applications` (list of dict): Each dict with keys:
    - `application_id` (int)
    - `pet_name` (str)
    - `date` (str, e.g., YYYY-MM-DD)
    - `status` (str)
  - `filter_status` (str) - currently applied status filter

---

### Route: `/favorites`
- **Function Name:** favorites
- **HTTP Method:** GET
- **Template:** `favorites.html`
- **Context Variables:**
  - `favorite_pets` (list of dict): List of favorite pets with keys:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `age` (str)

---

### Route: `/messages`
- **Function Name:** messages
- **HTTP Method:** GET
- **Template:** `messages.html`
- **Context Variables:**
  - `conversations` (list of dict): Each dict with keys:
    - `conversation_id` (int)
    - `with_user` (str) - username
    - `last_message` (str)
    - `unread_count` (int)

---

### Route: `/messages/send` (form submission)
- **Function Name:** send_message
- **HTTP Method:** POST
- **Template:** Redirect to `/messages`
- **Context Variables:** N/A

- **Form Fields:**
  - `recipient_username` (str)
  - `subject` (str)
  - `content` (str)

---

### Route: `/profile`
- **Function Name:** user_profile
- **HTTP Method:** GET
- **Template:** `profile.html`
- **Context Variables:**
  - `username` (str)
  - `email` (str)

---

### Route: `/profile/update` (form submission)
- **Function Name:** update_profile
- **HTTP Method:** POST
- **Template:** Redirect to `/profile`
- **Context Variables:** N/A

- **Form Fields:**
  - `email` (str)

---

### Route: `/admin`
- **Function Name:** admin_panel
- **HTTP Method:** GET
- **Template:** `admin_panel.html`
- **Context Variables:**
  - `pending_applications` (list of dict): each dict with:
    - `application_id` (int)
    - `pet_name` (str)
    - `applicant_name` (str)
    - `date_submitted` (str)
  - `all_pets` (list of dict): each dict with:
    - `pet_id` (int)
    - `name` (str)
    - `species` (str)
    - `status` (str)

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. `templates/dashboard.html`
- **Page Title:** Pet Adoption Dashboard
- **Main Header (<h1>):** Pet Adoption Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `browse-pets-button` → `url_for('pet_listings')`
  - `back-to-dashboard` → reload current dashboard page (`url_for('dashboard')`)
- **Context Variables:**
  - `featured_pets` (list of dict)

---

### 2. `templates/pet_listings.html`
- **Page Title:** Available Pets
- **Main Header (<h1>):** Available Pets
- **Element IDs:**
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (select dropdown)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
  - Each pet card within `pet-grid` should link pet name or card to `url_for('pet_details', pet_id=pet.pet_id)`
- **Context Variables:**
  - `pets` (list of dict)
  - `filter_species` (str)
  - `search_query` (str)

---

### 3. `templates/pet_details.html`
- **Page Title:** Pet Details
- **Main Header (<h1>):** Bound to `pet.name` (dynamic)
- **Element IDs:**
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- **Navigation:**
  - `back-to-listings` → `url_for('pet_listings')`
  - `adopt-button` → `url_for('adoption_application_page', pet_id=pet.pet_id)`
- **Context Variables:**
  - `pet` (dict)

---

### 4. `templates/add_pet.html`
- **Page Title:** Add New Pet
- **Main Header (<h1>):** Add New Pet
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
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:** None

---

### 5. `templates/adoption_application.html`
- **Page Title:** Adoption Application
- **Main Header (<h1>):** Adoption Application
- **Element IDs:**
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (select dropdown)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- **Navigation:**
  - `back-to-pet` → `url_for('pet_details', pet_id=pet_id)`
- **Context Variables:**
  - `pet_id` (int)
  - `pet_name` (str)

---

### 6. `templates/my_applications.html`
- **Page Title:** My Applications
- **Main Header (<h1>):** My Applications
- **Element IDs:**
  - `my-applications-page` (div)
  - `filter-status` (select dropdown)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:**
  - `applications` (list of dict)
  - `filter_status` (str)

---

### 7. `templates/favorites.html`
- **Page Title:** My Favorites
- **Main Header (<h1>):** My Favorites
- **Element IDs:**
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:**
  - `favorite_pets` (list of dict)

---

### 8. `templates/messages.html`
- **Page Title:** Messages
- **Main Header (<h1>):** Messages
- **Element IDs:**
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:**
  - `conversations` (list of dict)

---

### 9. `templates/profile.html`
- **Page Title:** My Profile
- **Main Header (<h1>):** My Profile
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:**
  - `username` (str)
  - `email` (str)

---

### 10. `templates/admin_panel.html`
- **Page Title:** Admin Panel
- **Main Header (<h1>):** Admin Panel
- **Element IDs:**
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`
- **Context Variables:**
  - `pending_applications` (list of dict)
  - `all_pets` (list of dict)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. `users.txt`
- **Fields:** `username|email|phone|address`
- **Field Descriptions:**
  - `username` (str): Unique user identifier
  - `email` (str): User email address
  - `phone` (str): Contact phone number
  - `address` (str): User address
- **Example Data:**
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

---

### 2. `pets.txt`
- **Fields:** `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- **Field Descriptions:**
  - `pet_id` (int): Unique pet identifier
  - `name` (str): Pet name
  - `species` (str): Species (Dog, Cat, Bird, Rabbit, Other)
  - `breed` (str): Breed details
  - `age` (str): Age description (e.g., "3 years")
  - `gender` (str): Gender (Male, Female)
  - `size` (str): Size (Small, Medium, Large)
  - `description` (str): Detailed pet description
  - `shelter_id` (int): Shelter identifier
  - `status` (str): Availability status (Available, Pending, Adopted)
  - `date_added` (str): Date added (YYYY-MM-DD)
- **Example Data:**
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

---

### 3. `applications.txt`
- **Fields:** `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- **Field Descriptions:**
  - `application_id` (int): Unique application identifier
  - `username` (str): User who submitted application
  - `pet_id` (int): Pet applied for
  - `applicant_name` (str): Full name of applicant
  - `phone` (str): Contact phone
  - `address` (str): Applicant address
  - `housing_type` (str): Housing type (House, Apartment, Condo, Other)
  - `has_yard` (str): Yes/No if applicant has a yard
  - `other_pets` (str): Description of other pets
  - `experience` (str): Applicant's experience with pets
  - `reason` (str): Reason for adoption
  - `status` (str): Application status (Pending, Approved, Rejected)
  - `date_submitted` (str): Date submitted (YYYY-MM-DD)
- **Example Data:**
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

---

### 4. `favorites.txt`
- **Fields:** `username|pet_id|date_added`
- **Field Descriptions:**
  - `username` (str): User identifier
  - `pet_id` (int): Favorite pet identifier
  - `date_added` (str): Date pet was favorited (YYYY-MM-DD)
- **Example Data:**
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

---

### 5. `messages.txt`
- **Fields:** `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- **Field Descriptions:**
  - `message_id` (int): Unique message ID
  - `sender_username` (str): Sender username
  - `recipient_username` (str): Recipient username
  - `subject` (str): Message subject
  - `content` (str): Message body content
  - `timestamp` (str): DateTime of message (YYYY-MM-DD HH:MM:SS)
  - `is_read` (str): "true"/"false" - read status
- **Example Data:**
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

---

### 6. `adoption_history.txt`
- **Fields:** `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- **Field Descriptions:**
  - `history_id` (int): Unique history record ID
  - `username` (str): User who adopted
  - `pet_id` (int): Adopted pet ID
  - `pet_name` (str): Name of adopted pet
  - `adoption_date` (str): Date of adoption (YYYY-MM-DD)
  - `shelter_id` (int): Shelter ID
- **Example Data:**
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

---

### 7. `shelters.txt`
- **Fields:** `shelter_id|name|address|phone|email`
- **Field Descriptions:**
  - `shelter_id` (int): Unique shelter ID
  - `name` (str): Shelter name
  - `address` (str): Shelter address
  - `phone` (str): Contact phone
  - `email` (str): Contact email
- **Example Data:**
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

# End of Specification
