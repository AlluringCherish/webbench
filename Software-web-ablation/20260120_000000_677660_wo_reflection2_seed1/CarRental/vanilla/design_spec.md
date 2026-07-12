# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name              | HTTP Method(s) | Template File            | Context Variables                                                                                      |
|----------------------------|----------------------------|----------------|--------------------------|------------------------------------------------------------------------------------------------------|
| /                          | redirect_to_dashboard       | GET            | N/A (redirect)            | N/A                                                                                                  |
| /dashboard                 | dashboard                  | GET            | dashboard.html            | featured_vehicles: list[dict], promotions: list[dict]                                                |
| /search-vehicles           | search_vehicles            | GET            | vehicle_search.html       | locations: list[dict], vehicle_types: list[str], filtered_vehicles: list[dict], search_filters: dict |
| /vehicle/<int:vehicle_id> | vehicle_details            | GET            | vehicle_details.html      | vehicle: dict, reviews: list[dict]                                                                   |
| /booking/<int:vehicle_id>  | booking                   | GET, POST      | booking.html              | vehicle: dict, locations: list[dict], calculated_price: float or None, booking_form: dict (on POST)   |
| /insurance/<int:reservation_id> | insurance_options          | GET, POST      | insurance_options.html    | reservation: dict, insurance_plans: list[dict], selected_insurance: dict or None                      |
| /rental-history            | rental_history             | GET            | rental_history.html       | rentals: list[dict], filtered_status: str                                                              |
| /my-reservations           | reservation_management     | GET, POST      | reservation_management.html| reservations: list[dict]                                                                             |
| /special-requests          | special_requests           | GET, POST      | special_requests.html     | reservations: list[dict], submitted_request: dict (on POST)                                          |
| /locations                | locations_page             | GET            | locations.html            | locations: list[dict]                                                                                |

### Route Details Explanation:

- **/** : Redirects to `/dashboard`.
- **/dashboard** : Shows main dashboard with featured vehicles and promotions.
- **/search-vehicles** : Shows vehicle search page with filters including location and vehicle type.
- **/vehicle/<vehicle_id>** : Shows detailed info for the vehicle with given ID, including customer reviews.
- **/booking/<vehicle_id>** : Displays booking page for vehicle identified by `vehicle_id`. Supports GET for form display and POST for booking submission/calculations.
- **/insurance/<reservation_id>** : Displays insurance options linked to the reservation. Supports GET for display and POST for selection confirmation.
- **/rental-history** : Displays past rentals filtered optionally by status.
- **/my-reservations** : Displays and manages user reservations, allowing modification and cancellation via POST.
- **/special-requests** : Allows submitting special requests related to selected reservation.
- **/locations** : Lists all rental pickup and dropoff locations.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard main content.
  - featured-vehicles (Div): Container for featured vehicle recommendations.
  - search-vehicles-button (Button): Navigates to search vehicles page.
  - my-reservations-button (Button): Navigates to reservation management page.
  - promotions-section (Div): Section listing current promotions.
- Navigation Mappings:
  - search-vehicles-button: url_for('search_vehicles')
  - my-reservations-button: url_for('reservation_management')
- Context Variables:
  - featured_vehicles: list of dict with vehicle details (e.g., id, make, model, daily_rate).
  - promotions: list of dict with promotion title and description.

### 2. templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for vehicle search page.
  - location-filter (Dropdown): Select pickup location filter.
  - vehicle-type-filter (Dropdown): Select vehicle type filter (Economy, Compact, Sedan, SUV, Luxury).
  - date-range-input (Input): Input field for rental date range.
  - vehicles-grid (Div): Container grid holding vehicle cards.
  - view-details-button-{vehicle_id} (Button): Button on each vehicle card for details.
- Navigation Mappings:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - locations: list of dict containing location_id and city.
  - vehicle_types: predefined list of strings.
  - filtered_vehicles: list of dict with vehicle data matching search/filter.
  - search_filters: dict containing current filters values.

### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container for this page content.
  - vehicle-name (H1): H1 tag displaying vehicle make and model.
  - vehicle-specs (Div): Vehicle specs details like engine, seats, transmission.
  - daily-rate (Div): Daily rental rate displayed.
  - book-now-button (Button): Button to proceed to booking page for vehicle.
  - vehicle-reviews (Div): Section listing customer reviews.
- Navigation Mappings:
  - book-now-button: url_for('booking', vehicle_id=vehicle['vehicle_id'])
- Context Variables:
  - vehicle: dict with all vehicle details.
  - reviews: list of dict with review information.

### 4. templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container for booking page.
  - pickup-location (Dropdown): Select pickup location.
  - dropoff-location (Dropdown): Select dropoff location.
  - pickup-date (Input): Pick-up date input.
  - dropoff-date (Input): Drop-off date input.
  - calculate-price-button (Button): Calculates total price when clicked.
  - total-price (Div): Displays calculated total rental price.
  - proceed-to-insurance-button (Button): Proceeds to insurance options page.
