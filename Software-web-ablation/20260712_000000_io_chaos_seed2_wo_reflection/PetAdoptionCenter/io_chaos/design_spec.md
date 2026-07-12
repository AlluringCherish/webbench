# PetAdoptionCenter Design Specifications

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                   | Function Name            | HTTP Method(s) | Template Rendered           | Context Variables (Name: Type)                                     |
|-----------------------------|--------------------------|----------------|-----------------------------|--------------------------------------------------------------------|
| /                           | root_redirect             | GET            | _redirects to /dashboard_   | None                                                               |
| /dashboard                  | dashboard_page            | GET            | dashboard.html              | featured_pets: list of dict (pet_id: int, name: str, species: str, age: str, photo_url: str), recent_activities: list of str |
| /pets                      | pet_listings_page          | GET            | pet_listings.html           | pets: list of dict (pet_id: int, name: str, species: str, age: str, photo_url: str), species_filter_options: list of str (All, Dog, Cat, Bird, Rabbit, Other), selected_species: str, search_query: str |
| /pets/<int:pet_id>         | pet_details_page           | GET            | pet_details.html            | pet: dict (pet_id: int, name: str, species: str, breed: str, age: str, gender: str, size: str, description: str, status: str), shelter_info: dict (shelter_id: int, name: str, phone: str, email: str) |
| /pets/add                  | add_pet_page               | GET, POST     | add_pet.html                | (GET) None; (POST) form submission handling                          |
| /applications/apply/<int:pet_id> | adoption_application_page | GET, POST     | adoption_application.html   | (GET) pet: dict (pet_id: int, name: str); (POST) form submission handling  |
| /applications/my           | my_applications_page       | GET            | my_applications.html        | applications: list of dict (application_id: int, pet_name: str, date: str, status: str), status_filter_options: list of str (All, Pending, Approved, Rejected), selected_status: str |
| /favorites                 | favorites_page             | GET            | favorites.html              | favorite_pets: list of dict (pet_id: int, name: str, species: str, age: str, photo_url: str) |
| /messages                  | messages_page              | GET, POST     | messages.html               | (GET) conversations: list of dict (conversation_id: int, participants: list of str, last_message_preview: str), (POST) message submission handling |
| /profile                   | user_profile_page          | GET, POST     | profile.html                | (GET) user_profile: dict (username: str, email: str), (POST) profile update submission handling |
| /admin                    | admin_panel_page           | GET            | admin_panel.html            | pending_applications: list of dict (application_id: int, applicant_name: str, pet_name: str, date_submitted: str), all_pets: list of dict (pet_id: int, name: str, status: str) |

---

### Notes on Flask Routes:
- The root route (`/`) redirects to `/dashboard`.
- POST methods used for form submissions: adding pets, submitting adoption applications, sending messages, and updating profiles.
- Context variables are typed precisely for frontend template consumption.


## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File: `templates/dashboard.html`
- Title: <title>Pet Adoption Dashboard</title>
- Heading: <h1 id="dashboard-page">Pet Adoption Dashboard</h1>
- Element IDs and Types:
  - dashboard-page (div)
  - featured-pets (div)
  - browse-pets-button (button)
  - back-to-dashboard (button)
- Navigation:
  - browse-pets-button: links to `url_for('pet_listings_page')`
  - back-to-dashboard: triggers a reload or links to `url_for('dashboard_page')`
- Context Variables:
  - featured_pets: list of dict {pet_id, name, species, age, photo_url}
  - recent_activities: list of str

### 2. Pet Listings Page
- File: `templates/pet_listings.html`
- Title: <title>Available Pets</title>
- Heading: <h1 id="pet-listings-page">Available Pets</h1>
- Element IDs and Types:
  - pet-listings-page (div)
  - search-input (input)
  - filter-species (select/dropdown)
  - pet-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
  - each pet card links to pet details using `url_for('pet_details_page', pet_id=pet.pet_id)`
- Context Variables:
  - pets: list of dict {pet_id, name, species, age, photo_url}
  - species_filter_options: list of str (All, Dog, Cat, Bird, Rabbit, Other)
  - selected_species: str
  - search_query: str

### 3. Pet Details Page
- File: `templates/pet_details.html`
- Title: <title>Pet Details</title>
- Heading: <h1 id="pet-name">{{ pet.name }}</h1>
- Element IDs and Types:
  - pet-details-page (div)
  - pet-name (h1)
  - pet-species (div)
  - pet-description (div)
  - adopt-button (button)
  - back-to-listings (button)
- Navigation:
  - adopt-button: links to `url_for('adoption_application_page', pet_id=pet.pet_id)`
  - back-to-listings: links to `url_for('pet_listings_page')`
- Context Variables:
  - pet: dict with full pet details
  - shelter_info: dict

### 4. Add Pet Page
- File: `templates/add_pet.html`
- Title: <title>Add New Pet</title>
- Heading: <h1 id="add-pet-page">Add New Pet</h1>
- Element IDs and Types:
  - add-pet-page (div)
  - pet-name-input (input)
  - pet-species-input (select/dropdown)
  - pet-breed-input (input)
  - pet-age-input (input)
  - pet-gender-input (select/dropdown)
  - pet-size-input (select/dropdown)
  - pet-description-input (textarea)
  - submit-pet-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - None (form only)

### 5. Adoption Application Page
- File: `templates/adoption_application.html`
- Title: <title>Adoption Application</title>
- Heading: <h1 id="application-page">Adoption Application</h1>
- Element IDs and Types:
  - application-page (div)
  - applicant-name (input)
  - applicant-phone (input)
  - housing-type (select/dropdown)
  - reason (textarea)
  - submit-application-button (button)
  - back-to-pet (button)
