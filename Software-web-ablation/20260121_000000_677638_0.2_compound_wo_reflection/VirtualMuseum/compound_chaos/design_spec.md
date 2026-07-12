# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Method     | Template Rendered        | Context Variables (Name: Type)                                                                                         |
|-------------------------------|-----------------------------|-----------------|--------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect               | GET             | Redirect to /dashboard   | None                                                                                                                   |
| /dashboard                    | dashboard                  | GET             | dashboard.html           | exhibitions_summary: dict (keys: total_exhibitions: int, active_exhibitions: int),
  user: str (current user, optional)                              |
| /artifact_catalog             | artifact_catalog           | GET, POST       | artifact_catalog.html    | artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str),
  search_query: str (optional, search term),
  filters_applied: bool                                                         |
| /exhibitions                  | exhibitions_list           | GET, POST       | exhibitions.html         | exhibitions: list of dict (exhibition_id: int, title: str, exhibition_type: str, start_date: str, end_date: str,
  gallery_name: str, status: str),
  filter_type: str (Permanent, Temporary, Virtual, optional)                                              |
| /exhibition/<int:exhibition_id> | exhibition_details         | GET             | exhibition_details.html  | exhibition: dict (exhibition_id: int, title: str, description: str, start_date: str, end_date: str),
  artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str)                               |
| /visitor_tickets              | visitor_tickets            | GET, POST       | visitor_tickets.html     | tickets: list of dict (ticket_id: int, ticket_type: str, visit_date: str, visit_time: str, number_of_tickets: int, price: float, visitor_name: str),
  purchase_status: str (optional success/failure message)                                                               |
| /virtual_events               | virtual_events             | GET, POST       | virtual_events.html      | events: list of dict (event_id: int, title: str, date: str, time: str, event_type: str, registration_status: dict with keys registered (bool), registration_id (int or None)),
  registration_message: str (optional)                                                                           |
| /audio_guides                | audio_guides               | GET, POST       | audio_guides.html        | audioguides: list of dict (guide_id: int, exhibit_number: int, title: str, language: str, duration: int),
  filter_language: str (optional from dropdown)                                                                        |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main <h1>: Museum Dashboard
- Container: div id="dashboard-page"
- Elements with IDs:
  - exhibition-summary (div)
  - artifact-catalog-button (button) - navigates to artifact_catalog via url_for('artifact_catalog')
  - exhibitions-button (button) - navigates to exhibitions_list via url_for('exhibitions_list')
  - visitor-tickets-button (button) - navigates to visitor_tickets via url_for('visitor_tickets')
  - virtual-events-button (button) - navigates to virtual_events via url_for('virtual_events')
  - audio-guides-button (button) - navigates to audio_guides via url_for('audio_guides')

### Context Variables Available:
- exhibitions_summary: dict (total_exhibitions: int, active_exhibitions: int)

---

### 2. artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main <h1>: Artifact Catalog
- Container: div id="artifact-catalog-page"
- Elements with IDs:
  - artifact-table (table)
  - search-artifact (input)
  - apply-artifact-filter (button) - applies search filter
  - back-to-dashboard (button) - navigates to dashboard via url_for('dashboard')

### Context Variables Available:
- artifacts: list of dict (artifact_id: int, artifact_name: str, period: str, origin: str, exhibition_title: str)
- search_query: str
- filters_applied: bool

---

### 3. exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main <h1>: Exhibitions
- Container: div id="exhibitions-page"
- Elements with IDs:
  - exhibition-list (table)
  - filter-exhibition-type (dropdown)
  - apply-exhibition-filter (button)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (button, dynamic for each exhibition)
  - back-to-dashboard (button) - navigates to dashboard via url_for('dashboard')

### Context Variables Available:
- exhibitions: list of dict (all exhibition details)
- filter_type: str

---

### 4. exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main <h1>: {{ exhibition.title }}
- Container: div id="exhibition-details-page"
- Elements with IDs:
  - exhibition-title (h1) - shows exhibition title
  - exhibition-description (div) - shows description
  - exhibition-dates (div) - shows start and end dates
  - exhibition-artifacts (table) - lists related artifacts
  - back-to-exhibitions (button) - navigates to exhibitions_list via url_for('exhibitions_list')

### Context Variables Available:
- exhibition: dict with keys (exhibition_id, title, description, start_date, end_date)
- artifacts: list of dict (artifact details in exhibition)

---

### 5. visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main <h1>: Visitor Tickets
- Container: div id="visitor-tickets-page"
- Elements with IDs:
  - ticket-type (dropdown)
  - number-of-tickets (input number)
  - purchase-ticket-button (button)
  - my-tickets-table (table)
  - back-to-dashboard (button) - navigates to dashboard via url_for('dashboard')

### Context Variables Available:
- tickets: list of dict (tickets owned by user)
- purchase_status: str (optional message)

---

### 6. virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main <h1>: Virtual Events
- Container: div id="virtual-events-page"
- Elements with IDs:
  - event-list (table)
  - register-event-button-{{ event.event_id }} (button, dynamic per event)
  - cancel-registration-button-{{ registration.registration_id }} (button, dynamic per registration)
  - back-to-dashboard (button) - navigates to dashboard via url_for('dashboard')

### Context Variables Available:
- events: list of dict (event details with registration status)
- registration_message: str (optional confirmation or error message)

---

### 7. audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main <h1>: Audio Guides
- Container: div id="audio-guides-page"
- Elements with IDs:
  - audio-guide-list (table)
  - filter-language (dropdown)
  - apply-language-filter (button)
  - play-guide-button-{{ guide.guide_id }} (button, dynamic per guide)
  - back-to-dashboard (button) - navigates to dashboard via url_for('dashboard')

### Context Variables Available:
- audioguides: list of dict (audio guide data)
- filter_language: str (current filter or empty)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Content: Stores usernames of application users.
- Format: Pipe-delimited single column (no headers)
  - username
- Examples:
  curator_john
  visitor_mary
  curator_sarah

---

### 2. galleries.txt
- Filename: data/galleries.txt
- Content: Contains details on gallery rooms in the museum.
- Format: Pipe-delimited fields:
  gallery_id|gallery_name|floor|capacity|theme|status
- Examples:
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation

---

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Content: Details of museum exhibitions.
- Format: Pipe-delimited fields:
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Examples:
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

---

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Content: Data of individual artifacts.
- Format: Pipe-delimited fields:
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Examples:
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

---

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Content: Audio guides metadata.
- Format: Pipe-delimited fields:
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Examples:
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

---

### 6. tickets.txt
- Filename: data/tickets.txt
- Content: Purchased visitor tickets details.
- Format: Pipe-delimited fields:
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Examples:
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

---

### 7. events.txt
- Filename: data/events.txt
- Content: Virtual events hosted by the museum.
- Format: Pipe-delimited fields:
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Examples:
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

---

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Content: User registrations for virtual events.
- Format: Pipe-delimited fields:
  registration_id|event_id|username|registration_date
- Examples:
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19

---

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Content: Logs of artifact collection activities.
- Format: Pipe-delimited fields:
  log_id|artifact_id|activity_type|date|notes|condition|curator
- Examples:
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

# End of design_spec.md
