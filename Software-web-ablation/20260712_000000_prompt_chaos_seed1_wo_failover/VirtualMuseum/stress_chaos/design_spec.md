# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name           | HTTP Method(s) | Template Filename       | Context Variables (name: type)                                        |
|--------------------------------|-------------------------|----------------|-------------------------|----------------------------------------------------------------------|
| /                              | root_redirect            | GET            | None (redirect)          | None                                                                 |
| /dashboard                     | dashboard_page           | GET            | dashboard.html          | total_exhibitions: int, active_exhibitions: int                       |
| /artifacts                    | artifact_catalog_page    | GET, POST      | artifact_catalog.html   | artifacts: list of dict, filtered_artifacts: list of dict (on filter) |
| /exhibitions                  | exhibitions_page         | GET, POST      | exhibitions.html        | exhibitions: list of dict, filtered_exhibitions: list of dict (on filter), filter_type: str |
| /exhibition/<int:exhibition_id> | exhibition_details_page  | GET            | exhibition_details.html | exhibition: dict, artifacts: list of dict                             |
| /tickets                      | visitor_tickets_page     | GET, POST      | visitor_tickets.html    | tickets: list of dict, purchase_status: str (optional)               |
| /events                      | virtual_events_page      | GET, POST      | virtual_events.html     | events: list of dict, registrations: list of dict                    |
| /register_event/<int:event_id> | register_for_event       | POST           | None (redirect)          | None                                                                 |
| /cancel_registration/<int:registration_id> | cancel_event_registration | POST           | None (redirect)          | None                                                                 |
| /audio_guides                | audio_guides_page        | GET, POST      | audio_guides.html       | audio_guides: list of dict, filtered_guides: list of dict (on filter), filter_language: str |

**Route Details and Context Notes:**
- `/` redirects to `/dashboard`.
- Dashboard shows summary counts for exhibitions (all and active).
- Artifact catalog supports search/filter via POST; context includes filtered artifacts.
- Exhibitions page supports filtering by exhibition type, POST to apply filter.
- Exhibition details page shows specific exhibition info and its artifact list.
- Visitor tickets page allows ticket purchase via POST; shows user's tickets.
- Virtual events page shows events, user registrations; POST on event registration and cancellations redirect back.
- Audio guides page supports filtering by language.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: `dashboard.html`
- Page Title: "Museum Dashboard"
- Main H1: "Museum Dashboard"
- Element IDs:
  - `dashboard-page` (div container)
  - `exhibition-summary` (div showing total exhibitions and active exhibitions count)
  - `artifact-catalog-button` (button, navigates to artifact catalog page using `url_for('artifact_catalog_page')`)
  - `exhibitions-button` (button, navigates to exhibitions page using `url_for('exhibitions_page')`)
  - `visitor-tickets-button` (button, navigates to visitor tickets page using `url_for('visitor_tickets_page')`)
  - `virtual-events-button` (button, navigates to virtual events page using `url_for('virtual_events_page')`)
  - `audio-guides-button` (button, navigates to audio guides page using `url_for('audio_guides_page')`)
- Context Variables:
  - `total_exhibitions` (int): total number of exhibitions
  - `active_exhibitions` (int): count of exhibitions currently active

---

### 2. artifact_catalog.html
- Filename: `artifact_catalog.html`
- Page Title: "Artifact Catalog"
- Main H1: "Artifact Catalog"
- Element IDs:
  - `artifact-catalog-page` (div container)
  - `artifact-table` (table showing artifacts with columns: ID, name, period, origin, exhibition, actions)
  - `search-artifact` (input field for artifact name or ID search)
  - `apply-artifact-filter` (button to apply search/filter)
  - `back-to-dashboard` (button to navigate to dashboard via `url_for('dashboard_page')`)
- Context Variables:
  - `artifacts` (list of dict): all artifacts
  - `filtered_artifacts` (list of dict): filtered artifact list after search/filter, used to populate `artifact-table`

---

