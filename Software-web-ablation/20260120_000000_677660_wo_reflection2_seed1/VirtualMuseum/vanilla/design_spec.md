# VirtualMuseum Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                    | Function Name               | HTTP Method | Template Filename         | Context Variables                                                     |
|-------------------------------|-----------------------------|-------------|---------------------------|---------------------------------------------------------------------|
| /                             | root_redirect               | GET         | None (Redirect)            | None                                                                |
| /dashboard                   | dashboard                  | GET         | dashboard.html            | exhibitions_summary (dict: {"total": int, "active": int}), 
                                                             artifacts_summary (dict: {"total": int}),
                                                             user (str, optional, e.g. current logged user or None)               |
| /artifacts                   | artifact_catalog           | GET, POST   | artifact_catalog.html      | artifacts (list of dict), 
                                                             filters (dict: search_term=str or empty), 
                                                             user (str, optional)                                               |
| /exhibitions                 | exhibitions                | GET, POST   | exhibitions.html           | exhibitions (list of dict), 
                                                             selected_type_filter (str),
                                                             user (str, optional)                                               |
| /exhibition/<int:exhibition_id> | exhibition_details          | GET         | exhibition_details.html    | exhibition (dict), 
                                                             artifacts (list of dict),
                                                             user (str, optional)                                               |
| /tickets                    | visitor_tickets            | GET, POST   | visitor_tickets.html       | tickets (list of dict for current user), 
                                                             ticket_types (list of str), 
                                                             user (str)                                                        |
| /events                     | virtual_events             | GET, POST   | virtual_events.html        | events (list of dict), 
                                                             registrations (list of dict for current user),
                                                             user (str)                                                        |
| /audio-guides               | audio_guides               | GET, POST   | audio_guides.html          | audio_guides (list of dict), 
                                                             selected_language (str),
                                                             user (str)                                                        |

---

## Section 2: HTML Templates Specification

### dashboard.html
- Filename: dashboard.html
- Page Title: Museum Dashboard
- Main Header: <h1>Museum Dashboard</h1>
- Element IDs:
  - dashboard-page (div container)
  - exhibition-summary (div container showing total and active exhibitions)
  - artifact-catalog-button (button)
  - exhibitions-button (button)
  - visitor-tickets-button (button)
  - virtual-events-button (button)
  - audio-guides-button (button)
- Navigation Buttons to Flask Routes:
  - artifact-catalog-button => url_for('artifact_catalog')
  - exhibitions-button => url_for('exhibitions')
  - visitor-tickets-button => url_for('visitor_tickets')
  - virtual-events-button => url_for('virtual_events')
  - audio-guides-button => url_for('audio_guides')
- Context Variables:
  - exhibitions_summary (dict): contains keys 'total' (int), 'active' (int)
  - artifacts_summary (dict): contains key 'total' (int)

### artifact_catalog.html
- Filename: artifact_catalog.html
- Page Title: Artifact Catalog
- Main Header: <h1>Artifact Catalog</h1>
- Element IDs:
  - artifact-catalog-page (div container)
  - artifact-table (table displaying artifact details)
  - search-artifact (input text for search)
  - apply-artifact-filter (button)
  - back-to-dashboard (button)
- Navigation Buttons:
  - apply-artifact-filter => triggers form POST or AJAX
  - back-to-dashboard => url_for('dashboard')
- Context Variables:
  - artifacts (list of dicts): each dict includes artifact_id (int), artifact_name (str), period (str), origin (str), exhibition (str or exhibition_id), and other fields for display
  - filters (dict) with 'search_term' key (str)

### exhibitions.html
- Filename: exhibitions.html
- Page Title: Exhibitions
- Main Header: <h1>Exhibitions</h1>
- Element IDs:
  - exhibitions-page (div container)
  - exhibition-list (table listing exhibitions with relevant info)
  - filter-exhibition-type (dropdown selecting Permanent, Temporary, Virtual)
  - apply-exhibition-filter (button)
  - view-exhibition-button-{exhibition_id} (button for each exhibition row)
  - back-to-dashboard (button)
- Navigation Buttons:
  - apply-exhibition-filter => triggers form POST or filter logic
  - view-exhibition-button-{exhibition_id} => url_for('exhibition_details', exhibition_id={{exhibition_id}})
  - back-to-dashboard => url_for('dashboard')
- Context Variables:
  - exhibitions (list of dicts): fields include exhibition_id (int), title (str), exhibition_type (str), start_date, end_date, gallery_name, status
  - selected_type_filter (str)

### exhibition_details.html
- Filename: exhibition_details.html
- Page Title: Exhibition Details
- Main Header: <h1 id="exhibition-title">{{ exhibition.title }}</h1>
- Element IDs:
  - exhibition-details-page (div container)
  - exhibition-title (h1 element)
  - exhibition-description (div)
  - exhibition-dates (div)
  - exhibition-artifacts (table listing artifacts in exhibition)
  - back-to-exhibitions (button)
