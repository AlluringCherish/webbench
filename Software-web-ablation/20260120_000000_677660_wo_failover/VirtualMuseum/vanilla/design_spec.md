# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Method     | Template Rendered        | Context Variables (Name: Type)                                                                                         |
|-------------------------------|-----------------------------|-----------------|--------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect               | GET             | Redirect to /dashboard   | None                                                                                                                   |
| /dashboard                    | dashboard                  | GET             | dashboard.html           | exhibitions_summary: dict (keys: total_exhibitions: int, active_exhibitions: int),
  user: str (current user, optional)                              |
| /artifact_catalog             | artifact_catalog           | GET, POST       | artifact_catalog.html    | artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str),
  search_query: str (optional, filter),
  filters_applied: bool                                               |
| /exhibitions                  | exhibitions                | GET, POST       | exhibitions.html         | exhibitions: list of dict (exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str, gallery_name: str, status: str),
  filter_type: str (Optional: "Permanent", "Temporary", "Virtual"),
  filters_applied: bool                                               |
| /exhibition/&lt;int:exhibition_id&gt; | exhibition_details         | GET             | exhibition_details.html  | exhibition: dict (exhibition_id: int, title: str, description: str, start_date: str, end_date: str),
  artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str)                                   |
| /visitor_tickets              | visitor_tickets            | GET, POST       | visitor_tickets.html     | tickets: list of dict (ticket_id: int, ticket_type: str, visit_date: str, number_of_tickets: int, price: float),
  purchase_success: bool (optional),
  purchase_errors: list of str (optional)                                          |
| /virtual_events               | virtual_events             | GET, POST       | virtual_events.html      | events: list of dict (event_id: int, title: str, date: str, time: str, event_type: str, is_registered: bool),
  registrations: list of dict (registration_id: int, event_id: int),
  registration_success: bool (optional),
  cancellation_success: bool (optional)                                        |
| /audio_guides                 | audio_guides               | GET, POST       | audio_guides.html        | audio_guides: list of dict (guide_id: int, exhibit_number: str, title: str, language: str, duration: int),
  filter_language: str (optional)                                                        |

---

## Section 2: HTML Templates Specification

### dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main &lt;h1&gt; Title: Museum Dashboard
- Element IDs:
  - dashboard-page (div container)
  - exhibition-summary (div showing total and active exhibitions)
  - artifact-catalog-button (button navigation to /artifact_catalog)
  - exhibitions-button (button navigation to /exhibitions)
  - visitor-tickets-button (button navigation to /visitor_tickets)
  - virtual-events-button (button navigation to /virtual_events)
  - audio-guides-button (button navigation to /audio_guides)
- Navigation Button ID to url_for mapping:
  - artifact-catalog-button: url_for('artifact_catalog')
  - exhibitions-button: url_for('exhibitions')
  - visitor-tickets-button: url_for('visitor_tickets')
  - virtual-events-button: url_for('virtual_events')
  - audio-guides-button: url_for('audio_guides')
- Context Variables:
  - exhibitions_summary: dict with keys total_exhibitions (int), active_exhibitions (int) to display summary info

---

### artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main &lt;h1&gt; Title: Artifact Catalog
- Element IDs:
  - artifact-catalog-page (div container)
  - artifact-table (table showing all artifact data columns)
  - search-artifact (input text for artifact search by ID or name)
  - apply-artifact-filter (button to trigger filter/search)
  - back-to-dashboard (button navigation back to dashboard)
- Navigation Button ID to url_for mapping:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - artifacts: list of dict each with keys artifact_id (int), artifact_name (str), period (str), origin (str), exhibition_title (str)
  - search_query: str (current search term, optional)
  - filters_applied: bool

---

### exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main &lt;h1&gt; Title: Exhibitions
- Element IDs:
  - exhibitions-page (div container)
  - exhibition-list (table listing exhibitions)
  - filter-exhibition-type (dropdown with values "Permanent", "Temporary", "Virtual")
  - apply-exhibition-filter (button to apply filter)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (button to view individual exhibition details)
  - back-to-dashboard (button navigation back to dashboard)
