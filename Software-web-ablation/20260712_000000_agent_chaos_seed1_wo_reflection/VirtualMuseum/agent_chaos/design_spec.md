# VirtualMuseum Design Specification

---

## 1. Flask Routes Specification

### 1. Root Route
- **Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method(s):** GET
- **Template:** None (redirect)
- **Context Variables:** None
- **Description:** Redirects to the Dashboard page route `/dashboard`.

### 2. Dashboard Page
- **Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method(s):** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `total_exhibitions` (int) - total number of exhibitions
  - `active_exhibitions` (int) - count of currently active exhibitions

### 3. Artifact Catalog Page
- **Path:** `/artifacts`
- **Function Name:** `artifact_catalog`
- **HTTP Method(s):** GET, POST
- **Template:** `artifact_catalog.html`
- **Context Variables:**
  - `artifacts` (list of dict) - list of artifact records to display
  - `search_query` (str) - current search keyword entered by user (empty if none)
  - `filter_applied` (bool) - indicates if filters/search are applied

### 4. Exhibitions Page
- **Path:** `/exhibitions`
- **Function Name:** `exhibitions`
- **HTTP Method(s):** GET, POST
- **Template:** `exhibitions.html`
- **Context Variables:**
  - `exhibitions` (list of dict) - list of exhibition records to display
  - `filter_type` (str) - current exhibition_type filter applied ("Permanent", "Temporary", "Virtual", or empty string for none)

### 5. Exhibition Details Page
- **Path:** `/exhibitions/<int:exhibition_id>`
- **Function Name:** `exhibition_details`
- **HTTP Method(s):** GET
- **Template:** `exhibition_details.html`
- **Context Variables:**
  - `exhibition` (dict) - detailed data about the exhibition
  - `artifacts` (list of dict) - list of artifacts belonging to the exhibition

### 6. Visitor Tickets Page
- **Path:** `/tickets`
- **Function Name:** `visitor_tickets`
- **HTTP Method(s):** GET, POST
- **Template:** `visitor_tickets.html`
- **Context Variables:**
  - `user_tickets` (list of dict) - current user's purchased ticket records
  - `purchase_success` (bool) - indicates if last purchase action succeeded (optional)

### 7. Virtual Events Page
- **Path:** `/events`
- **Function Name:** `virtual_events`
- **HTTP Method(s):** GET, POST
- **Template:** `virtual_events.html`
- **Context Variables:**
  - `events` (list of dict) - list of virtual museum events
  - `user_registrations` (list of dict) - list of event registrations by current user

### 8. Audio Guides Page
- **Path:** `/audioguides`
- **Function Name:** `audio_guides`
- **HTTP Method(s):** GET, POST
- **Template:** `audio_guides.html`
- **Context Variables:**
  - `audio_guides` (list of dict) - list of available audio guides
  - `language_filter` (str) - current language filter applied ("English", "Spanish", "French", or empty for none)

---

## 2. HTML Templates Specification

### 1. `dashboard.html`
- **Page Title:** Museum Dashboard
- **Main <h1>:** Museum Dashboard
- **Element IDs:**
  - `dashboard-page` (Div)
  - `exhibition-summary` (Div)
  - `artifact-catalog-button` (Button)
  - `exhibitions-button` (Button)
  - `visitor-tickets-button` (Button)
  - `virtual-events-button` (Button)
  - `audio-guides-button` (Button)
- **Navigation Buttons and Routes:**
  - `artifact-catalog-button`: `url_for('artifact_catalog')`
  - `exhibitions-button`: `url_for('exhibitions')`
  - `visitor-tickets-button`: `url_for('visitor_tickets')`
  - `virtual-events-button`: `url_for('virtual_events')`
  - `audio-guides-button`: `url_for('audio_guides')`
- **Context Variables:**
  - `total_exhibitions` (int) - to display total exhibitions count in `exhibition-summary`
  - `active_exhibitions` (int) - to display active exhibitions count in `exhibition-summary`

