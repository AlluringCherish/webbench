# PetAdoptionCenter Unified Design Specification

---

## 1. Overview

This unified design specification consolidates the best elements from Design Candidate A and B for the PetAdoptionCenter Python Flask web application. It provides a clear, actionable, and unambiguous blueprint for developers ensuring consistency of routes, element IDs, user flows, data interactions, and UI structures across all 10 application pages.

---

## 2. Pages, Routes, and Titles

| Page # | Route                 | Page Title             |
|--------|-----------------------|------------------------|
| 1      | `/dashboard`          | Pet Adoption Dashboard |
| 2      | `/pets`               | Available Pets         |
| 3      | `/pets/<pet_id>`      | Pet Details            |
| 4      | `/add-pet`            | Add New Pet            |
| 5      | `/adopt/<pet_id>`     | Adoption Application   |
| 6      | `/my-applications`    | My Applications        |
| 7      | `/favorites`          | My Favorites           |
| 8      | `/messages`           | Messages               |
| 9      | `/profile`            | My Profile             |
| 10     | `/admin-panel`        | Admin Panel            |

*Rationale: The routes reflect candidate B's clearer and RESTful route style for pet details `/pets/<pet_id>` and adoption application `/adopt/<pet_id>`. The admin panel route from candidate B `/admin-panel` is used for consistency.*

---

## 3. Page Elements and Structure

### 3.1 Dashboard Page (`/dashboard`)
- Div: `dashboard-page` (Container for dashboard page)
- Div: `featured-pets` (Up to 5 featured pets with clickable cards linked to `/pets/<pet_id>`)
- Button: `browse-pets-button` (Navigates to `/pets`)
- Button: `back-to-dashboard` (Refreshes `/dashboard`)

### 3.2 Pet Listings Page (`/pets`)
- Div: `pet-listings-page` (Container)
- Input: `search-input` (Text input to search pets by name)
- Dropdown: `filter-species` (Species filter: All, Dog, Cat, Bird, Rabbit, Other)
- Div: `pet-grid` (Grid display of clickable pet cards linking to `/pets/<pet_id>` , showing photo, name, species, age)
- Button: `back-to-dashboard` (Navigates to `/dashboard`)

### 3.3 Pet Details Page (`/pets/<pet_id>`)
- Div: `pet-details-page` (Container)
- H1: `pet-name` (Pet name)
- Div: `pet-species` (Species display)
- Div: `pet-description` (Detailed description)
- Button: `adopt-button` (Navigates to `/adopt/<pet_id>` to start application)
- Button: `back-to-listings` (Navigates to `/pets`)

*Note: Ability to add/remove pet to/from favorites from this page is an implied feature and should be implemented accordingly.*

### 3.4 Add Pet Page (`/add-pet`)
- Div: `add-pet-page` (Container)
- Input: `pet-name-input` (Pet name, required)
- Dropdown: `pet-species-input` (Species selection)
- Input: `pet-breed-input` (Breed input)
- Input: `pet-age-input` (Age input, format validated, e.g., "2 years")
- Dropdown: `pet-gender-input` (Gender selection: Male, Female)
- Dropdown: `pet-size-input` (Size selection: Small, Medium, Large)
- Textarea: `pet-description-input` (Detailed description)
- Button: `submit-pet-button` (Form submission)
- Button: `back-to-dashboard` (Navigate back to `/dashboard`)

### 3.5 Adoption Application Page (`/adopt/<pet_id>`)
- Div: `application-page` (Container)
- Input: `applicant-name` (Required)
- Input: `applicant-phone` (Phone input with format validation)
- Dropdown: `housing-type` (Housing type: House, Apartment, Condo, Other)
- Textarea: `reason` (Reason for adoption, required)
- Button: `submit-application-button` (Form submission)
- Button: `back-to-pet` (Navigates back to `/pets/<pet_id>`)

### 3.6 My Applications Page (`/my-applications`)
- Div: `my-applications-page` (Container)
- Dropdown: `filter-status` (Filter by status: All, Pending, Approved, Rejected)
- Table: `applications-table` (Columns: pet name, date, status, actions)
- Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 3.7 Favorites Page (`/favorites`)
- Div: `favorites-page` (Container)
- Div: `favorites-grid` (Grid of clickable favorite pet cards linking to `/pets/<pet_id>`)
- Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 3.8 Messages Page (`/messages`)
- Div: `messages-page` (Container)
- Div: `conversation-list` (List of message conversations, selectable to view)
- Textarea: `message-input` (Compose message area)
- Button: `send-message-button` (Send message)
- Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 3.9 User Profile Page (`/profile`)
- Div: `profile-page` (Container)
- Div: `profile-username` (Display username, read-only)
- Input: `profile-email` (Editable, with validation)
- Button: `update-profile-button` (Save changes)
- Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 3.10 Admin Panel Page (`/admin-panel`)
- Div: `admin-panel-page` (Container)
- Div: `pending-applications` (List pending adoption applications with approve/reject controls)
- Div: `all-pets-list` (List all pets with edit and delete controls)
- Button: `back-to-dashboard` (Navigate to `/dashboard`)

---

## 4. Navigation and User Interaction Flows

