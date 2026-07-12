# Design Specification for PetAdoptionCenter Web Application

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                 | Function Name           | HTTP Method | Template File           | Context Variables (Name : Type)                                                  |
|----------------------------|------------------------|-------------|-------------------------|----------------------------------------------------------------------------------|
| /                          | root_redirect           | GET         | (redirects to /dashboard) | None                                                                             |
| /dashboard                 | dashboard_page          | GET         | dashboard.html          | featured_pets : list of dict (each dict with keys: pet_id:int,name:str,species:str,age:str)  
|                            |                        |             |                         | recent_activities : list of str                                                  |
| /pets                      | pet_listings_page       | GET         | pet_listings.html       | pets : list of dict (pet_id:int,name:str,species:str,age:str,photo_url:str)      
|                            |                        |             |                         | filter_species : str (selected species filter)                                  |
| /pets/search               | pet_search              | POST        | pet_listings.html       | pets : list of dict (filtered results, pet_id:int,name:str,species:str,age:str,photo_url:str)  
|                            |                        |             |                         | filter_species : str                                                           |
| /pets/<int:pet_id>         | pet_details_page        | GET         | pet_details.html        | pet : dict (pet_id:int,name:str,species:str,breed:str,age:str,gender:str,size:str,
|                            |                        |             |                         | description:str,shelter_id:int,status:str,date_added:str)                      |
| /pets/add                  | add_pet_page            | GET         | add_pet.html            | None                                                                             |
| /pets/add                  | submit_new_pet          | POST        | add_pet.html (on error, else redirect) | form_errors : dict (field:str -> error_msg:str)                             |
| /applications/new/<int:pet_id> | adoption_application_page | GET     | adoption_application.html | pet : dict (pet_id:int,name:str)                                                |
| /applications/new/<int:pet_id> | submit_adoption_application | POST     | adoption_application.html (on error, else redirect) | form_errors : dict (field:str -> error_msg:str)  |
| /applications              | my_applications_page    | GET         | my_applications.html    | applications : list of dict (application_id:int,pet_name:str,date_submitted:str,status:str)
|                            |                        |             |                         | filter_status : str (selected status filter)                                  |
| /favorites                 | favorites_page          | GET         | favorites.html          | favorite_pets : list of dict (pet_id:int,name:str,species:str,age:str,photo_url:str)         |
| /messages                  | messages_page           | GET         | messages.html           | conversations : list of dict (conversation_id:int, with messages list),
|                            |                        |             |                         | user : dict (username:str)                                                      |
| /messages/send             | send_message            | POST        | messages.html (on error, else redirect) | form_errors : dict (field:str -> error_msg:str)                              |
| /profile                   | user_profile_page       | GET         | profile.html            | profile : dict (username:str,email:str)                                        |
| /profile                   | update_user_profile     | POST        | profile.html (on error, else redirect) | form_errors : dict (field:str -> error_msg:str)                              |
| /admin                     | admin_panel_page        | GET         | admin_panel.html        | pending_applications : list of dict (application_id:int,applicant_name:str,pet_name:str,date_submitted:str)  
|                            |                        |             |                         | all_pets : list of dict (pet_id:int,name:str,species:str,status:str)           |

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Title and H1: "Pet Adoption Dashboard"
- Elements:
  - div#dashboard-page
  - div#featured-pets
  - button#browse-pets-button
  - button#back-to-dashboard
- Navigation:
  - #browse-pets-button -> url_for('pet_listings_page')
  - #back-to-dashboard -> url_for('dashboard_page') (refresh page)
- Context Variables:
  - featured_pets: list of dict with keys pet_id:int, name:str, species:str, age:str
  - recent_activities: list of str

### 2. Pet Listings Page
- File Path: templates/pet_listings.html
- Title and H1: "Available Pets"
- Elements:
  - div#pet-listings-page
  - input#search-input
  - select#filter-species (options: All, Dog, Cat, Bird, Rabbit, Other)
  - div#pet-grid
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
  - pet cards in #pet-grid link to url_for('pet_details_page', pet_id=pet.pet_id) using Jinja2
- Context Variables:
  - pets: list of dict (pet_id:int, name:str, species:str, age:str, photo_url:str)
  - filter_species: str

### 3. Pet Details Page
- File Path: templates/pet_details.html
- Title and H1: "Pet Details"
- Elements:
  - div#pet-details-page
  - h1#pet-name
  - div#pet-species
  - div#pet-description
  - button#adopt-button
  - button#back-to-listings
- Navigation:
  - #adopt-button -> url_for('adoption_application_page', pet_id=pet.pet_id)
  - #back-to-listings -> url_for('pet_listings_page')
- Context Variables:
  - pet: dict with keys pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str,
    description:str, shelter_id:int, status:str, date_added:str

### 4. Add Pet Page
- File Path: templates/add_pet.html
- Title and H1: "Add New Pet"
- Elements:
  - div#add-pet-page
  - input#pet-name-input
  - select#pet-species-input (options: Dog, Cat, Bird, Rabbit, Other)
  - input#pet-breed-input
  - input#pet-age-input
  - select#pet-gender-input (options: Male, Female)
  - select#pet-size-input (options: Small, Medium, Large)
  - textarea#pet-description-input
  - button#submit-pet-button
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - None for GET; on POST error, form_errors dict with keys for field names to error messages

