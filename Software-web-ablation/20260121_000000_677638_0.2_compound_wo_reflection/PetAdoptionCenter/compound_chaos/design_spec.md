# PetAdoptionCenter Web Application Design Specification

---

## Section 1: Flask Routes

### Route List:

1. `/`  
   - Function: dashboard_page  
   - Method: GET  
   - Description: Render the main adoption dashboard page showing featured pets, activities, and navigation.

2. `/listings`  
   - Function: listings_page  
   - Method: GET  
   - Description: Display all available pets with filtering options by species.

3. `/pet/<int:pet_id>`  
   - Function: pet_details  
   - Method: GET  
   - Description: Show detailed information about a specific pet.

4. `/add-pet`  
   - Function: add_pet_page  
   - Method: GET  
   - Description: Render the page for shelter administrators to add new pets.

5. `/add-pet`  
   - Function: submit_new_pet  
   - Method: POST  
   - Description: Handle form submission to add a new pet to the shelter.

6. `/adoption-application`  
   - Function: adoption_application_page  
   - Method: GET  
   - Description: Display the application form for users to adopt a pet.

7. `/adoption-application`  
   - Function: submit_adoption_application  
   - Method: POST  
   - Description: Process the submitted adoption applications.

8. `/my-applications`  
   - Function: my_applications_page  
   - Method: GET  
   - Description: Display the current user's adoption applications with filtering by status.

9. `/favorites`  
   - Function: favorites_page  
   - Method: GET  
   - Description: Show the user's favorite pets list.

10. `/messages`  
    - Function: messages_page  
    - Method: GET  
    - Description: Display user messages and provide interface to send messages.

11. `/send-message`  
    - Function: send_message  
    - Method: POST  
    - Description: Process sending a new message.

12. `/profile`  
    - Function: profile_page  
    - Method: GET  
    - Description: Show user profile details.

13. `/profile`  
    - Function: update_profile  
    - Method: POST  
    - Description: Process updates to user profile information.

14. `/admin`  
    - Function: admin_dashboard  
    - Method: GET  
    - Description: Admin dashboard showing pending applications and all pets.

15. `/admin/approve/<int:application_id>`  
    - Function: approve_application  
    - Method: POST  
    - Description: Admin approves an adoption application.

16. `/admin/reject/<int:application_id>`  
    - Function: reject_application  
    - Method: POST  
    - Description: Admin rejects an adoption application.

---

## Section 2: HTML Template Specifications

### Templates Overview

Templates are located in `templates/` directory. Key templates include:

- `dashboard.html`  
- `listings.html`  
- `pet_details.html`  
- `add_pet.html`  
- `adoption_application.html`  
- `my_applications.html`  
- `favorites.html`  
- `messages.html`  
- `profile.html`  
- `admin_dashboard.html`

---

### Template: `dashboard.html`

- Title: "Pet Adoption Dashboard"
- Layout:
  - Featured pets list (div id: featured-pets) limited to featured pets.
  - Navigation buttons (id: back-to-dashboard, add navigation via Jinja2 macros/functions).
  - Dynamic elements use Jinja2 syntax for iteration and conditionals.

### Template: `listings.html`

- Title: "Pet Listings"
- Elements:
  - Search input (id: search-input)
  - Species filter dropdown (id: filter-species), options: Cat, Dog, Other
  - Pet listings container (id: pet-listings) displaying pet entries dynamically.
  - Button with id: back-to-dashboard for navigation.

### Template: `pet_details.html`

- Title: "Pet Details"
- Displays detailed info:
  - Pet name (id: pet-name, displayed in H1)
  - Species (id: pet-species)
  - Description (id: pet-description)
  - Adopt button (id: adopt-button)
  - Back to listings button (id: back-to-listings)

### Template: `add_pet.html`

