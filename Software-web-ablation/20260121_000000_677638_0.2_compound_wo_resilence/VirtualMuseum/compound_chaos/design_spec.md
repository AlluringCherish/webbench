# Design Specification Document for VirtualMuseum Web Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name             | HTTP Method(s) | Template Filename         | Context Variables (name: type)                                                                                         |
|-------------------------------|---------------------------|----------------|---------------------------|------------------------------------------------------------------------------------------------------------------------|
| `/`                           | root_redirect             | GET            | None (redirect)            | None                                                                                                                   |
| `/dashboard`                  | dashboard_page            | GET            | dashboard.html            | `total_exhibitions: int`, `active_exhibitions: int`                                                                     |
| `/artifacts`                  | artifact_catalog_page     | GET            | artifact_catalog.html     | `artifacts: list[dict]` (Each dict contains artifact_id: int, artifact_name: str, period: str, origin: str, exhibition: str) |
| `/artifacts/filter`           | filter_artifacts          | POST           | artifact_catalog.html     | `artifacts: list[dict]`, `search_term: str`                                                                            |
| `/exhibitions`                | exhibitions_page          | GET            | exhibitions.html          | `exhibitions: list[dict]`, `filter_type: str or None`                                                                   |
| `/exhibitions/filter`         | filter_exhibitions        | POST           | exhibitions.html          | `exhibitions: list[dict]`, `filter_type: str`                                                                           |
| `/exhibition/<int:exhibition_id>` | exhibition_details_page   | GET            | exhibition_details.html   | `exhibition: dict`, `artifacts: list[dict]`                                                                             |
| `/tickets`                   | visitor_tickets_page      | GET            | visitor_tickets.html      | `user_tickets: list[dict]`                                                                                              |
| `/tickets/purchase`          | purchase_ticket           | POST           | visitor_tickets.html      | `purchase_status: str`, `user_tickets: list[dict]`                                                                      |
| `/events`                    | virtual_events_page       | GET            | virtual_events.html       | `events: list[dict]`, `user_registrations: list[int]` (event_ids)                                                      |
| `/events/register/<int:event_id>` | register_event          | POST           | virtual_events.html       | `registration_status: str`, `events: list[dict]`, `user_registrations: list[int]`                                       |
| `/events/cancel/<int:registration_id>` | cancel_registration | POST           | virtual_events.html       | `cancellation_status: str`, `events: list[dict]`, `user_registrations: list[int]`                                       |
| `/audioguides`               | audio_guides_page         | GET            | audio_guides.html         | `audioguides: list[dict]`, `filter_language: str or None`                                                               |
| `/audioguides/filter`        | filter_audio_guides       | POST           | audio_guides.html         | `audioguides: list[dict]`, `filter_language: str`                                                                        |


### Detailed Route Descriptions

- `/` (root_redirect): Redirects immediately to `/dashboard`.

- `/dashboard` (dashboard_page): GET route displaying the dashboard.html template with context variables `total_exhibitions` (int) and `active_exhibitions` (int).

- `/artifacts` (artifact_catalog_page): GET route displaying artifact_catalog.html with a list of all artifacts.

- `/artifacts/filter` (filter_artifacts): POST route accepting search/filter parameters, returns artifact_catalog.html with filtered artifacts and search_term.

- `/exhibitions` (exhibitions_page): GET route displaying all exhibitions.

- `/exhibitions/filter` (filter_exhibitions): POST route to filter exhibitions by type, returns exhibitions.html.

- `/exhibition/<int:exhibition_id>` (exhibition_details_page): GET route for detailed info on a single exhibition and its associated artifacts.

- `/tickets` (visitor_tickets_page): GET route for visitor tickets management, lists user tickets.

- `/tickets/purchase` (purchase_ticket): POST route for purchasing tickets, returns purchase status and updated ticket list.

- `/events` (virtual_events_page): GET route showing all virtual events and the user's event registrations.

- `/events/register/<int:event_id>` (register_event): POST route for event registration.

- `/events/cancel/<int:registration_id>` (cancel_registration): POST route for canceling an event registration.

- `/audioguides` (audio_guides_page): GET route showing all audio guides.

- `/audioguides/filter` (filter_audio_guides): POST route to filter audio guides by language.


---

## Section 2: HTML Templates Specification

### 1. `dashboard.html`
- File name: `dashboard.html`
- Page Title: Museum Dashboard
- Main Heading (`<h1>`): Museum Dashboard
- Element IDs:
  - `dashboard-page` (div container)
  - `exhibition-summary` (div showing total and active exhibitions)
  - `artifact-catalog-button` (button)
  - `exhibitions-button` (button)
  - `visitor-tickets-button` (button)
  - `virtual-events-button` (button)
  - `audio-guides-button` (button)
- Navigation Buttons Mapped to Flask Route Functions via url_for():
  - `artifact-catalog-button`: `url_for('artifact_catalog_page')`
  - `exhibitions-button`: `url_for('exhibitions_page')`
  - `visitor-tickets-button`: `url_for('visitor_tickets_page')`
  - `virtual-events-button`: `url_for('virtual_events_page')`
  - `audio-guides-button`: `url_for('audio_guides_page')`
