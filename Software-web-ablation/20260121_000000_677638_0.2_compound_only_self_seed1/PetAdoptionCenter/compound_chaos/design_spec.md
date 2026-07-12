# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                | Function Name          | HTTP Method | Template File Rendered      | Context Variables (name: type)                                                                                         |
|---------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| `/`                       | `root_redirect`        | GET         | None (Redirect to /dashboard) | None                                                                                                                   |
| `/dashboard`              | `dashboard`            | GET         | `dashboard.html`             | featured_pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str))                  |
| `/pets`                   | `pet_listings`         | GET         | `pet_listings.html`          | pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str))                           |
| `/pets`                   | `pet_listings_filtered`| POST        | `pet_listings.html`          | pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str)) - filtered by search/filter|
| `/pets/<int:pet_id>`      | `pet_details`          | GET         | `pet_details.html`           | pet: dict (`pet_id`(int), `name`(str), `species`(str), `breed`(str), `age`(str), `gender`(str), `size`(str), `description`(str), `status`(str)) |
| `/pets/add`               | `add_pet`              | GET         | `add_pet.html`               | None                                                                                                                   |
| `/pets/add`               | `submit_pet`           | POST        | `add_pet.html`               | form errors: dict (str: str) or success message: str (status indications)                                              |
| `/applications/apply/<int:pet_id>` | `adoption_application` | GET         | `application.html`           | pet: dict (`pet_id`(int), `name`(str))                                                                                   |
| `/applications/apply/<int:pet_id>` | `submit_application`   | POST        | `application.html`           | form errors: dict (str: str) or success message: str                                                                    |
| `/applications`           | `my_applications`      | GET         | `my_applications.html`       | applications: list of dicts (`application_id`(int), `pet_name`(str), `date_submitted`(str), `status`(str))                 |
| `/favorites`              | `favorites`            | GET         | `favorites.html`             | favorite_pets: list of dicts (`pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str))                   |
| `/messages`               | `messages_page`        | GET         | `messages.html`              | conversations: list of dicts (`conversation_id`(int), `other_user`(str), `last_message`(str), `unread_count`(int))         |
| `/messages/send`           | `send_message`         | POST        | Redirect to `/messages`      | None                                                                                                                   |
| `/profile`                | `profile`              | GET         | `profile.html`               | username: str, email: str                                                                                                |
| `/profile`                | `update_profile`       | POST        | `profile.html`               | form errors: dict (str: str) or success message: str                                                                    |
| `/admin`                  | `admin_panel`          | GET         | `admin_panel.html`           | pending_applications: list of dicts (`application_id`(int), `applicant_name`(str), `pet_name`(str), `date_submitted`(str)), all_pets: list of dicts (pet_id, name, species, status) |
| `/admin/applications/approve/<int:application_id>` | `approve_application` | POST        | Redirect to `/admin`         | None                                                                                                                   |
| `/admin/applications/reject/<int:application_id>`  | `reject_application`  | POST        | Redirect to `/admin`         | None                                                                                                                   |
| `/admin/pets/edit/<int:pet_id>`  | `edit_pet`           | GET         | `edit_pet.html` (not specified in requirements, optional) | pet: dict detailed info                                                                                                |
| `/admin/pets/delete/<int:pet_id>`| `delete_pet`         | POST        | Redirect to `/admin`         | None                                                                                                                   |

Notes:
- The root route `/` should perform an HTTP redirect (302) to `/dashboard`, no template rendering.
- Some POST routes (like `/pets` filter/search) can be done with GET + query params alternatively; for clarity filtering via POST included.
- Context variables types are carefully specified to aid frontend template usage.

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File Path: `templates/dashboard.html`
- Page Title: `Pet Adoption Dashboard`
- IDs and Element Types:
  - `dashboard-page`: div
  - `featured-pets`: div
  - `browse-pets-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `browse-pets-button` navigates to `url_for('pet_listings')`
  - `back-to-dashboard` triggers refresh of dashboard page (reload `/dashboard`)
- Context Variables:
  - `featured_pets`: list of dicts with fields: `pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str)

### 2. Pet Listings Page
- File Path: `templates/pet_listings.html`
- Page Title: `Available Pets`
- IDs and Element Types:
  - `pet-listings-page`: div
  - `search-input`: input
  - `filter-species`: select (dropdown)
  - `pet-grid`: div
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
  - Each pet card in `pet-grid` includes a link/button navigating to `url_for('pet_details', pet_id=pet['pet_id'])`
- Context Variables:
  - `pets`: list of dicts with `pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str)

