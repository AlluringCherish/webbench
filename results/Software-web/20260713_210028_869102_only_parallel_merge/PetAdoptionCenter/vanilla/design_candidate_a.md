# PetAdoptionCenter Design Candidate A

---

## 1. Overview
This design candidate document provides a comprehensive design proposal for the 'PetAdoptionCenter' Python Flask web application. It covers all 10 pages with routes, element IDs, navigation flows, data file usage, CRUD operations, and communication flows based on the detailed user task description.

---

## 2. Pages, Routes, and Titles

| Page # | Route                | Page Title             |
|--------|----------------------|------------------------|
| 1      | /dashboard           | Pet Adoption Dashboard |
| 2      | /pets                | Available Pets         |
| 3      | /pet/<pet_id>        | Pet Details            |
| 4      | /add-pet             | Add New Pet            |
| 5      | /application/<pet_id>| Adoption Application   |
| 6      | /my-applications     | My Applications        |
| 7      | /favorites           | My Favorites           |
| 8      | /messages            | Messages               |
| 9      | /profile             | My Profile             |
| 10     | /admin               | Admin Panel            |

---

## 3. Page Elements and Structure

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Title:** Pet Adoption Dashboard
- **Elements:**
  - Div: `dashboard-page` (Container for dashboard page)
  - Div: `featured-pets` (Shows up to 5 featured pets available for adoption)
  - Button: `browse-pets-button` (Navigates to `/pets`)
  - Button: `back-to-dashboard` (Refreshes current dashboard page)

### 2. Pet Listings Page
- **Route:** `/pets`
- **Title:** Available Pets
- **Elements:**
  - Div: `pet-listings-page` (Container)
  - Input: `search-input` (Text field for pet name search)
  - Dropdown: `filter-species` (Filters species: All, Dog, Cat, Bird, Rabbit, Other)
  - Div: `pet-grid` (Grid display of pet cards showing photo, name, species, age)
  - Button: `back-to-dashboard` (Navigates to `/dashboard`)

### 3. Pet Details Page
- **Route:** `/pet/<pet_id>`
- **Title:** Pet Details
- **Elements:**
  - Div: `pet-details-page` (Container)
  - H1: `pet-name` (Pet name)
  - Div: `pet-species` (Pet species)
  - Div: `pet-description` (Detailed pet description)
  - Button: `adopt-button` (Starts adoption application; navigates to `/application/<pet_id>`)
  - Button: `back-to-listings` (Navigates to `/pets`)

### 4. Add Pet Page
- **Route:** `/add-pet`
- **Title:** Add New Pet
- **Elements:**
  - Div: `add-pet-page` (Container)
  - Input: `pet-name-input` (Input pet name)
  - Dropdown: `pet-species-input` (Select species: Dog, Cat, Bird, Rabbit, Other)
  - Input: `pet-breed-input` (Input breed)
  - Input: `pet-age-input` (Input age, e.g., "2 years")
  - Dropdown: `pet-gender-input` (Select gender: Male, Female)
  - Dropdown: `pet-size-input` (Select size: Small, Medium, Large)
  - Textarea: `pet-description-input` (Input detailed description)
  - Button: `submit-pet-button` (Submits new pet data to persist)
  - Button: `back-to-dashboard` (Navigates to `/dashboard`)

### 5. Adoption Application Page
- **Route:** `/application/<pet_id>`
- **Title:** Adoption Application
- **Elements:**
  - Div: `application-page` (Container)
  - Input: `applicant-name` (Applicant full name)
  - Input: `applicant-phone` (Phone number)
  - Dropdown: `housing-type` (Select housing: House, Apartment, Condo, Other)
  - Textarea: `reason` (Explain reason to adopt)
  - Button: `submit-application-button` (Submit adoption application)
  - Button: `back-to-pet` (Navigate back to `/pet/<pet_id>`)

### 6. My Applications Page
- **Route:** `/my-applications`
- **Title:** My Applications
- **Elements:**
  - Div: `my-applications-page` (Container)
  - Dropdown: `filter-status` (Filter applications by status: All, Pending, Approved, Rejected)
  - Table: `applications-table` (Columns: pet name, date, status, actions)
  - Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 7. Favorites Page
- **Route:** `/favorites`
- **Title:** My Favorites
- **Elements:**
  - Div: `favorites-page` (Container)
  - Div: `favorites-grid` (Grid of favorite pet cards)
  - Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 8. Messages Page
