# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path               | Function Name          | HTTP Methods    | Template Rendered         | Context Variables (Name : Type)                                           |
|--------------------------|------------------------|-----------------|---------------------------|---------------------------------------------------------------------------|
| `/`                      | root_redirect          | GET             | Redirect to `/dashboard`  | None                                                                      |
| `/dashboard`             | dashboard_page         | GET             | dashboard.html            | `featured_pets : list[dict]` (Each dict: pet_id:int, name:str, species:str, age:str, photo_url:str) |
| `/pets`                  | pet_listings_page      | GET             | pet_listings.html         | `pets : list[dict]` (Each dict: pet_id:int, name:str, species:str, age:str, photo_url:str)        |
| `/pets/search`           | pet_search             | POST            | Redirect to `/pets` with query params | `search_term : str`, `filter_species : str`                               |
| `/pets/<int:pet_id>`     | pet_details_page       | GET             | pet_details.html          | `pet : dict` (keys: pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str, description:str, shelter_id:int, status:str, date_added:str) |
| `/pets/add`              | add_pet_page           | GET             | add_pet.html              | None                                                                      |
| `/pets/add`              | submit_new_pet         | POST            | Redirect to `/pets`       | Form data (see HTML elements)                                            |
| `/adoption/apply/<int:pet_id>` | adoption_application_page | GET             | adoption_application.html | `pet : dict` (same structure as pet_details_page)                        |
| `/adoption/apply/<int:pet_id>` | submit_adoption_application | POST            | Redirect to `/my_applications` | Form data (applicant_name:str, phone:str, housing_type:str, reason:str)  |
| `/my_applications`       | my_applications_page   | GET             | my_applications.html      | `applications : list[dict]` (Each dict: application_id:int, pet_name:str, date_submitted:str, status:str) |
| `/my_applications/filter`| filter_applications    | POST            | Redirect to `/my_applications` | `filter_status : str`                                                    |
| `/favorites`             | favorites_page         | GET             | favorites.html            | `favorite_pets : list[dict]` (Each dict: pet_id:int, name:str, species:str, age:str, photo_url:str) |
| `/messages`              | messages_page          | GET             | messages.html             | `conversations : list[dict]` (Each dict: conversation_id:int, recipient_username:str, last_message:str, last_timestamp:str, unread_count:int) |
| `/messages/send/<recipient_username>` | send_message          | POST            | Redirect to `/messages`   | `message_content : str`                                                   |
| `/profile`               | user_profile_page      | GET             | profile.html              | `username : str`, `email : str`                                         |
| `/profile/update`        | update_profile         | POST            | Redirect to `/profile`    | `email : str`                                                             |
| `/admin`                 | admin_panel_page       | GET             | admin_panel.html          | `pending_applications : list[dict]` (application details), `all_pets : list[dict]` (pet details) |

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- Template filepath: `templates/dashboard.html`
- Page title: Pet Adoption Dashboard
- IDs and Element Types:
  - dashboard-page (Div)
  - featured-pets (Div)
  - browse-pets-button (Button)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - browse-pets-button: `{{ url_for('pet_listings_page') }}`
  - back-to-dashboard: reload current page (JavaScript or navigates to `{{ url_for('dashboard_page') }}`)
- Context variables:
  - featured_pets: list of dict with keys `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)

### 2. Pet Listings Page
- Template filepath: `templates/pet_listings.html`
- Page title: Available Pets
- IDs and Element Types:
  - pet-listings-page (Div)
  - search-input (Input)
  - filter-species (Dropdown)
  - pet-grid (Div)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
  - Each pet card in pet-grid links to: `{{ url_for('pet_details_page', pet_id=pet['pet_id']) }}`
- Context variables:
  - pets: list of dict with keys `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)

### 3. Pet Details Page
- Template filepath: `templates/pet_details.html`
- Page title: Pet Details
- IDs and Element Types:
  - pet-details-page (Div)
  - pet-name (H1)
  - pet-species (Div)
  - pet-description (Div)
  - adopt-button (Button)
  - back-to-listings (Button)
- Navigation URL mappings:
  - adopt-button: `{{ url_for('adoption_application_page', pet_id=pet['pet_id']) }}`
  - back-to-listings: `{{ url_for('pet_listings_page') }}`
- Context variables:
  - pet: dict with keys `pet_id` (int), `name` (str), `species` (str), `breed` (str), `age` (str), `gender` (str), `size` (str), `description` (str), `shelter_id` (int), `status` (str), `date_added` (str)

### 4. Add Pet Page
- Template filepath: `templates/add_pet.html`
- Page title: Add New Pet
- IDs and Element Types:
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
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables: None

### 5. Adoption Application Page
- Template filepath: `templates/adoption_application.html`
- Page title: Adoption Application
- IDs and Element Types:
  - application-page (Div)
  - applicant-name (Input)
  - applicant-phone (Input)
  - housing-type (Dropdown)
  - reason (Textarea)
  - submit-application-button (Button)
  - back-to-pet (Button)
- Navigation URL mappings:
  - back-to-pet: `{{ url_for('pet_details_page', pet_id=pet['pet_id']) }}`
- Context variables:
  - pet: dict (same structure as pet_details_page)

### 6. My Applications Page
- Template filepath: `templates/my_applications.html`
- Page title: My Applications
- IDs and Element Types:
  - my-applications-page (Div)
  - filter-status (Dropdown)
  - applications-table (Table)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables:
  - applications: list of dict with keys `application_id` (int), `pet_name` (str), `date_submitted` (str), `status` (str)

