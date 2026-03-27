# VirtualMuseum Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name               | HTTP Method(s) | Template Filename          | Context Variables with Types and Descriptions                          |
|--------------------------------|-----------------------------|----------------|----------------------------|-------------------------------------------------------------------------|
| /                              | root                        | GET            | Redirect to `/dashboard`   | None                                                                    |
| /dashboard                     | dashboard                   | GET            | dashboard.html             | exhibitions_summary: dict (keys: total_exhibitions (int), active_exhibitions (int)); 
|                                |                             |                |                            | user: str (current logged-in username, optional if authentication)       |
| /artifacts                    | artifact_catalog            | GET, POST      | artifacts.html             | artifacts: list of dict (fields: artifact_id (int), artifact_name (str), period (str), origin (str), description (str), exhibition_id (int), storage_location (str), acquisition_date (str), added_by (str));
|                                |                             |                |                            | filtered: bool (whether filter/search applied)                          |
| /exhibitions                   | exhibitions_list            | GET, POST      | exhibitions.html           | exhibitions: list of dict (exhibition_id (int), title (str), description (str), gallery_id (int), exhibition_type (str), start_date (str), end_date (str), curator_name (str), created_by (str));
|                                |                             |                |                            | filter_type: str (Optional, one of Permanent, Temporary, Virtual)       |
| /exhibition/<int:exhibition_id>| exhibition_details          | GET            | exhibition_details.html    | exhibition: dict (exhibition_id (int), title (str), description (str), gallery_id (int), exhibition_type (str), start_date (str), end_date (str), curator_name (str), created_by (str));
|                                |                             |                |                            | artifacts: list of dict (artifacts belonging to exhibition)             |
| /tickets                      | visitor_tickets             | GET, POST      | visitor_tickets.html       | tickets: list of dict (ticket_id (int), username (str), ticket_type (str), visit_date (str), visit_time (str), number_of_tickets (int), price (float), visitor_name (str), visitor_email (str), purchase_date (str));
|                                |                             |                |                            | current_user: str (username of logged-in user)                         |
| /events                       | virtual_events              | GET, POST      | virtual_events.html        | events: list of dict (event_id (int), title (str), date (str), time (str), event_type (str), speaker (str), capacity (int), description (str), created_by (str));
|                                |                             |                |                            | user_registrations: list of dict (registration_id (int), event_id (int), username (str), registration_date (str))
|                                |                             |                |                            | current_user: str (username)                                            |
| /events/register/<int:event_id> | register_event             | POST           | N/A (redirect after process)| event_id: int (in URL)                                                  |
| /events/cancel/<int:registration_id> | cancel_registration    | POST           | N/A (redirect after process)| registration_id: int (in URL)                                           |
| /audioguides                  | audio_guides                | GET, POST      | audio_guides.html          | audio_guides: list of dict (guide_id (int), exhibit_number (int), title (str), language (str), duration (int, minutes), script (str), narrator (str), created_by (str));
|                                |                             |                |                            | filter_language: str (language filter applied)                         |

**Route Details**

- The root `/` route performs a redirect to `/dashboard`.
- Dashboard (`/dashboard`): GET request only, displays overview counts.
- Artifact Catalog (`/artifacts`): GET to view all artifacts, POST to apply filters/search (search by name or ID).
- Exhibitions (`/exhibitions`): GET to view exhibitions list, POST to apply type filter.
- Exhibition Details (`/exhibition/<exhibition_id>`): GET to view details and artifacts within.
- Visitor Tickets (`/tickets`): GET displays tickets; POST processes new ticket purchases.
- Virtual Events (`/events`): GET displays events and registrations; POST handles filtering or other updates.
- Event registration and cancellation are POST requests to `/events/register/<event_id>` and `/events/cancel/<registration_id>` respectively.
- Audio Guides (`/audioguides`): GET displays guides; POST applies language filters.


---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: `dashboard.html`
- Page Title: "Museum Dashboard"
- Main Header `<h1>`: "Museum Dashboard"
- HTML Element IDs:
  - `dashboard-page` (div container)
  - `exhibition-summary` (div showing counts)
  - `artifact-catalog-button` (button, link to artifact_catalog route)
  - `exhibitions-button` (button, link to exhibitions_list route)
  - `visitor-tickets-button` (button, link to visitor_tickets route)
  - `virtual-events-button` (button, link to virtual_events route)
  - `audio-guides-button` (button, link to audio_guides route)
- Navigation buttons mapping:
  - `artifact-catalog-button` => `url_for('artifact_catalog')`
  - `exhibitions-button` => `url_for('exhibitions_list')`
  - `visitor-tickets-button` => `url_for('visitor_tickets')`
  - `virtual-events-button` => `url_for('virtual_events')`
  - `audio-guides-button` => `url_for('audio_guides')`
