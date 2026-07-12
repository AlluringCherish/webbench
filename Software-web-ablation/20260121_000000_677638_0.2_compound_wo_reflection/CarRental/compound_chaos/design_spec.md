# design_spec.md

---

## 1. Flask Routes Specification (Backend)

| Route Path                              | Function Name               | HTTP Methods | Template Filename             | Context Variables                                                                                             |
|---------------------------------------|-----------------------------|--------------|------------------------------|--------------------------------------------------------------------------------------------------------------|
| / (root)                              | root_redirect               | GET          | None                         | None (Redirects to /dashboard)                                                                               |
| /dashboard                           | dashboard                  | GET          | dashboard.html               | featured_vehicles: List[Dict[str, Any]] (vehicles), promotions: List[str]                                    |
| /search                             | vehicle_search             | GET          | search.html                  | vehicles: List[Vehicle], locations: List[str], vehicle_types: List[str], filters: Dict[str, str]             |
| /vehicle/<int:vehicle_id>           | vehicle_details            | GET          | vehicle_details.html         | vehicle: Vehicle, reviews: List[Dict[str, str]]                                                               |
| /booking/<int:vehicle_id>            | booking_page               | GET, POST    | booking.html                 | vehicle: Vehicle, locations: List[str], rental_data: Dict[str, str], total_price: float (optional)            |
| /insurance/<int:reservation_id>      | insurance_options          | GET, POST    | insurance.html               | insurance_plans: List[Insurance], selected_plan: Insurance or None, reservation_id: int                      |
| /history                            | rental_history             | GET          | history.html                 | rentals: List[Rental], filter_status: str                                                                      |
| /reservations                      | reservation_management     | GET, POST    | reservations.html            | reservations: List[Reservation], sorted_by_date: bool                                                       |
| /special_requests                   | special_requests           | GET, POST    | special_requests.html        | reservations: List[Reservation], submission_status: str                                                     |
| /locations                        | locations_page             | GET          | locations.html               | locations: List[Location], filter_hours: str, search_query: str                                            |

---

Notes on Context Variables Types:
- Vehicle: Dict with keys (vehicle_id: int, make: str, model: str, vehicle_type: str, daily_rate: float, seats: int, transmission: str, fuel_type: str, status: str)
- Rental: Dict with keys (rental_id: int, vehicle_id: int, customer_id: int, pickup_date: date, dropoff_date: date, pickup_location: str, dropoff_location: str, total_price: float, status: str)
- Insurance: Dict with keys (insurance_id: int, plan_name: str, description: str, daily_cost: float, coverage_limit: str, deductible: int/float or str)
- Reservation: Dict with keys (reservation_id: int, rental_id: int, vehicle_id: int, customer_id: int, status: str, insurance_id: int, special_requests: str)
- Location: Dict with keys (location_id: int, city: str, address: str, phone: str, hours: str, available_vehicles: int)


## 2. HTML Template Specifications (Frontend)

### 2.1 Dashboard Page
- Template Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-vehicles (Div): Displays featured vehicle recommendations.
  - search-vehicles-button (Button): Navigates to vehicle search page (url_for('vehicle_search')).
  - my-reservations-button (Button): Navigates to reservation management page (url_for('reservation_management')).
  - promotions-section (Div): Displays current promotions.
- Navigation Mapping:
  - search-vehicles-button -> url_for('vehicle_search')
  - my-reservations-button -> url_for('reservation_management')
- Context Variables:
  - featured_vehicles: List of dicts representing vehicles.
  - promotions: List of strings representing current offers.
- Jinja2 Usage:
  - Loop over featured_vehicles to display vehicle cards.
  - Loop over promotions to display promotional messages.

### 2.2 Vehicle Search Page
- Template Filename: templates/search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for search page.
  - location-filter (Dropdown/Select): Filter vehicles by pickup location.
  - vehicle-type-filter (Dropdown/Select): Filter by vehicle type.
  - date-range-input (Input): Select rental date range.
  - vehicles-grid (Div): Grid displaying each vehicle card.
  - view-details-button-{vehicle_id} (Button): Button to view details of vehicle with id vehicle_id.
