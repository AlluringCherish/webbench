# VirtualMuseum Design Specification

---

## Section 1: Flask Routes Specification

### Route: /
- Function Name: root_redirect
- HTTP Methods: GET
- Template: None (redirect to /dashboard)
- Context Variables: None
- Description: Redirect root URL to dashboard page.

---

### Route: /dashboard
- Function Name: dashboard
- HTTP Methods: GET
- Template: dashboard.html
- Context Variables:
  - exhibitions_summary (dict): Summary data including total_exhibitions (int), active_exhibitions (int)

---

### Route: /artifact-catalog
- Function Name: artifact_catalog
- HTTP Methods: GET, POST
- Template: artifact_catalog.html
- Context Variables:
  - artifacts (list of dict): List of artifact records matching data schema
  - search_query (str): Current search input for artifact name or ID
  - filters (dict): Additional filters if implemented (can be empty)

---

### Route: /exhibitions
- Function Name: exhibitions
- HTTP Methods: GET, POST
- Template: exhibitions.html
- Context Variables:
  - exhibitions (list of dict): List of exhibition records matching data schema
  - filter_type (str): Current exhibition type filter value ("Permanent", "Temporary", "Virtual", or empty string)

---

### Route: /exhibition/<int:exhibition_id>
- Function Name: exhibition_details
- HTTP Methods: GET
- Template: exhibition_details.html
- Context Variables:
  - exhibition (dict): Exhibition record for given exhibition_id
  - artifacts (list of dict): Artifacts belonging to this exhibition

---

### Route: /visitor-tickets
- Function Name: visitor_tickets
- HTTP Methods: GET, POST
- Template: visitor_tickets.html
- Context Variables:
  - ticket_types (list of str): ["Standard", "Student", "Senior", "Family", "VIP"]
  - my_tickets (list of dict): Tickets purchased by current user

---

### Route: /virtual-events
- Function Name: virtual_events
- HTTP Methods: GET, POST
- Template: virtual_events.html
- Context Variables:
  - events (list of dict): Virtual event records from events.txt
  - registrations (list of dict): Registrations of the current user from event_registrations.txt

---

### Route: /audio-guides
- Function Name: audio_guides
- HTTP Methods: GET, POST
- Template: audio_guides.html
- Context Variables:
  - audio_guides (list of dict): List of audio guide records
  - filter_language (str): Language filter value ("English", "Spanish", "French", or empty string)

---

### Route: /virtual-events/register/<int:event_id>
- Function Name: register_event
- HTTP Methods: POST
- Template: None (redirect to /virtual-events)
- Context Variables: None

---

### Route: /virtual-events/cancel/<int:registration_id>
- Function Name: cancel_registration
- HTTP Methods: POST
- Template: None (redirect to /virtual-events)
- Context Variables: None

---

### Route: /purchase-ticket
- Function Name: purchase_ticket
- HTTP Methods: POST
- Template: None (redirect to /visitor-tickets)
- Context Variables: None

---

### Navigation Buttons to Flask Route Mappings:
| Button ID                     | Flask Route Function       | URL Route                         |
| ----------------------------- | -------------------------- | -------------------------------- |
| artifact-catalog-button        | artifact_catalog           | /artifact-catalog                 |
| exhibitions-button             | exhibitions                | /exhibitions                     |
| visitor-tickets-button         | visitor_tickets            | /visitor-tickets                 |
| virtual-events-button          | virtual_events             | /virtual-events                  |
| audio-guides-button            | audio_guides               | /audio-guides                   |
| back-to-dashboard              | dashboard                  | /dashboard                      |
| back-to-exhibitions            | exhibitions                | /exhibitions                    |
| apply-artifact-filter          | artifact_catalog (POST/GET)| /artifact-catalog               |
| apply-exhibition-filter        | exhibitions (POST/GET)     | /exhibitions                   |
| view-exhibition-button-{id}   | exhibition_details         | /exhibition/<exhibition_id>    |
| register-event-button-{id}    | register_event (POST)      | /virtual-events/register/<event_id> |
| cancel-registration-button-{id}| cancel_registration (POST)| /virtual-events/cancel/<registration_id> |
| purchase-ticket-button         | purchase_ticket (POST)     | /purchase-ticket               |


