# CarRental Design Specification

---

## Section 1: Backend Routes and Data Schemas

### 1. Dashboard Page
- **Route:** `/dashboard`
- **Methods:** GET
- **Description:** Fetch featured vehicles (status="Available") from `vehicles.txt` and display current promotions.
- **Request Parameters:** None

---

### 2. Vehicle Search Page
- **Route:** `/vehicles/search`
- **Methods:** GET
- **Query Parameters:** 
  - `location` (optional)
  - `vehicle_type` (optional)
  - `start_date` (optional)
  - `end_date` (optional)
- **Description:** Load available vehicles from `vehicles.txt` (status="Available"), filter by vehicle type and location, filter based on rental date range by checking overlapping bookings in `rentals.txt`.
- **Response:** Filtered vehicle data.

---

### 3. Vehicle Details Page
- **Route:** `/vehicles/<int:vehicle_id>`
- **Methods:** GET
- **Description:** Retrieve vehicle details by `vehicle_id` from `vehicles.txt` including specs (make, model, seats, transmission, fuel type, daily rate). Reviews section can be static or empty.

---

### 4. Booking Page
- **Route:** `/booking`
- **Methods:** POST
- **Request Body (JSON):**
  - `vehicle_id` (int)
  - `pickup_location` (str)
  - `dropoff_location` (str)
  - `pickup_date` (date `YYYY-MM-DD`)
  - `dropoff_date` (date `YYYY-MM-DD`)
  - `customer_id` (int)
- **Business Logic:** Validate vehicle availability from `rentals.txt` within date range, calculate total price (daily_rate * number of days), store temporary booking or return price for confirmation.

---

### 5. Insurance Options Page
- **Route:** `/insurance`
- **Methods:** GET
- **Description:** Fetch insurance plans from `insurance.txt`. Return plan details: name, description, daily cost, coverage limit, deductible.

---

### 6. Confirm Booking with Insurance
- **Route:** `/booking/confirm`
- **Methods:** POST
- **Request Body (JSON):**
  - `vehicle_id` (int)
  - `customer_id` (int)
  - `pickup_location` (str)
  - `dropoff_location` (str)
  - `pickup_date` (date `YYYY-MM-DD`)
  - `dropoff_date` (date `YYYY-MM-DD`)
  - `insurance_id` (int)
  - `special_requests` (str, optional)
- **Business Logic:** Generate new `rental_id` and `reservation_id` by incrementing max existing IDs. Calculate total price as vehicle daily_rate * days + insurance daily_cost * days. Save new rental record with "Active" status to `rentals.txt`. Save reservation including special requests to `reservations.txt`.

---

### 7. Rental History Page
- **Route:** `/rentals/history`
- **Methods:** GET
- **Query Parameters:**
  - `customer_id` (optional)
  - `status` (optional; values: All, Active, Completed, Cancelled)
- **Description:** Load `rentals.txt` filtered by customer and status. Return rental history list.

---

### 8. Reservation Management Page
- **Route:** `/reservations`
- **Methods:** GET, POST, PUT, DELETE
- **GET:**
  - Query Parameter: `customer_id` (optional)
  - Returns current and upcoming reservations from `reservations.txt`, filtered if customer provided.
- **PUT:** `/reservations/<int:reservation_id>`
  - Modify reservation details or cancel; update in `reservations.txt`.
- **DELETE:** `/reservations/<int:reservation_id>`
  - Cancel reservation; update statuses to "Cancelled" in both reservations and rentals files.

---

### 9. Special Requests Page
- **Route:** `/reservations/<int:reservation_id>/special_requests`
- **Methods:** POST
- **Request Body (JSON):** Contains special request fields: driver assistance, GPS, child seat quantity, special notes.
- **Description:** Append or update `special_requests` field in `reservations.txt` for the reservation.

---

### 10. Locations Page
- **Route:** `/locations`
- **Methods:** GET
- **Query Parameters:**
  - `hours` (optional)
  - `search` (optional)
