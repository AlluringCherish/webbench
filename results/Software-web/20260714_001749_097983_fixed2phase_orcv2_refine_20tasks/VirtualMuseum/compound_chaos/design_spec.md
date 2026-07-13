# VirtualMuseum Web Application Design Specification

---

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Container ID: `dashboardPage`
- UI Elements:
  - Title (h1): `dashboardTitle`
  - Navigation Buttons:
    - Artifact Catalog Button (Button): `btnToCatalog`
    - Exhibitions Button (Button): `btnToExhibitions`
    - Visitor Tickets Button (Button): `btnToTickets`
    - Virtual Events Button (Button): `btnToEvents`
    - Audio Guides Button (Button): `btnToAudioGuides`

### 2. Artifact Catalog Page
- Container ID: `catalogPage`
- UI Elements:
  - Search Bar (Input Type Text): `catalogSearchBar`
  - Filter Dropdown (Select): `catalogFilter`
  - Artifacts List Container (Div): `artifactList`
  - Back to Dashboard Button (Button): `btnBackToDashboardFromCatalog`

### 3. Exhibitions Page
- Container ID: `exhibitionsPage`
- UI Elements:
  - Exhibitions List Container (Div): `exhibitionsList`
  - Back to Dashboard Button (Button): `btnBackToDashboardFromExhibitions`

### 4. Exhibition Details Page
- Container ID: `exhibitionDetailsPage`
- UI Elements:
  - Exhibition Title (h2): `exhibitionTitle`
  - Exhibition Description (Paragraph or Div): `exhibitionDescription`
  - Artifact List Container (Div): `exhibitionArtifactList`
  - Book Tickets Button (Button): `btnBookTicketsFromExhibition`
  - Back to Exhibitions Button (Button): `btnBackToExhibitions`

### 5. Visitor Tickets Page
- Container ID: `ticketsPage`
- UI Elements:
  - Tickets List Container (Div): `ticketsList`
  - Purchase Ticket Button (Button): `btnPurchaseTicket`
  - Back to Dashboard Button (Button): `btnBackToDashboardFromTickets`

### 6. Virtual Events Page
- Container ID: `eventsPage`
- UI Elements:
  - Events List Container (Div): `eventsList`
  - Register for Event Button (Button): `btnRegisterEvent`
  - Back to Dashboard Button (Button): `btnBackToDashboardFromEvents`

### 7. Audio Guides Page
- Container ID: `audioGuidesPage`
- UI Elements:
  - Audio Guides List Container (Div): `audioGuidesList`
  - Play Audio Guide Button (Button): `btnPlayAudioGuide`
  - Back to Dashboard Button (Button): `btnBackToDashboardFromAudioGuides`

---

## Section 2: Navigation Mapping

- Dashboard (`dashboardPage`):
  - `btnToCatalog` → Artifact Catalog Page
  - `btnToExhibitions` → Exhibitions Page
  - `btnToTickets` → Visitor Tickets Page
  - `btnToEvents` → Virtual Events Page
  - `btnToAudioGuides` → Audio Guides Page

- Artifact Catalog Page (`catalogPage`):
  - `btnBackToDashboardFromCatalog` → Dashboard Page

- Exhibitions Page (`exhibitionsPage`):
  - `btnBackToDashboardFromExhibitions` → Dashboard Page
  - Click on exhibition in `exhibitionsList` → Exhibition Details Page

- Exhibition Details Page (`exhibitionDetailsPage`):
  - `btnBackToExhibitions` → Exhibitions Page
  - `btnBookTicketsFromExhibition` → Visitor Tickets Page

- Visitor Tickets Page (`ticketsPage`):
  - `btnBackToDashboardFromTickets` → Dashboard Page
  - `btnPurchaseTicket` → Ticket purchase form/overlay

- Virtual Events Page (`eventsPage`):
  - `btnBackToDashboardFromEvents` → Dashboard Page
  - `btnRegisterEvent` → Event registration form/overlay

- Audio Guides Page (`audioGuidesPage`):
  - `btnBackToDashboardFromAudioGuides` → Dashboard Page
  - `btnPlayAudioGuide` → Play selected audio guide

---

## Section 3: Data Storage Formats

Data files are stored in the `data` directory as pipe (`|`) separated values.

### `users.dat`
- Fields: `user_id|username|email|password_hash|role`
- Example:
  - `1001|jdoe|jdoe@example.com|a1b2c3d4e5f6g7h8|visitor`

### `galleries.dat`
- Fields: `gallery_id|name|location|contact_info`
- Example:
  - `10|Modern Art Gallery|123 Art St, Cityville|info@modernart.example`

### `exhibitions.dat`
- Fields: `exhibition_id|gallery_id|title|description|start_date|end_date`
- Date format: `YYYY-MM-DD`
- Example:
  - `200|10|Impressionist Masterpieces|A collection of impressionist paintings|2024-06-01|2024-09-30`

### `artifacts.dat`
- Fields: `artifact_id|exhibition_id|name|description|origin|year|image_filename`
- Example:
  - `300|200|Water Lilies Painting|A famous painting of water lilies|France|1916|waterlilies.jpg`

### `audioguides.dat`
- Fields: `audio_id|artifact_id|title|audio_filename|duration_seconds`
- Example:
  - `400|300|Water Lilies Guide|waterlilies_guide.mp3|450`

### `tickets.dat`
- Fields: `ticket_id|user_id|exhibition_id|purchase_date|seat_number`
- Date format: `YYYY-MM-DD`
- Example:
  - `500|1001|200|2024-05-15|A12`

### `events.dat`
- Fields: `event_id|title|description|event_date|start_time|end_time`
- Date format: `YYYY-MM-DD`, time format: `HH:MM` 24-hour
- Example:
  - `600|Virtual Tour of Impressionism|Online virtual tour event|2024-07-10|18:00|19:30`

### `event_registrations.dat`
- Fields: `registration_id|event_id|user_id|registration_date`
- Date format: `YYYY-MM-DD`
- Example:
  - `700|600|1001|2024-06-01`

### `collection_logs.dat`
- Fields: `log_id|artifact_id|user_id|action|timestamp`
- Actions: `viewed`, `borrowed`, `returned`
- Timestamp: ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`
- Example:
  - `800|300|1001|viewed|2024-06-15T14:30:00Z`

---

End of VirtualMuseum Design Specification.