---

## Section 2: HTML Templates Specification

### Template: dashboard.html
- File path: templates/dashboard.html
- Page title: "Museum Dashboard"
- <title> and main <h1>: "Museum Dashboard"
- Element IDs:
  - dashboard-page (Div container)
  - exhibition-summary (Div showing total and active exhibitions)
  - artifact-catalog-button (Button to /artifact-catalog)
  - exhibitions-button (Button to /exhibitions)
  - visitor-tickets-button (Button to /visitor-tickets)
  - virtual-events-button (Button to /virtual-events)
  - audio-guides-button (Button to /audio-guides)
- Navigation buttons mapped to Flask routes:
  - artifact-catalog-button => url_for('artifact_catalog')
  - exhibitions-button => url_for('exhibitions')
  - visitor-tickets-button => url_for('visitor_tickets')
  - virtual-events-button => url_for('virtual_events')
  - audio-guides-button => url_for('audio_guides')
- Context variables:
  - exhibitions_summary (dict): Contains total_exhibitions (int), active_exhibitions (int)

---

### Template: artifact_catalog.html
- File path: templates/artifact_catalog.html
- Page title: "Artifact Catalog"
- <title> and main <h1>: "Artifact Catalog"
- Element IDs:
  - artifact-catalog-page (Div container)
  - artifact-table (Table displaying artifacts)
  - search-artifact (Input for searching by name or ID)
  - apply-artifact-filter (Button to apply filters/search)
  - back-to-dashboard (Button to navigate back to Dashboard)
- Navigation buttons mapped:
  - back-to-dashboard => url_for('dashboard')
- Context variables:
  - artifacts (list of dict): Artifact records
  - search_query (str): Current search input
  - filters (dict): Any active filters

---

### Template: exhibitions.html
- File path: templates/exhibitions.html
- Page title: "Exhibitions"
- <title> and main <h1>: "Exhibitions"
- Element IDs:
  - exhibitions-page (Div container)
  - exhibition-list (Table with exhibitions)
  - filter-exhibition-type (Dropdown for type filter)
  - apply-exhibition-filter (Button to filter exhibitions)
  - back-to-dashboard (Button to go back)
  - view-exhibition-button-{{ exhibition.exhibition_id }} (Buttons for each exhibition row)
- Navigation buttons mapped:
  - back-to-dashboard => url_for('dashboard')
  - view-exhibition-button-{{ exhibition.exhibition_id }} => url_for('exhibition_details', exhibition_id=exhibition.exhibition_id)
- Context variables:
  - exhibitions (list of dict): Exhibition records
  - filter_type (str): Current type filter

---

### Template: exhibition_details.html
- File path: templates/exhibition_details.html
- Page title: "Exhibition Details"
- <title> and main <h1>: "Exhibition Details"
- Element IDs:
  - exhibition-details-page (Div container)
  - exhibition-title (H1 title)
  - exhibition-description (Div description)
  - exhibition-dates (Div start and end dates)
  - exhibition-artifacts (Table of artifacts)
  - back-to-exhibitions (Button to exhibitions page)
- Navigation buttons mapped:
  - back-to-exhibitions => url_for('exhibitions')
- Context variables:
  - exhibition (dict): Detailed exhibition
  - artifacts (list of dict): Artifacts belonging to exhibition

---

### Template: visitor_tickets.html
- File path: templates/visitor_tickets.html
- Page title: "Visitor Tickets"
- <title> and main <h1>: "Visitor Tickets"
- Element IDs:
  - visitor-tickets-page (Div container)
  - ticket-type (Dropdown for ticket type selection)
  - number-of-tickets (Input number)
  - purchase-ticket-button (Button to purchase)
  - my-tickets-table (Table showing purchased tickets)
  - back-to-dashboard (Button back to dashboard)
