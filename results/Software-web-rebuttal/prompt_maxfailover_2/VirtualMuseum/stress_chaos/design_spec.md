# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path | Function Name | HTTP Method | Template Filename | Context Variables |
|---|---|---|---|---|
| / | root_redirect | GET | None (redirect to /dashboard) | None |
| /dashboard | dashboard | GET | dashboard.html | exhibition_summary (dict: total_exhibitions:int, active_exhibitions:int) |
| /artifact_catalog | artifact_catalog | GET, POST | artifact_catalog.html | artifacts (list of dict), search_query (str, optional), filter_applied (bool) |
| /exhibitions | exhibitions | GET, POST | exhibitions.html | exhibitions (list of dict), exhibition_types (list of str), selected_type (str, optional) |
| /exhibition/<int:exhibition_id> | exhibition_details | GET | exhibition_details.html | exhibition (dict), artifacts (list of dict) |
| /visitor_tickets | visitor_tickets | GET, POST | visitor_tickets.html | ticket_types (list of str), purchased_tickets (list of dict) |
| /virtual_events | virtual_events | GET, POST | virtual_events.html | events (list of dict), registrations (list of dict), user_registrations (list of dict), user_name (str) |
| /audio_guides | audio_guides | GET, POST | audio_guides.html | audio_guides (list of dict), languages (list of str), selected_language (str, optional) |


Detailed Route Information:

1. **Root Route `/`**
   - Function Name: `root_redirect`
   - HTTP Method: GET
   - Redirects to `/dashboard`

2. **Dashboard `/dashboard`**
   - Function Name: `dashboard`
   - HTTP Method: GET
   - Template: `dashboard.html`
   - Context Variables:
     - `exhibition_summary`: dict with keys
       - `total_exhibitions` (int)
       - `active_exhibitions` (int)

3. **Artifact Catalog `/artifact_catalog`**
   - Function Name: `artifact_catalog`
   - HTTP Method: GET, POST
   - Template: `artifact_catalog.html`
   - Context Variables:
     - `artifacts`: list of dicts each with fields: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str), `exhibition` (str)
     - `search_query`: str (optional, present on POST with search/filter)
     - `filter_applied`: bool

4. **Exhibitions `/exhibitions`**
   - Function Name: `exhibitions`
   - HTTP Method: GET, POST
   - Template: `exhibitions.html`
   - Context Variables:
     - `exhibitions`: list of dicts each with keys: `exhibition_id` (int), `title` (str), `exhibition_type` (str), `start_date` (str), `end_date` (str), `gallery` (str), `status` (str)
     - `exhibition_types`: list of str [`Permanent`, `Temporary`, `Virtual`]
     - `selected_type`: str (optional, filter selection)

5. **Exhibition Details `/exhibition/<int:exhibition_id>`**
   - Function Name: `exhibition_details`
   - HTTP Method: GET
   - Template: `exhibition_details.html`
   - Context Variables:
     - `exhibition`: dict with keys: `exhibition_id` (int), `title` (str), `description` (str), `start_date` (str), `end_date` (str)
     - `artifacts`: list of dicts for artifacts in exhibition each with keys: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str), `description` (str)

6. **Visitor Tickets `/visitor_tickets`**
   - Function Name: `visitor_tickets`
   - HTTP Method: GET, POST
   - Template: `visitor_tickets.html`
   - Context Variables:
     - `ticket_types`: list of str [`Standard`, `Student`, `Senior`, `Family`, `VIP`]
     - `purchased_tickets`: list of dicts with keys: `ticket_id` (int), `ticket_type` (str), `visit_date` (str), `visit_time` (str), `number_of_tickets` (int), `price` (float), `visitor_name` (str), `visitor_email` (str), `purchase_date` (str)

7. **Virtual Events `/virtual_events`**
   - Function Name: `virtual_events`
   - HTTP Method: GET, POST
   - Template: `virtual_events.html`
   - Context Variables:
     - `events`: list of dicts each with keys: `event_id` (int), `title` (str), `date` (str), `time` (str), `event_type` (str), `speaker` (str), `capacity` (int), `description` (str)
     - `registrations`: list of dicts with keys: `registration_id` (int), `event_id` (int), `username` (str), `registration_date` (str)
     - `user_registrations`: list of dicts for logged-in user registrations
     - `user_name`: str current user username

8. **Audio Guides `/audio_guides`**
   - Function Name: `audio_guides`
   - HTTP Method: GET, POST
   - Template: `audio_guides.html`
   - Context Variables:
     - `audio_guides`: list of dicts each with keys: `guide_id` (int), `exhibit_number` (str), `title` (str), `language` (str), `duration` (int, minutes)
     - `languages`: list of str [`English`, `Spanish`, `French`]
     - `selected_language`: str (optional)


## Section 2: HTML Templates Specification

---

