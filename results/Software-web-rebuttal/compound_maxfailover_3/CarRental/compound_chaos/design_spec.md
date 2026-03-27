# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                   | Function Name           | HTTP Method(s) | Template File         | Context Variables                                                                                                  |
|------------------------------|-------------------------|----------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect           | GET            | N/A (redirect to /dashboard) | None                                                                                                               |
| /dashboard                   | dashboard              | GET            | dashboard.html        | featured_vehicles: list[dict], promotions: list[dict]                                                             |
| /search                     | vehicle_search         | GET            | search.html           | vehicles: list[dict], locations: list[dict], vehicle_types: list[str], filters: dict[str, str]                      |
| /vehicle/<int:vehicle_id>   | vehicle_details        | GET            | vehicle_details.html  | vehicle: dict, reviews: list[dict]                                                                                 |
| /book/<int:vehicle_id>      | booking                | GET, POST      | booking.html          | vehicle: dict, locations: list[dict], price: float (optional), booking_data: dict (optional)                        |
| /insurance/<int:reservation_id> | insurance_options   | GET, POST      | insurance.html        | insurance_plans: list[dict], reservation: dict, selected_insurance: dict (optional)                                |
| /history                   | rental_history         | GET            | rental_history.html   | rentals: list[dict], status_filter: str                                                                            |
| /reservations              | reservation_management | GET            | reservations.html     | reservations: list[dict]                                                                                           |
| /special-requests            | special_requests       | GET, POST      | special_requests.html | reservations: list[dict]                                                                                           |
| /locations                 | locations_page         | GET            | locations.html        | locations: list[dict], hours_filter: str, search_query: str                                                       |

### Route Details

- `/` : Redirects to `/dashboard`.

- `/dashboard` : Displays the dashboard page showing featured vehicles and promotions.

- `/search` : Displays the search page showing a list of vehicles, with filters for pickup location, vehicle type, and rental date range.

- `/vehicle/<int:vehicle_id>` : Displays detailed information for a given vehicle including vehicle specs and customer reviews.

- `/book/<int:vehicle_id>` : Displays booking form for the selected vehicle. Supports POST for submitting booking data and calculating price.

- `/insurance/<int:reservation_id>` : Displays insurance options for a given reservation. POST used to confirm booking.

- `/history` : Displays rental history with optional filtering by rental status.

- `/reservations` : Shows the user's current and upcoming reservations with options to modify or cancel.

- `/special-requests` : Allows user to add special requests to an existing reservation. Supports POST for submitting requests.

- `/locations` : Shows list of rental pickup and dropoff locations with search and filter options.


---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container of dashboard content
  - featured-vehicles (Div): Showcases featured vehicles
  - search-vehicles-button (Button): Navigates to Vehicle Search page
  - my-reservations-button (Button): Navigates to Reservations page
  - promotions-section (Div): Displays promotions
- Navigation:
  - search-vehicles-button: url_for('vehicle_search')
  - my-reservations-button: url_for('reservation_management')
- Context Variables:
  - featured_vehicles: list[dict] with fields vehicle_id:int, make:str, model:str, daily_rate:float
  - promotions: list[dict] with fields title:str, description:str


### 2. Vehicle Search Page
- Filename: templates/search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Main container
  - location-filter (Dropdown): Filter by pickup location
  - vehicle-type-filter (Dropdown): Filter by vehicle type
  - date-range-input (Input): Rental date range selector
  - vehicles-grid (Div): Grid containing vehicle cards
  - view-details-button-{vehicle_id} (Button): Button to view details for each vehicle card
- Navigation:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list[dict] with vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int
  - locations: list[dict] with location_id:int, city:str
  - vehicle_types: list[str] (Economy, Compact, Sedan, SUV, Luxury)
  - filters: dict with keys: location:str, vehicle_type:str, date_range:str


### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container
  - vehicle-name (H1): Vehicle name and model
  - vehicle-specs (Div): Vehicle specifications (engine, seats, transmission)
  - daily-rate (Div): Daily rental rate
  - book-now-button (Button): Button to book this vehicle
  - vehicle-reviews (Div): Customer reviews section
- Navigation:
  - book-now-button: url_for('booking', vehicle_id=vehicle['vehicle_id'])
