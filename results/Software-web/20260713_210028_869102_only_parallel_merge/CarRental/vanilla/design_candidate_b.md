# CarRental Flask Web Application Design Candidate

---

## Flask Routes and HTTP Methods

### 1. Dashboard Page
- URL Path: `/` or `/dashboard`
- Methods: GET
- View Function: `dashboard()`

### 2. Vehicle Search Page
- URL Path: `/vehicles/search`
- Methods: GET (for display), POST (for filter/search postback)
- View Function: `vehicle_search()`

### 3. Vehicle Details Page
- URL Path: `/vehicles/<int:vehicle_id>`
- Methods: GET
- View Function: `vehicle_details(vehicle_id)`

### 4. Booking Page
- URL Path: `/booking/<int:vehicle_id>`
- Methods: GET (display booking form), POST (submit booking details)
- View Function: `booking(vehicle_id)`

### 5. Insurance Options Page
- URL Path: `/insurance/<int:reservation_id>`
- Methods: GET (display options), POST (select insurance and confirm booking)
- View Function: `insurance_options(reservation_id)`

### 6. Rental History Page
- URL Path: `/history`
- Methods: GET
- View Function: `rental_history()`

### 7. Reservation Management Page
- URL Path: `/reservations`
- Methods: GET
- View Function: `reservations()`

### 8. Special Requests Page
- URL Path: `/requests`
- Methods: GET (display form), POST (submit special requests)
- View Function: `special_requests()`

### 9. Locations Page
- URL Path: `/locations`
- Methods: GET
- View Function: `locations()`

---

## Page Titles and Container Element IDs

| Page                     | Page Title                 | Container ID            |
|--------------------------|----------------------------|------------------------|
| Dashboard                | Car Rental Dashboard        | dashboard-page         |
| Vehicle Search           | Search Vehicles             | search-page            |
| Vehicle Details          | Vehicle Details             | vehicle-details-page   |
| Booking                  | Book Your Rental            | booking-page           |
| Insurance Options        | Select Insurance Coverage   | insurance-page         |
| Rental History           | Rental History              | history-page           |
| Reservation Management   | My Reservations             | reservations-page      |
| Special Requests         | Special Requests            | requests-page          |
| Locations                | Pickup and Dropoff Locations| locations-page         |

---

## Element IDs and Notes by Page

### Dashboard Page
- **dashboard-page**: main container div
- **featured-vehicles**: div displaying featured vehicle recommendations
- **search-vehicles-button**: button navigates to `/vehicles/search`
- **my-reservations-button**: button navigates to `/reservations`
- **promotions-section**: div for current promotions/offers

### Vehicle Search Page
- **search-page**: main container div
- **location-filter**: dropdown to filter vehicles by pickup location
- **vehicle-type-filter**: dropdown with options Economy, Compact, Sedan, SUV, Luxury
- **date-range-input**: input field for rental date range (e.g., start and end dates)
- **vehicles-grid**: div displaying vehicle cards
- **view-details-button-{vehicle_id}**: dynamic button for each vehicle to navigate to vehicle details `/vehicles/<vehicle_id>`

### Vehicle Details Page
- **vehicle-details-page**: main container div
- **vehicle-name**: h1 element showing vehicle make and model
- **vehicle-specs**: div showing specs such as engine, seats, transmission
- **daily-rate**: div showing daily rental rate
- **book-now-button**: button navigating to `/booking/<vehicle_id>`
- **vehicle-reviews**: div displaying customer reviews

### Booking Page
- **booking-page**: main container div
- **pickup-location**: dropdown for pickup location
- **dropoff-location**: dropdown for dropoff location
- **pickup-date**: input for pickup date
- **dropoff-date**: input for dropoff date
- **calculate-price-button**: button triggers price calculation based on date range and daily rate
- **total-price**: div displaying calculated total price
- **proceed-to-insurance-button**: button navigates to `/insurance/<reservation_id>` after booking info submission

### Insurance Options Page
- **insurance-page**: main container div
- **insurance-options**: div displaying all insurance plans
- **select-insurance-{insurance_id}**: dynamic radio button per insurance plan
- **insurance-description**: div showing description of selected insurance
- **insurance-price**: div showing price (daily cost * rental duration)
- **confirm-booking-button**: button to confirm booking and finalize reservation

### Rental History Page
- **history-page**: main container div
- **rentals-table**: table listing rentals with columns: ID, vehicle, dates, location, status
- **view-rental-details-{rental_id}**: dynamic button to view details for each rental
- **status-filter**: dropdown filtering rentals by status (All, Active, Completed, Cancelled)
- **back-to-dashboard**: button to navigate back to `/dashboard`

### Reservation Management Page
- **reservations-page**: main container div
- **reservations-list**: div listing all reservations
- **modify-reservation-button-{reservation_id}**: dynamic button to modify reservation
- **cancel-reservation-button-{reservation_id}**: dynamic button to cancel reservation
- **sort-by-date-button**: button to sort reservations by date
- **back-to-dashboard**: button to navigate to `/dashboard`