- **Route:** `/messages`
- **Title:** Messages
- **Elements:**
  - Div: `messages-page` (Container)
  - Div: `conversation-list` (List of message conversations)
  - Textarea: `message-input` (Compose new message)
  - Button: `send-message-button` (Send message)
  - Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 9. User Profile Page
- **Route:** `/profile`
- **Title:** My Profile
- **Elements:**
  - Div: `profile-page` (Container)
  - Div: `profile-username` (Username displayed, read-only)
  - Input: `profile-email` (Update email address)
  - Button: `update-profile-button` (Save profile updates)
  - Button: `back-to-dashboard` (Navigate to `/dashboard`)

### 10. Admin Panel Page
- **Route:** `/admin`
- **Title:** Admin Panel
- **Elements:**
  - Div: `admin-panel-page` (Container)
  - Div: `pending-applications` (List of pending adoption applications with action options)
  - Div: `all-pets-list` (List of all pets with edit/delete controls)
  - Button: `back-to-dashboard` (Navigate to `/dashboard`)

---

## 4. Navigation and User Interaction Flows

1. **Dashboard to Pet Listings:** Clicking `browse-pets-button` navigates from `/dashboard` to `/pets`.
2. **Pet Listings to Pet Details:** Clicking a pet card in `pet-grid` navigates to `/pet/<pet_id>`.
3. **Pet Details to Adoption Application:** Clicking `adopt-button` navigates to `/application/<pet_id>`.
4. **Adoption Application Submission:** Clicking `submit-application-button` submits application data and redirects to `/my-applications` page.
5. **Back Buttons:** Buttons named `back-to-dashboard`, `back-to-listings`, or `back-to-pet` navigate respectively to `/dashboard`, `/pets`, or `/pet/<pet_id>`.
6. **Favorites:** User may add pets to favorites from `pet-details-page` (not explicitly listed but implied) and view them at `/favorites`.
7. **Messages:** From any page, user can navigate to `/messages` (not shown in buttons but can be included in header navigation).
8. **Add Pet:** Accessible to admin from `/dashboard` or `/admin` to `/add-pet`.
9. **Admin Panel:** Admin accesses `/admin` to manage pets and applications.

---

## 5. Data File Usage and CRUD Summary

| Page                    | Data Files Used                              | CRUD Actions                             |
|-------------------------|---------------------------------------------|-----------------------------------------|
| Dashboard               | `pets.txt`                                 | Read — retrieve featured pets           |
| Pet Listings            | `pets.txt`                                 | Read — list all available pets; filter species
| Pet Details             | `pets.txt`                                 | Read — detailed pet info                  |
| Add Pet                 | `pets.txt`                                 | Create — add new pet record               |
| Adoption Application    | `applications.txt`                         | Create — new application record          |
| My Applications         | `applications.txt`                         | Read — filter by username and status     |
| Favorites               | `favorites.txt`, `pets.txt`                | Read/Update — read favorites, add/remove favorites |
| Messages                | `messages.txt`                             | Read/Write — send and receive messages   |
| User Profile            | `users.txt`                               | Read/Update — user info editing           |
| Admin Panel             | `applications.txt`, `pets.txt`             | Read (all applications, pets), Update (application status), Delete/Edit pets |

### Notes on CRUD by Data File

- **users.txt:** Read user info on profile; update email.
- **pets.txt:** Read pet details, update pet status (e.g., Available, Pending), add new pets, delete or edit pets by admin.
- **applications.txt:** Read applications for user/admin; create new on application submission; update application status in admin.
- **favorites.txt:** Users' favorite pets read and updated (add/remove).
- **messages.txt:** Read conversations; append new messages with sender/recipient.
- **adoption_history.txt:** Used by admin to view historic adoptions; no direct user CRUD.
- **shelters.txt:** Used to display shelter info (may be in admin or pet data).

---

## 6. Communication Flows

- Users send messages to shelters or admin:
  - Message consists of: sender_username, recipient_username (typically shelter or admin), subject, content, timestamp, and is_read flag.
  - Sending is done via `send-message-button` on Messages Page.
- Messages stored in `messages.txt` with a unique message_id.
- Receiving messages: Displayed in `conversation-list` by messages exchanged with selected recipient.
- Mark messages as read when user views conversation.

---

## 7. Summary

This design candidate comprehensively maps all pages described, with exact element IDs and types, routes, detailed navigation flows, data operations aligned with the prescribed text file schema, and communication patterns through messaging. The design supports roles for general users, shelter administrators, and site admins, providing a clear modular structure for development.

---

*End of Design Candidate A*
