# PetAdoptionCenter Design Specification

---

## 1. Flask Routes Specification

| Route Path                  | Function Name            | HTTP Method | Template Rendered        | Context Variables (Name: Type)                                                                                                               |
|-----------------------------|--------------------------|-------------|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                         | root_redirect             | GET         | -                        | -                                                                                                                                             |
| `/dashboard`                | dashboard_page            | GET         | dashboard.html           | featured_pets: List[Dict] (each Dict contains: pet_id: int, name: str, species: str, age: str), recent_activities: List[str]                     |
| `/pets`                    | pet_listings_page         | GET         | pet_listings.html        | pets: List[Dict] (each Dict contains: pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, status: str), filter_species: str, search_query: str |
| `/pets/<int:pet_id>`       | pet_details_page          | GET         | pet_details.html         | pet: Dict (pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, shelter_id: int, status: str, date_added: str)                            |
| `/pets/add`                | add_pet_page              | GET         | add_pet.html             | -                                                                                                                                             |
| `/pets/add`                | submit_new_pet            | POST        | -                        | Form data from add pet inputs                                                                                                                 |
| `/applications/adopt/<int:pet_id>` | adoption_application_page | GET         | adoption_application.html | pet: Dict (pet_id: int, name: str)                                                                                                                                                 |
| `/applications/adopt/<int:pet_id>` | submit_adoption_application | POST        | -                        | Form data from adoption application inputs                                                                                                  |
| `/applications`            | my_applications_page      | GET         | my_applications.html     | applications: List[Dict] (each Dict contains: application_id: int, pet_name: str, date_submitted: str, status: str), filter_status: str          |
| `/favorites`               | favorites_page            | GET         | favorites.html           | favorite_pets: List[Dict] (each Dict contains: pet_id: int, name: str, species: str, age: str)                                                  |
| `/messages`                | messages_page             | GET         | messages.html            | conversations: List[Dict] (each Dict contains: message_id: int, sender_username: str, recipient_username: str, subject: str, last_message: str, unread_count: int)                      |
| `/messages/send`           | send_message              | POST        | -                        | Form data from message input                                                                                                                  |
| `/profile`                 | user_profile_page         | GET         | profile.html             | username: str, email: str                                                                                                                     |
| `/profile`                 | update_profile            | POST        | -                        | Form data from profile email input                                                                                                           |
| `/admin`                   | admin_panel_page          | GET         | admin_panel.html         | pending_applications: List[Dict] (application_id: int, applicant_name: str, pet_name: str, date_submitted: str), all_pets: List[Dict] (pet_id: int, name: str)                          |
| `/admin/applications/<int:application_id>/approve` | approve_application       | POST        | -                        | application_id: int                                                                                                                           |
| `/admin/applications/<int:application_id>/reject`  | reject_application        | POST        | -                        | application_id: int                                                                                                                           |
| `/admin/pets/<int:pet_id>/edit` | edit_pet_page             | GET         | edit_pet.html            | pet: Dict (same fields as pet_details)                                                                                                      |
| `/admin/pets/<int:pet_id>/edit` | submit_pet_edit           | POST        | -                        | Form data from pet edit inputs                                                                                                               |
| `/admin/pets/<int:pet_id>/delete` | delete_pet                | POST        | -                        | pet_id: int                                                                                                                                   |


---

## 2. HTML Template Specifications

### templates/dashboard.html
- Page Title: Pet Adoption Dashboard
- H1 Title: Pet Adoption Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-pets (Div)
  - browse-pets-button (Button)
  - back-to-dashboard (Button)
- Navigation Details:
  - browse-pets-button: link/button to `url_for('pet_listings_page')`
  - back-to-dashboard: reload current page `url_for('dashboard_page')`
- Context Variables:
  - featured_pets: List of Dicts with keys: pet_id (int), name (str), species (str), age (str)
  - recent_activities: List of strings

---

### templates/pet_listings.html
- Page Title: Available Pets
- H1 Title: Available Pets
- Element IDs:
  - pet-listings-page (Div)
  - search-input (Input)
  - filter-species (Dropdown)
  - pet-grid (Div)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - pets: List of Dicts, each Dict with pet_id (int), name (str), species (str), breed (str), age (str), gender (str), size (str), description (str), status (str)
  - filter_species: str (selected species filter)
  - search_query: str (search input value)

---

### templates/pet_details.html
- Page Title: Pet Details
- H1 Title: {{ pet.name }} (Dynamic)
- Element IDs:
  - pet-details-page (Div)
  - pet-name (H1)
  - pet-species (Div)
  - pet-description (Div)
  - adopt-button (Button)
  - back-to-listings (Button)
- Navigation Details:
  - adopt-button: link/button to `url_for('adoption_application_page', pet_id=pet.pet_id)`
  - back-to-listings: link/button to `url_for('pet_listings_page')`
- Context Variables:
  - pet: Dict as detailed in Flask Routes section

---

### templates/add_pet.html
- Page Title: Add New Pet
- H1 Title: Add New Pet
- Element IDs:
  - add-pet-page (Div)
  - pet-name-input (Input)
  - pet-species-input (Dropdown)
  - pet-breed-input (Input)
  - pet-age-input (Input)
  - pet-gender-input (Dropdown)
  - pet-size-input (Dropdown)
  - pet-description-input (Textarea)
  - submit-pet-button (Button)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - None (form fields only)

