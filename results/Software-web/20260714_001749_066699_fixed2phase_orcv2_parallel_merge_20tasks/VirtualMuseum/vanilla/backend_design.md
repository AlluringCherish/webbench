# VirtualMuseum Backend Design Documentation

---

## Section 1: Flask Route Specification

### 1. Dashboard Page
- **Route:** `/`
- **Method:** GET
- **Functionality:** Render the main dashboard page showing summary counts and navigation buttons.
- **Inputs:** None
- **Outputs:** Render template `dashboard.html`
- **Data Interaction:** Reads exhibitions.txt (to count total and active exhibitions), artifacts.txt (for summary count if needed).

### 2. Artifact Catalog Page
- **Route:** `/artifacts`
- **Method:** GET
- **Functionality:** Show all artifacts with optional filters (search by name or ID).
- **Inputs:** Query parameters `search` (string, optional) to filter by artifact name or artifact_id.
- **Outputs:** Render template `artifact_catalog.html` with filtered artifact list.
- **Data Interaction:** Reads artifacts.txt and exhibitions.txt (for exhibition names).


### 3. Exhibitions Page
- **Route:** `/exhibitions`
- **Method:** GET
- **Functionality:** Show all exhibitions with optional filter by exhibition_type.
- **Inputs:** Query parameter `type` (Permanent, Temporary, Virtual, optional)
- **Outputs:** Render template `exhibitions.html` with filtered exhibition list.
- **Data Interaction:** Reads exhibitions.txt and galleries.txt (for gallery names).


### 4. Exhibition Details Page
- **Route:** `/exhibitions/<exhibition_id>`
- **Method:** GET
- **Functionality:** Show detailed info about a specific exhibition, including artifacts in it.
- **Inputs:** URL parameter `exhibition_id` (integer)
- **Outputs:** Render template `exhibition_details.html` with exhibition info and artifacts.
- **Data Interaction:** Reads exhibitions.txt, artifacts.txt.


### 5. Visitor Tickets Page
- **Route:** `/tickets`
- **Method:** GET, POST
- **Functionality:** 
  - GET: Show the ticket purchase interface and user's purchased tickets.
  - POST: Process ticket purchase form submission.
- **GET Inputs:** User session (username) to show purchased tickets.
- **POST Inputs:** Form data -
  - `ticket_type` (Standard, Student, Senior, Family, VIP)
  - `number_of_tickets` (int)
  - `visit_date` (date string)
  - `visit_time` (string)
  - `visitor_name` (string)
  - `visitor_email` (string)
- **Outputs:** 
  - GET: Render template `visitor_tickets.html`.
  - POST: Redirect or render with purchase success/failure.
- **Data Interaction:** Reads and writes `tickets.txt`.


### 6. Virtual Events Page
- **Route:** `/events`
- **Method:** GET, POST (for registration and cancellation)
- **Functionality:** 
  - GET: List all events with registration info.
  - POST: Register or cancel registration to/from events.
- **GET Inputs:** User session for registered events display.
- **POST Inputs:** Form data:
  - `action` (register or cancel)
  - `event_id` (int)
- **Outputs:** Render template `virtual_events.html` with events and user registration status.
- **Data Interaction:** Reads `events.txt` and `event_registrations.txt`. Writes `event_registrations.txt` on registration changes.


### 7. Audio Guides Page
- **Route:** `/audioguides`
- **Method:** GET
- **Functionality:** Shows list of audio guides with optional filter by language.
- **Inputs:** Query parameter `language` (English, Spanish, French, optional)
- **Outputs:** Render template `audio_guides.html` with filtered audio guides list.
- **Data Interaction:** Reads audioguides.txt.


---

## Section 2: Local Text File Data Schemas

All files use pipe `|` delimiter with UTF-8 encoded plain text.

---

### 1. users.txt
- Filename: `data/users.txt`
- Fields:
  - `username` (str): Unique username
- Example:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

---

### 2. galleries.txt
- Filename: `data/galleries.txt`
- Fields:
  - `gallery_id` (int): Unique ID
  - `gallery_name` (str)
  - `floor` (int)
  - `capacity` (int)
  - `theme` (str)
  - `status` (str): e.g. Open, Renovation
- Example:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

---