### 2. `artifact_catalog.html`
- **Page Title:** Artifact Catalog
- **Main <h1>:** Artifact Catalog
- **Element IDs:**
  - `artifact-catalog-page` (Div)
  - `artifact-table` (Table)
  - `search-artifact` (Input)
  - `apply-artifact-filter` (Button)
  - `back-to-dashboard` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-dashboard`: `url_for('dashboard')`
- **Context Variables:**
  - `artifacts` (list of dict) - each dict includes artifact fields displayed
  - `search_query` (str) - pre-fills the search input
  - `filter_applied` (bool) - controls UI state for filters

### 3. `exhibitions.html`
- **Page Title:** Exhibitions
- **Main <h1>:** Exhibitions
- **Element IDs:**
  - `exhibitions-page` (Div)
  - `exhibition-list` (Table)
  - `filter-exhibition-type` (Dropdown)
  - `apply-exhibition-filter` (Button)
  - `back-to-dashboard` (Button)
  - Dynamic buttons for each exhibition row:
    - `view-exhibition-button-{{ exhibition.exhibition_id }}` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-dashboard`: `url_for('dashboard')`
  - `view-exhibition-button-{{ exhibition.exhibition_id }}`: `url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)`
- **Context Variables:**
  - `exhibitions` (list of dict) - each dict includes exhibition details
  - `filter_type` (str) - the current filter selection

### 4. `exhibition_details.html`
- **Page Title:** Exhibition Details
- **Main <h1>:**
  - Element `exhibition-title` (H1) displays the exhibition title
- **Element IDs:**
  - `exhibition-details-page` (Div)
  - `exhibition-title` (H1)
  - `exhibition-description` (Div)
  - `exhibition-dates` (Div)
  - `exhibition-artifacts` (Table)
  - `back-to-exhibitions` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-exhibitions`: `url_for('exhibitions')`
- **Context Variables:**
  - `exhibition` (dict) - full details of the exhibition
  - `artifacts` (list of dict) - artifact records linked to this exhibition

### 5. `visitor_tickets.html`
- **Page Title:** Visitor Tickets
- **Main <h1>:** Visitor Tickets
- **Element IDs:**
  - `visitor-tickets-page` (Div)
  - `ticket-type` (Dropdown)
  - `number-of-tickets` (Input of type number)
  - `purchase-ticket-button` (Button)
  - `my-tickets-table` (Table)
  - `back-to-dashboard` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-dashboard`: `url_for('dashboard')`
- **Context Variables:**
  - `user_tickets` (list of dict) - tickets owned by the current user
  - `purchase_success` (bool) - optional message for purchase operation

