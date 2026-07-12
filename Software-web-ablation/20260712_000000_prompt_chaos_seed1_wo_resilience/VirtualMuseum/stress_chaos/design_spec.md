# Design Specification for VirtualMuseum Web Application

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name          | HTTP Method | Template Filename        | Context Variables
|--------------------------------|------------------------|-------------|--------------------------|--------------------------|
| /                              | root_redirect          | GET         | N/A (redirect to /dashboard) | None
| /dashboard                     | dashboard              | GET         | dashboard.html           | exhibitions_summary (dict: {total_exhibitions: int, active_exhibitions: int}), user (str, optional)
| /artifact_catalog              | artifact_catalog       | GET, POST  | artifact_catalog.html    | artifacts (list of dict), search_query (str, optional)
| /exhibitions                  | exhibitions            | GET, POST  | exhibitions.html        | exhibitions (list of dict), selected_filter (str, optional)
| /exhibition/<int:exhibition_id> | exhibition_details      | GET         | exhibition_details.html | exhibition (dict), artifacts (list of dict)
| /visitor_tickets              | visitor_tickets        | GET, POST  | visitor_tickets.html    | tickets (list of dict), purchase_status (str, optional)
| /virtual_events               | virtual_events         | GET, POST  | virtual_events.html     | events (list of dict), registrations (list of dict), registration_status (str, optional)
| /audio_guides                 | audio_guides           | GET, POST  | audio_guides.html       | audioguides (list of dict), selected_language (str, optional)

### Details:

- Root route '/' redirects to '/dashboard'.
- GET requests render pages with data loaded from respective data files.
- POST requests handle form submissions like search filters, ticket purchases, event registration, and language filter.
- Context variables use exact names (e.g., `exhibitions_summary`, `artifacts`, `events`).
- Dynamic routes use `<int:exhibition_id>` for showing exhibition details.
- Back navigation buttons route to dashboard or previous list pages.

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main Header (<h1>): "Museum Dashboard"
- Container Div ID: dashboard-page
- Element IDs:
  - exhibition-summary (Div) - Displays total exhibitions and active exhibitions.
  - artifact-catalog-button (Button) - Navigates to 'artifact_catalog' route.
  - exhibitions-button (Button) - Navigates to 'exhibitions' route.
  - visitor-tickets-button (Button) - Navigates to 'visitor_tickets' route.
  - virtual-events-button (Button) - Navigates to 'virtual_events' route.
  - audio-guides-button (Button) - Navigates to 'audio_guides' route.
- Context Variables:
  - exhibitions_summary (dict with keys: total_exhibitions (int), active_exhibitions (int)) used to show summary data.

### 2. artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main Header (<h1>): "Artifact Catalog"
- Container Div ID: artifact-catalog-page
- Element IDs:
  - artifact-table (Table) - Columns: ID, Name, Period, Origin, Exhibition, Actions
  - search-artifact (Input) - For user search input by artifact ID or name.
  - apply-artifact-filter (Button) - Applies the search filter to reload artifacts.
  - back-to-dashboard (Button) - Navigates to 'dashboard' route.
- Context Variables:
  - artifacts (list of dict) - List of artifact records.
  - search_query (str) - User input search string (optional).

### 3. exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main Header (<h1>): "Exhibitions"
- Container Div ID: exhibitions-page
- Element IDs:
  - exhibition-list (Table) - Columns: Title, Type, Dates, Gallery, Status, Actions
  - filter-exhibition-type (Dropdown) - Options: Permanent, Temporary, Virtual
  - apply-exhibition-filter (Button) - Applies exhibition type filter.
  - view-exhibition-button-{{ exhibition.exhibition_id }} (Button) - Dynamic button to view details for each exhibition.
  - back-to-dashboard (Button) - Navigates to 'dashboard' route.
- Context Variables:
  - exhibitions (list of dict) - List of exhibition records.
  - selected_filter (str) - Current selected exhibition type filter (optional).

