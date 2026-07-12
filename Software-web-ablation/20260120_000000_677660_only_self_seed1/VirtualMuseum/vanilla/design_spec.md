# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Method | Template Filename         | Context Variables                                                     |
|-------------------------------|-----------------------------|-------------|---------------------------|---------------------------------------------------------------------|
| /                             | root_redirect               | GET         | -                         | - Redirects to /dashboard                                            |
| /dashboard                    | dashboard_view             | GET         | dashboard.html            | exhibitions_count: int, active_exhibitions_count: int               |
| /artifact-catalog             | artifact_catalog_view      | GET, POST   | artifact_catalog.html     | artifacts: list of dict, filtered_artifacts: list of dict (POST for filter/search), search_query: str (optional)        |
| /exhibitions                 | exhibitions_view           | GET, POST   | exhibitions.html          | exhibitions: list of dict, filtered_exhibitions: list of dict (POST for filter), exhibition_types: list[str]             |
| /exhibition/<int:exhibition_id> | exhibition_details_view      | GET         | exhibition_details.html   | exhibition: dict, artifacts: list of dict                           |
| /visitor-tickets             | visitor_tickets_view        | GET, POST   | visitor_tickets.html      | tickets: list of dict, ticket_types: list[str], purchase_result: str (on POST)                                      |
| /virtual-events              | virtual_events_view         | GET, POST   | virtual_events.html       | events: list of dict, event_registrations: list of dict, user_registrations: set of registration_ids, filter applied info (POST)          |
| /audio-guides                | audio_guides_view           | GET, POST   | audio_guides.html         | audioguides: list of dict, filter_language: str, filtered_guides: list of dict (POST)                             |
| /register-event/<int:event_id> | register_event              | POST        | -                         | Redirect/JSON response after registering an event                   |
| /cancel-registration/<int:registration_id> | cancel_registration          | POST        | -                         | Redirect/JSON response after cancelling registration                 |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: `dashboard.html`
- Page Title: `Museum Dashboard`
- Main Heading: `<h1 id="dashboard-page">Museum Dashboard</h1>`
- Element IDs:
  - `dashboard-page` (div, container)
  - `exhibition-summary` (div, shows total and active exhibitions count)
  - `artifact-catalog-button` (button, navigates to artifact catalog page)
  - `exhibitions-button` (button, navigates to exhibitions page)
  - `visitor-tickets-button` (button, navigates to visitor tickets page)
  - `virtual-events-button` (button, navigates to virtual events page)
  - `audio-guides-button` (button, navigates to audio guides page)
- Navigation Button to Route Map:
  - `artifact-catalog-button` -> `url_for('artifact_catalog_view')`
  - `exhibitions-button` -> `url_for('exhibitions_view')`
  - `visitor-tickets-button` -> `url_for('visitor_tickets_view')`
  - `virtual-events-button` -> `url_for('virtual_events_view')`
  - `audio-guides-button` -> `url_for('audio_guides_view')`
- Context Variables:
  - `exhibitions_count` (int): total number of exhibitions
  - `active_exhibitions_count` (int): count of exhibitions currently active


### 2. artifact_catalog.html
- Filename: `artifact_catalog.html`
- Page Title: `Artifact Catalog`
- Main Heading: `<h1 id="artifact-catalog-page">Artifact Catalog</h1>`
- Element IDs:
  - `artifact-catalog-page` (div, container)
  - `artifact-table` (table with columns: ID, name, period, origin, exhibition, actions)
  - `search-artifact` (input field for searching by name or ID)
  - `apply-artifact-filter` (button to apply search/filter)
  - `back-to-dashboard` (button to navigate back)
- Navigation Button Map:
  - `back-to-dashboard` -> `url_for('dashboard_view')`
- Context Variables:
  - `artifacts` (list of dict): all artifact data
  - `filtered_artifacts` (list of dict): search-filtered artifacts if POST
  - `search_query` (str): current search query