---

### templates/adoption_application.html
- Page Title: Adoption Application
- H1 Title: Adoption Application for {{ pet.name }}
- Element IDs:
  - application-page (Div)
  - applicant-name (Input)
  - applicant-phone (Input)
  - housing-type (Dropdown)
  - reason (Textarea)
  - submit-application-button (Button)
  - back-to-pet (Button)
- Navigation Details:
  - back-to-pet: link/button to `url_for('pet_details_page', pet_id=pet.pet_id)`
- Context Variables:
  - pet: Dict with pet_id (int), name (str)

---

### templates/my_applications.html
- Page Title: My Applications
- H1 Title: My Applications
- Element IDs:
  - my-applications-page (Div)
  - filter-status (Dropdown)
  - applications-table (Table)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - applications: List of Dicts with application_id (int), pet_name (str), date_submitted (str), status (str)
  - filter_status: str

---

### templates/favorites.html
- Page Title: My Favorites
- H1 Title: My Favorites
- Element IDs:
  - favorites-page (Div)
  - favorites-grid (Div)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - favorite_pets: List of Dicts with pet_id (int), name (str), species (str), age (str)

---

### templates/messages.html
- Page Title: Messages
- H1 Title: Messages
- Element IDs:
  - messages-page (Div)
  - conversation-list (Div)
  - message-input (Textarea)
  - send-message-button (Button)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - conversations: List of Dicts containing message_id (int), sender_username (str), recipient_username (str), subject (str), last_message (str), unread_count (int)

---

### templates/profile.html
- Page Title: My Profile
- H1 Title: My Profile
- Element IDs:
  - profile-page (Div)
  - profile-username (Div)
  - profile-email (Input)
  - update-profile-button (Button)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - username: str
  - email: str

---

### templates/admin_panel.html
- Page Title: Admin Panel
- H1 Title: Admin Panel
- Element IDs:
  - admin-panel-page (Div)
  - pending-applications (Div)
  - all-pets-list (Div)
  - back-to-dashboard (Button)
- Navigation Details:
  - back-to-dashboard: link/button to `url_for('dashboard_page')`
- Context Variables:
  - pending_applications: List of Dicts with application_id (int), applicant_name (str), pet_name (str), date_submitted (str)
  - all_pets: List of Dicts with pet_id (int), name (str)

---

## 3. Data File Schemas

### data/users.txt
- Fields (pipe-delimited):
  - username (str): Unique user identifier
  - email (str): User email address
  - phone (str): User phone number
  - address (str): User postal address
- Example:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

---

### data/pets.txt
- Fields (pipe-delimited):
  - pet_id (int): Unique pet identifier
  - name (str): Pet name
  - species (str): Species of pet (Dog, Cat, etc.)
  - breed (str): Breed
  - age (str): Age description
  - gender (str): Gender (Male, Female)
  - size (str): Size category (Small, Medium, Large)
  - description (str): Detailed description
  - shelter_id (int): Shelter identifier where pet is located
  - status (str): Availability status (Available, Pending, etc.)
  - date_added (str): Date added in YYYY-MM-DD format
- Example:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

---

### data/applications.txt
- Fields (pipe-delimited):
  - application_id (int): Unique application identifier
  - username (str): Username of applicant
  - pet_id (int): ID of pet applied for
  - applicant_name (str): Full name of applicant
  - phone (str): Applicant phone number
  - address (str): Applicant postal address
  - housing_type (str): Housing type (House, Apartment, Condo, Other)
  - has_yard (str): 'Yes' or 'No' indicating yard availability
  - other_pets (str): Description of other pets
  - experience (str): Experience with pets
  - reason (str): Reason for adoption
  - status (str): Application status (Pending, Approved, Rejected)
  - date_submitted (str): Submission date YYYY-MM-DD
- Example:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

---

### data/favorites.txt
- Fields (pipe-delimited):
  - username (str): User who favorited pet
  - pet_id (int): Pet identifier
  - date_added (str): Date when added YYYY-MM-DD
- Example:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

---

### data/messages.txt
- Fields (pipe-delimited):
  - message_id (int): Unique message identifier
  - sender_username (str): Sender username
  - recipient_username (str): Recipient username
  - subject (str): Message subject
  - content (str): Message content
  - timestamp (str): Date and time in YYYY-MM-DD HH:MM:SS
  - is_read (str): 'true' or 'false' string indicating read status
- Example:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

---

### data/adoption_history.txt
- Fields (pipe-delimited):
  - history_id (int): Unique history record identifier
  - username (str): Username who adopted
  - pet_id (int): Adopted pet ID
  - pet_name (str): Name of adopted pet
  - adoption_date (str): Adoption date YYYY-MM-DD
  - shelter_id (int): Shelter ID from which pet was adopted
- Example:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

---

### data/shelters.txt
- Fields (pipe-delimited):
  - shelter_id (int): Shelter identifier
  - name (str): Shelter name
  - address (str): Shelter postal address
  - phone (str): Shelter phone number
  - email (str): Shelter contact email
- Example:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

*End of Design Specification.*