### 4. exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main Header (<h1>) with ID exhibition-title - Show exhibition title
- Container Div ID: exhibition-details-page
- Element IDs:
  - exhibition-description (Div) - Description text
  - exhibition-dates (Div) - Shows start and end dates
  - exhibition-artifacts (Table) - Columns: Artifact ID, Name, Period, Origin, Description
  - back-to-exhibitions (Button) - Navigates to 'exhibitions' route.
- Context Variables:
  - exhibition (dict) - Detailed exhibition info
  - artifacts (list of dict) - Artifacts filtered by exhibition_id

### 5. visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main Header (<h1>): "Visitor Tickets"
- Container Div ID: visitor-tickets-page
- Element IDs:
  - ticket-type (Dropdown) - Options: Standard, Student, Senior, Family, VIP
  - number-of-tickets (Input number) - Number input for tickets
  - purchase-ticket-button (Button) - Submit ticket purchase
  - my-tickets-table (Table) - Displays user's purchased tickets with relevant columns.
  - back-to-dashboard (Button) - Navigates to 'dashboard' route.
- Context Variables:
  - tickets (list of dict) - Tickets purchased by logged user (or all if no user context)
  - purchase_status (str) - Feedback message after purchase (optional)

### 6. virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main Header (<h1>): "Virtual Events"
- Container Div ID: virtual-events-page
- Element IDs:
  - event-list (Table) - Columns: Title, Date, Time, Type, Registration Status, Actions
  - register-event-button-{{ event.event_id }} (Button) - Button to register for event
  - cancel-registration-button-{{ registration.registration_id }} (Button) - Button to cancel registration
  - back-to-dashboard (Button) - Navigates to 'dashboard' route.
- Context Variables:
  - events (list of dict) - List of all events
  - registrations (list of dict) - User's event registrations
  - registration_status (str) - Feedback message on registration (optional)

### 7. audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main Header (<h1>): "Audio Guides"
- Container Div ID: audio-guides-page
- Element IDs:
  - audio-guide-list (Table) - Columns: Exhibit Number, Title, Language, Duration, Actions
  - filter-language (Dropdown) - Filter options: English, Spanish, French
  - apply-language-filter (Button) - Apply language filter
  - play-guide-button-{{ guide.guide_id }} (Button) - Play audio guide
  - back-to-dashboard (Button) - Navigates to 'dashboard' route.
- Context Variables:
  - audioguides (list of dict) - All audio guides or filtered by language
  - selected_language (str) - Language filter applied (optional)

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Fields (pipe-delimited): username
- Purpose: Stores usernames for authentication and user identification.
- Example Data:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- Filename: data/galleries.txt
- Fields (pipe-delimited): gallery_id|gallery_name|floor|capacity|theme|status
- Purpose: Stores gallery details.
- Example Data:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Fields (pipe-delimited): exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Purpose: Stores exhibition information including type and scheduling.
- Example Data:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Fields (pipe-delimited): artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Purpose: Stores detailed artifact data linked to exhibitions.
- Example Data:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Fields (pipe-delimited): guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Purpose: Stores audio guides information.
- Example Data:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- Filename: data/tickets.txt
- Fields (pipe-delimited): ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Purpose: Stores visitor tickets purchased.
- Example Data:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- Filename: data/events.txt
- Fields (pipe-delimited): event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Purpose: Stores virtual event details.
- Example Data:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Fields (pipe-delimited): registration_id|event_id|username|registration_date
- Purpose: Stores registrations of users for virtual events.
- Example Data:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Fields (pipe-delimited): log_id|artifact_id|activity_type|date|notes|condition|curator
- Purpose: Logs activities related to artifact collection management.
- Example Data:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This design specification document provides a complete and structured guide for backend Flask route implementations, frontend HTML template construction, and the organization of data files to deliver the VirtualMuseum application fulfilling the specified requirements.