# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Methods:** `GET`
- **Template Rendered:** redirects to `/dashboard`
- **Context Variables:** None

### 2. Dashboard Page
- **Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Methods:** `GET`
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `total_exhibitions` (int) — total count of exhibitions
  - `active_exhibitions_count` (int) — count of exhibitions currently active (today's date between start_date and end_date)

### 3. Artifact Catalog Page
- **Path:** `/artifacts`
- **Function Name:** `artifact_catalog`
- **HTTP Methods:** `GET`, `POST` (POST for applying search/filter)
- **Template Rendered:** `artifact_catalog.html`
- **Context Variables:**
  - `artifacts_list` (list of dict) — list of artifacts, each with keys: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str), `exhibition_title` (str or None)
  - `search_query` (str) — current search keyword (optional)

### 4. Exhibitions Page
- **Path:** `/exhibitions`
- **Function Name:** `exhibitions`
- **HTTP Methods:** `GET`, `POST` (POST for applying exhibition type filter)
- **Template Rendered:** `exhibitions.html`
- **Context Variables:**
  - `exhibitions_list` (list of dict) — list of exhibitions, each with keys: `exhibition_id` (int), `title` (str), `exhibition_type` (str), `start_date` (str), `end_date` (str), `gallery_name` (str), `status` (str, derived from gallery status or current date comparison)
  - `filter_type` (str) — currently selected exhibition type filter (optional)

### 5. Exhibition Details Page
- **Path:** `/exhibition/<int:exhibition_id>`
- **Function Name:** `exhibition_details`
- **HTTP Methods:** `GET`
- **Template Rendered:** `exhibition_details.html`
- **Context Variables:**
  - `exhibition` (dict) — exhibition details with keys: `exhibition_id` (int), `title` (str), `description` (str), `start_date` (str), `end_date` (str)
  - `artifacts_in_exhibition` (list of dict) — list of artifacts belonging to the exhibition, each with keys: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str)

### 6. Visitor Tickets Page
- **Path:** `/visitor-tickets`
- **Function Name:** `visitor_tickets`
- **HTTP Methods:** `GET`, `POST` (POST to purchase tickets)
- **Template Rendered:** `visitor_tickets.html`
- **Context Variables:**
  - `user_tickets` (list of dict) — tickets purchased by current user, with keys: `ticket_id` (int), `ticket_type` (str), `visit_date` (str), `visit_time` (str), `number_of_tickets` (int), `price` (float), `visitor_name` (str), `visitor_email` (str), `purchase_date` (str)
  - `ticket_types` (list of str) — list of available ticket types [Standard, Student, Senior, Family, VIP]

### 7. Virtual Events Page
- **Path:** `/virtual-events`
- **Function Name:** `virtual_events`
- **HTTP Methods:** `GET`, `POST` (POST to register or cancel registration)
- **Template Rendered:** `virtual_events.html`
- **Context Variables:**
  - `events_list` (list of dict) — all events with keys: `event_id` (int), `title` (str), `date` (str), `time` (str), `event_type` (str), `registration_status` (str: 'Registered' or 'Not Registered' for the current user)
  - `user_registrations` (list of int) — event_ids the user is registered for

### 8. Audio Guides Page
- **Path:** `/audio-guides`
- **Function Name:** `audio_guides`
- **HTTP Methods:** `GET`, `POST` (POST for applying language filter)
- **Template Rendered:** `audio_guides.html`
- **Context Variables:**
  - `audio_guides_list` (list of dict) — audio guides with keys: `guide_id` (int), `exhibit_number` (str), `title` (str), `language` (str), `duration` (int)
  - `filter_language` (str) — current language filter (optional)
  - `languages` (list of str) — available languages [English, Spanish, French]

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- **Page Title:** Museum Dashboard
- **Main Heading (h1):** Museum Dashboard
- **Element IDs:**
  - `dashboard-page` (Div) - container for the entire page
  - `exhibition-summary` (Div) - displays total exhibitions and active exhibitions
  - `artifact-catalog-button` (Button) - navigates to artifact catalog page
  - `exhibitions-button` (Button) - navigates to exhibitions page
  - `visitor-tickets-button` (Button) - navigates to visitor tickets page
  - `virtual-events-button` (Button) - navigates to virtual events page
  - `audio-guides-button` (Button) - navigates to audio guides page
- **Button to Route Mapping:**
  - `artifact-catalog-button` &rarr; `url_for('artifact_catalog')`
  - `exhibitions-button` &rarr; `url_for('exhibitions')`
  - `visitor-tickets-button` &rarr; `url_for('visitor_tickets')`
  - `virtual-events-button` &rarr; `url_for('virtual_events')`
  - `audio-guides-button` &rarr; `url_for('audio_guides')`