### 3. Pet Details Page
- File Path: `templates/pet_details.html`
- Page Title: `Pet Details`
- IDs and Element Types:
  - `pet-details-page`: div
  - `pet-name`: h1
  - `pet-species`: div
  - `pet-description`: div
  - `adopt-button`: button
  - `back-to-listings`: button
- Navigation:
  - `back-to-listings` navigates to `url_for('pet_listings')`
  - `adopt-button` navigates to `url_for('adoption_application', pet_id=pet['pet_id'])`
- Context Variables:
  - `pet`: dict with `pet_id`(int), `name`(str), `species`(str), `breed`(str), `age`(str), `gender`(str), `size`(str), `description`(str), `status`(str)

### 4. Add Pet Page
- File Path: `templates/add_pet.html`
- Page Title: `Add New Pet`
- IDs and Element Types:
  - `add-pet-page`: div
  - `pet-name-input`: input
  - `pet-species-input`: select
  - `pet-breed-input`: input
  - `pet-age-input`: input
  - `pet-gender-input`: select
  - `pet-size-input`: select
  - `pet-description-input`: textarea
  - `submit-pet-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - May include form error messages (dict) or success messages (str) for feedback (optional)

### 5. Adoption Application Page
- File Path: `templates/application.html`
- Page Title: `Adoption Application`
- IDs and Element Types:
  - `application-page`: div
  - `applicant-name`: input
  - `applicant-phone`: input
  - `housing-type`: select
  - `reason`: textarea
  - `submit-application-button`: button
  - `back-to-pet`: button
- Navigation:
  - `back-to-pet` navigates to `url_for('pet_details', pet_id=pet['pet_id'])`
- Context Variables:
  - `pet`: dict with `pet_id`(int), `name`(str)
  - May include form error messages or success message (optional)

### 6. My Applications Page
- File Path: `templates/my_applications.html`
- Page Title: `My Applications`
- IDs and Element Types:
  - `my-applications-page`: div
  - `filter-status`: select
  - `applications-table`: table
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `applications`: list of dicts with `application_id`(int), `pet_name`(str), `date_submitted`(str), `status`(str)

### 7. Favorites Page
- File Path: `templates/favorites.html`
- Page Title: `My Favorites`
- IDs and Element Types:
  - `favorites-page`: div
  - `favorites-grid`: div
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `favorite_pets`: list of dicts with `pet_id`(int), `name`(str), `species`(str), `age`(str), `photo_url`(str)

### 8. Messages Page
- File Path: `templates/messages.html`
- Page Title: `Messages`
- IDs and Element Types:
  - `messages-page`: div
  - `conversation-list`: div
  - `message-input`: textarea
  - `send-message-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `conversations`: list of dicts with `conversation_id`(int), `other_user`(str), `last_message`(str), `unread_count`(int)

### 9. User Profile Page
- File Path: `templates/profile.html`
- Page Title: `My Profile`
- IDs and Element Types:
  - `profile-page`: div
  - `profile-username`: div
  - `profile-email`: input
  - `update-profile-button`: button
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `username`: str
  - `email`: str

### 10. Admin Panel Page
- File Path: `templates/admin_panel.html`
- Page Title: `Admin Panel`
- IDs and Element Types:
  - `admin-panel-page`: div
  - `pending-applications`: div
  - `all-pets-list`: div
  - `back-to-dashboard`: button
