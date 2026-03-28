# PetAdoptionCenter Flask Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

| Route Path             | Function Name          | HTTP Method | Template Rendered            | Context Variables Passed (name:type)                                                                                  |
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                      | root_redirect          | GET         | None (Redirect)              | None                                                                                                                   |
| /dashboard             | dashboard              | GET         | dashboard.html              | featured_pets: list of dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str,
  shelter_id: int,
  status: str,
  date_added: str
} (limit 5, only pets with status "Available")

| recent_activities: list of str (for example logs or messages to show recent events)

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /pets                  | pet_listings           | GET         | pet_listings.html           | pets: list of dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str,
  shelter_id: int,
  status: str,
  date_added: str
}

| filter_species: str (value from All, Dog, Cat, Bird, Rabbit, Other)

| search_name: str (search input value or empty string)

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /pets/<int:pet_id>     | pet_details            | GET         | pet_details.html            | pet: dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str,
  shelter_id: int,
  status: str,
  date_added: str
}

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /add-pet               | add_pet_page           | GET         | add_pet.html                | None                                                                                                                   |
| /add-pet               | add_pet_submit         | POST        | None (Redirect after submit) | Form data submitted with fields:
  - pet_name: str
  - pet_species: str (Dog, Cat, Bird, Rabbit, Other)
  - pet_breed: str
  - pet_age: str (format e.g. "2 years")
  - pet_gender: str (Male, Female)
  - pet_size: str (Small, Medium, Large)
  - pet_description: str

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /apply/<int:pet_id>    | adoption_application   | GET         | application.html            | pet: dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str
}

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /apply/<int:pet_id>    | submit_application     | POST        | None (Redirect to my-applications or confirmation page) | Form data submitted with fields:
  - applicant_name: str
  - applicant_phone: str
  - housing_type: str (House, Apartment, Condo, Other)
  - reason: str

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /my-applications       | my_applications        | GET         | my_applications.html        | applications: list of dict {
  application_id: int,
  pet_name: str,
  date_submitted: str,
  status: str
}

| filter_status: str (All, Pending, Approved, Rejected)

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /favorites             | favorites              | GET         | favorites.html              | favorites: list of dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str
}

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /messages              | messages               | GET         | messages.html               | conversations: list of dict {
  conversation_id: int,
  participant_username: str,
  last_message_summary: str,
  unread_count: int
}

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /messages/send         | send_message           | POST        | None (Redirect to messages) | Form data submitted with fields:
  - recipient_username: str
  - subject: str
  - content: str

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /profile               | user_profile           | GET         | profile.html                | user_profile: dict {
  username: str,
  email: str,
  phone: str,
  address: str
}

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /profile/update        | update_profile         | POST        | None (Redirect to profile)  | Form data submitted with fields:
  - email: str

| 
|------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /admin-panel           | admin_panel            | GET         | admin_panel.html            | pending_applications: list of dict {
  application_id: int,
  applicant_name: str,
  pet_name: str,
  date_submitted: str,
  status: str
}

| all_pets: list of dict {
  pet_id: int,
  name: str,
  species: str,
  breed: str,
  age: str,
  gender: str,
  size: str,
  description: str,
  status: str
}

---

## Section 2: HTML Template Specifications (Frontend Focus)

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title (for <title> and <h1>): Pet Adoption Dashboard
- Element IDs and Types:
  - dashboard-page: div
  - featured-pets: div
  - browse-pets-button: button
  - back-to-dashboard: button
- Navigation Mappings:
  - browse-pets-button: navigates to `url_for('pet_listings')`
  - back-to-dashboard: reloads the current dashboard (links to `url_for('dashboard')`)
- Context Variables:
  - featured_pets: list of dict (each dict fields: pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str, description:str, shelter_id:int, status:str, date_added:str)
  - recent_activities: list of str

### 2. Pet Listings Page
- File Path: templates/pet_listings.html
- Page Title: Available Pets
- Element IDs and Types:
  - pet-listings-page: div
  - search-input: input
  - filter-species: select (dropdown)
  - pet-grid: div
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
  - Pet cards inside pet-grid each link to pet detail page at `url_for('pet_details', pet_id=pet.pet_id)` where pet.pet_id is the id from context variable
- Context Variables:
  - pets: list of dict (fields as described)
  - filter_species: str (e.g. "All", "Dog", etc.)
  - search_name: str

### 3. Pet Details Page
- File Path: templates/pet_details.html
- Page Title: Pet Details
- Element IDs and Types:
  - pet-details-page: div
  - pet-name: h1
  - pet-species: div
  - pet-description: div
  - adopt-button: button
  - back-to-listings: button
- Navigation Mappings:
  - adopt-button: navigates to `url_for('adoption_application', pet_id=pet.pet_id)`
  - back-to-listings: navigates to `url_for('pet_listings')`
- Context Variables:
  - pet: dict as described

### 4. Add Pet Page
- File Path: templates/add_pet.html
- Page Title: Add New Pet
- Element IDs and Types:
  - add-pet-page: div
  - pet-name-input: input
  - pet-species-input: select (dropdown)
  - pet-breed-input: input
  - pet-age-input: input
  - pet-gender-input: select (dropdown)
  - pet-size-input: select (dropdown)
  - pet-description-input: textarea
  - submit-pet-button: button
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - None (form page)

### 5. Adoption Application Page
- File Path: templates/application.html
- Page Title: Adoption Application
- Element IDs and Types:
  - application-page: div
  - applicant-name: input
  - applicant-phone: input
  - housing-type: select (dropdown)
  - reason: textarea
  - submit-application-button: button
  - back-to-pet: button