### 5. Adoption Application Page
- File Path: templates/adoption_application.html
- Title and H1: "Adoption Application"
- Elements:
  - div#application-page
  - input#applicant-name
  - input#applicant-phone
  - select#housing-type (options: House, Apartment, Condo, Other)
  - textarea#reason
  - button#submit-application-button
  - button#back-to-pet
- Navigation:
  - #back-to-pet -> url_for('pet_details_page', pet_id=pet.pet_id)
- Context Variables:
  - pet: dict with keys pet_id:int, name:str
  - on error POST: form_errors dict

### 6. My Applications Page
- File Path: templates/my_applications.html
- Title and H1: "My Applications"
- Elements:
  - div#my-applications-page
  - select#filter-status (options: All, Pending, Approved, Rejected)
  - table#applications-table (columns: pet name, date, status, actions)
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - applications: list of dict (application_id:int, pet_name:str, date_submitted:str, status:str)
  - filter_status: str

### 7. Favorites Page
- File Path: templates/favorites.html
- Title and H1: "My Favorites"
- Elements:
  - div#favorites-page
  - div#favorites-grid
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - favorite_pets: list of dict (pet_id:int, name:str, species:str, age:str, photo_url:str)

### 8. Messages Page
- File Path: templates/messages.html
- Title and H1: "Messages"
- Elements:
  - div#messages-page
  - div#conversation-list
  - textarea#message-input
  - button#send-message-button
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - conversations: list of dict (conversation_id:int, messages:list of dict with fields message_id:int,
    sender_username:str, recipient_username:str, subject:str, content:str, timestamp:str, is_read:bool)
  - user: dict (username:str)

### 9. User Profile Page
- File Path: templates/profile.html
- Title and H1: "My Profile"
- Elements:
  - div#profile-page
  - div#profile-username
  - input#profile-email
  - button#update-profile-button
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - profile: dict (username:str, email:str)

### 10. Admin Panel Page
- File Path: templates/admin_panel.html
- Title and H1: "Admin Panel"
- Elements:
  - div#admin-panel-page
  - div#pending-applications
  - div#all-pets-list
  - button#back-to-dashboard
- Navigation:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - pending_applications: list of dict (application_id:int, applicant_name:str, pet_name:str, date_submitted:str)
  - all_pets: list of dict (pet_id:int, name:str, species:str, status:str)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited): username|email|phone|address
- Field Descriptions:
  - username: str, unique user identifier
  - email: str, user email
  - phone: str, contact phone number
  - address: str, home address
- Example:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. pets.txt
- Filename: data/pets.txt
- Fields (pipe-delimited): pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
- Field Descriptions:
  - pet_id: int, unique pet identifier
  - name: str, pet's name
  - species: str, pet species
  - breed: str, breed of pet
  - age: str, age description (e.g., "3 years")
  - gender: str, gender
  - size: str, size category
  - description: str, detailed pet description
  - shelter_id: int, associated shelter identifier
  - status: str, adoption status (Available, Pending, etc.)
  - date_added: str, date pet was added (YYYY-MM-DD)
- Example:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. applications.txt
- Filename: data/applications.txt
- Fields (pipe-delimited): application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
- Field Descriptions:
  - application_id: int, unique application identifier
  - username: str, user submitting application
  - pet_id: int, pet applied for
  - applicant_name: str, full name
  - phone: str, contact number
  - address: str, residence address
  - housing_type: str, type of housing
  - has_yard: str, Yes/No whether user has a yard
  - other_pets: str, description of other pets
  - experience: str, pet experience
  - reason: str, reason for adoption
  - status: str, application status
  - date_submitted: str, submission date (YYYY-MM-DD)
- Example:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. favorites.txt
- Filename: data/favorites.txt
- Fields (pipe-delimited): username|pet_id|date_added
- Field Descriptions:
  - username: str, user who saved favorite
  - pet_id: int, pet identifier
  - date_added: str, date added to favorites (YYYY-MM-DD)
- Example:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. messages.txt
- Filename: data/messages.txt
- Fields (pipe-delimited): message_id|sender_username|recipient_username|subject|content|timestamp|is_read
- Field Descriptions:
  - message_id: int, unique message identifier
  - sender_username: str, username of sender
  - recipient_username: str, username of recipient
  - subject: str, message subject
  - content: str, message body
  - timestamp: str, datetime of message sent (YYYY-MM-DD HH:mm:ss)
  - is_read: bool, message read status (true/false)
- Example:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. adoption_history.txt
- Filename: data/adoption_history.txt
- Fields (pipe-delimited): history_id|username|pet_id|pet_name|adoption_date|shelter_id
- Field Descriptions:
  - history_id: int, unique history record identifier
  - username: str, user who adopted
  - pet_id: int, pet adopted
  - pet_name: str, pet name
  - adoption_date: str, date of adoption (YYYY-MM-DD)
  - shelter_id: int, shelter associated
- Example:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. shelters.txt
- Filename: data/shelters.txt
- Fields (pipe-delimited): shelter_id|name|address|phone|email
- Field Descriptions:
  - shelter_id: int, unique shelter identifier
  - name: str, shelter name
  - address: str, shelter address
  - phone: str, shelter contact phone
  - email: str, shelter contact email
- Example:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
  ```

---

This specification provides strict details to enable backend and frontend developers to work independently and efficiently on the PetAdoptionCenter application.