- Context Variables:
  - `exhibitions_summary`: dict with keys `total_exhibitions` (int), `active_exhibitions` (int)
  - `user`: str (optional username)

---

### 2. artifacts.html
- Filename: `artifacts.html`
- Page Title: "Artifact Catalog"
- Main Header `<h1>`: "Artifact Catalog"
- HTML Element IDs:
  - `artifact-catalog-page` (div container)
  - `artifact-table` (table displaying artifacts)
  - `search-artifact` (input text for search by name or ID)
  - `apply-artifact-filter` (button to apply search/filter)
  - `back-to-dashboard` (button to go back to dashboard)
- Navigation Button:
  - `back-to-dashboard` => `url_for('dashboard')`
- Context Variables:
  - `artifacts`: list of artifacts (dict items with keys: artifact_id (int), artifact_name (str), period (str), origin (str), description (str), exhibition_id (int), storage_location (str), acquisition_date (str), added_by (str))
  - `filtered`: bool indicating if a filter or search is applied

---

### 3. exhibitions.html
- Filename: `exhibitions.html`
- Page Title: "Exhibitions"
- Main Header `<h1>`: "Exhibitions"
- HTML Element IDs:
  - `exhibitions-page` (div container)
  - `exhibition-list` (table displaying exhibitions)
  - `filter-exhibition-type` (dropdown select for exhibition type filter)
  - `apply-exhibition-filter` (button to apply filter)
  - For each exhibition row:
    - `view-exhibition-button-{{ exhibition.exhibition_id }}` (button to view details)
  - `back-to-dashboard` (button to go back to dashboard)
- Navigation Button:
  - `back-to-dashboard` => `url_for('dashboard')`
- Context Variables:
  - `exhibitions`: list of exhibitions (dict with keys: exhibition_id (int), title (str), description (str), gallery_id (int), exhibition_type (str), start_date (str), end_date (str), curator_name (str), created_by (str))
  - `filter_type`: str (selected exhibition type or empty)

---

### 4. exhibition_details.html
- Filename: `exhibition_details.html`
- Page Title: "Exhibition Details"
- Main Header `<h1>`:
  - id: `exhibition-title`, containing exhibition's title
- HTML Element IDs:
  - `exhibition-details-page` (div container)
  - `exhibition-title` (h1 title)
  - `exhibition-description` (div description)
  - `exhibition-dates` (div showing start and end dates)
  - `exhibition-artifacts` (table listing artifacts in exhibition)
  - `back-to-exhibitions` (button to return to exhibitions page)
- Navigation Button:
  - `back-to-exhibitions` => `url_for('exhibitions_list')`
- Context Variables:
  - `exhibition`: dict (exhibition details as in route)
  - `artifacts`: list of dict (artifacts under that exhibition)

---

