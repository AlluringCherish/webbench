# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name              | HTTP Method(s) | Template File            | Context Variables                                                                                      |
|----------------------------|----------------------------|----------------|--------------------------|------------------------------------------------------------------------------------------------------|
| /                          | redirect_to_dashboard       | GET            | N/A (redirect)            | N/A                                                                                                  |
| /dashboard                 | dashboard                  | GET            | dashboard.html            | featured_vehicles: list[dict], promotions: list[dict]                                                |
| /search-vehicles           | search_vehicles            | GET            | vehicle_search.html       | locations: list[dict], vehicle_types: list[str], filtered_vehicles: list[dict], search_filters: dict |
| /vehicle/<int:vehicle_id>  | vehicle_details            | GET            | vehicle_details.html      | vehicle: dict, reviews: list[dict]                                                                   |
| /booking/<int:vehicle_id>  | booking                   | GET, POST      | booking.html              | vehicle: dict, locations: list[dict], pickup_location: str (POST), dropoff_location: str (POST), pickup_date: str (POST), dropoff_date: str (POST), total_price: float (POST or None) |
| /insurance/<int:reservation_id> | insurance_options     | GET, POST      | insurance_options.html    | insurance_plans: list[dict], selected_plan: dict (POST or None), reservation_id: int                  |
| /rental-history            | rental_history             | GET            | rental_history.html       | rentals: list[dict], status_filter: str                                                               |
| /my-reservations           | my_reservations            | GET            | reservations.html         | reservations: list[dict]                                                                              |
| /modify-reservation/<int:reservation_id> | modify_reservation | GET, POST      | modify_reservation.html  | reservation: dict, action_result: str (POST or None)                                                |
| /cancel-reservation/<int:reservation_id> | cancel_reservation | POST      | redirect (back to my-reservations) | N/A                                                                                            |
| /special-requests          | special_requests           | GET, POST      | special_requests.html     | reservations: list[dict], submitted_request_result: str (POST or None)                              |
| /locations                 | locations                  | GET            | locations.html            | locations_list: list[dict], filters: dict                                                            |


**Details:**
- Root `/` redirects to `/dashboard`.
- Context variable types use Python typing style.
- POST methods handle form submissions with relevant variables.
- Navigation routes match page link/button functionalities.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - `dashboard-page` (Div): Main container for dashboard
  - `featured-vehicles` (Div): Featured vehicle recommendations
  - `search-vehicles-button` (Button): Navigate to vehicle search (url_for('search_vehicles'))
  - `my-reservations-button` (Button): Navigate to reservations (url_for('my_reservations'))
  - `promotions-section` (Div): Current promotions and offers
- Context Variables:
  - `featured_vehicles`: list of dictionaries containing vehicle info
  - `promotions`: list of dictionaries for current promotions

### 2. templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - `search-page` (Div): Container
  - `location-filter` (Dropdown/select): Filter by pickup location
  - `vehicle-type-filter` (Dropdown/select): Filter by vehicle type
  - `date-range-input` (Input): Rental date range selection
  - `vehicles-grid` (Div): Grid showing vehicle cards
  - `view-details-button-{vehicle_id}` (Button): View details for each vehicle
- Navigation Mappings:
  - `view-details-button-{vehicle_id}` triggers link to url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - `locations`: list of location dictionaries
  - `vehicle_types`: list of vehicle type strings
  - `filtered_vehicles`: list of vehicle dictionaries matching filters
  - `search_filters`: dict of current applied filters

### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - `vehicle-details-page` (Div)
  - `vehicle-name` (H1): Vehicle make and model
  - `vehicle-specs` (Div): Details like engine, seats, transmission
  - `daily-rate` (Div): Daily rental rate
  - `book-now-button` (Button): Link to booking page for this vehicle (url_for('booking', vehicle_id=vehicle['vehicle_id']))
  - `vehicle-reviews` (Div): Customer reviews section
- Context Variables:
  - `vehicle`: dict with all vehicle details
  - `reviews`: list of review dictionaries

