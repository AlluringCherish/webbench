# Merged Design Specification for CarRental Flask Web Application

---

## Overview
This document consolidates the design specifications of the CarRental web application by merging Design Candidates A and B and aligns all pages, routes, UI elements, navigation flows, and data storage handling according to the given user requirements.

---

# Flask Routes and HTTP Methods

| Page                     | Route Path                              | Methods     | View Function         | Notes on Parameters                           |
|--------------------------|----------------------------------------|-------------|-----------------------|----------------------------------------------|
| Dashboard                | `/`                                   | GET         | dashboard()           | Serves as home page; alternate `/dashboard` redirects here
| Vehicle Search           | `/search-vehicles`                    | GET, POST   | vehicle_search()      | POST for applying filters/search criteria    |
| Vehicle Details          | `/vehicle-details/<int:vehicle_id>`  | GET         | vehicle_details(vehicle_id) | Displays details for selected vehicle       |
| Booking                  | `/booking/<int:vehicle_id>`           | GET, POST   | booking(vehicle_id)    | Booking form and submission                   |
| Insurance Options        | `/insurance/<int:reservation_id>`    | GET, POST   | insurance_options(reservation_id) | Select insurance for a given reservation     |
| Rental History           | `/rental-history`                     | GET         | rental_history()       | Displays past rentals and status filter      |
| Reservation Management   | `/reservations`                      | GET, POST   | reservations()         | Manage current/upcoming reservations          |
| Special Requests         | `/special-requests`                   | GET, POST   | special_requests()     | Add special requests to a selected reservation |
| Locations                | `/locations`                         | GET         | locations()            | Display and filter rental locations           |

---

# Pages, Titles, and Container Element IDs

| Page                     | Page Title                      | Container ID          |
|--------------------------|--------------------------------|-----------------------|
| Dashboard                | Car Rental Dashboard            | dashboard-page        |
| Vehicle Search           | Search Vehicles                 | search-page           |
| Vehicle Details          | Vehicle Details                 | vehicle-details-page  |
| Booking                  | Book Your Rental                | booking-page          |
| Insurance Options        | Select Insurance Coverage       | insurance-page        |
| Rental History           | Rental History                 | history-page          |
| Reservation Management   | My Reservations                | reservations-page     |
| Special Requests         | Special Requests               | requests-page         |
| Locations                | Pickup and Dropoff Locations   | locations-page        |

---

# Detailed Page Element IDs and Descriptions

## 1. Dashboard Page
- **Element IDs:**
  - `dashboard-page` (Div container)
  - `featured-vehicles` (Div for featured vehicle recommendations)
  - `search-vehicles-button` (Button, navigates to `/search-vehicles`)
  - `my-reservations-button` (Button, navigates to `/reservations`)
  - `promotions-section` (Div for current promotions/offers)

## 2. Vehicle Search Page
- **Element IDs:**
  - `search-page` (Div container)
  - `location-filter` (Dropdown to filter by pickup location)
  - `vehicle-type-filter` (Dropdown with Economy, Compact, Sedan, SUV, Luxury)
  - `date-range-input` (Input field for rental date range selection)
  - `vehicles-grid` (Div displaying vehicle cards)
  - `view-details-button-{vehicle_id}` (Button to view details for each vehicle, navigates to `/vehicle-details/<vehicle_id>`)

## 3. Vehicle Details Page
- **Element IDs:**
  - `vehicle-details-page` (Div container)
  - `vehicle-name` (H1 element for vehicle name and model)
  - `vehicle-specs` (Div for engine, seats, transmission specs)
  - `daily-rate` (Div showing daily rental rate)
  - `book-now-button` (Button, navigates to `/booking/<vehicle_id>`)
  - `vehicle-reviews` (Div for customer reviews; data source may be extended)

## 4. Booking Page
- **Element IDs:**
  - `booking-page` (Div container)
  - `pickup-location` (Dropdown for pickup location)
  - `dropoff-location` (Dropdown for dropoff location)
  - `pickup-date` (Input for pickup date selection)
  - `dropoff-date` (Input for dropoff date selection)
  - `calculate-price-button` (Button to calculate rental price based on dates and daily rate)
  - `total-price` (Div displaying calculated total price)
  - `proceed-to-insurance-button` (Button, post booking info, navigates to insurance options for reservation)

## 5. Insurance Options Page
- **Element IDs:**
  - `insurance-page` (Div container)
  - `insurance-options` (Div listing all insurance plans from `insurance.txt`)
  - `select-insurance-{insurance_id}` (Radio buttons per insurance plan)
  - `insurance-description` (Div showing description for selected insurance)
  - `insurance-price` (Div showing total insurance price = daily cost * rental duration)
  - `confirm-booking-button` (Button to confirm booking and finalize reservation, saves to rentals and reservations files)

## 6. Rental History Page
- **Element IDs:**
  - `history-page` (Div container)
  - `rentals-table` (Table listing rentals with columns: ID, vehicle, dates, location, status)
  - `view-rental-details-{rental_id}` (Button to view details for each rental)
  - `status-filter` (Dropdown to filter rentals by statuses: All, Active, Completed, Cancelled)
  - `back-to-dashboard` (Button, navigates back to `/`)

