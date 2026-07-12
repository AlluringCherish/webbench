# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name            | HTTP Method | Template Filename        | Context Variables (name: type)                                                    |
|--------------------------|--------------------------|-------------|--------------------------|-----------------------------------------------------------------------------------|
| /                        | root_redirect            | GET         | N/A (Redirect)            | N/A                                                                               |
| /dashboard               | dashboard                | GET         | dashboard.html            | exhibitions_summary: dict (total: int, active: int), artifacts_summary: dict (total: int), user: str (optional) |
| /artifacts               | artifact_catalog         | GET, POST   | artifact_catalog.html     | artifacts: list of dicts ({artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str}), search_query: str (GET only) |
| /exhibitions             | exhibitions              | GET, POST   | exhibitions.html          | exhibitions: list of dicts ({exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str, gallery_name: str, status: str}), filter_type: str (GET only) |
| /exhibition/<int:id>     | exhibition_details       | GET         | exhibition_details.html   | exhibition: dict ({exhibition_id: int, title: str, description: str, start_date: str, end_date: str}), artifacts: list of dicts ({artifact_id: int, artifact_name: str, period: str, origin: str}) |
| /tickets                 | visitor_tickets          | GET, POST   | visitor_tickets.html      | tickets: list of dicts ({ticket_id: int, ticket_type: str, visit_date: str, visit_time: str, number_of_tickets: int, price: float, visitor_name: str}), ticket_types: list of str, user: str (current logged in username) |
| /virtual-events          | virtual_events           | GET, POST   | virtual_events.html       | events: list of dicts ({event_id: int, title: str, date: str, time: str, event_type: str, registration_status: str}), user_registrations: list of int (event_ids registered by the user) |
| /register-event/<int:id> | register_event           | POST        | N/A (redirect or JSON)    | registration_response: str (success/failure message)                              |
| /cancel-registration/<int:registration_id> | cancel_registration | POST        | N/A (redirect or JSON)    | cancel_response: str (success/failure message)                                  |
| /audio-guides            | audio_guides             | GET, POST   | audio_guides.html         | audio_guides: list of dicts ({guide_id: int, exhibit_number: int, title: str, language: str, duration: int}), filter_language: str (GET only) |

Notes:
- Root route (/) will redirect to /dashboard.
- POST methods are used for applying filters or submitting forms.
- Context variable 'user' represents currently authenticated username, if authentication is implemented.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Page title: Museum Dashboard
- Main <h1>: Museum Dashboard
- Element IDs:
  - dashboard-page (Div container)
  - exhibition-summary (Div showing total exhibitions, active exhibitions count)
  - artifact-catalog-button (Button, navigates to artifact_catalog)
  - exhibitions-button (Button, navigates to exhibitions)
  - visitor-tickets-button (Button, navigates to visitor_tickets)
  - virtual-events-button (Button, navigates to virtual_events)
  - audio-guides-button (Button, navigates to audio_guides)
- Navigation mapping:
  - artifact-catalog-button -> url_for('artifact_catalog')
  - exhibitions-button -> url_for('exhibitions')
  - visitor-tickets-button -> url_for('visitor_tickets')
  - virtual-events-button -> url_for('virtual_events')
  - audio-guides-button -> url_for('audio_guides')
- Context variables:
  - exhibitions_summary: dict, usage: display counts
  - artifacts_summary: dict, usage: display total artifacts

### 2. artifact_catalog.html
- Page title: Artifact Catalog
- Main <h1>: Artifact Catalog
- Element IDs:
  - artifact-catalog-page (Div container)
  - artifact-table (Table showing artifact_id, artifact_name, period, origin, exhibition title, actions)
  - search-artifact (Input text for search)
  - apply-artifact-filter (Button to apply search/filter)
  - back-to-dashboard (Button navigating back to dashboard)
- Navigation mapping:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - artifacts: list of dicts, each with keys: artifact_id (int), artifact_name (str), period (str), origin (str), exhibition_title (str)
  - search_query: str, current search input

### 3. exhibitions.html
- Page title: Exhibitions
- Main <h1>: Exhibitions
- Element IDs:
  - exhibitions-page (Div container)
  - exhibition-list (Table showing title, type, dates, gallery, status)
  - filter-exhibition-type (Dropdown for Permanent, Temporary, Virtual)
  - apply-exhibition-filter (Button to apply filter)
  - back-to-dashboard (Button navigating back to dashboard)
  - view-exhibition-button-{exhibition_id} (Button per exhibition row)
- Navigation mapping:
  - back-to-dashboard -> url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }} -> url_for('exhibition_details', id=exhibition.exhibition_id)
- Context variables:
  - exhibitions: list of dicts with exhibition_id (int), title (str), exhibition_type (str), start_date (str), end_date (str), gallery_name (str), status (str)
  - filter_type: str, current filter selected