- Navigation Mapping:
  - view-details-button-{vehicle_id} -> url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: List of Vehicle dicts.
  - locations: List of strings (location names) for filtering.
  - vehicle_types: List of vehicle type strings.
  - filters: Dict of current filter selections.
- Jinja2 Usage:
  - Use loops to generate vehicle cards.
  - Dynamically generate view-details-button-{vehicle_id} with vehicle_id.

### 2.3 Vehicle Details Page
- Template Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container for the page.
  - vehicle-name (H1): Display vehicle make and model.
  - vehicle-specs (Div): Show engine, seats, transmission specs.
  - daily-rate (Div): Show daily rental rate.
  - book-now-button (Button): Navigates to booking page for this vehicle (url_for('booking_page', vehicle_id=vehicle.vehicle_id)).
  - vehicle-reviews (Div): Display list of reviews.
- Navigation Mapping:
  - book-now-button -> url_for('booking_page', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: Vehicle dict.
  - reviews: List of dicts with keys e.g. {author: str, comment: str, rating: int}.
- Jinja2 Usage:
  - Display vehicle fields.
  - Loop through reviews.

### 2.4 Booking Page
- Template Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container for the booking page.
  - pickup-location (Dropdown/Select): Select pickup location.
  - dropoff-location (Dropdown/Select): Select dropoff location.
  - pickup-date (Input[type=date]): Select pickup date.
  - dropoff-date (Input[type=date]): Select dropoff date.
  - calculate-price-button (Button): Submit to calculate total rental price.
  - total-price (Div): Show calculated total price (visible after calculation).
  - proceed-to-insurance-button (Button): Proceed to insurance options page.
- Navigation Mapping:
  - proceed-to-insurance-button -> url_for('insurance_options', reservation_id=reservation_id) [POST form submission]
- Context Variables:
  - vehicle: Vehicle dict.
  - locations: List of strings.
  - rental_data: Dict with keys pickup_location (str), dropoff_location (str), pickup_date (str), dropoff_date (str) for form fields.
  - total_price: float or None
- Jinja2 Usage:
  - Render vehicle and location options.
  - Render form inputs with prefilled values from rental_data.
  - Conditionally show total-price div when total_price is available.

### 2.5 Insurance Options Page
- Template Filename: templates/insurance.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container for insurance page.
  - insurance-options (Div): Displays insurance plans.
  - select-insurance-{insurance_id} (Radio): Radio button for each insurance plan.
  - insurance-description (Div): Shows selected insurance description.
  - insurance-price (Div): Shows selected insurance daily cost.
  - confirm-booking-button (Button): Button to confirm booking with insurance.
- Navigation Mapping:
  - confirm-booking-button -> POST confirms booking for reservation_id.
- Context Variables:
  - insurance_plans: List of Insurance dicts.
  - selected_plan: Insurance dict or None.
  - reservation_id: int
- Jinja2 Usage:
  - Loop insurance_plans to generate radios.
  - Display details of selected_plan dynamically.

### 2.6 Rental History Page
- Template Filename: templates/history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container for history page.
  - rentals-table (Table): Table listing rentals with columns: ID, vehicle, dates, location, status.
  - view-rental-details-{rental_id} (Button): View detailed rental info.
  - status-filter (Dropdown/Select): Filter rentals by status (All, Active, Completed, Cancelled).
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mapping:
  - view-rental-details-{rental_id} -> url_for('rental_history') or a detail view if implemented.
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - rentals: List of Rental dicts.
  - filter_status: str
- Jinja2 Usage:
  - Loop over rentals to populate table rows.
  - Dynamic IDs for detail buttons.

### 2.7 Reservation Management Page
- Template Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container for reservations.
  - reservations-list (Div): Lists reservations with vehicle info, dates, status.
  - modify-reservation-button-{reservation_id} (Button): Modify reservation.
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation.
  - sort-by-date-button (Button): Sort reservations by date.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mapping:
  - modify-reservation-button-{reservation_id} -> url_for('reservation_management') [POST or GET form]
  - cancel-reservation-button-{reservation_id} -> url_for('reservation_management') [POST form]
  - sort-by-date-button -> url_for('reservation_management') [GET or POST with sorting]
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - reservations: List of Reservation dicts.
  - sorted_by_date: bool
- Jinja2 Usage:
  - Loop reservations to display info.
  - Dynamic element IDs for buttons.

### 2.8 Special Requests Page
- Template Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container for special requests.
  - select-reservation (Dropdown/Select): Select reservation to add requests.
  - driver-assistance-checkbox (Checkbox): Request driver assistance.
  - gps-option-checkbox (Checkbox): Request GPS option.
  - child-seat-quantity (Input[type=number]): Number of child seats.
  - special-notes (Textarea): Text field for notes.
  - submit-requests-button (Button): Submit special requests.
- Navigation Mapping:
  - submit-requests-button -> url_for('special_requests') [POST form]
- Context Variables:
  - reservations: List of Reservation dicts.
  - submission_status: str (e.g., success or error message)
- Jinja2 Usage:
  - Loop reservations to populate select.
  - Input elements bound to form fields.

### 2.9 Locations Page
- Template Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container for locations.
  - locations-list (Div): List all locations info.
  - location-detail-button-{location_id} (Button): View location details.
  - hours-filter (Dropdown/Select): Filter by operating hours.
  - search-location-input (Input): Search locations by city or name.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mapping:
  - location-detail-button-{location_id} -> url_for('locations_page') or detail view if implemented
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - locations: List of Location dicts.
  - filter_hours: str
  - search_query: str
- Jinja2 Usage:
  - Loop locations to display location cards.
  - Populate filters with current selections.


## 3. Data File Schemas

### 3.1 vehicles.txt
- Filename: data/vehicles.txt
- Fields (pipe-delimited in order):
  - vehicle_id (int)
  - make (str)
  - model (str)
  - vehicle_type (str)
  - daily_rate (float)
  - seats (int)
  - transmission (str)
  - fuel_type (str)
  - status (str)
- Purpose: Stores details of all vehicles available for rent.
- Example Lines:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

---

### 3.2 customers.txt
- Filename: data/customers.txt
- Fields (pipe-delimited in order):
  - customer_id (int)
  - name (str)
  - email (str)
  - phone (str)
  - driver_license (str)
  - license_expiry (date, YYYY-MM-DD)
- Purpose: Stores registered customer information.
- Example Lines:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

---

### 3.3 locations.txt
- Filename: data/locations.txt
- Fields (pipe-delimited in order):
  - location_id (int)
  - city (str)
  - address (str)
  - phone (str)
  - hours (str)
  - available_vehicles (int)
- Purpose: Stores rental pickup and dropoff locations.
- Example Lines:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

---

### 3.4 rentals.txt
- Filename: data/rentals.txt
- Fields (pipe-delimited in order):
  - rental_id (int)
  - vehicle_id (int)
  - customer_id (int)
  - pickup_date (date, YYYY-MM-DD)
  - dropoff_date (date, YYYY-MM-DD)
  - pickup_location (str)
  - dropoff_location (str)
  - total_price (float)
  - status (str)
- Purpose: Stores rental records.
- Example Lines:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

---

### 3.5 insurance.txt
- Filename: data/insurance.txt
- Fields (pipe-delimited in order):
  - insurance_id (int)
  - plan_name (str)
  - description (str)
  - daily_cost (float)
  - coverage_limit (str)
  - deductible (int/float/str)
- Purpose: Stores insurance plans available for rentals.
- Example Lines:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

---

### 3.6 reservations.txt
- Filename: data/reservations.txt
- Fields (pipe-delimited in order):
  - reservation_id (int)
  - rental_id (int)
  - vehicle_id (int)
  - customer_id (int)
  - status (str)
  - insurance_id (int)
  - special_requests (str)
- Purpose: Stores reservation details linking rentals and extra info.
- Example Lines:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

