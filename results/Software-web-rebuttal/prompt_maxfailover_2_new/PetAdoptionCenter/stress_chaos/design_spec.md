# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend-Focused)

### Route: `/`
- Function Name: `root_redirect`
- HTTP Method: GET
- Action: Redirects to `/dashboard`

### Route: `/dashboard`
- Function Name: `dashboard`
- HTTP Method: GET
- Template Rendered: `dashboard.html`
- Context Variables:
  - `featured_pets` (list of dict): List of max 5 featured pet dictionaries with keys: `pet_id` (int), `name` (str), `species` (str), `age` (str)

### Route: `/pets`
- Function Name: `pet_listings`
- HTTP Method: GET
- Template Rendered: `pet_listings.html`
- Context Variables:
  - `pets` (list of dict): List of all available pet dictionaries with keys: `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str, optional if images supported)
  - `selected_species` (str): Currently selected species filter ("All", "Dog", "Cat", "Bird", "Rabbit", "Other")
  - `search_query` (str): Current search query for pet names

### Route: `/pets/<int:pet_id>`
- Function Name: `pet_details`
- HTTP Method: GET
- Template Rendered: `pet_details.html`
- Context Variables:
  - `pet` (dict): Dictionary containing detailed pet info with keys: `pet_id` (int), `name` (str), `species` (str), `breed` (str), `age` (str), `gender` (str), `size` (str), `description` (str), `status` (str), `date_added` (str)

### Route: `/pets/add` (GET)
- Function Name: `add_pet_form`
- HTTP Method: GET
- Template Rendered: `add_pet.html`
- Context Variables: None

### Route: `/pets/add` (POST)
- Function Name: `submit_new_pet`
- HTTP Method: POST
- Template Rendered: Redirects to `/dashboard` on success
- Context Variables: None
- Description: Handles form submission for adding new pet

### Route: `/applications/adopt/<int:pet_id>` (GET)
- Function Name: `adoption_application_form`
- HTTP Method: GET
- Template Rendered: `adoption_application.html`
- Context Variables:
  - `pet_id` (int): ID of the pet for adoption
  - `pet_name` (str): Name of the pet

### Route: `/applications/adopt/<int:pet_id>` (POST)
- Function Name: `submit_adoption_application`
- HTTP Method: POST
- Template Rendered: Redirects to `/pets/<pet_id>` on success
- Context Variables: None
- Description: Handles adoption application submission form

### Route: `/applications/my` (GET)
- Function Name: `my_applications`
- HTTP Method: GET
- Template Rendered: `my_applications.html`
- Context Variables:
  - `applications` (list of dict): List of application dictionaries with keys: `application_id` (int), `pet_name` (str), `date_submitted` (str), `status` (str)
  - `selected_status` (str): Selected filter status ("All", "Pending", "Approved", "Rejected")

### Route: `/favorites` (GET)
- Function Name: `favorites`
- HTTP Method: GET
- Template Rendered: `favorites.html`
- Context Variables:
  - `favorite_pets` (list of dict): List of favorite pet dictionaries with keys: `pet_id` (int), `name` (str), `species` (str), `age` (str)

### Route: `/messages` (GET)
- Function Name: `messages`
- HTTP Method: GET
- Template Rendered: `messages.html`
- Context Variables:
  - `conversations` (list of dict): List of message conversation dictionaries with keys: `message_id` (int), `sender_username` (str), `recipient_username` (str), `subject` (str), `content` (str), `timestamp` (str), `is_read` (bool)

### Route: `/messages/send` (POST)
- Function Name: `send_message`
- HTTP Method: POST
- Template Rendered: Redirects to `/messages` on success
- Context Variables: None
- Description: Handles sending a message to a shelter or user

### Route: `/profile` (GET)
- Function Name: `profile`
- HTTP Method: GET
- Template Rendered: `profile.html`
- Context Variables:
  - `username` (str): Username of current user
  - `email` (str): Email of current user

### Route: `/profile/update` (POST)
- Function Name: `update_profile`
- HTTP Method: POST
- Template Rendered: Redirects to `/profile` on success
- Context Variables: None
- Description: Handles updating user profile info

### Route: `/admin` (GET)
- Function Name: `admin_panel`
- HTTP Method: GET
- Template Rendered: `admin_panel.html`
- Context Variables:
  - `pending_applications` (list of dict): List of adoption applications with status 'Pending', with keys: `application_id` (int), `applicant_name` (str), `pet_name` (str), `date_submitted` (str)
  - `all_pets` (list of dict): List of all pets with keys: `pet_id` (int), `name` (str), `status` (str)

---

## Section 2: HTML Template Specifications (Frontend-Focused)

### Template: `dashboard.html`
- File Path: `templates/dashboard.html`
- Page Title (`<title>` and `<h1>`): "Pet Adoption Dashboard"
- Element IDs:
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `browse-pets-button`: `url_for('pet_listings')`
  - `back-to-dashboard`: reloads current `/dashboard`
- Context Variables:
  - `featured_pets` (list of dict): Each pet dict with `pet_id` (int), `name` (str), `species` (str), `age` (str)

### Template: `pet_listings.html`
- File Path: `templates/pet_listings.html`
- Page Title: "Available Pets"
- Element IDs:
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (dropdown/select)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
  - Clicking a pet card in `pet-grid`: `url_for('pet_details', pet_id=pet.pet_id)` using Jinja2 syntax
- Context Variables:
  - `pets` (list of dict): each dict with `pet_id` (int), `name` (str), `species` (str), `age` (str)
  - `selected_species` (str)
  - `search_query` (str)

### Template: `pet_details.html`
- File Path: `templates/pet_details.html`
- Page Title: "Pet Details"
- Element IDs:
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- Navigation:
  - `adopt-button`: `url_for('adoption_application_form', pet_id=pet.pet_id)`
  - `back-to-listings`: `url_for('pet_listings')`
- Context Variables:
  - `pet` (dict) with fields `pet_id` (int), `name` (str), `species` (str), `breed` (str), `age` (str), `gender` (str), `size` (str), `description` (str), `status` (str), `date_added` (str)

### Template: `add_pet.html`
- File Path: `templates/add_pet.html`
- Page Title: "Add New Pet"
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
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables: None

### Template: `adoption_application.html`
- File Path: `templates/adoption_application.html`
- Page Title: "Adoption Application"
- Element IDs:
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (dropdown/select)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- Navigation:
  - `back-to-pet`: `url_for('pet_details', pet_id=pet_id)` using Jinja2
- Context Variables:
  - `pet_id` (int)
  - `pet_name` (str)

### Template: `my_applications.html`
- File Path: `templates/my_applications.html`
- Page Title: "My Applications"
- Element IDs:
  - `my-applications-page` (div)
  - `filter-status` (dropdown/select)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `applications` (list of dict) with keys: `application_id` (int), `pet_name` (str), `date_submitted` (str), `status` (str)
  - `selected_status` (str)

### Template: `favorites.html`
- File Path: `templates/favorites.html`
- Page Title: "My Favorites"
- Element IDs:
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `favorite_pets` (list of dict) with keys: `pet_id` (int), `name` (str), `species` (str), `age` (str)

### Template: `messages.html`
- File Path: `templates/messages.html`
- Page Title: "Messages"
- Element IDs:
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `conversations` (list of dict) with keys: `message_id` (int), `sender_username` (str), `recipient_username` (str), `subject` (str), `content` (str), `timestamp` (str), `is_read` (bool)

### Template: `profile.html`
- File Path: `templates/profile.html`
- Page Title: "My Profile"
- Element IDs:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `username` (str)
  - `email` (str)

### Template: `admin_panel.html`
- File Path: `templates/admin_panel.html`
- Page Title: "Admin Panel"
- Element IDs:
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: `url_for('dashboard')`
- Context Variables:
  - `pending_applications` (list of dict) with keys: `application_id` (int), `applicant_name` (str), `pet_name` (str), `date_submitted` (str)
  - `all_pets` (list of dict) with keys: `pet_id` (int), `name` (str), `status` (str)

---

## Section 3: Data File Schemas (Backend-Focused)

All data files will be stored in the `data/` directory.

### 1. Users Data
- Filename: `users.txt`
- Field Order (pipe-delimited):
  - `username` (str): Unique user identifier
  - `email` (str): User's email address
  - `phone` (str): User's phone number
  - `address` (str): User's physical address
- Example Data:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pets Data
- Filename: `pets.txt`
- Field Order (pipe-delimited):
  - `pet_id` (int): Unique pet identifier
  - `name` (str): Pet name
  - `species` (str): Species of pet (Dog, Cat, Bird, Rabbit, Other)
  - `breed` (str): Breed of pet
  - `age` (str): Age, e.g., "3 years"
  - `gender` (str): Gender (Male, Female)
  - `size` (str): Size category (Small, Medium, Large)
  - `description` (str): Detailed description
  - `shelter_id` (int): Identifier of shelter
  - `status` (str): Adoption status (Available, Pending, Adopted)
  - `date_added` (str): Date pet was added (YYYY-MM-DD)
- Example Data:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- Filename: `applications.txt`
- Field Order (pipe-delimited):
  - `application_id` (int): Unique application identifier
  - `username` (str): Username of applicant
  - `pet_id` (int): ID of the pet applied for
  - `applicant_name` (str): Full name of applicant
  - `phone` (str): Applicant phone number
  - `address` (str): Applicant address
  - `housing_type` (str): Housing type (House, Apartment, Condo, Other)
  - `has_yard` (str): "Yes" or "No" indicating if yard is present
  - `other_pets` (str): Description of other pets in household
  - `experience` (str): Experience with pets
  - `reason` (str): Reason for adopting
  - `status` (str): Application status (Pending, Approved, Rejected)
  - `date_submitted` (str): Date application submitted (YYYY-MM-DD)
- Example Data:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- Filename: `favorites.txt`
- Field Order (pipe-delimited):
  - `username` (str): Username of user
  - `pet_id` (int): Pet ID favorited
  - `date_added` (str): Date pet was favorited (YYYY-MM-DD)
- Example Data:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- Filename: `messages.txt`
- Field Order (pipe-delimited):
  - `message_id` (int): Unique message identifier
  - `sender_username` (str): Username of sender
  - `recipient_username` (str): Username of recipient
  - `subject` (str): Subject of message
  - `content` (str): Message content
  - `timestamp` (str): Message timestamp (YYYY-MM-DD HH:MM:SS)
  - `is_read` (str): "true" or "false" indicating if message was read
- Example Data:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- Filename: `adoption_history.txt`
- Field Order (pipe-delimited):
  - `history_id` (int): Unique history record identifier
  - `username` (str): Username of adopter
  - `pet_id` (int): ID of adopted pet
  - `pet_name` (str): Name of pet
  - `adoption_date` (str): Date of adoption (YYYY-MM-DD)
  - `shelter_id` (int): ID of shelter
- Example Data:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- Filename: `shelters.txt`
- Field Order (pipe-delimited):
  - `shelter_id` (int): Unique shelter identifier
  - `name` (str): Shelter name
  - `address` (str): Shelter address
  - `phone` (str): Shelter phone number
  - `email` (str): Shelter email address
- Example Data:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

# End of Design Specification
