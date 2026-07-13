# Requirements Analysis for 'CarRental' Web Application

---

## 1. Page Structures

### 1. Dashboard Page
- **Page Title:** Car Rental Dashboard
- **Overview:** Main hub displaying featured vehicles, current promotions, and quick navigation to all functionalities.
- **Elements:**
  - `dashboard-page` (Div): Container for the dashboard page.
  - `featured-vehicles` (Div): Displays featured vehicle recommendations.
  - `search-vehicles-button` (Button): Button to navigate to Vehicle Search page.
  - `my-reservations-button` (Button): Button to navigate to Reservation Management page.
  - `promotions-section` (Div): Displays current promotions and offers.

### 2. Vehicle Search Page
- **Page Title:** Search Vehicles
- **Overview:** Displays all available vehicles with search and filter capabilities.
- **Elements:**
  - `search-page` (Div): Container for the search page.
  - `location-filter` (Dropdown): Filter vehicles by pickup location.
  - `vehicle-type-filter` (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - `date-range-input` (Input): Select rental date range.
  - `vehicles-grid` (Div): Grid displaying vehicle cards each with image, model, and price per day.
  - `view-details-button-{vehicle_id}` (Button): Button on each vehicle card to view detailed information.

### 3. Vehicle Details Page
- **Page Title:** Vehicle Details
- **Overview:** Shows detailed info of a specific vehicle.
- **Elements:**
  - `vehicle-details-page` (Div): Container for vehicle details.
  - `vehicle-name` (H1): Vehicle name and model display.
  - `vehicle-specs` (Div): Vehicle specifications including engine, seats, transmission.
  - `daily-rate` (Div): Display of daily rental rate.
  - `book-now-button` (Button): Button to book the vehicle.
  - `vehicle-reviews` (Div): Section showing customer reviews.

### 4. Booking Page
- **Page Title:** Book Your Rental
- **Overview:** Complete rental booking with dates and location selection.
- **Elements:**
  - `booking-page` (Div): Container for booking page.
  - `pickup-location` (Dropdown): Select pickup location.
  - `dropoff-location` (Dropdown): Select dropoff location.
  - `pickup-date` (Input): Select pickup date.
  - `dropoff-date` (Input): Select dropoff date.
  - `calculate-price-button` (Button): Calculate total rental price.
  - `total-price` (Div): Display calculated price.
  - `proceed-to-insurance-button` (Button): Proceed to insurance selection.

### 5. Insurance Options Page
- **Page Title:** Select Insurance Coverage
- **Overview:** Select insurance coverage options.
- **Elements:**
  - `insurance-page` (Div): Container for insurance page.
  - `insurance-options` (Div): Display available insurance plans.
  - `select-insurance-{insurance_id}` (Radio): Radio button for insurance plan selection.
  - `insurance-description` (Div): Description of selected plan.
  - `insurance-price` (Div): Display insurance price.
  - `confirm-booking-button` (Button): Confirm booking with insurance selection.

### 6. Rental History Page
- **Page Title:** Rental History
- **Overview:** Displays all previous rentals with details and status.
- **Elements:**
  - `history-page` (Div): Container for rental history.
  - `rentals-table` (Table): Table listing rentals with ID, vehicle, dates, location, status.
  - `view-rental-details-{rental_id}` (Button): View details of a rental.
  - `status-filter` (Dropdown): Filter rentals by status (All, Active, Completed, Cancelled).
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

### 7. Reservation Management Page
- **Page Title:** My Reservations
- **Overview:** Displays current and upcoming reservations with management options.
- **Elements:**
  - `reservations-page` (Div): Container for reservations management.
  - `reservations-list` (Div): List of reservations with vehicle, dates, status.
  - `modify-reservation-button-{reservation_id}` (Button): Modify a reservation.
  - `cancel-reservation-button-{reservation_id}` (Button): Cancel a reservation.
  - `sort-by-date-button` (Button): Sort reservations by date.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

### 8. Special Requests Page
- **Page Title:** Special Requests
- **Overview:** Allows users to add special requests to rental bookings.
- **Elements:**
  - `requests-page` (Div): Container for special requests page.
  - `select-reservation` (Dropdown): Select reservation to add requests.
  - `driver-assistance-checkbox` (Checkbox): Driver assistance request option.
  - `gps-option-checkbox` (Checkbox): GPS option.
  - `child-seat-quantity` (Input): Specify number of child seats.
  - `special-notes` (Textarea): Enter special notes or requests.
  - `submit-requests-button` (Button): Submit special requests.

### 9. Locations Page
- **Page Title:** Pickup and Dropoff Locations
- **Overview:** Displays all rental pickup and dropoff locations.
- **Elements:**
  - `locations-page` (Div): Container for locations page.
  - `locations-list` (Div): List of all rental locations with address and hours.
  - `location-detail-button-{location_id}` (Button): View location details.
  - `hours-filter` (Dropdown): Filter by operating hours (24/7, Business Hours, Weekend).
  - `search-location-input` (Input): Search locations by city or name.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.


## 2. Data Storage

All data files reside under `data/` directory and are pipe-delimited text files.

### 1. Vehicles Data
- **Filename:** vehicles.txt
- **Format:** vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- **Example:**
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. Customers Data
- **Filename:** customers.txt
- **Format:** customer_id|name|email|phone|driver_license|license_expiry
- **Example:**
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. Locations Data
- **Filename:** locations.txt
- **Format:** location_id|city|address|phone|hours|available_vehicles
- **Example:**
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. Rentals Data
- **Filename:** rentals.txt
- **Format:** rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- **Example:**
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. Insurance Data
- **Filename:** insurance.txt
- **Format:** insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- **Example:**
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. Reservations Data
- **Filename:** reservations.txt
- **Format:** reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- **Example:**
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```


## 3. Navigation and Interaction Flows

- The website starts at the **Dashboard Page** (`dashboard-page`).
- From Dashboard:
  - `search-vehicles-button` navigates to Vehicle Search Page.
  - `my-reservations-button` navigates to Reservation Management Page.
  - `back-to-dashboard` buttons present in Rental History, Reservation Management, Locations pages navigate back here.

- From Vehicle Search Page:
  - Clicking `view-details-button-{vehicle_id}` navigates to Vehicle Details Page for that vehicle.

- From Vehicle Details Page:
  - Clicking `book-now-button` opens Booking Page.

- From Booking Page:
  - After filling pickup/dropoff and dates, clicking `calculate-price-button` calculates cost displayed in `total-price`.
  - Clicking `proceed-to-insurance-button` navigates to Insurance Options Page.

- From Insurance Options Page:
  - Selecting insurance via `select-insurance-{insurance_id}` updates details and price.
  - Clicking `confirm-booking-button` confirms the booking and presumably stores it.

- From Rental History Page:
  - Use `status-filter` to filter rentals.
  - Clicking `view-rental-details-{rental_id}` shows rental details.
  - `back-to-dashboard` navigates to Dashboard.

- From Reservation Management Page:
  - `modify-reservation-button-{reservation_id}` allows modifications.
  - `cancel-reservation-button-{reservation_id}` cancels a reservation.
  - `sort-by-date-button` sorts reservations.
  - `back-to-dashboard` navigates to Dashboard.

- From Special Requests Page:
  - Select reservation via `select-reservation` dropdown.
  - Fill checkboxes and inputs for assistance, GPS, child seat, and notes.
  - `submit-requests-button` submits the requests.

- From Locations Page:
  - Filter locations by `hours-filter` and search by `search-location-input`.
  - View location details with `location-detail-button-{location_id}`.
  - `back-to-dashboard` navigates to Dashboard.

---

**End of Requirements Analysis**