- **Description:** Load locations from `locations.txt`, filter by operating hours and search by city or name. Return location list.

---

## Section 2: Data File Schemas and Formats

### 1. vehicles.txt
- **Fields:** vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int), transmission (str), fuel_type (str), status (str)
- **Delimiter:** `|`
- **Example:**
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

---

### 2. customers.txt
- **Fields:** customer_id (int), name (str), email (str), phone (str), driver_license (str), license_expiry (date `YYYY-MM-DD`)
- **Delimiter:** `|`
- **Example:**
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

---

### 3. locations.txt
- **Fields:** location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)
- **Delimiter:** `|`
- **Example:**
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

---

### 4. rentals.txt
- **Fields:** rental_id (int), vehicle_id (int), customer_id (int), pickup_date (date `YYYY-MM-DD`), dropoff_date (date `YYYY-MM-DD`), pickup_location (str), dropoff_location (str), total_price (float), status (str)
- **Delimiter:** `|`
- **Example:**
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

---

### 5. insurance.txt
- **Fields:** insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (str or float), deductible (float)
- **Delimiter:** `|`
- **Example:**
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

---

### 6. reservations.txt
- **Fields:** reservation_id (int), rental_id (int), vehicle_id (int), customer_id (int), status (str), insurance_id (int), special_requests (str)
- **Delimiter:** `|`
- **Example:**
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

## Section 3: Frontend Templates and Navigation

### 1. Dashboard Page
- **Template Filename:** dashboard.html
- **Page Title:** Car Rental Dashboard
- **Elements:**
  - `dashboard-page` (Div): Main container
  - `featured-vehicles` (Div): Featured vehicle recommendations display
  - `search-vehicles-button` (Button): Navigate to Vehicle Search page
  - `my-reservations-button` (Button): Navigate to Reservations page
  - `promotions-section` (Div): Current promotions display

---

### 2. Vehicle Search Page
- **Template Filename:** vehicle_search.html
- **Page Title:** Search Vehicles
- **Elements:**
  - `search-page` (Div): Main container
  - `location-filter` (Dropdown): Filter by pickup location
  - `vehicle-type-filter` (Dropdown): Filter by vehicle type [Economy, Compact, Sedan, SUV, Luxury]
  - `date-range-input` (Input): Rental date range input
  - `vehicles-grid` (Div): Grid displaying vehicle cards
    - Each vehicle card includes:
      - Vehicle image (img tag, Jinja for loop used, no fixed id)
      - Model and price per day
      - `view-details-button-{vehicle_id}` (Button): View vehicle details

---

### 3. Vehicle Details Page
- **Template Filename:** vehicle_details.html
- **Page Title:** Vehicle Details
- **Elements:**
  - `vehicle-details-page` (Div): Container for details page
  - `vehicle-name` (H1): Vehicle make and model display
  - `vehicle-specs` (Div): Vehicle specifications (engine, seats, transmission)
  - `daily-rate` (Div): Daily rental rate
  - `book-now-button` (Button): Initiate booking process
  - `vehicle-reviews` (Div): Customer reviews section

---

### 4. Booking Page
- **Template Filename:** booking.html
- **Page Title:** Book Your Rental
- **Elements:**
  - `booking-page` (Div): Container
  - `pickup-location` (Dropdown): Pickup location selection
  - `dropoff-location` (Dropdown): Dropoff location selection
  - `pickup-date` (Input): Pickup date selector
  - `dropoff-date` (Input): Dropoff date selector
  - `calculate-price-button` (Button): Compute total rental price
  - `total-price` (Div): Display total price
  - `proceed-to-insurance-button` (Button): Proceed to Insurance Options page

---

### 5. Insurance Options Page
- **Template Filename:** insurance.html
- **Page Title:** Select Insurance Coverage
- **Elements:**
  - `insurance-page` (Div): Container
  - `insurance-options` (Div): Insurance plans display
    - Each plan includes:
      - `select-insurance-{insurance_id}` (Radio): Select insurance radio button
  - `insurance-description` (Div): Description of selected plan
  - `insurance-price` (Div): Price of selected insurance
  - `confirm-booking-button` (Button): Confirm booking with insurance

