# VirtualMuseum System Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name           | HTTP Method(s) | Template Filename           | Context Variables (name: type)                                |
|-------------------------------|------------------------|----------------|-----------------------------|---------------------------------------------------------------|
| /                             | root_redirect          | GET            | N/A (Redirect)              | N/A                                                           |
| /dashboard                    | dashboard_page         | GET            | dashboard.html              | total_exhibitions: int, active_exhibitions: int               |
| /artifacts                   | artifact_catalog       | GET, POST      | artifact_catalog.html       | artifacts: list of dict, filter_query: str (optional)         |
| /exhibitions                 | exhibitions_list       | GET, POST      | exhibitions.html            | exhibitions: list of dict, filter_type: str (optional)         |
| /exhibition/<int:exhibition_id> | exhibition_details    | GET            | exhibition_details.html     | exhibition: dict, artifacts: list of dict                      |
| /tickets                    | visitor_tickets        | GET, POST      | visitor_tickets.html        | tickets: list of dict (user tickets), ticket_types: list[str] |
| /events                     | virtual_events         | GET, POST      | virtual_events.html         | events: list of dict, registrations: list of dict (user reg)  |
| /audio-guides               | audio_guides           | GET, POST      | audio_guides.html           | audio_guides: list of dict, filter_language: str (optional)   |

---

## Section 2: HTML Templates Specification

### Template: dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main Heading (<h1>): Museum Dashboard
- Element IDs:
  - dashboard-page (div)
  - exhibition-summary (div)
  - artifact-catalog-button (button)
  - exhibitions-button (button)
  - visitor-tickets-button (button)
  - virtual-events-button (button)
  - audio-guides-button (button)
- Navigation Buttons Mapping:
  - artifact-catalog-button: url_for('artifact_catalog')
  - exhibitions-button: url_for('exhibitions_list')
  - visitor-tickets-button: url_for('visitor_tickets')
  - virtual-events-button: url_for('virtual_events')
  - audio-guides-button: url_for('audio_guides')
- Context Variables:
  - total_exhibitions (int): Total number of exhibitions
  - active_exhibitions (int): Count of active exhibitions

### Template: artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main Heading (<h1>): Artifact Catalog
- Element IDs:
  - artifact-catalog-page (div)
  - artifact-table (table)
  - search-artifact (input)
  - apply-artifact-filter (button)
  - back-to-dashboard (button)
- Navigation Buttons Mapping:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - artifacts (list of dict): List of artifacts; each dict contains fields as per data schema
  - filter_query (str, optional): Current search/filter query

### Template: exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main Heading (<h1>): Exhibitions
- Element IDs:
  - exhibitions-page (div)
  - exhibition-list (table)
  - filter-exhibition-type (dropdown/select)
  - apply-exhibition-filter (button)
  - back-to-dashboard (button)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (button for each exhibition row)
- Navigation Buttons Mapping:
  - back-to-dashboard: url_for('dashboard_page')
  - view-exhibition-button-{{ exhibition.exhibition_id }}: url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- Context Variables:
  - exhibitions (list of dict): List of exhibitions with all relevant fields
  - filter_type (str, optional): Current exhibition filter type

### Template: exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main Heading (<h1>): (value of exhibition.title)
- Element IDs:
  - exhibition-details-page (div)
  - exhibition-title (h1)
  - exhibition-description (div)
  - exhibition-dates (div)
  - exhibition-artifacts (table)
  - back-to-exhibitions (button)
- Navigation Buttons Mapping:
  - back-to-exhibitions: url_for('exhibitions_list')
- Context Variables:
  - exhibition (dict): Exhibition details matching data schema
  - artifacts (list of dict): Artifacts associated with the exhibition

### Template: visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main Heading (<h1>): Visitor Tickets
- Element IDs:
  - visitor-tickets-page (div)
  - ticket-type (dropdown/select)
  - number-of-tickets (input, number)
  - purchase-ticket-button (button)
  - my-tickets-table (table)
  - back-to-dashboard (button)
