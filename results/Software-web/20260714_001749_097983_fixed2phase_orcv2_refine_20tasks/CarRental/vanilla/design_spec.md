# CarRental Application Design Specification

## Section 1: Page Designs and Element IDs

### 1. Dashboard Page
- Page Title: Car Rental Dashboard
- Container Div ID: `dashboard-page`
- Elements:
  - Featured Vehicles Div: `featured-vehicles`
  - Search Vehicles Button: `search-vehicles-button`
  - My Reservations Button: `my-reservations-button`
  - Promotions Section Div: `promotions-section`

### 2. Vehicle Search Page
- Page Title: Search Vehicles
- Container Div ID: `search-page`
- Elements:
  - Location Filter Dropdown: `location-filter`
  - Vehicle Type Filter Dropdown: `vehicle-type-filter` (Options: Economy, Compact, Sedan, SUV, Luxury)
  - Date Range Input Field: `date-range-input`
  - Vehicles Grid Div: `vehicles-grid`
  - View Details Button per vehicle: `view-details-button-{vehicle_id}`

### 3. Vehicle Details Page
- Page Title: Vehicle Details
- Container Div ID: `vehicle-details-page`
- Elements:
  - Vehicle Name H1: `vehicle-name`
  - Vehicle Specifications Div: `vehicle-specs` (engine, seats, transmission)
  - Daily Rate Div: `daily-rate`
  - Book Now Button: `book-now-button`
  - Vehicle Reviews Div: `vehicle-reviews`

### 4. Booking Page
- Page Title: Book Your Rental
- Container Div ID: `booking-page`
- Elements:
  - Pickup Location Dropdown: `pickup-location`
  - Dropoff Location Dropdown: `dropoff-location`
  - Pickup Date Input: `pickup-date`
  - Dropoff Date Input: `dropoff-date`
  - Calculate Price Button: `calculate-price-button`
  - Total Price Div: `total-price`
  - Proceed to Insurance Button: `proceed-to-insurance-button`

### 5. Insurance Options Page
- Page Title: Select Insurance Coverage
- Container Div ID: `insurance-page`
- Elements:
  - Insurance Options Div: `insurance-options`
  - Select Insurance Radio per plan: `select-insurance-{insurance_id}`
  - Insurance Description Div: `insurance-description`
  - Insurance Price Div: `insurance-price`
  - Confirm Booking Button: `confirm-booking-button`

### 6. Rental History Page
- Page Title: Rental History
- Container Div ID: `history-page`
- Elements:
  - Rentals Table: `rentals-table` (Columns: ID, Vehicle, Dates, Location, Status)
  - View Rental Details Button per rental: `view-rental-details-{rental_id}`
  - Status Filter Dropdown: `status-filter` (Options: All, Active, Completed, Cancelled)
  - Back to Dashboard Button: `back-to-dashboard`

### 7. Reservation Management Page
- Page Title: My Reservations
- Container Div ID: `reservations-page`
- Elements:
  - Reservations List Div: `reservations-list`
  - Modify Reservation Button per reservation: `modify-reservation-button-{reservation_id}`
  - Cancel Reservation Button per reservation: `cancel-reservation-button-{reservation_id}`
  - Sort by Date Button: `sort-by-date-button`
  - Back to Dashboard Button: `back-to-dashboard`

### 8. Special Requests Page
- Page Title: Special Requests
- Container Div ID: `requests-page`
- Elements:
  - Select Reservation Dropdown: `select-reservation`
  - Driver Assistance Checkbox: `driver-assistance-checkbox`
  - GPS Option Checkbox: `gps-option-checkbox`
  - Child Seat Quantity Input: `child-seat-quantity`
  - Special Notes Textarea: `special-notes`
  - Submit Requests Button: `submit-requests-button`

### 9. Locations Page
- Page Title: Pickup and Dropoff Locations
- Container Div ID: `locations-page`
- Elements:
  - Locations List Div: `locations-list`
  - Location Detail Button per location: `location-detail-button-{location_id}`
  - Hours Filter Dropdown: `hours-filter` (Options: 24/7, Business Hours, Weekend)
  - Search Location Input: `search-location-input`
  - Back to Dashboard Button: `back-to-dashboard`

---

## Section 2: Navigation and User Flows

- **Starting Point:** Dashboard Page (`dashboard-page`)

- From **Dashboard Page**:
  - `search-vehicles-button` -> Vehicle Search Page (`search-page`)
  - `my-reservations-button` -> Reservation Management Page (`reservations-page`)
  - Navigation to Locations Page or Rental History Page can also be linked from Dashboard if needed (not explicitly specified but may be linked via promotions or navigation bar in UI).

- From **Vehicle Search Page**:
  - `view-details-button-{vehicle_id}` -> Vehicle Details Page (`vehicle-details-page`) displaying the selected vehicle details.

- From **Vehicle Details Page**:
  - `book-now-button` -> Booking Page (`booking-page`) with selected vehicle context.

- From **Booking Page**:
  - `calculate-price-button` -> Dynamically calculate and display price in `total-price` div.
  - `proceed-to-insurance-button` -> Insurance Options Page (`insurance-page`).

- From **Insurance Options Page**:
  - Selecting an insurance plan radio `select-insurance-{insurance_id}` updates `insurance-description` and `insurance-price`.
  - `confirm-booking-button` finalizes booking and may redirect to Reservation Management Page or Dashboard.

- From **Rental History Page**:
  - `view-rental-details-{rental_id}` -> Show detailed rental information (likely a modal or a separate detail page not specified).
  - `status-filter` dynamically filters rentals shown.
  - `back-to-dashboard` -> Dashboard Page

- From **Reservation Management Page**:
  - `modify-reservation-button-{reservation_id}` -> Initiates modification flow for a reservation.
  - `cancel-reservation-button-{reservation_id}` -> Cancels the selected reservation.
  - `sort-by-date-button` -> Sort the reservation list by date.
  - `back-to-dashboard` -> Dashboard Page

- From **Special Requests Page**:
  - User selects a reservation (`select-reservation` dropdown) and adds special requests.
  - `submit-requests-button` submits and stores special requests.

- From **Locations Page**:
  - `location-detail-button-{location_id}` shows detailed info of location.
  - `hours-filter` filters locations by operating hours.
  - `search-location-input` filters locations by city or name.
  - `back-to-dashboard` -> Dashboard Page

---

## Section 3: Data File Storage and Formats

### 1. Vehicles Data
- File Name: `vehicles.txt`
- Format: pipe-separated values (PSV)
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
```
- Example:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

### 2. Customers Data
- File Name: `customers.txt`
- Format:
```
customer_id|name|email|phone|driver_license|license_expiry
```
- Example:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

### 3. Locations Data
- File Name: `locations.txt`
- Format:
```
location_id|city|address|phone|hours|available_vehicles
```
- Example:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

### 4. Rentals Data
- File Name: `rentals.txt`
- Format:
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
```
- Example:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

### 5. Insurance Data
- File Name: `insurance.txt`
- Format:
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
```
- Example:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

### 6. Reservations Data
- File Name: `reservations.txt`
- Format:
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
```
- Example:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

This concludes the comprehensive design specification for the CarRental web application as per the provided requirements.
