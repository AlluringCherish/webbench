# VirtualMuseum Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path            | HTTP Method | Template File              | Context Variables                                                     | Description / Notes                                    |
|-----------------------|-------------|----------------------------|----------------------------------------------------------------------|--------------------------------------------------------|
| `/`                   | GET         | dashboard.html             | `exhibition_summary`: {total_exhibitions: int, active_exhibitions: int} | The root path; renders Dashboard page as primary entry |
| `/dashboard`          | GET         | dashboard.html             | `exhibition_summary`                                                  | Alternate URL for Dashboard; same as root              |
| `/artifacts`          | GET         | artifact_catalog.html      | `artifacts`: List of artifact dicts with keys: 
  - artifact_id
  - artifact_name
  - period
  - origin
  - exhibition_title
| Displays all artifacts with search/filter support     |
| `/artifacts/search`   | POST        | artifact_catalog.html      | `artifacts` (filtered list)                                          | Handles search/filter form submission                   |
| `/exhibitions`        | GET         | exhibitions.html           | `exhibitions`: List of exhibitions with keys: 
  - exhibition_id
  - title
  - exhibition_type
  - start_date
  - end_date
  - gallery_name
  - status
| Shows exhibitions list with filter                     |
| `/exhibitions/filter` | POST        | exhibitions.html           | `exhibitions` (filtered)                                            | Applies filter from filter-exhibition-type dropdown    |
| `/exhibitions/<int:exhibition_id>` | GET | exhibition_details.html  | `exhibition`: dict with details including 
  - exhibition_id
  - title
  - description
  - dates (start_date, end_date)
  - artifacts: list of artifact dicts in this exhibition
| Shows detailed info for specific exhibition           |
| `/tickets`            | GET         | visitor_tickets.html       | `tickets`: List of tickets purchased by current user               | Visitor tickets overview and purchase form              |
| `/tickets/purchase`   | POST        | visitor_tickets.html       | `tickets` (updated list)                                           | Handle purchase ticket form submission                  |
| `/events`             | GET         | virtual_events.html        | `events`: List of events with keys: 
  - event_id
  - title
  - date
  - time
  - event_type
  - registration_status (per user) | Lists virtual museum events                            |
| `/events/register/<int:event_id>` | POST | virtual_events.html     | `events` (updated with registration status)                         | Handles registering for event                           |
| `/events/cancel/<int:registration_id>` | POST | virtual_events.html  | `events` (updated)                                                  | Handle cancellation of event registration               |
| `/audio-guides`       | GET         | audio_guides.html          | `audio_guides`: List of audio guide dicts with keys:
  - guide_id
  - exhibit_number
  - title
  - language
  - duration
| Lists and filters audio guides                         |
| `/audio-guides/filter`| POST        | audio_guides.html          | `audio_guides` (filtered by language)                               | Apply language filter                                   |

---

## Section 2: HTML Template and Element Mapping

### 1. dashboard.html
- Page Title: Museum Dashboard
- Container ID: `dashboard-page` (Div)
- Elements:
  - `exhibition-summary` (Div): shows total exhibitions and active exhibitions count
  - Buttons:
    - `artifact-catalog-button`: navigates to `/artifacts`
    - `exhibitions-button`: navigates to `/exhibitions`
    - `visitor-tickets-button`: navigates to `/tickets`
    - `virtual-events-button`: navigates to `/events`
    - `audio-guides-button`: navigates to `/audio-guides`

### 2. artifact_catalog.html
- Page Title: Artifact Catalog
- Container ID: `artifact-catalog-page` (Div)
- Elements:
  - `artifact-table` (Table): displays artifacts with columns: ID, Name, Period, Origin, Exhibition, Actions
    - Actions might include navigation buttons to exhibition details
  - Search input: `search-artifact`
  - `apply-artifact-filter` (Button): applies search/filter
  - `back-to-dashboard` (Button): navigates back to `/` or `/dashboard`

### 3. exhibitions.html
- Page Title: Exhibitions
- Container ID: `exhibitions-page` (Div)
- Elements:
  - `exhibition-list` (Table): displays exhibitions with columns: Title, Type, Dates, Gallery, Status
    - Each row includes button with dynamic ID: `view-exhibition-button-{exhibition_id}` to view details
  - Dropdown: `filter-exhibition-type` to select exhibition type filter
  - `apply-exhibition-filter` (Button)
  - `back-to-dashboard` (Button)

### 4. exhibition_details.html
- Page Title: Exhibition Details
- Container ID: `exhibition-details-page` (Div)
- Elements:
  - `exhibition-title` (H1)
  - `exhibition-description` (Div)
  - `exhibition-dates` (Div)
  - `exhibition-artifacts` (Table): lists artifacts in this exhibition
  - `back-to-exhibitions` (Button): navigates back to `/exhibitions`

### 5. visitor_tickets.html
- Page Title: Visitor Tickets
- Container ID: `visitor-tickets-page` (Div)
- Elements:
  - Dropdown: `ticket-type` (Standard, Student, Senior, Family, VIP)
  - Input (number): `number-of-tickets`
  - Button: `purchase-ticket-button`
  - Table: `my-tickets-table` showing user's purchased tickets
  - Button: `back-to-dashboard`

### 6. virtual_events.html
- Page Title: Virtual Events
- Container ID: `virtual-events-page` (Div)
- Elements:
  - Table: `event-list` with columns: Title, Date, Time, Type, Registration Status
    - Buttons per row:
      - `register-event-button-{event_id}`
      - `cancel-registration-button-{registration_id}`
  - `back-to-dashboard` Button

### 7. audio_guides.html
- Page Title: Audio Guides
- Container ID: `audio-guides-page` (Div)
- Elements:
  - Table: `audio-guide-list` with columns: Exhibit Number, Title, Language, Duration
    - Buttons per row: `play-guide-button-{guide_id}`
  - Dropdown: `filter-language` (English, Spanish, French)
  - Button: `apply-language-filter`
  - Button: `back-to-dashboard`

---

## Section 3: Local Text File Data Schemas

All data files are located under directory `data/` and use pipe (`|`) as the delimiter.

### 1. User Authentication Data
- File: `data/users.txt`
- Fields: `username`
- Example:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Gallery Data
- File: `data/galleries.txt`
- Fields: `gallery_id|gallery_name|floor|capacity|theme|status`
- Example:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibition Data
- File: `data/exhibitions.txt`
- Fields: `exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by`
- Example:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifact Data
- File: `data/artifacts.txt`
- Fields: `artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by`
- Example:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guide Data
- File: `data/audioguides.txt`
- Fields: `guide_id|exhibit_number|title|language|duration|script|narrator|created_by`
- Example:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducci\u0000n al Arte Egipcio|Spanish|5|Bienvenido a la exhibici\u0000n egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Ticket Data
- File: `data/tickets.txt`
- Fields: `ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date`
- Example:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Event Data
- File: `data/events.txt`
- Fields: `event_id|title|date|time|event_type|speaker|capacity|description|created_by`
- Example:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registration Data
- File: `data/event_registrations.txt`
- Fields: `registration_id|event_id|username|registration_date`
- Example:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Log Data
- File: `data/collection_logs.txt`
- Fields: `log_id|artifact_id|activity_type|date|notes|condition|curator`
- Example:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

**End of Design Specification Document**
