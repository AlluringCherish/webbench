# VirtualMuseum System Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name             | HTTP Method | Template Filename       | Context Variables (Name: Type)                                      |
|-------------------------------|---------------------------|-------------|-------------------------|---------------------------------------------------------------------|
| /                             | root_redirect             | GET         | N/A (Redirect to /dashboard) | None                                                                |
| /dashboard                    | dashboard                 | GET         | dashboard.html           | exhibitions: list(dict), artifacts: list(dict) - for summary counts |
| /artifacts                   | artifact_catalog          | GET, POST   | artifact_catalog.html    | artifacts: list(dict), search_query: str (if POST), filtered_artifacts: list(dict)       |
| /exhibitions                 | exhibitions               | GET, POST   | exhibitions.html         | exhibitions: list(dict), filter_type: str (optional)                |
| /exhibition/<int:exhibition_id> | exhibition_details        | GET         | exhibition_details.html  | exhibition: dict, artifacts: list(dict)                            |
| /tickets                    | visitor_tickets           | GET, POST   | visitor_tickets.html     | tickets: list(dict), ticket_types: list(str), purchase_status: str (optional)             |
| /events                     | virtual_events            | GET, POST   | virtual_events.html      | events: list(dict), registrations: list(dict), user_registrations: list(dict)             |
| /audio-guides               | audio_guides              | GET, POST   | audio_guides.html        | audioguides: list(dict), filter_language: str (optional)             |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- **Page Title:** Museum Dashboard
- **Main <h1>:** Museum Dashboard
- **Element IDs:**
  - dashboard-page (Div)
  - exhibition-summary (Div)
  - artifact-catalog-button (Button) - nav to artifact_catalog
  - exhibitions-button (Button) - nav to exhibitions
  - visitor-tickets-button (Button) - nav to visitor_tickets
  - virtual-events-button (Button) - nav to virtual_events
  - audio-guides-button (Button) - nav to audio_guides
- **Navigation Button Mappings:**
  - artifact-catalog-button: url_for('artifact_catalog')
  - exhibitions-button: url_for('exhibitions')
  - visitor-tickets-button: url_for('visitor_tickets')
  - virtual-events-button: url_for('virtual_events')
  - audio-guides-button: url_for('audio_guides')
- **Context Variables:**
  - exhibitions: list(dict) - list of exhibitions to summarize counts
  - artifacts: list(dict) - list of artifacts for summary

### 2. artifact_catalog.html
- **Page Title:** Artifact Catalog
- **Main <h1>:** Artifact Catalog
- **Element IDs:**
  - artifact-catalog-page (Div)
  - artifact-table (Table) - shows artifact details
  - search-artifact (Input) - search box for artifact name or ID
  - apply-artifact-filter (Button) - to apply search/filter
  - back-to-dashboard (Button) - nav back to dashboard
- **Navigation Button Mappings:**
  - back-to-dashboard: url_for('dashboard')
- **Context Variables:**
  - artifacts: list(dict) - all artifacts
  - search_query: str (optional) - current search input
  - filtered_artifacts: list(dict) - results after search/filter

### 3. exhibitions.html
- **Page Title:** Exhibitions
- **Main <h1>:** Exhibitions
- **Element IDs:**
  - exhibitions-page (Div)
  - exhibition-list (Table) - all exhibitions with details
  - filter-exhibition-type (Dropdown) - filter by exhibition type
  - apply-exhibition-filter (Button) - apply filter
  - view-exhibition-button-{{ exhibition.exhibition_id }} (Button) - view details per exhibition
  - back-to-dashboard (Button) - nav back to dashboard
- **Navigation Button Mappings:**
  - back-to-dashboard: url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }}: url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- **Context Variables:**
  - exhibitions: list(dict) - all exhibitions
  - filter_type: str (optional) - currently applied filter

### 4. exhibition_details.html
- **Page Title:** Exhibition Details
- **Main <h1>:** exhibition_title (exhibition.title)
- **Element IDs:**
  - exhibition-details-page (Div)
  - exhibition-title (H1)
  - exhibition-description (Div)
  - exhibition-dates (Div)
  - exhibition-artifacts (Table)
  - back-to-exhibitions (Button) - nav back to exhibitions
