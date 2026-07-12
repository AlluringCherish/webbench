# CarRental Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                  | Function Name               | HTTP Method(s) | Template File             | Context Variables                                                                                               |
|-----------------------------|-----------------------------|----------------|---------------------------|----------------------------------------------------------------------------------------------------------------|
| /                           | root_redirect               | GET            | None (redirect)            | None                                                                                                           |
| /dashboard                  | dashboard_page              | GET            | dashboard.html             | featured_vehicles: List[Dict[str, str]], promotions: List[str]                                                 |
| /vehicles                  | vehicle_search              | GET            | vehicle_search.html        | locations: List[str], vehicle_types: List[str], vehicles: List[Dict[str, Any]]                                 |
| /vehicle/<int:vehicle_id>  | vehicle_details             | GET            | vehicle_details.html       | vehicle: Dict[str, Any], reviews: List[Dict[str, str]]                                                        |
| /booking/<int:vehicle_id>  | booking_page                | GET, POST       | booking.html               | vehicle_id: int, locations: List[str], total_price: float or None, booking_form: Dict[str, Any] (POST form data) |
| /insurance/<int:reservation_id> | insurance_options          | GET, POST       | insurance_options.html     | insurance_plans: List[Dict[str, Any]], selected_insurance_id: int or None, reservation_id: int                  |
| /history                   | rental_history              | GET            | rental_history.html        | rentals: List[Dict[str, Any]], status_filter: str                                                              |
| /reservations              | reservation_management       | GET, POST       | reservations.html          | reservations: List[Dict[str, Any]]                                                                              |
| /special-requests          | special_requests             | GET, POST       | special_requests.html      | reservations: List[Dict[str, Any]], submitted: bool or None                                                    |
| /locations                | locations_page               | GET            | locations.html             | locations: List[Dict[str, Any]]                                                                                |


Details:
- Root route `/` redirects to `/dashboard`.
- `dashboard_page` shows featured vehicles and promotions.
- `vehicle_search` allows filtering vehicles by location and type.
- `vehicle_details` shows details of selected vehicle including reviews.
- `booking_page` handles rental booking for a selected vehicle with pickup/dropoff location and date, calculates price.
- `insurance_options` allows choosing insurance for a reservation before confirming booking.
- `rental_history` displays user's rental history with filter by status.
- `reservation_management` allows viewing and managing current and upcoming reservations.
- `special_requests` page allows submitting extra requests for reservations.
- `locations_page` displays all rental locations and allows filtering/searching.

---

## Section 2: HTML Template Specifications (Frontend)

### templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div, main container)
  - featured-vehicles (Div, featured vehicle recommendations)
  - search-vehicles-button (Button, navigate to vehicle search)
  - my-reservations-button (Button, navigate to reservations)
  - promotions-section (Div, current promotions)
- Navigation Mappings:
  - search-vehicles-button: url_for('vehicle_search')
  - my-reservations-button: url_for('reservation_management')
- Context Variables:
  - featured_vehicles: List of dict with keys: vehicle_id (int), make (str), model (str), daily_rate (float)
  - promotions: List of strings

### templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div, main container)
  - location-filter (Dropdown, filter by location)
  - vehicle-type-filter (Dropdown, filter by vehicle type)
  - date-range-input (Input, date range selection)
  - vehicles-grid (Div, displays vehicle cards)
  - view-details-button-{vehicle_id} (Button, view details per vehicle)
- Navigation Mappings:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - locations: List[str]
  - vehicle_types: List[str]
  - vehicles: List of dict with keys: vehicle_id (int), make (str), model (str), daily_rate (float)

### templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div)
  - vehicle-name (H1, vehicle name and model)
  - vehicle-specs (Div, engine, seats, transmission)
  - daily-rate (Div, daily rental rate)
  - book-now-button (Button, book this vehicle)
  - vehicle-reviews (Div, customer reviews)
- Navigation Mappings:
  - book-now-button: url_for('booking_page', vehicle_id=vehicle['vehicle_id'])
