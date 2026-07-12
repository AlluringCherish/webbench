# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                | Function Name          | HTTP Method(s) | Template File Rendered        | Context Variables (name:type)                                                                                                                    |
|---------------------------|------------------------|----------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| /                         | root_redirect          | GET            | Redirect to /dashboard        | None                                                                                                                                            |
| /dashboard                | dashboard              | GET            | dashboard.html                | featured_pets: list of dict {pet_id:int, name:str, species:str, age:str, photo_url:str (optional)} , recent_activities: list of str (if used)    |
| /pets                     | pet_listings           | GET            | pet_listings.html             | pets: list of dict {pet_id:int, name:str, species:str, age:str, photo_url:str (optional)} , filter_species: str (current filter)                 |
| /pets/<int:pet_id>        | pet_details            | GET            | pet_details.html              | pet: dict {pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str, description:str, shelter_id:int, status:str, date_added:str} |
| /pets/add                 | add_pet                | GET, POST      | add_pet.html                  | (GET) no variables; (POST) on submission redirects or returns errors                                                                            |
| /applications/<int:pet_id>/apply | adoption_application | GET, POST      | adoption_application.html     | pet: dict {pet_id:int, name:str}, application_errors: dict[str,str] (if POST errors)                                                             |
| /my_applications           | my_applications        | GET            | my_applications.html          | applications: list of dict {application_id:int, pet_name:str, date_submitted:str, status:str} , filter_status: str                                |
| /favorites                | favorites              | GET            | favorites.html                | favorites: list of dict {pet_id:int, name:str, species:str, age:str, photo_url:str (optional)}                                                    |
| /messages                 | messages               | GET, POST      | messages.html                 | conversations: list of dict {conversation_id:int, other_user:str, last_message:str, unread_count:int} , messages: list of dict {sender:str, recipient:str, subject:str, content:str, timestamp:str} |
| /profile                  | user_profile           | GET, POST      | profile.html                  | user: dict {username:str, email:str} , profile_update_errors: dict[str,str] (if POST errors)                                                      |
| /admin                   | admin_panel            | GET            | admin_panel.html              | pending_applications: list of dict {application_id:int, applicant_name:str, pet_name:str, date_submitted:str, status:str} , all_pets: list of dict {pet_id:int, name:str, status:str} |

### Additional Route Details:
- The root route `/` redirects (HTTP 302) to `/dashboard`.
- The `/pets/add` route handles GET to show form and POST to submit new pet. The POST receives fields for: name, species, breed, age, gender, size, description.
- The `/applications/<int:pet_id>/apply` route handles GET to show the form and POST to receive application data: applicant_name(str), phone(str), housing_type(str), reason(str), etc.
- For forms submission routes (`/pets/add`, `/applications/<int:pet_id>/apply`, `/profile`), POST method must be used with CSRF protection (assumed).
- Context variables for templates are typed precisely.

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- **File Path:** `templates/dashboard.html`
- **Page Title:** Pet Adoption Dashboard
- **<title> Tag:** Pet Adoption Dashboard
- **<h1> Tag:** Pet Adoption Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `featured-pets` (div)
  - `browse-pets-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `browse-pets-button`: Link to `url_for('pet_listings')`
  - `back-to-dashboard`: Reloads `/dashboard` or link to `url_for('dashboard')`
- **Context Variables:**
  - `featured_pets`: list of dicts with keys: pet_id(int), name(str), species(str), age(str), photo_url(str optional, if image shown)
  - `recent_activities`: list of str (optional, if displayed)

### 2. Pet Listings Page
- **File Path:** `templates/pet_listings.html`
- **Page Title:** Available Pets
- **<title> Tag:** Available Pets
- **<h1> Tag:** Available Pets
- **Element IDs:**
  - `pet-listings-page` (div)
  - `search-input` (input)
  - `filter-species` (select/dropdown)
  - `pet-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
  - Pet cards inside `pet-grid`:
    - Each pet card includes at least a clickable element linking to `url_for('pet_details', pet_id=pet.pet_id)` (dynamic via Jinja2)
- **Context Variables:**
  - `pets`: list of dict {pet_id:int, name:str, species:str, age:str, photo_url:str (optional)}
  - `filter_species`: str (current species filter)

