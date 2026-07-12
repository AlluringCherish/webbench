# CarRental Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                    | Function Name               | HTTP Method(s) | Template File            | Context Variables                                                                                  |
|------------------------------|-----------------------------|----------------|--------------------------|--------------------------------------------------------------------------------------------------|
| /                            | root_redirect               | GET            | (redirect to /dashboard)  | None                                                                                             |
| /dashboard                   | dashboard_page              | GET            | dashboard.html           | featured_vehicles: list[dict], promotions: list[str]                                            |
| /vehicles                   | vehicle_search_page          | GET            | vehicle_search.html      | vehicles: list[dict], locations: list[str], vehicle_types: list[str]                             |
| /vehicles/<int:vehicle_id>   | vehicle_details_page        | GET            | vehicle_details.html     | vehicle: dict, reviews: list[str]                                                               |
| /vehicles/<int:vehicle_id>/book | booking_page             | GET, POST      | booking.html             | vehicle: dict, locations: list[str], pickup_date: str (optional), dropoff_date: str (optional), total_price: float (optional) |
| /insurance                   | insurance_options_page      | GET, POST      | insurance_options.html   | insurance_plans: list[dict], selected_insurance: dict (optional)                                |
| /rentals/history             | rental_history_page         | GET            | rental_history.html      | rentals: list[dict], filter_status: str                                                           |
| /reservations                | reservation_management_page | GET, POST      | reservations.html        | reservations: list[dict]                                                                          |
| /special-requests            | special_requests_page       | GET, POST      | special_requests.html    | reservations: list[dict], special_requests_form_data: dict (optional)                            |
| /locations                  | locations_page              | GET            | locations.html           | locations: list[dict]                                                                             |

Notes:
- The root route '/' redirects to '/dashboard'.
- Function names are descriptive and lowercase with underscores.
- Context variables correspond exactly to data schema fields or form inputs.
- Navigation routes correspond to page buttons and links as described.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-vehicles (Div): Display of featured vehicle recommendations.
  - search-vehicles-button (Button): Navigate to vehicle search page.
  - my-reservations-button (Button): Navigate to reservations page.
  - promotions-section (Div): Display of current promotions and offers.
- Navigation Mappings:
  - search-vehicles-button: url_for('vehicle_search_page')
  - my-reservations-button: url_for('reservation_management_page')
- Context Variables:
  - featured_vehicles: list of dicts with vehicle info (vehicle_id:int, make:str, model:str, daily_rate:float)
  - promotions: list of str

### 2. Vehicle Search Page
- Filename: templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for the search page.
  - location-filter (Dropdown): Filter by pickup location.
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - date-range-input (Input): Select rental date range.
  - vehicles-grid (Div): Grid displaying vehicle cards.
  - view-details-button-{vehicle_id} (Button): Button for each vehicle to view details.
- Navigation Mappings:
  - view-details-button-{vehicle_id}: url_for('vehicle_details_page', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list of dicts (vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int, transmission:str, fuel_type:str, status:str)
  - locations: list of str
  - vehicle_types: list of str [Economy, Compact, Sedan, SUV, Luxury]

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container.
  - vehicle-name (H1): Vehicle name and model.
  - vehicle-specs (Div): Specs - engine (not in data, so omit), seats, transmission.
  - daily-rate (Div): Daily rental rate.
  - book-now-button (Button): Book this vehicle.
  - vehicle-reviews (Div): Customer reviews.
- Navigation Mappings:
  - book-now-button: url_for('booking_page', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: dict (vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int, transmission:str, fuel_type:str, status:str)
  - reviews: list of str

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container.
  - pickup-location (Dropdown): Select pickup location.
  - dropoff-location (Dropdown): Select dropoff location.
  - pickup-date (Input): Pickup date.
  - dropoff-date (Input): Dropoff date.
  - calculate-price-button (Button): Calculate total rental price.
  - total-price (Div): Display total price.
  - proceed-to-insurance-button (Button): Proceed to insurance options.
- Navigation Mappings:
  - proceed-to-insurance-button: url_for('insurance_options_page')
- Context Variables:
  - vehicle: dict
  - locations: list of str
  - pickup_date: str
  - dropoff_date: str
  - total_price: float

### 5. Insurance Options Page
- Filename: templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container.
  - insurance-options (Div): Available insurance plans.
  - select-insurance-{insurance_id} (Radio): Select insurance plan.
  - insurance-description (Div): Description of selected plan.
  - insurance-price (Div): Insurance price.
  - confirm-booking-button (Button): Confirm booking.
- Navigation Mappings:
  - confirm-booking-button: Submit POST to /insurance
- Context Variables:
  - insurance_plans: list of dict (insurance_id:int, plan_name:str, description:str, daily_cost:float, coverage_limit:int or str, deductible:int)
  - selected_insurance: dict (optional)

### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container.
  - rentals-table (Table): Display rentals.
  - view-rental-details-{rental_id} (Button): View rental details.
  - status-filter (Dropdown): Filter by status (All, Active, Completed, Cancelled).
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - rentals: list of dict (rental_id:int, vehicle_id:int, customer_id:int, pickup_date:str, dropoff_date:str, pickup_location:str, dropoff_location:str, total_price:float, status:str)
  - filter_status: str

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container.
  - reservations-list (Div): List of reservations.
  - modify-reservation-button-{reservation_id} (Button): Modify reservation.
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation.
  - sort-by-date-button (Button): Sort reservations by date.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - reservations: list of dict (reservation_id:int, rental_id:int, vehicle_id:int, customer_id:int, status:str, insurance_id:int, special_requests:str)

### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container.
  - select-reservation (Dropdown): Select reservation.
  - driver-assistance-checkbox (Checkbox): Driver assistance request.
  - gps-option-checkbox (Checkbox): GPS option.
  - child-seat-quantity (Input): Number of child seats.
  - special-notes (Textarea): Special notes.
  - submit-requests-button (Button): Submit special requests.
- Navigation Mappings:
  - submit-requests-button: POST to /special-requests
- Context Variables:
  - reservations: list of dict (reservation_id:int, rental_id:int, vehicle_id:int, customer_id:int, status:str, insurance_id:int, special_requests:str)
  - special_requests_form_data: dict (optional)

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container.
  - locations-list (Div): List of locations.
  - location-detail-button-{location_id} (Button): View location details.
  - hours-filter (Dropdown): Filter by operating hours.
  - search-location-input (Input): Search locations by city or name.
  - back-to-dashboard (Button): Navigate to dashboard.
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Context Variables:
  - locations: list of dict (location_id:int, city:str, address:str, phone:str, hours:str, available_vehicles:int)

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Stores all vehicle details.
- Format (pipe-delimited):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields and types:
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

### 2. customers.txt
- Stores customer details.
- Format (pipe-delimited):
  customer_id|name|email|phone|driver_license|license_expiry
- Fields and types:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example lines:
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

### 3. locations.txt
- Stores rental pickup and dropoff locations.
- Format (pipe-delimited):
  location_id|city|address|phone|hours|available_vehicles
- Fields and types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str
  - available_vehicles: int
- Example lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

### 4. rentals.txt
- Stores rental records.
- Format (pipe-delimited):
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Fields and types:
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

### 5. insurance.txt
- Stores insurance plan details.
- Format (pipe-delimited):
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields and types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: int or str (e.g., 'Unlimited')
  - deductible: int
- Example lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

### 6. reservations.txt
- Stores reservations associated with rentals.
- Format (pipe-delimited):
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields and types:
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


# End of Design Specifications
