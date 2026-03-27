# VirtualMuseum Design Specification

---

## 1. Flask Routes Specification

| Route Path                     | Function Name           | HTTP Method | Template Filename        | Context Variables (Name: Type)                                            |
|-------------------------------|------------------------|-------------|--------------------------|---------------------------------------------------------------------------|
| `/`                           | root                   | GET         | Redirects to `/dashboard`| None (Redirect)                                                            |
| `/dashboard`                  | dashboard_page         | GET         | `dashboard.html`          | `total_exhibitions: int`, `active_exhibitions: int`                       |
| `/artifact-catalog`           | artifact_catalog_page  | GET         | `artifact_catalog.html`   | `artifacts: list[dict]`, `search_query: str`, `filters: dict`             |
| `/artifact-catalog/filter`    | apply_artifact_filter  | POST        | `artifact_catalog.html`   | `artifacts: list[dict]`, `search_query: str`, `filters: dict`             |
| `/exhibitions`                | exhibitions_page       | GET         | `exhibitions.html`        | `exhibitions: list[dict]`, `filter_type: str`                            |
| `/exhibitions/filter`         | apply_exhibition_filter| POST        | `exhibitions.html`        | `exhibitions: list[dict]`, `filter_type: str`                            |
| `/exhibition/<int:exhibition_id>` | exhibition_details_page| GET         | `exhibition_details.html` | `exhibition: dict`, `artifacts: list[dict]`                             |
| `/visitor-tickets`            | visitor_tickets_page   | GET         | `visitor_tickets.html`    | `tickets: list[dict]`, `username: str`                                  |
| `/visitor-tickets/purchase`   | purchase_ticket        | POST        | `visitor_tickets.html`    | `tickets: list[dict]`, `purchase_success: bool`, `purchase_error: str or None`|
| `/virtual-events`             | virtual_events_page    | GET         | `virtual_events.html`     | `events: list[dict]`, `registrations: list[dict]`, `username: str`       |
| `/virtual-events/register/<int:event_id>` | register_event     | POST        | Redirects to `/virtual-events`| None (Redirect)                                                        |
| `/virtual-events/cancel/<int:registration_id>`| cancel_registration| POST        | Redirects to `/virtual-events`| None (Redirect)                                                        |
| `/audio-guides`               | audio_guides_page      | GET         | `audio_guides.html`       | `audioguides: list[dict]`, `filter_language: str`                       |
| `/audio-guides/filter`        | apply_language_filter  | POST        | `audio_guides.html`       | `audioguides: list[dict]`, `filter_language: str`                       |

**Notes:**
- Root route `/` redirects to `/dashboard` with HTTP status 302.
- GET methods are used for rendering pages; POST methods are used for form submissions and filters.
- Dynamic route parameters defined for exhibition details and event registrations.


---

## 2. HTML Templates Specification

### 2.1 Dashboard Page - `dashboard.html`
- **Page Title:** Museum Dashboard
- **Main Heading (`<h1>`):** Museum Dashboard
- **Element IDs:**
  - `dashboard-page` (Div container)
  - `exhibition-summary` (Div showing total and active exhibitions)
  - `artifact-catalog-button` (Button) - navigates to `artifact_catalog_page`
  - `exhibitions-button` (Button) - navigates to `exhibitions_page`
  - `visitor-tickets-button` (Button) - navigates to `visitor_tickets_page`
  - `virtual-events-button` (Button) - navigates to `virtual_events_page`
  - `audio-guides-button` (Button) - navigates to `audio_guides_page`

- **Navigation Buttons Mapping:**
  | Element ID               | Flask Route Function          |
  |--------------------------|-------------------------------|
  | `artifact-catalog-button`| `artifact_catalog_page`        |
  | `exhibitions-button`     | `exhibitions_page`             |
  | `visitor-tickets-button` | `visitor_tickets_page`         |
  | `virtual-events-button`  | `virtual_events_page`          |
  | `audio-guides-button`    | `audio_guides_page`            |

- **Context Variables:**
  - `total_exhibitions` (int): Total number of exhibitions
  - `active_exhibitions` (int): Count of currently active exhibitions


### 2.2 Artifact Catalog Page - `artifact_catalog.html`
- **Page Title:** Artifact Catalog
- **Main Heading (`<h1>`):** Artifact Catalog
- **Element IDs:**
  - `artifact-catalog-page` (Div container)
  - `artifact-table` (Table displaying artifacts list)
  - `search-artifact` (Input text, search field)
  - `apply-artifact-filter` (Button, to apply search/filter)
  - `back-to-dashboard` (Button, navigation)

