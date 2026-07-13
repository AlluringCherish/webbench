# Frontend Design Document for PetAdoptionCenter

---

## Section 1: HTML Template Structure and IDs

### 1. Dashboard Page
- Template Filename: dashboard.html
- Page Title: Pet Adoption Dashboard
- Elements:
  - div#dashboard-page (container)
  - div#featured-pets (featured pets display, max 5 pets)
  - button#browse-pets-button (navigate to Pet Listings page)
  - button#back-to-dashboard (refresh dashboard page)

---

### 2. Pet Listings Page
- Template Filename: pet_listings.html
- Page Title: Available Pets
- Elements:
  - div#pet-listings-page (container)
  - input#search-input (text input for searching pets by name)
  - select#filter-species (dropdown filter for species: All, Dog, Cat, Bird, Rabbit, Other)
  - div#pet-grid (grid container for pet cards: photo, name, species, age)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

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

---

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

---

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

---

### 6. My Applications Page
- Template Filename: my_applications.html
- Page Title: My Applications
- Elements:
  - div#my-applications-page (container)
  - select#filter-status (filter applications by status: All, Pending, Approved, Rejected)
  - table#applications-table (displays applications with columns: pet name, date, status, actions)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

### 7. Favorites Page
- Template Filename: favorites.html
- Page Title: My Favorites
- Elements:
  - div#favorites-page (container)
  - div#favorites-grid (grid for favorite pet cards)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

### 8. Messages Page
- Template Filename: messages.html
- Page Title: Messages
- Elements:
  - div#messages-page (container)
  - div#conversation-list (list of message conversations)
  - textarea#message-input (compose new message)
  - button#send-message-button (send message)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

### 9. User Profile Page
- Template Filename: profile.html
- Page Title: My Profile
- Elements:
  - div#profile-page (container)
  - div#profile-username (display username, not editable)
  - input#profile-email (input field to update email)
  - button#update-profile-button (save profile changes)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

### 10. Admin Panel Page
- Template Filename: admin_panel.html
- Page Title: Admin Panel
- Elements:
  - div#admin-panel-page (container)
  - div#pending-applications (list of pending adoption applications)
  - div#all-pets-list (list of all pets with edit/delete options)
  - button#back-to-dashboard (navigate back to Dashboard page)

---

## Section 2: Navigation and Interaction Flow

- Dashboard Page:
  - #browse-pets-button navigates to Pet Listings Page (pet_listings.html)
  - #back-to-dashboard on Dashboard page refreshes the dashboard content

- Pet Listings Page:
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)
  - Pet cards inside #pet-grid should be clickable to navigate to Pet Details Page with selected pet's details

- Pet Details Page:
  - #adopt-button navigates to Adoption Application Page (adoption_application.html) with pet context
  - #back-to-listings navigates back to Pet Listings Page (pet_listings.html)

- Add Pet Page:
  - #submit-pet-button triggers submission of new pet data
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)

- Adoption Application Page:
  - #submit-application-button submits application data
  - #back-to-pet navigates back to Pet Details Page (pet_details.html) for the pet in application context

- My Applications Page:
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)
  - Actions in #applications-table may include buttons to view details or cancel applications

- Favorites Page:
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)
  - Favorite pet cards in #favorites-grid link to corresponding Pet Details Page

- Messages Page:
  - #send-message-button sends composed message
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)
  - Clicking conversations in #conversation-list loads the conversation thread

- User Profile Page:
  - #update-profile-button saves profile changes
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)

- Admin Panel Page:
  - #back-to-dashboard navigates to Dashboard Page (dashboard.html)
  - #pending-applications includes controls for approving/rejecting applications
  - #all-pets-list includes controls for editing/deleting pet entries

---

## Section 3: Data Binding Placeholders

Note: Placeholder syntax is generic and may be templating-engine specific (e.g. {{variable}}) in implementation.

### Dashboard Page
- #featured-pets: List of featured pets with properties (photo, name, species, age) limited to 5.

### Pet Listings Page
- #search-input: Two-way binding with search query string.
- #filter-species: Bound to species filter selection.
- #pet-grid: Dynamic list of pet cards, each with:
  - pet photo
  - pet name
  - species
  - age

### Pet Details Page
- #pet-name: {{pet.name}}
- #pet-species: {{pet.species}}
- #pet-description: {{pet.description}}
- Pet context (pet_id) passed for adoption application and navigation.

### Add Pet Page
- #pet-name-input, #pet-breed-input, #pet-age-input, #pet-description-input: Bound to new pet entry fields.
- #pet-species-input, #pet-gender-input, #pet-size-input: Bound to selected dropdown options.

### Adoption Application Page
- #applicant-name, #applicant-phone: Bound to user input.
- #housing-type: Selected housing option.
- #reason: Textarea content.
- Associated pet context (pet_id) for application.

### My Applications Page
- #filter-status: Bound to application status filter.
- #applications-table: Dynamic rows with application details:
  - Pet name
  - Application date
  - Status
  - Action buttons (view/cancel)

### Favorites Page
- #favorites-grid: Dynamic grid of favorite pets, each pet card with data as in listings.

### Messages Page
- #conversation-list: List of conversations with snippet preview.
- #message-input: Bound to new message content.
- Messages linked by sender and recipient usernames.

### User Profile Page
- #profile-username: Display current username.
- #profile-email: Editable email input.

### Admin Panel Page
- #pending-applications: List of applications with approve/reject controls.
- #all-pets-list: List of pets with edit/delete controls.

---

This design document provides a clear and detailed blueprint for frontend template development of the PetAdoptionCenter application, ensuring consistent ID usage, proper navigation flows, and comprehensive data placeholders for integration with backend functionality.