### 3. Pet Details Page
- **File Path:** `templates/pet_details.html`
- **Page Title:** Pet Details
- **<title> Tag:** Pet Details
- **<h1> Tag:** (Text is the pet's name rendered dynamically)
- **Element IDs:**
  - `pet-details-page` (div)
  - `pet-name` (h1) - Pet name displayed
  - `pet-species` (div)
  - `pet-description` (div)
  - `adopt-button` (button)
  - `back-to-listings` (button)
- **Navigation:**
  - `adopt-button`: Link to `url_for('adoption_application', pet_id=pet.pet_id)`
  - `back-to-listings`: Link to `url_for('pet_listings')`
- **Context Variables:**
  - `pet`: dict with keys: pet_id(int), name(str), species(str), breed(str), age(str), gender(str), size(str), description(str), shelter_id(int), status(str), date_added(str)

### 4. Add Pet Page
- **File Path:** `templates/add_pet.html`
- **Page Title:** Add New Pet
- **<title> Tag:** Add New Pet
- **<h1> Tag:** Add New Pet
- **Element IDs:**
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
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - None for GET. For POST error display, use a context variable `form_errors`: dict[str,str] (optional)

### 5. Adoption Application Page
- **File Path:** `templates/adoption_application.html`
- **Page Title:** Adoption Application
- **<title> Tag:** Adoption Application
- **<h1> Tag:** Adoption Application
- **Element IDs:**
  - `application-page` (div)
  - `applicant-name` (input)
  - `applicant-phone` (input)
  - `housing-type` (select/dropdown)
  - `reason` (textarea)
  - `submit-application-button` (button)
  - `back-to-pet` (button)
- **Navigation:**
  - `back-to-pet`: Link to `url_for('pet_details', pet_id=pet.pet_id)`
- **Context Variables:**
  - `pet`: dict {pet_id:int, name:str}
  - `application_errors`: dict[str,str] (optional, form validation errors)

### 6. My Applications Page
- **File Path:** `templates/my_applications.html`
- **Page Title:** My Applications
- **<title> Tag:** My Applications
- **<h1> Tag:** My Applications
- **Element IDs:**
  - `my-applications-page` (div)
  - `filter-status` (select/dropdown)
  - `applications-table` (table)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - `applications`: list of dict {application_id:int, pet_name:str, date_submitted:str, status:str}
  - `filter_status`: str (current filter)

### 7. Favorites Page
- **File Path:** `templates/favorites.html`
- **Page Title:** My Favorites
- **<title> Tag:** My Favorites
- **<h1> Tag:** My Favorites
- **Element IDs:**
  - `favorites-page` (div)
  - `favorites-grid` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - `favorites`: list of dict {pet_id:int, name:str, species:str, age:str, photo_url:str (optional)}

### 8. Messages Page
- **File Path:** `templates/messages.html`
- **Page Title:** Messages
- **<title> Tag:** Messages
- **<h1> Tag:** Messages
- **Element IDs:**
  - `messages-page` (div)
  - `conversation-list` (div)
  - `message-input` (textarea)
  - `send-message-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - `conversations`: list of dict {conversation_id:int, other_user:str, last_message:str, unread_count:int}
  - `messages`: list of dict {sender_username:str, recipient_username:str, subject:str, content:str, timestamp:str, is_read:bool}

### 9. User Profile Page
- **File Path:** `templates/profile.html`
- **Page Title:** My Profile
- **<title> Tag:** My Profile
- **<h1> Tag:** My Profile
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - `user`: dict {username:str, email:str}
  - `profile_update_errors`: dict[str,str] (optional)

### 10. Admin Panel Page
- **File Path:** `templates/admin_panel.html`
- **Page Title:** Admin Panel
- **<title> Tag:** Admin Panel
- **<h1> Tag:** Admin Panel
- **Element IDs:**
  - `admin-panel-page` (div)
  - `pending-applications` (div)
  - `all-pets-list` (div)
  - `back-to-dashboard` (button)
- **Navigation:**
  - `back-to-dashboard`: Link to `url_for('dashboard')`
- **Context Variables:**
  - `pending_applications`: list of dict {application_id:int, applicant_name:str, pet_name:str, date_submitted:str, status:str}
  - `all_pets`: list of dict {pet_id:int, name:str, status:str}

---

## Section 3: Data File Schemas (Backend Focus)

### 1. Users Data
- Filename: `data/users.txt`
- Fields (pipe-delimited):
  - username (str) - unique user identifier
  - email (str) - user email address
  - phone (str) - contact phone number
  - address (str) - mailing address
- Example:
```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. Pets Data
- Filename: `data/pets.txt`
- Fields (pipe-delimited):
  - pet_id (int) - unique pet identifier
  - name (str)
  - species (str) - Dog, Cat, Bird, Rabbit, Other
  - breed (str)
  - age (str) - e.g., "3 years"
  - gender (str) - Male or Female
  - size (str) - Small, Medium, Large
  - description (str) - detailed description
  - shelter_id (int) - associated shelter
  - status (str) - Available, Pending, Adopted, etc.
  - date_added (str) - YYYY-MM-DD
- Example:
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. Adoption Applications Data
- Filename: `data/applications.txt`
- Fields (pipe-delimited):
  - application_id (int) - unique application identifier
  - username (str) - applicant username
  - pet_id (int)
  - applicant_name (str)
  - phone (str)
  - address (str)
  - housing_type (str) - House, Apartment, Condo, Other
  - has_yard (str) - Yes or No
  - other_pets (str) - description
  - experience (str) - years or description
  - reason (str) - reason for adoption
  - status (str) - Pending, Approved, Rejected
  - date_submitted (str) - YYYY-MM-DD
- Example:
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. Favorites Data
- Filename: `data/favorites.txt`
- Fields (pipe-delimited):
  - username (str)
  - pet_id (int)
  - date_added (str) - YYYY-MM-DD
- Example:
```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. Messages Data
- Filename: `data/messages.txt`
- Fields (pipe-delimited):
  - message_id (int) - unique message identifier
  - sender_username (str)
  - recipient_username (str)
  - subject (str)
  - content (str)
  - timestamp (str) - YYYY-MM-DD HH:MM:SS
  - is_read (str) - "true" or "false" (to be converted to bool)
- Example:
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. Adoption History Data
- Filename: `data/adoption_history.txt`
- Fields (pipe-delimited):
  - history_id (int) - unique history identifier
  - username (str)
  - pet_id (int)
  - pet_name (str)
  - adoption_date (str) - YYYY-MM-DD
  - shelter_id (int)
- Example:
```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. Shelters Data
- Filename: `data/shelters.txt`
- Fields (pipe-delimited):
  - shelter_id (int) - unique shelter identifier
  - name (str)
  - address (str)
  - phone (str)
  - email (str)
- Example:
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```

---

This specification enables independent yet complete development of:
- Backend Flask routes and data handling from Sections 1 and 3
- Frontend HTML templates from Section 2

No assumptions needed beyond this document.