- **Context Variables:**
  - `total_exhibitions` (int) — for displaying total exhibitions count
  - `active_exhibitions_count` (int) — for displaying active exhibitions count

### 2. artifact_catalog.html
- **Page Title:** Artifact Catalog
- **Main Heading (h1):** Artifact Catalog
- **Element IDs:**
  - `artifact-catalog-page` (Div) - page container
  - `artifact-table` (Table) - lists artifacts with columns: ID, name, period, origin, exhibition, actions
  - `search-artifact` (Input) - text input for search
  - `apply-artifact-filter` (Button) - to apply search/filter
  - `back-to-dashboard` (Button) - navigate to dashboard
- **Button to Route Mapping:**
  - `apply-artifact-filter` &rarr; `url_for('artifact_catalog')` (POST triggers filtering/search)
  - `back-to-dashboard` &rarr; `url_for('dashboard')`
- **Context Variables:**
  - `artifacts_list` (list) — used to populate `artifact-table`
  - `search_query` (str) — to populate `search-artifact` input field

### 3. exhibitions.html
- **Page Title:** Exhibitions
- **Main Heading (h1):** Exhibitions
- **Element IDs:**
  - `exhibitions-page` (Div) - page container
  - `exhibition-list` (Table) - exhibitions table
  - `filter-exhibition-type` (Dropdown) - exhibition type filter
  - `apply-exhibition-filter` (Button) - apply filter action
  - `back-to-dashboard` (Button) - navigate back to dashboard
  - Dynamic button ids per exhibition row:
    - `view-exhibition-button-{{ exhibition.exhibition_id }}` (Button) - to view details
