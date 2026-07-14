# CarRental Flask Web Application Specification - Consolidated Design Debate A Revised

## Section 1: Web Routes and Navigation

### Route Definitions

| Route Path                | HTTP Method     | Description                                        | Template           | Context Variables Passed                                   |
|---------------------------|-----------------|----------------------------------------------------|--------------------|------------------------------------------------------------|
| `/`                       | GET             | Entry point; renders Dashboard                     | dashboard.html     | featured_vehicles (list of dict), promotions (list of dict) |
| `/dashboard`              | GET             | Alternate entry to Dashboard                        | dashboard.html     | featured_vehicles (list of dict), promotions (list of dict) |
| `/search`                 | GET, POST       | Search Vehicles page with filters                   | search.html        | locations (list of dict), vehicle_types (list of str), filtered_vehicles (list of dict), selected_location (str or None), selected_vehicle_type (str or None), selected_date_range (str) |
| `/vehicle/<int:vehicle_id>`| GET            | Vehicle Details by vehicle_id                       | vehicle_details.html| vehicle (dict), reviews (list of dict)                     |
| `/booking/<int:vehicle_id>`| GET, POST      | Booking page; GET form, POST booking submission or price calculation | booking.html       | vehicle (dict), locations (list of dict), calculated_price (float or None) |
| `/insurance/<int:reservation_id>` | GET, POST | Insurance selection and booking confirmation       | insurance.html     | insurance_plans (list of dict), selected_plan (dict or None), reservation (dict) |
| `/history`                | GET, POST       | Rental History page with status filter              | history.html       | rentals (list of dict), status_options (list of str), selected_status (str) |
| `/reservations`           | GET, POST       | Manage reservations including modify/cancel actions| reservations.html  | reservations (list of dict)                               |
| `/requests`               | GET, POST       | Submit special requests                             | requests.html      | reservations (list of dict)                               |
| `/locations`              | GET, POST       | Locations page with hours filter and search input  | locations.html     | locations (list of dict), hours_options (list of str), selected_hours_filter (str or None), search_text (str) |

### Navigation and Form Actions

- `search-vehicles-button`: Navigate with GET to `/search`
- `my-reservations-button`: Navigate with GET to `/reservations`
- `view-details-button-{vehicle_id}`: Navigate GET `/vehicle/{vehicle_id}`
- `book-now-button`: Navigate GET `/booking/{vehicle_id}`
- `calculate-price-button`: POST on `/booking/{vehicle_id}` to calculate price
- `proceed-to-insurance-button`: Navigate GET or POST `/insurance/{reservation_id}` to proceed
- `select-insurance-{insurance_id}`: Radio selection within `/insurance/{reservation_id}`, POST form selects plan
- `confirm-booking-button`: POST on `/insurance/{reservation_id}` finalizes booking
- `view-rental-details-{rental_id}`: Button for future usage, non-route dependent
- `modify-reservation-button-{reservation_id}`: POST `/reservations` modifies reservation
- `cancel-reservation-button-{reservation_id}`: POST `/reservations` cancels reservation
- `sort-by-date-button`: POST or GET `/reservations` sorts list
- `submit-requests-button`: POST `/requests` submits special requests
- `location-detail-button-{location_id}`: client-side detail, no separate route
- `back-to-dashboard`: GET `/` or `/dashboard`

## Section 2: HTML Page and Element Specifications

### 1. Dashboard Page (`dashboard.html`)
- Title: "Car Rental Dashboard"
- Container ID: `dashboard-page`
- Elements:
  - `featured-vehicles` (div)
  - `search-vehicles-button` (button)
  - `my-reservations-button` (button)
  - `promotions-section` (div)

### 2. Vehicle Search Page (`search.html`)
- Title: "Search Vehicles"
- Container ID: `search-page`
- Elements:
  - `location-filter` (dropdown)
  - `vehicle-type-filter` (dropdown) (Economy, Compact, Sedan, SUV, Luxury)
  - `date-range-input` (input)
  - `vehicles-grid` (div)
  - Dynamic button: `view-details-button-{vehicle_id}`