- Navigation:
  - back-to-pet: links to `url_for('pet_details_page', pet_id=pet.pet_id)`
- Context Variables:
  - pet: dict (pet_id, name)

### 6. My Applications Page
- File: `templates/my_applications.html`
- Title: <title>My Applications</title>
- Heading: <h1 id="my-applications-page">My Applications</h1>
- Element IDs and Types:
  - my-applications-page (div)
  - filter-status (select/dropdown)
  - applications-table (table)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - applications: list of dict {application_id, pet_name, date, status}
  - status_filter_options: list of str
  - selected_status: str

### 7. Favorites Page
- File: `templates/favorites.html`
- Title: <title>My Favorites</title>
- Heading: <h1 id="favorites-page">My Favorites</h1>
- Element IDs and Types:
  - favorites-page (div)
  - favorites-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - favorite_pets: list of dict {pet_id, name, species, age, photo_url}

### 8. Messages Page
- File: `templates/messages.html`
- Title: <title>Messages</title>
- Heading: <h1 id="messages-page">Messages</h1>
- Element IDs and Types:
  - messages-page (div)
  - conversation-list (div)
  - message-input (textarea)
  - send-message-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - conversations: list of dict {conversation_id, participants: list of str, last_message_preview: str}

### 9. User Profile Page
- File: `templates/profile.html`
- Title: <title>My Profile</title>
- Heading: <h1 id="profile-page">My Profile</h1>
- Element IDs and Types:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - user_profile: dict {username: str, email: str}

### 10. Admin Panel Page
- File: `templates/admin_panel.html`
- Title: <title>Admin Panel</title>
- Heading: <h1 id="admin-panel-page">Admin Panel</h1>
- Element IDs and Types:
  - admin-panel-page (div)
  - pending-applications (div)
  - all-pets-list (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: links to `url_for('dashboard_page')`
- Context Variables:
  - pending_applications: list of dict {application_id, applicant_name, pet_name, date_submitted}
  - all_pets: list of dict {pet_id, name, status}

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: `data/users.txt`
- Fields (pipe-delimited):
  1. username (str): Unique user identifier
  2. email (str): User's email address
  3. phone (str): User's phone number
  4. address (str): User's mailing address
- Example Row:
  `john_doe|john@example.com|555-1234|123 Main St, City`

### 2. pets.txt
- Filename: `data/pets.txt`
- Fields (pipe-delimited):
  1. pet_id (int): Unique pet identifier
  2. name (str): Pet's name
  3. species (str): Species of the pet
  4. breed (str): Breed of the pet
  5. age (str): Age of the pet (e.g., "3 years")
  6. gender (str): "Male" or "Female"
  7. size (str): Size category (Small, Medium, Large)
  8. description (str): Detailed pet description
  9. shelter_id (int): Shelter identifier where pet is located
  10. status (str): Adoption status (Available, Pending)
  11. date_added (str): Date added in YYYY-MM-DD format
- Example Row:
  `1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15`

### 3. applications.txt
- Filename: `data/applications.txt`
- Fields (pipe-delimited):
  1. application_id (int): Unique application identifier
  2. username (str): Username of applicant
  3. pet_id (int): Pet identifier applied for
  4. applicant_name (str): Full name of applicant
  5. phone (str): Contact phone number
  6. address (str): Applicant's address
  7. housing_type (str): Housing type (House, Apartment, Condo, Other)
  8. has_yard (str): "Yes" or "No"
  9. other_pets (str): Description of other pets
  10. experience (str): Experience with pets
  11. reason (str): Reason for adoption
  12. status (str): Application status (Pending, Approved, Rejected)
  13. date_submitted (str): Date submitted YYYY-MM-DD
- Example Row:
  `1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10`

### 4. favorites.txt
- Filename: `data/favorites.txt`
- Fields (pipe-delimited):
  1. username (str): Username
  2. pet_id (int): Pet identifier
  3. date_added (str): Date added YYYY-MM-DD
- Example Row:
  `john_doe|1|2024-11-01`

### 5. messages.txt
- Filename: `data/messages.txt`
- Fields (pipe-delimited):
  1. message_id (int): Unique message identifier
  2. sender_username (str): Sender's username
  3. recipient_username (str): Recipient's username
  4. subject (str): Subject of message
  5. content (str): Message content
  6. timestamp (str): DateTime in YYYY-MM-DD HH:MM:SS
  7. is_read (str): "true" or "false" indicating read status
- Example Row:
  `1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true`

### 6. adoption_history.txt
- Filename: `data/adoption_history.txt`
- Fields (pipe-delimited):
  1. history_id (int): Unique history record identifier
  2. username (str): Username of adopter
  3. pet_id (int): Pet identifier
  4. pet_name (str): Pet name
  5. adoption_date (str): Adoption date YYYY-MM-DD
  6. shelter_id (int): Shelter identifier
- Example Row:
  `1|jane_smith|2|Whiskers|2024-11-15|1`

### 7. shelters.txt
- Filename: `data/shelters.txt`
- Fields (pipe-delimited):
  1. shelter_id (int): Unique shelter identifier
  2. name (str): Shelter name
  3. address (str): Shelter address
  4. phone (str): Shelter phone number
  5. email (str): Shelter contact email
- Example Row:
  `1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com`

---

This design specification document provides all required details to enable backend and frontend developers to work independently and in parallel for the PetAdoptionCenter application.
