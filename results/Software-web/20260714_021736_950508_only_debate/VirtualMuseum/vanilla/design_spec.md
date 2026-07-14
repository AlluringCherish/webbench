# VirtualMuseum Web Application Design Specification

---

## Section 1: Flask Routes Specification

1. `/` (GET)
   - Description: Root path, redirects to the Dashboard page.
   - Behavior: Redirects to `/dashboard`.

2. `/dashboard` (GET)
   - Description: Main hub showing overview of exhibitions, artifacts, and navigation.
   - Template: `dashboard.html`
   - Context Variables:
     - `total_exhibitions` (int)
     - `active_exhibitions` (int)

3. `/artifacts` (GET)
   - Description: Artifact Catalog page showing all artifacts with search/filter support.
   - Template: `artifact_catalog.html`
   - Context Variables:
     - `artifacts` (list of dicts with keys: artifact_id, artifact_name, period, origin, exhibition_title)

4. `/artifacts/search` (POST)
   - Description: Handles artifact search/filter form submission.
   - Template: `artifact_catalog.html`
   - Context Variables:
     - `artifacts` (filtered list of artifact dicts)

5. `/exhibitions` (GET)
   - Description: Exhibitions listing and filtering page.
   - Template: `exhibitions.html`
   - Context Variables:
     - `exhibitions` (list of dicts with keys: exhibition_id, title, exhibition_type, start_date, end_date, gallery_name, status)

6. `/exhibitions/filter` (POST)
   - Description: Applies exhibition type filter from dropdown.
   - Template: `exhibitions.html`
   - Context Variables:
     - `exhibitions` (filtered list of exhibition dicts)

7. `/exhibitions/<int:exhibition_id>` (GET)
   - Description: Exhibition Details page for a specific exhibition.
   - Template: `exhibition_details.html`
   - Context Variables:
     - `exhibition` (dict with exhibition details including exhibition_id, title, description, start_date, end_date)
     - `artifacts` (list of artifact dicts in this exhibition)

8. `/tickets` (GET)
   - Description: Visitor Tickets page showing ticket overview.
   - Template: `visitor_tickets.html`
   - Context Variables:
     - `tickets` (list of dicts showing tickets purchased by the current user)

9. `/tickets/purchase` (POST)
   - Description: Handles ticket purchase form submission.
   - Template: `visitor_tickets.html`
   - Context Variables:
     - `tickets` (updated list of tickets)

10. `/events` (GET)
    - Description: Virtual Events listing.
    - Template: `virtual_events.html`
    - Context Variables:
      - `events` (list of dicts with keys: event_id, title, date, time, event_type, registration_status per user)

11. `/events/register/<int:event_id>` (POST)
    - Description: Registers for a specified event.
    - Template: `virtual_events.html`
    - Context Variables:
      - `events` (updated events list with registration status)

12. `/events/cancel/<int:registration_id>` (POST)
    - Description: Cancels registration for a specified event.
    - Template: `virtual_events.html`
    - Context Variables:
      - `events` (updated events list)

13. `/audio-guides` (GET)
    - Description: Audio Guides browsing page.
    - Template: `audio_guides.html`
    - Context Variables:
      - `audio_guides` (list of dicts with keys: guide_id, exhibit_number, title, language, duration)

14. `/audio-guides/filter` (POST)
    - Description: Applies language filter for audio guides.
    - Template: `audio_guides.html`
    - Context Variables:
      - `audio_guides` (filtered list by language)

---

## Section 2: HTML Templates and Element IDs

### 1. Dashboard Page (`dashboard.html`)
- Page Title: Museum Dashboard
- Elements and IDs:
  - `dashboard-page` (Div container)
  - `exhibition-summary` (Div showing exhibition summary: total and active exhibitions)
  - `artifact-catalog-button` (Button, navigates to `/artifacts`)
  - `exhibitions-button` (Button, navigates to `/exhibitions`)
  - `visitor-tickets-button` (Button, navigates to `/tickets`)
  - `virtual-events-button` (Button, navigates to `/events`)
  - `audio-guides-button` (Button, navigates to `/audio-guides`)

### 2. Artifact Catalog Page (`artifact_catalog.html`)
- Page Title: Artifact Catalog
- Elements and IDs:
  - `artifact-catalog-page` (Div container)
  - `artifact-table` (Table displaying artifacts with columns: ID, Name, Period, Origin, Exhibition, Actions)
  - `search-artifact` (Input for artifact name or ID search)
  - `apply-artifact-filter` (Button to apply search/filter)
  - `back-to-dashboard` (Button, navigates to `/dashboard`)