### 3. exhibitions.txt
- Filename: `data/exhibitions.txt`
- Fields:
  - `exhibition_id` (int): Unique identifier
  - `title` (str): Exhibition title
  - `description` (str): Description text
  - `gallery_id` (int): Foreign key to galleries.txt
  - `exhibition_type` (str): Permanent, Temporary, Virtual
  - `start_date` (date, YYYY-MM-DD)
  - `end_date` (date, YYYY-MM-DD)
  - `curator_name` (str)
  - `created_by` (str): username
- Example:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

---

### 4. artifacts.txt
- Filename: `data/artifacts.txt`
- Fields:
  - `artifact_id` (int)
  - `artifact_name` (str)
  - `period` (str)
  - `origin` (str)
  - `description` (str)
  - `exhibition_id` (int)
  - `storage_location` (str)
  - `acquisition_date` (date, YYYY-MM-DD)
  - `added_by` (str): username
- Example:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

---

### 5. audioguides.txt
- Filename: `data/audioguides.txt`
- Fields:
  - `guide_id` (int)
  - `exhibit_number` (int): Numeric exhibit identifier
  - `title` (str)
  - `language` (str): Supported - English, Spanish, French
  - `duration` (int): Duration in minutes
  - `script` (str): Text script of audio
  - `narrator` (str)
  - `created_by` (str)
- Example:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```
---

### 6. tickets.txt
- Filename: `data/tickets.txt`
- Fields:
  - `ticket_id` (int): Unique ticket identifier
  - `username` (str): Purchaser username
  - `ticket_type` (str): Standard, Student, Senior, Family, VIP
  - `visit_date` (date, YYYY-MM-DD)
  - `visit_time` (str): e.g. "11:00 AM"
  - `number_of_tickets` (int)
  - `price` (float or int)
  - `visitor_name` (str)
  - `visitor_email` (str)
  - `purchase_date` (date, YYYY-MM-DD)
- Example:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

---

### 7. events.txt
- Filename: `data/events.txt`
- Fields:
  - `event_id` (int)
  - `title` (str)
  - `date` (date, YYYY-MM-DD)
  - `time` (str)
  - `event_type` (str): Webinar, Artist Talk, Virtual Tour
  - `speaker` (str)
  - `capacity` (int)
  - `description` (str)
  - `created_by` (str)
- Example:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

---

### 8. event_registrations.txt
- Filename: `data/event_registrations.txt`
- Fields:
  - `registration_id` (int)
  - `event_id` (int)
  - `username` (str)
  - `registration_date` (date, YYYY-MM-DD)
- Example:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

---

### 9. collection_logs.txt
- Filename: `data/collection_logs.txt`
- Fields:
  - `log_id` (int)
  - `artifact_id` (int)
  - `activity_type` (str): e.g. Inspection, Cleaning, Photography, Restoration
  - `date` (date, YYYY-MM-DD)
  - `notes` (str)
  - `condition` (str): e.g. Excellent, Good
  - `curator` (str)
- Example:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

## Section 3: Business Logic and Data Contracts

### User Authentication
- All user-related actions require a valid logged-in username stored in session.
- Usernames are validated against `users.txt`.

### Dashboard
- On load, count total exhibitions and active exhibitions (based on current date between start_date and end_date).

### Artifacts Filtering
- Search filters artifacts by exact or partial name or artifact_id.
- Return paginated or full list depending on queries (pagination optional).

### Exhibitions Filtering
- Filter exhibitions by type.
- Show exhibitions with gallery names resolved by gallery_id.

### Exhibition Details
- List all artifacts linked by exhibition_id.

### Ticket Purchasing
- Validate ticket_type is valid.
- Number of tickets must be positive integer.
- Compute price based on ticket_type unit price (defined in backend constants).
- Append new ticket record to `tickets.txt` with new ticket_id generated by incrementing largest existing ID.

### Event Registration
- Register user for event only if capacity not exceeded and user not already registered.
- Cancel registration by removing corresponding record.
- Maintain event_registrations.txt consistency.

### Audio Guides Filtering
- Filter by language when specified.

### Side Effects on Data Files
- Tickets purchase: Append one or multiple rows in `tickets.txt`.
- Event registration: Append or remove record in `event_registrations.txt`.

---

This design fully supports implementing the VirtualMuseum backend application using Flask and local text files as data store. Routes and data contracts are well defined for developers to proceed with implementation.