- **Button to Route Mapping:**
  - `apply-exhibition-filter` &rarr; `url_for('exhibitions')` (POST to apply filter)
  - `back-to-dashboard` &rarr; `url_for('dashboard')`
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` &rarr; `url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)`
- **Context Variables:**
  - `exhibitions_list` (list) — populate `exhibition-list` table
  - `filter_type` (str) — current filter selection

### 4. exhibition_details.html
- **Page Title:** Exhibition Details
- **Main Heading (h1):** `{{ exhibition.title }}`
- **Element IDs:**
  - `exhibition-details-page` (Div) - container
  - `exhibition-title` (H1) - exhibition title
  - `exhibition-description` (Div) - description text
  - `exhibition-dates` (Div) - start and end dates
  - `exhibition-artifacts` (Table) - list of artifacts in this exhibition
  - `back-to-exhibitions` (Button) - back to exhibitions page
- **Button to Route Mapping:**
  - `back-to-exhibitions` &rarr; `url_for('exhibitions')`
- **Context Variables:**
  - `exhibition` (dict) — used for title, description, dates
  - `artifacts_in_exhibition` (list) — populate artifacts table

### 5. visitor_tickets.html
- **Page Title:** Visitor Tickets
- **Main Heading (h1):** Visitor Tickets
- **Element IDs:**
  - `visitor-tickets-page` (Div) - container
  - `ticket-type` (Dropdown) - select ticket type
  - `number-of-tickets` (Input number) - number input
  - `purchase-ticket-button` (Button) - purchase tickets
  - `my-tickets-table` (Table) - user tickets list
  - `back-to-dashboard` (Button) - back to dashboard
- **Button to Route Mapping:**
  - `purchase-ticket-button` &rarr; `url_for('visitor_tickets')` (POST to purchase)
  - `back-to-dashboard` &rarr; `url_for('dashboard')`
- **Context Variables:**
  - `user_tickets` (list) — populate tickets table
  - `ticket_types` (list) — populate ticket-type dropdown

### 6. virtual_events.html
- **Page Title:** Virtual Events
- **Main Heading (h1):** Virtual Events
- **Element IDs:**
  - `virtual-events-page` (Div) - container
  - `event-list` (Table) - table of events
  - Dynamic buttons per event row:
    - `register-event-button-{{ event.event_id }}` (Button) - register
    - `cancel-registration-button-{{ registration.registration_id }}` (Button) - cancel registration
  - `back-to-dashboard` (Button) - back to dashboard
- **Button to Route Mapping:**
  - `register-event-button-{{ event.event_id }}` &rarr; `url_for('virtual_events')` (POST to register)
  - `cancel-registration-button-{{ registration.registration_id }}` &rarr; `url_for('virtual_events')` (POST to cancel)
  - `back-to-dashboard` &rarr; `url_for('dashboard')`
- **Context Variables:**
  - `events_list` (list) — populate event-list table
  - `user_registrations` (list) — track registrations for dynamic buttons

### 7. audio_guides.html
- **Page Title:** Audio Guides
- **Main Heading (h1):** Audio Guides
- **Element IDs:**
  - `audio-guides-page` (Div) - container
  - `audio-guide-list` (Table) - listing guides
  - `filter-language` (Dropdown) - language filter
  - `apply-language-filter` (Button) - apply language filter
  - Dynamic buttons per guide:
    - `play-guide-button-{{ guide.guide_id }}` (Button) - play audio
  - `back-to-dashboard` (Button) - back to dashboard
- **Button to Route Mapping:**
  - `apply-language-filter` &rarr; `url_for('audio_guides')` (POST to apply filter)
  - `play-guide-button-{{ guide.guide_id }}` &rarr; No route - client-side control or handled by JavaScript (out of scope)
  - `back-to-dashboard` &rarr; `url_for('dashboard')`
- **Context Variables:**
  - `audio_guides_list` (list) — populate table
  - `filter_language` (str) — selected language filter
  - `languages` (list) — available languages selection

---

## Section 3: Data File Schemas

### 1. users.txt
- **File Name:** `users.txt`
- **Fields:**
  - `username`
- **Purpose:** Stores usernames of museum curators and visitors authorized on the platform.
- **Example Rows:**
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- **File Name:** `galleries.txt`
- **Fields:**
  - `gallery_id` (int)
  - `gallery_name` (str)
  - `floor` (int)
  - `capacity` (int)
  - `theme` (str)
  - `status` (str) — e.g., Open, Renovation
- **Purpose:** Contains information on gallery rooms including location and availability.
- **Example Rows:**
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- **File Name:** `exhibitions.txt`
- **Fields:**
  - `exhibition_id` (int)
  - `title` (str)
  - `description` (str)
  - `gallery_id` (int)
  - `exhibition_type` (str) — Permanent, Temporary, Virtual
  - `start_date` (str, YYYY-MM-DD)
  - `end_date` (str, YYYY-MM-DD)
  - `curator_name` (str)
  - `created_by` (str, username)
- **Purpose:** Stores exhibitions metadata and scheduling.
- **Example Rows:**
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- **File Name:** `artifacts.txt`
- **Fields:**
  - `artifact_id` (int)
  - `artifact_name` (str)
  - `period` (str)
  - `origin` (str)
  - `description` (str)
  - `exhibition_id` (int)
  - `storage_location` (str)
  - `acquisition_date` (str, YYYY-MM-DD)
  - `added_by` (str, username)
- **Purpose:** Stores all artifact details and metadata.
- **Example Rows:**
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- **File Name:** `audioguides.txt`
- **Fields:**
  - `guide_id` (int)
  - `exhibit_number` (str)
  - `title` (str)
  - `language` (str) — English, Spanish, French
  - `duration` (int, minutes)
  - `script` (str)
  - `narrator` (str)
  - `created_by` (str, username)
- **Purpose:** Audio guides details for exhibits.
- **Example Rows:**
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- **File Name:** `tickets.txt`
- **Fields:**
  - `ticket_id` (int)
  - `username` (str)
  - `ticket_type` (str)
  - `visit_date` (str, YYYY-MM-DD)
  - `visit_time` (str)
  - `number_of_tickets` (int)
  - `price` (float)
  - `visitor_name` (str)
  - `visitor_email` (str)
  - `purchase_date` (str, YYYY-MM-DD)
- **Purpose:** Visitor ticket purchasing and tracking data.
- **Example Rows:**
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- **File Name:** `events.txt`
- **Fields:**
  - `event_id` (int)
  - `title` (str)
  - `date` (str, YYYY-MM-DD)
  - `time` (str)
  - `event_type` (str) — Webinar, Artist Talk, Virtual Tour
  - `speaker` (str)
  - `capacity` (int)
  - `description` (str)
  - `created_by` (str, username)
- **Purpose:** Virtual events offered by the museum.
- **Example Rows:**
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- **File Name:** `event_registrations.txt`
- **Fields:**
  - `registration_id` (int)
  - `event_id` (int)
  - `username` (str)
  - `registration_date` (str, YYYY-MM-DD)
- **Purpose:** Tracks user registrations to virtual events.
- **Example Rows:**
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- **File Name:** `collection_logs.txt`
- **Fields:**
  - `log_id` (int)
  - `artifact_id` (int)
  - `activity_type` (str)
  - `date` (str, YYYY-MM-DD)
  - `notes` (str)
  - `condition` (str)
  - `curator` (str, username)
- **Purpose:** Logs artifact activity such as inspections, cleaning, photography.
- **Example Rows:**
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

End of Design Specification Document