### 3. Exhibitions Page (`exhibitions.html`)
- Page Title: Exhibitions
- Elements and IDs:
  - `exhibitions-page` (Div container)
  - `exhibition-list` (Table with columns: Title, Type, Dates, Gallery, Status)
  - `filter-exhibition-type` (Dropdown with options: Permanent, Temporary, Virtual)
  - `apply-exhibition-filter` (Button to apply selected filter)
  - `view-exhibition-button-{exhibition_id}` (Button to view details, dynamic per exhibition)
  - `back-to-dashboard` (Button, navigates to `/dashboard`)

### 4. Exhibition Details Page (`exhibition_details.html`)
- Page Title: Exhibition Details
- Elements and IDs:
  - `exhibition-details-page` (Div container)
  - `exhibition-title` (H1 for exhibition title)
  - `exhibition-description` (Div for exhibition description)
  - `exhibition-dates` (Div showing start and end dates)
  - `exhibition-artifacts` (Table listing artifacts in this exhibition)
  - `back-to-exhibitions` (Button, navigates to `/exhibitions`)

### 5. Visitor Tickets Page (`visitor_tickets.html`)
- Page Title: Visitor Tickets
- Elements and IDs:
  - `visitor-tickets-page` (Div container)
  - `ticket-type` (Dropdown with ticket types: Standard, Student, Senior, Family, VIP)
  - `number-of-tickets` (Input number for ticket quantity)
  - `purchase-ticket-button` (Button to purchase tickets)
  - `my-tickets-table` (Table showing user's purchased tickets)
  - `back-to-dashboard` (Button, navigates to `/dashboard`)

### 6. Virtual Events Page (`virtual_events.html`)
- Page Title: Virtual Events
- Elements and IDs:
  - `virtual-events-page` (Div container)
  - `event-list` (Table with columns: Title, Date, Time, Type, Registration Status)
  - `register-event-button-{event_id}` (Button to register for event, dynamic per event)
  - `cancel-registration-button-{registration_id}` (Button to cancel registration, dynamic per registration)
  - `back-to-dashboard` (Button, navigates to `/dashboard`)

### 7. Audio Guides Page (`audio_guides.html`)
- Page Title: Audio Guides
- Elements and IDs:
  - `audio-guides-page` (Div container)
  - `audio-guide-list` (Table with columns: Exhibit Number, Title, Language, Duration)
  - `filter-language` (Dropdown with options: English, Spanish, French)
  - `apply-language-filter` (Button to apply language filter)
  - `play-guide-button-{guide_id}` (Button to play guide, dynamic per guide)
  - `back-to-dashboard` (Button, navigates to `/dashboard`)

---

## Section 3: Local Text File Schemas

All data files reside in the `data/` directory and use pipe (`|`) as the field delimiter.

1. `users.txt`
   - Fields: `username`
   - Description: Authentication users, e.g., curators and visitors.
   - Example:
     ```
     curator_john
     visitor_mary
     curator_sarah
     ```

2. `galleries.txt`
   - Fields: `gallery_id|gallery_name|floor|capacity|theme|status`
   - Description: Gallery details including location and status.
   - Example:
     ```
     1|Ancient Civilizations Hall|1|50|Ancient|Open
     2|Modern Art Wing|2|30|Modern|Open
     3|Science Discovery Center|3|40|Science|Renovation
     ```

3. `exhibitions.txt`
   - Fields: `exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by`
   - Description: Exhibition metadata.
   - Example:
     ```
     1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
     2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
     3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
     ```

4. `artifacts.txt`
   - Fields: `artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by`
   - Description: Artifact details linked to exhibitions.
   - Example:
     ```
     1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
     2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
     3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
     ```

5. `audioguides.txt`
   - Fields: `guide_id|exhibit_number|title|language|duration|script|narrator|created_by`
   - Description: Audio guide metadata including language and narrator.
   - Example:
     ```
     1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
     2|101|Introducci\u0000n al Arte Egipcio|Spanish|5|Bienvenido a la exhibici\u0000n egipcia...|Maria Garcia|curator_john
     3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
     ```

6. `tickets.txt`
   - Fields: `ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date`
   - Description: Visitor ticket purchases.
   - Example:
     ```
     1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
     2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
     3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
     ```

7. `events.txt`
   - Fields: `event_id|title|date|time|event_type|speaker|capacity|description|created_by`
   - Description: Virtual museum event details.
   - Example:
     ```
     1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
     2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
     3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
     ```

8. `event_registrations.txt`
   - Fields: `registration_id|event_id|username|registration_date`
   - Description: Event registration records.
   - Example:
     ```
     1|1|visitor_mary|2024-11-20
     2|2|visitor_mary|2024-11-21
     3|1|visitor_tom|2024-11-19
     ```

9. `collection_logs.txt`
   - Fields: `log_id|artifact_id|activity_type|date|notes|condition|curator`
   - Description: Logs of artifact activities and conditions.
   - Example:
     ```
     1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
     2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
     3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
     4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
     ```

---

This specification consolidates all essential routes, templates, UI element IDs, and data schemas ensuring strict compliance with the user requirements for the VirtualMuseum Flask web application.