### 6. `virtual_events.html`
- **Page Title:** Virtual Events
- **Main <h1>:** Virtual Events
- **Element IDs:**
  - `virtual-events-page` (Div)
  - `event-list` (Table)
  - Dynamic buttons for each event row:
    - `register-event-button-{{ event.event_id }}` (Button)
    - `cancel-registration-button-{{ registration.registration_id }}` (Button)
  - `back-to-dashboard` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-dashboard`: `url_for('dashboard')`
  - `register-event-button-{{ event.event_id }}`: `url_for('virtual_events')` (POST to register)
  - `cancel-registration-button-{{ registration.registration_id }}`: `url_for('virtual_events')` (POST to cancel)
- **Context Variables:**
  - `events` (list of dict) - all virtual events
  - `user_registrations` (list of dict) - current user's event registrations

### 7. `audio_guides.html`
- **Page Title:** Audio Guides
- **Main <h1>:** Audio Guides
- **Element IDs:**
  - `audio-guides-page` (Div)
  - `audio-guide-list` (Table)
  - `filter-language` (Dropdown)
  - `apply-language-filter` (Button)
  - Dynamic buttons for each audio guide row:
    - `play-guide-button-{{ guide.guide_id }}` (Button)
  - `back-to-dashboard` (Button)
- **Navigation Buttons and Routes:**
  - `back-to-dashboard`: `url_for('dashboard')`
  - `play-guide-button-{{ guide.guide_id }}`: No separate route; triggers audio playback client-side
- **Context Variables:**
  - `audio_guides` (list of dict) - all available guides
  - `language_filter` (str) - current language filter applied

---

## 3. Data File Schemas

### 1. `users.txt`
- **Fields:**
  - `username` (str)
- **Purpose:** Stores usernames for authentication.
- **Example Data:**
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. `galleries.txt`
- **Fields:**
  - `gallery_id` (int)
  - `gallery_name` (str)
  - `floor` (int)
  - `capacity` (int)
  - `theme` (str)
  - `status` (str)
- **Purpose:** Details about museum galleries where exhibitions are held.
- **Example Data:**
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. `exhibitions.txt`
- **Fields:**
  - `exhibition_id` (int)
  - `title` (str)
  - `description` (str)
  - `gallery_id` (int)
  - `exhibition_type` (str) - one of "Permanent", "Temporary", "Virtual"
  - `start_date` (str) - format YYYY-MM-DD
  - `end_date` (str) - format YYYY-MM-DD
  - `curator_name` (str)
  - `created_by` (str)
- **Purpose:** Stores data for exhibitions.
- **Example Data:**
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. `artifacts.txt`
- **Fields:**
  - `artifact_id` (int)
  - `artifact_name` (str)
  - `period` (str)
  - `origin` (str)
  - `description` (str)
  - `exhibition_id` (int)
  - `storage_location` (str)
  - `acquisition_date` (str) - format YYYY-MM-DD
  - `added_by` (str)
- **Purpose:** Details of artifacts managed by museum.
- **Example Data:**
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. `audioguides.txt`
- **Fields:**
  - `guide_id` (int)
  - `exhibit_number` (int)
  - `title` (str)
  - `language` (str) - values in {"English", "Spanish", "French"}
  - `duration` (int) - duration in minutes
  - `script` (str)
  - `narrator` (str)
  - `created_by` (str)
- **Purpose:** Audio guide information for exhibits.
- **Example Data:**
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. `tickets.txt`
- **Fields:**
  - `ticket_id` (int)
  - `username` (str)
  - `ticket_type` (str) - e.g. Standard, Student, Senior, Family, VIP
  - `visit_date` (str) - format YYYY-MM-DD
  - `visit_time` (str) - e.g. "11:00 AM"
  - `number_of_tickets` (int)
  - `price` (float or int)
  - `visitor_name` (str)
  - `visitor_email` (str)
  - `purchase_date` (str) - format YYYY-MM-DD
- **Purpose:** Stores visitor ticket purchase records.
- **Example Data:**
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. `events.txt`
- **Fields:**
  - `event_id` (int)
  - `title` (str)
  - `date` (str) - format YYYY-MM-DD
  - `time` (str) - e.g. "2:00 PM"
  - `event_type` (str) - e.g. Webinar, Artist Talk, Virtual Tour
  - `speaker` (str)
  - `capacity` (int)
  - `description` (str)
  - `created_by` (str)
- **Purpose:** Virtual event records and details.
- **Example Data:**
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. `event_registrations.txt`
- **Fields:**
  - `registration_id` (int)
  - `event_id` (int)
  - `username` (str)
  - `registration_date` (str) - format YYYY-MM-DD
- **Purpose:** Stores user registrations for virtual events.
- **Example Data:**
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. `collection_logs.txt`
- **Fields:**
  - `log_id` (int)
  - `artifact_id` (int)
  - `activity_type` (str)
  - `date` (str) - format YYYY-MM-DD
  - `notes` (str)
  - `condition` (str)
  - `curator` (str)
- **Purpose:** Logs related to artifact activity and condition maintenance.
- **Example Data:**
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This design specification provides comprehensive and exact details for Flask backend route implementations, HTML template designs with element IDs and context variables, and all data file schemas with sample data, ensuring clear development guidance for the VirtualMuseum application.