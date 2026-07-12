# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                | Function Name          | HTTP Method(s) | Template File Rendered        | Context Variables (name:type)                                                                                                                    |
|---------------------------|------------------------|----------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| /                         | root_redirect          | GET            | Redirect to /dashboard        | None                                                                                                                                            |
| /dashboard                | dashboard              | GET            | dashboard.html                | featured_pets: List[Dict[str, Any]]  # List of up to 5 dictionaries representing pets with keys: id (int), name (str), species (str), age (str), photo_url (str)
| /pets                     | pet_listings           | GET            | pet_listings.html             | pets: List[Dict[str, Any]]  # All available pets with keys: id (int), name (str), species (str), age (str), photo_url (str)
| /pets                     | pet_listings_filter    | POST           | pet_listings.html             | pets: List[Dict[str, Any]]  # Filtered/sorted pets based on POST data filters
| /pets/<int:pet_id>        | pet_details            | GET            | pet_details.html              | pet: Dict[str, Any]  # Single pet detail with keys: id (int), name (str), species (str), description (str), age (str), gender (str), size (str), shelter_id (int), status (str)
| /pets/add                 | add_pet                | GET            | add_pet.html                  | None                                                                                                                                             |
| /pets/add                 | add_pet_post           | POST           | add_pet.html                  | message: str (success or error message after submission)                                                                                       |
| /applications/new/<int:pet_id>| adoption_application | GET            | adoption_application.html     | pet_id: int, pet_name: str                                                                                                                       |
| /applications/new/<int:pet_id>| submit_adoption_application | POST  | adoption_application.html     | message: str (success or error), pet_id: int, pet_name: str                                                                                      |
| /applications             | my_applications        | GET            | my_applications.html          | applications: List[Dict[str, Any]]  # User's applications with keys: application_id (int), pet_name (str), date (str), status (str)
| /favorites                | favorites              | GET            | favorites.html                | favorites: List[Dict[str, Any]]  # Favorited pets with keys: pet_id (int), name (str), species (str), age (str), photo_url (str)
| /messages                 | messages               | GET            | messages.html                 | conversations: List[Dict[str, Any]]  # List of message conversation overviews (recipient_username str, last_message:str, unread_count int)
| /messages/send            | send_message           | POST           | messages.html                 | message: str (confirmation or error)                                                                                                           |
| /profile                  | user_profile           | GET            | profile.html                  | username: str, email: str                                                                                                                       |
| /profile                  | update_profile         | POST           | profile.html                  | message: str (success or error), username: str, email: str                                                                                      |
| /admin                   | admin_panel            | GET            | admin_panel.html              | pending_applications: List[Dict[str, Any]], all_pets: List[Dict[str, Any]]                                                                     |
| /admin/applications/<int:application_id>/approve | approve_application | POST | admin_panel.html | message: str (success or failure)                                                                                                              |
| /admin/applications/<int:application_id>/reject | reject_application | POST  | admin_panel.html | message: str (success or failure)                                                                                                              |
| /admin/pets/<int:pet_id>/edit | edit_pet             | GET            | add_pet.html                  | pet: Dict[str, Any] (pet info for editing)                                                                                                     |
| /admin/pets/<int:pet_id>/edit | edit_pet_post        | POST           | add_pet.html                  | message: str (success or error)                                                                                                                  |
| /admin/pets/<int:pet_id>/delete | delete_pet         | POST           | admin_panel.html              | message: str (success or error)                                                                                                                  |

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Pet Adoption Dashboard
- IDs and Element Types:
  - dashboard-page (div)
  - featured-pets (div)
  - browse-pets-button (button)
  - back-to-dashboard (button)
- Navigation:
  - browse-pets-button: navigates to `url_for('pet_listings')`
  - back-to-dashboard: triggers page refresh via JS or links to `url_for('dashboard')`
- Context Variables:
  - featured_pets: List of dicts each with keys (id:int, name:str, species:str, age:str, photo_url:str)

---

### 2. pet_listings.html
- File Path: templates/pet_listings.html
- Page Title: Available Pets
- IDs and Element Types:
  - pet-listings-page (div)
  - search-input (input)
  - filter-species (select/dropdown)
  - pet-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
  - Each pet card inside pet-grid should have a clickable element linking to `url_for('pet_details', pet_id=pet.id)`
- Context Variables:
  - pets: List of dicts with keys (id:int, name:str, species:str, age:str, photo_url:str)

---

### 3. pet_details.html
- File Path: templates/pet_details.html
- Page Title: Pet Details
- IDs and Element Types:
  - pet-details-page (div)
  - pet-name (h1)
  - pet-species (div)
  - pet-description (div)
  - adopt-button (button)
  - back-to-listings (button)
- Navigation:
  - adopt-button: link to `url_for('adoption_application', pet_id=pet.id)`
  - back-to-listings: `url_for('pet_listings')`
- Context Variables:
  - pet: dict with keys (id:int, name:str, species:str, description:str, age:str, gender:str, size:str, shelter_id:int, status:str)

---

### 4. add_pet.html
- File Path: templates/add_pet.html
- Page Title: Add New Pet
- IDs and Element Types:
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
  - back-to-dashboard: `url_for('dashboard')`
- Context Variables:
  - message (optional): str, success or error message from submission
- Form:
  - Form method POST to `/pets/add` for submitting new pet

---

