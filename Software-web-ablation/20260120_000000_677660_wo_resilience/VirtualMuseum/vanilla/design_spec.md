# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Method     | Template Rendered        | Context Variables (Name:Type)                                                                                         |
|-------------------------------|-----------------------------|-----------------|--------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect               | GET             | Redirect to /dashboard   | None                                                                                                                   |
| /dashboard                    | dashboard                  | GET             | dashboard.html           | exhibitions_summary: dict (keys: total_exhibitions:int, active_exhibitions:int)
  
| /artifacts                   | artifact_catalog            | GET, POST       | artifact_catalog.html    | artifacts: list of dict (artifact_id:int, artifact_name:str, period:str, origin:str, exhibition_title:str)
  search_query: str (from form or query param)
  
| /exhibitions                 | exhibitions_list            | GET, POST       | exhibitions.html         | exhibitions: list of dict (exhibition_id:int, title:str, exhibition_type:str, start_date:str, end_date:str, gallery_name:str, status:str)
  filter_type: str (Permanent, Temporary, Virtual or empty for all)
  
| /exhibition/<int:exhibition_id> | exhibition_details        | GET             | exhibition_details.html  | exhibition: dict (exhibition_id:int, title:str, description:str, start_date:str, end_date:str)
  artifacts: list of dict (artifact_id:int, artifact_name:str, period:str, origin:str)
  
| /tickets                    | visitor_tickets             | GET, POST       | visitor_tickets.html     | tickets: list of dict (ticket_id:int, ticket_type:str, visit_date:str, visit_time:str, number_of_tickets:int, price:str)
  username: str (current user)
  form submission data: ticket_type:str, number_of_tickets:int
  
| /events                     | virtual_events              | GET, POST       | virtual_events.html      | events: list of dict (event_id:int, title:str, date:str, time:str, event_type:str, registration_status:bool)
  user_registrations: list of int (event_ids for current user)
  
| /event/register/<int:event_id>  | register_event            | POST            | Redirect to /events      | registration action for event_id
  
| /event/cancel/<int:registration_id> | cancel_event_registration| POST            | Redirect to /events      | cancel registration action for given registration_id
  
| /audio-guides               | audio_guides                | GET, POST       | audio_guides.html        | audio_guides: list of dict (guide_id:int, exhibit_number:str, title:str, language:str, duration:str)
  filter_language: str (English, Spanish, French or empty for all)
  

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: `dashboard.html`
- Page Title and H1: "Museum Dashboard"
- Element IDs and Types:
  - `dashboard-page`: Div container for the dashboard
  - `exhibition-summary`: Div showing total and active exhibitions
  - `artifact-catalog-button`: Button | url_for('artifact_catalog')
  - `exhibitions-button`: Button | url_for('exhibitions_list')
  - `visitor-tickets-button`: Button | url_for('visitor_tickets')
  - `virtual-events-button`: Button | url_for('virtual_events')
  - `audio-guides-button`: Button | url_for('audio_guides')
- Context Variables:
  - `exhibitions_summary` (dict): with keys `total_exhibitions` (int), `active_exhibitions` (int)

### 2. artifact_catalog.html
- Filename: `artifact_catalog.html`
- Page Title and H1: "Artifact Catalog"
- Element IDs and Types:
  - `artifact-catalog-page`: Div container
  - `artifact-table`: Table displaying columns ID, Name, Period, Origin, Exhibition, Actions
  - `search-artifact`: Input text for searching by name or ID
  - `apply-artifact-filter`: Button to apply the search/filter
  - `back-to-dashboard`: Button | url_for('dashboard')
- Context Variables:
  - `artifacts` (list of dict): each dict with keys `artifact_id`(int), `artifact_name`(str), `period`(str), `origin`(str), `exhibition_title`(str)
  - `search_query` (str): current search string to populate input

### 3. exhibitions.html
- Filename: `exhibitions.html`
- Page Title and H1: "Exhibitions"
- Element IDs and Types:
  - `exhibitions-page`: Div container
  - `exhibition-list`: Table with columns Title, Type, Dates, Gallery, Status, View Button
  - `filter-exhibition-type`: Dropdown with options: Permanent, Temporary, Virtual
  - `apply-exhibition-filter`: Button to apply filter
  - `view-exhibition-button-{{ exhibition.exhibition_id }}`: Dynamic button for each exhibition row
  - `back-to-dashboard`: Button | url_for('dashboard')
- Context Variables:
  - `exhibitions` (list of dict): keys `exhibition_id`(int), `title`(str), `exhibition_type`(str), `start_date`(str), `end_date`(str), `gallery_name`(str), `status`(str)
  - `filter_type` (str): current filter selection