### 5. visitor_tickets.html
- Filename: `visitor_tickets.html`
- Page Title: "Visitor Tickets"
- Main Header `<h1>`: "Visitor Tickets"
- HTML Element IDs:
  - `visitor-tickets-page` (div container)
  - `ticket-type` (dropdown for ticket type)
  - `number-of-tickets` (numeric input for quantity)
  - `purchase-ticket-button` (button to submit purchase)
  - `my-tickets-table` (table listing user's tickets)
  - `back-to-dashboard` (button to return to dashboard)
- Navigation Button:
  - `back-to-dashboard` => `url_for('dashboard')`
- Context Variables:
  - `tickets`: list of dict (each with ticket_id, username, ticket_type, visit_date, visit_time, number_of_tickets, price (float), visitor_name, visitor_email, purchase_date)
  - `current_user`: str (logged-in username)

---

### 6. virtual_events.html
- Filename: `virtual_events.html`
- Page Title: "Virtual Events"
- Main Header `<h1>`: "Virtual Events"
- HTML Element IDs:
  - `virtual-events-page` (div container)
  - `event-list` (table showing all virtual events)
  - For each event row:
    - `register-event-button-{{ event.event_id }}` (button to register for event)
  - For each user registration row:
    - `cancel-registration-button-{{ registration.registration_id }}` (button to cancel registration)
  - `back-to-dashboard` (button to return to dashboard)
- Navigation Button:
  - `back-to-dashboard` => `url_for('dashboard')`
- Context Variables:
  - `events`: list of dict (event_id, title, date, time, event_type, speaker, capacity, description, created_by)
  - `user_registrations`: list of dict (registration_id, event_id, username, registration_date) filtered by current user
  - `current_user`: str (username)

---

### 7. audio_guides.html
- Filename: `audio_guides.html`
- Page Title: "Audio Guides"
- Main Header `<h1>`: "Audio Guides"
- HTML Element IDs:
  - `audio-guides-page` (div container)
  - `audio-guide-list` (table listing all audio guides)
  - `filter-language` (dropdown to select language filter)
  - `apply-language-filter` (button to apply language filter)
  - For each guide row:
    - `play-guide-button-{{ guide.guide_id }}` (button to play the audio guide)
  - `back-to-dashboard` (button to go back to dashboard)
- Navigation Button:
  - `back-to-dashboard` => `url_for('dashboard')`
- Context Variables:
  - `audio_guides`: list of dict (guide_id (int), exhibit_number (int), title (str), language (str), duration (int), script (str), narrator (str), created_by (str))
  - `filter_language`: str (language filter value)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: `data/users.txt`
- Fields (pipe-delimited, no header in file):
  - username
- Description: Stores usernames for authentication/user identification.
- Sample Rows:
  - curator_john
  - visitor_mary
  - curator_sarah

---

### 2. galleries.txt
- Filename: `data/galleries.txt`
- Fields (pipe-delimited, no header):
  - gallery_id (int)
  - gallery_name (str)
  - floor (int)
  - capacity (int)
  - theme (str)
  - status (str) [e.g., Open, Renovation]
- Description: Contains details of galleries within the museum.
- Sample Rows:
  - 1|Ancient Civilizations Hall|1|50|Ancient|Open
  - 2|Modern Art Wing|2|30|Modern|Open
  - 3|Science Discovery Center|3|40|Science|Renovation

---

### 3. exhibitions.txt
- Filename: `data/exhibitions.txt`
- Fields (pipe-delimited, no header):
  - exhibition_id (int)
  - title (str)
  - description (str)
  - gallery_id (int)
  - exhibition_type (str) [Permanent, Temporary, Virtual]
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - curator_name (str)
  - created_by (str)
- Description: Details about exhibitions, types, dates, galleries, and responsible curators.
- Sample Rows:
  - 1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  - 2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  - 3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

---

### 4. artifacts.txt
- Filename: `data/artifacts.txt`
- Fields (pipe-delimited, no header):
  - artifact_id (int)
  - artifact_name (str)
  - period (str)
  - origin (str)
  - description (str)
  - exhibition_id (int)
  - storage_location (str)
  - acquisition_date (str, YYYY-MM-DD)
  - added_by (str)
- Description: Data about artifact items curated under exhibitions.
- Sample Rows:
  - 1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  - 2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  - 3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

---

### 5. audioguides.txt
- Filename: `data/audioguides.txt`
- Fields (pipe-delimited, no header):
  - guide_id (int)
  - exhibit_number (int)
  - title (str)
  - language (str) [English, Spanish, French]
  - duration (int, minutes)
  - script (str)
  - narrator (str)
  - created_by (str)
- Description: Audio guide details per exhibit with language variations.
- Sample Rows:
  - 1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  - 2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  - 3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

---

### 6. tickets.txt
- Filename: `data/tickets.txt`
- Fields (pipe-delimited, no header):
  - ticket_id (int)
  - username (str)
  - ticket_type (str) [Standard, Student, Senior, Family, VIP]
  - visit_date (str, YYYY-MM-DD)
  - visit_time (str, e.g. 11:00 AM)
  - number_of_tickets (int)
  - price (float)
  - visitor_name (str)
  - visitor_email (str)
  - purchase_date (str, YYYY-MM-DD)
- Description: Visitor ticket purchases data with user info and purchase details.
- Sample Rows:
  - 1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  - 2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  - 3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

---

### 7. events.txt
- Filename: `data/events.txt`
- Fields (pipe-delimited, no header):
  - event_id (int)
  - title (str)
  - date (str, YYYY-MM-DD)
  - time (str, e.g. 6:00 PM)
  - event_type (str) [Webinar, Artist Talk, Virtual Tour]
  - speaker (str)
  - capacity (int)
  - description (str)
  - created_by (str)
- Description: Museum virtual events including webinars, talks, and tours.
- Sample Rows:
  - 1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  - 2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  - 3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

---

### 8. event_registrations.txt
- Filename: `data/event_registrations.txt`
- Fields (pipe-delimited, no header):
  - registration_id (int)
  - event_id (int)
  - username (str)
  - registration_date (str, YYYY-MM-DD)
- Description: Records of users registered for events.
- Sample Rows:
  - 1|1|visitor_mary|2024-11-20
  - 2|2|visitor_mary|2024-11-21
  - 3|1|visitor_tom|2024-11-19

---

### 9. collection_logs.txt
- Filename: `data/collection_logs.txt`
- Fields (pipe-delimited, no header):
  - log_id (int)
  - artifact_id (int)
  - activity_type (str) [e.g., Inspection, Cleaning, Photography, Restoration]
  - date (str, YYYY-MM-DD)
  - notes (str)
  - condition (str) [e.g., Excellent, Good]
  - curator (str)
- Description: Logs activities related to artifact maintenance and condition.
- Sample Rows:
  - 1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  - 2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  - 3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  - 4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---


***End of Design Specification***