### 5. adoption_application.html
- File Path: templates/adoption_application.html
- Page Title: Adoption Application
- IDs and Element Types:
  - application-page (div)
  - applicant-name (input)
  - applicant-phone (input)
  - housing-type (select/dropdown)
  - reason (textarea)
  - submit-application-button (button)
  - back-to-pet (button)
- Navigation:
  - back-to-pet: `url_for('pet_details', pet_id=pet_id)`
- Context Variables:
  - pet_id: int
  - pet_name: str
  - message (optional): str
- Form:
  - Form method POST to `/applications/new/<pet_id>` to submit application

---

### 6. my_applications.html
- File Path: templates/my_applications.html
- Page Title: My Applications
- IDs and Element Types:
  - my-applications-page (div)
  - filter-status (select/dropdown)
  - applications-table (table)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
- Context Variables:
  - applications: List of dicts with keys (application_id:int, pet_name:str, date:str, status:str)

---

### 7. favorites.html
- File Path: templates/favorites.html
- Page Title: My Favorites
- IDs and Element Types:
  - favorites-page (div)
  - favorites-grid (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
- Context Variables:
  - favorites: List of dicts (pet_id:int, name:str, species:str, age:str, photo_url:str)

---

### 8. messages.html
- File Path: templates/messages.html
- Page Title: Messages
- IDs and Element Types:
  - messages-page (div)
  - conversation-list (div)
  - message-input (textarea)
  - send-message-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
- Context Variables:
  - conversations: List of dicts (recipient_username:str, last_message:str, unread_count:int)
- Form:
  - Form method POST to `/messages/send` to send new messages

---

### 9. profile.html
- File Path: templates/profile.html
- Page Title: My Profile
- IDs and Element Types:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
- Context Variables:
  - username: str
  - email: str
- Form:
  - Form method POST to `/profile` to update profile information

---

### 10. admin_panel.html
- File Path: templates/admin_panel.html
- Page Title: Admin Panel
- IDs and Element Types:
  - admin-panel-page (div)
  - pending-applications (div)
  - all-pets-list (div)
  - back-to-dashboard (button)
- Navigation:
  - back-to-dashboard: `url_for('dashboard')`
  - Pending application approvals/rejections: Buttons with actions POST to `/admin/applications/<application_id>/approve` and `/admin/applications/<application_id>/reject`
  - Pet edit and delete buttons each POST to `/admin/pets/<pet_id>/edit` and `/admin/pets/<pet_id>/delete` respectively
- Context Variables:
  - pending_applications: List of dicts with keys (application_id:int, applicant_name:str, pet_name:str, date_submitted:str, status:str)
  - all_pets: List of dicts with keys (pet_id:int, name:str, species:str, status:str)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited):
  - username (str): User login name
  - email (str): User email address
  - phone (str): Phone number
  - address (str): Physical address
- Example Rows:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

---

### 2. pets.txt
- Filename: data/pets.txt
- Fields (pipe-delimited):
  - pet_id (int): Unique pet identifier
  - name (str): Pet's name
  - species (str): Species (Dog, Cat, Bird, Rabbit, Other)
  - breed (str): Breed of the pet
  - age (str): Age description (e.g., "3 years")
  - gender (str): Gender (Male, Female)
  - size (str): Size (Small, Medium, Large)
  - description (str): Detailed description
  - shelter_id (int): Shelter hosting the pet
  - status (str): Availability status (Available, Pending, Adopted)
  - date_added (str): Date the pet was added (YYYY-MM-DD)
- Example Rows:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

---

### 3. applications.txt
- Filename: data/applications.txt
- Fields (pipe-delimited):
  - application_id (int): Unique id for application
  - username (str): Applicant's username
  - pet_id (int): Pet id applied for
  - applicant_name (str): Full name of applicant
  - phone (str): Applicant phone
  - address (str): Applicant address
  - housing_type (str): Type of housing (House, Apartment, etc.)
  - has_yard (str): Yes or No
  - other_pets (str): Description of other pets
  - experience (str): Experience with pets
  - reason (str): Reason for adoption
  - status (str): Application status (Pending, Approved, Rejected)
  - date_submitted (str): Date of submission (YYYY-MM-DD)
- Example Rows:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

---

### 4. favorites.txt
- Filename: data/favorites.txt
- Fields (pipe-delimited):
  - username (str): User who favorited
  - pet_id (int): ID of favorite pet
  - date_added (str): Date pet added to favorites (YYYY-MM-DD)
- Example Rows:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

---

### 5. messages.txt
- Filename: data/messages.txt
- Fields (pipe-delimited):
  - message_id (int): Unique message id
  - sender_username (str): Username of sender
  - recipient_username (str): Username of recipient
  - subject (str): Subject line
  - content (str): Message content
  - timestamp (str): Datetime stamp (YYYY-MM-DD HH:MM:SS)
  - is_read (str): "true" or "false" indicating read status
- Example Rows:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

---

### 6. adoption_history.txt
- Filename: data/adoption_history.txt
- Fields (pipe-delimited):
  - history_id (int): Unique id
  - username (str): User who adopted
  - pet_id (int): Adopted pet id
  - pet_name (str): Pet name
  - adoption_date (str): Adoption date (YYYY-MM-DD)
  - shelter_id (int): Shelter id
- Example Rows:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

---

### 7. shelters.txt
- Filename: data/shelters.txt
- Fields (pipe-delimited):
  - shelter_id (int): Unique id
  - name (str): Shelter name
  - address (str): Shelter physical address
  - phone (str): Shelter phone number
  - email (str): Shelter email address
- Example Rows:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

*End of specification*  