- Title: "Add New Pet"
- Form inputs include:
  - Pet name input (id: pet-name-input)
  - Species dropdown (id: species-select) with options Dog, Cat, Other
  - Age input (id: age-input)
  - Breed input (id: breed-input)
  - Size dropdown (id: size-select) options Small, Medium, Large
  - Description textarea (id: description-input)
  - Submit button (id: submit-pet-button)
  - Button to return to dashboard (id: back-to-dashboard)

### Template: `adoption_application.html`

- Title: "Adoption Application"
- Form elements:
  - Applicant name input (id: applicant-name)
  - Applicant phone input (id: applicant-phone)
  - Housing type dropdown (id: housing-type) with options House, Apartment, Other
  - Reason textarea (id: reason)
  - Submit button (id: submit-application-button)
  - Button to go back to pet details (id: back-to-pet)

### Template: `my_applications.html`

- Title: "My Applications"
- Elements:
  - Filter dropdown by status (id: filter-status) with options All, Pending, Approved, Rejected
  - List or table of applications (id: applications-list) with columns for pet name, date, status, and actions
  - Button to go back to dashboard (id: back-to-dashboard)

### Template: `favorites.html`

- Title: "My Favorites"
- Container (id: favorites-container) to list favorite pets with details
- Button to return to dashboard (id: back-to-dashboard)

### Template: `messages.html`

- Title: "Messages"
- Messages list container (id: messages-container)
- Input field for new message (id: new-message-input)
- Send button (id: send-message-button)
- Button to return to dashboard (id: back-to-dashboard)

### Template: `profile.html`

- Title: "User Profile"
- Display username (id: profile-username)
- Display email (id: profile-email)
- Save changes button (id: save-profile-button)
- Button to return to dashboard (id: back-to-dashboard)

### Template: `admin_dashboard.html`

- Title: "Admin Dashboard"
- Sections:
  - Pending adoption applications (div id: pending-applications)
  - All pets list (div id: all-pets-list)
  - Approve/reject buttons associated with each application

---

## Section 3: Data Specifications (Backend)

### 1. File: `users.txt`
- Format: Pipe delimited
- Fields: `username|email|phone|address|housing_type|has_pets|pets_description`
- Example row:
```
jane_smith|jane@example.com|555-5678|789 Shelter Ave|House|Yes|One cat
```

### 2. File: `pets.txt`
- Format: Pipe delimited
- Fields: `pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added`
- Example row:
```
3|Charlie|Dog|Beagle|5|Male|Medium|Affectionate senior dog great with children.|1|Pending|2024-10-20
```

### 3. File: `applications.txt`
- Format: Pipe delimited
- Fields: `application_id|username|pet_id|pet_name|status|application_date`
- Example row:
```
2|jane_smith|3|Charlie|Approved|2024-11-05
```

### 4. File: `favorites.txt`
- Format: Pipe delimited
- Fields: `username|pet_id|date_added`
- Example row:
```
john_doe|1|2024-11-01
```

### 5. File: `messages.txt`
- Format: Pipe delimited
- Fields: `message_id|sender|receiver|message|date_sent`
- Example row:
```
1|john_doe|admin_user|Question about Buddy? |2024-11-10
```

### 6. File: `history.txt`
- Format: Pipe delimited
- Fields: `history_id|username|pet_id|pet_name|adoption_date|shelter_id`

### 7. File: `shelters.txt`
- Format: Pipe delimited
- Fields: `shelter_id|name|address|phone|email`
- Example row:
```
1|Happy Paws Shelter|100 Shelter Road|200-385-xxxx|info@happypaws.org
```

---

# Notes:
- All data parsed and handled on backend using these specifications.
- Frontend templates utilize Jinja2 for dynamic data rendering and navigation using url_for and macros.
- All forms submitting data to backend via POST where applicable.
- All variable names are precisely typed in the codebase, e.g., pet_id: int, username: str, application_date: date string YYYY-MM-DD.

---

End of Design Specification.