- **Navigation Button Mappings:**
  - back-to-exhibitions: url_for('exhibitions')
- **Context Variables:**
  - exhibition: dict - showing all exhibition details
  - artifacts: list(dict) - artifacts in the exhibition

### 5. visitor_tickets.html
- **Page Title:** Visitor Tickets
- **Main <h1>:** Visitor Tickets
- **Element IDs:**
  - visitor-tickets-page (Div)
  - ticket-type (Dropdown) - select ticket type
  - number-of-tickets (Input number) - quantity field
  - purchase-ticket-button (Button) - to purchase tickets
  - my-tickets-table (Table) - showing purchased tickets
  - back-to-dashboard (Button) - nav back to dashboard
- **Navigation Button Mappings:**
  - back-to-dashboard: url_for('dashboard')
- **Context Variables:**
  - tickets: list(dict) - user's purchased tickets
  - ticket_types: list(str) - available ticket types
  - purchase_status: str (optional) - status message after purchase

### 6. virtual_events.html
- **Page Title:** Virtual Events
- **Main <h1>:** Virtual Events
- **Element IDs:**
  - virtual-events-page (Div)
  - event-list (Table) - all events with details
  - register-event-button-{{ event.event_id }} (Button) - register for event
  - cancel-registration-button-{{ registration.registration_id }} (Button) - cancel registration
  - back-to-dashboard (Button) - nav back to dashboard
- **Navigation Button Mappings:**
  - back-to-dashboard: url_for('dashboard')
  - register-event-button-{{ event.event_id }}: url_for('virtual_events')  # POST action handled on same page
  - cancel-registration-button-{{ registration.registration_id }}: url_for('virtual_events')  # POST actions
- **Context Variables:**
  - events: list(dict) - all events
  - registrations: list(dict) - all event registrations
  - user_registrations: list(dict) - registrations for current user

### 7. audio_guides.html
- **Page Title:** Audio Guides
- **Main <h1>:** Audio Guides
- **Element IDs:**
  - audio-guides-page (Div)
  - audio-guide-list (Table) - list of audio guides
  - filter-language (Dropdown) - filter by language
  - apply-language-filter (Button) - apply language filter
  - play-guide-button-{{ guide.guide_id }} (Button) - play guide
  - back-to-dashboard (Button) - nav back to dashboard
- **Navigation Button Mappings:**
  - back-to-dashboard: url_for('dashboard')
  - apply-language-filter: url_for('audio_guides')  # POST for filtering
  - play-guide-button-{{ guide.guide_id }}: url_for('audio_guides')  # POST or GET action
- **Context Variables:**
  - audioguides: list(dict) - all guides
  - filter_language: str (optional) - current filter

---

## Section 3: Data File Schemas

### 1. users.txt
- **Filename:** data/users.txt
- **Fields:** username
- **Description:** Stores usernames authorized to access the system.
- **Example Rows:**
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- **Filename:** data/galleries.txt
- **Fields:** gallery_id|gallery_name|floor|capacity|theme|status
- **Description:** Information about museum galleries where exhibitions are hosted.
- **Example Rows:**
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- **Filename:** data/exhibitions.txt
- **Fields:** exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- **Description:** Details of exhibitions including type and dates.
- **Example Rows:**
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- **Filename:** data/artifacts.txt
- **Fields:** artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- **Description:** Artifact details linked to exhibitions.
- **Example Rows:**
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- **Filename:** data/audioguides.txt
- **Fields:** guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- **Description:** Audio guide metadata and content scripting.
- **Example Rows:**
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- **Filename:** data/tickets.txt
- **Fields:** ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- **Description:** Visitor tickets purchases with details.
- **Example Rows:**
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- **Filename:** data/events.txt
- **Fields:** event_id|title|date|time|event_type|speaker|capacity|description|created_by
- **Description:** Virtual events hosted by the museum.
- **Example Rows:**
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- **Filename:** data/event_registrations.txt
- **Fields:** registration_id|event_id|username|registration_date
- **Description:** User registrations for virtual events.
- **Example Rows:**
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- **Filename:** data/collection_logs.txt
- **Fields:** log_id|artifact_id|activity_type|date|notes|condition|curator
- **Description:** Logs capturing artifact activities and conditions.
- **Example Rows:**
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

*End of Design Specification Document*