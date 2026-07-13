# PetAdoptionCenter Web Application Design Specification

---

## Section 1: Page Structure and Element IDs

### 1. Dashboard Page
- Page Title: Pet Adoption Dashboard
- Container ID: dashboard-page
- Elements:
  - featured-pets (Div): Display featured pets (limit 5)
  - browse-pets-button (Button): Button to navigate to Pet Listings Page
  - back-to-dashboard (Button): Button to refresh dashboard

### 2. Pet Listings Page
- Page Title: Available Pets
- Container ID: pet-listings-page
- Elements:
  - search-input (Input): Field to search pets by name
  - filter-species (Dropdown): Dropdown to filter by species (All, Dog, Cat, Bird, Rabbit, Other)
  - pet-grid (Div): Grid displaying pet cards with photo, name, species, and age
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 3. Pet Details Page
- Page Title: Pet Details
- Container ID: pet-details-page
- Elements:
  - pet-name (H1): Display pet name
  - pet-species (Div): Display pet species
  - pet-description (Div): Display detailed description about the pet
  - adopt-button (Button): Button to start adoption application process
  - back-to-listings (Button): Button to navigate back to Pet Listings

### 4. Add Pet Page
- Page Title: Add New Pet
- Container ID: add-pet-page
- Elements:
  - pet-name-input (Input): Field to input pet name
  - pet-species-input (Dropdown): Dropdown to select species (Dog, Cat, Bird, Rabbit, Other)
  - pet-breed-input (Input): Field to input breed
  - pet-age-input (Input): Field to input age (e.g., "2 years")
  - pet-gender-input (Dropdown): Dropdown to select gender (Male, Female)
  - pet-size-input (Dropdown): Dropdown to select size (Small, Medium, Large)
  - pet-description-input (Textarea): Field to input detailed description
  - submit-pet-button (Button): Button to submit new pet listing
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 5. Adoption Application Page
- Page Title: Adoption Application
- Container ID: application-page
- Elements:
  - applicant-name (Input): Field to input applicant's full name
  - applicant-phone (Input): Field to input phone number
  - housing-type (Dropdown): Dropdown to select housing type (House, Apartment, Condo, Other)
  - reason (Textarea): Field to explain why they want to adopt this pet
  - submit-application-button (Button): Button to submit application
  - back-to-pet (Button): Button to navigate back to Pet Details

### 6. My Applications Page
- Page Title: My Applications
- Container ID: my-applications-page
- Elements:
  - filter-status (Dropdown): Dropdown to filter by status (All, Pending, Approved, Rejected)
  - applications-table (Table): Table displaying applications with pet name, date, status, and actions
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 7. Favorites Page
- Page Title: My Favorites
- Container ID: favorites-page
- Elements:
  - favorites-grid (Div): Grid displaying favorite pet cards
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 8. Messages Page
- Page Title: Messages
- Container ID: messages-page
- Elements:
  - conversation-list (Div): List of message conversations
  - message-input (Textarea): Field to compose new message
  - send-message-button (Button): Button to send message
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 9. User Profile Page
- Page Title: My Profile
- Container ID: profile-page
- Elements:
  - profile-username (Div): Display username (not editable)
  - profile-email (Input): Field to update email
  - update-profile-button (Button): Button to save profile changes
  - back-to-dashboard (Button): Button to navigate back to Dashboard

### 10. Admin Panel Page
- Page Title: Admin Panel
- Container ID: admin-panel-page
- Elements:
  - pending-applications (Div): List of pending adoption applications
  - all-pets-list (Div): List of all pets with edit/delete options
  - back-to-dashboard (Button): Button to navigate back to Dashboard

---

## Section 2: Navigation and User Workflows

### Starting Page
- The application starts at the Dashboard page with container ID "dashboard-page".

### Navigation Flows:
- Dashboard:
  - browse-pets-button -> Pet Listings Page
  - back-to-dashboard -> Refresh Dashboard Page
  - Navigation to Add Pet Page, Favorites, Messages, User Profile, Admin Panel assumed via menus or links (IDs not specified).

- Pet Listings Page:
  - Clicking pet card (no explicit element ID) -> Pet Details Page
  - back-to-dashboard -> Dashboard Page

- Pet Details Page:
  - adopt-button -> Adoption Application Page
  - back-to-listings -> Pet Listings Page

- Adoption Application Page:
  - back-to-pet -> Pet Details Page

- My Applications Page:
  - back-to-dashboard -> Dashboard Page

- Favorites Page:
  - back-to-dashboard -> Dashboard Page

- Messages Page:
  - back-to-dashboard -> Dashboard Page

- User Profile Page:
  - back-to-dashboard -> Dashboard Page

- Admin Panel Page:
  - back-to-dashboard -> Dashboard Page

### User Roles
- **User**:
  - Can browse pets, submit adoption applications, manage favorites, send messages, view and edit profile.

- **Admin**:
  - Has all user rights plus access to Add Pet Page and Admin Panel.
  - Can manage pets and applications.

Access control limits Add Pet Page and Admin Panel to Admin role only.

---

## Section 3: Local Data File Directory Structure and Formats

### Directory Structure
- All data files are stored in the "data" directory at the root of the application.

### Data Files and Formats:

1. users.txt
  - Delimiter: Pipe (|)
  - Fields: username | email | phone | address
  - Sample Line:
    john_doe|john@example.com|555-1234|123 Main St, City

2. pets.txt
  - Delimiter: Pipe (|)
  - Fields: pet_id | name | species | breed | age | gender | size | description | shelter_id | status | date_added
  - Sample Line:
    1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15

3. applications.txt
  - Delimiter: Pipe (|)
  - Fields: application_id | username | pet_id | applicant_name | phone | address | housing_type | has_yard | other_pets | experience | reason | status | date_submitted
  - Sample Line:
    1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10

4. favorites.txt
  - Delimiter: Pipe (|)
  - Fields: username | pet_id | date_added
  - Sample Line:
    john_doe|1|2024-11-01

5. messages.txt
  - Delimiter: Pipe (|)
  - Fields: message_id | sender_username | recipient_username | subject | content | timestamp | is_read
  - Sample Line:
    1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true

6. adoption_history.txt
  - Delimiter: Pipe (|)
  - Fields: history_id | username | pet_id | pet_name | adoption_date | shelter_id
  - Sample Line:
    1|jane_smith|2|Whiskers|2024-11-15|1

7. shelters.txt
  - Delimiter: Pipe (|)
  - Fields: shelter_id | name | address | phone | email
  - Sample Line:
    1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com

---

This completes the detailed design specification for the PetAdoptionCenter web application.