### 3. exhibitions.html
- Filename: `exhibitions.html`
- Page Title: "Exhibitions"
- Main H1: "Exhibitions"
- Element IDs:
  - `exhibitions-page` (div container)
  - `exhibition-list` (table showing exhibitions with columns: title, type, dates, gallery, status)
  - `filter-exhibition-type` (dropdown with options: Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (button to apply filter)
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` (button in each row to view exhibition details, uses `url_for('exhibition_details_page', exhibition_id=exhibition.exhibition_id)`)
  - `back-to-dashboard` (button to navigate to dashboard via `url_for('dashboard_page')`)
- Context Variables:
  - `exhibitions` (list of dict): all exhibitions
  - `filtered_exhibitions` (list of dict): filtered exhibitions after applying filter
  - `filter_type` (str): current filter selection

---

### 4. exhibition_details.html
- Filename: `exhibition_details.html`
- Page Title: "Exhibition Details"
- Main H1: Exhibition title from `exhibition['title']`
- Element IDs:
  - `exhibition-details-page` (div container)
  - `exhibition-title` (h1 showing exhibition title)
  - `exhibition-description` (div showing exhibition description)
  - `exhibition-dates` (div showing start and end dates)
  - `exhibition-artifacts` (table displaying artifacts in this exhibition)
  - `back-to-exhibitions` (button, navigates back to exhibitions list via `url_for('exhibitions_page')`)
- Context Variables:
  - `exhibition` (dict): exhibition details
  - `artifacts` (list of dict): artifacts belonging to this exhibition

---

### 5. visitor_tickets.html
- Filename: `visitor_tickets.html`
- Page Title: "Visitor Tickets"
- Main H1: "Visitor Tickets"
- Element IDs:
  - `visitor-tickets-page` (div container)
  - `ticket-type` (dropdown with options: Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (number input field)
  - `purchase-ticket-button` (button to submit ticket purchase)
  - `my-tickets-table` (table showing user's purchased tickets with relevant details)
  - `back-to-dashboard` (button to navigate back to dashboard via `url_for('dashboard_page')`)
- Context Variables:
  - `tickets` (list of dict): tickets purchased by current user
  - `purchase_status` (str, optional): message after purchase action

---

### 6. virtual_events.html
- Filename: `virtual_events.html`
- Page Title: "Virtual Events"
- Main H1: "Virtual Events"
- Element IDs:
  - `virtual-events-page` (div container)
  - `event-list` (table showing events with columns: title, date, time, type, registration status)
  - `register-event-button-{{ event.event_id }}` (button to register for event, uses `url_for('register_for_event', event_id=event.event_id)`)
  - `cancel-registration-button-{{ registration.registration_id }}` (button to cancel registration, uses `url_for('cancel_event_registration', registration_id=registration.registration_id)`)
  - `back-to-dashboard` (button to navigate back to dashboard via `url_for('dashboard_page')`)
- Context Variables:
  - `events` (list of dict): all events
  - `registrations` (list of dict): current user's event registrations

---

### 7. audio_guides.html
- Filename: `audio_guides.html`
- Page Title: "Audio Guides"
- Main H1: "Audio Guides"
- Element IDs:
  - `audio-guides-page` (div container)
  - `audio-guide-list` (table showing audio guides with columns: exhibit number, title, language, duration)
  - `filter-language` (dropdown with options: English, Spanish, French)
  - `apply-language-filter` (button to apply language filter)
  - `play-guide-button-{{ guide.guide_id }}` (button to play audio guide, uses `url_for('audio_guides_page')` or JS handler)
  - `back-to-dashboard` (button to navigate back to dashboard via `url_for('dashboard_page')`)
- Context Variables:
  - `audio_guides` (list of dict): all audio guides
  - `filtered_guides` (list of dict): audio guides after applying language filter
  - `filter_language` (str): current selected language filter

---

## Section 3: Data File Schemas

### 1. users.txt
- Location: `data/users.txt`
- Fields: `username`
- Purpose: Stores usernames for authentication
- Example Rows:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

---

### 2. galleries.txt
- Location: `data/galleries.txt`
- Fields: `gallery_id|gallery_name|floor|capacity|theme|status`
- Purpose: Stores gallery information
- Example Rows:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

---

### 3. exhibitions.txt
- Location: `data/exhibitions.txt`
- Fields: `exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by`
- Purpose: Stores exhibition details
- Example Rows:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

---

### 4. artifacts.txt
- Location: `data/artifacts.txt`
- Fields: `artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by`
- Purpose: Stores artifact information
- Example Rows:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

---

### 5. audioguides.txt
- Location: `data/audioguides.txt`
- Fields: `guide_id|exhibit_number|title|language|duration|script|narrator|created_by`
- Purpose: Stores audio guide data
- Example Rows:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

---

### 6. tickets.txt
- Location: `data/tickets.txt`
- Fields: `ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date`
- Purpose: Stores visitor ticket purchases
- Example Rows:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

---

### 7. events.txt
- Location: `data/events.txt`
- Fields: `event_id|title|date|time|event_type|speaker|capacity|description|created_by`
- Purpose: Stores virtual event details
- Example Rows:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

---

### 8. event_registrations.txt
- Location: `data/event_registrations.txt`
- Fields: `registration_id|event_id|username|registration_date`
- Purpose: Stores user registrations for events
- Example Rows:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

---

### 9. collection_logs.txt
- Location: `data/collection_logs.txt`
- Fields: `log_id|artifact_id|activity_type|date|notes|condition|curator`
- Purpose: Logs activity history of artifacts
- Example Rows:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

# End of Design Specification