## 7. Reservation Management Page
- **Element IDs:**
  - `reservations-page` (Div container)
  - `reservations-list` (Div listing all reservations with vehicle info, dates, status)
  - `modify-reservation-button-{reservation_id}` (Button per reservation to modify details)
  - `cancel-reservation-button-{reservation_id}` (Button per reservation to cancel)
  - `sort-by-date-button` (Button to sort reservations by date)
  - `back-to-dashboard` (Button, navigates to `/`)

## 8. Special Requests Page
- **Element IDs:**
  - `requests-page` (Div container)
  - `select-reservation` (Dropdown to select reservation to add requests)
  - `driver-assistance-checkbox` (Checkbox for driver assistance request)
  - `gps-option-checkbox` (Checkbox for GPS option)
  - `child-seat-quantity` (Input for number of child seats needed)
  - `special-notes` (Textarea for additional notes/requests)
  - `submit-requests-button` (Button to submit special requests)

## 9. Locations Page
- **Element IDs:**
  - `locations-page` (Div container)
  - `locations-list` (Div listing all rental pickup and dropoff locations)
  - `location-detail-button-{location_id}` (Button to view details for each location)
  - `hours-filter` (Dropdown to filter locations by operating hours: 24/7, Business Hours, Weekend)
  - `search-location-input` (Input field for searching locations by city or name)
  - `back-to-dashboard` (Button, navigates back to `/`)

---

# Navigation and User Interaction Flow

- **Dashboard Page:**
  - `search-vehicles-button` navigates to Vehicle Search Page (`url_for('vehicle_search')`)
  - `my-reservations-button` navigates to Reservations Page (`url_for('reservations')`)

- **Vehicle Search Page:**
  - Filters applied via POST or GET parameters
  - `view-details-button-{vehicle_id}` navigates to Vehicle Details Page (`url_for('vehicle_details', vehicle_id=vehicle_id)`)

- **Vehicle Details Page:**
  - `book-now-button` navigates to Booking Page (`url_for('booking', vehicle_id=vehicle_id)`)

- **Booking Page:**
  - User selects pickup/dropoff locations and dates
  - `calculate-price-button` calculates rental total price
  - `proceed-to-insurance-button` submits booking info and navigates to Insurance Options Page (`url_for('insurance_options', reservation_id=reservation_id)`)

- **Insurance Options Page:**
  - Selecting insurance updates description and price dynamically
  - `confirm-booking-button` confirms booking, writes to rentals and reservations files, then navigates to Reservations Page (`url_for('reservations')`)

- **Rental History Page:**
  - Filters rentals by status via `status-filter`
  - `view-rental-details-{rental_id}` shows rental detail view
  - `back-to-dashboard` navigates back to Dashboard

- **Reservations Page:**
  - `modify-reservation-button-{reservation_id}` opens modify form or page
  - `cancel-reservation-button-{reservation_id}` updates reservation and rental statuses
  - `sort-by-date-button` sorts reservations
  - `back-to-dashboard` navigates back to Dashboard

- **Special Requests Page:**
  - User selects reservation via dropdown
  - User enters special requests and submits via `submit-requests-button`
  - Data updates corresponding reservation's `special_requests` field

- **Locations Page:**
  - `location-detail-button-{location_id}` shows detailed location info
  - `hours-filter` and `search-location-input` filter and search locations
  - `back-to-dashboard` navigates back to Dashboard

---

# Data Storage and File Handling

## Data Directory
All data files are located in the `data/` directory relative to the application base.

## Files, Formats, and Usage

| File Name       | Format (pipe `|` delimited)                                                                                          | Usage Contexts                                     | Operations          |
|-----------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|---------------------|
| vehicles.txt    | `vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status`                                 | Dashboard, Vehicle Search, Vehicle Details        | Read-only           |
| customers.txt   | `customer_id|name|email|phone|driver_license|license_expiry`                                                      | Rentals (joining), Reservations                     | Read-only           |
| locations.txt   | `location_id|city|address|phone|hours|available_vehicles`                                                         | Booking, Locations Page                             | Read-only           |
| rentals.txt     | `rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status`    | Rental History, Booking finalization, Reservations update    | Read & Write        |
| insurance.txt   | `insurance_id|plan_name|description|daily_cost|coverage_limit|deductible`                                        | Insurance Options                                   | Read-only           |
| reservations.txt| `reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests`                            | Reservation Management, Special Requests            | Read & Write        |

## File Access Protocols
- Read files with UTF-8 encoding.
- Parse lines splitting by pipe `|` delimiter.
- Validate record field counts before processing.
- Write files by either overwriting entire contents or appending new lines.
- Use atomic write or file locking strategies to maintain data integrity.

---

# Additional Notes

- The root URL `/` serves as the dashboard page.
- POST method is used for filtering/search and form submissions (booking, special requests, reservation modifications).
- Temporary booking data during flow is managed via session or request parameters, especially for linking booking to insurance selection.
- Customer association is assumed handled externally or via session, as no authentication is required.
- UI consistency, accessibility, and user feedback for actions such as price calculations and booking confirmations are emphasized.

---

This finalized design specification is ready for implementation.