### 7. Favorites Page
- Template filepath: `templates/favorites.html`
- Page title: My Favorites
- IDs and Element Types:
  - favorites-page (Div)
  - favorites-grid (Div)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables:
  - favorite_pets: list of dict with keys `pet_id` (int), `name` (str), `species` (str), `age` (str), `photo_url` (str)

### 8. Messages Page
- Template filepath: `templates/messages.html`
- Page title: Messages
- IDs and Element Types:
  - messages-page (Div)
  - conversation-list (Div)
  - message-input (Textarea)
  - send-message-button (Button)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables:
  - conversations: list of dict with keys `conversation_id` (int), `recipient_username` (str), `last_message` (str), `last_timestamp` (str), `unread_count` (int)

### 9. User Profile Page
- Template filepath: `templates/profile.html`
- Page title: My Profile
- IDs and Element Types:
  - profile-page (Div)
  - profile-username (Div)
  - profile-email (Input)
  - update-profile-button (Button)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables:
  - username: str
  - email: str

### 10. Admin Panel Page
- Template filepath: `templates/admin_panel.html`
- Page title: Admin Panel
- IDs and Element Types:
  - admin-panel-page (Div)
  - pending-applications (Div)
  - all-pets-list (Div)
  - back-to-dashboard (Button)
- Navigation URL mappings:
  - back-to-dashboard: `{{ url_for('dashboard_page') }}`
- Context variables:
  - pending_applications: list of dict (application details including relevant fields)
  - all_pets: list of dict (pet details including relevant fields)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: `data/users.txt`
- Fields (pipe | delimited):
  `username|email|phone|address`
- Field descriptions:
  - username: Unique user identifier (str)
  - email: User email address (str)
  - phone: Contact phone number (str)
  - address: User's physical address (str)
- Example rows:
  - `john_doe|john@example.com|555-1234|123 Main St, City`
  - `admin_user|admin@shelter.com|555-0000|456 Shelter Ave`
  - `jane_smith|jane@example.com|555-5678|789 Oak Rd, Town`

### 2. pets.txt
- Filename: `data/pets.txt`
- Fields (pipe | delimited):
  `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Field descriptions:
  - pet_id: Unique identifier (int)
  - name: Pet name (str)
  - species: Species type (str)
  - breed: Pet breed (str)
  - age: Age description (str)
  - gender: Gender (str)
  - size: Size category (str)
  - description: Detailed description (str)
  - shelter_id: Shelter unique id (int)
  - status: Adoption status (Available, Pending, etc.) (str)
  - date_added: Date added to system (YYYY-MM-DD) (str)
- Example rows:
  - `1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15`
  - `2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20`
  - `3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01`

### 3. applications.txt
- Filename: `data/applications.txt`
- Fields (pipe | delimited):
  `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Field descriptions:
  - application_id: Unique identifier (int)
  - username: User's username (str)
  - pet_id: ID of pet applying for (int)
  - applicant_name: Applicant full name (str)
  - phone: Contact phone (str)
  - address: Applicant address (str)
  - housing_type: Type of housing (House, Apartment, Condo, Other) (str)
  - has_yard: If has yard (Yes/No) (str)
  - other_pets: Description of other pets (str)
  - experience: Pet experience description (str)
  - reason: Reason for adoption (str)
  - status: Application status (Pending, Approved, Rejected) (str)
  - date_submitted: Date application submitted (YYYY-MM-DD) (str)
- Example rows:
  - `1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10`
  - `2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05`

### 4. favorites.txt
- Filename: `data/favorites.txt`
- Fields (pipe | delimited):
  `username|pet_id|date_added`
- Field descriptions:
  - username: User's username (str)
  - pet_id: Pet ID (int)
  - date_added: Date added to favorites (YYYY-MM-DD) (str)
- Example rows:
  - `john_doe|1|2024-11-01`
  - `john_doe|3|2024-11-05`
  - `jane_smith|2|2024-10-25`

### 5. messages.txt
- Filename: `data/messages.txt`
- Fields (pipe | delimited):
  `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Field descriptions:
  - message_id: Unique message identifier (int)
  - sender_username: Username of sender (str)
  - recipient_username: Username of recipient (str)
  - subject: Message subject line (str)
  - content: Full message content (str)
  - timestamp: Date and time sent (YYYY-MM-DD HH:MM:SS) (str)
  - is_read: Read status (true/false) (str)
- Example rows:
  - `1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true`
  - `2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false`

### 6. adoption_history.txt
- Filename: `data/adoption_history.txt`
- Fields (pipe | delimited):
  `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Field descriptions:
  - history_id: Unique history entry identifier (int)
  - username: User's username (str)
  - pet_id: Pet ID (int)
  - pet_name: Pet's name (str)
  - adoption_date: Date of adoption (YYYY-MM-DD) (str)
  - shelter_id: Shelter ID (int)
- Example rows:
  - `1|jane_smith|2|Whiskers|2024-11-15|1`

### 7. shelters.txt
- Filename: `data/shelters.txt`
- Fields (pipe | delimited):
  `shelter_id|name|address|phone|email`
- Field descriptions:
  - shelter_id: Unique shelter identifier (int)
  - name: Shelter name (str)
  - address: Shelter address (str)
  - phone: Shelter contact phone (str)
  - email: Shelter email (str)
- Example rows:
  - `1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com`
  - `2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org`
