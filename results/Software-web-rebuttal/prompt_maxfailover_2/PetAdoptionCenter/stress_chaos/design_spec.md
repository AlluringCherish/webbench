# PetAdoptionCenter Flask Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path             | Function Name           | HTTP Method | Template Rendered            | Context Variables Passed (name: type)                        |
|------------------------|-------------------------|-------------|-----------------------------|--------------------------------------------------------------|
| /                      | root_redirect            | GET         | None (Redirects to /dashboard) | None                                                         |
| /dashboard             | dashboard                | GET         | dashboard.html              | featured_pets: list of dict {pet_id: int, name: str, species: str, age: str} 
|                        |                         |             |                             | recent_activities: list of dict {activity_id: int, description: str, date: str} (optional, if implemented) |
| /pets                  | pet_listings             | GET         | pet_listings.html           | pets: list of dict {pet_id: int, name: str, species: str, age: str, photo_url: str (if using), breed: str} |
|                        |                         |             |                             | filter_species: str (current species filter value, e.g. 'All', 'Dog')|
| /pets/search           | pet_search               | POST        | pet_listings.html (on form submit) | pets: filtered list as above depending on search and filter criteria|
| /pets/<int:pet_id>     | pet_details              | GET         | pet_details.html            | pet: dict {pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, shelter_id: int, status: str, date_added: str}|
| /pets/add              | add_pet                  | GET         | add_pet.html                | None                                                         |
| /pets/add              | add_pet_submit           | POST        | add_pet.html (on failure) or Redirect to /pets (on success) | form errors: dict (optional, for validation errors)            |
| /applications/new/<int:pet_id> | adoption_application    | GET         | adoption_application.html   | pet: dict as above (essential pet data), empty application form fields|
| /applications/new/<int:pet_id> | submit_adoption_application | POST        | adoption_application.html (on failure) or Redirect to /my-applications (on success) | form errors: dict (optional)                                   |
| /my-applications       | my_applications          | GET         | my_applications.html        | applications: list of dict {application_id: int, pet_id: int, pet_name: str, date_submitted: str, status: str}|
|                        |                         |             |                             | filter_status: str ('All', 'Pending', 'Approved', 'Rejected')    |
| /favorites             | favorites                | GET         | favorites.html              | favorites: list of dict {pet_id: int, name: str, species: str, age: str}|
| /messages              | messages                 | GET         | messages.html               | conversations: list of dict {conversation_id: int, other_user: str, last_message: str, timestamp: str}|
| /messages/send         | send_message             | POST        | messages.html (on failure) or Redirect to /messages (on success) | form errors: dict (optional)                                   |
| /profile               | user_profile             | GET         | profile.html                | username: str, email: str                                       |
| /profile/update        | update_profile           | POST        | profile.html (on failure) or Redirect to /dashboard (on success) | form errors: dict (optional)                                   |
| /admin                 | admin_panel              | GET         | admin_panel.html            | pending_applications: list of dict {application_id: int, applicant_name: str, pet_name: str, status: str} | 
|                        |                         |             |                             | all_pets: list of dict {pet_id: int, name: str, species: str, status: str}|

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File path: templates/dashboard.html
- Page Title (for <title> and <h1>): Pet Adoption Dashboard
- Element IDs and types:
  - dashboard-page: div
  - featured-pets: div
  - browse-pets-button: button
  - back-to-dashboard: button
- Navigation mappings:
  - browse-pets-button: url_for('pet_listings')
  - back-to-dashboard: url_for('dashboard') (reloads current page)
- Context variables:
  - featured_pets: list of dict {pet_id: int, name: str, species: str, age: str}
  - recent_activities: list of dict (optional if implemented)

### 2. Pet Listings Page
- File path: templates/pet_listings.html
- Page Title: Available Pets
- Element IDs and types:
  - pet-listings-page: div
  - search-input: input
  - filter-species: select
  - pet-grid: div
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
  - Each pet card inside pet-grid links to pet details page via: url_for('pet_details', pet_id=pet.pet_id)
- Context variables:
  - pets: list of dict {pet_id: int, name: str, species: str, age: str, photo_url: str (optional), breed: str}
  - filter_species: str

### 3. Pet Details Page
- File path: templates/pet_details.html
- Page Title: Pet Details
- Element IDs and types:
  - pet-details-page: div
  - pet-name: h1
  - pet-species: div
  - pet-description: div
  - adopt-button: button
  - back-to-listings: button
- Navigation mappings:
  - adopt-button: url_for('adoption_application', pet_id=pet.pet_id)
  - back-to-listings: url_for('pet_listings')
- Context variables:
  - pet: dict {pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, shelter_id: int, status: str, date_added: str}

### 4. Add Pet Page
- File path: templates/add_pet.html
- Page Title: Add New Pet
- Element IDs and types:
  - add-pet-page: div
  - pet-name-input: input
  - pet-species-input: select
  - pet-breed-input: input
  - pet-age-input: input
  - pet-gender-input: select
  - pet-size-input: select
  - pet-description-input: textarea
  - submit-pet-button: button
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - None (for GET request, empty form)
  - form errors: dict (optional, to show validation messages)

### 5. Adoption Application Page
- File path: templates/adoption_application.html
- Page Title: Adoption Application
- Element IDs and types:
  - application-page: div
  - applicant-name: input
  - applicant-phone: input
  - housing-type: select
  - reason: textarea
  - submit-application-button: button
  - back-to-pet: button
- Navigation mappings:
  - back-to-pet: url_for('pet_details', pet_id=pet.pet_id)