- Navigation Mappings:
  - proceed-to-insurance-button: url_for('insurance_options', reservation_id=reservation_id) (POST creates reservation)
- Context Variables:
  - vehicle: dict with selected vehicle details.
  - locations: list of dict with pickup/dropoff locations.
  - calculated_price: float or None (initially None)
  - booking_form: dict or None for submitted form details if POST

### 5. templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container for insurance options.
  - insurance-options (Div): Display list of insurance plans.
  - select-insurance-{insurance_id} (Radio): Radio button for insurance selection.
  - insurance-description (Div): Displays description of selected insurance plan.
  - insurance-price (Div): Displays insurance daily cost.
  - confirm-booking-button (Button): Confirms booking with insurance.
- Navigation Mappings:
  - confirm-booking-button: submits selection (POST) and redirects to rental history or confirmation page.
- Context Variables:
  - reservation: dict representing the current reservation.
  - insurance_plans: list of dict for all available insurance plans.
  - selected_insurance: dict or None (currently selected insurance plan)

### 6. templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container for rental history page.
  - rentals-table (Table): Table showing all past rentals.
  - view-rental-details-{rental_id} (Button): Button to view more details on rental.
  - status-filter (Dropdown): Filter rentals by status (All, Active, Completed, Cancelled).
  - back-to-dashboard (Button): Return to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - rentals: list of dict with rental records.
  - filtered_status: str current filter selection

### 7. templates/reservation_management.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container for managing reservations.
  - reservations-list (Div): List all reservations.
  - modify-reservation-button-{reservation_id} (Button): Button to modify reservation.
  - cancel-reservation-button-{reservation_id} (Button): Button to cancel reservation.
  - sort-by-date-button (Button): Sort reservations by date.
  - back-to-dashboard (Button): Return to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - reservations: list of dict with reservation data

### 8. templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container for special requests form.
  - select-reservation (Dropdown): Select reservation to add requests to.
  - driver-assistance-checkbox (Checkbox): Request for driver assistance.
  - gps-option-checkbox (Checkbox): Request GPS option.
  - child-seat-quantity (Input): Number of child seats requested.
  - special-notes (Textarea): Field for special notes.
  - submit-requests-button (Button): Submit requests.
- Navigation Mappings:
  - submit-requests-button: POST to same page
- Context Variables:
  - reservations: list of dict for dropdown selections
  - submitted_request: dict with submitted request details on POST

### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container for locations listing.
  - locations-list (Div): List of locations with details.
  - location-detail-button-{location_id} (Button): Button for detailed view of location.
  - hours-filter (Dropdown): Filter locations by operating hours.
  - search-location-input (Input): Search locations by city or name.
  - back-to-dashboard (Button): Return to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - locations: list of dict with location details

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- **Purpose**: Stores all vehicle information available for rental.
- **Format** (pipe-delimited, no header):
  ```
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
  ```
- **Field Descriptions**:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury, etc.)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str (Petrol, Diesel, Electric)
  - status: str (Available, Rented, Maintenance)

- **Example Data**:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

---

### 2. customers.txt
- **Purpose**: Stores customer personal and license details.
- **Format** (pipe-delimited, no header):
  ```
  customer_id|name|email|phone|driver_license|license_expiry
  ```
- **Field Descriptions**:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)

- **Example Data**:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

---

### 3. locations.txt
- **Purpose**: Holds data on all vehicle pickup and dropoff locations.
- **Format** (pipe-delimited, no header):
  ```
  location_id|city|address|phone|hours|available_vehicles
  ```
- **Field Descriptions**:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g. 24/7, 09:00-18:00)
  - available_vehicles: int

- **Example Data**:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

---

### 4. rentals.txt
- **Purpose**: Logs rental transactions with rental and vehicle details.
- **Format** (pipe-delimited, no header):
  ```
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
  ```
- **Field Descriptions**:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str (city name or location identifier)
  - dropoff_location: str (city name or location identifier)
  - total_price: float
  - status: str (Active, Completed, Cancelled)

- **Example Data**:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

---

### 5. insurance.txt
- **Purpose**: Lists insurance plans with costs and coverage details.
- **Format** (pipe-delimited, no header):
  ```
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
  ```
- **Field Descriptions**:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g., number or 'Unlimited')
  - deductible: int

- **Example Data**:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

---

### 6. reservations.txt
- **Purpose**: Tracks reservations linked to rentals, vehicles, and insurance.
- **Format** (pipe-delimited, no header):
  ```
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
  ```
- **Field Descriptions**:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str

- **Example Data**:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

# End of CarRental Design Specification
