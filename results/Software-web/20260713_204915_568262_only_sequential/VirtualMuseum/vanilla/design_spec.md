# VirtualMuseum Flask Application Design Specification

---

## 1. Flask Routes Specification

| Route Path | Function Name | HTTP Method(s) | Template Rendered | Context Variables Passed |
|------------|---------------|----------------|-------------------|--------------------------|
| `/` | `root_redirect` | GET | Redirect to dashboard | None |
| `/dashboard` | `dashboard_page` | GET | `dashboard.html` | `exhibition_summary` (dict with total_exhibitions, active_exhibitions) |
| `/artifact-catalog` | `artifact_catalog_page` | GET, POST* (filter/search) | `artifact_catalog.html` | `artifacts` (list of dicts), `search_query` (str) [if POST], filter criteria |
| `/exhibitions` | `exhibitions_page` | GET, POST* (filter) | `exhibitions.html` | `exhibitions` (list of dicts), `filter_type` (str) [if POST] |
| `/exhibition/<int:exhibition_id>` | `exhibition_details_page` | GET | `exhibition_details.html` | `exhibition` (dict), `artifacts` (list of dicts) |
| `/visitor-tickets` | `visitor_tickets_page` | GET, POST* (purchase) | `visitor_tickets.html` | `tickets` (list of dicts), form submitted values on POST |
| `/virtual-events` | `virtual_events_page` | GET | `virtual_events.html` | `events` (list of dicts), `registrations` (list of dicts for user) |
| `/virtual-events/register/<int:event_id>` | `register_for_event` | POST | Redirect to virtual_events_page | None |
| `/virtual-events/cancel/<int:registration_id>` | `cancel_event_registration` | POST | Redirect to virtual_events_page | None |
| `/audio-guides` | `audio_guides_page` | GET, POST* (filter) | `audio_guides.html` | `audio_guides` (list of dicts), `filter_language` (str) [if POST] |

*Filters and searches submitted via POST methods.

---

## 2. HTML Templates Specification

### 2.1 `dashboard.html`
- Page Title (`<title>` and main `<h1>`): "Museum Dashboard"
- Container ID: `dashboard-page` (Div)
- Elements:
  - `exhibition-summary` (Div)
  - Buttons:
    - `artifact-catalog-button`
    - `exhibitions-button`
    - `visitor-tickets-button`
    - `virtual-events-button`
    - `audio-guides-button`

### 2.2 `artifact_catalog.html`
- Page Title: "Artifact Catalog"
- Container ID: `artifact-catalog-page` (Div)
- Elements:
  - `artifact-table` (Table with columns: ID, name, period, origin, exhibition, actions)
  - `search-artifact` (Input)
  - `apply-artifact-filter` (Button)
  - `back-to-dashboard` (Button)

