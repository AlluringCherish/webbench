# CarRental Application Design Specification

## 1. Page Designs and Element IDs

### 1. Dashboard Page
- Page Title: Car Rental Dashboard
- Container ID: dashboard-page
- Elements:
  - featured-vehicles (Div)
  - search-vehicles-button (Button)
  - my-reservations-button (Button)
  - promotions-section (Div)

### 2. Vehicle Search Page
- Page Title: Search Vehicles
- Container ID: search-page
- Elements:
  - location-filter (Dropdown)
  - vehicle-type-filter (Dropdown)
  - date-range-input (Input)
  - vehicles-grid (Div)
  - view-details-button-{vehicle_id} (Button) [Dynamic per vehicle]

### 3. Vehicle Details Page
- Page Title: Vehicle Details
- Container ID: vehicle-details-page
- Elements:
  - vehicle-name (H1)
  - vehicle-specs (Div)
  - daily-rate (Div)
  - book-now-button (Button)
  - vehicle-reviews (Div)

### 4. Booking Page
- Page Title: Book Your Rental
- Container ID: booking-page
- Elements:
  - pickup-location (Dropdown)
  - dropoff-location (Dropdown)
  - pickup-date (Input)
  - dropoff-date (Input)
  - calculate-price-button (Button)
  - total-price (Div)
  - proceed-to-insurance-button (Button)

### 5. Insurance Options Page
- Page Title: Select Insurance Coverage
- Container ID: insurance-page
- Elements:
  - insurance-options (Div)
  - select-insurance-{insurance_id} (Radio) [Dynamic per insurance plan]
  - insurance-description (Div)
  - insurance-price (Div)
  - confirm-booking-button (Button)

### 6. Rental History Page
- Page Title: Rental History
- Container ID: history-page
- Elements:
  - rentals-table (Table)
  - view-rental-details-{rental_id} (Button) [Dynamic per rental]
  - status-filter (Dropdown)
  - back-to-dashboard (Button)

### 7. Reservation Management Page
- Page Title: My Reservations
- Container ID: reservations-page
- Elements:
  - reservations-list (Div)
  - modify-reservation-button-{reservation_id} (Button) [Dynamic per reservation]
  - cancel-reservation-button-{reservation_id} (Button) [Dynamic per reservation]
  - sort-by-date-button (Button)
  - back-to-dashboard (Button)

### 8. Special Requests Page
- Page Title: Special Requests
- Container ID: requests-page
- Elements:
  - select-reservation (Dropdown)
  - driver-assistance-checkbox (Checkbox)
  - gps-option-checkbox (Checkbox)
  - child-seat-quantity (Input)
  - special-notes (Textarea)
  - submit-requests-button (Button)

### 9. Locations Page
- Page Title: Pickup and Dropoff Locations
- Container ID: locations-page
- Elements:
  - locations-list (Div)
  - location-detail-button-{location_id} (Button) [Dynamic per location]
  - hours-filter (Dropdown)
  - search-location-input (Input)
  - back-to-dashboard (Button)


## 2. Navigation and User Flows

The navigation flow starts from the Dashboard Page. All pages are publicly accessible with no authentication.

- **Dashboard Page**
  - Buttons:
    - search-vehicles-button => Vehicle Search Page
    - my-reservations-button => Reservation Management Page
    - Back navigation to Dashboard from pages with back-to-dashboard buttons.

- **Vehicle Search Page**
  - view-details-button-{vehicle_id} => Vehicle Details Page (shows selected vehicle)
  - Back to Dashboard via browser or UI not explicitly specified (recommended to add button as needed)

- **Vehicle Details Page**
  - book-now-button => Booking Page (for selected vehicle)
  - Back to Vehicle Search Page via browser or app logic

- **Booking Page**
  - calculate-price-button calculates price on current input
  - proceed-to-insurance-button => Insurance Options Page (passes booking info and vehicle)
  - Back to Vehicle Details Page via browser or app logic

- **Insurance Options Page**
  - confirm-booking-button => Completion (store booking with insurance)
  - Back to Booking Page via browser or app logic

- **Rental History Page**
  - view-rental-details-{rental_id} shows detailed rental info (could be modal or new page)
  - status-filter filters the rentals displayed
  - back-to-dashboard => Dashboard Page

- **Reservation Management Page**
  - modify-reservation-button-{reservation_id} => Modify reservation workflow
  - cancel-reservation-button-{reservation_id} => Cancel reservation functionality
  - sort-by-date-button sorts reservation list
  - back-to-dashboard => Dashboard Page

- **Special Requests Page**
  - submit-requests-button submits special requests for the selected reservation
  - Navigation into this page assumed from reservation management or booking confirmation (not explicitly listed but logically linked in UI)

- **Locations Page**
  - location-detail-button-{location_id} => shows location details
  - hours-filter filters locations by operating hours
  - search-location-input filters locations by name or city
  - back-to-dashboard => Dashboard Page


## 3. Data File Storage and Formats

The application stores data in local text files in a 'data' directory.

### Vehicles Data
- File: data/vehicles.txt
- Format: vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Example:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### Customers Data
- File: data/customers.txt
- Format: customer_id|name|email|phone|driver_license|license_expiry
- Example:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### Locations Data
- File: data/locations.txt
- Format: location_id|city|address|phone|hours|available_vehicles
- Example:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### Rentals Data
- File: data/rentals.txt
- Format: rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Example:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### Insurance Data
- File: data/insurance.txt
- Format: insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Example:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### Reservations Data
- File: data/reservations.txt
- Format: reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Example:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```
