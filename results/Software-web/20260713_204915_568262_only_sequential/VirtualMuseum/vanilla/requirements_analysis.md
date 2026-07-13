# VirtualMuseum Web Application Requirements Analysis

## 1. Page Designs and Elements

### 1. Dashboard Page
- Page Title: Museum Dashboard
- Container ID: `dashboard-page` (Div)
- Elements:
  - `exhibition-summary` (Div) - Summary showing total exhibitions, active exhibitions count
  - `artifact-catalog-button` (Button) - Navigate to Artifact Catalog Page
  - `exhibitions-button` (Button) - Navigate to Exhibitions Page
  - `visitor-tickets-button` (Button) - Navigate to Visitor Tickets Page
  - `virtual-events-button` (Button) - Navigate to Virtual Events Page
  - `audio-guides-button` (Button) - Navigate to Audio Guides Page

### 2. Artifact Catalog Page
- Page Title: Artifact Catalog
- Container ID: `artifact-catalog-page` (Div)
- Elements:
  - `artifact-table` (Table) - Columns: ID, name, period, origin, exhibition, actions
  - `search-artifact` (Input) - Search artifacts by name or ID
  - `apply-artifact-filter` (Button) - Apply filters
  - `back-to-dashboard` (Button) - Navigate back to Dashboard Page

### 3. Exhibitions Page
- Page Title: Exhibitions
- Container ID: `exhibitions-page` (Div)
- Elements:
  - `exhibition-list` (Table) - Columns: title, type, dates, gallery, status
  - `filter-exhibition-type` (Dropdown) - Filter by Exhibition Type (Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (Button) - Apply exhibition filter
  - `view-exhibition-button-{exhibition_id}` (Button) - View exhibition details; unique per exhibition row
  - `back-to-dashboard` (Button) - Navigate back to Dashboard Page

### 4. Exhibition Details Page
- Page Title: Exhibition Details
- Container ID: `exhibition-details-page` (Div)
- Elements:
  - `exhibition-title` (H1) - Exhibition title
  - `exhibition-description` (Div) - Exhibition description
  - `exhibition-dates` (Div) - Start and end dates
  - `exhibition-artifacts` (Table) - Artifacts in the exhibition
  - `back-to-exhibitions` (Button) - Navigate back to Exhibitions Page

### 5. Visitor Tickets Page
- Page Title: Visitor Tickets
- Container ID: `visitor-tickets-page` (Div)
- Elements:
  - `ticket-type` (Dropdown) - Select ticket type (Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (Input number) - Input number of tickets
  - `purchase-ticket-button` (Button) - Purchase tickets
  - `my-tickets-table` (Table) - Display user's purchased tickets
  - `back-to-dashboard` (Button) - Navigate back to Dashboard Page

### 6. Virtual Events Page
- Page Title: Virtual Events
- Container ID: `virtual-events-page` (Div)
- Elements:
  - `event-list` (Table) - Columns: title, date, time, type, registration status
  - `register-event-button-{event_id}` (Button) - Register for an event; unique per event row
  - `cancel-registration-button-{registration_id}` (Button) - Cancel registration; unique per registered event row
  - `back-to-dashboard` (Button) - Navigate back to Dashboard Page

### 7. Audio Guides Page
- Page Title: Audio Guides
- Container ID: `audio-guides-page` (Div)
- Elements:
  - `audio-guide-list` (Table) - Columns: exhibit number, title, language, duration
  - `filter-language` (Dropdown) - Filter by language (English, Spanish, French)
  - `apply-language-filter` (Button) - Apply language filter
  - `play-guide-button-{guide_id}` (Button) - Play audio guide; unique per guide row
  - `back-to-dashboard` (Button) - Navigate back to Dashboard Page

## 2. Navigation Flow
- From Dashboard:
  - `artifact-catalog-button` → Artifact Catalog Page
  - `exhibitions-button` → Exhibitions Page
  - `visitor-tickets-button` → Visitor Tickets Page
  - `virtual-events-button` → Virtual Events Page
  - `audio-guides-button` → Audio Guides Page
- From Artifact Catalog Page:
  - `back-to-dashboard` → Dashboard Page
- From Exhibitions Page:
  - `view-exhibition-button-{exhibition_id}` → Exhibition Details Page
  - `back-to-dashboard` → Dashboard Page
- From Exhibition Details Page:
  - `back-to-exhibitions` → Exhibitions Page
- From Visitor Tickets Page:
  - `back-to-dashboard` → Dashboard Page
- From Virtual Events Page:
  - `back-to-dashboard` → Dashboard Page
- From Audio Guides Page:
  - `back-to-dashboard` → Dashboard Page

## 3. Data Storage Specifications

All data files stored locally in the `data` directory using pipe (`|`) delimiter except for users.txt which is line based.

### 1. User Authentication Data
- Filename: `users.txt`
- Fields:
  - username
- Format: Single field per line
- Sample Data:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Gallery Data
- Filename: `galleries.txt`
- Fields (pipe `|` delimited):
  1. gallery_id
  2. gallery_name
  3. floor
  4. capacity
  5. theme
  6. status
- Sample Data:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibition Data
- Filename: `exhibitions.txt`
- Fields (pipe `|` delimited):
  1. exhibition_id
  2. title
  3. description
  4. gallery_id
  5. exhibition_type
  6. start_date (YYYY-MM-DD)
  7. end_date (YYYY-MM-DD)
  8. curator_name
  9. created_by
- Sample Data:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifact Data
- Filename: `artifacts.txt`
- Fields (pipe `|` delimited):
  1. artifact_id
  2. artifact_name
  3. period
  4. origin
  5. description
  6. exhibition_id
  7. storage_location
  8. acquisition_date (YYYY-MM-DD)
  9. added_by
- Sample Data:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guide Data
- Filename: `audioguides.txt`
- Fields (pipe `|` delimited):
  1. guide_id
  2. exhibit_number
  3. title
  4. language
  5. duration (minutes)
  6. script
  7. narrator
  8. created_by
- Sample Data:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Ticket Data
- Filename: `tickets.txt`
- Fields (pipe `|` delimited):
  1. ticket_id
  2. username
  3. ticket_type
  4. visit_date (YYYY-MM-DD)
  5. visit_time (hh:mm AM/PM)
  6. number_of_tickets
  7. price
  8. visitor_name
  9. visitor_email
  10. purchase_date (YYYY-MM-DD)
- Sample Data:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Event Data
- Filename: `events.txt`
- Fields (pipe `|` delimited):
  1. event_id
  2. title
  3. date (YYYY-MM-DD)
  4. time (hh:mm AM/PM)
  5. event_type
  6. speaker
  7. capacity
  8. description
  9. created_by
- Sample Data:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registration Data
- Filename: `event_registrations.txt`
- Fields (pipe `|` delimited):
  1. registration_id
  2. event_id
  3. username
  4. registration_date (YYYY-MM-DD)
- Sample Data:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Log Data
- Filename: `collection_logs.txt`
- Fields (pipe `|` delimited):
  1. log_id
  2. artifact_id
  3. activity_type
  4. date (YYYY-MM-DD)
  5. notes
  6. condition
  7. curator
- Sample Data:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```