### 2.3 `exhibitions.html`
- Page Title: "Exhibitions"
- Container ID: `exhibitions-page` (Div)
- Elements:
  - `exhibition-list` (Table with columns: title, type, dates, gallery, status)
  - `filter-exhibition-type` (Dropdown: Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (Button)
  - `view-exhibition-button-{exhibition_id}` (Button for each exhibition row, dynamic ID)
  - `back-to-dashboard` (Button)

### 2.4 `exhibition_details.html`
- Page Title: "Exhibition Details"
- Container ID: `exhibition-details-page` (Div)
- Elements:
  - `exhibition-title` (H1)
  - `exhibition-description` (Div)
  - `exhibition-dates` (Div)
  - `exhibition-artifacts` (Table)
  - `back-to-exhibitions` (Button)

### 2.5 `visitor_tickets.html`
- Page Title: "Visitor Tickets"
- Container ID: `visitor-tickets-page` (Div)
- Elements:
  - `ticket-type` (Dropdown: Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (Input number)
  - `purchase-ticket-button` (Button)
  - `my-tickets-table` (Table)
  - `back-to-dashboard` (Button)

### 2.6 `virtual_events.html`
- Page Title: "Virtual Events"
- Container ID: `virtual-events-page` (Div)
- Elements:
  - `event-list` (Table with columns: title, date, time, type, registration status)
  - `register-event-button-{event_id}` (Button, dynamic ID per event row)
  - `cancel-registration-button-{registration_id}` (Button, dynamic ID per registered event row)
  - `back-to-dashboard` (Button)

### 2.7 `audio_guides.html`
- Page Title: "Audio Guides"
- Container ID: `audio-guides-page` (Div)
- Elements:
  - `audio-guide-list` (Table with columns: exhibit number, title, language, duration)
  - `filter-language` (Dropdown: English, Spanish, French)
  - `apply-language-filter` (Button)
  - `play-guide-button-{guide_id}` (Button, dynamic ID per guide row)
  - `back-to-dashboard` (Button)

---

## 3. Navigation Flow

- From Dashboard (`dashboard.html`):
  - Click `artifact-catalog-button` → `/artifact-catalog`
  - Click `exhibitions-button` → `/exhibitions`
  - Click `visitor-tickets-button` → `/visitor-tickets`
  - Click `virtual-events-button` → `/virtual-events`
  - Click `audio-guides-button` → `/audio-guides`

- From Artifact Catalog (`artifact_catalog.html`):
  - Click `back-to-dashboard` → `/dashboard`

- From Exhibitions (`exhibitions.html`):
  - Click `view-exhibition-button-{exhibition_id}` → `/exhibition/<exhibition_id>`
  - Click `back-to-dashboard` → `/dashboard`

- From Exhibition Details (`exhibition_details.html`):
  - Click `back-to-exhibitions` → `/exhibitions`

- From Visitor Tickets (`visitor_tickets.html`):
  - Click `back-to-dashboard` → `/dashboard`

- From Virtual Events (`virtual_events.html`):
  - Click `back-to-dashboard` → `/dashboard`

- From Audio Guides (`audio_guides.html`):
  - Click `back-to-dashboard` → `/dashboard`

---

## 4. Data File Specifications

All data files are stored locally in the `data/` directory with pipe (`|`) as delimiter except `users.txt` which is a single username per line.

### 4.1 User Authentication Data
- File: `data/users.txt`
- Fields (one per line): `username`
- Sample:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 4.2 Gallery Data
- File: `data/galleries.txt`
- Delimiter: `|`
- Fields order:
  1. `gallery_id`
  2. `gallery_name`
  3. `floor`
  4. `capacity`
  5. `theme`
  6. `status`
- Sample:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 4.3 Exhibition Data
- File: `data/exhibitions.txt`
- Delimiter: `|`
- Fields order:
  1. `exhibition_id`
  2. `title`
  3. `description`
  4. `gallery_id`
  5. `exhibition_type`
  6. `start_date` (YYYY-MM-DD)
  7. `end_date` (YYYY-MM-DD)
  8. `curator_name`
  9. `created_by`
- Sample:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4.4 Artifact Data
- File: `data/artifacts.txt`
- Delimiter: `|`
- Fields order:
  1. `artifact_id`
  2. `artifact_name`
  3. `period`
  4. `origin`
  5. `description`
  6. `exhibition_id`
  7. `storage_location`
  8. `acquisition_date` (YYYY-MM-DD)
  9. `added_by`
- Sample:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 4.5 Audio Guide Data
- File: `data/audioguides.txt`
- Delimiter: `|`
- Fields order:
  1. `guide_id`
  2. `exhibit_number`
  3. `title`
  4. `language`
  5. `duration` (minutes)
  6. `script`
  7. `narrator`
  8. `created_by`
- Sample:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 4.6 Ticket Data
- File: `data/tickets.txt`
- Delimiter: `|`
- Fields order:
  1. `ticket_id`
  2. `username`
  3. `ticket_type`
  4. `visit_date` (YYYY-MM-DD)
  5. `visit_time` (hh:mm AM/PM)
  6. `number_of_tickets`
  7. `price`
  8. `visitor_name`
  9. `visitor_email`
  10. `purchase_date` (YYYY-MM-DD)
- Sample:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 4.7 Virtual Event Data
- File: `data/events.txt`
- Delimiter: `|`
- Fields order:
  1. `event_id`
  2. `title`
  3. `date` (YYYY-MM-DD)
  4. `time` (hh:mm AM/PM)
  5. `event_type`
  6. `speaker`
  7. `capacity`
  8. `description`
  9. `created_by`
- Sample:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 4.8 Event Registration Data
- File: `data/event_registrations.txt`
- Delimiter: `|`
- Fields order:
  1. `registration_id`
  2. `event_id`
  3. `username`
  4. `registration_date` (YYYY-MM-DD)
- Sample:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 4.9 Collection Log Data
- File: `data/collection_logs.txt`
- Delimiter: `|`
- Fields order:
  1. `log_id`
  2. `artifact_id`
  3. `activity_type`
  4. `date` (YYYY-MM-DD)
  5. `notes`
  6. `condition`
  7. `curator`
- Sample:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This design_spec.md fully defines the Flask routes, templates with elements including dynamic IDs, navigation between pages, and local data file schemas needed for independent backend and frontend implementation of the VirtualMuseum web app.