- Navigation buttons mapped:
  - back-to-dashboard => url_for('dashboard')
- Context variables:
  - ticket_types (list of str): Available ticket types
  - my_tickets (list of dict): Tickets purchased by user

---

### Template: virtual_events.html
- File path: templates/virtual_events.html
- Page title: "Virtual Events"
- <title> and main <h1>: "Virtual Events"
- Element IDs:
  - virtual-events-page (Div container)
  - event-list (Table of events)
  - register-event-button-{{ event.event_id }} (Buttons for event registration)
  - cancel-registration-button-{{ registration.registration_id }} (Buttons to cancel registration)
  - back-to-dashboard (Button back to dashboard)
- Navigation buttons mapped:
  - back-to-dashboard => url_for('dashboard')
  - register-event-button-{{ event.event_id }} => POST /virtual-events/register/{{ event.event_id }}
  - cancel-registration-button-{{ registration.registration_id }} => POST /virtual-events/cancel/{{ registration.registration_id }}
- Context variables:
  - events (list of dict): Event records
  - registrations (list of dict): Current user's registrations

---

### Template: audio_guides.html
- File path: templates/audio_guides.html
- Page title: "Audio Guides"
- <title> and main <h1>: "Audio Guides"
- Element IDs:
  - audio-guides-page (Div container)
  - audio-guide-list (Table of audio guides)
  - filter-language (Dropdown to filter by language)
  - apply-language-filter (Button to apply language filter)
  - play-guide-button-{{ guide.guide_id }} (Buttons to play guide audio)
  - back-to-dashboard (Button back to dashboard)
- Navigation buttons mapped:
  - back-to-dashboard => url_for('dashboard')
- Context variables:
  - audio_guides (list of dict): Audio guide records
  - filter_language (str): Selected language filter

---

## Section 3: Data File Schemas

### users.txt
- Path: data/users.txt
- Fields (pipe-delimited): username
- Description: User authentication data; stores usernames.
- Example Rows:
  - curator_john
  - visitor_mary
  - curator_sarah

---

### galleries.txt
- Path: data/galleries.txt
- Fields: gallery_id|gallery_name|floor|capacity|theme|status
- Description: Contains gallery information including location and current status.
- Example Rows:
  - 1|Ancient Civilizations Hall|1|50|Ancient|Open
  - 2|Modern Art Wing|2|30|Modern|Open
  - 3|Science Discovery Center|3|40|Science|Renovation

---

### exhibitions.txt
- Path: data/exhibitions.txt
- Fields: exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Description: Records of museum exhibitions and their details.
- Example Rows:
  - 1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  - 2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  - 3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

---

### artifacts.txt
- Path: data/artifacts.txt
- Fields: artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Description: Artifact records including exhibition affiliations.
- Example Rows:
  - 1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  - 2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  - 3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

---

### audioguides.txt
- Path: data/audioguides.txt
- Fields: guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Description: Audio guide info by language and exhibit.
- Example Rows:
  - 1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  - 2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  - 3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

---

### tickets.txt
- Path: data/tickets.txt
- Fields: ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Description: Records of tickets purchased by visitors.
- Example Rows:
  - 1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  - 2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  - 3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

---

### events.txt
- Path: data/events.txt
- Fields: event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Description: Virtual event data with speakers and registration capacity.
- Example Rows:
  - 1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  - 2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  - 3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

---

### event_registrations.txt
- Path: data/event_registrations.txt
- Fields: registration_id|event_id|username|registration_date
- Description: Records of event registrations by users.
- Example Rows:
  - 1|1|visitor_mary|2024-11-20
  - 2|2|visitor_mary|2024-11-21
  - 3|1|visitor_tom|2024-11-19

---

### collection_logs.txt
- Path: data/collection_logs.txt
- Fields: log_id|artifact_id|activity_type|date|notes|condition|curator
- Description: Logs activities related to artifacts and conservation.
- Example Rows:
  - 1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  - 2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  - 3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  - 4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

# End of VirtualMuseum Design Specification
