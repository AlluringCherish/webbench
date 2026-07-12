# PetAdoptionCenter Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path                    | Function Name              | HTTP Method  | Template Rendered          | Context Variables (Name : Type)                                                                                      |
|------------------------------|----------------------------|--------------|----------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect               | GET          | Redirect to /dashboard      | None                                                                                                                |
| /dashboard                   | dashboard                  | GET          | dashboard.html             | featured_pets : list of Dict (Each dict with keys: 'pet_id': int, 'name': str, 'species': str, 'age': str)           |
|                              |                            |              |                            | recent_activities : list of str                                                                                      |
| /pets                       | pet_listings               | GET          | pet_listings.html          | pets : list of Dict (Each dict with keys: 'pet_id': int, 'name': str, 'species': str, 'age': str, 'photo_url': str)   |
|                              |                            |              |                            | species_filter_options : list of str (['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other'])                             |
| /pets/<int:pet_id>           | pet_details                | GET          | pet_details.html           | pet : Dict (keys: 'pet_id': int, 'name': str, 'species': str, 'breed': str, 'age': str, 'gender': str, 'size': str,     |
|                              |                            |              |                            | 'description': str, 'status': str)                                                                                   |
| /add-pet                    | add_pet                   | GET          | add_pet.html               | species_options : list of str (['Dog', 'Cat', 'Bird', 'Rabbit', 'Other'])                                            |
| /add-pet                    | submit_pet                | POST         | add_pet.html (on validation)| success : bool, error_message : str (only if success false)                                                        |
| /apply/<int:pet_id>          | adoption_application       | GET          | application.html           | pet : Dict (keys as in pet_details)                                                                                  |
| /apply/<int:pet_id>          | submit_application         | POST         | application.html           | success : bool, error_message : str (only if success false)                                                        |
| /my-applications             | my_applications            | GET          | my_applications.html       | applications : list of Dict (keys: 'application_id': int, 'pet_name': str, 'date': str, 'status': str)                |
|                              |                            |              |                            | status_filter_options : list of str (['All', 'Pending', 'Approved', 'Rejected'])                                     |
| /favorites                  | favorites                  | GET          | favorites.html             | favorite_pets : list of Dict (keys as in pet_details)                                                               |
| /messages                   | messages                  | GET          | messages.html              | conversations : list of Dict (keys: 'conversation_id': int, 'participants': list of str, 'last_message': str)        |
| /messages/send              | send_message              | POST         | messages.html              | success : bool, error_message : str (only if success false)                                                        |
| /profile                   | user_profile              | GET          | profile.html               | username : str, email : str                                                                                         |
| /profile                   | update_profile            | POST         | profile.html               | success : bool, error_message : str (only if success false)                                                        |
| /admin                     | admin_panel               | GET          | admin_panel.html           | pending_applications : list of Dict (keys: 'application_id': int, 'applicant_name': str, 'pet_name': str, 'date': str,|
|                              |                            |              |                            | 'status': str), all_pets : list of Dict (keys as in pet_details)                                                     |

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title (for <title> and <h1>): Pet Adoption Dashboard
- Element IDs and Types:
  - dashboard-page : div
  - featured-pets : div
  - browse-pets-button : button
  - back-to-dashboard : button
- Navigation:
  - browse-pets-button: Navigates to pet listings page via `url_for('pet_listings')`
  - back-to-dashboard: Refreshes dashboard via `url_for('dashboard')`
- Context Variables:
  - featured_pets: list of dicts with keys 'pet_id' (int), 'name' (str), 'species' (str), 'age' (str)
  - recent_activities: list of str

### 2. Pet Listings Page
- File Path: templates/pet_listings.html
- Page Title: Available Pets
- Element IDs and Types:
  - pet-listings-page : div
  - search-input : input
  - filter-species : select (dropdown)
  - pet-grid : div
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
  - Dynamic pet details link on each pet card using `url_for('pet_details', pet_id=pet.pet_id)`
- Context Variables:
  - pets: list of dicts with keys 'pet_id' (int), 'name' (str), 'species' (str), 'age' (str), 'photo_url' (str)
  - species_filter_options: list of str

### 3. Pet Details Page
- File Path: templates/pet_details.html
- Page Title: Pet Details
- Element IDs and Types:
  - pet-details-page : div
  - pet-name : h1
  - pet-species : div
  - pet-description : div
  - adopt-button : button
  - back-to-listings : button
- Navigation:
  - adopt-button: Navigates to adoption application page via `url_for('adoption_application', pet_id=pet.pet_id)`
  - back-to-listings: Navigates back to pet listings via `url_for('pet_listings')`
- Context Variables:
  - pet: dict with keys 'pet_id' (int), 'name' (str), 'species' (str), 'breed' (str), 'age' (str), 'gender' (str), 'size' (str), 'description' (str), 'status' (str)

### 4. Add Pet Page
- File Path: templates/add_pet.html
- Page Title: Add New Pet
- Element IDs and Types:
  - add-pet-page : div
  - pet-name-input : input
  - pet-species-input : select (dropdown)
  - pet-breed-input : input
  - pet-age-input : input
  - pet-gender-input : select (dropdown)
  - pet-size-input : select (dropdown)
  - pet-description-input : textarea
  - submit-pet-button : button
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - species_options: list of str ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']

