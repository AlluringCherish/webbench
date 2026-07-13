# PetAdoptionCenter Detailed Design Specification

---

## 1. Flask Route Architecture

| Route Path                  | Function Name           | HTTP Methods | Template File                 | Context Variables (Type)                                                  |
|-----------------------------|------------------------|--------------|------------------------------|--------------------------------------------------------------------------|
| /                           | dashboard              | GET          | templates/dashboard.html     | featured_pets (list of dict: pet_id, name, species, age, photo_url)       |
| /pets                       | pet_listings           | GET          | templates/pet_listings.html  | pets (list of dict), filter_species (str), search_query (str)            |
| /pet/<int:pet_id>           | pet_details            | GET          | templates/pet_details.html   | pet (dict), e.g. name (str), species (str), description (str), status(str) |
| /pet/add                   | add_pet                | GET, POST    | templates/add_pet.html       | For GET no context; For POST, form submission processing                 |
| /application/<int:pet_id>   | adoption_application   | GET, POST    | templates/application.html    | pet (dict), user info form fields on GET; form data on POST              |
| /applications               | my_applications        | GET          | templates/my_applications.html| applications (list of dict), filter_status (str)                        |
| /favorites                 | favorites              | GET          | templates/favorites.html     | favorite_pets (list of dict)                                              |
| /messages                  | messages               | GET, POST    | templates/messages.html      | conversations (list of dict), messages, on POST process sending          |
| /profile                   | user_profile           | GET, POST    | templates/profile.html       | user profile info dict                                                   |
| /admin                    | admin_panel            | GET          | templates/admin_panel.html   | pending_applications (list of dict), all_pets (list of dict)             |

---

## 2. Page and Template Mapping with UI Elements

### 1. Dashboard Page - templates/dashboard.html
- Container Div: ID: dashboard-page
- Featured Pets Div: ID: featured-pets
- Button: ID: browse-pets-button (navigate to pet_listings)
- Button: ID: back-to-dashboard (refreshes dashboard)

Context Variables:
- featured_pets: List of pets dict (pet_id:int, name:str, species:str, age:str, photo_url:str)

---

### 2. Pet Listings Page - templates/pet_listings.html
- Container Div: ID: pet-listings-page
- Input: ID: search-input (text input to filter pets by name)
- Dropdown: ID: filter-species (options: All, Dog, Cat, Bird, Rabbit, Other)
- Div (Grid): ID: pet-grid (displays pet cards with photo, name, species, age)
- Button: ID: back-to-dashboard (navigate to dashboard)

Context Variables:
- pets: List of pet dict (id, name, species, breed, age, gender, size, description, shelter_id, status, date_added)
- filter_species: str
- search_query: str

---

### 3. Pet Details Page - templates/pet_details.html
- Container Div: ID: pet-details-page
- H1: ID: pet-name (pet name)
- Div: ID: pet-species (pet species)
- Div: ID: pet-description (full description)
- Button: ID: adopt-button (navigate to adoption_application with pet_id)
- Button: ID: back-to-listings (navigate back to pet_listings)

Context Variables:
- pet: dict with pet details

---

### 4. Add Pet Page - templates/add_pet.html
- Container Div: ID: add-pet-page
- Input: ID: pet-name-input
- Dropdown: ID: pet-species-input (Dog, Cat, Bird, Rabbit, Other)
- Input: ID: pet-breed-input
- Input: ID: pet-age-input
- Dropdown: ID: pet-gender-input (Male, Female)
- Dropdown: ID: pet-size-input (Small, Medium, Large)
- Textarea: ID: pet-description-input
- Button: ID: submit-pet-button
- Button: ID: back-to-dashboard

Context Variables:
- None for GET, POST processes form submission

---

### 5. Adoption Application Page - templates/application.html
- Container Div: ID: application-page
- Input: ID: applicant-name
- Input: ID: applicant-phone
- Dropdown: ID: housing-type (House, Apartment, Condo, Other)
- Textarea: ID: reason
- Button: ID: submit-application-button
- Button: ID: back-to-pet

Context Variables:
- pet: dict

---

### 6. My Applications Page - templates/my_applications.html
- Container Div: ID: my-applications-page
- Dropdown: ID: filter-status (All, Pending, Approved, Rejected)
- Table: ID: applications-table (Columns: pet name, date submitted, status, actions)
- Button: ID: back-to-dashboard

Context Variables:
- applications: list of dicts (application_id, pet_name, date_submitted, status)
- filter_status: str

---

### 7. Favorites Page - templates/favorites.html
- Container Div: ID: favorites-page
- Div Grid: ID: favorites-grid
- Button: ID: back-to-dashboard

Context Variables:
- favorite_pets: list of pet dicts

---

### 8. Messages Page - templates/messages.html
- Container Div: ID: messages-page
- Div: ID: conversation-list (list of message conversations)
- Textarea: ID: message-input
- Button: ID: send-message-button
- Button: ID: back-to-dashboard