### 4. templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - `booking-page` (Div)
  - `pickup-location` (Dropdown/select): Pickup location selection
  - `dropoff-location` (Dropdown/select): Dropoff location selection
  - `pickup-date` (Input, date)
  - `dropoff-date` (Input, date)
  - `calculate-price-button` (Button)
  - `total-price` (Div): Show calculated price
  - `proceed-to-insurance-button` (Button): Link to insurance options (url_for('insurance_options', reservation_id=reservation_id))
- Context Variables:
  - `vehicle`: dict
  - `locations`: list of location dicts
  - `pickup_location`, `dropoff_location`, `pickup_date`, `dropoff_date`: str user input
  - `total_price`: float or None

### 5. templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - `insurance-page` (Div)
  - `insurance-options` (Div): List of insurance plans
  - `select-insurance-{insurance_id}` (Radio buttons)
  - `insurance-description` (Div): Description of selected plan
  - `insurance-price` (Div): Price of selected plan
  - `confirm-booking-button` (Button): Finalize booking
- Context Variables:
  - `insurance_plans`: list of dicts
  - `selected_plan`: dict or None
  - `reservation_id`: int

### 6. templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - `history-page` (Div)
  - `rentals-table` (Table): Columns for ID, vehicle, dates, location, status
  - `view-rental-details-{rental_id}` (Button)
  - `status-filter` (Dropdown)
  - `back-to-dashboard` (Button): url_for('dashboard')
- Context Variables:
  - `rentals`: list of dicts
  - `status_filter`: str

### 7. templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - `reservations-page` (Div)
  - `reservations-list` (Div): Each reservation with vehicle, dates, status
  - `modify-reservation-button-{reservation_id}` (Button)
  - `cancel-reservation-button-{reservation_id}` (Button)
  - `sort-by-date-button` (Button)
  - `back-to-dashboard` (Button): url_for('dashboard')
- Context Variables:
  - `reservations`: list of dicts

### 8. templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - `requests-page` (Div)
  - `select-reservation` (Dropdown/select)
  - `driver-assistance-checkbox` (Checkbox)
  - `gps-option-checkbox` (Checkbox)
  - `child-seat-quantity` (Input, number)
  - `special-notes` (Textarea)
  - `submit-requests-button` (Button)
- Context Variables:
  - `reservations`: list of dicts
  - `submitted_request_result`: str or None

### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - `locations-page` (Div)
  - `locations-list` (Div)
  - `location-detail-button-{location_id}` (Button)
  - `hours-filter` (Dropdown/select)
  - `search-location-input` (Input)
  - `back-to-dashboard` (Button): url_for('dashboard')
- Context Variables:
  - `locations_list`: list of dicts
  - `filters`: dict

---

## Section 3: Data File Schemas

### 1. data/vehicles.txt
- Format (pipe-delimited):
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
```
- Field Types:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (e.g., Automatic)
  - fuel_type: str (e.g., Petrol, Diesel)
  - status: str (Available, etc.)
- Example Lines:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```
- Description: Stores all vehicle listing details for the rental fleet.

### 2. data/customers.txt
- Format:
```
customer_id|name|email|phone|driver_license|license_expiry
```
- Field Types:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example Lines:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```
- Description: Stores customer personal and license information.

### 3. data/locations.txt
- Format:
```
location_id|city|address|phone|hours|available_vehicles
```
- Field Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., 24/7, 09:00-18:00)
  - available_vehicles: int
- Example Lines:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```
- Description: Stores rental pickup and dropoff location details.

### 4. data/rentals.txt
- Format:
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
```
- Field Types:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str
  - dropoff_location: str
  - total_price: float
  - status: str (Completed, Active, etc.)
- Example Lines:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```
- Description: Stores rental transaction details.

### 5. data/insurance.txt
- Format:
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
```
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str or int (e.g., 50000 or 'Unlimited')
  - deductible: int
- Example Lines:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```
- Description: Stores available insurance coverage plans.

### 6. data/reservations.txt
- Format:
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
```
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, etc.)
  - insurance_id: int
  - special_requests: str
- Example Lines:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```
- Description: Stores reservation details with insurance and special requests.

---

This design specification enables complete independent development of backend and frontend code for the CarRental application while ensuring data consistency and UI correctness.