- Context Variables:
  - vehicle: Dict[str, Any] with keys vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int), transmission (str), fuel_type (str), status (str)
  - reviews: List[Dict[str, str]] with keys reviewer (str), comment (str)

### templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div)
  - pickup-location (Dropdown)
  - dropoff-location (Dropdown)
  - pickup-date (Input)
  - dropoff-date (Input)
  - calculate-price-button (Button)
  - total-price (Div)
  - proceed-to-insurance-button (Button)
- Navigation Mappings:
  - proceed-to-insurance-button: url_for('insurance_options', reservation_id=some_reservation_id)
- Context Variables:
  - vehicle_id: int
  - locations: List[str]
  - total_price: Optional[float]
  - booking_form: Optional[Dict[str, Any]] (POSTed form fields)

### templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div)
  - insurance-options (Div)
  - select-insurance-{insurance_id} (Radio button for insurance selection)
  - insurance-description (Div)
  - insurance-price (Div)
  - confirm-booking-button (Button)
- Navigation Mappings:
  - confirm-booking-button: Submits POST form to insurance_options endpoint
- Context Variables:
  - insurance_plans: List[Dict[str, Any]] with keys insurance_id (int), plan_name (str), description (str), daily_cost (float)
  - selected_insurance_id: Optional[int]
  - reservation_id: int

### templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div)
  - rentals-table (Table)
  - view-rental-details-{rental_id} (Button)
  - status-filter (Dropdown)
  - back-to-dashboard (Button)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - rentals: List[Dict[str, Any]] with keys rental_id (int), vehicle_id (int), customer_id (int), pickup_date (str), dropoff_date (str), pickup_location (str), dropoff_location (str), total_price (float), status (str)
  - status_filter: str

### templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div)
  - reservations-list (Div)
  - modify-reservation-button-{reservation_id} (Button)
  - cancel-reservation-button-{reservation_id} (Button)
  - sort-by-date-button (Button)
  - back-to-dashboard (Button)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - reservations: List[Dict[str, Any]] with keys reservation_id (int), rental_id (int), vehicle_id (int), customer_id (int), status (str), insurance_id (int), special_requests (str)

### templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div)
  - select-reservation (Dropdown)
  - driver-assistance-checkbox (Checkbox)
  - gps-option-checkbox (Checkbox)
  - child-seat-quantity (Input)
  - special-notes (Textarea)
  - submit-requests-button (Button)
- Navigation Mappings:
  - submit-requests-button: Posts special requests form
- Context Variables:
  - reservations: List[Dict[str, Any]] with keys reservation_id (int), vehicle_id (int), customer_id (int), status (str)
  - submitted: Optional[bool]

### templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div)
  - locations-list (Div)
  - location-detail-button-{location_id} (Button)
  - hours-filter (Dropdown)
  - search-location-input (Input)
  - back-to-dashboard (Button)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - locations: List[Dict[str, Any]] with keys location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)

---

## Section 3: Data File Schemas

### vehicles.txt
- Filename: data/vehicles.txt
- Format (pipe-delimited):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str
  - daily_rate: float
  - seats: int
  - transmission: str
  - fuel_type: str
  - status: str
- Example lines:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

### customers.txt
- Filename: data/customers.txt
- Format (pipe-delimited):
  customer_id|name|email|phone|driver_license|license_expiry
- Fields:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example lines:
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

### locations.txt
- Filename: data/locations.txt
- Format (pipe-delimited):
  location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str
  - available_vehicles: int
- Example lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

### rentals.txt
- Filename: data/rentals.txt
- Format (pipe-delimited):
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Fields:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str
  - dropoff_location: str
  - total_price: float
  - status: str
- Example lines:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

### insurance.txt
- Filename: data/insurance.txt
- Format (pipe-delimited):
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (amount or 'Unlimited')
  - deductible: int
- Example lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

### reservations.txt
- Filename: data/reservations.txt
- Format (pipe-delimited):
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str
  - insurance_id: int
  - special_requests: str
- Example lines:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed

---

This spec allows independent backend and frontend development with consistent naming and data structures.