### 3. exhibitions.html
- Filename: `exhibitions.html`
- Page Title: `Exhibitions`
- Main Heading: `<h1 id="exhibitions-page">Exhibitions</h1>`
- Element IDs:
  - `exhibitions-page` (div, container)
  - `exhibition-list` (table showing exhibitions with columns: title, type, dates, gallery, status)
  - `filter-exhibition-type` (dropdown with options: Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (button to apply filter)
  - `back-to-dashboard` (button to navigate back)
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` (button per exhibition row to view details)
- Navigation Button Map:
  - `back-to-dashboard` -> `url_for('dashboard_view')`
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` -> `url_for('exhibition_details_view', exhibition_id=exhibition.exhibition_id)`
- Context Variables:
  - `exhibitions` (list of dict): all exhibitions
  - `filtered_exhibitions` (list of dict): filtered exhibitions
  - `exhibition_types` (list[str]): ["Permanent", "Temporary", "Virtual"]


### 4. exhibition_details.html
- Filename: `exhibition_details.html`
- Page Title: `Exhibition Details`
- Main Heading: `<h1 id="exhibition-title">{{ exhibition.title }}</h1>`
- Element IDs:
  - `exhibition-details-page` (div, container)
  - `exhibition-title` (h1, displays exhibition title)
  - `exhibition-description` (div, shows exhibition description)
  - `exhibition-dates` (div, start and end dates)
  - `exhibition-artifacts` (table, lists artifacts in exhibition)
  - `back-to-exhibitions` (button, navigates back to exhibitions list)
- Navigation Button Map:
  - `back-to-exhibitions` -> `url_for('exhibitions_view')`
- Context Variables:
  - `exhibition` (dict): exhibition details
  - `artifacts` (list of dict): artifacts associated with this exhibition


### 5. visitor_tickets.html
- Filename: `visitor_tickets.html`
- Page Title: `Visitor Tickets`
- Main Heading: `<h1 id="visitor-tickets-page">Visitor Tickets</h1>`
- Element IDs:
  - `visitor-tickets-page` (div, container)
  - `ticket-type` (dropdown with options: Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (input type number)
  - `purchase-ticket-button` (button to purchase tickets)
  - `my-tickets-table` (table listing user's purchased tickets)
  - `back-to-dashboard` (button to navigate back)
- Navigation Button Map:
  - `back-to-dashboard` -> `url_for('dashboard_view')`
- Context Variables:
  - `tickets` (list of dict): tickets purchased by the current user
  - `ticket_types` (list[str]): ["Standard", "Student", "Senior", "Family", "VIP"]
  - `purchase_result` (str, optional): success/failure message after purchase


### 6. virtual_events.html
- Filename: `virtual_events.html`
- Page Title: `Virtual Events`
- Main Heading: `<h1 id="virtual-events-page">Virtual Events</h1>`
- Element IDs:
  - `virtual-events-page` (div, container)
  - `event-list` (table with columns: title, date, time, type, registration status)
  - `register-event-button-{{ event.event_id }}` (button per event row to register)
  - `cancel-registration-button-{{ registration.registration_id }}` (button per registration row to cancel)
  - `back-to-dashboard` (button to navigate back)
- Navigation Button Map:
  - `back-to-dashboard` -> `url_for('dashboard_view')`
- Context Variables:
  - `events` (list of dict): all events
  - `event_registrations` (list of dict): all event registrations
  - `user_registrations` (set of int): IDs of registrations for current user


### 7. audio_guides.html
- Filename: `audio_guides.html`
- Page Title: `Audio Guides`
- Main Heading: `<h1 id="audio-guides-page">Audio Guides</h1>`
- Element IDs:
  - `audio-guides-page` (div, container)
  - `audio-guide-list` (table with columns: exhibit number, title, language, duration)
  - `filter-language` (dropdown with options: English, Spanish, French)
  - `apply-language-filter` (button to apply language filter)
  - `play-guide-button-{{ guide.guide_id }}` (button per audio guide row to play guide)
  - `back-to-dashboard` (button to navigate back)
- Navigation Button Map:
  - `back-to-dashboard` -> `url_for('dashboard_view')`
- Context Variables:
  - `audioguides` (list of dict): all audio guides
  - `filter_language` (str): current language filter
  - `filtered_guides` (list of dict): filtered audio guides

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: `data/users.txt`
- Purpose: Stores usernames for user authentication
- Format: Pipe (`|`) delimited single field
- Fields:
  - `username` (str)
- Example:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

---

### 2. galleries.txt
- Filename: `data/galleries.txt`
- Purpose: Stores detailed gallery information
- Format: Pipe-delimited
- Fields:
  - `gallery_id` (int)
  - `gallery_name` (str)
  - `floor` (int)
  - `capacity` (int)
  - `theme` (str)
  - `status` (str) - e.g., "Open", "Renovation"
- Example:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

---

### 3. exhibitions.txt
- Filename: `data/exhibitions.txt`
- Purpose: Stores exhibitions data
- Format: Pipe-delimited
- Fields:
  - `exhibition_id` (int)
  - `title` (str)
  - `description` (str)
  - `gallery_id` (int)
  - `exhibition_type` (str) - Permanent, Temporary, Virtual
  - `start_date` (date, YYYY-MM-DD)
  - `end_date` (date, YYYY-MM-DD)
  - `curator_name` (str)
  - `created_by` (str, username)
- Example:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

---

### 4. artifacts.txt
- Filename: `data/artifacts.txt`
- Purpose: Stores artifact collection details
- Format: Pipe-delimited
- Fields:
  - `artifact_id` (int)
  - `artifact_name` (str)
  - `period` (str)
  - `origin` (str)
  - `description` (str)
  - `exhibition_id` (int)
  - `storage_location` (str)
  - `acquisition_date` (date, YYYY-MM-DD)
  - `added_by` (str, username)
- Example:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

---

### 5. audioguides.txt
- Filename: `data/audioguides.txt`
- Purpose: Stores audio guide information for exhibits
- Format: Pipe-delimited
- Fields:
  - `guide_id` (int)
  - `exhibit_number` (int)
  - `title` (str)
  - `language` (str) - English, Spanish, French
  - `duration` (int) - duration in minutes
  - `script` (str)
  - `narrator` (str)
  - `created_by` (str, username)
- Example:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

---

### 6. tickets.txt
- Filename: `data/tickets.txt`
- Purpose: Stores visitor ticket purchases
- Format: Pipe-delimited
- Fields:
  - `ticket_id` (int)
  - `username` (str)
  - `ticket_type` (str) - Standard, Student, Senior, Family, VIP
  - `visit_date` (date, YYYY-MM-DD)
  - `visit_time` (str, e.g., "11:00 AM")
  - `number_of_tickets` (int)
  - `price` (int/float)
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
- Purpose: Stores virtual museum event information
- Format: Pipe-delimited
- Fields:
  - `event_id` (int)
  - `title` (str)
  - `date` (date, YYYY-MM-DD)
  - `time` (str, e.g. "2:00 PM")
  - `event_type` (str) - Webinar, Artist Talk, Virtual Tour
  - `speaker` (str)
  - `capacity` (int)
  - `description` (str)
  - `created_by` (str, username)
- Example:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

---

### 8. event_registrations.txt
- Filename: `data/event_registrations.txt`
- Purpose: Stores registration records for virtual events
- Format: Pipe-delimited
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
- Purpose: Logs artifact collection activities
- Format: Pipe-delimited
- Fields:
  - `log_id` (int)
  - `artifact_id` (int)
  - `activity_type` (str) - e.g., Inspection, Cleaning, Photography, Restoration
  - `date` (date, YYYY-MM-DD)
  - `notes` (str)
  - `condition` (str) - condition report
  - `curator` (str) - username responsible
- Example:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

# End of Design Specification
