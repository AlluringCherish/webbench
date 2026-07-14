# CarRental Flask Adaptive Web Design Specification

---

## Section 1: Flask Routing and Template Context

### Routes

1. **Dashboard Page**
- Path: `/` and `/dashboard`
- Methods: GET
- Purpose: Default entry point to show dashboard overview
- Template: `dashboard.html`
- Context: 
  ```python
  {
    "featured_vehicles": list_of_featured_vehicles,
    "promotions": current_promotions
  }
  ```

2. **Vehicle Search Page**
- Path: `/search`
- Methods: GET, POST (POST for form filters)
- Purpose: Show all available vehicles with filter options
- Template: `search.html`
- Context:
  ```python
  {
    "locations": list_of_locations,
    "vehicle_types": ["Economy", "Compact", "Sedan", "SUV", "Luxury"],
    "filtered_vehicles": filtered_vehicle_list,
    "selected_location": selected_pickup_location or None,
    "selected_vehicle_type": selected_vehicle_type or None,
    "selected_date_range": selected_date_range or ""
  }
  ```

3. **Vehicle Details Page**
- Path: `/vehicle/<int:vehicle_id>`
- Methods: GET
- Purpose: Show detailed vehicle information
- Template: `vehicle_details.html`
- Context:
  ```python
  {
    "vehicle": vehicle_object,
    "reviews": reviews_for_vehicle
  }
  ```

4. **Booking Page**
- Path: `/book/<int:vehicle_id>`
- Methods: GET, POST (POST to submit booking details and calculate price)
- Purpose: User selects pickup, dropoff, dates to book vehicle
- Template: `booking.html`
- Context:
  ```python
  {
    "vehicle": vehicle_object,
    "locations": list_of_locations,
    "calculated_price": calculated_price or None
  }
  ```

5. **Insurance Options Page**
- Path: `/insurance/<int:reservation_id>`
- Methods: GET, POST (POST to select insurance plan and confirm booking)
- Purpose: Select insurance coverage for rental
- Template: `insurance.html`
- Context:
  ```python
  {
    "insurance_plans": insurance_plan_list,
    "selected_plan": selected_insurance_plan or None,
    "reservation": reservation_object
  }
  ```

6. **Rental History Page**
- Path: `/history`
- Methods: GET, POST (POST for status filter)
- Purpose: Show previous rentals with filter by status
- Template: `history.html`
- Context:
  ```python
  {
    "rentals": rentals_filtered_by_status,
    "status_options": ["All", "Active", "Completed", "Cancelled"],
    "selected_status": selected_status_filter or "All"
  }
  ```

7. **Reservation Management Page**
- Path: `/reservations`
- Methods: GET, POST (POST handles modify/cancel actions and optionally sorting)
- Purpose: Manage current/upcoming reservations
- Template: `reservations.html`
- Context:
  ```python
  {
    "reservations": current_reservations_list
  }
  ```

8. **Special Requests Page**
- Path: `/requests`
- Methods: GET, POST (POST submits special requests)
- Purpose: Add special requests to a reservation
- Template: `requests.html`
- Context:
  ```python
  {
    "reservations": active_reservations_list
  }
  ```

9. **Locations Page**
- Path: `/locations`
- Methods: GET, POST (POST for filtering by hours or search)
- Purpose: Display rental pickup/dropoff locations
- Template: `locations.html`
- Context:
  ```python
  {
    "locations": filtered_locations_list,
    "hours_options": ["24/7", "Business Hours", "Weekend"],
    "selected_hours_filter": selected_hours or None,
    "search_text": search_text or ""
  }
  ```

---

## Section 2: HTML Template and Dynamic Element IDs

### 1. Dashboard Page (`dashboard.html`)
- Title: "Car Rental Dashboard"
- Container Div: `dashboard-page`
- Elements:
  - `featured-vehicles` (Div)
  - `search-vehicles-button` (Button)
  - `my-reservations-button` (Button)
  - `promotions-section` (Div)

### 2. Vehicle Search Page (`search.html`)
- Title: "Search Vehicles"
- Container Div: `search-page`
- Elements:
  - `location-filter` (Dropdown)
  - `vehicle-type-filter` (Dropdown, options: Economy, Compact, Sedan, SUV, Luxury)
  - `date-range-input` (Input)
  - `vehicles-grid` (Div)
  - For each vehicle:
    - `view-details-button-{vehicle_id}` (Button) e.g. `view-details-button-3`

