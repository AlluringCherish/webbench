# Design Candidate for VirtualMuseum Web Application

## 1. Routes and Navigation

| Route Path              | Page Name            | Navigation From                          | Navigation To                                                                                  |
|-------------------------|----------------------|----------------------------------------|-----------------------------------------------------------------------------------------------|
| `/`                     | Dashboard            | Entry point (root route)                | Artifact Catalog, Exhibitions, Visitor Tickets, Virtual Events, Audio Guides                   |
| `/artifacts`            | Artifact Catalog     | Dashboard                              | Dashboard                                                                                      |
| `/exhibitions`          | Exhibitions          | Dashboard                              | Exhibition Details (dynamic), Dashboard                                                        |
| `/exhibitions/{id}`     | Exhibition Details   | Exhibitions                           | Exhibitions                                                                                   |
| `/visitor-tickets`      | Visitor Tickets      | Dashboard                              | Dashboard                                                                                      |
| `/virtual-events`       | Virtual Events       | Dashboard                              | Dashboard                                                                                      |
| `/audio-guides`         | Audio Guides         | Dashboard                              | Dashboard                                                                                      |

## 2. Page Details

### 2.1 Dashboard Page
- Route: `/`
- Page Title: "Museum Dashboard"
- Container ID: `dashboard-page`
- Elements:
  - `exhibition-summary` (Div): Summary showing total exhibitions and active exhibitions count.
  - `artifact-catalog-button` (Button): Navigates to `/artifacts`.
  - `exhibitions-button` (Button): Navigates to `/exhibitions`.
  - `visitor-tickets-button` (Button): Navigates to `/visitor-tickets`.
  - `virtual-events-button` (Button): Navigates to `/virtual-events`.
  - `audio-guides-button` (Button): Navigates to `/audio-guides`.

### 2.2 Artifact Catalog Page
- Route: `/artifacts`
- Page Title: "Artifact Catalog"
- Container ID: `artifact-catalog-page`
- Elements:
  - `artifact-table` (Table): Displays columns - ID, Name, Period, Origin, Exhibition, Actions (e.g. view details if needed).
  - `search-artifact` (Input): Search field for artifact name or ID.
  - `apply-artifact-filter` (Button): Applies search and filters.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.3 Exhibitions Page
- Route: `/exhibitions`
- Page Title: "Exhibitions"
- Container ID: `exhibitions-page`
- Elements:
  - `exhibition-list` (Table): Columns include title, type, dates, gallery, and status.
  - `filter-exhibition-type` (Dropdown): Values - Permanent, Temporary, Virtual.
  - `apply-exhibition-filter` (Button): Applies filter by exhibition type.
  - `view-exhibition-button-{exhibition_id}` (Buttons): One per exhibition row; navigates to `/exhibitions/{exhibition_id}`.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.4 Exhibition Details Page
- Route: `/exhibitions/{id}`
- Page Title: "Exhibition Details"
- Container ID: `exhibition-details-page`
- Elements:
  - `exhibition-title` (H1): Title of the exhibition.
  - `exhibition-description` (Div): Description text.
  - `exhibition-dates` (Div): Displays start and end dates.
  - `exhibition-artifacts` (Table): Lists artifacts in this exhibition with relevant details.
  - `back-to-exhibitions` (Button): Navigates back to `/exhibitions`.

### 2.5 Visitor Tickets Page
- Route: `/visitor-tickets`
- Page Title: "Visitor Tickets"
- Container ID: `visitor-tickets-page`
- Elements:
  - `ticket-type` (Dropdown): Options - Standard, Student, Senior, Family, VIP.
  - `number-of-tickets` (Input type=number): Number of tickets to purchase.
  - `purchase-ticket-button` (Button): To trigger ticket purchase.
  - `my-tickets-table` (Table): Displays user's purchased tickets.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.6 Virtual Events Page
- Route: `/virtual-events`
- Page Title: "Virtual Events"
- Container ID: `virtual-events-page`
- Elements:
  - `event-list` (Table): Columns - title, date, time, type, registration status.
  - `register-event-button-{event_id}` (Button): For each event, to register.
  - `cancel-registration-button-{registration_id}` (Button): For each registered event, to cancel registration.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.7 Audio Guides Page
- Route: `/audio-guides`
- Page Title: "Audio Guides"
- Container ID: `audio-guides-page`
- Elements:
  - `audio-guide-list` (Table): Columns - exhibit number, title, language, duration.
  - `filter-language` (Dropdown): Filter options - English, Spanish, French.
  - `apply-language-filter` (Button): Applies language filter.
  - `play-guide-button-{guide_id}` (Button): Plays audio guide.
  - `back-to-dashboard` (Button): Navigates back to `/`.

## 3. Data Storage

All data files are stored locally in the `data/` directory. All files use pipe (`|`) as delimiter.

### 3.1 Users
- File: `data/users.txt`
- Fields per line: `username`
- Notes: Stores authorized usernames.

### 3.2 Galleries
- File: `data/galleries.txt`
- Fields: `gallery_id|gallery_name|floor|capacity|theme|status`

### 3.3 Exhibitions
- File: `data/exhibitions.txt`
- Fields: `exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by`

### 3.4 Artifacts
- File: `data/artifacts.txt`
- Fields: `artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by`

### 3.5 Audio Guides
- File: `data/audioguides.txt`
- Fields: `guide_id|exhibit_number|title|language|duration|script|narrator|created_by`

### 3.6 Tickets
- File: `data/tickets.txt`
- Fields: `ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date`

### 3.7 Events
- File: `data/events.txt`
- Fields: `event_id|title|date|time|event_type|speaker|capacity|description|created_by`

### 3.8 Event Registrations
- File: `data/event_registrations.txt`
- Fields: `registration_id|event_id|username|registration_date`

### 3.9 Collection Logs
- File: `data/collection_logs.txt`
- Fields: `log_id|artifact_id|activity_type|date|notes|condition|curator`

## 4. Navigation Flow Summary

- Starting at `/` (Dashboard), users can navigate to any main function via buttons.
- From Exhibitions list, users can view exhibition details.
- Back buttons return to their respective previous main pages.
- Buttons with dynamic IDs are keyed with entity IDs for precise binding.

---

This design candidate includes all required page routes, UI element IDs, navigation logic, and data file structures for full implementation of the VirtualMuseum web application as specified.
