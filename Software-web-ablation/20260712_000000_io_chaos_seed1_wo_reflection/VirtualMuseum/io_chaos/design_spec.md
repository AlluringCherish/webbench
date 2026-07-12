# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name             | HTTP Method | Template Filename      | Context Variables (Name: Type)                                                                                       |
|-------------------------------|---------------------------|-------------|------------------------|-----------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect             | GET         | N/A                    | None (Redirects to /dashboard)                                                                                        |
| /dashboard                    | dashboard                 | GET         | dashboard.html         | total_exhibitions: int, active_exhibitions: int                                                                        |
| /artifact-catalog             | artifact_catalog          | GET, POST   | artifact_catalog.html  | artifacts: list of dict, filtered by search/filter input; each artifact dict with fields (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str) |
| /exhibitions                  | exhibitions               | GET, POST   | exhibitions.html       | exhibitions: list of dict, filtered by exhibition_type; each dict with (exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str, gallery_name: str, status: str) |
| /exhibition/<int:exhibition_id> | exhibition_details       | GET         | exhibition_details.html| exhibition: dict (exhibition_id: int, title: str, description: str, start_date: str, end_date: str),
  artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str)                                |
| /visitor-tickets             | visitor_tickets           | GET, POST   | visitor_tickets.html   | tickets: list of dict (ticket_id: int, ticket_type: str, visit_date: str, visit_time: str, number_of_tickets: int, price: float)
  available_ticket_types: list of str ("Standard", "Student", "Senior", "Family", "VIP")                            |
| /virtual-events              | virtual_events            | GET         | virtual_events.html    | events: list of dict (event_id: int, title: str, date: str, time: str, event_type: str, registration_status: dict),
  registrations: list of dict (registration_id: int, event_id: int)                                                      |
| /virtual-events/register/<int:event_id> | register_event    | POST        | N/A                    | event_id: int (From URL param)                                                                                         |
| /virtual-events/cancel/<int:registration_id> | cancel_event_registration | POST | N/A                     | registration_id: int (From URL param)                                                                                  |
| /audio-guides                | audio_guides              | GET, POST   | audio_guides.html      | audio_guides: list of dict (guide_id: int, exhibit_number: str, title: str, language: str, duration: int),
  filter_languages: list of str ("English", "Spanish", "French")                                                  |


## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Museum Dashboard
- Main h1 Title: Museum Dashboard
- Element IDs:
  - dashboard-page (Div container)
  - exhibition-summary (Div showing total and active exhibitions)
  - artifact-catalog-button (Button, navigates to artifact_catalog)
  - exhibitions-button (Button, navigates to exhibitions)
  - visitor-tickets-button (Button, navigates to visitor_tickets)
  - virtual-events-button (Button, navigates to virtual_events)
  - audio-guides-button (Button, navigates to audio_guides)
- Navigation buttons mapped via url_for:
  - artifact-catalog-button -> url_for('artifact_catalog')
  - exhibitions-button -> url_for('exhibitions')
  - visitor-tickets-button -> url_for('visitor_tickets')
  - virtual-events-button -> url_for('virtual_events')
  - audio-guides-button -> url_for('audio_guides')
- Context variables:
  - total_exhibitions (int): Used in exhibition-summary
  - active_exhibitions (int): Used in exhibition-summary

---

### 2. artifact_catalog.html
- Filename: templates/artifact_catalog.html
- Page Title: Artifact Catalog
- Main h1 Title: Artifact Catalog
- Element IDs:
  - artifact-catalog-page (Div container)
  - artifact-table (Table to display artifacts with columns: ID, name, period, origin, exhibition, actions)
  - search-artifact (Input for search by artifact name or ID)
  - apply-artifact-filter (Button to apply search/filter)
  - back-to-dashboard (Button to navigate back to dashboard)
- Navigation buttons mapped via url_for:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - artifacts (list of dict): Each dict contains artifact_id (int), artifact_name (str), period (str), origin (str), exhibition_title (str)

---

### 3. exhibitions.html
- Filename: templates/exhibitions.html
- Page Title: Exhibitions
- Main h1 Title: Exhibitions
- Element IDs:
  - exhibitions-page (Div container)
  - exhibition-list (Table columns: title, type, dates, gallery, status, with each row having a button)
  - filter-exhibition-type (Dropdown with options Permanent, Temporary, Virtual)
  - apply-exhibition-filter (Button to apply filter)
  - back-to-dashboard (Button to navigate back)
  - Dynamic buttons:
    - view-exhibition-button-{{ exhibition.exhibition_id }} (Button to view details)
- Navigation buttons mapped via url_for:
  - back-to-dashboard -> url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }} -> url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- Context variables:
  - exhibitions (list of dict): Each dict has exhibition_id (int), title (str), exhibition_type (str), start_date (str), end_date (str), gallery_name (str), status (str)

---