### 1. dashboard.html
- Page Title: "Museum Dashboard"
- Main Heading (<h1>): "Museum Dashboard"
- Container Div ID: `dashboard-page`
- Elements and IDs:
  - Div: `exhibition-summary` (displays total exhibitions and active exhibitions counts)
  - Button: `artifact-catalog-button` (navigates to artifact_catalog)
  - Button: `exhibitions-button` (navigates to exhibitions)
  - Button: `visitor-tickets-button` (navigates to visitor_tickets)
  - Button: `virtual-events-button` (navigates to virtual_events)
  - Button: `audio-guides-button` (navigates to audio_guides)

- Navigation Button Mappings (using url_for):
  - `artifact-catalog-button` -> `artifact_catalog`
  - `exhibitions-button` -> `exhibitions`
  - `visitor-tickets-button` -> `visitor_tickets`
  - `virtual-events-button` -> `virtual_events`
  - `audio-guides-button` -> `audio_guides`

- Context Variables:
  - `exhibition_summary` (dict) with keys `total_exhibitions` (int), `active_exhibitions` (int)

---

### 2. artifact_catalog.html
- Page Title: "Artifact Catalog"
- Main Heading (<h1>): "Artifact Catalog"
- Container Div ID: `artifact-catalog-page`
- Elements and IDs:
  - Table: `artifact-table` with columns: ID, Name, Period, Origin, Exhibition, Actions
  - Input: `search-artifact` for search field
  - Button: `apply-artifact-filter` to apply filters/search
  - Button: `back-to-dashboard` to return to dashboard

- Navigation Button Mappings:
  - `back-to-dashboard` -> `dashboard`

- Actions within table (no specified IDs for action buttons, assumed no separate button IDs needed for each artifact)

- Context Variables:
  - `artifacts` (list of dicts with artifact fields)
  - `search_query` (str, optional)
  - `filter_applied` (bool)

---

### 3. exhibitions.html
- Page Title: "Exhibitions"
- Main Heading (<h1>): "Exhibitions"
- Container Div ID: `exhibitions-page`
- Elements and IDs:
  - Table: `exhibition-list` with columns: Title, Type, Dates, Gallery, Status, Actions
  - Dropdown: `filter-exhibition-type` with options "Permanent", "Temporary", "Virtual"
  - Button: `apply-exhibition-filter`
  - Buttons per row: `view-exhibition-button-{{ exhibition.exhibition_id }}` (one per exhibition)
  - Button: `back-to-dashboard`

- Navigation Button Mappings:
  - `back-to-dashboard` -> `dashboard`
  - `view-exhibition-button-{{ exhibition.exhibition_id }}` -> `exhibition_details` with `exhibition_id` param

- Context Variables:
  - `exhibitions` (list of dicts)
  - `exhibition_types` (list of str)
  - `selected_type` (str, optional)

---

### 4. exhibition_details.html
- Page Title: "Exhibition Details"
- Main Heading (<h1>): Exhibition title from `exhibition.title`
- Container Div ID: `exhibition-details-page`
- Elements and IDs:
  - H1: `exhibition-title` (exhibition title)
  - Div: `exhibition-description` (exhibition description)
  - Div: `exhibition-dates` (shows start and end dates)
  - Table: `exhibition-artifacts` showing artifact details
  - Button: `back-to-exhibitions`

- Navigation Button Mappings:
  - `back-to-exhibitions` -> `exhibitions`

- Context Variables:
  - `exhibition` (dict)
  - `artifacts` (list of dicts)

---

### 5. visitor_tickets.html
- Page Title: "Visitor Tickets"
- Main Heading (<h1>): "Visitor Tickets"
- Container Div ID: `visitor-tickets-page`
- Elements and IDs:
  - Dropdown: `ticket-type` with options `Standard`, `Student`, `Senior`, `Family`, `VIP`
  - Input (number): `number-of-tickets`
  - Button: `purchase-ticket-button`
  - Table: `my-tickets-table` displaying purchased tickets with columns including ticket type, visit date/time, ticket count, price, visitor info, purchase date
  - Button: `back-to-dashboard`

- Navigation Button Mappings:
  - `back-to-dashboard` -> `dashboard`

- Context Variables:
  - `ticket_types` (list of str)
  - `purchased_tickets` (list of dicts)

---

### 6. virtual_events.html
- Page Title: "Virtual Events"
- Main Heading (<h1>): "Virtual Events"
- Container Div ID: `virtual-events-page`
- Elements and IDs:
  - Table: `event-list` with columns: Title, Date, Time, Type, Registration Status, Actions
  - Button per row: `register-event-button-{{ event.event_id }}` to register
  - Button per row: `cancel-registration-button-{{ registration.registration_id }}` to cancel registration
  - Button: `back-to-dashboard`

- Navigation Button Mappings:
  - `back-to-dashboard` -> `dashboard`
  - `register-event-button-{{ event.event_id }}` -> route handling registration
  - `cancel-registration-button-{{ registration.registration_id }}` -> route handling cancellation

