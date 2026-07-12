# Design Specification for PetAdoptionCenter Web Application

---

## Section 1: Flask Routes Specification (Backend Focus)

### General Notes
- The root route `/` redirects to the Dashboard page at `/dashboard`.
- Form submissions use POST methods.
- All context variables are explicitly typed.

---

### Route List

1. **Route:** `/`
   - Function Name: `root_redirect`
   - HTTP Method: GET
   - Behavior: Redirects to `/dashboard`
   - Template: None
   - Context Variables: None

2. **Route:** `/dashboard`
   - Function Name: `dashboard`
   - HTTP Method: GET
   - Template: `dashboard.html`
   - Context Variables:
     - `featured_pets` (list of dict): Each dict contains keys: `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str or None)
     - `recent_activities` (list of str) - (Optional enhancement - per overview, can be empty list)

3. **Route:** `/pets`
   - Function Name: `pet_listings`
   - HTTP Method: GET
   - Template: `pet_listings.html`
   - Context Variables:
     - `pets` (list of dict): Each dict includes keys: `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str or None)
     - `filter_species` (str): Current species filter value (default "All")
     - `search_query` (str): Current search string (default empty)

4. **Route:** `/pets/<int:pet_id>`
   - Function Name: `pet_details`
   - HTTP Method: GET
   - Template: `pet_details.html`
   - Context Variables:
     - `pet` (dict): Fields: `pet_id` (int), `name` (str), `species` (str), `breed` (str), `age` (str), `gender` (str), `size` (str), `description` (str), `status` (str)

5. **Route:** `/pets/add`
   - Function Name: `add_pet`
   - HTTP Methods: GET, POST
   - Template: `add_pet.html`
   - GET Context Variables: None
   - POST Behavior: Process form submission to add new pet
     - Expected form fields (via request.form): `pet_name` (str), `pet_species` (str), `pet_breed` (str), `pet_age` (str), `pet_gender` (str), `pet_size` (str), `pet_description` (str)
     - On success, redirect to `/dashboard`

6. **Route:** `/application/<int:pet_id>`
   - Function Name: `adoption_application`
   - HTTP Methods: GET, POST
   - Template: `adoption_application.html`
   - GET Context Variables:
     - `pet` (dict): as in pet_details
   - POST Behavior: Process form submission for adoption application
     - Expected form fields: `applicant_name` (str), `applicant_phone` (str), `housing_type` (str), `reason` (str)
     - On success, redirect to `/my_applications`

7. **Route:** `/my_applications`
   - Function Name: `my_applications`
   - HTTP Method: GET
   - Template: `my_applications.html`
   - Context Variables:
     - `applications` (list of dict): Each dict fields: `application_id` (int), `pet_name` (str), `date` (str, e.g., "YYYY-MM-DD"), `status` (str)
     - `filter_status` (str): Current status filter (default "All")

