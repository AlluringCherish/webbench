# VirtualMuseum Frontend Design Specifications

---

## Section 1: Templates and Layout

### 1. Dashboard Page
- **Template Name:** `dashboard.html`
- **Page Title:** Museum Dashboard
- **Elements:**
  - `dashboard-page` (Div): Container for the entire dashboard page.
  - `exhibition-summary` (Div): Displays summary info such as total exhibitions and active exhibitions count.
  - `artifact-catalog-button` (Button): Navigates to the Artifact Catalog page.
  - `exhibitions-button` (Button): Navigates to the Exhibitions page.
  - `visitor-tickets-button` (Button): Navigates to the Visitor Tickets page.
  - `virtual-events-button` (Button): Navigates to the Virtual Events page.
  - `audio-guides-button` (Button): Navigates to the Audio Guides page.

---

### 2. Artifact Catalog Page
- **Template Name:** `artifact_catalog.html`
- **Page Title:** Artifact Catalog
- **Elements:**
  - `artifact-catalog-page` (Div): Container for the artifact catalog page.
  - `search-artifact` (Input, text): Search input for artifacts by name or ID.
  - `apply-artifact-filter` (Button): Button to apply search/filter.
  - `artifact-table` (Table): Displays artifact data with columns:
    - Artifact ID
    - Name
    - Period
    - Origin
    - Exhibition
    - Actions (e.g., Edit/View if applicable)
    - Table rows will be dynamically rendered using Jinja2 placeholder `artifacts`.
  - `back-to-dashboard` (Button): Navigates back to Dashboard page.

---

### 3. Exhibitions Page
- **Template Name:** `exhibitions.html`
- **Page Title:** Exhibitions
- **Elements:**
  - `exhibitions-page` (Div): Container for exhibitions page.
  - `filter-exhibition-type` (Dropdown/select): Options - Permanent, Temporary, Virtual.
  - `apply-exhibition-filter` (Button): Applies the selected filter.
  - `exhibition-list` (Table): Columns:
    - Title
    - Type
    - Start Date
    - End Date
    - Gallery
    - Status
    - Actions: Button with ID `view-exhibition-button-{exhibition_id}` to view details
    - Table rows rendered dynamically from `exhibitions` context variable.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

---

### 4. Exhibition Details Page
- **Template Name:** `exhibition_details.html`
- **Page Title:** Exhibition Details
- **Elements:**
  - `exhibition-details-page` (Div): Container for this page.
  - `exhibition-title` (H1): Title of the exhibition.
  - `exhibition-description` (Div): Detailed description.
  - `exhibition-dates` (Div): Shows start and end dates.
  - `exhibition-artifacts` (Table): Columns for artifacts related to this exhibition (e.g., ID, Name, Period, Origin).
  - `back-to-exhibitions` (Button): Navigates back to Exhibitions page.

---

### 5. Visitor Tickets Page
- **Template Name:** `visitor_tickets.html`
- **Page Title:** Visitor Tickets
- **Elements:**
  - `visitor-tickets-page` (Div): Container for ticket section.
  - `ticket-type` (Dropdown/select): Ticket types: Standard, Student, Senior, Family, VIP.
  - `number-of-tickets` (Input, number): Field for inputting number of tickets; must be positive integer.
  - `purchase-ticket-button` (Button): Action to purchase tickets.
  - `my-tickets-table` (Table): Displays tickets purchased by the user with columns like Ticket ID, Type, Date, Time, Quantity, Price.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

---

### 6. Virtual Events Page
- **Template Name:** `virtual_events.html`
- **Page Title:** Virtual Events
- **Elements:**
  - `virtual-events-page` (Div): Container.
  - `event-list` (Table): Columns - Title, Date, Time, Type, Registration Status, Actions.
    Actions include:
      - Button `register-event-button-{event_id}`: To register for event.
      - Button `cancel-registration-button-{registration_id}`: To cancel registration.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

---

