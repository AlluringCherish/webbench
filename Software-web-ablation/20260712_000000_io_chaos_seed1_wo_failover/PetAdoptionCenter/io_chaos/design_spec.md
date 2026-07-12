# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path              | Function Name           | HTTP Method | Template Rendered           | Context Variables Passed (name: type)                                           |
|-------------------------|------------------------|-------------|-----------------------------|---------------------------------------------------------------------------------|
| `/`                     | root_redirect           | GET         | Redirect to `/dashboard`    | None                                                                            |
| `/dashboard`            | dashboard_page         | GET         | `dashboard.html`             | featured_pets: list[dict] (Each dict with keys: pet_id: int, name: str, species: str, age: str, photo_url: str)
|                         |                        |             |                             | recent_activities: list[str]                                                    |
| `/pets`                 | pet_listings_page      | GET         | `pet_listings.html`          | pets: list[dict] (Each dict with: pet_id: int, name: str, species: str, age: str, photo_url: str)
|                         |                        |             |                             | filter_species: str (One of: "All", "Dog", "Cat", "Bird", "Rabbit", "Other")
| `/pets/search`           | pet_search             | POST        | Redirect to `/pets` with filtered pets or returns filtered pets in context |
| `/pets/<int:pet_id>`    | pet_details_page       | GET         | `pet_details.html`           | pet: dict with keys: pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, status: str, date_added: str  |
| `/pets/add`             | add_pet_page           | GET         | `add_pet.html`               | None                                                                            |
| `/pets/add`             | submit_new_pet         | POST        | Redirect to `/pets` or render `add_pet.html` with errors                        | form_data fields from form submission:
- pet_name: str
- pet_species: str (Dog, Cat, Bird, Rabbit, Other)
- pet_breed: str
- pet_age: str
- pet_gender: str (Male, Female)
- pet_size: str (Small, Medium, Large)
- pet_description: str                                                      |
| `/adoption/apply/<int:pet_id>` | adoption_application_page | GET         | `adoption_application.html` | pet_id: int, pet_name: str                                                        |
| `/adoption/apply/<int:pet_id>` | submit_adoption_application | POST        | Redirect to `/my_applications` or render `adoption_application.html` with errors | Form fields:
- applicant_name: str
- applicant_phone: str
- housing_type: str (House, Apartment, Condo, Other)
- reason: str                                                                    |
| `/my_applications`      | my_applications_page   | GET         | `my_applications.html`       | applications: list[dict] (Each dict with keys: application_id: int, pet_name: str, date_submitted: str, status: str)                    |
| `/favorites`            | favorites_page         | GET         | `favorites.html`             | favorites: list[dict] (Each dict with keys: pet_id: int, name: str, species: str, age: str)                                              |
| `/messages`             | messages_page          | GET         | `messages.html`              | conversations: list[dict] (Each with keys: message_id:int, sender_username:str, recipient_username:str, subject:str, content:str, timestamp:str, is_read: bool) |
| `/messages/send`        | send_message           | POST        | Redirect to `/messages`      | Form fields:
- recipient_username: str
- subject: str
- content: str                                                             |
| `/profile`              | user_profile_page      | GET         | `profile.html`               | username: str
email: str                                                         |
| `/profile/update`       | update_profile         | POST        | Redirect to `/profile` or render `profile.html` with errors                    | Form fields:
- email: str                                                                   |
| `/admin`                | admin_panel_page       | GET         | `admin_panel.html`           | pending_applications: list[dict] (keys: application_id:int, pet_name:str, applicant_name:str, date_submitted:str, status:str)
all_pets: list[dict] (keys: pet_id:int, name:str, species:str, status:str) |
| `/admin/applications/approve/<int:application_id>` | approve_application | POST        | Redirect to `/admin` or render errors                                         | None                                                                            |
| `/admin/applications/reject/<int:application_id>` | reject_application | POST        | Redirect to `/admin` or render errors                                         | None                                                                            |

Note: Forms are submitted via POST. Navigation buttons use GET routes unless otherwise specified.

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File: `templates/dashboard.html`
- Page Title: "Pet Adoption Dashboard"
- <h1> Tag: "Pet Adoption Dashboard"
- Element IDs and Types:
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `browse-pets-button`: link to `url_for('pet_listings_page')`
  - `back-to-dashboard`: refresh dashboard, link to `url_for('dashboard_page')`
- Context Variables:
  - `featured_pets`: list of dicts with pet data (pet_id, name, species, age, photo_url)
  - `recent_activities`: list of strings

### 2. Pet Listings Page
- File: `templates/pet_listings.html`
- Page Title: "Available Pets"
- <h1> Tag: "Available Pets"
- Element IDs and Types:
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (select/dropdown)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
  - Each pet card in `pet-grid` has a link button to `url_for('pet_details_page', pet_id=pet.pet_id)` using Jinja2 syntax
- Context Variables:
  - `pets`: list of dicts with keys (pet_id, name, species, age, photo_url)
  - `filter_species`: current selected species filter as str

### 3. Pet Details Page
- File: `templates/pet_details.html`
- Page Title: "Pet Details"
- <h1> Tag: Bound to `pet.name` (dynamic)
- Element IDs and Types:
  - `pet-details-page` (div)
  - `pet-name` (h1)
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- Navigation:
  - `back-to-listings`: link to `url_for('pet_listings_page')`
  - `adopt-button`: link to `url_for('adoption_application_page', pet_id=pet.pet_id)`
- Context Variables:
  - `pet`: dict with keys matching pet attributes

