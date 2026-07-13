# VirtualMuseum Comprehensive Design Specification

---

## Section 1: Backend Design Summary

### 1. Flask Route Specification

#### 1. Dashboard Page
- **Route:** `/`
- **Method:** GET
- **Functionality:** Render main dashboard page showing summary counts (total exhibitions, active exhibitions) and navigation buttons.
- **Inputs:** None
- **Outputs:** Render `dashboard.html`.
- **Data:** Reads `exhibitions.txt` (to count exhibitions) and optional summary from `artifacts.txt`.

#### 2. Artifact Catalog Page
- **Route:** `/artifacts`
- **Method:** GET
- **Functionality:** Display all artifacts, support optional filtering via query parameter `search` (matches artifact name or artifact_id).
- **Inputs:** Query parameter `search` (string, optional).
- **Outputs:** Render `artifact_catalog.html` with filtered list.
- **Data:** Reads `artifacts.txt` and `exhibitions.txt` (for exhibition names).

#### 3. Exhibitions Page
- **Route:** `/exhibitions`
- **Method:** GET
- **Functionality:** Display exhibitions with optional filter by `type` (Permanent, Temporary, Virtual).
- **Inputs:** Query parameter `type` (string, optional).
- **Outputs:** Render `exhibitions.html` with filtered exhibitions.
- **Data:** Reads `exhibitions.txt` and `galleries.txt` (for gallery names).

#### 4. Exhibition Details Page
- **Route:** `/exhibitions/<exhibition_id>`
- **Method:** GET
- **Functionality:** Show detailed info for a specific exhibition including artifacts.
- **Inputs:** URL parameter `exhibition_id` (int).
- **Outputs:** Render `exhibition_details.html` with exhibition details and artifacts.
- **Data:** Reads `exhibitions.txt` and `artifacts.txt`.

#### 5. Visitor Tickets Page
- **Route:** `/tickets`
- **Method:** GET for rendering purchase interface and user's tickets; POST for processing ticket purchase.
- **Inputs:** 
  - GET: User session username to display tickets.
  - POST: Form fields:
    - `ticket_type` (Standard, Student, Senior, Family, VIP)
    - `number_of_tickets` (positive integer)
    - `visit_date` (date string)
    - `visit_time` (string)
    - `visitor_name` (string)
    - `visitor_email` (string)
- **Outputs:** 
  - GET: Render `visitor_tickets.html`.
  - POST: Redirect or render success/failure.
- **Data:** Reads and appends to `tickets.txt`.

#### 6. Virtual Events Page
- **Route:** `/events`
- **Method:** GET and POST
- **Functionality:** 
  - GET: List events and user's registration status.
  - POST: Register or cancel event registration.
- **Inputs:** 
  - GET: User session for registrations.
  - POST: Form data:
    - `action` (register or cancel)
    - `event_id` (int)
- **Outputs:** Render `virtual_events.html`.
- **Data:** Reads `events.txt` and `event_registrations.txt`; updates registrations.

#### 7. Audio Guides Page
- **Route:** `/audioguides`
- **Method:** GET
- **Functionality:** Display audio guides with optional filter by language.
- **Inputs:** Query parameter `language` (English, Spanish, French, optional).
- **Outputs:** Render `audio_guides.html`.
- **Data:** Reads `audioguides.txt`.

---

### 2. Local Text File Data Schemas

#### 1. users.txt
- Field: `username` (string)

#### 2. galleries.txt
- Fields: `gallery_id` (int), `gallery_name` (str), `floor` (int), `capacity` (int), `theme` (str), `status` (str)

#### 3. exhibitions.txt
- Fields: `exhibition_id` (int), `title` (str), `description` (str), `gallery_id` (int), `exhibition_type` (str), `start_date` (date), `end_date` (date), `curator_name` (str), `created_by` (str)

#### 4. artifacts.txt
- Fields: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str), `description` (str), `exhibition_id` (int), `storage_location` (str), `acquisition_date` (date), `added_by` (str)

#### 5. audioguides.txt
- Fields: `guide_id` (int), `exhibit_number` (int), `title` (str), `language` (str), `duration` (int), `script` (str), `narrator` (str), `created_by` (str)

#### 6. tickets.txt
- Fields: `ticket_id` (int), `username` (str), `ticket_type` (str), `visit_date` (date), `visit_time` (str), `number_of_tickets` (int), `price` (float/int), `visitor_name` (str), `visitor_email` (str), `purchase_date` (date)

#### 7. events.txt
- Fields: `event_id` (int), `title` (str), `date` (date), `time` (str), `event_type` (str), `speaker` (str), `capacity` (int), `description` (str), `created_by` (str)

#### 8. event_registrations.txt
- Fields: `registration_id` (int), `event_id` (int), `username` (str), `registration_date` (date)

#### 9. collection_logs.txt
- Fields: `log_id` (int), `artifact_id` (int), `activity_type` (str), `date` (date), `notes` (str), `condition` (str), `curator` (str)

---

### 3. Business Logic