### 3. Vehicle Details Page (`vehicle_details.html`)
- Title: "Vehicle Details"
- Container Div: `vehicle-details-page`
- Elements:
  - `vehicle-name` (H1)
  - `vehicle-specs` (Div) [engine, seats, transmission details]
  - `daily-rate` (Div)
  - `book-now-button` (Button)
  - `vehicle-reviews` (Div)

### 4. Booking Page (`booking.html`)
- Title: "Book Your Rental"
- Container Div: `booking-page`
- Elements:
  - `pickup-location` (Dropdown)
  - `dropoff-location` (Dropdown)
  - `pickup-date` (Input date)
  - `dropoff-date` (Input date)
  - `calculate-price-button` (Button)
  - `total-price` (Div)
  - `proceed-to-insurance-button` (Button)

### 5. Insurance Options Page (`insurance.html`)
- Title: "Select Insurance Coverage"
- Container Div: `insurance-page`
- Elements:
  - `insurance-options` (Div)
  - For each insurance plan:
    - `select-insurance-{insurance_id}` (Radio button) e.g. `select-insurance-2`
  - `insurance-description` (Div)
  - `insurance-price` (Div)
  - `confirm-booking-button` (Button)

### 6. Rental History Page (`history.html`)
- Title: "Rental History"
- Container Div: `history-page`
- Elements:
  - `rentals-table` (Table) with columns: ID, vehicle, dates, location, status
  - For each rental row:
    - `view-rental-details-{rental_id}` (Button)
  - `status-filter` (Dropdown) choices: All, Active, Completed, Cancelled
  - `back-to-dashboard` (Button)

### 7. Reservation Management Page (`reservations.html`)
- Title: "My Reservations"
- Container Div: `reservations-page`
- Elements:
  - `reservations-list` (Div) listing reservations
  - For each reservation:
    - `modify-reservation-button-{reservation_id}` (Button)
    - `cancel-reservation-button-{reservation_id}` (Button)
  - `sort-by-date-button` (Button)
  - `back-to-dashboard` (Button)

### 8. Special Requests Page (`requests.html`)
- Title: "Special Requests"
- Container Div: `requests-page`
- Elements:
  - `select-reservation` (Dropdown)
  - `driver-assistance-checkbox` (Checkbox)
  - `gps-option-checkbox` (Checkbox)
  - `child-seat-quantity` (Input number)
  - `special-notes` (Textarea)
  - `submit-requests-button` (Button)

### 9. Locations Page (`locations.html`)
- Title: "Pickup and Dropoff Locations"
- Container Div: `locations-page`
- Elements:
  - `locations-list` (Div)
  - For each location:
    - `location-detail-button-{location_id}` (Button)
  - `hours-filter` (Dropdown) options: 24/7, Business Hours, Weekend
  - `search-location-input` (Input)
  - `back-to-dashboard` (Button)

---

## Section 3: Data File Specifications

### 1. vehicles.txt
- Fields: vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Example rows:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. customers.txt
- Fields: customer_id|name|email|phone|driver_license|license_expiry
- Example rows:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. locations.txt
- Fields: location_id|city|address|phone|hours|available_vehicles
- Example rows:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. rentals.txt
- Fields: rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Example rows:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. insurance.txt
- Fields: insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Example rows:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. reservations.txt
- Fields: reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Example rows:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

## Section 4: Cross-Artifact Consistency

- The `/` route is configured to render or redirect immediately to the Dashboard page with no authentication required.
- All pages and POST routes follow a strict naming and method convention matching element IDs with route parameters.
- Dynamic IDs such as `view-details-button-{vehicle_id}`, `select-insurance-{insurance_id}`, `modify-reservation-button-{reservation_id}`, etc. are precisely from the data keys.
- Routes that modify data (booking, insurance selection, requests submission, modify/cancel reservations) exclusively use POST and return updated views keeping user on contextually relevant page.
- Navigation buttons like `back-to-dashboard`, `search-vehicles-button`, `my-reservations-button` use GET and route exactly to their destinations.
- Local text files follow the exact field order, separator `|`, and sample row formatting as detailed to ensure stable data parsing.
- Filters use POST to allow form submissions and display filtered results without page reload anomalies.
- The design fully respects laid out page elements, their types, container IDs, and inner control IDs for seamless front-end/backend interaction.

---

End of CarRental Flask Adaptive Web Design Specification
