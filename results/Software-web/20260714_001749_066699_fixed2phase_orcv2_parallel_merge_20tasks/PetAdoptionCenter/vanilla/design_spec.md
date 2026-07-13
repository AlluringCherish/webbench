# Design Specification Document for PetAdoptionCenter

---

## Section 1: Comprehensive Backend Routes and Data Schemas

### 1. Flask Routes Specification

#### Dashboard Page
- **Route:** `/dashboard`
- **Methods:** GET
- **Purpose:** Load main dashboard displaying featured pets and recent activities.

#### Pet Listings Page
- **Route:** `/pets`
- **Methods:** GET
- **Parameters:** Optional query parameters: `search`, `species` (supports All, Dog, Cat, Bird, Rabbit, Other)
- **Purpose:** List all available pets applying optional filters.

#### Pet Details Page
- **Route:** `/pets/<int:pet_id>`
- **Methods:** GET
- **Purpose:** Show detailed information for a pet identified by `pet_id`.

#### Add Pet Page
- **Route:** `/pets/add`
- **Methods:** GET (load form), POST (submit new pet)
- **Purpose:** Allow shelter administrators to add new pet listings.

#### Adoption Application Page
- **Route:** `/applications/add/<int:pet_id>`
- **Methods:** GET (load form), POST (submit application)
- **Purpose:** Submit new adoption application for pet `pet_id`.

#### My Applications Page
- **Route:** `/applications`
- **Methods:** GET
- **Parameters:** Optional query parameter: `status` (All, Pending, Approved, Rejected)
- **Purpose:** List all adoption applications by current user filtered by status.

#### Favorites Page
- **Route:** `/favorites`
- **Methods:** GET
- **Purpose:** Display pets marked as favorites by the current user.

- **Route (Add Favorite):** `/favorites/add/<int:pet_id>`
- **Methods:** POST
- **Purpose:** Add a pet to user's favorites.

- **Route (Remove Favorite):** `/favorites/remove/<int:pet_id>`
- **Methods:** POST
- **Purpose:** Remove a pet from user's favorites.

#### Messages Page
- **Route:** `/messages`
- **Methods:** GET
- **Purpose:** Display list of message conversations for current user.

- **Route (Send Message):** `/messages/send`
- **Methods:** POST
- **Purpose:** Send message from current user to a shelter or other user.

- **Route (View Conversation):** `/messages/conversation/<string:other_username>`
- **Methods:** GET
- **Purpose:** View message history between current user and `other_username`.

#### User Profile Page
- **Route:** `/profile`
- **Methods:** GET (view profile), POST (update profile email)
- **Purpose:** View and update user profile information.

#### Admin Panel Page
- **Route:** `/admin`
- **Methods:** GET
- **Purpose:** Display list of pending applications and all pets with edit/delete options.

- **Route (Update Application Status):** `/admin/application/<int:application_id>/update`
- **Methods:** POST
- **Purpose:** Admin updates adoption application status.

- **Route (Edit Pet):** `/admin/pet/<int:pet_id>/edit`
- **Methods:** GET (load edit form), POST (submit edits)
- **Purpose:** Admin edits pet details.

- **Route (Delete Pet):** `/admin/pet/<int:pet_id>/delete`
- **Methods:** POST
- **Purpose:** Admin deletes pet from listings.

### 2. Data Schemas

Data files are located in the `data/` folder, using pipe `|` delimited fields.

#### 2.1 users.txt
- Fields: `username|email|phone|address`
- Example: `john_doe|john@example.com|555-1234|123 Main St, City`
- Operations: Read for user info, overwrite line on updates.

#### 2.2 pets.txt
- Fields:
```
pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
```
- Example:
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
```
- Operations: Read all; add/edit/delete; filter by status/species.

#### 2.3 applications.txt
- Fields:
```
application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
```
- Example:
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
```
- Operations: Read all user applications; add new; update status.

#### 2.4 favorites.txt
- Fields:
```
username|pet_id|date_added
```
- Example:
```
john_doe|1|2024-11-01
```
- Operations: Read favorites; add/remove entries.

#### 2.5 messages.txt
- Fields:
```
message_id|sender_username|recipient_username|subject|content|timestamp|is_read
```
- Example:
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
```
- Operations: Read sent/received; add new; update read status.

#### 2.6 adoption_history.txt
- Fields:
```
history_id|username|pet_id|pet_name|adoption_date|shelter_id
```
- Example:
```
1|jane_smith|2|Whiskers|2024-11-15|1
```
- Operations: Read history for showing successful adoptions.

#### 2.7 shelters.txt
- Fields:
```
shelter_id|name|address|phone|email
```
- Example:
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
```
- Operations: Read shelter info for display and messaging.

### 3. Backend Logic Overview

- Dashboard fetches up to 5 latest available pets and recent activities.
- Pet Listings supports filtering by name and species.
- Pet Details provides full pet info including shelter details.
- Add Pet allows admins to add new pets with validation.
- Adoption Application page manages applying for adoption with form submission.
- My Applications lists current user's adoption applications filtered by status.
- Favorites page shows user's favorite pets; supports add/remove.
- Messages page lists conversations and enables sending messages.
- User Profile shows and updates user's email.
- Admin Panel manages applications and pets including edit/delete.


---

## Section 2: Detailed Frontend Template Specifications

