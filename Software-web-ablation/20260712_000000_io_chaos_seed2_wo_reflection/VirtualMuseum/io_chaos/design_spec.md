# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                         | Function Name          | HTTP Method(s) | Template Filename          | Context Variables (name: type)                                      |
|----------------------------------|------------------------|----------------|----------------------------|----------------------------------------------------------------------|
| /                                | root_redirect          | GET            | None (redirect)             | None                                                                 |
| /dashboard                       | dashboard              | GET            | dashboard.html             | exhibitions_overview: dict (summary counts), e.g., total: int, active: int |
|                                  |                        |                |                            |                                                                                |
| /artifacts                      | artifact_catalog        | GET, POST     | artifact_catalog.html      | artifacts: list(dict), search_query: str (from form, optional)         |
|                                  |                        |                |                            |                                                                                |
| /exhibitions                    | exhibitions             | GET, POST     | exhibitions.html           | exhibitions: list(dict), filter_type: str (optional filter term)        |
|                                  |                        |                |                            |                                                                                |
| /exhibition/<int:exhibition_id> | exhibition_details      | GET           | exhibition_details.html    | exhibition: dict, artifacts: list(dict)                                 |
|                                  |                        |                |                            |                                                                                |
| /tickets                       | visitor_tickets         | GET, POST     | visitor_tickets.html       | tickets: list(dict), purchase_status: str (optional), user: str          |
|                                  |                        |                |                            |                                                                                |
| /events                        | virtual_events          | GET, POST     | virtual_events.html        | events: list(dict), registrations: list(dict)                           |
|                                  |                        |                |                            |                                                                                |
| /events/register/<int:event_id>| register_event          | POST          | None (redirect back to /events)| event_id: int, user: str (from session or post)                       |
| /events/cancel/<int:registration_id>| cancel_registration  | POST          | None (redirect back to /events)| registration_id: int, user: str (from session or post)                |
|                                  |                        |                |                            |                                                                                |
| /audioguides                   | audio_guides            | GET, POST     | audio_guides.html          | guides: list(dict), filter_language: str (optional)                     |

**Notes:**
- Root path `/` redirects to `/dashboard`.
- All pages that accept filters will support POST for filter submission.
- Actions like event registration and cancellation use POST and redirect back to events page.
- Context variables provide exactly named data as required for UI rendering.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: `dashboard.html`
- Page Title: Museum Dashboard
- Main <h1>: Museum Dashboard
- Element IDs:
  - dashboard-page (div container)
  - exhibition-summary (div for total exhibitions and active count)
  - artifact-catalog-button (button navigates to `artifact_catalog`)
  - exhibitions-button (button navigates to `exhibitions`)
  - visitor-tickets-button (button navigates to `visitor_tickets`)
  - virtual-events-button (button navigates to `virtual_events`)
  - audio-guides-button (button navigates to `audio_guides`)
- Navigation button url_for mappings:
  - artifact-catalog-button -> url_for('artifact_catalog')
  - exhibitions-button -> url_for('exhibitions')
  - visitor-tickets-button -> url_for('visitor_tickets')
  - virtual-events-button -> url_for('virtual_events')
  - audio-guides-button -> url_for('audio_guides')
- Context variables:
  - exhibitions_overview: dict
    - total: int
    - active: int

---

### 2. artifact_catalog.html
- Filename: `artifact_catalog.html`
- Page Title: Artifact Catalog
- Main <h1>: Artifact Catalog
- Element IDs:
  - artifact-catalog-page (div container)
  - artifact-table (table with columns: ID, Name, Period, Origin, Exhibition, Actions)
  - search-artifact (input for artifact name or ID search)
  - apply-artifact-filter (button to apply search/filter)
  - back-to-dashboard (button navigates back to dashboard)
- Navigation button url_for mappings:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - artifacts: list(dict) with fields:
    - artifact_id: int
    - artifact_name: str
    - period: str
    - origin: str
    - exhibition_name: str (resolved exhibition title)

---

### 3. exhibitions.html
- Filename: `exhibitions.html`
- Page Title: Exhibitions
- Main <h1>: Exhibitions
- Element IDs:
  - exhibitions-page (div container)
  - exhibition-list (table with columns: Title, Type, Dates, Gallery, Status)
  - filter-exhibition-type (dropdown for Permanent, Temporary, Virtual)
  - apply-exhibition-filter (button to apply filter)
  - back-to-dashboard (button navigates to dashboard)
  - view-exhibition-button-{exhibition_id} (button for each exhibition row)
- Navigation button url_for mappings:
  - back-to-dashboard -> url_for('dashboard')
  - view-exhibition-button-{exhibition_id} -> url_for('exhibition_details', exhibition_id=exhibition_id)
- Context variables:
  - exhibitions: list(dict) with fields:
    - exhibition_id: int
    - title: str
    - exhibition_type: str
    - start_date: str
    - end_date: str
    - gallery_name: str (resolved from gallery_id)
    - status: str (derived from gallery or exhibition dates)