1. From **Dashboard**:
   - `browse-pets-button` navigates to `/pets`.
   - `back-to-dashboard` refreshes `/dashboard`.

2. From **Pet Listings** (`/pets`):
   - Clicking pet cards in `pet-grid` navigates to `/pets/<pet_id>`.
   - `back-to-dashboard` navigates to `/dashboard`.

3. From **Pet Details** (`/pets/<pet_id>`):
   - `adopt-button` navigates to `/adopt/<pet_id>`.
   - `back-to-listings` navigates to `/pets`.
   - Optionally add/remove pet to/from favorites (UI button to be implemented).

4. From **Adoption Application** (`/adopt/<pet_id>`):
   - `submit-application-button` submits adoption application; on success redirects to `/my-applications`.
   - `back-to-pet` navigates to `/pets/<pet_id>`.

5. From **My Applications** (`/my-applications`):
   - Filtering by `filter-status` reloads table accordingly.
   - `back-to-dashboard` navigates to `/dashboard`.

6. From **Favorites** (`/favorites`):
   - Clicking favorite pet cards navigates to `/pets/<pet_id>`.
   - `back-to-dashboard` navigates to `/dashboard`.

7. From **Messages** (`/messages`):
   - Selecting a conversation from `conversation-list` loads the specific chat.
   - `send-message-button` sends the composed message.
   - `back-to-dashboard` navigates to `/dashboard`.

8. From **User Profile** (`/profile`):
   - `update-profile-button` submits profile updates.
   - `back-to-dashboard` navigates to `/dashboard`.

9. From **Admin Panel** (`/admin-panel`):
   - Admin manages applications, pets.
   - Admin can navigate to `/add-pet` to add new pets.
   - `back-to-dashboard` navigates to `/dashboard`.

---

## 5. Data File Usage and CRUD Operations

| Page                  | Data Files                        | CRUD Actions                                         |
|-----------------------|---------------------------------|-----------------------------------------------------|
| Dashboard             | `pets.txt`                      | Read for retrieving featured pets                    |
| Pet Listings          | `pets.txt`                      | Read to list available pets; filtering by species    |
| Pet Details           | `pets.txt`                      | Read detailed pet information                         |
| Add Pet               | `pets.txt`                      | Create new pet record                                 |
| Adoption Application  | `applications.txt`              | Create new application                                |
| My Applications       | `applications.txt`              | Read filtered by user and status                      |
| Favorites             | `favorites.txt`, `pets.txt`     | Read and update for favorites add/remove pet         |
| Messages              | `messages.txt`                  | Read and write messages                               |
| User Profile          | `users.txt`                    | Read and update user profile info (email updates)   |
| Admin Panel           | `applications.txt`, `pets.txt`  | Read all applications and pets; update status; edit/delete pets |

### Data File Notes:
- `users.txt`: Stores username, email, phone, and address; supports reading and email updates.
- `pets.txt`: Stores detailed pet info including status; supports create, update, delete.
- `applications.txt`: Stores application details including status; supports create and status updates.
- `favorites.txt`: Records user favorite pets; supports add/remove operations.
- `messages.txt`: Stores messages with unique IDs, sender, recipient, subject, content, timestamp, and read status; supports messaging flows.
- `adoption_history.txt`: Contains historic adoption records; appended to by admin.
- `shelters.txt`: Contains shelter info, read by admins and for pet details display where relevant.

---

## 6. Communication Flows

- Users may send messages to shelters or administrators.
  - Message data: `message_id`, `sender_username`, `recipient_username`, `subject`, `content`, `timestamp`, and `is_read` flag.
  - Sending performed by `send-message-button` on Messages Page.
  - Messages saved in `messages.txt` file.
  - Received messages displayed in the `conversation-list` UI.
  - Messages marked as read upon viewing a conversation.

---

## 7. Form Validation and Data Processing

- **Add Pet Form:** Validate required fields (name, species, gender, size), age format checked (digits + " years"), on success append new pet with unique ID, status "Available", and current date; redirect to dashboard with confirmation.

- **Adoption Application Form:** Validate required fields (applicant name, phone format, reason); on success append new application with status "Pending"; redirect to My Applications.

- **Message Sending:** Validate non-empty content; append new message with timestamp and `is_read=false`; update UI.

- **Profile Update:** Validate email format; save updated email in `users.txt`; confirm success.

---

## 8. Assumptions and Conflict Resolutions

- Routes from Candidate B chosen as canonical for consistency and RESTfulness (e.g., `/pets/<pet_id>`, `/adopt/<pet_id>`, `/admin-panel`).
- Element IDs are unified and consistent across pages; only singular instances per page are allowed.
- Navigation button IDs and their functions standardized for clarity and ease of implementation.
- Favorites addition/removal on pet details page is an implicit needed feature, recommended for implementation though not specifically enumerated.
- Data file structure and CRUD responsibilities follow Candidate B's expanded descriptions aligned with Candidate A's summary.
- Message storage and communication flows are consistent and detailed with unique message_id usage.

---

## 9. Summary

This unified design specification provides developers with complete, detailed, and coherent guidance covering all user interface elements, page routes, navigation logic, data management, CRUD operations, and communication flows. It is ready for direct implementation in the Python Flask web application for PetAdoptionCenter.

---

*End of Unified Design Specification*