- Navigation Buttons:
  - back-to-exhibitions => url_for('exhibitions')
- Context Variables:
  - exhibition (dict): keys include title (str), description (str), start_date (str), end_date (str)
  - artifacts (list of dicts) with artifact details

### visitor_tickets.html
- Filename: visitor_tickets.html
- Page Title: Visitor Tickets
- Main Header: <h1>Visitor Tickets</h1>
- Element IDs:
  - visitor-tickets-page (div container)
  - ticket-type (dropdown: Standard, Student, Senior, Family, VIP)
  - number-of-tickets (input number)
  - purchase-ticket-button (button)
  - my-tickets-table (table showing user's tickets)
  - back-to-dashboard (button)
- Navigation Buttons:
  - purchase-ticket-button => POST form action
  - back-to-dashboard => url_for('dashboard')
- Context Variables:
  - tickets (list of dicts): each dict includes ticket details for current user
  - ticket_types (list of str)

### virtual_events.html
- Filename: virtual_events.html
- Page Title: Virtual Events
- Main Header: <h1>Virtual Events</h1>
- Element IDs:
  - virtual-events-page (div container)
  - event-list (table of events)
  - register-event-button-{event_id} (button per event)
  - cancel-registration-button-{registration_id} (button per registration)
  - back-to-dashboard (button)
- Navigation Buttons:
  - register-event-button-{event_id} => POST /event registration or equivalent
  - cancel-registration-button-{registration_id} => POST /cancel registration or equivalent
  - back-to-dashboard => url_for('dashboard')
- Context Variables:
  - events (list of dicts): event details
  - registrations (list of dicts): current user's event registrations

### audio_guides.html
- Filename: audio_guides.html
- Page Title: Audio Guides
- Main Header: <h1>Audio Guides</h1>
- Element IDs:
  - audio-guides-page (div container)
  - audio-guide-list (table listing guides)
  - filter-language (dropdown: English, Spanish, French)
  - apply-language-filter (button)
  - play-guide-button-{guide_id} (button per guide)
  - back-to-dashboard (button)
- Navigation Buttons:
  - apply-language-filter => POST form or filter
  - play-guide-button-{guide_id} => Play audio guide action
  - back-to-dashboard => url_for('dashboard')
- Context Variables:
  - audio_guides (list of dicts), each with guide_id, exhibit_number, title, language, duration
  - selected_language (str)

---

## Section 3: Data File Schemas

### users.txt
- Filename: data/users.txt
- Content / Purpose: List of usernames authorized as users of the system.
- Pipe-delimited Fields:
  - username
- Example Rows:
  curator_john
  visitor_mary
  curator_sarah

### galleries.txt
- Filename: data/galleries.txt
- Content / Purpose: Details of galleries in the museum, their capacity and status.
- Pipe-delimited Fields:
  - gallery_id|gallery_name|floor|capacity|theme|status
- Example Rows:
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation

### exhibitions.txt
- Filename: data/exhibitions.txt
- Content / Purpose: Information on each exhibition, including type, curator and dates.
- Pipe-delimited Fields:
  - exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
- Example Rows:
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john

### artifacts.txt
- Filename: data/artifacts.txt
- Content / Purpose: Data on all artifacts including details and exhibition association.
- Pipe-delimited Fields:
  - artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
- Example Rows:
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john

### audioguides.txt
- Filename: data/audioguides.txt
- Content / Purpose: Information about audio guides including language and narration details.
- Pipe-delimited Fields:
  - guide_id|exhibit_number|title|language|duration|script|narrator|created_by
- Example Rows:
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah

### tickets.txt
- Filename: data/tickets.txt
- Content / Purpose: Records of purchased visitor tickets.
- Pipe-delimited Fields:
  - ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
- Example Rows:
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18

### events.txt
- Filename: data/events.txt
- Content / Purpose: Details of virtual events including speaker and capacity.
- Pipe-delimited Fields:
  - event_id|title|date|time|event_type|speaker|capacity|description|created_by
- Example Rows:
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john

### event_registrations.txt
- Filename: data/event_registrations.txt
- Content / Purpose: User registrations for virtual events.
- Pipe-delimited Fields:
  - registration_id|event_id|username|registration_date
- Example Rows:
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19

### collection_logs.txt
- Filename: data/collection_logs.txt
- Content / Purpose: Logs for artifact collection activities and condition tracking.
- Pipe-delimited Fields:
  - log_id|artifact_id|activity_type|date|notes|condition|curator
- Example Rows:
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john

---

This completes the comprehensive design specification for the VirtualMuseum application, enabling parallel and independent frontend/backend development and accurate data handling.

