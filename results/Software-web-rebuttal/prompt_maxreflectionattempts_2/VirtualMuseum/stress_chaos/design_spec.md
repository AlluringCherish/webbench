# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path | Function Name | HTTP Method | Template Filename | Context Variables |
|---|---|---|---|---|
| / | root_redirect | GET | Redirect to /dashboard | None |
| /dashboard | dashboard | GET | dashboard.html | exhibitions_summary: dict (keys: total_exhibitions:int, active_exhibitions:int), exhibitions: list(dict), artifacts: list(dict) |
| /artifact-catalog | artifact_catalog | GET, POST | artifact_catalog.html | artifacts: list(dict), search_query: str (optional), filters: dict (optional) |
| /exhibitions | exhibitions | GET, POST | exhibitions.html | exhibitions: list(dict), exhibition_types: list(str), selected_exhibition_type: str (optional) |
| /exhibition/<int:exhibition_id> | exhibition_details | GET | exhibition_details.html | exhibition: dict, artifacts: list(dict) |
| /visitor-tickets | visitor_tickets | GET, POST | visitor_tickets.html | ticket_types: list(str), my_tickets: list(dict) |
| /virtual-events | virtual_events | GET, POST | virtual_events.html | events: list(dict), registrations: list(dict), user_registrations: list(dict) |
| /audio-guides | audio_guides | GET, POST | audio_guides.html | audio_guides: list(dict), languages: list(str), selected_language: str (optional) |

---

### Route Details

- **Root Route (/) :**
  - Redirects to `/dashboard`.

- **Dashboard (/dashboard) :**
  - GET: Displays main dashboard.
  - Context:
    - `exhibitions_summary` (dict): counts of total and active exhibitions.
    - `exhibitions` (list of dict): brief list of exhibitions for summary or future extensions.
    - `artifacts` (list of dict): optional list for summaries.

- **Artifact Catalog (/artifact-catalog) :**
  - GET: Display all artifacts.
  - POST: Handle search/filter forms.
  - Context:
    - `artifacts` (list of dict): filtered or full artifacts list.
    - `search_query` (str): search text input.
    - `filters` (dict): filter criteria.

- **Exhibitions (/exhibitions) :**
  - GET: Show all exhibitions.
  - POST: Filter by exhibition_type.
  - Context:
    - `exhibitions` (list of dict): list of all or filtered exhibitions.
    - `exhibition_types` (list of str): ['Permanent', 'Temporary', 'Virtual'].
    - `selected_exhibition_type` (str): current filter selection.

- **Exhibition Details (/exhibition/<int:exhibition_id>) :**
  - GET: Show details for specific exhibition.
  - Context:
    - `exhibition` (dict): detailed exhibition info.
    - `artifacts` (list of dict): artifacts belonging to this exhibition.

- **Visitor Tickets (/visitor-tickets) :**
  - GET: Show ticket purchase form and user's tickets.
  - POST: Process ticket purchase.
  - Context:
    - `ticket_types` (list of str): ['Standard', 'Student', 'Senior', 'Family', 'VIP'].
    - `my_tickets` (list of dict): tickets purchased by the current user.

- **Virtual Events (/virtual-events) :**
  - GET: List all virtual events & user registrations.
  - POST: Register or cancel event registration.
  - Context:
    - `events` (list of dict): events information.
    - `registrations` (list of dict): all registrations.
    - `user_registrations` (list of dict): registrations for current user.

- **Audio Guides (/audio-guides) :**
  - GET: List all audio guides (with optional filtering).
  - POST: Apply language filter.
  - Context:
    - `audio_guides` (list of dict): audio guides list.
    - `languages` (list of str): ['English', 'Spanish', 'French'].
    - `selected_language` (str): selected filtering language.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main Heading: Museum Dashboard (h1 with id="dashboard-page")
- Element IDs:
  - dashboard-page (div): container for dashboard
  - exhibition-summary (div): exhibition total and active counts
  - artifact-catalog-button (button): navigate to artifact catalog
  - exhibitions-button (button): navigate to exhibitions page
  - visitor-tickets-button (button): navigate to visitor tickets
  - virtual-events-button (button): navigate to virtual events
  - audio-guides-button (button): navigate to audio guides
- Navigation Button Mappings:
  - artifact-catalog-button: url_for('artifact_catalog')
  - exhibitions-button: url_for('exhibitions')
  - visitor-tickets-button: url_for('visitor_tickets')
  - virtual-events-button: url_for('virtual_events')
  - audio-guides-button: url_for('audio_guides')
