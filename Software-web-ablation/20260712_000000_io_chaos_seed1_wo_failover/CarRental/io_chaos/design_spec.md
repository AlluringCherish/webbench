# CarRental Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                           | Function Name              | HTTP Method(s) | Template File               | Context Variables                                                                                                   |
|------------------------------------|----------------------------|----------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------|
| /                                  | root_redirect              | GET            | N/A (redirect to /dashboard) | None                                                                                                              |
| /dashboard                        | dashboard_page            | GET            | dashboard.html              | featured_vehicles: list of dict {vehicle_id: int, make: str, model: str, daily_rate: float}, promotions: list of str    |
| /vehicles                        | vehicle_search            | GET            | vehicle_search.html         | vehicles: list of dict {vehicle_id: int, make: str, model: str, vehicle_type: str, daily_rate: float, seats: int}, filters: dict {locations: list of str, vehicle_types: list of str}, selected_location: str or None, selected_vehicle_type: str or None, selected_date_range: str or None                        |
| /vehicle/<int:vehicle_id>         | vehicle_details           | GET            | vehicle_details.html        | vehicle: dict {vehicle_id: int, make: str, model: str, vehicle_type: str, daily_rate: float, seats: int, transmission: str, fuel_type: str, status: str}, reviews: list of str                                           |
| /booking/<int:vehicle_id>          | booking_page              | GET, POST      | booking.html                | vehicle: dict {vehicle_id: int, make: str, model: str, daily_rate: float}, pickup_locations: list of str, dropoff_locations: list of str, total_price: float or None, booking_form_data: dict for POST fields                                     |
| /insurance/<int:booking_id>        | insurance_options_page    | GET, POST      | insurance_options.html      | insurance_plans: list of dict {insurance_id: int, plan_name: str, description: str, daily_cost: float, coverage_limit: str, deductible: int}, selected_insurance_id: int or None, booking_id: int                              |
| /rental-history                   | rental_history            | GET            | rental_history.html         | rentals: list of dict {rental_id: int, vehicle: str, pickup_date: str, dropoff_date: str, pickup_location: str, dropoff_location: str, status: str}, status_filter: str                                                 |
| /reservations                    | reservation_management    | GET, POST      | reservation_management.html | reservations: list of dict {reservation_id: int, vehicle: str, pickup_date: str, dropoff_date: str, status: str}, filter_date_sorted: bool                                       |
| /reservation/modify/<int:reservation_id>  | modify_reservation        | POST           | N/A                         | modification_data: dict POST                                                                                         |
| /reservation/cancel/<int:reservation_id>  | cancel_reservation        | POST           | N/A                         | cancellation_confirmation: str                                                                                      |
| /special-requests                | special_requests          | GET, POST      | special_requests.html       | reservations: list of dict {reservation_id: int, vehicle: str, pickup_date: str, dropoff_date: str, status: str}, form_data: dict (POST request)                              |
| /locations                      | locations_page            | GET            | locations.html              | locations: list of dict {location_id: int, city: str, address: str, phone: str, hours: str, available_vehicles: int}, filter_hours: str, search_query: str                      |

---

## Section 2: HTML Template Specifications (Frontend)

---

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-vehicles (Div): Display of featured vehicle recommendations
  - search-vehicles-button (Button): Button to navigate to vehicle search page
  - my-reservations-button (Button): Button to navigate to reservations page
  - promotions-section (Div): Display of current promotions and offers
- Navigation:
  - search-vehicles-button -> url_for('vehicle_search')
  - my-reservations-button -> url_for('reservation_management')
- Context Variables:
  - featured_vehicles: List of dicts with keys: vehicle_id (int), make (str), model (str), daily_rate (float)
  - promotions: List of strings

---

### 2. templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for the search page
  - location-filter (Dropdown): Filter by pickup location
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury)
  - date-range-input (Input): Rental date range input
  - vehicles-grid (Div): Grid of vehicle cards
  - view-details-button-{vehicle_id} (Button): Button to view vehicle details, dynamic element with vehicle_id in ID
- Navigation:
  - view-details-button-{vehicle_id} -> url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: List of dicts with keys: vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int)
  - filters: Dict containing lists 'locations' (str), 'vehicle_types' (str)
  - selected_location: Optional str
  - selected_vehicle_type: Optional str
  - selected_date_range: Optional str

---

### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container for the vehicle details page
  - vehicle-name (H1): Display vehicle name and model
  - vehicle-specs (Div): Display vehicle engine, seats, transmission
  - daily-rate (Div): Display daily rental rate
  - book-now-button (Button): Button to book this vehicle
  - vehicle-reviews (Div): Customer reviews section
- Navigation:
  - book-now-button -> url_for('booking_page', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: Dict with keys vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int), transmission (str), fuel_type (str), status (str)
  - reviews: List of strings

