# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name               | HTTP Method(s) | Template File              | Context Variables                                                                                  |
|----------------------------|-----------------------------|----------------|----------------------------|--------------------------------------------------------------------------------------------------|
| /                          | root_redirect               | GET            | N/A (redirect to /dashboard) | None                                                                                             |
| /dashboard                 | dashboard                  | GET            | dashboard.html              | featured_vehicles: list[dict], promotions: list[dict]                                           |
| /search                   | vehicle_search             | GET            | search.html                 | vehicles: list[dict], locations: list[dict], vehicle_types: list[str]                           |
| /vehicle/<int:vehicle_id>  | vehicle_details            | GET            | vehicle_details.html        | vehicle: dict, reviews: list[dict]                                                              |
| /booking/<int:vehicle_id>  | booking                   | GET, POST      | booking.html                | locations: list[dict], booking_form_data: dict (for POST: pickup_location:str, dropoff_location:str, pickup_date:str (YYYY-MM-DD), dropoff_date:str (YYYY-MM-DD), total_price:float)
| /insurance/<int:reservation_id> | insurance_options      | GET, POST      | insurance.html              | insurance_plans: list[dict], selected_plan: dict or None, reservation_id: int                     |
| /history                  | rental_history             | GET            | rental_history.html         | rentals: list[dict], filter_status: str                                                          |
| /reservations             | reservation_management      | GET            | reservations.html           | reservations: list[dict]                                                                          |
| /special_requests         | special_requests           | GET, POST      | special_requests.html       | reservations: list[dict], submitted_data: dict or None                                           |
| /locations                | locations                  | GET            | locations.html              | locations: list[dict], hours_filter_options: list[str]                                         |

### Routes Details:

- **/**: Redirects to `/dashboard`.
- **/dashboard**: Shows main dashboard with featured vehicles and promotions.
- **/search**: Displays all available vehicles with filters for location and type.
- **/vehicle/<vehicle_id>**: Shows detailed information about a selected vehicle.
- **/booking/<vehicle_id>**: Allows booking input for specified vehicle; processes booking form data.
- **/insurance/<reservation_id>**: Displays insurance options to select for given reservation.
- **/history**: Shows rental history with filtering on status.
- **/reservations**: Manages current and upcoming reservations with modification and cancellation.
- **/special_requests**: Form to add requests for existing reservations.
- **/locations**: Displays pickup/dropoff locations with filters and search.

All context variables closely map to fields outlined in data schemas (Section 3) or form input fields defined in Section 2.


---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Elements:
  - `dashboard-page`: Div container for dashboard page
  - `featured-vehicles`: Div showing featured vehicle recommendations
  - `search-vehicles-button`: Button navigating to the vehicle search page (url_for('vehicle_search'))
  - `my-reservations-button`: Button navigating to reservations page (url_for('reservation_management'))
  - `promotions-section`: Div displaying current promotions
- Context Variables:
  - `featured_vehicles`: list of dict with keys: vehicle_id (int), make (str), model (str), daily_rate (float)
  - `promotions`: list of dict with keys: title (str), description (str)

### 2. Vehicle Search Page
- Filename: templates/search.html
- Page Title: Search Vehicles
- Elements:
  - `search-page`: Div container
  - `location-filter`: Dropdown for pickup location filter
  - `vehicle-type-filter`: Dropdown for vehicle type (Economy, Compact, Sedan, SUV, Luxury)
  - `date-range-input`: Input field for rental date range
  - `vehicles-grid`: Div container for vehicle cards
  - `view-details-button-{vehicle_id}`: Button on each vehicle card to view details
- Context Variables:
  - `vehicles`: list of dict with vehicle details matching data schema:
    - vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int), transmission (str), fuel_type (str), status (str)
  - `locations`: list of dict for filtering pickup locations:
    - location_id (int), city (str), address (str)
  - `vehicle_types`: list[str] vehicle categories (Economy, Compact, Sedan, SUV, Luxury)

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Elements:
  - `vehicle-details-page`: Div container
  - `vehicle-name`: H1 displaying full vehicle name and model
  - `vehicle-specs`: Div showing specs - engine (str), seats (int), transmission (str)
  - `daily-rate`: Div showing daily rental rate
  - `book-now-button`: Button navigating to booking for this vehicle (url_for('booking', vehicle_id=vehicle.vehicle_id))
  - `vehicle-reviews`: Div displaying customer reviews