---

### 6. Rental History Page
- **Template Filename:** rental_history.html
- **Page Title:** Rental History
- **Elements:**
  - `history-page` (Div): Container
  - `rentals-table` (Table): Rental details table (ID, vehicle, dates, location, status)
  - `view-rental-details-{rental_id}` (Button): View rental details
  - `status-filter` (Dropdown): Filter by rental status
  - `back-to-dashboard` (Button): Navigate to Dashboard page

---

### 7. Reservation Management Page
- **Template Filename:** reservations.html
- **Page Title:** My Reservations
- **Elements:**
  - `reservations-page` (Div): Container
  - `reservations-list` (Div): List of reservations
    - Each reservation item includes:
      - `modify-reservation-button-{reservation_id}` (Button): Modify reservation
      - `cancel-reservation-button-{reservation_id}` (Button): Cancel reservation
  - `sort-by-date-button` (Button): Sort reservations
  - `back-to-dashboard` (Button): Navigate to Dashboard

---

### 8. Special Requests Page
- **Template Filename:** special_requests.html
- **Page Title:** Special Requests
- **Elements:**
  - `requests-page` (Div): Container
  - `select-reservation` (Dropdown): Select reservation for requests
  - `driver-assistance-checkbox` (Checkbox): Driver assistance request
  - `gps-option-checkbox` (Checkbox): GPS option
  - `child-seat-quantity` (Input): Number of child seats
  - `special-notes` (Textarea): Additional notes
  - `submit-requests-button` (Button): Submit requests

---

### 9. Locations Page
- **Template Filename:** locations.html
- **Page Title:** Pickup and Dropoff Locations
- **Elements:**
  - `locations-page` (Div): Container
  - `locations-list` (Div): List of locations
    - Each location item has:
      - `location-detail-button-{location_id}` (Button): View location details
  - `hours-filter` (Dropdown): Filter by operating hours
  - `search-location-input` (Input): Search by city or name
  - `back-to-dashboard` (Button): Navigate to Dashboard

---

## Section 4: Navigation and Interaction

### Navigation Flows
- Dashboard page buttons:
  - `search-vehicles-button` -> Vehicle Search Page
  - `my-reservations-button` -> Reservations Page
  - `back-to-dashboard` (where present) -> Dashboard Page
- Vehicle Search:
  - `view-details-button-{vehicle_id}` -> Vehicle Details Page
- Vehicle Details:
  - `book-now-button` -> Booking Page with vehicle context
- Booking:
  - `calculate-price-button` -> Compute and show price
  - `proceed-to-insurance-button` -> Insurance Options Page
- Insurance Options:
  - `confirm-booking-button` -> Confirm booking and navigate to Rental History or Reservations
- Rental History:
  - `view-rental-details-{rental_id}` -> Show rental details
  - `back-to-dashboard` -> Dashboard
- Reservations:
  - `modify-reservation-button-{reservation_id}` -> Modify reservation
  - `cancel-reservation-button-{reservation_id}` -> Cancel reservation
  - `sort-by-date-button` -> Sort reservations
  - `back-to-dashboard` -> Dashboard
- Special Requests:
  - `submit-requests-button` -> Submit and confirm requests
- Locations:
  - `location-detail-button-{location_id}` -> Show location details
  - `back-to-dashboard` -> Dashboard

---

### Dynamic Data Placeholders (Jinja2 Variable Usage)
- Vehicles lists: `{% for vehicle in vehicles %}`, vehicle attributes via `vehicle.id`, `vehicle.make`, `vehicle.model`, `vehicle.daily_rate`.
- Locations: `{% for location in locations %}`
- Reservations and Rentals: `{% for reservation in reservations %}` or `{% for rental in rentals %}`
- Insurance options: `{% for plan in insurance_plans %}`
- Special requests: Populate `select-reservation` dropdown with reservation IDs.

---

# End of CarRental Design Specification