8. **Route:** `/favorites`
   - Function Name: `favorites`
   - HTTP Method: GET
   - Template: `favorites.html`
   - Context Variables:
     - `favorite_pets` (list of dict): Each dict fields: `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str or None)

9. **Route:** `/messages`
   - Function Name: `messages`
   - HTTP Methods: GET, POST
   - Template: `messages.html`
   - GET Context Variables:
     - `conversations` (list of dict): Each dict includes keys: `recipient_username` (str), `last_message` (str), `last_timestamp` (str), `unread_count` (int)
   - POST Behavior: Process sending a new message
     - Expected form fields: `recipient_username` (str), `subject` (str), `content` (str)
     - On success, refresh messages page

10. **Route:** `/profile`
    - Function Name: `profile`
    - HTTP Methods: GET, POST
    - Template: `profile.html`
    - GET Context Variables:
      - `username` (str)
      - `email` (str)
    - POST Behavior: Update profile email
      - Expected form field: `email` (str)
      - On success, refresh profile page

11. **Route:** `/admin`
    - Function Name: `admin_panel`
    - HTTP Method: GET
    - Template: `admin_panel.html`
    - Context Variables:
      - `pending_applications` (list of dict): Each dict includes `application_id` (int), `applicant_name` (str), `pet_name` (str), `date_submitted` (str)
      - `all_pets` (list of dict): Each dict includes `pet_id` (int), `name` (str), `species` (str), `status` (str)

12. **Route:** `/admin/pets/<int:pet_id>/edit`
    - Function Name: `edit_pet`
    - HTTP Methods: GET, POST
    - Template: `edit_pet.html`
    - GET Context Variables:
      - `pet` (dict): Full pet detail same as in `pet_details`
    - POST Behavior:
      - Accept form fields to update pet info
      - On success, redirect back to `/admin`

13. **Route:** `/admin/pets/<int:pet_id>/delete`
    - Function Name: `delete_pet`
    - HTTP Method: POST
    - Template: None (redirect only)
    - Behavior: Delete pet record then redirect to `/admin`

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File Path: `templates/dashboard.html`
- Page Title (for `<title>` and `<h1>`): `Pet Adoption Dashboard`
- Element IDs:
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `browse-pets-button` navigates to `url_for('pet_listings')`
  - `back-to-dashboard` refreshes current page
- Context Variables:
  - `featured_pets` (list of dict with `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str or None))
  - `recent_activities` (list of str)

### 2. Pet Listings Page
- File Path: `templates/pet_listings.html`
- Page Title: `Available Pets`
- Element IDs:
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (dropdown/select)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
  - Each pet in `pet-grid` links to `url_for('pet_details', pet_id=pet.pet_id)`
- Context Variables:
  - `pets` (list of dict as above)
  - `filter_species` (str)
  - `search_query` (str)

### 3. Pet Details Page
- File Path: `templates/pet_details.html`
- Page Title: `Pet Details`
- Element IDs:
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- Navigation:
  - `adopt-button` navigates to `url_for('adoption_application', pet_id=pet.pet_id)`
  - `back-to-listings` navigates to `url_for('pet_listings')`
- Context Variables:
  - `pet` (dict as above)

### 4. Add Pet Page
- File Path: `templates/add_pet.html`
- Page Title: `Add New Pet`
- Element IDs:
  - `add-pet-page` (div)
  - `pet-name-input` (input)
  - `pet-species-input` (dropdown/select)
  - `pet-breed-input` (input)
  - `pet-age-input` (input)
  - `pet-gender-input` (dropdown/select)
  - `pet-size-input` (dropdown/select)
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables: None (form page)

### 5. Adoption Application Page
- File Path: `templates/adoption_application.html`
- Page Title: `Adoption Application`
- Element IDs:
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (dropdown/select)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- Navigation:
  - `back-to-pet` navigates to `url_for('pet_details', pet_id=pet.pet_id)`
- Context Variables:
  - `pet` (dict as above)

### 6. My Applications Page
- File Path: `templates/my_applications.html`
- Page Title: `My Applications`
- Element IDs:
  - `my-applications-page` (div)
  - `filter-status` (dropdown/select)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `applications` (list of dict: `application_id` (int), `pet_name` (str), `date` (str), `status` (str))
  - `filter_status` (str)

### 7. Favorites Page
- File Path: `templates/favorites.html`
- Page Title: `My Favorites`
- Element IDs:
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `favorite_pets` (list of dict as above)

### 8. Messages Page
- File Path: `templates/messages.html`
- Page Title: `Messages`
- Element IDs:
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `conversations` (list of dict: `recipient_username` (str), `last_message` (str), `last_timestamp` (str), `unread_count` (int))

### 9. User Profile Page
- File Path: `templates/profile.html`
- Page Title: `My Profile`
- Element IDs:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `username` (str)
  - `email` (str)