- Navigation Button ID to url_for mapping:
  - back-to-dashboard: url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }}: url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- Context Variables:
  - exhibitions: list of dict each with keys exhibition_id (int), title (str), exhibition_type (str), start_date (str), end_date (str), gallery_name (str), status (str)
  - filter_type: str (optional filter for exhibition type)
  - filters_applied: bool

---

### exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main &lt;h1&gt; Title: Exhibition Details
- Element IDs:
  - exhibition-details-page (div container)
  - exhibition-title (h1 showing exhibition title)
  - exhibition-description (div with description text)
  - exhibition-dates (div with start and end date)
  - exhibition-artifacts (table with artifact info)
  - back-to-exhibitions (button navigation back to exhibitions page)
- Navigation Button ID to url_for mapping:
  - back-to-exhibitions: url_for('exhibitions')
- Context Variables:
  - exhibition: dict with keys exhibition_id (int), title (str), description (str), start_date (str), end_date (str)
  - artifacts: list of dict each with keys artifact_id (int), artifact_name (str), period (str), origin (str)

---

### visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main &lt;h1&gt; Title: Visitor Tickets
- Element IDs:
  - visitor-tickets-page (div container)
  - ticket-type (dropdown with options: Standard, Student, Senior, Family, VIP)
  - number-of-tickets (number input)
  - purchase-ticket-button (button to submit ticket purchase)
  - my-tickets-table (table showing purchased tickets data)
  - back-to-dashboard (button navigation back to dashboard)
- Navigation Button ID to url_for mapping:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - tickets: list of dict each with keys ticket_id (int), ticket_type (str), visit_date (str), number_of_tickets (int), price (float)
  - purchase_success: bool (optional)
  - purchase_errors: list of str (optional)

---

### virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main &lt;h1&gt; Title: Virtual Events
- Element IDs:
  - virtual-events-page (div container)
  - event-list (table with columns title, date, time, type, registration status)
  - register-event-button-{{ event.event_id }} (button to register for event)
  - cancel-registration-button-{{ registration.registration_id }} (button to cancel registration)
  - back-to-dashboard (button navigation back to dashboard)
- Navigation Button ID to url_for mapping:
  - back-to-dashboard: url_for('dashboard')
  - register-event-button-{{ event.event_id }}: url_for('virtual_events')  # POST to this route with event_id
  - cancel-registration-button-{{ registration.registration_id }}: url_for('virtual_events')  # POST to this route with registration_id
- Context Variables:
  - events: list of dict each with keys event_id (int), title (str), date (str), time (str), event_type (str), is_registered (bool)
  - registrations: list of dict each with keys registration_id (int), event_id (int)
  - registration_success: bool (optional)
  - cancellation_success: bool (optional)

---

### audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main &lt;h1&gt; Title: Audio Guides
- Element IDs:
  - audio-guides-page (div container)
  - audio-guide-list (table listing audio guides)
  - filter-language (dropdown with options English, Spanish, French)
  - apply-language-filter (button to apply language filter)
  - play-guide-button-{{ guide.guide_id }} (button to play audio guide)
  - back-to-dashboard (button navigation back to dashboard)
- Navigation Button ID to url_for mapping:
  - back-to-dashboard: url_for('dashboard')
  - play-guide-button-{{ guide.guide_id }}: url_for('audio_guides')  # POST or client play action
- Context Variables:
  - audio_guides: list of dict each with keys guide_id (int), exhibit_number (str), title (str), language (str), duration (int)
  - filter_language: str (optional)

---

## Section 3: Data File Schemas

### 1. users.txt
- Location: data/users.txt
- Purpose: Stores usernames for authentication
- Pipe-Delimited Fields:
  - username