- Navigation:
  - `back-to-dashboard` navigates to `url_for('dashboard')`
- Context Variables:
  - `pending_applications`: list of dicts with `application_id`(int), `applicant_name`(str), `pet_name`(str), `date_submitted`(str)
  - `all_pets`: list of dicts with `pet_id`(int), `name`(str), `species`(str), `status`(str)

---

## Section 3: Data File Schemas (Backend Focus)

All data files are located in the `data` directory and use pipe-delimited (`|`) fields.

### 1. User Data
- Filename: `users.txt`
- Fields (pipe-delimited): `username|email|phone|address`
- Description:
  - `username`: unique user identifier (str)
  - `email`: user email address (str)
  - `phone`: contact phone number (str)
  - `address`: mailing address (str)
- Example:
  ```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. Pet Data
- Filename: `pets.txt`
- Fields (pipe-delimited):
  `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Description:
  - `pet_id`: unique integer ID
  - `name`: pet name (str)
  - `species`: e.g., Dog, Cat, Bird, Rabbit, Other (str)
  - `breed`: breed description (str)
  - `age`: age descriptor (str), e.g., "3 years"
  - `gender`: Male or Female (str)
  - `size`: Small, Medium, Large (str)
  - `description`: detailed text description (str)
  - `shelter_id`: ID of shelter (int)
  - `status`: Adoption status, e.g. Available, Pending (str)
  - `date_added`: YYYY-MM-DD format (str)
- Example:
  ```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. Adoption Applications Data
- Filename: `applications.txt`
- Fields (pipe-delimited):
  `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Description:
  - `application_id`: unique application integer ID
  - `username`: user who submitted (str)
  - `pet_id`: integer pet ID (int)
  - `applicant_name`: applicant full name (str)
  - `phone`: contact phone number (str)
  - `address`: postal address (str)
  - `housing_type`: House, Apartment, Condo, Other (str)
  - `has_yard`: Yes or No (str)
  - `other_pets`: description of other pets, e.g. "One cat" (str)
  - `experience`: experience description (str)
  - `reason`: reason for adoption (str)
  - `status`: Pending, Approved, Rejected (str)
  - `date_submitted`: submission date YYYY-MM-DD (str)
- Example:
  ```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. Favorites Data
- Filename: `favorites.txt`
- Fields (pipe-delimited): `username|pet_id|date_added`
- Description:
  - `username`: user who favorited (str)
  - `pet_id`: integer pet ID (int)
  - `date_added`: date added YYYY-MM-DD (str)
- Example:
  ```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. Messages Data
- Filename: `messages.txt`
- Fields (pipe-delimited):
  `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Description:
  - `message_id`: unique integer ID
  - `sender_username`: sender user (str)
  - `recipient_username`: recipient user (str)
  - `subject`: message subject (str)
  - `content`: message body (str)
  - `timestamp`: date and time as `YYYY-MM-DD HH:MM:SS` (str)
  - `is_read`: boolean represented as string "true" or "false" (str)
- Example:
  ```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. Adoption History Data
- Filename: `adoption_history.txt`
- Fields (pipe-delimited): `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Description:
  - `history_id`: unique integer ID
  - `username`: user who adopted (str)
  - `pet_id`: integer pet ID (int)
  - `pet_name`: pet name at time of adoption (str)
  - `adoption_date`: date adopted YYYY-MM-DD (str)
  - `shelter_id`: will link to shelter info (int)
- Example:
  ```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. Shelters Data
- Filename: `shelters.txt`
- Fields (pipe-delimited): `shelter_id|name|address|phone|email`
- Description:
  - `shelter_id`: unique integer ID
  - `name`: shelter name (str)
  - `address`: shelter address (str)
  - `phone`: contact phone number (str)
  - `email`: contact email (str)
- Example:
  ```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```

---

This completes the comprehensive design specification for the PetAdoptionCenter application ensuring backend and frontend teams can work independently and align precisely on implementation details.