### 4. exhibition_details.html
- Filename: `exhibition_details.html`
- Page Title and H1: "Exhibition Details"
- Element IDs and Types:
  - `exhibition-details-page`: Div container
  - `exhibition-title`: H1 element for exhibition title
  - `exhibition-description`: Div for exhibition description text
  - `exhibition-dates`: Div showing start and end dates
  - `exhibition-artifacts`: Table for artifacts in exhibition
  - `back-to-exhibitions`: Button | url_for('exhibitions_list')
- Context Variables:
  - `exhibition` (dict): keys `exhibition_id`(int), `title`(str), `description`(str), `start_date`(str), `end_date`(str)
  - `artifacts` (list of dict): keys `artifact_id`(int), `artifact_name`(str), `period`(str), `origin`(str)

### 5. visitor_tickets.html
- Filename: `visitor_tickets.html`
- Page Title and H1: "Visitor Tickets"
- Element IDs and Types:
  - `visitor-tickets-page`: Div container
  - `ticket-type`: Dropdown with options: Standard, Student, Senior, Family, VIP
  - `number-of-tickets`: Input (number) for ticket quantity
  - `purchase-ticket-button`: Button to submit purchase
  - `my-tickets-table`: Table displaying columns ticket_id, ticket_type, visit_date, visit_time, number_of_tickets, price
  - `back-to-dashboard`: Button | url_for('dashboard')
- Context Variables:
  - `tickets` (list of dict): keys `ticket_id`(int), `ticket_type`(str), `visit_date`(str), `visit_time`(str), `number_of_tickets`(int), `price`(str)
  - `username` (str): current user's username

### 6. virtual_events.html
- Filename: `virtual_events.html`
- Page Title and H1: "Virtual Events"
- Element IDs and Types:
  - `virtual-events-page`: Div container
  - `event-list`: Table columns Title, Date, Time, Type, Registration Status
  - `register-event-button-{{ event.event_id }}`: Dynamic button to register for event
  - `cancel-registration-button-{{ registration.registration_id }}`: Dynamic button to cancel registration
  - `back-to-dashboard`: Button | url_for('dashboard')
- Context Variables:
  - `events` (list of dict): keys `event_id`(int), `title`(str), `date`(str), `time`(str), `event_type`(str), `registration_status`(bool)
  - `user_registrations` (list of int): event_ids registered by current user

### 7. audio_guides.html
- Filename: `audio_guides.html`
- Page Title and H1: "Audio Guides"
- Element IDs and Types:
  - `audio-guides-page`: Div container
  - `audio-guide-list`: Table showing exhibit_number, title, language, duration, play button
  - `filter-language`: Dropdown with options English, Spanish, French
  - `apply-language-filter`: Button to apply filter selection
  - `play-guide-button-{{ guide.guide_id }}`: Dynamic button to play guide
  - `back-to-dashboard`: Button | url_for('dashboard')
- Context Variables:
  - `audio_guides` (list of dict): keys `guide_id`(int), `exhibit_number`(str), `title`(str), `language`(str), `duration`(str)
  - `filter_language` (str): currently selected filter

---

## Section 3: Data File Schemas

### 1. users.txt
- Filename: data/users.txt
- Content: List of usernames
- Fields (pipe-delimited):
  - username
- Example rows:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. galleries.txt
- Filename: data/galleries.txt
- Content: Galleries information for exhibitions
- Fields:
  - gallery_id|gallery_name|floor|capacity|theme|status
- Example rows:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. exhibitions.txt
- Filename: data/exhibitions.txt
- Content: Exhibition details including type, dates, curator
- Fields:
  - exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Example rows:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. artifacts.txt
- Filename: data/artifacts.txt
- Content: Artifact details linked to exhibition
- Fields:
  - artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Example rows:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. audioguides.txt
- Filename: data/audioguides.txt
- Content: Audio guides metadata
- Fields:
  - guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Example rows:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. tickets.txt
- Filename: data/tickets.txt
- Content: Ticket purchases records
- Fields:
  - ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Example rows:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. events.txt
- Filename: data/events.txt
- Content: Virtual museum events
- Fields:
  - event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Example rows:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. event_registrations.txt
- Filename: data/event_registrations.txt
- Content: Event registration records
- Fields:
  - registration_id|event_id|username|registration_date
- Example rows:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. collection_logs.txt
- Filename: data/collection_logs.txt
- Content: Logs of artifact collection activities
- Fields:
  - log_id|artifact_id|activity_type|date|notes|condition|curator
- Example rows:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

This design specification is comprehensive and enables clear parallel development of backend and frontend components based on defined routes, data schemas, and UI elements.

