# Backend Design Document for PetAdoptionCenter

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Methods:** GET
- **Purpose:** Load main dashboard displaying featured pets and recent activities.

### 2. Pet Listings Page
- **Route:** `/pets`
- **Methods:** GET
- **Parameters:** Optional query parameters: `search`, `species` (supports All, Dog, Cat, Bird, Rabbit, Other)
- **Purpose:** List all available pets applying optional filters.

### 3. Pet Details Page
- **Route:** `/pets/<int:pet_id>`
- **Methods:** GET
- **Purpose:** Show detailed information for a pet identified by `pet_id`.

### 4. Add Pet Page
- **Route:** `/pets/add`
- **Methods:** GET (load form), POST (submit new pet)
- **Purpose:** Allow shelter administrators to add new pet listings.

### 5. Adoption Application Page
- **Route:** `/applications/add/<int:pet_id>`
- **Methods:** GET (load form), POST (submit application)
- **Purpose:** Submit new adoption application for pet `pet_id`.

### 6. My Applications Page
- **Route:** `/applications`
- **Methods:** GET
- **Parameters:** Optional query parameter: `status` (All, Pending, Approved, Rejected)
- **Purpose:** List all adoption applications by current user filtered by status.

### 7. Favorites Page
- **Route:** `/favorites`
- **Methods:** GET
- **Purpose:** Display pets marked as favorites by the current user.

- **Route (Add Favorite):** `/favorites/add/<int:pet_id>`
- **Methods:** POST
- **Purpose:** Add a pet to user's favorites.

- **Route (Remove Favorite):** `/favorites/remove/<int:pet_id>`
- **Methods:** POST
- **Purpose:** Remove a pet from user's favorites.

### 8. Messages Page
- **Route:** `/messages`
- **Methods:** GET
- **Purpose:** Display list of message conversations for current user.

- **Route (Send Message):** `/messages/send`
- **Methods:** POST
- **Purpose:** Send message from current user to a shelter or other user.

- **Route (View Conversation):** `/messages/conversation/<string:other_username>`
- **Methods:** GET
- **Purpose:** View message history between current user and `other_username`.

### 9. User Profile Page
- **Route:** `/profile`
- **Methods:** GET (view profile), POST (update profile email)
- **Purpose:** View and update user profile information.

### 10. Admin Panel Page
- **Route:** `/admin`
- **Methods:** GET
- **Purpose:** Display list of pending applications and all pets with edit/delete options.

- **Route (Update Application Status):** `/admin/application/<int:application_id>/update`
- **Methods:** POST
- **Purpose:** Admin updates adoption application status.

- **Route (Edit Pet):** `/admin/pet/<int:pet_id>/edit`
- **Methods:** GET (load edit form), POST (submit edits)
- **Purpose:** Admin edits pet details.

- **Route (Delete Pet):** `/admin/pet/<int:pet_id>/delete`
- **Methods:** POST
- **Purpose:** Admin deletes pet from listings.


## Section 2: Data Interaction and Schema Definition

All data is stored in text files within `data/` folder using pipe-delimited (`|`) fields.

### 1. users.txt
- **Fields:** `username|email|phone|address`
- **Example:** `john_doe|john@example.com|555-1234|123 Main St, City`
- **Operations:** Read whole file to retrieve user info; overwrite line on email update.

### 2. pets.txt
- **Fields:** 
```
pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
```
- **Example:**
```
1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
```
- **Operations:** Read all pets; add/edit/delete lines for pet management; filter by status/species.

### 3. applications.txt
- **Fields:**
```
application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
```
- **Example:**
```
1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
```
- **Operations:** Read all user applications; add new applications; update application status (admin).

### 4. favorites.txt
- **Fields:**
```
username|pet_id|date_added
```
- **Example:**
```
john_doe|1|2024-11-01
```
- **Operations:** Read user favorites; add or remove pet entries.

### 5. messages.txt
- **Fields:**
```
message_id|sender_username|recipient_username|subject|content|timestamp|is_read
```
- **Example:**
```
1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
```
- **Operations:** Read user's sent and received messages; add new messages; update read status.

### 6. adoption_history.txt
- **Fields:**
```
history_id|username|pet_id|pet_name|adoption_date|shelter_id
```
- **Example:**
```
1|jane_smith|2|Whiskers|2024-11-15|1
```
- **Operations:** Read history to show successful adoptions.

### 7. shelters.txt
- **Fields:**
```
shelter_id|name|address|phone|email
```
- **Example:**
```
1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
```
- **Operations:** Read shelter info for display and message routing.


### Data Reading and Writing Notes
- On reads, load entire file into memory, parse by lines, split by `|` into dicts.
- On writes, overwrite entire file or append if adding.
- Concurrency: assume serialized access (single user/process for simplicity).
- Error Handling: Validate data completeness and format before writes; handle missing or malformed data gracefully.


## Section 3: Backend Logic and Workflow

### Dashboard (`/dashboard`)
- Read `pets.txt` to list up to 5 latest pets with status "Available" as featured pets.
- Read recent activities such as recent adoption applications or adoptions if needed.
- Render dashboard data in JSON or template.

### Pet Listings (`/pets`)
- Read all pets with status = "Available".
- Apply filters if query params present: search by pet name (case-insensitive), filter species.
- Return filtered list as JSON.

### Pet Details (`/pets/<pet_id>`)
- Read pet details by matching pet_id.
- Include shelter info from `shelters.txt`.
- Return pet full details.

### Add Pet (`/pets/add`)
- GET: Render form for adding pet.
- POST: Validate form data; generate new pet_id (max existing +1).
- Append new pet line to `pets.txt` with status="Available".
- Redirect or return success.

### Adoption Application (`/applications/add/<pet_id>`)
- GET: Render application form with pet info.
- POST: Validate input.
- Generate new application_id.
- Append application line with status="Pending" and current date.
- Return confirmation.

### My Applications (`/applications`)
- Read all applications for current user.
- Filter by status if provided.
- Return list for display.

### Favorites (`/favorites`)
- Read all favorites for current user.
- Get pet details for each favorite pet_id.
- Return list.

- Add/Remove favorites POST routes update `favorites.txt` accordingly.

### Messages (`/messages`)
- GET: Read all messages where current user is sender or recipient.
- Group messages by conversation partner.
- Return conversation list.

- POST `/messages/send`: Validate and add new message line with timestamp.

- Conversation View: return sorted messages between current user and other.

### User Profile (`/profile`)
- GET: Read user info from `users.txt` by username.
- POST: Update email if changed in file.

### Admin Panel (`/admin`)
- GET: Read all pending applications and all pets.
- POST to update application status or pet details.
- Delete pet route removes from `pets.txt`.


### Session/User State
- The system assumes a logged-in user with username available for each route.
- User-specific routes filter data by this username.
- Admin routes checked by username role, assumed to be differentiated outside file storage.


---

This backend design document defines all necessary routes, data schema interactions, and logic workflows for full implementation of the PetAdoptionCenter backend in Flask.