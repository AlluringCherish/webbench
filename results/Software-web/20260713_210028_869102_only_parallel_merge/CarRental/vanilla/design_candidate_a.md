# CarRental Application Design Candidate A

---

## Overview
This document provides a detailed design candidate for the 'CarRental' Flask web application based on the provided requirements. It includes defined Flask routes, page titles, element IDs, navigation flows, and data storage strategies corresponding to the nine specified pages. All data is managed through local text files under the `data/` directory.

---

# 1. Dashboard Page

- **Route:** `/` (GET)
- **View Function:** `dashboard()`
- **Page Title:** `Car Rental Dashboard`
- **Element IDs:**
  - `dashboard-page` (Container div)
  - `featured-vehicles`
  - `search-vehicles-button` (Button)
  - `my-reservations-button` (Button)
  - `promotions-section`

### Navigation and Actions:
- Clicking `search-vehicles-button` navigates to `/search-vehicles` (vehicle_search).
- Clicking `my-reservations-button` navigates to `/reservations` (reservations).

### Data Handling:
- Reads vehicles data from `data/vehicles.txt` to populate `featured-vehicles` (e.g., top 3 featured vehicles).
- Reads promotions data from local static data or separate file if available (not specified). Could be hard-coded or extended later.

---

# 2. Vehicle Search Page

- **Route:** `/search-vehicles` (GET, POST)
- **View Function:** `vehicle_search()`
- **Page Title:** `Search Vehicles`
- **Element IDs:**
  - `search-page`
  - `location-filter` (Dropdown)
  - `vehicle-type-filter` (Dropdown)
  - `date-range-input` (Input; possibly custom date range picker)
  - `vehicles-grid` (Div to display vehicle cards)
  - `view-details-button-{vehicle_id}` (Button for each vehicle)

### Navigation and Actions:
- Filters are applied via POST (or GET with parameters), filtering vehicles by availability based on selected location, type, and date-range.
- Clicking `view-details-button-{vehicle_id}` redirects to `/vehicle-details/<vehicle_id>` (vehicle_details).

### Data Handling:
- Reads `vehicles.txt` for available vehicles.
- Filters vehicles based on `status` and possibly availability at location (requires cross-check with rentals/reservations).
- For each vehicle, show image (if available), model, and price per day.

---

# 3. Vehicle Details Page

- **Route:** `/vehicle-details/<int:vehicle_id>` (GET)
- **View Function:** `vehicle_details(vehicle_id)`
- **Page Title:** `Vehicle Details`
- **Element IDs:**
  - `vehicle-details-page`
  - `vehicle-name` (H1)
  - `vehicle-specs` (Div with engine, seats, transmission)
  - `daily-rate` (Div)
  - `book-now-button` (Button)
  - `vehicle-reviews` (Div)

### Navigation and Actions:
- Clicking `book-now-button` navigates to `/booking/<vehicle_id>` (booking).

### Data Handling:
- Reads vehicle info from `vehicles.txt` by `vehicle_id`.
- Customer reviews could be stored separately or hardcoded as not specified, so this section can be read from a local reviews file if implemented.

---

# 4. Booking Page

- **Route:** `/booking/<int:vehicle_id>` (GET, POST)
- **View Function:** `booking(vehicle_id)`
- **Page Title:** `Book Your Rental`
- **Element IDs:**
  - `booking-page`
  - `pickup-location` (Dropdown)
  - `dropoff-location` (Dropdown)
  - `pickup-date` (Input - date picker)
  - `dropoff-date` (Input - date picker)
  - `calculate-price-button` (Button)
  - `total-price` (Div)
  - `proceed-to-insurance-button` (Button)

### Navigation and Actions:
- `calculate-price-button` computes rental price = daily_rate * number_of_days (based on input dates).
- Clicking `proceed-to-insurance-button` submits booking dates and locations, then navigates to `/insurance-options/<vehicle_id>` (insurance_options), passing booking and pricing info accordingly.

### Data Handling:
- Reads vehicle daily rate from `vehicles.txt`.
- Reads pickup/dropoff locations from `locations.txt`.
- Stores booking details temporarily in session or via POST/GET params until confirmed.

---

# 5. Insurance Options Page

- **Route:** `/insurance-options/<int:vehicle_id>` (GET, POST)
- **View Function:** `insurance_options(vehicle_id)`
- **Page Title:** `Select Insurance Coverage`
- **Element IDs:**
  - `insurance-page`
  - `insurance-options` (Div listing all insurance plans)
  - `select-insurance-{insurance_id}` (Radio button for each plan)
  - `insurance-description`
  - `insurance-price`
  - `confirm-booking-button` (Button)