- **Navigation Buttons Mapping:**
  | Element ID          | Flask Route Function     |
  |---------------------|--------------------------|
  | `back-to-dashboard`  | `dashboard_page`          |

- **Context Variables:**
  - `artifacts` (list of dict): Each dict includes keys: `artifact_id` (int), `artifact_name` (str), `period` (str), `origin` (str), `exhibition` (str or None)
  - `search_query` (str): Current search text input
  - `filters` (dict): Any applied filters, e.g. search terms


### 2.3 Exhibitions Page - `exhibitions.html`
- **Page Title:** Exhibitions
- **Main Heading (`<h1>`):** Exhibitions
- **Element IDs:**
  - `exhibitions-page` (Div container)
  - `exhibition-list` (Table listing exhibitions)
  - `filter-exhibition-type` (Dropdown for exhibition type filter)
  - `apply-exhibition-filter` (Button to apply filter)
  - Dynamic: `view-exhibition-button-{{ exhibition.exhibition_id }}` (Button to view details)
  - `back-to-dashboard` (Button navigation)

- **Navigation Buttons Mapping:**
  | Element ID Pattern                      | Flask Route Function         |
  |----------------------------------------|-----------------------------|
  | `view-exhibition-button-{{ exhibition_id }}` | `exhibition_details_page` (dynamic, exhibition_id parameter) |
  | `back-to-dashboard`                     | `dashboard_page`              |

- **Context Variables:**
  - `exhibitions` (list of dict): Each dict with keys: `exhibition_id` (int), `title` (str), `exhibition_type` (str), `start_date` (str), `end_date` (str), `gallery` (str), `status` (str)
  - `filter_type` (str): Current selected exhibition type filter


### 2.4 Exhibition Details Page - `exhibition_details.html`
- **Page Title:** Exhibition Details
- **Main Heading (`<h1>`):**
  - Element ID: `exhibition-title` contains the exhibition title
- **Element IDs:**
  - `exhibition-details-page` (Div container)
  - `exhibition-title` (H1 element, title)
  - `exhibition-description` (Div with description)
  - `exhibition-dates` (Div with start and end dates)
  - `exhibition-artifacts` (Table listing artifacts for this exhibition)
  - `back-to-exhibitions` (Button navigation)

- **Navigation Buttons Mapping:**
  | Element ID          | Flask Route Function     |
  |---------------------|--------------------------|
  | `back-to-exhibitions`| `exhibitions_page`        |

- **Context Variables:**
  - `exhibition` (dict): Keys - `exhibition_id` (int), `title` (str), `description` (str), `gallery_id` (int), `exhibition_type` (str), `start_date` (str), `end_date` (str), `curator_name` (str), `created_by` (str)
  - `artifacts` (list of dict): List of artifact dicts belonging to this exhibition


