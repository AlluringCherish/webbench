# PetAdoptionCenter Web Application Design Candidate B

---

## 1. Overview

This design candidate B presents a comprehensive alternative for the PetAdoptionCenter web application. It includes detailed page routes, UI elements with IDs and types, data management specs, form validation and processing flows, and user interaction scenarios ensuring full compliance with the given requirements.

---

## 2. Page Routes and Navigation

| Page Name             | URL Route                  | Navigation Paths / Links & Buttons                                        |
|-----------------------|----------------------------|--------------------------------------------------------------------------|
| Dashboard             | `/dashboard`               | - `browse-pets-button` -> `/pets`
- `back-to-dashboard` -> Reload `/dashboard`
| Pet Listings          | `/pets`                   | - Pet card click -> `/pets/<pet_id>` 
- `back-to-dashboard` -> `/dashboard`
| Pet Details           | `/pets/<pet_id>`          | - `adopt-button` -> `/adopt/<pet_id>` 
- `back-to-listings` -> `/pets`
| Add Pet               | `/add-pet`                | - `submit-pet-button` (form submission)
- `back-to-dashboard` -> `/dashboard`
| Adoption Application  | `/adopt/<pet_id>`         | - `submit-application-button` (form submission)
- `back-to-pet` -> `/pets/<pet_id>`
| My Applications       | `/my-applications`        | - Filter status dropdown changes reload/filter table 
- `back-to-dashboard` -> `/dashboard`
| Favorites             | `/favorites`              | - Click favorite pet card -> `/pets/<pet_id>`
- `back-to-dashboard` -> `/dashboard`
| Messages              | `/messages`               | - Select conversation from `conversation-list`
- Send message with `send-message-button`
- `back-to-dashboard` -> `/dashboard`
| User Profile          | `/profile`                | - `update-profile-button` submits profile update
- `back-to-dashboard` -> `/dashboard`
| Admin Panel           | `/admin-panel`            | - Manage applications, pets
- `back-to-dashboard` -> `/dashboard`

---

## 3. Page Composition and UI Elements

### 3.1 Dashboard Page (`/dashboard`)
- **dashboard-page** (Div): Main container for Dashboard
- **featured-pets** (Div): Shows up to 5 featured pets; each with clickable card linking to pet details
- **browse-pets-button** (Button): Navigates to `/pets`
- **back-to-dashboard** (Button): Refreshes the dashboard page

### 3.2 Pet Listings Page (`/pets`)
- **pet-listings-page** (Div): Container
- **search-input** (Input text): Allows text search by pet name; id triggers filter
- **filter-species** (Dropdown): Filter pets by species (All, Dog, Cat, Bird, Rabbit, Other)
- **pet-grid** (Div): Grid display of pet cards, each card clickable linking to pet details
- **back-to-dashboard** (Button): Return to dashboard

### 3.3 Pet Details Page (`/pets/<pet_id>`)
- **pet-details-page** (Div)
- **pet-name** (H1): Displays pet name
- **pet-species** (Div): Displays species
- **pet-description** (Div): Detailed pet description
- **adopt-button** (Button): Starts adoption process (`/adopt/<pet_id>`)
- **back-to-listings** (Button): Back to listings

### 3.4 Add Pet Page (`/add-pet`)
- **add-pet-page** (Div)
- **pet-name-input** (Input text): Name input, required
- **pet-species-input** (Dropdown): Species select
- **pet-breed-input** (Input text): Breed input
- **pet-age-input** (Input text): Age input (format validated)
- **pet-gender-input** (Dropdown): Gender select
- **pet-size-input** (Dropdown): Size select
- **pet-description-input** (Textarea): Description
- **submit-pet-button** (Button): Submits new pet
- **back-to-dashboard** (Button): Back to dashboard

### 3.5 Adoption Application Page (`/adopt/<pet_id>`)
- **application-page** (Div)
- **applicant-name** (Input text): Required
- **applicant-phone** (Input text): Phone format validation
- **housing-type** (Dropdown): Housing type
- **reason** (Textarea): Reason for adoption, required
- **submit-application-button** (Button): Submits application
- **back-to-pet** (Button): Back to pet details