### Navigation and Actions:
- Selecting a radio updates `insurance-description` and `insurance-price` dynamically.
- Clicking `confirm-booking-button` finalizes booking:
  - Writes new entries to `rentals.txt` and `reservations.txt` with assigned IDs.
  - Redirect to `/my-reservations` (reservations) or a booking confirmation page.

### Data Handling:
- Reads insurance plans from `insurance.txt`.
- On confirm, writes updated rental and reservation data.

---

# 6. Rental History Page

- **Route:** `/rental-history` (GET)
- **View Function:** `rental_history()`
- **Page Title:** `Rental History`
- **Element IDs:**
  - `history-page`
  - `rentals-table` (Table listing all rentals)
  - `view-rental-details-{rental_id}` (Button for each rental)
  - `status-filter` (Dropdown filter)
  - `back-to-dashboard` (Button)

### Navigation and Actions:
- Clicking a rental's `view-rental-details-{rental_id}` shows detailed info, optionally a modal or new page.
- `status-filter` filters rentals by status.
- Clicking `back-to-dashboard` navigates to `/` (dashboard).

### Data Handling:
- Reads all rentals from `rentals.txt`.
- Joins vehicle and customer data for display as needed.

---

# 7. Reservation Management Page

- **Route:** `/reservations` (GET, POST)
- **View Function:** `reservations()`
- **Page Title:** `My Reservations`
- **Element IDs:**
  - `reservations-page`
  - `reservations-list`
  - `modify-reservation-button-{reservation_id}` (Button per reservation)
  - `cancel-reservation-button-{reservation_id}` (Button per reservation)
  - `sort-by-date-button` (Button)
  - `back-to-dashboard` (Button)

### Navigation and Actions:
- Clicking `modify-reservation-button-{reservation_id}` opens a form/page to edit dates or locations.
- Clicking `cancel-reservation-button-{reservation_id}` updates status to cancelled in `reservations.txt` and possibly `rentals.txt`.
- `sort-by-date-button` sorts reservations chronologically.
- Clicking `back-to-dashboard` navigates to `/`.

### Data Handling:
- Reads `reservations.txt` for current and upcoming reservations.
- Update operations write back to `reservations.txt`.

---

# 8. Special Requests Page

- **Route:** `/special-requests` (GET, POST)
- **View Function:** `special_requests()`
- **Page Title:** `Special Requests`
- **Element IDs:**
  - `requests-page`
  - `select-reservation` (Dropdown of active reservations)
  - `driver-assistance-checkbox` (Checkbox)
  - `gps-option-checkbox` (Checkbox)
  - `child-seat-quantity` (Input)
  - `special-notes` (Textarea)
  - `submit-requests-button` (Button)

### Navigation and Actions:
- User selects a reservation, specifies special requests, and submits.
- On submit, updates the `special_requests` field in `reservations.txt` for that reservation.

### Data Handling:
- Reads active reservations from `reservations.txt`.
- Writes updated special requests back into `reservations.txt`.

---

# 9. Locations Page

- **Route:** `/locations` (GET)
- **View Function:** `locations()`
- **Page Title:** `Pickup and Dropoff Locations`
- **Element IDs:**
  - `locations-page`
  - `locations-list`
  - `location-detail-button-{location_id}` (Button per location)
  - `hours-filter` (Dropdown)
  - `search-location-input` (Input)
  - `back-to-dashboard` (Button)

### Navigation and Actions:
- Filtering locations by operating hours using `hours-filter`.
- Searching by city or name using `search-location-input`.
- Clicking `location-detail-button-{location_id}` shows detailed information about location.
- Clicking `back-to-dashboard` navigates to `/`.

### Data Handling:
- Reads `locations.txt` for list and details.

---

# Data Storage Strategy Summary

| Data File         | Usage Context(s)                                | Operation           |
|-------------------|------------------------------------------------|---------------------|
| `vehicles.txt`     | Dashboard (featured), Search Vehicles, Details | Read-only           |
| `customers.txt`    | Rentals, Reservations (joining data)           | Read-only           |
| `locations.txt`    | Booking, Locations page                         | Read-only           |
| `rentals.txt`      | Rental History, Reservations, Booking finalize | Read & Write        |
| `insurance.txt`    | Insurance Options                               | Read-only           |
| `reservations.txt` | Reservation Management, Special Requests       | Read & Write        |

---

# UI/UX and Overall Flow Considerations:
- The root URL `/` serves the Dashboard.
- All navigation uses HTTP GET for page loads, POST for data modifications (booking, updates).
- Use consistent button styles and accessible labels.
- Provide feedback on data operations (e.g., price calculation, booking confirmation).
- Filters and dropdowns allow easy dynamic content adjustment.
- Data validation on forms (dates, locations, quantities).
- Session or query parameters can carry temporary booking context between pages.

---

This design document is ready for implementation as design_candidate_a.md.