### 4. Add Pet Page
- File: `templates/add_pet.html`
- Page Title: "Add New Pet"
- <h1> Tag: "Add New Pet"
- Element IDs and Types:
  - `add-pet-page` (div)
  - `pet-name-input` (input)
  - `pet-species-input` (select/dropdown)
  - `pet-breed-input` (input)
  - `pet-age-input` (input)
  - `pet-gender-input` (select/dropdown)
  - `pet-size-input` (select/dropdown)
  - `pet-description-input` (textarea)
  - `submit-pet-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables: None

### 5. Adoption Application Page
- File: `templates/adoption_application.html`
- Page Title: "Adoption Application"
- <h1> Tag: "Adoption Application"
- Element IDs and Types:
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (select/dropdown)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- Navigation:
  - `back-to-pet`: link to `url_for('pet_details_page', pet_id=pet_id)`
- Context Variables:
  - `pet_id`: int
  - `pet_name`: str

### 6. My Applications Page
- File: `templates/my_applications.html`
- Page Title: "My Applications"
- <h1> Tag: "My Applications"
- Element IDs and Types:
  - `my-applications-page` (div)
  - `filter-status` (select/dropdown)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables:
  - `applications`: list of dicts with keys (application_id, pet_name, date_submitted, status)

### 7. Favorites Page
- File: `templates/favorites.html`
- Page Title: "My Favorites"
- <h1> Tag: "My Favorites"
- Element IDs and Types:
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables:
  - `favorites`: list of dicts with keys (pet_id, name, species, age)

### 8. Messages Page
- File: `templates/messages.html`
- Page Title: "Messages"
- <h1> Tag: "Messages"
- Element IDs and Types:
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables:
  - `conversations`: list of dicts with keys (message_id, sender_username, recipient_username, subject, content, timestamp, is_read)

### 9. User Profile Page
- File: `templates/profile.html`
- Page Title: "My Profile"
- <h1> Tag: "My Profile"
- Element IDs and Types:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables:
  - `username`: str
  - `email`: str

### 10. Admin Panel Page
- File: `templates/admin_panel.html`
- Page Title: "Admin Panel"
- <h1> Tag: "Admin Panel"
- Element IDs and Types:
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- Navigation:
  - `back-to-dashboard`: link to `url_for('dashboard_page')`
- Context Variables:
  - `pending_applications`: list of dicts (keys: application_id, pet_name, applicant_name, date_submitted, status)
  - `all_pets`: list of dicts (keys: pet_id, name, species, status)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. `users.txt`
- Fields: `username|email|phone|address`
- Description:
  - `username`: User's unique identifier (str)
  - `email`: User email address (str)
  - `phone`: Contact phone number (str)
  - `address`: User's physical address (str)
- Example:
  ```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. `pets.txt`
- Fields: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Description:
  - `pet_id`: Unique integer ID for pet
  - `name`: Pet name (str)
  - `species`: Species name (Dog, Cat, Bird, Rabbit, Other)
  - `breed`: Breed of pet (str)
  - `age`: Age description (str, e.g. "2 years")
  - `gender`: Gender (Male or Female)
  - `size`: Size category (Small, Medium, Large)
  - `description`: Detailed description (str)
  - `shelter_id`: Shelter identifier (int)
  - `status`: Status (Available, Pending, Adopted, etc.)
  - `date_added`: Date added (YYYY-MM-DD format string)
- Example:
  ```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. `applications.txt`
- Fields: `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Description:
  - `application_id`: Unique integer ID for application
  - `username`: User who submitted application (str)
  - `pet_id`: Pet being applied for (int)
  - `applicant_name`: Name of applicant (str)
  - `phone`: Contact phone (str)
  - `address`: Applicant's address (str)
  - `housing_type`: Housing type (House, Apartment, Condo, Other)
  - `has_yard`: Yes or No (str)
  - `other_pets`: Description of other pets (str)
  - `experience`: Experience with pets (str)
  - `reason`: Reason for adoption (str)
  - `status`: Status of application (Pending, Approved, Rejected)
  - `date_submitted`: Date application was submitted (YYYY-MM-DD string)
- Example:
  ```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. `favorites.txt`
- Fields: `username|pet_id|date_added`
- Description:
  - `username`: User who favorited pet (str)
  - `pet_id`: Pet ID (int)
  - `date_added`: Date pet was added to favorites (YYYY-MM-DD string)
- Example:
  ```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. `messages.txt`
- Fields: `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Description:
  - `message_id`: Unique integer ID for message
  - `sender_username`: Sender's username (str)
  - `recipient_username`: Recipient's username (str)
  - `subject`: Message subject (str)
  - `content`: Message body content (str)
  - `timestamp`: Date and time sent (YYYY-MM-DD HH:MM:SS string)
  - `is_read`: Boolean flag (true/false)
- Example:
  ```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. `adoption_history.txt`
- Fields: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Description:
  - `history_id`: Unique integer ID for history record
  - `username`: User who adopted pet (str)
  - `pet_id`: Pet ID (int)
  - `pet_name`: Pet name (str)
  - `adoption_date`: Date of adoption (YYYY-MM-DD string)
  - `shelter_id`: Shelter ID (int)
- Example:
  ```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. `shelters.txt`
- Fields: `shelter_id|name|address|phone|email`
- Description:
  - `shelter_id`: Unique integer ID for shelter
  - `name`: Shelter name (str)
  - `address`: Shelter address (str)
  - `phone`: Contact phone number (str)
  - `email`: Contact email (str)
- Example:
  ```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```

---

This design specification provides all detailed backend route information, exact frontend template requirements, and definitive data file schemas to guarantee independent and parallel development for both backend and frontend teams of the PetAdoptionCenter application.