---

### 4. exhibition_details.html
- Filename: `exhibition_details.html`
- Page Title: Exhibition Details
- Main <h1>: exhibition.title (dynamic)
- Element IDs:
  - exhibition-details-page (div container)
  - exhibition-title (h1, exhibition title)
  - exhibition-description (div, exhibition.description)
  - exhibition-dates (div, formatted start_date to end_date)
  - exhibition-artifacts (table with artifacts in this exhibition)
  - back-to-exhibitions (button navigates back to exhibitions)
- Navigation button url_for mappings:
  - back-to-exhibitions -> url_for('exhibitions')
- Context variables:
  - exhibition: dict with fields from exhibitions.txt
  - artifacts: list(dict) filtered by exhibition_id

---

### 5. visitor_tickets.html
- Filename: `visitor_tickets.html`
- Page Title: Visitor Tickets
- Main <h1>: Visitor Tickets
- Element IDs:
  - visitor-tickets-page (div container)
  - ticket-type (dropdown: Standard, Student, Senior, Family, VIP)
  - number-of-tickets (numeric input)
  - purchase-ticket-button (button to submit purchase)
  - my-tickets-table (table showing purchased tickets)
  - back-to-dashboard (button navigates back to dashboard)
- Navigation button url_for mappings:
  - back-to-dashboard -> url_for('dashboard')
- Context variables:
  - tickets: list(dict) filtered by logged in user
  - purchase_status: str (optional message)

---

### 6. virtual_events.html
- Filename: `virtual_events.html`
- Page Title: Virtual Events
- Main <h1>: Virtual Events
- Element IDs:
  - virtual-events-page (div container)
  - event-list (table with Title, Date, Time, Type, Registration Status columns)
  - register-event-button-{event_id} (button for each event)
  - cancel-registration-button-{registration_id} (button for each registration row)
  - back-to-dashboard (button navigates back to dashboard)
- Navigation button url_for mappings:
  - back-to-dashboard -> url_for('dashboard')
  - register-event-button-{event_id} -> url_for('register_event', event_id=event_id)
  - cancel-registration-button-{registration_id} -> url_for('cancel_registration', registration_id=registration_id)
- Context variables:
  - events: list(dict) with event details
  - registrations: list(dict) with user's registrations

---

### 7. audio_guides.html
- Filename: `audio_guides.html`
- Page Title: Audio Guides
- Main <h1>: Audio Guides
- Element IDs:
  - audio-guides-page (div container)
  - audio-guide-list (table with Exhibit Number, Title, Language, Duration columns)
  - filter-language (dropdown: English, Spanish, French)
  - apply-language-filter (button to apply filter)
  - play-guide-button-{guide_id} (button for each audio guide row)
  - back-to-dashboard (button navigates back to dashboard)
- Navigation button url_for mappings:
  - back-to-dashboard -> url_for('dashboard')
  - play-guide-button-{guide_id} -> (play action handled client-side or initiation)
- Context variables:
  - guides: list(dict) with audio guide data
  - filter_language: str (optional)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: `data/users.txt`
- Fields (pipe-delimited):
  - username
- Description: Stores usernames for authentication.
- Example rows:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

---

### 2. galleries.txt
- Filename: `data/galleries.txt`
- Fields (pipe-delimited):
  - gallery_id|gallery_name|floor|capacity|theme|status
- Description: Stores gallery details including location and status.
- Example rows:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

---

### 3. exhibitions.txt
- Filename: `data/exhibitions.txt`
- Fields (pipe-delimited):
  - exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Description: Stores exhibitions with metadata and curator info.
- Example rows:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

---

### 4. artifacts.txt
- Filename: `data/artifacts.txt`
- Fields (pipe-delimited):
  - artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Description: Stores artifact details linked to exhibitions.
- Example rows:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

---

### 5. audioguides.txt
- Filename: `data/audioguides.txt`
- Fields (pipe-delimited):
  - guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Description: Stores audio guide metadata and script text.
- Example rows:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

---

### 6. tickets.txt
- Filename: `data/tickets.txt`
- Fields (pipe-delimited):
  - ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Description: Records ticket purchases by visitors.
- Example rows:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

---

### 7. events.txt
- Filename: `data/events.txt`
- Fields (pipe-delimited):
  - event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Description: Stores virtual event details hosted by museums.
- Example rows:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

---

### 8. event_registrations.txt
- Filename: `data/event_registrations.txt`
- Fields (pipe-delimited):
  - registration_id|event_id|username|registration_date
- Description: Tracks user registrations to events.
- Example rows:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

---

### 9. collection_logs.txt
- Filename: `data/collection_logs.txt`
- Fields (pipe-delimited):
  - log_id|artifact_id|activity_type|date|notes|condition|curator
- Description: Logs activities related to artifact collection management.
- Example rows:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

# End of Design Specification Document