### 3.6 My Applications Page (`/my-applications`)
- **my-applications-page** (Div)
- **filter-status** (Dropdown): Filter status among All, Pending, Approved, Rejected
- **applications-table** (Table): Rows with application info: pet name, date, status, actions
- **back-to-dashboard** (Button): Back to dashboard

### 3.7 Favorites Page (`/favorites`)
- **favorites-page** (Div)
- **favorites-grid** (Div): Grid of favorite pet cards, clickable
- **back-to-dashboard** (Button): Back to dashboard

### 3.8 Messages Page (`/messages`)
- **messages-page** (Div)
- **conversation-list** (Div): Lists conversations, selectable
- **message-input** (Textarea): Compose message
- **send-message-button** (Button): Send message
- **back-to-dashboard** (Button): Back to dashboard

### 3.9 User Profile Page (`/profile`)
- **profile-page** (Div)
- **profile-username** (Div): Username (read-only)
- **profile-email** (Input): Editable email with validation
- **update-profile-button** (Button): Save profile changes
- **back-to-dashboard** (Button): Back to dashboard

### 3.10 Admin Panel Page (`/admin-panel`)
- **admin-panel-page** (Div)
- **pending-applications** (Div): List pending adoption applications with approve/reject buttons
- **all-pets-list** (Div): List all pets with edit/delete controls
- **back-to-dashboard** (Button): Back to dashboard

---

## 4. Data Management and CRUD Operations

All data files are located under `data/` directory. 

### 4.1 User Data - `users.txt`
- Read to authenticate users and display profile info
- Update email in profile page writes new email in line

### 4.2 Pet Data - `pets.txt`
- Read to display pets on dashboard, listings, details
- On Add Pet Page, append new pet record with unique pet_id, status 'Available', current date
- On Admin panel, edit/delete updates file accordingly

### 4.3 Adoption Applications - `applications.txt`
- Read for My Applications, Admin Pending Applications
- Submit application appends new record with status 'Pending'
- Admin approve/reject updates status in file

### 4.4 Favorites - `favorites.txt`
- Read to show favorites grid
- Adding/removing favorites updates file

### 4.5 Messages - `messages.txt`
- Read to show conversations
- Sending message appends new message with timestamp and `is_read=false`
- Marking messages as read modifies flag

### 4.6 Adoption History - `adoption_history.txt`
- Append successful adoptions
- Read to display adoption histories if needed

### 4.7 Shelters Data - `shelters.txt`
- Read to show shelter info on details or admin panel

---

## 5. Form Validation and Processing Flows

### 5.1 Add Pet Form
- Validate all required fields (name, species, gender, size)
- Age format checked (e.g. digits + " years")
- On submit: Validate -> Save pet record -> Redirect to dashboard with success message

### 5.2 Adoption Application Form
- Validate applicant name, phone (pattern), reason
- On submit: Validate -> Save application with status "Pending" -> Redirect to My Applications

### 5.3 Message Sending
- Validate non-empty message content
- On send: Append message record, update UI conversation list, clear message input

### 5.4 Profile Update
- Validate email format
- On update: Save email in file, confirm success

---

## 6. User Interaction and Messaging Workflows

### 6.1 Navigation Paths
- Dashboard main hub
- From Dashboard to Pet Listings and featured pets detail
- From Listings to Details then either to Adoption Application or back
- My Applications filtered dynamically
- Favorites clickable to pet details
- Messages: Select conversation updates displayed messages

### 6.2 Messaging Conversations
- Conversation List displays unique chat threads by user and shelter
- Selecting conversation loads messages in read/write format
- Sending message adds new message, refresh conversation

### 6.3 UI State Changes
- Multi-step adoption process: Viewing pet details, then application page
- Form submission results in page redirects with confirmation messages

---

## 7. Conclusion

This design candidate B provides a clear, structured alternative UI and backend interaction outcome for the PetAdoptionCenter application, focusing on solid user flows, robust data handling, and clear navigation schemes to support all the specified features.