### Special Requests Page
- **requests-page**: main container div
- **select-reservation**: dropdown to select a reservation for adding special requests
- **driver-assistance-checkbox**: checkbox for driver assistance
- **gps-option-checkbox**: checkbox for GPS option
- **child-seat-quantity**: input field for number of child seats
- **special-notes**: textarea field for additional notes
- **submit-requests-button**: button to submit special requests

### Locations Page
- **locations-page**: main container div
- **locations-list**: div listing all rental locations
- **location-detail-button-{location_id}**: dynamic button to view details for each location
- **hours-filter**: dropdown to filter by hours (24/7, Business Hours, Weekend)
- **search-location-input**: input field to search locations by city or name
- **back-to-dashboard**: button to navigate to `/dashboard`

---

## Navigation and User Interaction Flow

- **Dashboard**:
  - `search-vehicles-button` &rarr; Vehicle Search Page (`url_for('vehicle_search')`)
  - `my-reservations-button` &rarr; Reservations Page (`url_for('reservations')`)
  - other featured vehicle or promotion links as applicable

- **Vehicle Search Page**:
  - Filtering uses POST or AJAX to refresh vehicle listings
  - `view-details-button-{vehicle_id}` &rarr; Vehicle Details Page (`url_for('vehicle_details', vehicle_id=vehicle_id)`)

- **Vehicle Details Page**:
  - `book-now-button` &rarr; Booking Page (`url_for('booking', vehicle_id=vehicle_id)`)

- **Booking Page**:
  - After entering pickup/dropoff and dates, `calculate-price-button` calculates and updates `total-price`
  - `proceed-to-insurance-button` creates reservation and navigates to Insurance Options Page (`url_for('insurance_options', reservation_id=reservation_id)`)

- **Insurance Options Page**:
  - Selecting radio buttons changes insurance description and price dynamically
  - `confirm-booking-button` finalizes booking, saves data, and navigates to Reservations Page (`url_for('reservations')`)

- **Rental History Page**:
  - `status-filter` filters displayed rentals
  - `view-rental-details-{rental_id}` shows detailed info about the rental
  - `back-to-dashboard` returns to Dashboard

- **Reservations Page**:
  - `modify-reservation-button-{reservation_id}` &rarr; Modify reservation form (possibly reopening Booking Page or a dedicated route)
  - `cancel-reservation-button-{reservation_id}` updates data and refreshes list
  - `sort-by-date-button` sorts reservation list
  - `back-to-dashboard` returns to Dashboard

- **Special Requests Page**:
  - User selects reservation via dropdown
  - User marks checkboxes and fills quantities/notes
  - `submit-requests-button` saves special requests and confirms action

- **Locations Page**:
  - `location-detail-button-{location_id}` navigates or expands to show details
  - `hours-filter` and `search-location-input` filter locations displayed
  - `back-to-dashboard` returns to Dashboard

---

## Data Storage and File Handling

All data files are under the `data/` directory relative to the application base.

### 1. Vehicles Data (`vehicles.txt`)
- Read for Vehicle Search, Vehicle Details
- Format per line: `vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status`
- Read entire file into data structures for filtering and display
- Updates occur rarely; primarily read-only

### 2. Customers Data (`customers.txt`)
- Required for association with bookings and rentals
- Format per line: `customer_id|name|email|phone|driver_license|license_expiry`
- Read for user context (no auth mandated, so association assumed by session or passed parameters)

### 3. Locations Data (`locations.txt`)
- Used for location selections in Booking, Vehicle Search filters, and Locations Page
- Format per line: `location_id|city|address|phone|hours|available_vehicles`
- Read to populate dropdowns and display lists

### 4. Rentals Data (`rentals.txt`)
- Read and write for rental history, booking confirmations
- Format per line: `rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status`
- Read all into data structures for display/filter
- Append new rentals after booking confirmation
- Update status on cancellations or completions

### 5. Insurance Data (`insurance.txt`)
- Read for Insurance Options Page
- Format per line: `insurance_id|plan_name|description|daily_cost|coverage_limit|deductible`
- Used to display options and calculate insurance price

### 6. Reservations Data (`reservations.txt`)
- Read and write for reservations management
- Format per line: `reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests`
- Append new reservations upon booking with insurance
- Update reservation status on cancellation or modification

### File Read and Write Specifications
- Read files by opening with UTF-8 encoding
- Parse lines splitting by pipe `|` delimiter
- Validate data field counts before processing
- Write files by overwriting entire content or appending lines
- Maintain data consistency and avoid file corruption by locking or atomic writes as per implementation

---

This design fully outlines the Flask route structure, UI elements with precise IDs, navigation flows, and detailed data management for the CarRental application as specified.