### 10. Admin Panel Page
- File Path: `templates/admin_panel.html`
- Page Title: `Admin Panel`
- Element IDs:
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `pending_applications` (list of dict with `application_id` (int), `applicant_name` (str), `pet_name` (str), `date_submitted` (str))
  - `all_pets` (list of dict with `pet_id` (int), `name` (str), `species` (str), `status` (str))

### 11. Edit Pet Page (Admin)
- File Path: `templates/edit_pet.html`
- Page Title: `Edit Pet`
- Element IDs:
  - `edit-pet-page` (div)
  - Same input fields as Add Pet page with their IDs matching Add Pet page
  - Additional `submit-edit-button` (button) for submitting edits
  - `back-to-admin` (button) to return to admin panel
- Navigation:
  - `back-to-admin` navigates to `url_for('admin_panel')`
- Context Variables:
  - `pet` (dict as in pet_details)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: `data/users.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `username|email|phone|address`
- Field Descriptions:
  - `username` (str): Unique user identifier
  - `email` (str): User’s email address
  - `phone` (str): Phone number
  - `address` (str): Physical address
- Example Rows:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- Filename: `data/pets.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Field Descriptions:
  - `pet_id` (int): Unique pet identifier
  - `name` (str): Pet’s name
  - `species` (str): Species (Dog, Cat, Bird, Rabbit, Other)
  - `breed` (str): Breed
  - `age` (str): Age description (e.g., "3 years")
  - `gender` (str): Gender (Male, Female)
  - `size` (str): Size (Small, Medium, Large)
  - `description` (str): Detailed description
  - `shelter_id` (int): Shelter identifier
  - `status` (str): Adoption status (Available, Pending, etc.)
  - `date_added` (str): Date added (YYYY-MM-DD)
- Example Rows:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- Filename: `data/applications.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Field Descriptions:
  - `application_id` (int): Unique application ID
  - `username` (str): User who submitted
  - `pet_id` (int): Pet applied for
  - `applicant_name` (str): Applicant full name
  - `phone` (str): Phone number
  - `address` (str): User address
  - `housing_type` (str): House, Apartment, Condo, Other
  - `has_yard` (str): Yes/No
  - `other_pets` (str): Text description
  - `experience` (str): Years of pet experience
  - `reason` (str): Reason for adoption
  - `status` (str): Pending, Approved, Rejected
  - `date_submitted` (str): Date submitted (YYYY-MM-DD)
- Example Rows:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- Filename: `data/favorites.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `username|pet_id|date_added`
- Field Descriptions:
  - `username` (str): User identifier
  - `pet_id` (int): Pet identifier
  - `date_added` (str): Date favorite added (YYYY-MM-DD)
- Example Rows:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- Filename: `data/messages.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Field Descriptions:
  - `message_id` (int): Unique message ID
  - `sender_username` (str): Sender
  - `recipient_username` (str): Recipient
  - `subject` (str): Message subject
  - `content` (str): Message body content
  - `timestamp` (str): Datetime (YYYY-MM-DD HH:MM:SS)
  - `is_read` (str - "true" or "false"): Read status
- Example Rows:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- Filename: `data/adoption_history.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Field Descriptions:
  - `history_id` (int): Unique history record ID
  - `username` (str): User who adopted
  - `pet_id` (int): Pet adopted
  - `pet_name` (str): Name of pet
  - `adoption_date` (str): Date of adoption (YYYY-MM-DD)
  - `shelter_id` (int): Shelter associated
- Example Rows:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- Filename: `data/shelters.txt`
- Delimiter: Pipe (`|`)
- Fields Order: `shelter_id|name|address|phone|email`
- Field Descriptions:
  - `shelter_id` (int): Unique shelter ID
  - `name` (str): Shelter name
  - `address` (str): Address
  - `phone` (str): Phone number
  - `email` (str): Email
- Example Rows:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This specification ensures that Backend developers can implement the Flask routes and data handling purely from Sections 1 and 3, and Frontend developers can build the HTML templates solely from Section 2.
All context variable names and element IDs are consistent between sections to support independent parallel development.

---