- Context variables:
  - pet: dict {pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, shelter_id: int, status: str, date_added: str}
  - Empty fields for form input on GET
  - form errors: dict (optional)

### 6. My Applications Page
- File path: templates/my_applications.html
- Page Title: My Applications
- Element IDs and types:
  - my-applications-page: div
  - filter-status: select
  - applications-table: table
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - applications: list of dict {application_id: int, pet_id: int, pet_name: str, date_submitted: str, status: str}
  - filter_status: str

### 7. Favorites Page
- File path: templates/favorites.html
- Page Title: My Favorites
- Element IDs and types:
  - favorites-page: div
  - favorites-grid: div
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - favorites: list of dict {pet_id: int, name: str, species: str, age: str}

### 8. Messages Page
- File path: templates/messages.html
- Page Title: Messages
- Element IDs and types:
  - messages-page: div
  - conversation-list: div
  - message-input: textarea
  - send-message-button: button
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - conversations: list of dict {conversation_id: int, other_user: str, last_message: str, timestamp: str}

### 9. User Profile Page
- File path: templates/profile.html
- Page Title: My Profile
- Element IDs and types:
  - profile-page: div
  - profile-username: div
  - profile-email: input
  - update-profile-button: button
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - username: str
  - email: str

### 10. Admin Panel Page
- File path: templates/admin_panel.html
- Page Title: Admin Panel
- Element IDs and types:
  - admin-panel-page: div
  - pending-applications: div
  - all-pets-list: div
  - back-to-dashboard: button
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Context variables:
  - pending_applications: list of dict {application_id: int, applicant_name: str, pet_name: str, status: str}
  - all_pets: list of dict {pet_id: int, name: str, species: str, status: str}

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited): username|email|phone|address
- Field Descriptions:
  - username: str, unique user identifier
  - email: str, user email address
  - phone: str, user phone number
  - address: str, user mailing address
- Example Rows:
```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. pets.txt
- Filename: data/pets.txt
- Fields (pipe-delimited): pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
- Field Descriptions:
  - pet_id: int, unique pet identifier
  - name: str, pet name
  - species: str, species of pet (Dog, Cat, Bird, Rabbit, Other)
  - breed: str, breed of pet
  - age: str, age description (e.g., "3 years")
  - gender: str, gender (Male, Female)
  - size: str, size category (Small, Medium, Large)
  - description: str, detailed description
  - shelter_id: int, identifier of shelter
  - status: str, availability status (Available, Pending, Adopted)
  - date_added: str, date the pet was added (YYYY-MM-DD)
- Example Rows:
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. applications.txt
- Filename: data/applications.txt
- Fields (pipe-delimited): application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
- Field Descriptions:
  - application_id: int, unique application identifier
  - username: str, user submitting application
  - pet_id: int, pet applied for
  - applicant_name: str, full name of applicant
  - phone: str, contact number
  - address: str, address of applicant
  - housing_type: str, type of housing (House, Apartment, Condo, Other)
  - has_yard: str, "Yes" or "No" indicating presence of yard
  - other_pets: str, description of other pets
  - experience: str, experience with pets
  - reason: str, explanation why they want the pet
  - status: str, application status (Pending, Approved, Rejected)
  - date_submitted: str, date application submitted (YYYY-MM-DD)
- Example Rows:
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. favorites.txt
- Filename: data/favorites.txt
- Fields (pipe-delimited): username|pet_id|date_added
- Field Descriptions:
  - username: str, user saving favorite
  - pet_id: int, pet saved
  - date_added: str, date pet was favorited (YYYY-MM-DD)
- Example Rows:
```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. messages.txt
- Filename: data/messages.txt
- Fields (pipe-delimited): message_id|sender_username|recipient_username|subject|content|timestamp|is_read
- Field Descriptions:
  - message_id: int, unique message ID
  - sender_username: str, sender's username
  - recipient_username: str, recipient's username
  - subject: str, message subject
  - content: str, message body
  - timestamp: str, datetime of message (YYYY-MM-DD HH:MM:SS)
  - is_read: str, "true" or "false" indicating read status
- Example Rows:
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. adoption_history.txt
- Filename: data/adoption_history.txt
- Fields (pipe-delimited): history_id|username|pet_id|pet_name|adoption_date|shelter_id
- Field Descriptions:
  - history_id: int, unique adoption history ID
  - username: str, adopter's username
  - pet_id: int, adopted pet's ID
  - pet_name: str, adopted pet's name
  - adoption_date: str, date of adoption (YYYY-MM-DD)
  - shelter_id: int, shelter ID
- Example Rows:
```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. shelters.txt
- Filename: data/shelters.txt
- Fields (pipe-delimited): shelter_id|name|address|phone|email
- Field Descriptions:
  - shelter_id: int, unique shelter identifier
  - name: str, shelter name
  - address: str, shelter address
  - phone: str, contact phone number
  - email: str, contact email address
- Example Rows:
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```

---

### Notes:
- All context variable names and element IDs must match exactly as specified above.
- Form submissions are handled via POST requests where indicated.
- Dynamic route parameters use Flask/Jinja2 syntax for template dynamic URLs.
- Pagination or additional filtering beyond requirements is not defined but can be considered in backend logic.
- Backend developers should parse and write text files according to the exact pipe-delimited format.
- Frontend templates will consume context variables as described, supporting display and input forms accordingly.

This design specification fully supports complete independent parallel development of backend and frontend components of PetAdoptionCenter.