- Context Variables:
  - `vehicle`: dict from vehicles.txt with all vehicle details
  - `reviews`: list of dict with keys: reviewer_name (str), rating (int 1-5), comment (str)

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Elements:
  - `booking-page`: Div container
  - `pickup-location`: Dropdown for selecting pickup location
  - `dropoff-location`: Dropdown for dropoff location
  - `pickup-date`: Input (date)
  - `dropoff-date`: Input (date)
  - `calculate-price-button`: Button to calculate price
  - `total-price`: Div to display total rental price
  - `proceed-to-insurance-button`: Button navigating to insurance options
- Context Variables:
  - `locations`: list of dict (location_id:int, city:str, address:str)
  - `booking_form_data`: dict with form input values and calculated total_price (float)

### 5. Insurance Options Page
- Filename: templates/insurance.html
- Page Title: Select Insurance Coverage
- Elements:
  - `insurance-page`: Div container
  - `insurance-options`: Div listing insurance plans
  - `select-insurance-{insurance_id}`: Radio button for each insurance plan
  - `insurance-description`: Div displaying description of selected plan
  - `insurance-price`: Div displaying daily insurance price
  - `confirm-booking-button`: Button to confirm booking with selected insurance
- Context Variables:
  - `insurance_plans`: list of dict with insurance data fields
  - `selected_plan`: dict or None
  - `reservation_id`: int

### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Elements:
  - `history-page`: Div container
  - `rentals-table`: Table with columns: rental_id, vehicle info, dates, location, status
  - `view-rental-details-{rental_id}`: Button for each rental to view detailed info
  - `status-filter`: Dropdown to filter rental status (All, Active, Completed, Cancelled)
  - `back-to-dashboard`: Button navigates to dashboard
- Context Variables:
  - `rentals`: list of dict with rental data
  - `filter_status`: str current status filter

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Elements:
  - `reservations-page`: Div container
  - `reservations-list`: Div listing reservations
  - `modify-reservation-button-{reservation_id}`: Button for modifying reservation
  - `cancel-reservation-button-{reservation_id}`: Button for cancelling reservation
  - `sort-by-date-button`: Button to sort by date
  - `back-to-dashboard`: Button to dashboard
- Context Variables:
  - `reservations`: list of dict from reservations.txt

### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Elements:
  - `requests-page`: Div container
  - `select-reservation`: Dropdown to select reservation
  - `driver-assistance-checkbox`: Checkbox
  - `gps-option-checkbox`: Checkbox
  - `child-seat-quantity`: Input (number)
  - `special-notes`: Textarea
  - `submit-requests-button`: Button to submit
- Context Variables:
  - `reservations`: list of dict from reservations.txt
  - `submitted_data`: dict or None for data after submission

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Elements:
  - `locations-page`: Div container
  - `locations-list`: Div listing all locations
  - `location-detail-button-{location_id}`: Button to view location details
  - `hours-filter`: Dropdown filter (24/7, Business Hours, Weekend)
  - `search-location-input`: Input for city/name search
  - `back-to-dashboard`: Button to dashboard
- Context Variables:
  - `locations`: list of dict from locations.txt
  - `hours_filter_options`: list[str] for hours filter choices

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Stores all vehicle information.
- Format (pipe-delimited):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Field Types:
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
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

### 2. customers.txt
- Stores customer profiles.
- Format:
  customer_id|name|email|phone|driver_license|license_expiry
- Field Types:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example Lines:
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

### 3. locations.txt
- Stores rental pickup/dropoff locations.
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Field Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str
  - available_vehicles: int
- Example Lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

### 4. rentals.txt
- Stores vehicle rental records.
- Format:
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Field Types:
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
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

### 5. insurance.txt
- Stores insurance coverage plans.
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Example Lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

### 6. reservations.txt
- Stores rental reservations.
- Format:
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str
  - insurance_id: int
  - special_requests: str
- Example Lines:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed

---

# End of Design Specifications