### 4. exhibition_details.html
- Page title: Exhibition Details
- Main <h1>: exhibition.title (exhibition title)
- Element IDs:
  - exhibition-details-page (Div container)
  - exhibition-title (H1 for title)
  - exhibition-description (Div)
  - exhibition-dates (Div showing start and end date)
  - exhibition-artifacts (Table showing artifacts in the exhibition)
  - back-to-exhibitions (Button navigating back to exhibitions)
- Navigation mapping:
  - back-to-exhibitions -> url_for('exhibitions')
- Context variables:
  - exhibition: dict with exhibition_id (int), title (str), description (str), start_date (str), end_date (str)
  - artifacts: list of dicts with artifact_id (int), artifact_name (str), period (str), origin (str)

### 5. visitor_tickets.html
- Page title: Visitor Tickets
- Main <h1>: Visitor Tickets
- Element IDs:
  - visitor-tickets-page (Div container)
  - ticket-type (Dropdown: Standard, Student, Senior, Family, VIP)
  - number-of-tickets (Input number)
  - purchase-ticket-button (Button)
  - my-tickets-table (Table showing user's tickets)
  - back-to-dashboard (Button navigating back to dashboard)
- Navigation mapping:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - tickets: list of dicts with ticket_id (int), ticket_type (str), visit_date (str), visit_time (str), number_of_tickets (int), price (float), visitor_name (str)
  - ticket_types: list of str

### 6. virtual_events.html
- Page title: Virtual Events
- Main <h1>: Virtual Events
- Element IDs:
  - virtual-events-page (Div container)
  - event-list (Table showing title, date, time, type, registration status)
  - register-event-button-{event_id} (Button per event)
  - cancel-registration-button-{registration_id} (Button per registration)
  - back-to-dashboard (Button navigating back to dashboard)
- Navigation mapping:
  - back-to-dashboard -> url_for('dashboard')
  - register-event-button-{{ event.event_id }} -> url_for('register_event', id=event.event_id)
  - cancel-registration-button-{{ registration.registration_id }} -> url_for('cancel_registration', registration_id=registration.registration_id)
- Context variables:
  - events: list of dicts with event_id (int), title (str), date (str), time (str), event_type (str), registration_status (str)
  - user_registrations: list of int (event_ids)

### 7. audio_guides.html
- Page title: Audio Guides
- Main <h1>: Audio Guides
- Element IDs:
  - audio-guides-page (Div container)
  - audio-guide-list (Table showing exhibit_number, title, language, duration)
  - filter-language (Dropdown: English, Spanish, French)
  - apply-language-filter (Button)
  - play-guide-button-{guide_id} (Button per audio guide)
  - back-to-dashboard (Button navigating back to dashboard)
- Navigation mapping:
  - back-to-dashboard -> url_for('dashboard')
  - play-guide-button-{{ guide.guide_id }} -> url_for('audio_guides') (with play action via JS or separate endpoint)
- Context variables:
  - audio_guides: list of dicts with guide_id (int), exhibit_number (int), title (str), language (str), duration (int minutes)
  - filter_language: str

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited): username
- Purpose: Contains usernames for authentication
- Example Rows:
  - curator_john
  - visitor_mary
  - curator_sarah

### 2. galleries.txt
- Filename: data/galleries.txt
- Fields (pipe-delimited): gallery_id|gallery_name|floor|capacity|theme|status
- Purpose: Lists galleries with details
- Example Rows:
  - 1|Ancient Civilizations Hall|1|50|Ancient|Open
  - 2|Modern Art Wing|2|30|Modern|Open
  - 3|Science Discovery Center|3|40|Science|Renovation

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Fields (pipe-delimited): exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Purpose: Details of exhibitions
- Example Rows:
  - 1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  - 2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  - 3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Fields (pipe-delimited): artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Purpose: Artifact catalog details
- Example Rows:
  - 1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  - 2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  - 3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Fields (pipe-delimited): guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Purpose: Audio guides for exhibits
- Example Rows:
  - 1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  - 2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  - 3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

### 6. tickets.txt
- Filename: data/tickets.txt
- Fields (pipe-delimited): ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Purpose: Visitor tickets sales and records
- Example Rows:
  - 1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  - 2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  - 3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

### 7. events.txt
- Filename: data/events.txt
- Fields (pipe-delimited): event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Purpose: Virtual museum events
- Example Rows:
  - 1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  - 2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  - 3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Fields (pipe-delimited): registration_id|event_id|username|registration_date
- Purpose: Registrations for virtual events
- Example Rows:
  - 1|1|visitor_mary|2024-11-20
  - 2|2|visitor_mary|2024-11-21
  - 3|1|visitor_tom|2024-11-19

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Fields (pipe-delimited): log_id|artifact_id|activity_type|date|notes|condition|curator
- Purpose: Logs of artifact maintenance and activities
- Example Rows:
  - 1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  - 2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  - 3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  - 4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---


--- End of Design Specification ---
