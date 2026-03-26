# design_spec.md - CarRental Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name                 | HTTP Methods | Template Filename          | Context Variables (name: type)                                                                                              |
|-------------------------------|-------------------------------|--------------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect                  | GET          | None (Redirect)             | None                                                                                                                        |
| /dashboard                    | dashboard                     | GET          | dashboard.html              | featured_vehicles: List[Dict[str, Any]] (vehicles info), promotions: List[str]                                              |
| /search-vehicles              | search_vehicles               | GET          | search_vehicles.html        | locations: List[str], vehicle_types: List[str], selected_location: Optional[str], selected_vehicle_type: Optional[str], rental_date_range: Optional[Tuple[str, str]], available_vehicles: List[Dict[str, Any]] |
| /vehicle-details/<int:vehicle_id> | vehicle_details              | GET          | vehicle_details.html        | vehicle: Dict[str, Any], vehicle_reviews: List[Dict[str, Any]]                                                               |
| /booking/<int:vehicle_id>     | booking                      | GET, POST    | booking.html                | vehicle: Dict[str, Any], pickup_locations: List[str], dropoff_locations: List[str], pickup_date: Optional[str], dropoff_date: Optional[str], total_price: Optional[float]  |
| /insurance-options/<int:reservation_id> | insurance_options           | GET, POST    | insurance_options.html      | insurance_plans: List[Dict[str, Any]], selected_insurance_id: Optional[int], selected_insurance_description: Optional[str], selected_insurance_price: Optional[float] |
| /rental-history               | rental_history               | GET          | rental_history.html         | rentals: List[Dict[str, Any]], status_filter_options: List[str], selected_status_filter: str                                |
| /rental-details/<int:rental_id> | rental_details              | GET          | rental_details.html         | rental: Dict[str, Any]                                                                                                       |
| /my-reservations              | my_reservations              | GET          | my_reservations.html        | reservations: List[Dict[str, Any]]                                                                                           |
| /modify-reservation/<int:reservation_id> | modify_reservation          | GET, POST    | modify_reservation.html     | reservation: Dict[str, Any]                                                                                                  |
| /cancel-reservation/<int:reservation_id> | cancel_reservation          | POST         | None (redirect as needed)   | None                                                                                                                        |
| /special-requests             | special_requests             | GET, POST    | special_requests.html       | reservations: List[Dict[str, Any]], submission_status: Optional[str]                                                         |
| /locations                   | locations                   | GET          | locations.html              | locations: List[Dict[str, Any]] , hours_filter_options: List[str], selected_hours_filter: Optional[str], search_query: Optional[str] |
| /location-details/<int:location_id> | location_details            | GET          | location_details.html       | location: Dict[str, Any]                                                                                                     |

---

## Section 2: HTML Template Specifications (Frontend)

### 1. dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-vehicles (Div): Display featured vehicle recommendations.
  - search-vehicles-button (Button): Navigate to vehicle search page.
  - my-reservations-button (Button): Navigate to reservations page.
  - promotions-section (Div): Display current promotions and offers.
- Navigation:
  - search-vehicles-button: url_for('search_vehicles')
  - my-reservations-button: url_for('my_reservations')
- Context Variables:
  - featured_vehicles: List[Dict[str, Any]] (Each vehicle dict with keys: vehicle_id (int), make (str), model (str), daily_rate (float))
  - promotions: List[str]

### 2. search_vehicles.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for the search page.
  - location-filter (Dropdown): Filter by pickup location.
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - date-range-input (Input): Rental date range selection.
  - vehicles-grid (Div): Displays vehicle cards.
  - view-details-button-{vehicle_id} (Button): View details for each vehicle.
- Navigation:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - locations: List[str]
  - vehicle_types: List[str]
  - selected_location: Optional[str]
  - selected_vehicle_type: Optional[str]
  - rental_date_range: Optional[Tuple[str, str]] (start_date, end_date strings in 'YYYY-MM-DD')
  - available_vehicles: List[Dict[str, Any]] (each dict includes vehicle_id (int), make (str), model (str), daily_rate (float), vehicle_type (str))

### 3. vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container for vehicle details.
  - vehicle-name (H1): Displays vehicle name and model.
  - vehicle-specs (Div): Engine, seats, transmission specs.
  - daily-rate (Div): Display daily rental rate.
  - book-now-button (Button): Book this vehicle.
  - vehicle-reviews (Div): Customer reviews section.