- Context Variables:
  - exhibitions_summary (dict): {total_exhibitions: int, active_exhibitions: int}
  - exhibitions (list of dict)
  - artifacts (list of dict)

### 2. artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main Heading: Artifact Catalog (h1 id="artifact-catalog-page")
- Element IDs:
  - artifact-catalog-page (div)
  - artifact-table (table): lists artifacts (columns: ID, name, period, origin, exhibition, actions)
  - search-artifact (input, text): searchbar
  - apply-artifact-filter (button): apply filter button
  - back-to-dashboard (button): navigate back
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - artifacts (list of dict)
  - search_query (str)
  - filters (dict)

### 3. exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main Heading: Exhibitions (h1 id="exhibitions-page")
- Element IDs:
  - exhibitions-page (div)
  - exhibition-list (table): shows exhibitions with columns: title, type, dates, gallery, status
  - filter-exhibition-type (select dropdown): options - Permanent, Temporary, Virtual
  - apply-exhibition-filter (button)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (button) - dynamic
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }}: url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- Context Variables:
  - exhibitions (list of dict)
  - exhibition_types (list of str)
  - selected_exhibition_type (str)

### 4. exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main Heading: exhibition.title (h1 id="exhibition-title")
- Element IDs:
  - exhibition-details-page (div)
  - exhibition-title (h1)
  - exhibition-description (div)
  - exhibition-dates (div)
  - exhibition-artifacts (table): artifacts in exhibition
  - back-to-exhibitions (button)
- Navigation Button Mappings:
  - back-to-exhibitions: url_for('exhibitions')
- Context Variables:
  - exhibition (dict)
  - artifacts (list of dict)

### 5. visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main Heading: Visitor Tickets (h1 id="visitor-tickets-page")
- Element IDs:
  - visitor-tickets-page (div)
  - ticket-type (select dropdown): Standard, Student, Senior, Family, VIP
  - number-of-tickets (input, number)
  - purchase-ticket-button (button)
  - my-tickets-table (table): user purchased tickets
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - ticket_types (list of str)
  - my_tickets (list of dict)

### 6. virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main Heading: Virtual Events (h1 id="virtual-events-page")
- Element IDs:
  - virtual-events-page (div)
  - event-list (table): shows events with columns: title, date, time, type, registration status
  - register-event-button-{{ event.event_id }} (button) - dynamic
  - cancel-registration-button-{{ registration.registration_id }} (button) - dynamic
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard')
  - register-event-button-{{ event.event_id }}: url_for('virtual_events') (POST register)
  - cancel-registration-button-{{ registration.registration_id }}: url_for('virtual_events') (POST cancel)
- Context Variables:
  - events (list of dict)
  - registrations (list of dict)
  - user_registrations (list of dict)

### 7. audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main Heading: Audio Guides (h1 id="audio-guides-page")
- Element IDs:
  - audio-guides-page (div)
  - audio-guide-list (table): columns: exhibit number, title, language, duration
  - filter-language (select dropdown): English, Spanish, French
  - apply-language-filter (button)
  - play-guide-button-{{ guide.guide_id }} (button) - dynamic
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard')
  - apply-language-filter: url_for('audio_guides') (POST apply filter)
  - play-guide-button-{{ guide.guide_id }}: url_for('audio_guides') (POST play)
- Context Variables:
  - audio_guides (list of dict)
  - languages (list of str)
  - selected_language (str)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Purpose: User authentication usernames
- Format: username
- Example Data:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- Filename: data/galleries.txt
- Purpose: Museum gallery details
- Format (pipe-delimited): gallery_id|gallery_name|floor|capacity|theme|status
- Example Data:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Purpose: Exhibitions information
- Format (pipe-delimited): exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Example Data:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Purpose: Artifacts in the museum
- Format (pipe-delimited): artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Example Data:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Purpose: Audio guide details
- Format (pipe-delimited): guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Example Data:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- Filename: data/tickets.txt
- Purpose: Visitor tickets records
- Format (pipe-delimited): ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Example Data:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- Filename: data/events.txt
- Purpose: Virtual museum events
- Format (pipe-delimited): event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Example Data:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Purpose: User registrations for events
- Format (pipe-delimited): registration_id|event_id|username|registration_date
- Example Data:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Purpose: Logs of artifact collection activities
- Format (pipe-delimited): log_id|artifact_id|activity_type|date|notes|condition|curator
- Example Data:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

# End of VirtualMuseum Design Specification Document