### 5. Adoption Application Page
- File Path: templates/application.html
- Page Title: Adoption Application
- Element IDs and Types:
  - application-page : div
  - applicant-name : input
  - applicant-phone : input
  - housing-type : select (dropdown)
  - reason : textarea
  - submit-application-button : button
  - back-to-pet : button
- Navigation:
  - back-to-pet: Navigates back to pet details via `url_for('pet_details', pet_id=pet.pet_id)`
- Context Variables:
  - pet: dict with keys 'pet_id' (int), 'name' (str), 'species' (str), 'breed' (str), 'age' (str), 'gender' (str), 'size' (str), 'description' (str), 'status' (str)

### 6. My Applications Page
- File Path: templates/my_applications.html
- Page Title: My Applications
- Element IDs and Types:
  - my-applications-page : div
  - filter-status : select (dropdown)
  - applications-table : table
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - applications: list of dicts with keys 'application_id' (int), 'pet_name' (str), 'date' (str), 'status' (str)
  - status_filter_options: list of str ['All', 'Pending', 'Approved', 'Rejected']

### 7. Favorites Page
- File Path: templates/favorites.html
- Page Title: My Favorites
- Element IDs and Types:
  - favorites-page : div
  - favorites-grid : div
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - favorite_pets: list of dicts with keys as in pet details

### 8. Messages Page
- File Path: templates/messages.html
- Page Title: Messages
- Element IDs and Types:
  - messages-page : div
  - conversation-list : div
  - message-input : textarea
  - send-message-button : button
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - conversations: list of dicts with keys 'conversation_id' (int), 'participants' (list of str), 'last_message' (str)

### 9. User Profile Page
- File Path: templates/profile.html
- Page Title: My Profile
- Element IDs and Types:
  - profile-page : div
  - profile-username : div
  - profile-email : input
  - update-profile-button : button
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - username : str
  - email : str

### 10. Admin Panel Page
- File Path: templates/admin_panel.html
- Page Title: Admin Panel
- Element IDs and Types:
  - admin-panel-page : div
  - pending-applications : div
  - all-pets-list : div
  - back-to-dashboard : button
- Navigation:
  - back-to-dashboard: Navigates to dashboard via `url_for('dashboard')`
- Context Variables:
  - pending_applications: list of dicts with keys 'application_id' (int), 'applicant_name' (str), 'pet_name' (str), 'date' (str), 'status' (str)
  - all_pets: list of dicts with keys as in pet details

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: data/users.txt
- Field Order and Description:
  - username (str): Unique user identifier
  - email (str): User email address
  - phone (str): Contact phone number
  - address (str): User physical address
- Example Data Rows:
```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. pets.txt
- Filename: data/pets.txt
- Field Order and Description:
  - pet_id (int): Unique pet identifier
  - name (str): Pet name
  - species (str): Species type (Dog, Cat, Bird, Rabbit, Other)
  - breed (str): Pet breed
  - age (str): Age description (e.g., "3 years")
  - gender (str): Gender (Male, Female)
  - size (str): Size category (Small, Medium, Large)
  - description (str): Detailed description
  - shelter_id (int): Associated shelter identifier
  - status (str): Availability status (Available, Pending, etc.)
  - date_added (str): Date added to system (YYYY-MM-DD)
- Example Data Rows:
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. applications.txt
- Filename: data/applications.txt
- Field Order and Description:
  - application_id (int): Unique application identifier
  - username (str): User who submitted application
  - pet_id (int): Pet applied for
  - applicant_name (str): Full name of applicant
  - phone (str): Contact phone number
  - address (str): Applicant address
  - housing_type (str): Housing type (House, Apartment, Condo, Other)
  - has_yard (str): 'Yes' or 'No' indicating yard availability
  - other_pets (str): Description of other pets owned
  - experience (str): Experience details (e.g., "5 years with dogs")
  - reason (str): Reason for adoption
  - status (str): Application status (Pending, Approved, Rejected)
  - date_submitted (str): Submission date (YYYY-MM-DD)
- Example Data Rows:
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. favorites.txt
- Filename: data/favorites.txt
- Field Order and Description:
  - username (str): User who favorited pet
  - pet_id (int): Pet identifier
  - date_added (str): Date pet was favorited (YYYY-MM-DD)
- Example Data Rows:
```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. messages.txt
- Filename: data/messages.txt
- Field Order and Description:
  - message_id (int): Unique message identifier
  - sender_username (str): Message sender
  - recipient_username (str): Message recipient
  - subject (str): Message subject
  - content (str): Message content
  - timestamp (str): Date and time of message (YYYY-MM-DD HH:MM:SS)
  - is_read (str): 'true' or 'false' indicating read status
- Example Data Rows:
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. adoption_history.txt
- Filename: data/adoption_history.txt
- Field Order and Description:
  - history_id (int): Unique history record identifier
  - username (str): Adopter username
  - pet_id (int): Pet identifier
  - pet_name (str): Pet name at adoption
  - adoption_date (str): Date of adoption (YYYY-MM-DD)
  - shelter_id (int): Shelter associated
- Example Data Rows:
```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. shelters.txt
- Filename: data/shelters.txt
- Field Order and Description:
  - shelter_id (int): Unique shelter identifier
  - name (str): Shelter name
  - address (str): Shelter address
  - phone (str): Contact phone number
  - email (str): Contact email
- Example Data Rows:
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```

---

# End of Design Specification