- Navigation Buttons Mapping:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - tickets (list of dict): User purchased tickets
  - ticket_types (list of str): ['Standard', 'Student', 'Senior', 'Family', 'VIP']

### Template: virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main Heading (<h1>): Virtual Events
- Element IDs:
  - virtual-events-page (div)
  - event-list (table)
  - register-event-button-{{ event.event_id }} (button for each event row)
  - cancel-registration-button-{{ registration.registration_id }} (button for each registration row)
  - back-to-dashboard (button)
- Navigation Buttons Mapping:
  - back-to-dashboard: url_for('dashboard_page')
  - register-event-button-{{ event.event_id }}: url_for('virtual_events') [POST for registration action]
  - cancel-registration-button-{{ registration.registration_id }}: url_for('virtual_events') [POST for cancellation action]
- Context Variables:
  - events (list of dict): All virtual events
  - registrations (list of dict): User's event registrations

### Template: audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main Heading (<h1>): Audio Guides
- Element IDs:
  - audio-guides-page (div)
  - audio-guide-list (table)
  - filter-language (dropdown/select)
  - apply-language-filter (button)
  - play-guide-button-{{ guide.guide_id }} (button for each audio guide row)
  - back-to-dashboard (button)
- Navigation Buttons Mapping:
  - back-to-dashboard: url_for('dashboard_page')
  - apply-language-filter: url_for('audio_guides') [POST]
  - play-guide-button-{{ guide.guide_id }}: url_for('audio_guides') [POST to play/select guide]
- Context Variables:
  - audio_guides (list of dict): Audio guide records
  - filter_language (str, optional): Current language filter

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Purpose: Store usernames for authentication and user tracking.
- Fields (pipe-delimited):
  - username
- Example rows:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- Filename: data/galleries.txt
- Purpose: Store details about museum galleries.
- Fields (pipe-delimited):
  - gallery_id
  - gallery_name
  - floor
  - capacity
  - theme
  - status
- Example rows:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Purpose: Store exhibition records and metadata.
- Fields (pipe-delimited):
  - exhibition_id
  - title
  - description
  - gallery_id
  - exhibition_type
  - start_date
  - end_date
  - curator_name
  - created_by
- Example rows:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Purpose: Store artifact information linked to exhibitions.
- Fields (pipe-delimited):
  - artifact_id
  - artifact_name
  - period
  - origin
  - description
  - exhibition_id
  - storage_location
  - acquisition_date
  - added_by
- Example rows:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Purpose: Store audio guide metadata and scripts.
- Fields (pipe-delimited):
  - guide_id
  - exhibit_number
  - title
  - language
  - duration
  - script
  - narrator
  - created_by
- Example rows:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- Filename: data/tickets.txt
- Purpose: Store visitor ticket purchases and details.
- Fields (pipe-delimited):
  - ticket_id
  - username
  - ticket_type
  - visit_date
  - visit_time
  - number_of_tickets
  - price
  - visitor_name
  - visitor_email
  - purchase_date
- Example rows:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- Filename: data/events.txt
- Purpose: Store virtual museum event details.
- Fields (pipe-delimited):
  - event_id
  - title
  - date
  - time
  - event_type
  - speaker
  - capacity
  - description
  - created_by
- Example rows:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Purpose: Store user registrations for events.
- Fields (pipe-delimited):
  - registration_id
  - event_id
  - username
  - registration_date
- Example rows:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Purpose: Log activities and conditions on artifacts.
- Fields (pipe-delimited):
  - log_id
  - artifact_id
  - activity_type
  - date
  - notes
  - condition
  - curator
- Example rows:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This specification document fully enables parallel backend and frontend development. Backend developers can implement route handlers and data processing strictly adhering to Section 1 and 3, while frontend developers can create the templates as per Section 2 without ambiguity. Element IDs, function names, context variables, and data schemas are consistent and complete as required.