### 2.5 Visitor Tickets Page - `visitor_tickets.html`
- **Page Title:** Visitor Tickets
- **Main Heading (`<h1>`):** Visitor Tickets
- **Element IDs:**
  - `visitor-tickets-page` (Div container)
  - `ticket-type` (Dropdown selection for ticket type)
  - `number-of-tickets` (Input number field)
  - `purchase-ticket-button` (Button to purchase tickets)
  - `my-tickets-table` (Table showing user's purchased tickets)
  - `back-to-dashboard` (Button navigation)

- **Navigation Buttons Mapping:**
  | Element ID           | Flask Route Function       |
  |----------------------|----------------------------|
  | `back-to-dashboard`   | `dashboard_page`            |

- **Context Variables:**
  - `tickets` (list of dict): Each dict includes ticket details: `ticket_id` (int), `ticket_type` (str), `visit_date` (str), `visit_time` (str), `number_of_tickets` (int), `price` (float), `visitor_name` (str), `visitor_email` (str), `purchase_date` (str)
  - `username` (str): Current logged-in user
  - `purchase_success` (bool, optional): Flag indicating success of purchase
  - `purchase_error` (str or None, optional): Error message if purchase failed


### 2.6 Virtual Events Page - `virtual_events.html`
- **Page Title:** Virtual Events
- **Main Heading (`<h1>`):** Virtual Events
- **Element IDs:**
  - `virtual-events-page` (Div container)
  - `event-list` (Table of virtual events)
  - Dynamic: `register-event-button-{{ event.event_id }}` (Button to register for event)
  - Dynamic: `cancel-registration-button-{{ registration.registration_id }}` (Button to cancel registration)
  - `back-to-dashboard` (Button navigation)

- **Navigation Buttons Mapping:**
  | Element ID Pattern                   | Flask Route Function               |
  |------------------------------------|----------------------------------|
  | `register-event-button-{{ event_id }}` | `register_event` (POST, event_id parameter)            |
  | `cancel-registration-button-{{ registration_id }}` | `cancel_registration` (POST, registration_id parameter) |
  | `back-to-dashboard`                 | `dashboard_page`                  |

- **Context Variables:**
  - `events` (list of dict): Events with keys `event_id` (int), `title` (str), `date` (str), `time` (str), `event_type` (str), `speaker` (str), `capacity` (int), `description` (str), `created_by` (str)
  - `registrations` (list of dict): Registrations with keys `registration_id` (int), `event_id` (int), `username` (str), `registration_date` (str)
  - `username` (str): Current user logged in


### 2.7 Audio Guides Page - `audio_guides.html`
- **Page Title:** Audio Guides
- **Main Heading (`<h1>`):** Audio Guides
- **Element IDs:**
  - `audio-guides-page` (Div container)
  - `audio-guide-list` (Table listing audio guides)
  - `filter-language` (Dropdown to filter by language)
  - `apply-language-filter` (Button to apply language filter)
  - Dynamic: `play-guide-button-{{ guide.guide_id }}` (Button to play audio)
  - `back-to-dashboard` (Button navigation)

- **Navigation Buttons Mapping:**
  | Element ID           | Flask Route Function       |
  |----------------------|----------------------------|
  | `back-to-dashboard`   | `dashboard_page`            |

- **Context Variables:**
  - `audioguides` (list of dict): Keys - `guide_id` (int), `exhibit_number` (int), `title` (str), `language` (str), `duration` (int), `script` (str), `narrator` (str), `created_by` (str)
  - `filter_language` (str): Currently selected language filter


---

## 3. Data File Schemas

### 3.1 User Authentication Data - `data/users.txt`
| Field Names: `username` |

- **Content & Purpose:** Contains usernames of users accessing the application.

- **Example Rows:**
```
curator_john
visitor_mary
curator_sarah
```


### 3.2 Gallery Data - `data/galleries.txt`
| Field Names: `gallery_id|gallery_name|floor|capacity|theme|status` |

- **Content & Purpose:** Details of galleries with identification, location and status.

- **Example Rows:**
```
1|Ancient Civilizations Hall|1|50|Ancient|Open
2|Modern Art Wing|2|30|Modern|Open
3|Science Discovery Center|3|40|Science|Renovation
```


### 3.3 Exhibition Data - `data/exhibitions.txt`
| Field Names: `exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by` |

- **Content & Purpose:** Stores exhibitions' details including type, dates, and curators.

- **Example Rows:**
```
1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
```


### 3.4 Artifact Data - `data/artifacts.txt`
| Field Names: `artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by` |

- **Content & Purpose:** Data of artifacts including identification, exhibition relation, and acquisition.

- **Example Rows:**
```
1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
```


### 3.5 Audio Guide Data - `data/audioguides.txt`
| Field Names: `guide_id|exhibit_number|title|language|duration|script|narrator|created_by` |

- **Content & Purpose:** Audio guides metadata and narrative scripts.

- **Example Rows:**
```
1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
```


### 3.6 Ticket Data - `data/tickets.txt`
| Field Names: `ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date` |

- **Content & Purpose:** Records of ticket purchases along with visitor details.

- **Example Rows:**
```
1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
```


### 3.7 Virtual Event Data - `data/events.txt`
| Field Names: `event_id|title|date|time|event_type|speaker|capacity|description|created_by` |

- **Content & Purpose:** Details of virtual museum events such as webinars and artist talks.

- **Example Rows:**
```
1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
```


### 3.8 Event Registration Data - `data/event_registrations.txt`
| Field Names: `registration_id|event_id|username|registration_date` |

- **Content & Purpose:** Tracks user registrations to virtual events.

- **Example Rows:**
```
1|1|visitor_mary|2024-11-20
2|2|visitor_mary|2024-11-21
3|1|visitor_tom|2024-11-19
```


### 3.9 Collection Log Data - `data/collection_logs.txt`
| Field Names: `log_id|artifact_id|activity_type|date|notes|condition|curator` |

- **Content & Purpose:** Logs of artifact condition and curator activities.

- **Example Rows:**
```
1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
```

---

*End of design_spec.md*