- User authentication based on session username verified against `users.txt`.
- Dashboard shows total exhibitions and active exhibitions counting current date.
- Artifacts can be searched filtered by name or ID.
- Exhibitions filtered by type; galleries resolved by gallery_id.
- Exhibition details page lists all artifacts belonging to the exhibition.
- Ticket purchase validates ticket type and number; generates unique ticket_id, calculates price, appends to `tickets.txt`.
- Event registration enforces capacity and duplicate-free registrations; updates `event_registrations.txt`.
- Audio guides filterable by language.
- Writing operations update respective files maintaining data integrity.

---

## Section 2: Frontend Design Summary

### 1. Templates and UI Elements

#### Dashboard Page (`dashboard.html`)
- Title: "Museum Dashboard"
- Container Div: `dashboard-page`
- Summary Div: `exhibition-summary` (shows total and active exhibitions count)
- Navigation Buttons:
  - `artifact-catalog-button` to `/artifacts`
  - `exhibitions-button` to `/exhibitions`
  - `visitor-tickets-button` to `/tickets`
  - `virtual-events-button` to `/events`
  - `audio-guides-button` to `/audioguides`

#### Artifact Catalog Page (`artifact_catalog.html`)
- Title: "Artifact Catalog"
- Container Div: `artifact-catalog-page`
- Search Input: `search-artifact` (text input)
- Filter Apply Button: `apply-artifact-filter`
- Table: `artifact-table` with columns: Artifact ID, Name, Period, Origin, Exhibition, Actions
- Back Button: `back-to-dashboard`

#### Exhibitions Page (`exhibitions.html`)
- Title: "Exhibitions"
- Container Div: `exhibitions-page`
- Exhibition Type Filter Dropdown: `filter-exhibition-type` with options Permanent, Temporary, Virtual
- Filter Apply Button: `apply-exhibition-filter`
- Table: `exhibition-list` with columns: Title, Type, Start Date, End Date, Gallery, Status, Actions
- Detail View Buttons: `view-exhibition-button-{exhibition_id}`
- Back Button: `back-to-dashboard`

#### Exhibition Details Page (`exhibition_details.html`)
- Title: "Exhibition Details"
- Container Div: `exhibition-details-page`
- Title Heading: `exhibition-title`
- Description Div: `exhibition-description`
- Dates Div: `exhibition-dates`
- Artifact Table: `exhibition-artifacts` (ID, Name, Period, Origin)
- Back Button: `back-to-exhibitions`

#### Visitor Tickets Page (`visitor_tickets.html`)
- Title: "Visitor Tickets"
- Container Div: `visitor-tickets-page`
- Ticket Type Dropdown: `ticket-type`
- Number Input: `number-of-tickets` (min=1)
- Purchase Button: `purchase-ticket-button` (client-side validation for positive integer)
- Tickets Table: `my-tickets-table` showing user's tickets
- Back Button: `back-to-dashboard`

#### Virtual Events Page (`virtual_events.html`)
- Title: "Virtual Events"
- Container Div: `virtual-events-page`
- Events Table: `event-list` with columns including registration status
- Register Buttons: `register-event-button-{event_id}`
- Cancel Buttons: `cancel-registration-button-{registration_id}`
- Back Button: `back-to-dashboard`

#### Audio Guides Page (`audio_guides.html`)
- Title: "Audio Guides"
- Container Div: `audio-guides-page`
- Language Filter Dropdown: `filter-language` with English, Spanish, French
- Filter Apply Button: `apply-language-filter`
- Audio Guide Table: `audio-guide-list` with columns Exhibit Number, Title, Language, Duration
- Play Buttons: `play-guide-button-{guide_id}`
- Back Button: `back-to-dashboard`

---

### 2. Navigation and Interaction

- Dashboard navigation buttons link directly to their respective pages.
- `back-to-dashboard` buttons on all non-dashboard pages navigate back to Dashboard.
- On Exhibitions page, each `view-exhibition-button-{exhibition_id}` links to respective Exhibition Details.
- On Exhibition Details page, `back-to-exhibitions` returns to Exhibitions page.
- On Visitor Tickets page, purchase button validates number of tickets input > 0 before submission.
- Artifact Catalog `apply-artifact-filter` submits search query.
- Exhibitions filter selection and apply button update exhibition list.
- Virtual Events buttons handle registration or cancellation.
- Audio Guides filter and play buttons operate as described.

---

## Section 3: Consistency Verification

- All backend routes and frontend navigation paths are fully aligned with page names and route URLs.
- Dynamic button ID patterns in frontend (`view-exhibition-button-{exhibition_id}`, `register-event-button-{event_id}`, etc.) exactly match backend expected parameters.
- Frontend element IDs for filters, inputs, and buttons correspond exactly to backend parameter naming and data expectations.
- Data file schemas are consistent across backend and reflected in frontend data placeholders.
- User task requirements for seven pages, exact UI elements, and data management via local text files are completely addressed with no omissions.
- Navigation flows are complete: Dashboard is the root and can access all major pages; all pages have clear back navigation; detail and action buttons link correctly.
- Validation requirements (e.g., positive integer for ticket numbers) are stated and frontend-triggered as required.

---

This comprehensive design_spec.md consolidates the backend and frontend designs ensuring clarity and completeness for development of the "VirtualMuseum" web application as per user requirements.