### 7. Audio Guides Page
- **Template Name:** `audio_guides.html`
- **Page Title:** Audio Guides
- **Elements:**
  - `audio-guides-page` (Div): Container.
  - `filter-language` (Dropdown/select): Languages - English, Spanish, French.
  - `apply-language-filter` (Button): Apply selected language filter.
  - `audio-guide-list` (Table): Columns - Exhibit Number, Title, Language, Duration, Actions.
    - Each row includes a `play-guide-button-{guide_id}` button to play audio.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

---

## Section 2: Navigation and Interaction

- All navigation buttons with IDs `artifact-catalog-button`, `exhibitions-button`, `visitor-tickets-button`, `virtual-events-button`, and `audio-guides-button` on the Dashboard page link to their respective pages.

- On each page, the `back-to-dashboard` button returns the user to the Dashboard page.

- On Exhibitions page, the `view-exhibition-button-{exhibition_id}` buttons link to the Exhibition Details page for the corresponding exhibition.

- On Exhibition Details page, the `back-to-exhibitions` button navigates back to the Exhibitions page.

- On Visitor Tickets page, the `purchase-ticket-button` triggers frontend validation:
  - Ensure `number-of-tickets` input is a positive integer before submission.

- On Artifact Catalog page, the `apply-artifact-filter` button submits the search input `search-artifact` to filter artifacts.

- On Exhibitions page, selecting an option from `filter-exhibition-type` and clicking `apply-exhibition-filter` filters the exhibition list.

- On Virtual Events page:
  - `register-event-button-{event_id}` registers the user for that event.
  - `cancel-registration-button-{registration_id}` cancels the registration.

- On Audio Guides page:
  - `filter-language` dropdown + `apply-language-filter` button filters audio guides.
  - `play-guide-button-{guide_id}` plays the selected audio guide.


## Section 3: UI Component Details

### Tables
- Artifact Table (`artifact-table`):
  - Columns: Artifact ID, Name, Period, Origin, Exhibition, Actions
  - Rows populated dynamically with artifact data placeholders, e.g., `{{ artifact.artifact_id }}`, `{{ artifact.artifact_name }}` etc.

- Exhibitions Table (`exhibition-list`):
  - Columns: Title, Type, Start Date, End Date, Gallery, Status, Actions
  - Each row includes a button `view-exhibition-button-{{ exhibition.exhibition_id }}`

- Exhibition Artifacts Table (`exhibition-artifacts`):
  - Columns: Artifact ID, Name, Period, Origin

- Visitor Tickets Table (`my-tickets-table`):
  - Columns: Ticket ID, Ticket Type, Visit Date, Visit Time, Number of Tickets, Price

- Virtual Events Table (`event-list`):
  - Columns: Title, Date, Time, Type, Registration Status, Actions
  - Actions column includes buttons with dynamic IDs for register or cancel actions

- Audio Guides Table (`audio-guide-list`):
  - Columns: Exhibit Number, Title, Language, Duration, Actions
  - Actions column includes buttons `play-guide-button-{{ guide.guide_id }}`

### Inputs
- Search input for artifacts (`search-artifact`): type text, placeholder "Search by Artifact Name or ID"
- Number of tickets (`number-of-tickets`): type number, min="1", placeholder "Enter number of tickets"

### Dropdowns
- Exhibition type filter (`filter-exhibition-type`): Options - Permanent, Temporary, Virtual
- Ticket type selector (`ticket-type`): Options - Standard, Student, Senior, Family, VIP
- Audio guide language filter (`filter-language`): Options - English, Spanish, French

### Buttons
- Standard buttons for navigation and actions as described, with exact IDs.
- Dynamic buttons in tables must have IDs with the pattern described:
  - `view-exhibition-button-{exhibition_id}`
  - `register-event-button-{event_id}`
  - `cancel-registration-button-{registration_id}`
  - `play-guide-button-{guide_id}`

### Additional Notes
- Each template should include page title in the `<title>` tag matching the indicated page title.
- Containers should be used to wrap content consistently for styling and JS targeting.

---

This detailed specification enables frontend developers to build the VirtualMuseum HTML templates and UI exactly as required.