Context Variables:
- conversations: list of message conversation dicts

---

### 9. User Profile Page - templates/profile.html
- Container Div: ID: profile-page
- Div: ID: profile-username (display only username)
- Input: ID: profile-email
- Button: ID: update-profile-button
- Button: ID: back-to-dashboard

Context Variables:
- user_profile: dict (username, email, phone, address)

---

### 10. Admin Panel Page - templates/admin_panel.html
- Container Div: ID: admin-panel-page
- Div: ID: pending-applications
- Div: ID: all-pets-list
- Button: ID: back-to-dashboard

Context Variables:
- pending_applications: list of application dict (application_id, pet_id, applicant_name, ...)
- all_pets: list of pet dicts

---

## 3. Navigation Logic

- Starting point: Dashboard Page route `/` (function dashboard)

### From Dashboard
- browse-pets-button ➔ `pet_listings` (route: `/pets`)
- back-to-dashboard ➔ refresh dashboard (reload `/`)

### From Pet Listings Page
- back-to-dashboard ➔ `dashboard` (`/`)
- Clicking pet in pet-grid ➔ `pet_details` (`/pet/<pet_id>`)

### From Pet Details Page
- adopt-button ➔ `adoption_application` (`/application/<pet_id>`)
- back-to-listings ➔ `pet_listings` (`/pets`)

### From Add Pet Page
- submit-pet-button ➔ Processes form submission POST on `/pet/add`
- back-to-dashboard ➔ `dashboard` (`/`)

### From Adoption Application Page
- submit-application-button ➔ Processes form submission POST on `/application/<pet_id>`
- back-to-pet ➔ `pet_details` (`/pet/<pet_id>`)

### From My Applications Page
- back-to-dashboard ➔ `dashboard` (`/`)

### From Favorites Page
- back-to-dashboard ➔ `dashboard` (`/`)

### From Messages Page
- back-to-dashboard ➔ `dashboard` (`/`)

### From User Profile Page
- update-profile-button ➔ Processes POST form submission on `/profile`
- back-to-dashboard ➔ `dashboard` (`/`)

### From Admin Panel Page
- back-to-dashboard ➔ `dashboard` (`/`)

---

## 4. Data Files Storage and Access Schema

All files placed in `data/` directory. Parsing and writing uses pipe (`|`) delimiter. Files read and updated atomically.

### users.txt
- Fields (in order): `username|email|phone|address`
- Usage: Store user account data; updated when profile changes.

### pets.txt
- Fields: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Usage: Manage pet listings, add new pets, update status for adoption progress.

### applications.txt
- Fields: `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Usage: Store adoption application details and status changes.

### favorites.txt
- Fields: `username|pet_id|date_added`
- Usage: Manage user's favorite pets.

### messages.txt
- Fields: `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Usage: Manage user and admin messaging.

### adoption_history.txt
- Fields: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Usage: Keep record of completed adoptions.

### shelters.txt
- Fields: `shelter_id|name|address|phone|email`
- Usage: Shelter details used in pet records and admin functions.

---

## 5. Interaction Contracts

### Dashboard Page
- `browse-pets-button`: On click, triggers redirect to `pet_listings` route.
- `back-to-dashboard`: On click, reloads the dashboard page.

### Pet Listings Page
- `search-input`: On input, filters pet grid by name.
- `filter-species`: On change, filters pet grid by species.
- Each pet card in `pet-grid`: On click, navigates to pet details page for that pet.
- `back-to-dashboard`: Navigates back to dashboard.

### Pet Details Page
- `adopt-button`: Navigates to adoption application page for current pet.
- `back-to-listings`: Navigates back to pet listings page.

### Add Pet Page
- `submit-pet-button`: Submits form data via POST to add new pet listing.
- `back-to-dashboard`: Navigates back to dashboard.

### Adoption Application Page
- `submit-application-button`: Submits application form via POST.
- `back-to-pet`: Navigates back to pet details page.

### My Applications Page
- `filter-status`: Filters applications shown by their status.
- `back-to-dashboard`: Navigates back to dashboard.

### Favorites Page
- Displays favorite pets with clickable cards.
- `back-to-dashboard`: Navigates back to dashboard.

### Messages Page
- `send-message-button`: Sends the composed message.
- `back-to-dashboard`: Navigates back to dashboard.

### User Profile Page
- `update-profile-button`: Submits updated profile email via POST.
- `back-to-dashboard`: Navigates back to dashboard.

### Admin Panel Page
- Allows reviewing and managing pending adoption applications and pets.
- `back-to-dashboard`: Navigates back to dashboard.

---

This completes the detailed design specification for the PetAdoptionCenter Flask web application, addressing backend routing, frontend UI elements, user navigation flows, data file schemas, and interaction contracts required for implementation.