- Navigation:
  - book-now-button: url_for('booking', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: Dict[str, Any] (keys: vehicle_id (int), make (str), model (str), engine (str), seats (int), transmission (str), daily_rate (float), fuel_type (str), status (str))
  - vehicle_reviews: List[Dict[str, Any]] (each with review_id (int), customer_name (str), rating (int), comment (str))

### 4. booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container for booking page.
  - pickup-location (Dropdown): Select pickup location.
  - dropoff-location (Dropdown): Select dropoff location.
  - pickup-date (Input): Pickup date.
  - dropoff-date (Input): Dropoff date.
  - calculate-price-button (Button): Calculate total rental price.
  - total-price (Div): Display calculated total price.
  - proceed-to-insurance-button (Button): Proceed to insurance options.
- Navigation:
  - proceed-to-insurance-button: url_for('insurance_options', reservation_id=reservation_id)
- Context Variables:
  - vehicle: Dict[str, Any] (vehicle_id (int), make (str), model (str), daily_rate (float))
  - pickup_locations: List[str]
  - dropoff_locations: List[str]
  - pickup_date: Optional[str]
  - dropoff_date: Optional[str]
  - total_price: Optional[float]

### 5. insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container for insurance page.
  - insurance-options (Div): Display insurance plans.
  - select-insurance-{insurance_id} (Radio): Select insurance plan.
  - insurance-description (Div): Description of selected insurance plan.
  - insurance-price (Div): Insurance price.
  - confirm-booking-button (Button): Confirm booking.
- Navigation:
  - confirm-booking-button: url_for('confirm_booking') or appropriate route
- Context Variables:
  - insurance_plans: List[Dict[str, Any]] (insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (int or str), deductible (int))
  - selected_insurance_id: Optional[int]
  - selected_insurance_description: Optional[str]
  - selected_insurance_price: Optional[float]

### 6. rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container for rental history page.
  - rentals-table (Table): Rental records table.
  - view-rental-details-{rental_id} (Button): View rental details.
  - status-filter (Dropdown): Filter by status (All, Active, Completed, Cancelled).
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - view-rental-details-{rental_id}: url_for('rental_details', rental_id=rental_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - rentals: List[Dict[str, Any]] (rental_id (int), vehicle_info (str), pickup_date (str), dropoff_date (str), pickup_location (str), dropoff_location (str), total_price (float), status (str))
  - status_filter_options: List[str] = ["All", "Active", "Completed", "Cancelled"]
  - selected_status_filter: str

### 7. my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container for reservations page.
  - reservations-list (Div): List reservations.
  - modify-reservation-button-{reservation_id} (Button): Modify reservation.
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation.
  - sort-by-date-button (Button): Sort reservations by date.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - modify-reservation-button-{reservation_id}: url_for('modify_reservation', reservation_id=reservation_id)
  - cancel-reservation-button-{reservation_id}: sends POST to url_for('cancel_reservation', reservation_id=reservation_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - reservations: List[Dict[str, Any]] (reservation_id (int), vehicle_info (str), dates (str), status (str))

### 8. special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container for special requests page.
  - select-reservation (Dropdown): Select reservation to add requests to.
  - driver-assistance-checkbox (Checkbox): Driver assistance request.
  - gps-option-checkbox (Checkbox): GPS option.
  - child-seat-quantity (Input): Number of child seats.
  - special-notes (Textarea): Special notes.
  - submit-requests-button (Button): Submit requests.
- Navigation:
  - No navigation buttons specified.
- Context Variables:
  - reservations: List[Dict[str, Any]] (reservation_id (int), description (str))
  - submission_status: Optional[str]

### 9. locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container for locations page.
  - locations-list (Div): List all locations.
  - location-detail-button-{location_id} (Button): View location details.
  - hours-filter (Dropdown): Filter by operating hours (24/7, Business Hours, Weekend).
  - search-location-input (Input): Search locations by city or name.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - location-detail-button-{location_id}: url_for('location_details', location_id=location_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - locations: List[Dict[str, Any]] (location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int))
  - hours_filter_options: List[str] = ["24/7", "Business Hours", "Weekend"]
  - selected_hours_filter: Optional[str]
  - search_query: Optional[str]

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Purpose: Contains details of vehicles available for rental including specifications and status.
- Filename: vehicles.txt
- Format (pipe-delimited fields):
  vehicle_id (int) | make (str) | model (str) | vehicle_type (str) | daily_rate (float) | seats (int) | transmission (str) | fuel_type (str) | status (str)
- Example Lines:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

---

### 2. customers.txt
- Purpose: Stores customer personal and license information.
- Filename: customers.txt
- Format (pipe-delimited fields):
  customer_id (int) | name (str) | email (str) | phone (str) | driver_license (str) | license_expiry (str, date YYYY-MM-DD)
- Example Lines:
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

---

### 3. locations.txt
- Purpose: Contains pickup and dropoff location details including operating hours and vehicle availability.
- Filename: locations.txt
- Format (pipe-delimited fields):
  location_id (int) | city (str) | address (str) | phone (str) | hours (str) | available_vehicles (int)
- Example Lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

---

### 4. rentals.txt
- Purpose: Tracks rental transactions including vehicle, customer, dates, locations, price, and status.
- Filename: rentals.txt
- Format (pipe-delimited fields):
  rental_id (int) | vehicle_id (int) | customer_id (int) | pickup_date (str, YYYY-MM-DD) | dropoff_date (str, YYYY-MM-DD) | pickup_location (str) | dropoff_location (str) | total_price (float) | status (str)
- Example Lines:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

---

### 5. insurance.txt
- Purpose: Stores insurance plan details available for rental coverage.
- Filename: insurance.txt
- Format (pipe-delimited fields):
  insurance_id (int) | plan_name (str) | description (str) | daily_cost (float) | coverage_limit (int or str) | deductible (int)
- Example Lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

---

### 6. reservations.txt
- Purpose: Manages rental reservations linking rentals, vehicles, customers, insurance, and special requests.
- Filename: reservations.txt
- Format (pipe-delimited fields):
  reservation_id (int) | rental_id (int) | vehicle_id (int) | customer_id (int) | status (str) | insurance_id (int) | special_requests (str)
- Example Lines:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed

---