- Example Data Rows:
  - curator_john
  - visitor_mary
  - curator_sarah

---

### 2. galleries.txt
- Location: data/galleries.txt
- Purpose: Stores museum gallery information
- Pipe-Delimited Fields in order:
  - gallery_id (int)
  - gallery_name (str)
  - floor (int)
  - capacity (int)
  - theme (str)
  - status (str)  # e.g. Open, Renovation
- Example Data Rows:
  - 1|Ancient Civilizations Hall|1|50|Ancient|Open
  - 2|Modern Art Wing|2|30|Modern|Open
  - 3|Science Discovery Center|3|40|Science|Renovation

---

### 3. exhibitions.txt
- Location: data/exhibitions.txt
- Purpose: Stores exhibition metadata
- Pipe-Delimited Fields in order:
  - exhibition_id (int)
  - title (str)
  - description (str)
  - gallery_id (int)
  - exhibition_type (str)  # Permanent, Temporary, Virtual
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - curator_name (str)
  - created_by (str, username)
- Example Data Rows:
  - 1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  - 2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  - 3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

---

### 4. artifacts.txt
- Location: data/artifacts.txt
- Purpose: Stores artifact details
- Pipe-Delimited Fields in order:
  - artifact_id (int)
  - artifact_name (str)
  - period (str)
  - origin (str)
  - description (str)
  - exhibition_id (int)
  - storage_location (str)
  - acquisition_date (str, YYYY-MM-DD)
  - added_by (str, username)
- Example Data Rows:
  - 1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  - 2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  - 3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

---

### 5. audioguides.txt
- Location: data/audioguides.txt
- Purpose: Stores audio guide data for exhibits
- Pipe-Delimited Fields in order:
  - guide_id (int)
  - exhibit_number (str)
  - title (str)
  - language (str)
  - duration (int, minutes)
  - script (str)
  - narrator (str)
  - created_by (str, username)
- Example Data Rows:
  - 1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  - 2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  - 3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

---

### 6. tickets.txt
- Location: data/tickets.txt
- Purpose: Stores visitor ticket purchases
- Pipe-Delimited Fields in order:
  - ticket_id (int)
  - username (str)
  - ticket_type (str)  # Standard, Student, Senior, Family, VIP
  - visit_date (str, YYYY-MM-DD)
  - visit_time (str)
  - number_of_tickets (int)
  - price (float)
  - visitor_name (str)
  - visitor_email (str)
  - purchase_date (str, YYYY-MM-DD)
- Example Data Rows:
  - 1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  - 2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  - 3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

---

### 7. events.txt
- Location: data/events.txt
- Purpose: Stores virtual event information
- Pipe-Delimited Fields in order:
  - event_id (int)
  - title (str)
  - date (str, YYYY-MM-DD)
  - time (str)
  - event_type (str)  # Webinar, Artist Talk, Virtual Tour
  - speaker (str)
  - capacity (int)
  - description (str)
  - created_by (str, username)
- Example Data Rows:
  - 1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  - 2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  - 3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

---

### 8. event_registrations.txt
- Location: data/event_registrations.txt
- Purpose: Stores registrations for virtual events
- Pipe-Delimited Fields in order:
  - registration_id (int)
  - event_id (int)
  - username (str)
  - registration_date (str, YYYY-MM-DD)
- Example Data Rows:
  - 1|1|visitor_mary|2024-11-20
  - 2|2|visitor_mary|2024-11-21
  - 3|1|visitor_tom|2024-11-19

---

### 9. collection_logs.txt
- Location: data/collection_logs.txt
- Purpose: Stores artifact management logs
- Pipe-Delimited Fields in order:
  - log_id (int)
  - artifact_id (int)
  - activity_type (str)
  - date (str, YYYY-MM-DD)
  - notes (str)
  - condition (str)
  - curator (str, username)
- Example Data Rows:
  - 1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  - 2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  - 3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  - 4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

# End of Design Specification
