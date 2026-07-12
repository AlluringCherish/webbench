# Design Specification Document for VirtualMuseum Web Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name          | HTTP Method | Template Filename         | Context Variables (Name: Type)                                          |
|-------------------------------|------------------------|-------------|---------------------------|-------------------------------------------------------------------------|
| /                             | root_redirect           | GET         | Redirect to /dashboard    | None                                                                    |
| /dashboard                    | dashboard_page          | GET         | dashboard.html            | exhibitions_summary: dict (with keys: total_exhibitions: int, active_exhibitions: int)
                                                                     |
|                               |                        |             |                           | Note: Used to populate #exhibition-summary                             |
| /artifacts                    | artifact_catalog_page   | GET, POST   | artifact_catalog.html     | artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str or None)
                                                                     |
|                               |                        |             |                           | search_query: str (optional, for filtered search)                      |
| /exhibitions                  | exhibitions_page        | GET         | exhibitions.html          | exhibitions: list of dict (exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str, gallery_name: str, status: str)
|                               |                        |             |                           | selected_filter: str (optional, exhibition type filter)               |
| /exhibition/<int:exhibition_id> | exhibition_details_page | GET         | exhibition_details.html   | exhibition: dict (exhibition_id: int, title: str, description: str, start_date: str, end_date: str)
                                                                     |
|                               |                        |             |                           | artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str) for artifacts in this exhibition
| /visitor_tickets              | visitor_tickets_page    | GET, POST   | visitor_tickets.html      | tickets: list of dict (ticket_id: int, ticket_type: str, visit_date: str, visit_time: str, number_of_tickets: int, price: float, visitor_name: str)
                                                                     |
|                               |                        |             |                           | purchase_success: bool (optional, indicates if last purchase succeeded)
| /virtual_events               | virtual_events_page     | GET         | virtual_events.html       | events: list of dict (event_id: int, title: str, date: str, time: str, event_type: str, registration_status: dict (registered: bool, registration_id: int or None))
                                                                     |
| /register_event/<int:event_id> | register_event          | POST        | Redirect back to /virtual_events | None                                                                |
| /cancel_registration/<int:registration_id> | cancel_registration | POST        | Redirect back to /virtual_events | None                                                                |
| /audio_guides                | audio_guides_page       | GET         | audio_guides.html         | audioguides: list of dict (guide_id: int, exhibit_number: int or str, title: str, language: str, duration: int, narrator: str)
|                               |                        |             |                           | selected_language: str (optional, language filter applied)            |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main H1: Museum Dashboard
- Element IDs:
  - dashboard-page (div)
  - exhibition-summary (div)
  - artifact-catalog-button (button)
  - exhibitions-button (button)
  - visitor-tickets-button (button)
  - virtual-events-button (button)
  - audio-guides-button (button)
- Navigation Button Mappings:
  - artifact-catalog-button: url_for('artifact_catalog_page')
  - exhibitions-button: url_for('exhibitions_page')
  - visitor-tickets-button: url_for('visitor_tickets_page')
  - virtual-events-button: url_for('virtual_events_page')
  - audio-guides-button: url_for('audio_guides_page')
- Context Variables:
  - exhibitions_summary: dict {total_exhibitions: int, active_exhibitions: int} - Used in #exhibition-summary to display counts

### 2. artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main H1: Artifact Catalog
- Element IDs:
  - artifact-catalog-page (div)
  - artifact-table (table) - columns: ID, Name, Period, Origin, Exhibition, Actions
  - search-artifact (input text)
  - apply-artifact-filter (button)
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - artifacts: list of dict with keys (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str or None)
  - search_query: str (optional, for pre-filling the search box)

### 3. exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main H1: Exhibitions
- Element IDs:
  - exhibitions-page (div)
  - exhibition-list (table) - columns: Title, Type, Dates, Gallery, Status, Actions
  - filter-exhibition-type (dropdown) options: Permanent, Temporary, Virtual
  - apply-exhibition-filter (button)
  - back-to-dashboard (button)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (button, dynamic per exhibition row)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard_page')
  - view-exhibition-button-{{ exhibition.exhibition_id }}: url_for('exhibition_details_page', exhibition_id=exhibition.exhibition_id)
- Context Variables:
  - exhibitions: list of dict with keys (exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str, gallery_name: str, status: str)
  - selected_filter: str (optional, current filter selection)

### 4. exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main H1: exhibition.title (dynamic from context)
- Element IDs:
  - exhibition-details-page (div)
  - exhibition-title (h1)
  - exhibition-description (div)
  - exhibition-dates (div) - formatted start and end dates
  - exhibition-artifacts (table) - columns: ID, Name, Period, Origin
  - back-to-exhibitions (button)
- Navigation Button Mappings:
  - back-to-exhibitions: url_for('exhibitions_page')
- Context Variables:
  - exhibition: dict (exhibition_id: int, title: str, description: str, start_date: str, end_date: str)
  - artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str)

### 5. visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main H1: Visitor Tickets
- Element IDs:
  - visitor-tickets-page (div)
  - ticket-type (dropdown) options: Standard, Student, Senior, Family, VIP
  - number-of-tickets (input number)
  - purchase-ticket-button (button)
  - my-tickets-table (table) - columns: Ticket Type, Visit Date, Time, Number of Tickets, Price, Visitor Name
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - tickets: list of dict (ticket_id: int, ticket_type: str, visit_date: str, visit_time: str, number_of_tickets: int, price: float, visitor_name: str)
  - purchase_success: bool (optional)

