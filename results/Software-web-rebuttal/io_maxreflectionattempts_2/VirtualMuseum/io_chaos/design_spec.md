# VirtualMuseum Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                         | Function Name       | HTTP Methods | Template Filename       | Context Variables                                                                                     |
|----------------------------------|---------------------|--------------|-------------------------|-----------------------------------------------------------------------------------------------------|
| /                                | root_redirect       | GET          | None (redirect to /dashboard) | None                                                                                                |
| /dashboard                      | dashboard           | GET          | dashboard.html          | exhibition_summary (dict: total_exhibitions:int, active_exhibitions:int)                            |
| /artifact_catalog               | artifact_catalog    | GET, POST    | artifact_catalog.html   | artifacts (list of dict), search_query (str, optional), filter_applied (bool)                       |
| /exhibitions                   | exhibitions         | GET, POST    | exhibitions.html        | exhibitions (list of dict), exhibition_types (list of str), selected_type (str, optional)          |
| /exhibition/<int:exhibition_id> | exhibition_details | GET          | exhibition_details.html  | exhibition (dict), artifacts (list of dict)                                                         |
| /visitor_tickets               | visitor_tickets     | GET, POST    | visitor_tickets.html    | ticket_types (list of str), purchased_tickets (list of dict), purchase_message (str, optional)     |
| /virtual_events                | virtual_events      | GET, POST    | virtual_events.html     | events (list of dict), user_registrations (list of dict), registration_message (str, optional)      |
| /audio_guides                 | audio_guides        | GET, POST    | audio_guides.html       | audio_guides (list of dict), languages (list of str), selected_language (str, optional)             |

### Route Details

- **/** (root_redirect): Redirects to `/dashboard`. GET method only.

- **/dashboard** (dashboard): GET method.
  - Renders `dashboard.html`.
  - Provides `exhibition_summary` with counts for total and active exhibitions.

- **/artifact_catalog** (artifact_catalog): GET and POST methods.
  - GET to load all artifacts.
  - POST to handle search/filter input.
  - Renders `artifact_catalog.html`.
  - Context vars include list of `artifacts`, optional `search_query`, and `filter_applied` boolean.

- **/exhibitions** (exhibitions): GET and POST methods.
  - GET loads exhibition list.
  - POST applies exhibition type filter.
  - Renders `exhibitions.html`.
  - Context vars include `exhibitions`, list of `exhibition_types`, and optional `selected_type`.

- **/exhibition/<int:exhibition_id>** (exhibition_details): GET method.
  - Shows detailed info for given exhibition ID.
  - Renders `exhibition_details.html`.
  - Context vars: single `exhibition` dict and list of `artifacts` in exhibition.

- **/visitor_tickets** (visitor_tickets): GET and POST methods.
  - GET lists user's tickets.
  - POST processes ticket purchase.
  - Renders `visitor_tickets.html`.
  - Context vars: list of `ticket_types`, user's `purchased_tickets`, optional `purchase_message`.

- **/virtual_events** (virtual_events): GET and POST methods.
  - GET displays events and registrations.
  - POST handles event registration or cancellation.
  - Renders `virtual_events.html`.
  - Context vars: list of `events`, user's `user_registrations`, optional `registration_message`.

- **/audio_guides** (audio_guides): GET and POST methods.
  - GET displays all guides.
  - POST applies language filter.
  - Renders `audio_guides.html`.
  - Context vars include list of `audio_guides`, list of `languages`, optional `selected_language`.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Page Title: Museum Dashboard
- Main Heading (h1): Museum Dashboard
- Element IDs:
  - `dashboard-page` (Div container)
  - `exhibition-summary` (Div showing counts)
  - `artifact-catalog-button` (Button) — navigates to `/artifact_catalog`
  - `exhibitions-button` (Button) — navigates to `/exhibitions`
  - `visitor-tickets-button` (Button) — navigates to `/visitor_tickets`
  - `virtual-events-button` (Button) — navigates to `/virtual_events`
  - `audio-guides-button` (Button) — navigates to `/audio_guides`
- Context Variables:
  - `exhibition_summary` (dict with int keys `total_exhibitions`, `active_exhibitions`)

### 2. artifact_catalog.html
- Page Title: Artifact Catalog
- Main Heading: Artifact Catalog
- Element IDs:
  - `artifact-catalog-page` (Div container)
  - `artifact-table` (Table) listing artifacts with columns: ID, name, period, origin, exhibition, actions
  - `search-artifact` (Input) field for search by name or ID
  - `apply-artifact-filter` (Button) applies search/filter
  - `back-to-dashboard` (Button) navigates back to `/dashboard`
- Context Variables:
  - `artifacts` (list of dict)
  - `search_query` (str, optional)
  - `filter_applied` (bool)