### 3. Vehicle Details Page (`vehicle_details.html`)
- Title: "Vehicle Details"
- Container ID: `vehicle-details-page`
- Elements:
  - `vehicle-name` (h1)
  - `vehicle-specs` (div)
  - `daily-rate` (div)
  - `book-now-button` (button)
  - `vehicle-reviews` (div)

### 4. Booking Page (`booking.html`)
- Title: "Book Your Rental"
- Container ID: `booking-page`
- Elements:
  - `pickup-location` (dropdown)
  - `dropoff-location` (dropdown)
  - `pickup-date` (input date)
  - `dropoff-date` (input date)
  - `calculate-price-button` (button)
  - `total-price` (div)
  - `proceed-to-insurance-button` (button)

### 5. Insurance Options Page (`insurance.html`)
- Title: "Select Insurance Coverage"
- Container ID: `insurance-page`
- Elements:
  - `insurance-options` (div)
  - Dynamic radio buttons: `select-insurance-{insurance_id}`
  - `insurance-description` (div)
  - `insurance-price` (div)
  - `confirm-booking-button` (button)

### 6. Rental History Page (`history.html`)
- Title: "Rental History"
- Container ID: `history-page`
- Elements:
  - `rentals-table` (table) with columns: ID, vehicle, dates, location, status
  - Dynamic buttons: `view-rental-details-{rental_id}`
  - `status-filter` (dropdown) with options All, Active, Completed, Cancelled
  - `back-to-dashboard` (button)

### 7. Reservation Management Page (`reservations.html`)
- Title: "My Reservations"
- Container ID: `reservations-page`
- Elements:
  - `reservations-list` (div)
  - Dynamic buttons: `modify-reservation-button-{reservation_id}`, `cancel-reservation-button-{reservation_id}`
  - `sort-by-date-button` (button)
  - `back-to-dashboard` (button)

### 8. Special Requests Page (`requests.html`)
- Title: "Special Requests"
- Container ID: `requests-page`
- Elements:
  - `select-reservation` (dropdown)
  - `driver-assistance-checkbox` (checkbox)
  - `gps-option-checkbox` (checkbox)
  - `child-seat-quantity` (input number)
  - `special-notes` (textarea)
  - `submit-requests-button` (button)

### 9. Locations Page (`locations.html`)
- Title: "Pickup and Dropoff Locations"
- Container ID: `locations-page`
- Elements:
  - `locations-list` (div)
  - Dynamic buttons: `location-detail-button-{location_id}`
  - `hours-filter` (dropdown) with options 24/7, Business Hours, Weekend
  - `search-location-input` (input)
  - `back-to-dashboard` (button)

## Section 3: Local Text Data File Format and Schema

All data files are stored in the `data/` directory. Fields are pipe `|` separated.

1. vehicles.txt
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

2. customers.txt
```
customer_id|name|email|phone|driver_license|license_expiry
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

3. locations.txt
```
location_id|city|address|phone|hours|available_vehicles
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

4. rentals.txt
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

5. insurance.txt
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

6. reservations.txt
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

## Section 4: Consistency Requirements

- `/` route is the mandatory entry point and renders the dashboard page immediately.
- Both `/` and `/dashboard` routes serve the dashboard template.
- POST methods are used exclusively for data-altering operations (booking submission, insurance selection, reservation modification, requests submission).
- GET methods serve page content and navigation.
- All dynamic element IDs match data keys exactly (e.g., `view-details-button-3`).
- Navigation buttons and form submissions align with declared routes and HTTP methods.
- Data file formats and field orders are strictly maintained as specified.
- Filter and search forms typically use POST to submit filter criteria and refresh listings.

---

This finalized design_debate_a.md incorporates peer design details and complies fully with the user requirements and adaptive web contract rules.