### 6. virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main H1: Virtual Events
- Element IDs:
  - virtual-events-page (div)
  - event-list (table) - columns: Title, Date, Time, Type, Registration Status, Actions
  - register-event-button-{{ event.event_id }} (button, dynamic per event row)
  - cancel-registration-button-{{ registration.registration_id }} (button, dynamic per registration row)
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard_page')
  - register-event-button-{{ event.event_id }}: url_for('register_event', event_id=event.event_id)
  - cancel-registration-button-{{ registration.registration_id }}: url_for('cancel_registration', registration_id=registration.registration_id)
- Context Variables:
  - events: list of dict (event_id: int, title: str, date: str, time: str, event_type: str, registration_status: dict with keys registered: bool, registration_id: int or None)

### 7. audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main H1: Audio Guides
- Element IDs:
  - audio-guides-page (div)
  - audio-guide-list (table) - columns: Exhibit Number, Title, Language, Duration, Actions
  - filter-language (dropdown) options: English, Spanish, French
  - apply-language-filter (button)
  - play-guide-button-{{ guide.guide_id }} (button, dynamic per row)
  - back-to-dashboard (button)
- Navigation Button Mappings:
  - back-to-dashboard: url_for('dashboard_page')
  - play-guide-button-{{ guide.guide_id }}: (Action to play audio guide - dynamic behavior, no Flask route required)
- Context Variables:
  - audioguides: list of dict (guide_id: int, exhibit_number: int or str, title: str, language: str, duration: int, narrator: str)
  - selected_language: str (optional)

---

## Section 3: Data File Schemas

### 1. Users Data
- Filename: data/users.txt
- Purpose: Stores usernames of users such as curators and visitors.
- Fields (pipe-delimited):
  - username
- Example Data:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Galleries Data
- Filename: data/galleries.txt
- Purpose: Stores galleries details including their floor, capacity and theme.
- Fields (pipe-delimited):
  - gallery_id (int)
  - gallery_name (str)
  - floor (int)
  - capacity (int)
  - theme (str)
  - status (str)
- Example Data:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibitions Data
- Filename: data/exhibitions.txt
- Purpose: Stores exhibitions information including type, dates, and curator.
- Fields (pipe-delimited):
  - exhibition_id (int)
  - title (str)
  - description (str)
  - gallery_id (int)
  - exhibition_type (str) [Permanent, Temporary, Virtual]
  - start_date (str) YYYY-MM-DD
  - end_date (str) YYYY-MM-DD
  - curator_name (str)
  - created_by (str) username
- Example Data:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifacts Data
- Filename: data/artifacts.txt
- Purpose: Stores detailed information about artifacts including exhibition association and storage location.
- Fields (pipe-delimited):
  - artifact_id (int)
  - artifact_name (str)
  - period (str)
  - origin (str)
  - description (str)
  - exhibition_id (int)
  - storage_location (str)
  - acquisition_date (str) YYYY-MM-DD
  - added_by (str) username
- Example Data:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guides Data
- Filename: data/audioguides.txt
- Purpose: Stores audio guides metadata including language and narration details.
- Fields (pipe-delimited):
  - guide_id (int)
  - exhibit_number (int or str)
  - title (str)
  - language (str) [English, Spanish, French]
  - duration (int) minutes
  - script (str)
  - narrator (str)
  - created_by (str) username
- Example Data:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Tickets Data
- Filename: data/tickets.txt
- Purpose: Stores visitor ticket purchases and related visitor information.
- Fields (pipe-delimited):
  - ticket_id (int)
  - username (str)
  - ticket_type (str) [Standard, Student, Senior, Family, VIP]
  - visit_date (str) YYYY-MM-DD
  - visit_time (str) time format (e.g. "11:00 AM")
  - number_of_tickets (int)
  - price (float)
  - visitor_name (str)
  - visitor_email (str)
  - purchase_date (str) YYYY-MM-DD
- Example Data:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Events Data
- Filename: data/events.txt
- Purpose: Stores details of virtual events such as webinars and artist talks.
- Fields (pipe-delimited):
  - event_id (int)
  - title (str)
  - date (str) YYYY-MM-DD
  - time (str) time format (e.g. "2:00 PM")
  - event_type (str) [Webinar, Artist Talk, Virtual Tour]
  - speaker (str)
  - capacity (int)
  - description (str)
  - created_by (str) username
- Example Data:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registrations Data
- Filename: data/event_registrations.txt
- Purpose: Stores registrations for virtual events by users.
- Fields (pipe-delimited):
  - registration_id (int)
  - event_id (int)
  - username (str)
  - registration_date (str) YYYY-MM-DD
- Example Data:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Logs Data
- Filename: data/collection_logs.txt
- Purpose: Stores curator logs of activities performed on artifacts.
- Fields (pipe-delimited):
  - log_id (int)
  - artifact_id (int)
  - activity_type (str)
  - date (str) YYYY-MM-DD
  - notes (str)
  - condition (str)
  - curator (str)
- Example Data:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This document fully enables an independent Backend Developer to implement all Flask routes with data parsing based on Section 1 & 3, and an independent Frontend Developer to build templates exactly as specified in Section 2.

All element IDs, page titles, and context variables are consistent across sections for accurate integration.