### 4. exhibition_details.html
- Filename: templates/exhibition_details.html
- Page Title: Exhibition Details
- Main h1 Title: (Value of exhibition.title)
- Element IDs:
  - exhibition-details-page (Div container)
  - exhibition-title (H1, shows exhibition.title)
  - exhibition-description (Div for exhibition.description)
  - exhibition-dates (Div showing formatted start_date and end_date)
  - exhibition-artifacts (Table showing artifacts in exhibition with columns: ID, name, period, origin)
  - back-to-exhibitions (Button to navigate back to exhibitions page)
- Navigation buttons mapped via url_for:
  - back-to-exhibitions -> url_for('exhibitions')
- Context variables:
  - exhibition (dict): exhibition_id (int), title (str), description (str), start_date (str), end_date (str)
  - artifacts (list of dict): artifact_id (int), artifact_name (str), period (str), origin (str)

---

### 5. visitor_tickets.html
- Filename: templates/visitor_tickets.html
- Page Title: Visitor Tickets
- Main h1 Title: Visitor Tickets
- Element IDs:
  - visitor-tickets-page (Div container)
  - ticket-type (Dropdown with options Standard, Student, Senior, Family, VIP)
  - number-of-tickets (Input number)
  - purchase-ticket-button (Button to submit purchase)
  - my-tickets-table (Table showing user's purchased tickets columns: Ticket ID, Type, Date, Time, Qty, Price)
  - back-to-dashboard (Button to navigate back)
- Navigation buttons mapped via url_for:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - tickets (list of dict): ticket_id (int), ticket_type (str), visit_date (str), visit_time (str), number_of_tickets (int), price (float)
  - available_ticket_types (list of str): ["Standard", "Student", "Senior", "Family", "VIP"]

---

### 6. virtual_events.html
- Filename: templates/virtual_events.html
- Page Title: Virtual Events
- Main h1 Title: Virtual Events
- Element IDs:
  - virtual-events-page (Div container)
  - event-list (Table showing events with columns: title, date, time, type, registration status)
  - register-event-button-{{ event.event_id }} (Button to register per event)
  - cancel-registration-button-{{ registration.registration_id }} (Button to cancel per registration)
  - back-to-dashboard (Button to navigate back)
- Navigation buttons mapped via url_for:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - events (list of dict): event_id (int), title (str), date (str), time (str), event_type (str), registration_status (dict: keys username, values bool)
  - registrations (list of dict): registration_id (int), event_id (int)

---

### 7. audio_guides.html
- Filename: templates/audio_guides.html
- Page Title: Audio Guides
- Main h1 Title: Audio Guides
- Element IDs:
  - audio-guides-page (Div container)
  - audio-guide-list (Table with columns: exhibit number, title, language, duration)
  - filter-language (Dropdown with options English, Spanish, French)
  - apply-language-filter (Button to apply filter)
  - play-guide-button-{{ guide.guide_id }} (Button to play guide audio)
  - back-to-dashboard (Button to navigate back)
- Navigation buttons mapped via url_for:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - audio_guides (list of dict): guide_id (int), exhibit_number (str), title (str), language (str), duration (int)
  - filter_languages (list of str): ["English", "Spanish", "French"]


## Section 3: Data File Schemas

| Filename                | Field Order (pipe-delimited)                                                                                       | Content Description                                            | Example Rows                                                                                                   |
|-------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| data/users.txt          | username                                                                                                          | List of users by username                                     | curator_john
visitor_mary
curator_sarah                                                                    |
| data/galleries.txt      | gallery_id|gallery_name|floor|capacity|theme|status                                                              | Galleries with location, capacity and status                | 1|Ancient Civilizations Hall|1|50|Ancient|Open
2|Modern Art Wing|2|30|Modern|Open
3|Science Discovery Center|3|40|Science|Renovation|
| data/exhibitions.txt    | exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by                | Exhibitions with metadata and curator info           | 1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john |
| data/artifacts.txt      | artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by                                  | Artifact details for exhibitions                       | 1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john                                         |
| data/audioguides.txt    | guide_id|exhibit_number|title|language|duration|script|narrator|created_by                                                     | Audio guides metadata                                  | 1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah                                   |
| data/tickets.txt        | ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date                         | Visitor ticket sales with buyer info                   | 1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18                                         |
| data/events.txt         | event_id|title|date|time|event_type|speaker|capacity|description|created_by                                            | Virtual events data with descriptions                  | 1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john                       |
| data/event_registrations.txt | registration_id|event_id|username|registration_date                                                           | Event registrations tracking                          | 1|1|visitor_mary|2024-11-20
2|2|visitor_mary|2024-11-21
3|1|visitor_tom|2024-11-19                                                    |
| data/collection_logs.txt| log_id|artifact_id|activity_type|date|notes|condition|curator                                                                 | Logs of artifact maintenance and activities           | 1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john        |

---

# End of Design Specification
