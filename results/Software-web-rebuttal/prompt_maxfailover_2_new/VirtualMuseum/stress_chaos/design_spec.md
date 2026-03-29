# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path | Function Name | HTTP Method | Template Filename | Context Variables |
|---|---|---|---|---|
| / | root_redirect | GET | None (Redirect to /dashboard) | None |
| /dashboard | dashboard | GET | dashboard.html | exhibition_summary (dict: total_exhibitions:int, active_exhibitions:int), username (str), other_overview_data (dict) |
| /artifacts | artifact_catalog | GET, POST | artifact_catalog.html | artifacts (list of dict), search_query (str), filters (dict) |
| /exhibitions | exhibitions | GET, POST | exhibitions.html | exhibitions (list of dict), filter_type (str) |
| /exhibition/<int:exhibition_id> | exhibition_details | GET | exhibition_details.html | exhibition (dict), artifacts (list of dict) |
| /tickets | visitor_tickets | GET, POST | visitor_tickets.html | tickets (list of dict), ticket_types (list of str) |
| /events | virtual_events | GET, POST | virtual_events.html | events (list of dict), registrations (list of dict), user_registrations (list of dict) |
| /register_event/<int:event_id> | register_event | POST | None (Redirect) | None |
| /cancel_registration/<int:registration_id> | cancel_registration | POST | None (Redirect) | None |
| /audio_guides | audio_guides | GET, POST | audio_guides.html | audio_guides (list of dict), filter_language (str) |

**Notes on HTTP Methods:**
- GET for all pages for initial rendering.
- POST for form submissions such as filtering, purchasing tickets, event registration.


---

## Section 2: HTML Templates Specification

### 1. Template: dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main Heading (H1): Museum Dashboard
- Element IDs:
  - dashboard-page (Div container)
  - exhibition-summary (Div showing total and active exhibitions)
  - artifact-catalog-button (Button) - navigates to artifact_catalog
  - exhibitions-button (Button) - navigates to exhibitions
  - visitor-tickets-button (Button) - navigates to visitor_tickets
  - virtual-events-button (Button) - navigates to virtual_events
  - audio-guides-button (Button) - navigates to audio_guides
- Navigation button url_for mappings:
  - artifact-catalog-button → url_for('artifact_catalog')
  - exhibitions-button → url_for('exhibitions')
  - visitor-tickets-button → url_for('visitor_tickets')
  - virtual-events-button → url_for('virtual_events')
  - audio-guides-button → url_for('audio_guides')
- Context Variables:
  - exhibition_summary (dict: total_exhibitions:int, active_exhibitions:int)
  - username (str)

### 2. Template: artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main Heading (H1): Artifact Catalog
- Element IDs:
  - artifact-catalog-page (Div container)
  - artifact-table (Table) showing artifact columns: ID, name, period, origin, exhibition, actions
  - search-artifact (Input text) for searching by name or ID
  - apply-artifact-filter (Button) to submit filters
  - back-to-dashboard (Button) navigates to dashboard
- Navigation button url_for mappings:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - artifacts (list of dict)
  - search_query (str)
  - filters (dict)

### 3. Template: exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main Heading (H1): Exhibitions
- Element IDs:
  - exhibitions-page (Div container)
  - exhibition-list (Table) with columns: title, type, dates, gallery, status
  - filter-exhibition-type (Dropdown) options: Permanent, Temporary, Virtual
  - apply-exhibition-filter (Button)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (Button) one per exhibition row
  - back-to-dashboard (Button) navigates to dashboard
- Navigation button url_for mappings:
  - view-exhibition-button-{{ exhibition.exhibition_id }} → url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - exhibitions (list of dict)
  - filter_type (str)

### 4. Template: exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main Heading (H1): exhibition.title
- Element IDs:
  - exhibition-details-page (Div container)
  - exhibition-title (H1)
  - exhibition-description (Div)
  - exhibition-dates (Div) showing start and end dates
  - exhibition-artifacts (Table) listing artifacts for this exhibition
  - back-to-exhibitions (Button) navigates back to exhibitions
- Navigation button url_for mappings:
  - back-to-exhibitions → url_for('exhibitions')
- Context Variables:
  - exhibition (dict)
  - artifacts (list of dict)

### 5. Template: visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main Heading (H1): Visitor Tickets
- Element IDs:
  - visitor-tickets-page (Div container)
  - ticket-type (Dropdown) options: Standard, Student, Senior, Family, VIP
  - number-of-tickets (Input number)
  - purchase-ticket-button (Button)
  - my-tickets-table (Table) showing user's tickets
  - back-to-dashboard (Button) navigates to dashboard
- Navigation button url_for mappings:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - tickets (list of dict)
  - ticket_types (list of str)

### 6. Template: virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main Heading (H1): Virtual Events
- Element IDs:
  - virtual-events-page (Div container)
  - event-list (Table) with columns: title, date, time, type, registration status
  - register-event-button-{{ event.event_id }} (Button) to register for event
  - cancel-registration-button-{{ registration.registration_id }} (Button) to cancel registration
  - back-to-dashboard (Button) navigates to dashboard
- Navigation button url_for mappings:
  - register-event-button-{{ event.event_id }} → url_for('register_event', event_id=event.event_id)
  - cancel-registration-button-{{ registration.registration_id }} → url_for('cancel_registration', registration_id=registration.registration_id)
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - events (list of dict)
  - registrations (list of dict)
  - user_registrations (list of dict)

### 7. Template: audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main Heading (H1): Audio Guides
- Element IDs:
  - audio-guides-page (Div container)
  - audio-guide-list (Table) columns: exhibit number, title, language, duration
  - filter-language (Dropdown) options: English, Spanish, French
  - apply-language-filter (Button)
  - play-guide-button-{{ guide.guide_id }} (Button) to play audio guide
  - back-to-dashboard (Button) navigates to dashboard
- Navigation button url_for mappings:
  - play-guide-button-{{ guide.guide_id }} → url_for('audio_guides_play', guide_id=guide.guide_id)
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - audio_guides (list of dict)
  - filter_language (str)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Purpose: Stores usernames for user authentication
- Format (pipe-delimited fields):
  username
- Example Data:
  curator_john
  visitor_mary
  curator_sarah

### 2. galleries.txt
- Filename: data/galleries.txt
- Purpose: Stores details of physical galleries
- Format:
  gallery_id|gallery_name|floor|capacity|theme|status
- Example Data:
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Purpose: Stores virtual and physical exhibitions
- Format:
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Example Data:
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Purpose: Stores information about artifacts
- Format:
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Example Data:
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Purpose: Stores audio guides for exhibits
- Format:
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Example Data:
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

### 6. tickets.txt
- Filename: data/tickets.txt
- Purpose: Stores visitor ticket purchases
- Format:
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Example Data:
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

### 7. events.txt
- Filename: data/events.txt
- Purpose: Stores virtual museum events
- Format:
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Example Data:
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Purpose: Stores event registration records
- Format:
  registration_id|event_id|username|registration_date
- Example Data:
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Purpose: Logs activities related to artifacts
- Format:
  log_id|artifact_id|activity_type|date|notes|condition|curator
- Example Data:
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

This completes the comprehensive design specification for the VirtualMuseum web application.

All naming conventions, element IDs, template titles, route functions, and data file schemas strictly adhere to the user requirements.

This document enables independent, parallel development for frontend and backend teams with clear responsibilities and interfaces.