### 1. Dashboard Page
- Template Filename: dashboard.html
- Page Title: Pet Adoption Dashboard
- Elements:
  - div#dashboard-page (container)
  - div#featured-pets (featured pets display, max 5 pets)
  - button#browse-pets-button (navigate to Pet Listings page)
  - button#back-to-dashboard (refresh dashboard page)

### 2. Pet Listings Page
- Template Filename: pet_listings.html
- Page Title: Available Pets
- Elements:
  - div#pet-listings-page (container)
  - input#search-input (search pets by name)
  - select#filter-species (dropdown filter for species: All, Dog, Cat, Bird, Rabbit, Other)
  - div#pet-grid (grid container for pet cards: photo, name, species, age)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 3. Pet Details Page
- Template Filename: pet_details.html
- Page Title: Pet Details
- Elements:
  - div#pet-details-page (container)
  - h1#pet-name (displays pet's name)
  - div#pet-species (displays pet species)
  - div#pet-description (detailed pet description)
  - button#adopt-button (starts adoption application process)
  - button#back-to-listings (navigate back to Pet Listings page)

### 4. Add Pet Page
- Template Filename: add_pet.html
- Page Title: Add New Pet
- Elements:
  - div#add-pet-page (container)
  - input#pet-name-input (input pet name)
  - select#pet-species-input (select species from Dog, Cat, Bird, Rabbit, Other)
  - input#pet-breed-input (input breed)
  - input#pet-age-input (input age, e.g., "2 years")
  - select#pet-gender-input (select gender: Male, Female)
  - select#pet-size-input (select size: Small, Medium, Large)
  - textarea#pet-description-input (input detailed pet description)
  - button#submit-pet-button (submit new pet listing)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 5. Adoption Application Page
- Template Filename: adoption_application.html
- Page Title: Adoption Application
- Elements:
  - div#application-page (container)
  - input#applicant-name (input full name)
  - input#applicant-phone (input phone number)
  - select#housing-type (select housing type: House, Apartment, Condo, Other)
  - textarea#reason (textarea explaining reason for adoption)
  - button#submit-application-button (submit adoption application)
  - button#back-to-pet (navigate back to Pet Details page)

### 6. My Applications Page
- Template Filename: my_applications.html
- Page Title: My Applications
- Elements:
  - div#my-applications-page (container)
  - select#filter-status (filter applications by status: All, Pending, Approved, Rejected)
  - table#applications-table (displays applications with columns: pet name, date, status, actions)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 7. Favorites Page
- Template Filename: favorites.html
- Page Title: My Favorites
- Elements:
  - div#favorites-page (container)
  - div#favorites-grid (grid for favorite pet cards)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 8. Messages Page
- Template Filename: messages.html
- Page Title: Messages
- Elements:
  - div#messages-page (container)
  - div#conversation-list (list of message conversations)
  - textarea#message-input (compose new message)
  - button#send-message-button (send message)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 9. User Profile Page
- Template Filename: profile.html
- Page Title: My Profile
- Elements:
  - div#profile-page (container)
  - div#profile-username (display username, not editable)
  - input#profile-email (input field to update email)
  - button#update-profile-button (save profile changes)
  - button#back-to-dashboard (navigate back to Dashboard page)

### 10. Admin Panel Page
- Template Filename: admin_panel.html
- Page Title: Admin Panel
- Elements:
  - div#admin-panel-page (container)
  - div#pending-applications (list of pending adoption applications)
  - div#all-pets-list (list of all pets with edit/delete options)
  - button#back-to-dashboard (navigate back to Dashboard page)


---

## Section 3: Cross-Artifact Consistency Checks and Navigation Mappings

### Navigation and Interaction Flow Consistency
- Dashboard #browse-pets-button navigates to `/pets` page with template `pet_listings.html`.
- Pet Listings page uses `/pets` route, with optional query parameters matching filters #search-input and #filter-species.
- Pet cards in #pet-grid link to `/pets/<pet_id>` route, rendered with `pet_details.html`.
- Pet Details page #adopt-button navigates to `/applications/add/<pet_id>` adoption application page.
- Adoption Application page #submit-application-button posts to `/applications/add/<pet_id>`.
- My Applications page corresponds to `/applications` GET route with optional `status` filter matching #filter-status dropdown.
- Favorites page `/favorites` matches UI container #favorites-page and supports add/remove favorites via POST to `/favorites/add/<pet_id>` and `/favorites/remove/<pet_id>`.
- Messages page `/messages` supports GET for conversation list, POST to `/messages/send` for sending.
- User Profile page `/profile` supports GET and POST for profile viewing/updating, matching UI elements.
- Admin Panel `/admin` and subpaths support management of applications and pets, matching UI lists and controls.

### Parameter and Field Name Consistency
- Route parameters `<int:pet_id>`, `<int:application_id>`, and `<string:other_username>` correspond exactly to frontend context usage.
- Data fields used in backend files match frontend data binding placeholders:
  - Pet fields for name, species, age, description
  - Application fields including applicant name, phone, reason etc.
  - User fields for username and email
- UI element IDs correspond perfectly with expected functional elements for user interaction.

### Summary
The merged design specification assures:
- Complete backend route and data schema definitions aligned with frontend page templates and UI elements.
- Consistent parameter passing and data binding between backend and frontend.
- Clear navigation flows between pages consistent with route definitions.
- No additional features or requirements beyond the given user specifications.

This document provides a unified blueprint for both backend Flask API and frontend HTML template development, enabling seamless integration in the PetAdoptionCenter project.
