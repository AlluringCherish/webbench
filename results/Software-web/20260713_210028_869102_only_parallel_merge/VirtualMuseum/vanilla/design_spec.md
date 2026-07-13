# Unified Design Specification for VirtualMuseum Web Application

---

## 1. Routes and Navigation

| Route Path              | Page Name            | Navigation From             | Navigation To                                                                                                 |
|-------------------------|----------------------|----------------------------|--------------------------------------------------------------------------------------------------------------|
| `/`                     | Dashboard            | Entry point (root route)    | Artifact Catalog, Exhibitions, Visitor Tickets, Virtual Events, Audio Guides                                |
| `/artifacts`            | Artifact Catalog     | Dashboard (`/`)             | Dashboard (`/`)                                                                                              |
| `/exhibitions`          | Exhibitions          | Dashboard (`/`)             | Exhibition Details (`/exhibitions/{exhibition_id}`), Dashboard (`/`)                                        |
| `/exhibitions/{exhibition_id}` | Exhibition Details   | Exhibitions (`/exhibitions`) | Exhibitions (`/exhibitions`)                                                                |
| `/visitor-tickets`      | Visitor Tickets      | Dashboard (`/`)             | Dashboard (`/`)                                                                                              |
| `/virtual-events`       | Virtual Events       | Dashboard (`/`)             | Dashboard (`/`)                                                                                              |
| `/audio-guides`         | Audio Guides         | Dashboard (`/`)             | Dashboard (`/`)                                                                                              |

---

## 2. Page Details

### 2.1 Dashboard Page
- Route: `/`
- Page Title: "Museum Dashboard"
- Container ID: `dashboard-page`
- Elements:
  - `exhibition-summary` (Div): Shows total exhibitions and count of active exhibitions.
  - `artifact-summary` (Div): Shows total artifact count.
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
  - `search-artifact` (Input): Search field for artifact name or ID.
  - `filter-period` (Dropdown): Filter artifacts by period (e.g., Ancient, Contemporary).
  - `filter-origin` (Dropdown): Filter artifacts by origin country/region.
  - `apply-artifact-filter` (Button): Applies the search and selected filters.
  - `artifact-table` (Table): Columns: `Artifact ID`, `Name`, `Period`, `Origin`, `Exhibition Title`, `Actions`.
    - Actions include `view-artifact-button-{artifact_id}` (Button) to view detailed artifact info.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.3 Exhibitions Page
- Route: `/exhibitions`
- Page Title: "Exhibitions"
- Container ID: `exhibitions-page`
- Elements:
  - `filter-exhibition-type` (Dropdown): Filter exhibitions by type: Permanent, Temporary, Virtual.
  - `filter-gallery` (Dropdown): Filter exhibitions by gallery location.
  - `apply-exhibition-filter` (Button): Applies the selected filters.
  - `exhibition-list` (Table): Columns: `ID`, `Title`, `Type`, `Start Date`, `End Date`, `Gallery Name`, `Status`, `Actions`.
    - Actions include `view-exhibition-button-{exhibition_id}` (Button) for navigation to details.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.4 Exhibition Details Page
- Route: `/exhibitions/{exhibition_id}`
- Page Title: "Exhibition Details"
- Container ID: `exhibition-details-page`
- Elements:
  - `exhibition-title` (H1): Title of the exhibition.
  - `exhibition-description` (Div): Description text.
  - `exhibition-dates` (Div): Displays start and end dates in human-readable format.
  - `exhibition-gallery` (Div): Shows gallery name.
  - `exhibition-artifacts` (Table): Columns: `Artifact ID`, `Name`, `Period`, `Origin`, `Storage Location`, `Acquisition Date`.
  - `back-to-exhibitions` (Button): Navigates back to `/exhibitions`.

### 2.5 Visitor Tickets Page
- Route: `/visitor-tickets`
- Page Title: "Visitor Tickets"
- Container ID: `visitor-tickets-page`
- Elements:
  - `ticket-type` (Dropdown): Options: Standard, Student, Senior, Family, VIP.
  - `visit-date` (Date input): Date for ticket visit.
  - `visit-time` (Time input): Preferred visit time.
  - `number-of-tickets` (Input type=number): Number of tickets to purchase.
  - `visitor-name` (Input): Name of visitor.
  - `visitor-email` (Input): Visitor's email address.
  - `purchase-ticket-button` (Button): To purchase tickets.
  - `my-tickets-table` (Table): Displays tickets purchased by the user.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.6 Virtual Events Page
- Route: `/virtual-events`
- Page Title: "Virtual Events"
- Container ID: `virtual-events-page`
- Elements:
  - `filter-event-type` (Dropdown): Filter events by type: Webinar, Artist Talk, Virtual Tour.
  - `apply-event-filter` (Button): Applies selected filters.
  - `event-list` (Table): Columns: `Event ID`, `Title`, `Date`, `Time`, `Type`, `Speaker`, `Capacity`, `Description`, `Actions`.
    - Actions column:
      - `register-event-button-{event_id}` (Button) if user not registered.
      - `cancel-registration-button-{registration_id}` (Button) if user registered.
  - `back-to-dashboard` (Button): Navigates back to `/`.

### 2.7 Audio Guides Page
- Route: `/audio-guides`
- Page Title: "Audio Guides"
- Container ID: `audio-guides-page`
- Elements:
  - `filter-language` (Dropdown): Filter guides by language (English, Spanish, French).
  - `apply-language-filter` (Button): Applies language filter.
  - `audio-guide-list` (Table): Columns: `Guide ID`, `Exhibit Number`, `Title`, `Language`, `Duration (min)`, `Narrator`, `Actions`.
    - Actions include `play-guide-button-{guide_id}` (Button) to play audio.
  - `back-to-dashboard` (Button): Navigates back to `/`.

---

## 3. Data Storage

All data files are stored within the `data/` directory. All files use pipe (`|`) as delimiter.

### 3.1 Users
- File: `data/users.txt`
- Format: Plain text line-separated usernames.
- Example:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 3.2 Galleries
- File: `data/galleries.txt`
- Format:
  ```
  gallery_id|gallery_name|floor|capacity|theme|status
  ```
- Example:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3.3 Exhibitions
- File: `data/exhibitions.txt`
- Format:
  ```
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
  ```
- Example:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 3.4 Artifacts
- File: `data/artifacts.txt`
- Format:
  ```
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
  ```
- Example:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 3.5 Audio Guides
- File: `data/audioguides.txt`
- Format:
  ```
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
  ```
- Example:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 3.6 Tickets
- File: `data/tickets.txt`
- Format:
  ```
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
  ```
- Example:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 3.7 Virtual Events
- File: `data/events.txt`
- Format:
  ```
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
  ```
- Example:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 3.8 Event Registrations
- File: `data/event_registrations.txt`
- Format:
  ```
  registration_id|event_id|username|registration_date
  ```
- Example:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 3.9 Collection Logs
- File: `data/collection_logs.txt`
- Format:
  ```
  log_id|artifact_id|activity_type|date|notes|condition|curator
  ```
- Example:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

---

## 4. Navigation Flow Summary

- Starting at `/` (Dashboard), users can navigate via buttons to all other main pages.
- All list/detail pages provide appropriate back buttons returning to the correct previous page.
- Dynamic buttons have IDs with entity IDs for unique identification (e.g., `view-exhibition-button-2`).
- Filtering and search fields exist on artifact catalog, exhibitions, virtual events, and audio guides pages.

---

This unified design specification integrates all user requirements and merges the best elements from both design candidates, providing a consistent, clear, and complete blueprint for VirtualMuseum web application implementation.
