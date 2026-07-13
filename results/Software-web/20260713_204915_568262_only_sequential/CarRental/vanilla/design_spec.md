# Design Specification for CarRental Flask Application

---

## 1. Page Definitions

### 1. Dashboard Page
- **Route:** `/` (GET)
- **Page Title:** Car Rental Dashboard
- **Container:** `dashboard-page` (Div)
- **Elements:**
  - `featured-vehicles` (Div): Displays featured vehicle recommendations.
  - `search-vehicles-button` (Button): Navigates to Vehicle Search page (`/search-vehicles`).
  - `my-reservations-button` (Button): Navigates to Reservation Management page (`/my-reservations`).
  - `promotions-section` (Div): Displays current promotions and offers.

---

### 2. Vehicle Search Page
- **Route:** `/search-vehicles` (GET)
- **Page Title:** Search Vehicles
- **Container:** `search-page` (Div)
- **Elements:**
  - `location-filter` (Dropdown): Filter vehicles by pickup location.
  - `vehicle-type-filter` (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - `date-range-input` (Input): Select rental date range.
  - `vehicles-grid` (Div): Displays vehicle cards.
  - Vehicle Card Buttons:
    - `view-details-button-{vehicle_id}` (Button): For each vehicle, navigates to Vehicle Details page (`/vehicle-details/{vehicle_id}`).

---

### 3. Vehicle Details Page
- **Route:** `/vehicle-details/<vehicle_id>` (GET)
- **Page Title:** Vehicle Details
- **Container:** `vehicle-details-page` (Div)
- **Elements:**
  - `vehicle-name` (H1): Displays vehicle name and model.
  - `vehicle-specs` (Div): Engine, seats, transmission specs.
  - `daily-rate` (Div): Daily rental price.
  - `book-now-button` (Button): Navigates to Booking page (`/booking/{vehicle_id}`).
  - `vehicle-reviews` (Div): Customer reviews section.

---

### 4. Booking Page
- **Route:** `/booking/<vehicle_id>` (GET, POST)
- **Page Title:** Book Your Rental
- **Container:** `booking-page` (Div)
- **Elements:**
  - `pickup-location` (Dropdown): Pickup location selection.
  - `dropoff-location` (Dropdown): Dropoff location selection.
  - `pickup-date` (Input): Pickup date picker.
  - `dropoff-date` (Input): Dropoff date picker.
  - `calculate-price-button` (Button): Calculates total price.
  - `total-price` (Div): Displays calculated rental price.
  - `proceed-to-insurance-button` (Button): Navigates to Insurance Options page (`/insurance-options`).

---

### 5. Insurance Options Page
- **Route:** `/insurance-options` (GET, POST)
- **Page Title:** Select Insurance Coverage
- **Container:** `insurance-page` (Div)
- **Elements:**
  - `insurance-options` (Div): Displays insurance plans.
  - Insurance Plan Inputs:
    - `select-insurance-{insurance_id}` (Radio): Select insurance plan.
  - `insurance-description` (Div): Description of selected insurance.
  - `insurance-price` (Div): Price of the insurance.
  - `confirm-booking-button` (Button): Confirms booking and stores data.

---

### 6. Rental History Page
- **Route:** `/rental-history` (GET)
- **Page Title:** Rental History
- **Container:** `history-page` (Div)
- **Elements:**
  - `rentals-table` (Table): Lists rentals with columns for ID, vehicle, dates, locations, status.
  - `view-rental-details-{rental_id}` (Button): View rental details.
  - `status-filter` (Dropdown): Filter rentals by status (All, Active, Completed, Cancelled).
  - `back-to-dashboard` (Button): Navigates back to Dashboard (`/`).

---

### 7. Reservation Management Page
- **Route:** `/my-reservations` (GET)
- **Page Title:** My Reservations
- **Container:** `reservations-page` (Div)
- **Elements:**
  - `reservations-list` (Div): Lists reservations with vehicle, dates, status.
  - `modify-reservation-button-{reservation_id}` (Button): Modify reservation.
  - `cancel-reservation-button-{reservation_id}` (Button): Cancel reservation.
  - `sort-by-date-button` (Button): Sort reservations by date.
  - `back-to-dashboard` (Button): Navigate back to Dashboard (`/`).

---

### 8. Special Requests Page
- **Route:** `/special-requests` (GET, POST)
- **Page Title:** Special Requests
- **Container:** `requests-page` (Div)
- **Elements:**
  - `select-reservation` (Dropdown): Select reservation to add special requests.
  - `driver-assistance-checkbox` (Checkbox): Driver assistance option.
  - `gps-option-checkbox` (Checkbox): GPS option.
  - `child-seat-quantity` (Input): Number of child seats.
  - `special-notes` (Textarea): Additional notes.
  - `submit-requests-button` (Button): Submit special requests.

---

### 9. Locations Page
- **Route:** `/locations` (GET)
- **Page Title:** Pickup and Dropoff Locations
- **Container:** `locations-page` (Div)
- **Elements:**
  - `locations-list` (Div): List all rental locations.
  - `location-detail-button-{location_id}` (Button): View location details.
  - `hours-filter` (Dropdown): Filter locations by operating hours (24/7, Business Hours, Weekend).
  - `search-location-input` (Input): Search locations by city or name.
  - `back-to-dashboard` (Button): Navigate back to Dashboard (`/`).

---

## 2. Data File Schemas (under `data/` directory)

### 1. vehicles.txt
- **Fields:** vehicle_id | make | model | vehicle_type | daily_rate | seats | transmission | fuel_type | status
- **Description:** Stores vehicle details and availability.
- **Sample Data:**
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

### 2. customers.txt
- **Fields:** customer_id | name | email | phone | driver_license | license_expiry
- **Description:** Customer personal and license information.
- **Sample Data:**
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

### 3. locations.txt
- **Fields:** location_id | city | address | phone | hours | available_vehicles
- **Description:** Rental locations details including operating hours.
- **Sample Data:**
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

### 4. rentals.txt
- **Fields:** rental_id | vehicle_id | customer_id | pickup_date | dropoff_date | pickup_location | dropoff_location | total_price | status
- **Description:** Records of vehicle rentals and their statuses.
- **Sample Data:**
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

### 5. insurance.txt
- **Fields:** insurance_id | plan_name | description | daily_cost | coverage_limit | deductible
- **Description:** Insurance plan details.
- **Sample Data:**
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

### 6. reservations.txt
- **Fields:** reservation_id | rental_id | vehicle_id | customer_id | status | insurance_id | special_requests
- **Description:** Reservation information linked to rentals, vehicles, insurance.
- **Sample Data:**
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

## 3. Navigation Mappings

- **Start page:** Dashboard (`/`)

### From Dashboard
- `search-vehicles-button` → `/search-vehicles`
- `my-reservations-button` → `/my-reservations`

### From Vehicle Search Page
- `view-details-button-{vehicle_id}` → `/vehicle-details/{vehicle_id}`

### From Vehicle Details Page
- `book-now-button` → `/booking/{vehicle_id}`

### From Booking Page
- `calculate-price-button` → triggers backend price calculation (no navigation)
- `proceed-to-insurance-button` → `/insurance-options`

### From Insurance Options Page
- `select-insurance-{insurance_id}` → updates insurance details dynamically (no navigation)
- `confirm-booking-button` → completes booking process (POST) and redirects to Dashboard or confirmation page

### From Rental History Page
- `view-rental-details-{rental_id}` → detailed rental view or modal (implementation detail)
- `back-to-dashboard` → `/`
- Filter via `status-filter` updates rentals view dynamically

### From Reservation Management Page
- `modify-reservation-button-{reservation_id}` → reservation modification endpoint (implementation detail)
- `cancel-reservation-button-{reservation_id}` → reservation cancellation endpoint (implementation detail)
- `sort-by-date-button` → sorts reservation list dynamically
- `back-to-dashboard` → `/`

### From Special Requests Page
- `submit-requests-button` → submits requests (POST) to update reservation

### From Locations Page
- `location-detail-button-{location_id}` → shows details (modal or route)
- `back-to-dashboard` → `/`
- Filters (`hours-filter`, `search-location-input`) update locations list dynamically

---

## 4. Programmatic Constraints and Integration Points

- All page containers and interactive elements use specified IDs for precise DOM manipulation.
- Backend must provide REST-like endpoints corresponding to Flask route definitions with JSON endpoints for dynamic content and filtering.
- Frontend must consume backend endpoints to populate dropdowns, lists, tables, and to submit forms.
- Data files in `data/` serve as the persistent storage and are to be read/written with locking to prevent race conditions.
- ID placeholders (`{vehicle_id}`, `{reservation_id}`, etc.) must be correctly replaced with data-driven values in URLs and element IDs.
- Booking and reservation modifications require synchronization with backend data files to maintain consistency.
- Price calculations triggered in Booking page should be supported by backend computation based on vehicle daily rate, rental duration, and optional insurance costs.
- Navigation is primarily via buttons and links identified by their IDs; JavaScript on frontend should handle dynamic filtering, sorting, and UI updates.

---

This detailed specification ensures frontend and backend teams can independently and concurrently develop the application modules with a crystal-clear contract of UI elements, data contracts, and navigation flows.

---