---

### 4. templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container for the booking page
  - pickup-location (Dropdown): Pickup location selection
  - dropoff-location (Dropdown): Dropoff location selection
  - pickup-date (Input): Pickup date
  - dropoff-date (Input): Dropoff date
  - calculate-price-button (Button): Button to calculate total price
  - total-price (Div): Displays calculated total price
  - proceed-to-insurance-button (Button): Button to proceed to insurance options
- Navigation:
  - proceed-to-insurance-button -> url_for('insurance_options_page', booking_id=booking_id)
- Context Variables:
  - vehicle: Dict with vehicle details vehicle_id (int), make (str), model (str), daily_rate (float)
  - pickup_locations: List of strings
  - dropoff_locations: List of strings
  - total_price: Float or None
  - booking_form_data: Dict (for form values on POST)

---

### 5. templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container for insurance options
  - insurance-options (Div): Displays insurance plans
  - select-insurance-{insurance_id} (Radio): Radio button for each insurance plan, dynamic element with insurance_id in ID
  - insurance-description (Div): Shows description of selected plan
  - insurance-price (Div): Shows price of selected plan
  - confirm-booking-button (Button): Confirm booking with insurance
- Navigation:
  - confirm-booking-button -> POST to confirm booking
- Context Variables:
  - insurance_plans: List dict with insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (str), deductible (int)
  - selected_insurance_id: int or None
  - booking_id: int

---

### 6. templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container for rental history
  - rentals-table (Table): Table with rentals info
  - view-rental-details-{rental_id} (Button): Dynamic button
  - status-filter (Dropdown): Filter by rental status
  - back-to-dashboard (Button): Navigation back
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - rentals: List dict with rental_id (int), vehicle (str), pickup_date (str), dropoff_date (str), pickup_location (str), dropoff_location (str), status (str)
  - status_filter: str

---

### 7. templates/reservation_management.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container for reservations page
  - reservations-list (Div): List of reservations
  - modify-reservation-button-{reservation_id} (Button): Dynamic modify buttons
  - cancel-reservation-button-{reservation_id} (Button): Dynamic cancel buttons
  - sort-by-date-button (Button): Sort reservations
  - back-to-dashboard (Button): Navigate back
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - reservations: List dict with reservation_id (int), vehicle (str), pickup_date (str), dropoff_date (str), status (str)
  - filter_date_sorted: bool

---

### 8. templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container for special requests
  - select-reservation (Dropdown): Select reservation
  - driver-assistance-checkbox (Checkbox): Driver assistance option
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Notes input
  - submit-requests-button (Button): Submit requests
- Navigation:
  - submit-requests-button -> POST form
- Context Variables:
  - reservations: List dict with reservation_id (int), vehicle (str), pickup_date (str), dropoff_date (str), status (str)
  - form_data: dict (POST form fields)

---

### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container for locations page
  - locations-list (Div): List of locations
  - location-detail-button-{location_id} (Button): View location detail, dynamic
  - hours-filter (Dropdown): Filter by operating hours
  - search-location-input (Input): Search by city or name
  - back-to-dashboard (Button): Navigate back
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - locations: List dict with location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)
  - filter_hours: str
  - search_query: str

---

## Section 3: Data File Schemas

---

### 1. vehicles.txt
- File: data/vehicles.txt
- Format: vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
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
- Example Lines:
  - 1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  - 2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  - 3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
- Description: Stores all vehicle details for rental availability and pricing.

---

### 2. customers.txt
- File: data/customers.txt
- Format: customer_id|name|email|phone|driver_license|license_expiry
- Fields:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example Lines:
  - 1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  - 2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
- Description: Stores customer personal and driving license information.

---

### 3. locations.txt
- File: data/locations.txt
- Format: location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str
  - available_vehicles: int
- Example Lines:
  - 1|New York|123 Main St, NYC|555-1000|24/7|12
  - 2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
- Description: Stores pickup and dropoff location details.

---

### 4. rentals.txt
- File: data/rentals.txt
- Format: rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
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
- Example Lines:
  - 1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  - 2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
- Description: Stores all rental transaction details.

---

### 5. insurance.txt
- File: data/insurance.txt
- Format: insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Example Lines:
  - 1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  - 2|Standard Coverage|Collision and theft protection|12.00|250000|500
  - 3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
- Description: Stores insurance plans available for rentals.

---

### 6. reservations.txt
- File: data/reservations.txt
- Format: reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str
  - insurance_id: int
  - special_requests: str
- Example Lines:
  - 1|1|1|1|Confirmed|2|Driver assistance requested
  - 2|2|2|2|Active|1|GPS and child seat needed
- Description: Stores reservation details including status and special requests.

