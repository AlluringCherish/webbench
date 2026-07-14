# TravelPlanner Web Application Design Specification (design_debate_b.md) - Revised Round 2

---

## Section 1: Route and URL Structure

1. **Root Route**
   - Route: `/`
   - HTTP Method: `GET`
   - Behavior: Render the Dashboard page. (As a landing entry page)

2. **Dashboard Page**
   - Route: `/dashboard`
   - HTTP Method: `GET`
   - Render template: `dashboard.html`

3. **Destinations Page**
   - Route: `/destinations`
   - HTTP Methods: `GET`, `POST`
   - POST method included to handle search/filter submissions as recommended by peer.
   - Render template: `destinations.html`

4. **Destination Details Page**
   - Route: `/destination/<int:dest_id>`  <!-- aligned route to peer 'destination/<int:dest_id>' to be consistent -->
   - HTTP Methods: `GET`, `POST`
   - POST for 'add to trip' action per peer suggestion.
   - Render template: `destination_details.html`

5. **Itinerary Planning Page**
   - Route: `/itinerary`
   - HTTP Methods: `GET`, `POST`
   - POST for creation/updating activities or whole itinerary.
   - Render template: `itinerary.html`

6. **Accommodations Page**
   - Route: `/accommodations`
   - HTTP Methods: `GET`, `POST`
   - POST for search/filter submission.
   - Render template: `accommodations.html`

7. **Transportation Page**
   - Route: `/transportation`
   - HTTP Methods: `GET`, `POST`
   - POST for flight search/filter.
   - Render template: `transportation.html`

8. **Travel Packages Page**
   - Route: `/packages`
   - HTTP Methods: `GET`, `POST`
   - POST to handle package booking operations.
   - Render template: `packages.html`

9. **Package Details and Booking**
   - View Package Details:
     - Route: `/packages/<int:pkg_id>`
     - HTTP Method: `GET`
     - Render template: `package_details.html`
   - Book Package:
     - Route: `/packages/<int:pkg_id>/book`
     - HTTP Method: `POST`
     - Form action to `/packages/<int:pkg_id>/book`

10. **Trip Management Page**
    - Route: `/trips`
    - HTTP Methods: `GET`, `POST`
    - POST used for edit/delete trip operations.
    - Render template: `trips.html`

11. **Trip Details**
    - Route: `/trips/<int:trip_id>`
    - HTTP Method: `GET`
    - Render template: `trip_details.html`

12. **Booking Confirmation Page**
    - Route: `/booking-confirmation`  <!-- aligned with peer route style -->
    - HTTP Method: `GET`
    - Render template: `booking_confirmation.html`

13. **Travel Recommendations Page**
    - Route: `/recommendations`
    - HTTP Methods: `GET`, `POST`
    - POST to handle filters as suggested by peer.
    - Render template: `recommendations.html`

---

## Section 2: Template Files and HTML Element Details

### Dashboard Page (template: `dashboard.html`)
- Elements:
  - Div ID: `dashboard-page`
  - Div ID: `featured-destinations`
  - Div ID: `upcoming-trips`
  - Button ID: `browse-destinations-button` (navigates to `/destinations`)
  - Button ID: `plan-itinerary-button` (navigates to `/itinerary`)

### Destinations Page (template: `destinations.html`)
- Elements:
  - Div ID: `destinations-page`
  - Input ID: `search-destination`
  - Dropdown ID: `region-filter` (Asia, Europe, Americas, Africa, Oceania)
  - Div ID: `destinations-grid`
  - Buttons with ID pattern: `view-destination-button-{dest_id}`

### Destination Details Page (template: `destination_details.html`)
- Elements:
  - Div ID: `destination-details-page`
  - H1 ID: `destination-name`
  - Div ID: `destination-country`
  - Div ID: `destination-description`
  - Button ID: `add-to-trip-button`
  - Div ID: `destination-attractions`

### Itinerary Planning Page (template: `itinerary.html`)
- Elements:
  - Div ID: `itinerary-page`
  - Input ID: `itinerary-name-input`
  - Input (date) ID: `start-date-input`
  - Input (date) ID: `end-date-input`
  - Button ID: `add-activity-button`
  - Div ID: `itinerary-list`

### Accommodations Page (template: `accommodations.html`)
- Elements:
  - Div ID: `accommodations-page`
  - Input ID: `destination-input`
  - Input (date) ID: `check-in-date`
  - Input (date) ID: `check-out-date`
  - Dropdown ID: `price-filter` (Budget, Mid-range, Luxury)
  - Div ID: `hotels-list`

### Transportation Page (template: `transportation.html`)
- Elements:
  - Div ID: `transportation-page`
  - Input ID: `departure-city`
  - Input ID: `arrival-city`
  - Input (date) ID: `departure-date`
  - Dropdown ID: `flight-class-filter` (Economy, Business, First Class)
  - Div ID: `available-flights`

### Travel Packages Page (template: `packages.html`)
- Elements:
  - Div ID: `packages-page`
  - Div ID: `packages-grid`
  - Dropdown ID: `duration-filter` (3-5 days, 7-10 days, 14+ days)
  - Buttons with ID pattern: `view-package-details-button-{pkg_id}`
  - Buttons with ID pattern: `book-package-button-{pkg_id}`

### Trip Management Page (template: `trips.html`)
- Elements:
  - Div ID: `trips-page`
  - Table ID: `trips-table`
  - Buttons with ID patterns: `view-trip-details-button-{trip_id}`, `edit-trip-button-{trip_id}`, `delete-trip-button-{trip_id}`

### Booking Confirmation Page (template: `booking_confirmation.html`)
- Elements:
  - Div ID: `confirmation-page`
  - Div ID: `confirmation-number`
  - Div ID: `booking-details`
  - Button ID: `download-itinerary-button`
  - Button ID: `share-trip-button`
  - Button ID: `back-to-dashboard` (navigates to `/dashboard`)

### Travel Recommendations Page (template: `recommendations.html`)
- Elements:
  - Div ID: `recommendations-page`
  - Div ID: `trending-destinations`
  - Dropdown ID: `recommendation-season-filter` (Spring, Summer, Fall, Winter)
  - Dropdown ID: `budget-filter` (Low, Medium, High)
  - Button ID: `back-to-dashboard` (navigates to `/dashboard`)

---

## Section 3: Local Text Data Persistence

- All data files are under `data/` folder.

### Destinations Data
- File: `data/destinations.txt`
- Fields: `dest_id|name|country|region|description|attractions|climate`
- Read for destinations lists and details.

### Itineraries Data
- File: `data/itineraries.txt`
- Fields: `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
- Read and write for managing itineraries.

### Hotels Data
- File: `data/hotels.txt`
- Fields: `hotel_id|name|city|rating|price_per_night|amenities|category`
- Read for hotel listings and filtering.

### Flights Data
- File: `data/flights.txt`
- Fields: `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
- Read for flight search and listings.

### Travel Packages Data
- File: `data/packages.txt`
- Fields: `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
- Read for package listings and details, write on booking.

### Trips Data
- File: `data/trips.txt`
- Fields: `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
- Read/write for trip management.

### Bookings Data
- File: `data/bookings.txt`
- Fields: `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
- Append and update for booking confirmation page.

---

*End of Revised design_debate_b.md After Peer Review*