- Navigation Mappings:
  - back-to-pet: navigates to `url_for('pet_details', pet_id=pet.pet_id)`
- Context Variables:
  - pet: dict as described

### 6. My Applications Page
- File Path: templates/my_applications.html
- Page Title: My Applications
- Element IDs and Types:
  - my-applications-page: div
  - filter-status: select (dropdown)
  - applications-table: table
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - applications: list of dict (application_id:int, pet_name:str, date_submitted:str, status:str)
  - filter_status: str

### 7. Favorites Page
- File Path: templates/favorites.html
- Page Title: My Favorites
- Element IDs and Types:
  - favorites-page: div
  - favorites-grid: div
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - favorites: list of dict (pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str, description:str)

### 8. Messages Page
- File Path: templates/messages.html
- Page Title: Messages
- Element IDs and Types:
  - messages-page: div
  - conversation-list: div
  - message-input: textarea
  - send-message-button: button
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - conversations: list of dict (conversation_id:int, participant_username:str, last_message_summary:str, unread_count:int)

### 9. User Profile Page
- File Path: templates/profile.html
- Page Title: My Profile
- Element IDs and Types:
  - profile-page: div
  - profile-username: div
  - profile-email: input
  - update-profile-button: button
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - user_profile: dict (username:str, email:str, phone:str, address:str)

### 10. Admin Panel Page
- File Path: templates/admin_panel.html
- Page Title: Admin Panel
- Element IDs and Types:
  - admin-panel-page: div
  - pending-applications: div
  - all-pets-list: div
  - back-to-dashboard: button
- Navigation Mappings:
  - back-to-dashboard: navigates to `url_for('dashboard')`
- Context Variables:
  - pending_applications: list of dict (application_id:int, applicant_name:str, pet_name:str, date_submitted:str, status:str)
  - all_pets: list of dict (pet_id:int, name:str, species:str, breed:str, age:str, gender:str, size:str, description:str, status:str)

---

## Section 3: Data File Schemas (Backend Focus)

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited):
  - username (str): Unique username identifier
  - email (str): User email address
  - phone (str): User phone number
  - address (str): User physical address
- Example Data Rows:
```
john_doe|john@example.com|555-1234|123 Main St, City
admin_user|admin@shelter.com|555-0000|456 Shelter Ave
jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
```

### 2. pets.txt
- Filename: data/pets.txt
- Fields (pipe-delimited):
  - pet_id (int): Unique pet identifier
  - name (str): Pet's name
  - species (str): Species of the pet (Dog, Cat, Bird, Rabbit, Other)
  - breed (str): Breed of the pet
  - age (str): Age description (e.g., "3 years")
  - gender (str): Gender (Male, Female)
  - size (str): Size category (Small, Medium, Large)
  - description (str): Detailed description of the pet
  - shelter_id (int): Identifier of the shelter responsible
  - status (str): Current status (Available, Pending, Adopted, etc.)
  - date_added (str): Date added to system in YYYY-MM-DD format
- Example Data Rows:
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
```

### 3. applications.txt
- Filename: data/applications.txt
- Fields (pipe-delimited):
  - application_id (int): Unique application identifier
  - username (str): Username of applicant
  - pet_id (int): Pet identifier applied for
  - applicant_name (str): Full name of applicant
  - phone (str): Applicant phone number
  - address (str): Applicant address
  - housing_type (str): Housing type (House, Apartment, Condo, Other)
  - has_yard (str): Yes/No if applicant has yard
  - other_pets (str): Description of other pets
  - experience (str): Experience with pets
  - reason (str): Reason for adopting
  - status (str): Application status (Pending, Approved, Rejected)
  - date_submitted (str): Date application submitted YYYY-MM-DD
- Example Data Rows:
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
```

### 4. favorites.txt
- Filename: data/favorites.txt
- Fields (pipe-delimited):
  - username (str): Username of the user
  - pet_id (int): Pet identifier added to favorites
  - date_added (str): Date pet was added YYYY-MM-DD
- Example Data Rows:
```
john_doe|1|2024-11-01
john_doe|3|2024-11-05
jane_smith|2|2024-10-25
```

### 5. messages.txt
- Filename: data/messages.txt
- Fields (pipe-delimited):
  - message_id (int): Unique message identifier
  - sender_username (str): Username of sender
  - recipient_username (str): Username of recipient
  - subject (str): Subject line of message
  - content (str): Message content body
  - timestamp (str): Date and time of message YYYY-MM-DD HH:MM:SS
  - is_read (str): true/false indicating if message has been read
- Example Data Rows:
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
```

### 6. adoption_history.txt
- Filename: data/adoption_history.txt
- Fields (pipe-delimited):
  - history_id (int): Unique history record identifier
  - username (str): Username of adopter
  - pet_id (int): Pet identifier
  - pet_name (str): Name of pet adopted
  - adoption_date (str): Date of adoption YYYY-MM-DD
  - shelter_id (int): Shelter where pet was adopted from
- Example Data Rows:
```
1|jane_smith|2|Whiskers|2024-11-15|1
```

### 7. shelters.txt
- Filename: data/shelters.txt
- Fields (pipe-delimited):
  - shelter_id (int): Unique shelter identifier
  - name (str): Shelter name
  - address (str): Shelter physical address
  - phone (str): Shelter contact phone
  - email (str): Shelter contact email
- Example Data Rows:
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
```