### 3. exhibitions.html
- Page Title: Exhibitions
- Main Heading: Exhibitions
- Element IDs:
  - `exhibitions-page` (Div container)
  - `exhibition-list` (Table) columns: title, type, dates, gallery, status
  - `filter-exhibition-type` (Dropdown) with options: Permanent, Temporary, Virtual
  - `apply-exhibition-filter` (Button)
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` (Button per row) — navigates to exhibition details
  - `back-to-dashboard` (Button) navigates back to `/dashboard`
- Context Variables:
  - `exhibitions` (list of dict)
  - `exhibition_types` (list of str)
  - `selected_type` (str, optional)

### 4. exhibition_details.html
- Page Title: Exhibition Details
- Main Heading (`h1`): Text with ID `exhibition-title` showing exhibition.title
- Element IDs:
  - `exhibition-details-page` (Div container)
  - `exhibition-title` (H1)
  - `exhibition-description` (Div)
  - `exhibition-dates` (Div)
  - `exhibition-artifacts` (Table) listing artifacts
  - `back-to-exhibitions` (Button) navigates to `/exhibitions`
- Context Variables:
  - `exhibition` (dict)
  - `artifacts` (list of dict)

### 5. visitor_tickets.html
- Page Title: Visitor Tickets
- Main Heading: Visitor Tickets
- Element IDs:
  - `visitor-tickets-page` (Div container)
  - `ticket-type` (Dropdown) with options: Standard, Student, Senior, Family, VIP
  - `number-of-tickets` (Input number)
  - `purchase-ticket-button` (Button)
  - `my-tickets-table` (Table) shows user's purchased tickets
  - `back-to-dashboard` (Button) navigates to `/dashboard`
- Context Variables:
  - `ticket_types` (list of str)
  - `purchased_tickets` (list of dict)
  - `purchase_message` (str, optional)

### 6. virtual_events.html
- Page Title: Virtual Events
- Main Heading: Virtual Events
- Element IDs:
  - `virtual-events-page` (Div container)
  - `event-list` (Table) with columns: title, date, time, type, registration status
  - `register-event-button-{{ event.event_id }}` (Button per event) to register
  - `cancel-registration-button-{{ registration.registration_id }}` (Button per registration) to cancel
  - `back-to-dashboard` (Button) navigates to `/dashboard`
- Context Variables:
  - `events` (list of dict)
  - `user_registrations` (list of dict)
  - `registration_message` (str, optional)

### 7. audio_guides.html
- Page Title: Audio Guides
- Main Heading: Audio Guides
- Element IDs:
  - `audio-guides-page` (Div container)
  - `audio-guide-list` (Table) with columns: exhibit number, title, language, duration
  - `filter-language` (Dropdown) options: English, Spanish, French
  - `apply-language-filter` (Button)
  - `play-guide-button-{{ guide.guide_id }}` (Button per guide) to play audio
  - `back-to-dashboard` (Button) navigates to `/dashboard`
- Context Variables:
  - `audio_guides` (list of dict)
  - `languages` (list of str)
  - `selected_language` (str, optional)

---

## Section 3: Data File Schemas

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited):
  - username
- Purpose: Stores usernames for authentication
- Example Data:
  curator_john
  visitor_mary
  curator_sarah

### 2. galleries.txt
- Path: data/galleries.txt
- Fields:
  gallery_id|gallery_name|floor|capacity|theme|status
- Purpose: Contains gallery metadata
- Example Data:
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation

### 3. exhibitions.txt
- Path: data/exhibitions.txt
- Fields:
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Purpose: Stores exhibition details
- Example Data:
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

### 4. artifacts.txt
- Path: data/artifacts.txt
- Fields:
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Purpose: Artifact data
- Example Data:
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

### 5. audioguides.txt
- Path: data/audioguides.txt
- Fields:
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Purpose: Audio guide info
- Example Data:
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

### 6. tickets.txt
- Path: data/tickets.txt
- Fields:
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Purpose: Visitor ticket purchases
- Example Data:
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

### 7. events.txt
- Path: data/events.txt
- Fields:
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Purpose: Virtual event data
- Example Data:
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

### 8. event_registrations.txt
- Path: data/event_registrations.txt
- Fields:
  registration_id|event_id|username|registration_date
- Purpose: User registrations for events
- Example Data:
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19

### 9. collection_logs.txt
- Path: data/collection_logs.txt
- Fields:
  log_id|artifact_id|activity_type|date|notes|condition|curator
- Purpose: Artifact activity logs
- Example Data:
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

This specification precisely defines the backend routes, frontend templates, and data schema to facilitate parallel development for the VirtualMuseum project.