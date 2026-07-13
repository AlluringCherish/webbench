# VirtualMuseum Web Application Design Specification

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Container ID: dashboard-container
- UI Elements:
  - Heading: h1 with id "dashboard-title" (text: "VirtualMuseum Dashboard")
  - Navigation Buttons:
    - Artifact Catalog button: button with id "btn-artifact-catalog"
    - Exhibitions button: button with id "btn-exhibitions"
    - Visitor Tickets button: button with id "btn-visitor-tickets"
    - Virtual Events button: button with id "btn-virtual-events"
    - Audio Guides button: button with id "btn-audio-guides"

### 2. Artifact Catalog Page
- Container ID: artifact-catalog-container
- UI Elements:
  - Heading: h1 with id "artifact-catalog-title" (text: "Artifact Catalog")
  - Artifact List Container: div with id "artifact-list"
  - Artifact Search Input: input text with id "artifact-search"
  - Navigation Buttons:
    - Back to Dashboard button: button with id "btn-back-dashboard"
    - Exhibition Details button: button with id "btn-artifact-exhibition-details"
      (Visible and enabled only when the selected artifact is linked to an exhibition; otherwise hidden or disabled.)

### 3. Exhibitions Page
- Container ID: exhibitions-container
- UI Elements:
  - Heading: h1 with id "exhibitions-title" (text: "Exhibitions")
  - Exhibitions List Container: div with id "exhibitions-list"
  - Navigation Buttons:
    - Back to Dashboard button: button with id "btn-back-dashboard"
    - Exhibition Details button: button with id "btn-exhibition-exhibition-details"

### 4. Exhibition Details Page
- Container ID: exhibition-details-container
- UI Elements:
  - Heading: h1 with id "exhibition-details-title" (dynamic text: exhibition name)
  - Exhibition Description: p with id "exhibition-description"
  - Artifact List Container: div with id "exhibition-artifact-list"
  - Navigation Buttons:
    - Back to Exhibitions button: button with id "btn-back-exhibitions"
    - Back to Artifact Catalog button: button with id "btn-back-artifact-catalog"

### 5. Visitor Tickets Page
- Container ID: visitor-tickets-container
- UI Elements:
  - Heading: h1 with id "visitor-tickets-title" (text: "Visitor Tickets")
  - Ticket Purchase Form: form with id "ticket-purchase-form"
    - Input for visitor name: input text with id "input-visitor-name"
    - Select for exhibition: select dropdown with id "select-exhibition"
    - Input for date: input date with id "input-ticket-date" (format: yyyy-mm-dd)
    - Submit button: button with id "btn-submit-ticket"
  - Navigation Buttons:
    - Back to Dashboard button: button with id "btn-back-dashboard"

### 6. Virtual Events Page
- Container ID: virtual-events-container
- UI Elements:
  - Heading: h1 with id "virtual-events-title" (text: "Virtual Events")
  - Events List Container: div with id "events-list"
  - Register for Event Form: form with id "event-registration-form"
    - Input for visitor name: input text with id "input-event-visitor-name"
    - Select for event: select dropdown with id "select-event"
    - Submit button: button with id "btn-submit-registration"
  - Navigation Buttons:
    - Back to Dashboard button: button with id "btn-back-dashboard"

### 7. Audio Guides Page
- Container ID: audio-guides-container
- UI Elements:
  - Heading: h1 with id "audio-guides-title" (text: "Audio Guides")
  - Audio Guides List Container: div with id "audio-guides-list" (UI provides selection of audio guide)
  - Play Audio Guide Button: button with id "btn-play-audio-guide" (plays selected audio guide)
  - Navigation Buttons:
    - Back to Dashboard button: button with id "btn-back-dashboard"

## Section 2: Navigation Mapping

- Dashboard Page Navigation:
  - btn-artifact-catalog -> Artifact Catalog Page
  - btn-exhibitions -> Exhibitions Page
  - btn-visitor-tickets -> Visitor Tickets Page
  - btn-virtual-events -> Virtual Events Page
  - btn-audio-guides -> Audio Guides Page

- Artifact Catalog Page Navigation:
  - btn-back-dashboard -> Dashboard Page
  - btn-artifact-exhibition-details -> Exhibition Details Page (for selected artifact's exhibition)

- Exhibitions Page Navigation:
  - btn-back-dashboard -> Dashboard Page
  - btn-exhibition-exhibition-details -> Exhibition Details Page (for selected exhibition)

- Exhibition Details Page Navigation:
  - btn-back-exhibitions -> Exhibitions Page
  - btn-back-artifact-catalog -> Artifact Catalog Page

- Visitor Tickets Page Navigation:
  - btn-back-dashboard -> Dashboard Page

- Virtual Events Page Navigation:
  - btn-back-dashboard -> Dashboard Page

- Audio Guides Page Navigation:
  - btn-back-dashboard -> Dashboard Page

## Section 3: Data Storage Formats

All data files are stored in the `data` directory.
Audio media files referenced in audioguides.txt are stored under an `audio` directory relative to the application root.

### 1. users.txt
- Format: pipe-separated
- Fields: user_id|username|password_hash|role
- Example: 1|john_doe|abcd1234hash|visitor

### 2. galleries.txt
- Format: pipe-separated
- Fields: gallery_id|name|location
- Example: 10|Ancient Artifacts Gallery|First Floor

### 3. exhibitions.txt
- Format: pipe-separated
- Fields: exhibition_id|name|description|gallery_id
- Example: 101|Egyptian Antiquities|A collection of artifacts from ancient Egypt|10

### 4. artifacts.txt
- Format: pipe-separated
- Fields: artifact_id|name|description|exhibition_id
- Example: 1001|Golden Mask of Tutankhamun|A burial mask from 14th century BC|101

### 5. audioguides.txt
- Format: pipe-separated
- Fields: guide_id|artifact_id|audio_file_path
- Note: audio_file_path is relative to application root, usually under `audio/` directory
- Example: 2001|1001|audio/golden_mask_guide.mp3

### 6. tickets.txt
- Format: pipe-separated
- Fields: ticket_id|visitor_name|exhibition_id|date
- Date format: yyyy-mm-dd (ISO 8601)
- Example: 3001|Jane Smith|101|2024-07-15

### 7. events.txt
- Format: pipe-separated
- Fields: event_id|name|description|date|time
- Date format: yyyy-mm-dd, Time format: HH:mm (24-hour)
- Example: 4001|Virtual Tour of Egyptian Antiquities|An online guided tour|2024-08-01|14:00

### 8. event_registrations.txt
- Format: pipe-separated
- Fields: registration_id|event_id|visitor_name
- Example: 5001|4001|Jane Smith

### 9. collection_logs.txt
- Format: pipe-separated
- Fields: log_id|artifact_id|visitor_name|date
- Date format: yyyy-mm-dd
- Example: 6001|1001|Jane Smith|2024-07-15

## Additional Notes
- User roles defined in users.txt exist, but role-based UI or access controls are currently out of scope.
- To avoid ID collisions, different button IDs are used on Artifact Catalog and Exhibitions pages for "Exhibition Details" navigation:
  - Artifact Catalog: btn-artifact-exhibition-details
  - Exhibitions: btn-exhibition-exhibition-details
- Audio Guides page includes a selection list of guides; "Play Audio Guide" button acts on selected guide.
- Date formats are consistent across UI inputs and data files, following ISO 8601 pattern.
- Audio files are stored separately in an `audio` directory per relative paths in audioguides.txt.

---

End of VirtualMuseum Design Specification