- Context Variables:
  - `total_exhibitions` (int): displayed in `exhibition-summary`
  - `active_exhibitions` (int): displayed in `exhibition-summary`

### 2. `artifact_catalog.html`
- File name: `artifact_catalog.html`
- Page Title: Artifact Catalog
- Main Heading (`<h1>`): Artifact Catalog
- Element IDs:
  - `artifact-catalog-page` (div container)
  - `artifact-table` (table listing artifacts)
  - `search-artifact` (input field for search text)
  - `apply-artifact-filter` (button to apply search/filter)
  - `back-to-dashboard` (button)
- Navigation Buttons:
  - `back-to-dashboard`: `url_for('dashboard_page')`
- Context Variables:
  - `artifacts` (list of dict): Each dict with keys: artifact_id (int), artifact_name (str), period (str), origin (str), exhibition (str)
  - `search_term` (str): the current search/filter text

### 3. `exhibitions.html`
- File name: `exhibitions.html`
- Page Title: Exhibitions
- Main Heading (`<h1>`): Exhibitions
- Element IDs:
  - `exhibitions-page` (div container)
  - `exhibition-list` (table of exhibitions)
  - `filter-exhibition-type` (dropdown for exhibition types: Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (button)
  - `back-to-dashboard` (button)
  - Dynamic per exhibition row:
    - `view-exhibition-button-{{ exhibition.exhibition_id }}` (button to view details)
- Navigation Buttons:
  - `back-to-dashboard`: `url_for('dashboard_page')`
  - `view-exhibition-button-{{ exhibition.exhibition_id }}`: `url_for('exhibition_details_page', exhibition_id=exhibition.exhibition_id)`
- Context Variables:
  - `exhibitions` (list of dict): with exhibition_id (int), title (str), exhibition_type (str), start_date (str), end_date (str), gallery_name (str), status (str)
  - `filter_type` (str or None): current filter selected

### 4. `exhibition_details.html`
- File name: `exhibition_details.html`
- Page Title: Exhibition Details
- Main Heading (`<h1>`): Dynamic with exhibition title, element id `exhibition-title`
- Element IDs:
  - `exhibition-details-page` (div container)
  - `exhibition-title` (h1) - exhibition.title
  - `exhibition-description` (div)
  - `exhibition-dates` (div) - start and end dates
  - `exhibition-artifacts` (table) - artifacts in exhibition
  - `back-to-exhibitions` (button)
- Navigation Buttons:
  - `back-to-exhibitions`: `url_for('exhibitions_page')`
- Context Variables:
  - `exhibition` (dict): fields including title (str), description (str), start_date (str), end_date (str)
  - `artifacts` (list of dict): artifact info related to exhibition

### 5. `visitor_tickets.html`
- File name: `visitor_tickets.html`
- Page Title: Visitor Tickets
- Main Heading (`<h1>`): Visitor Tickets
- Element IDs:
  - `visitor-tickets-page` (div container)
  - `ticket-type` (dropdown: Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (input number)
  - `purchase-ticket-button` (button)
  - `my-tickets-table` (table) - showing purchased tickets
  - `back-to-dashboard` (button)
- Navigation Buttons:
  - `back-to-dashboard`: `url_for('dashboard_page')`
- Context Variables:
  - `user_tickets` (list of dict): each with ticket info (ticket_id, ticket_type, visit_date, number_of_tickets, price, visitor_name, visitor_email)
  - `purchase_status` (str): message about last purchase attempt

### 6. `virtual_events.html`
- File name: `virtual_events.html`
- Page Title: Virtual Events
- Main Heading (`<h1>`): Virtual Events
- Element IDs:
  - `virtual-events-page` (div container)
  - `event-list` (table) - event info
  - Dynamic per event row:
    - `register-event-button-{{ event.event_id }}` (button to register)
    - `cancel-registration-button-{{ registration.registration_id }}` (button to cancel)
  - `back-to-dashboard` (button)
- Navigation Buttons:
  - `back-to-dashboard`: `url_for('dashboard_page')`
  - `register-event-button-{{ event.event_id }}`: `url_for('register_event', event_id=event.event_id)`
  - `cancel-registration-button-{{ registration.registration_id }}`: `url_for('cancel_registration', registration_id=registration.registration_id)`
- Context Variables:
  - `events` (list of dict): event data
  - `user_registrations` (list of int): event_ids where user registered
  - `registrations` (list of dict): optional if needed for cancel button matching

### 7. `audio_guides.html`
- File name: `audio_guides.html`
- Page Title: Audio Guides
- Main Heading (`<h1>`): Audio Guides
- Element IDs:
  - `audio-guides-page` (div container)
  - `audio-guide-list` (table)
  - `filter-language` (dropdown: English, Spanish, French)
  - `apply-language-filter` (button)
  - Dynamic per guide row:
    - `play-guide-button-{{ guide.guide_id }}` (button to play audio guide)
  - `back-to-dashboard` (button)
- Navigation Buttons:
  - `back-to-dashboard`: `url_for('dashboard_page')`
  - `play-guide-button-{{ guide.guide_id }}`: `url_for('audio_guides_page')` or JS handler
- Context Variables:
  - `audioguides` (list of dict): with guide_id, exhibit_number, title, language, duration
  - `filter_language` (str or None): currently selected language filter

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: `data/users.txt`
- Content: List of usernames (one per line)
- Fields (single field):
  - `username` (str)
- Example Data:
```
curator_john
visitor_mary
curator_sarah
```

### 2. galleries.txt
- Filename: `data/galleries.txt`
- Pipe-delimited fields:
  1. `gallery_id` (int)
  2. `gallery_name` (str)
  3. `floor` (int)
  4. `capacity` (int)
  5. `theme` (str)
  6. `status` (str)
- Purpose: Stores info about museum galleries
- Example rows:
```
1|Ancient Civilizations Hall|1|50|Ancient|Open
2|Modern Art Wing|2|30|Modern|Open
3|Science Discovery Center|3|40|Science|Renovation
```

### 3. exhibitions.txt
- Filename: `data/exhibitions.txt`
- Pipe-delimited fields:
  1. `exhibition_id` (int)
  2. `title` (str)
  3. `description` (str)
  4. `gallery_id` (int)
  5. `exhibition_type` (str) (Permanent, Temporary, Virtual)
  6. `start_date` (str) (YYYY-MM-DD)
  7. `end_date` (str) (YYYY-MM-DD)
  8. `curator_name` (str)
  9. `created_by` (str) (username)
- Purpose: Contains exhibitions
- Example rows:
```
1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
```

### 4. artifacts.txt
- Filename: `data/artifacts.txt`
- Pipe-delimited fields:
  1. `artifact_id` (int)
  2. `artifact_name` (str)
  3. `period` (str)
  4. `origin` (str)
  5. `description` (str)
  6. `exhibition_id` (int)
  7. `storage_location` (str)
  8. `acquisition_date` (str) (YYYY-MM-DD)
  9. `added_by` (str)
- Purpose: Details about artifacts
- Example rows:
```
1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
```

### 5. audioguides.txt
- Filename: `data/audioguides.txt`
- Pipe-delimited fields:
  1. `guide_id` (int)
  2. `exhibit_number` (int)
  3. `title` (str)
  4. `language` (str)
  5. `duration` (int, minutes)
  6. `script` (str)
  7. `narrator` (str)
  8. `created_by` (str)
- Purpose: Contains audio guides metadata
- Example rows:
```
1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
```

### 6. tickets.txt
- Filename: `data/tickets.txt`
- Pipe-delimited fields:
  1. `ticket_id` (int)
  2. `username` (str)
  3. `ticket_type` (str) (Standard, Student, Senior, Family, VIP)
  4. `visit_date` (str, YYYY-MM-DD)
  5. `visit_time` (str, e.g. "11:00 AM")
  6. `number_of_tickets` (int)
  7. `price` (float)
  8. `visitor_name` (str)
  9. `visitor_email` (str)
  10. `purchase_date` (str, YYYY-MM-DD)
- Purpose: Tracks visitor ticket purchases
- Example rows:
```
1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
```

### 7. events.txt
- Filename: `data/events.txt`
- Pipe-delimited fields:
  1. `event_id` (int)
  2. `title` (str)
  3. `date` (str, YYYY-MM-DD)
  4. `time` (str, e.g. "2:00 PM")
  5. `event_type` (str) (Webinar, Artist Talk, Virtual Tour)
  6. `speaker` (str)
  7. `capacity` (int)
  8. `description` (str)
  9. `created_by` (str)
- Purpose: Virtual events information
- Example rows:
```
1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
```

### 8. event_registrations.txt
- Filename: `data/event_registrations.txt`
- Pipe-delimited fields:
  1. `registration_id` (int)
  2. `event_id` (int)
  3. `username` (str)
  4. `registration_date` (str, YYYY-MM-DD)
- Purpose: Tracks user registrations for events
- Example rows:
```
1|1|visitor_mary|2024-11-20
2|2|visitor_mary|2024-11-21
3|1|visitor_tom|2024-11-19
```

### 9. collection_logs.txt
- Filename: `data/collection_logs.txt`
- Pipe-delimited fields:
  1. `log_id` (int)
  2. `artifact_id` (int)
  3. `activity_type` (str) (Inspection, Cleaning, Photography, Restoration, etc.)
  4. `date` (str, YYYY-MM-DD)
  5. `notes` (str)
  6. `condition` (str) (e.g., Excellent, Good, Fair)
  7. `curator` (str)
- Purpose: Logs of artifact maintenance and activities
- Example rows:
```
1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
```

---

**End of Design Specification Document**
