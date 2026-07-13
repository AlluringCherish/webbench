# Frontend Design for CarRental Web Application

## Section 1: HTML Template Specifications

---

### 1. Dashboard Page
- Template Filename: dashboard.html
- Page Title: Car Rental Dashboard
- Elements:
  - ID: dashboard-page (Div) - Main container for the dashboard page.
  - ID: featured-vehicles (Div) - Displays featured vehicle recommendations.
  - ID: search-vehicles-button (Button) - Navigates to Vehicle Search page.
  - ID: my-reservations-button (Button) - Navigates to My Reservations page.
  - ID: promotions-section (Div) - Displays current promotions and offers.

---

### 2. Vehicle Search Page
- Template Filename: vehicle_search.html
- Page Title: Search Vehicles
- Elements:
  - ID: search-page (Div) - Container for the search page.
  - ID: location-filter (Dropdown) - Filter by pickup location.
  - ID: vehicle-type-filter (Dropdown) - Filter by vehicle type [Economy, Compact, Sedan, SUV, Luxury].
  - ID: date-range-input (Input) - Input to select rental date range.
  - ID: vehicles-grid (Div) - Grid displaying vehicle cards.
    - Each vehicle card includes:
      - Vehicle image (img tag, no fixed id - use Jinja loop)
      - Model and price per day (within vehicle card)
      - ID: view-details-button-{vehicle_id} (Button) - Button to view detailed info of that vehicle.

---

### 3. Vehicle Details Page
- Template Filename: vehicle_details.html
- Page Title: Vehicle Details
- Elements:
  - ID: vehicle-details-page (Div) - Main container for vehicle details.
  - ID: vehicle-name (H1) - Displays vehicle name and model.
  - ID: vehicle-specs (Div) - Displays vehicle specifications (engine, seats, transmission).
  - ID: daily-rate (Div) - Shows daily rental rate.
  - ID: book-now-button (Button) - Button to initiate booking for this vehicle.
  - ID: vehicle-reviews (Div) - Section for customer reviews on this vehicle.

---

### 4. Booking Page
- Template Filename: booking.html
- Page Title: Book Your Rental
- Elements:
  - ID: booking-page (Div) - Container for booking page.
  - ID: pickup-location (Dropdown) - Select pickup location.
  - ID: dropoff-location (Dropdown) - Select dropoff location.
  - ID: pickup-date (Input) - Pickup date selector.
  - ID: dropoff-date (Input) - Dropoff date selector.
  - ID: calculate-price-button (Button) - Calculates total rental price.
  - ID: total-price (Div) - Displays calculated total price.
  - ID: proceed-to-insurance-button (Button) - Proceed to Insurance Options page.

---

### 5. Insurance Options Page
- Template Filename: insurance.html
- Page Title: Select Insurance Coverage
- Elements:
  - ID: insurance-page (Div) - Main container for insurance selection.
  - ID: insurance-options (Div) - Displays available insurance plans.
    - Each plan includes:
      - ID: select-insurance-{insurance_id} (Radio) - Radio button to select insurance plan.
  - ID: insurance-description (Div) - Description of selected insurance plan.
  - ID: insurance-price (Div) - Price of selected insurance plan.
  - ID: confirm-booking-button (Button) - Confirm booking with insurance selection.

---

### 6. Rental History Page
- Template Filename: rental_history.html
- Page Title: Rental History
- Elements:
  - ID: history-page (Div) - Container for rental history page.
  - ID: rentals-table (Table) - Table of rentals with columns: ID, vehicle, dates, location, status.
  - ID: view-rental-details-{rental_id} (Button) - Button to view details of rental.
  - ID: status-filter (Dropdown) - Filter rentals by status (All, Active, Completed, Cancelled).
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.

---

### 7. Reservation Management Page
- Template Filename: reservations.html
- Page Title: My Reservations
- Elements:
  - ID: reservations-page (Div) - Container for reservations.
  - ID: reservations-list (Div) - List of current and upcoming reservations.
    - Each reservation item includes:
      - ID: modify-reservation-button-{reservation_id} (Button) - Modify reservation button.
      - ID: cancel-reservation-button-{reservation_id} (Button) - Cancel reservation button.
  - ID: sort-by-date-button (Button) - Sort reservations by date.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.

---

### 8. Special Requests Page
- Template Filename: special_requests.html
- Page Title: Special Requests
- Elements:
  - ID: requests-page (Div) - Container for special requests.
  - ID: select-reservation (Dropdown) - Select reservation to add requests.
  - ID: driver-assistance-checkbox (Checkbox) - Request driver assistance.
  - ID: gps-option-checkbox (Checkbox) - Include GPS option.
  - ID: child-seat-quantity (Input) - Number input for child seats.
  - ID: special-notes (Textarea) - Field for additional notes.
  - ID: submit-requests-button (Button) - Submit special requests.

---

### 9. Locations Page
- Template Filename: locations.html
- Page Title: Pickup and Dropoff Locations
- Elements:
  - ID: locations-page (Div) - Container for locations.
  - ID: locations-list (Div) - List of rental locations.
    - Each location item includes:
      - ID: location-detail-button-{location_id} (Button) - View location details.
  - ID: hours-filter (Dropdown) - Filter by operating hours (24/7, Business Hours, Weekend).
  - ID: search-location-input (Input) - Search locations by city or name.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.

---

## Section 2: Navigation and Interaction Design

### Navigation Flows

- From Dashboard:
  - search-vehicles-button -> Navigate to Vehicle Search Page (vehicle_search.html)
  - my-reservations-button -> Navigate to Reservations Page (reservations.html)
  - back-to-dashboard (where present) navigates to Dashboard Page (dashboard.html)

- From Vehicle Search:
  - view-details-button-{vehicle_id} -> Navigate to Vehicle Details Page (vehicle_details.html) for selected vehicle.

- From Vehicle Details:
  - book-now-button -> Navigate to Booking Page (booking.html) with selected vehicle context.

- From Booking:
  - calculate-price-button -> Calculate and display total price in total-price div.
  - proceed-to-insurance-button -> Navigate to Insurance Options Page (insurance.html) with booking details.

- From Insurance Options:
  - confirm-booking-button -> Finalize booking and navigate to Rental History or Reservations as confirmation.

- From Rental History:
  - view-rental-details-{rental_id} -> Show rental details (could be modal or new page)
  - back-to-dashboard -> Dashboard Page

- From Reservations:
  - modify-reservation-button-{reservation_id} -> Modify selected reservation page or modal
  - cancel-reservation-button-{reservation_id} -> Cancel reservation action
  - sort-by-date-button -> Sort reservation list
  - back-to-dashboard -> Dashboard Page

- From Special Requests:
  - submit-requests-button -> Submit special requests and confirm

- From Locations:
  - location-detail-button-{location_id} -> Show location details
  - back-to-dashboard -> Dashboard Page

### Dynamic Data Placeholders (Typical Jinja2 Variable Usage)

- Vehicles list for vehicle search and featured vehicles: `{% for vehicle in vehicles %}` with attributes like `vehicle.id`, `vehicle.make`, `vehicle.model`, `vehicle.daily_rate`.
- Locations list for location-filter, pickup and dropoff locations: `{% for location in locations %}`
- Reservations and Rentals: `{% for reservation in reservations %}` or `{% for rental in rentals %}`
- Insurance options: `{% for plan in insurance_plans %}`
- Special requests per reservation: Reservation IDs populate `select-reservation` dropdown.

---

This completes the frontend design specification for the CarRental app covering all 9 pages, UI components, element IDs, and navigation flows as required.