- Context Variables:
  - `events` (list of dicts)
  - `registrations` (list of dicts)
  - `user_registrations` (list of dicts)
  - `user_name` (str)

---

### 7. audio_guides.html
- Page Title: "Audio Guides"
- Main Heading (<h1>): "Audio Guides"
- Container Div ID: `audio-guides-page`
- Elements and IDs:
  - Table: `audio-guide-list` with columns: Exhibit Number, Title, Language, Duration, Actions
  - Dropdown: `filter-language` with options `English`, `Spanish`, `French`
  - Button: `apply-language-filter`
  - Button per row: `play-guide-button-{{ guide.guide_id }}` to play audio
  - Button: `back-to-dashboard`

- Navigation Button Mappings:
  - `back-to-dashboard` -> `dashboard`
  - `play-guide-button-{{ guide.guide_id }}` -> route handling playing guide

- Context Variables:
  - `audio_guides` (list of dicts)
  - `languages` (list of str)
  - `selected_language` (str, optional)


---

## Section 3: Data File Schemas

1. **users.txt**
   - Location: `data/users.txt`
   - Fields (pipe-delimited):
     - username
   - Purpose: User authentication usernames
   - Example rows:
     ```
     curator_john
     visitor_mary
     curator_sarah
     ```

2. **galleries.txt**
   - Location: `data/galleries.txt`
   - Fields:
     - gallery_id (int)
     - gallery_name (str)
     - floor (int)
     - capacity (int)
     - theme (str)
     - status (str)
   - Purpose: Details of museum galleries
   - Example rows:
     ```
     1|Ancient Civilizations Hall|1|50|Ancient|Open
     2|Modern Art Wing|2|30|Modern|Open
     3|Science Discovery Center|3|40|Science|Renovation
     ```

3. **exhibitions.txt**
   - Location: `data/exhibitions.txt`
   - Fields:
     - exhibition_id (int)
     - title (str)
     - description (str)
     - gallery_id (int)
     - exhibition_type (str)
     - start_date (YYYY-MM-DD)
     - end_date (YYYY-MM-DD)
     - curator_name (str)
     - created_by (str)
   - Purpose: Information on exhibitions
   - Example rows:
     ```
     1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
     2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
     3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
     ```

4. **artifacts.txt**
   - Location: `data/artifacts.txt`
   - Fields:
     - artifact_id (int)
     - artifact_name (str)
     - period (str)
     - origin (str)
     - description (str)
     - exhibition_id (int)
     - storage_location (str)
     - acquisition_date (YYYY-MM-DD)
     - added_by (str)
   - Purpose: Artifact collection details
   - Example rows:
     ```
     1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
     2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
     3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
     ```

5. **audioguides.txt**
   - Location: `data/audioguides.txt`
   - Fields:
     - guide_id (int)
     - exhibit_number (str)
     - title (str)
     - language (str)
     - duration (int, minutes)
     - script (str)
     - narrator (str)
     - created_by (str)
   - Purpose: Audio guides metadata
   - Example rows:
     ```
     1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
     2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
     3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
     ```

6. **tickets.txt**
   - Location: `data/tickets.txt`
   - Fields:
     - ticket_id (int)
     - username (str)
     - ticket_type (str)
     - visit_date (YYYY-MM-DD)
     - visit_time (str)
     - number_of_tickets (int)
     - price (float)
     - visitor_name (str)
     - visitor_email (str)
     - purchase_date (YYYY-MM-DD)
   - Purpose: Visitor ticket sales data
   - Example rows:
     ```
     1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
     2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
     3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
     ```

7. **events.txt**
   - Location: `data/events.txt`
   - Fields:
     - event_id (int)
     - title (str)
     - date (YYYY-MM-DD)
     - time (str)
     - event_type (str)
     - speaker (str)
     - capacity (int)
     - description (str)
     - created_by (str)
   - Purpose: Virtual museum events
   - Example rows:
     ```
     1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
     2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
     3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
     ```

8. **event_registrations.txt**
   - Location: `data/event_registrations.txt`
   - Fields:
     - registration_id (int)
     - event_id (int)
     - username (str)
     - registration_date (YYYY-MM-DD)
   - Purpose: User registrations for events
   - Example rows:
     ```
     1|1|visitor_mary|2024-11-20
     2|2|visitor_mary|2024-11-21
     3|1|visitor_tom|2024-11-19
     ```

9. **collection_logs.txt**
   - Location: `data/collection_logs.txt`
   - Fields:
     - log_id (int)
     - artifact_id (int)
     - activity_type (str)
     - date (YYYY-MM-DD)
     - notes (str)
     - condition (str)
     - curator (str)
   - Purpose: Logs of artifact activities and condition
   - Example rows:
     ```
     1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
     2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
     3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
     4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
     ```

---

This completes the detailed design specification document for 'VirtualMuseum'. The provided three sections enable backend and frontend teams to work independently and ensure consistent integration.