- Context Variables:
  - vehicle: dict with vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int, transmission:str, fuel_type:str, status:str
  - reviews: list[dict] with reviewer:str, rating:int, comment:str


### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container
  - pickup-location (Dropdown): Select pickup location
  - dropoff-location (Dropdown): Select dropoff location
  - pickup-date (Input): Select pickup date
  - dropoff-date (Input): Select dropoff date
  - calculate-price-button (Button): Calculate total rental price
  - total-price (Div): Show calculated price
  - proceed-to-insurance-button (Button): Proceed to insurance page
- Navigation:
  - proceed-to-insurance-button: url_for('insurance_options', reservation_id=reservation_id_placeholder)
- Context Variables:
  - vehicle: dict with vehicle_id:int, make:str, model:str, daily_rate:float
  - locations: list[dict] with location_id:int, city:str, address:str
  - price: float (optional)
  - booking_data: dict (optional) with keys pickup_location:str, dropoff_location:str, pickup_date:str, dropoff_date:str


### 5. Insurance Options Page
- Filename: templates/insurance.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container
  - insurance-options (Div): Available insurance plans list
  - select-insurance-{insurance_id} (Radio): Radio to select insurance plan
  - insurance-description (Div): Description of selected insurance plan
  - insurance-price (Div): Price of selected insurance plan
  - confirm-booking-button (Button): Confirm booking
- Navigation:
  - confirm-booking-button: url_for('insurance_options', reservation_id=reservation['reservation_id'])
- Context Variables:
  - insurance_plans: list[dict] with insurance_id:int, plan_name:str, description:str, daily_cost:float, coverage_limit:str, deductible:int
  - reservation: dict
  - selected_insurance: dict (optional)


### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container
  - rentals-table (Table): Table showing rental records
  - view-rental-details-{rental_id} (Button): Button to view rental details
  - status-filter (Dropdown): Filter rentals by status
  - back-to-dashboard (Button): Back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - view-rental-details-{rental_id}: url_for('rental_history', rental_id=rental_id) [if implemented]
- Context Variables:
  - rentals: list[dict]
  - status_filter: str


### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container
  - reservations-list (Div): List of reservations
  - modify-reservation-button-{reservation_id} (Button): Modify reservation button
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation button
  - sort-by-date-button (Button): Sort reservations by date
  - back-to-dashboard (Button): Back to dashboard
- Navigation:
  - modify-reservation-button-{reservation_id}: url_for('reservation_management', action='modify', reservation_id=reservation_id)
  - cancel-reservation-button-{reservation_id}: url_for('reservation_management', action='cancel', reservation_id=reservation_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - reservations: list[dict]


### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container
  - select-reservation (Dropdown): Select reservation
  - driver-assistance-checkbox (Checkbox): Driver assistance request
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Additional notes
  - submit-requests-button (Button): Submit special requests
- Navigation:
  - submit-requests-button: url_for('special_requests')
- Context Variables:
  - reservations: list[dict]


### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container
  - locations-list (Div): List of locations
  - location-detail-button-{location_id} (Button): View location details
  - hours-filter (Dropdown): Filter by operating hours
  - search-location-input (Input): Search locations
  - back-to-dashboard (Button): Back to dashboard
- Navigation:
  - location-detail-button-{location_id}: url_for('locations_page', location_id=location_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - locations: list[dict]
  - hours_filter: str
  - search_query: str


---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Description: Stores details of vehicles available for rent.
- Format (pipe-delimited, no header):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str (Petrol, Diesel)
  - status: str (Available, Rented, Maintenance)
- Examples:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. customers.txt
- Description: Stores customer information.
- Format:
  customer_id|name|email|phone|driver_license|license_expiry
- Fields:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Examples:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. locations.txt
- Description: Stores rental location information.
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., '24/7', '09:00-18:00')
  - available_vehicles: int
- Examples:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. rentals.txt
- Description: Stores rental transaction details.
- Format:
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
  - status: str (Completed, Active, Cancelled)
- Examples:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. insurance.txt
- Description: Stores insurance plan options.
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (number or 'Unlimited')
  - deductible: int
- Examples:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. reservations.txt
- Description: Stores reservation data linked to rentals.
- Format:
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Examples:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

This comprehensive specification enables backend developers and frontend developers to independently implement their parts for the CarRental web application without ambiguity or dependencies.