# PetAdoptionCenter Web Application Design Specification

---

## Section 1: Page Structure and Element IDs

### 1. Dashboard Page
- Page Title: Pet Adoption Dashboard
- Container ID: dashboard-page
- Elements:
  - featured-pets (Div): Display featured pets available for adoption (limit 5)
  - browse-pets-button (Button): Navigate to Pet Listings page
  - back-to-dashboard (Button): Refresh dashboard or reload Dashboard

### 2. Pet Listings Page
- Page Title: Available Pets
- Container ID: pet-listings-page
- Elements:
  - search-input (Input): Search pets by name
  - filter-species (Dropdown): Filter by species (All, Dog, Cat, Bird, Rabbit, Other)
  - pet-grid (Div): Grid displaying pet cards with photo, name, species, and age
  - back-to-dashboard (Button): Navigate back to Dashboard

### 3. Pet Details Page
- Page Title: Pet Details
- Container ID: pet-details-page
- Elements:
  - pet-name (H1): Display selected pet's name
  - pet-species (Div): Display pet species
  - pet-description (Div): Detailed description about the pet
  - adopt-button (Button): Begin adoption application process
  - back-to-listings (Button): Navigate back to Pet Listings page

### 4. Add Pet Page
- Page Title: Add New Pet
- Container ID: add-pet-page
- Elements:
  - pet-name-input (Input): Input field for pet name
  - pet-species-input (Dropdown): Select species (Dog, Cat, Bird, Rabbit, Other)
  - pet-breed-input (Input): Input for breed
  - pet-age-input (Input): Input for age (e.g., "2 years")
  - pet-gender-input (Dropdown): Select gender (Male, Female)
  - pet-size-input (Dropdown): Select size (Small, Medium, Large)
  - pet-description-input (Textarea): Input detailed pet description
  - submit-pet-button (Button): Submit new pet listing
  - back-to-dashboard (Button): Navigate back to Dashboard

### 5. Adoption Application Page
- Page Title: Adoption Application
- Container ID: application-page
- Elements:
  - applicant-name (Input): Enter applicant's full name
  - applicant-phone (Input): Enter phone number
  - housing-type (Dropdown): Select housing type (House, Apartment, Condo, Other)
  - reason (Textarea): Explanation for wanting to adopt the pet
  - submit-application-button (Button): Submit adoption application
  - back-to-pet (Button): Navigate back to Pet Details page

### 6. My Applications Page
- Page Title: My Applications
- Container ID: my-applications-page
- Elements:
  - filter-status (Dropdown): Filter applications by status (All, Pending, Approved, Rejected)
  - applications-table (Table): Displays applications with pet name, date, status, and actions
  - back-to-dashboard (Button): Navigate back to Dashboard

### 7. Favorites Page
- Page Title: My Favorites
- Container ID: favorites-page
- Elements:
  - favorites-grid (Div): Grid displaying favorite pet cards
  - back-to-dashboard (Button): Navigate back to Dashboard

### 8. Messages Page
- Page Title: Messages
- Container ID: messages-page
- Elements:
  - conversation-list (Div): List of message conversations
  - message-input (Textarea): Compose new message field
  - send-message-button (Button): Send message
  - back-to-dashboard (Button): Navigate back to Dashboard

### 9. User Profile Page
- Page Title: My Profile
- Container ID: profile-page
- Elements:
  - profile-username (Div): Display username (read-only)
  - profile-email (Input): Edit email address
  - update-profile-button (Button): Save profile changes
  - back-to-dashboard (Button): Navigate back to Dashboard

### 10. Admin Panel Page
- Page Title: Admin Panel
- Container ID: admin-panel-page
- Elements:
  - pending-applications (Div): List of pending adoption applications
  - all-pets-list (Div): List of all pets with edit/delete options
  - back-to-dashboard (Button): Navigate back to Dashboard

---

## Section 2: Navigation and User Workflows

- Starting page is Dashboard (dashboard-page).

- Navigation from Dashboard:
  - browse-pets-button: Pet Listings page (pet-listings-page)
  - back-to-dashboard buttons on other pages return here

- From Pet Listings:
  - Selecting a pet card navigates to Pet Details page (pet-details-page)
  - back-to-dashboard returns to Dashboard

- From Pet Details:
  - adopt-button navigates to Adoption Application page (application-page)
  - back-to-listings navigates back to Pet Listings

- From Add Pet:
  - submit-pet-button submits a new pet and returns to Dashboard
  - back-to-dashboard returns to Dashboard

- From Adoption Application:
  - submit-application-button submits the adoption application and then returns to Dashboard or confirmation
  - back-to-pet returns to Pet Details page

- From My Applications:
  - back-to-dashboard returns to Dashboard

- From Favorites:
  - back-to-dashboard returns to Dashboard

- From Messages:
  - back-to-dashboard returns to Dashboard

- From User Profile:
  - update-profile-button saves profile changes
  - back-to-dashboard returns to Dashboard

- From Admin Panel:
  - back-to-dashboard returns to Dashboard

### User Roles and Access

- **Regular Users:**
  - Browse pets, submit adoption applications, manage favorites, send/receive messages, edit profile.

- **Shelter Administrators:**
  - Access Add Pet page and Admin Panel.
  - Manage pets listings and adoption applications.

- Access to Add Pet and Admin Panel pages restricted to administrators.

---

## Section 3: Local Data File Formats

All data files stored in the `data/` directory.

### 1. User Data
- File: `users.txt`
- Format: `username|email|phone|address`
- Example:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pet Data
- File: `pets.txt`
- Format: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Example:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- File: `applications.txt`
- Format: `application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted`
- Example:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- File: `favorites.txt`
- Format: `username|pet_id|date_added`
- Example:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- File: `messages.txt`
- Format: `message_id|sender_username|recipient_username|subject|content|timestamp|is_read`
- Example:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- File: `adoption_history.txt`
- Format: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`
- Example:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- File: `shelters.txt`
- Format: `shelter_id|name|address|phone|email`
- Example:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This document provides a comprehensive design specification covering all 10 pages with exact element IDs, the navigation flows including user role-based access, and detailed local text file formats for the 'PetAdoptionCenter' application.
