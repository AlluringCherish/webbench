# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path               | Function Name             | HTTP Method(s) | Template File           | Context Variables                                                                                     |
|--------------------------|---------------------------|----------------|-------------------------|-----------------------------------------------------------------------------------------------------|
| /                        | root_redirect             | GET            | N/A (Redirect)          | None                                                                                                |
| /dashboard               | dashboard_page            | GET            | dashboard.html          | featured_vehicles: list[dict], promotions: list[dict]                                               |
| /vehicles                | vehicle_search_page       | GET            | vehicle_search.html     | vehicles: list[dict], locations: list[dict], filters: dict (keys: location(str), vehicle_type(str)) |
| /vehicle/<int:vehicle_id>| vehicle_details_page      | GET            | vehicle_details.html    | vehicle: dict, reviews: list[dict]                                                                  |
| /booking/<int:vehicle_id>| booking_page              | GET, POST      | booking.html            | vehicle: dict, locations: list[dict], pickup_date: str, dropoff_date: str, total_price: float        |
| /insurance/<int:reservation_id>| insurance_options_page | GET, POST | insurance_options.html  | insurance_plans: list[dict], selected_insurance: dict, reservation_id: int                           |
| /rental-history          | rental_history_page       | GET            | rental_history.html     | rentals: list[dict], filter_status: str                                                             |
| /reservations            | reservation_management_page| GET, POST      | reservations.html       | reservations: list[dict]                                                                             |
| /reservation/modify/<int:reservation_id>| modify_reservation_page | POST      | N/A                   | reservation_id: int, updated_data: dict                                                             |
| /reservation/cancel/<int:reservation_id>| cancel_reservation_page  | POST      | N/A                   | reservation_id: int                                                                                  |
| /special-requests        | special_requests_page     | GET, POST      | special_requests.html   | reservations: list[dict], submitted_data: dict                                                      |
| /locations               | locations_page            | GET            | locations.html          | locations: list[dict]                                                                               |

**Notes:**
- The root route `/` redirects to `/dashboard`.
- Context variable names follow data schemas closely.
- POST methods are included where user input will be processed.


## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-vehicles (Div): Display featured vehicles (iterate list of dicts with vehicle info)
  - search-vehicles-button (Button): Navigates to vehicle_search_page
  - my-reservations-button (Button): Navigates to reservation_management_page
  - promotions-section (Div): Displays promotions list
- Navigation mappings:
  - `url_for('vehicle_search_page')` for search-vehicles-button
  - `url_for('reservation_management_page')` for my-reservations-button
- Context variables:
  - featured_vehicles: list of dicts {vehicle_id:int, make:str, model:str, daily_rate:float}
  - promotions: list of dicts {title:str, description:str}

### 2. Vehicle Search Page
- Filename: templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Main container
  - location-filter (Dropdown): Options from locations data (city names)
  - vehicle-type-filter (Dropdown): Static options [Economy, Compact, Sedan, SUV, Luxury]
  - date-range-input (Input): Date range selector (string or two date inputs)
  - vehicles-grid (Div): Grid container for vehicle cards
  - view-details-button-{vehicle_id} (Button): For each vehicle card
- Navigation mappings:
  - `url_for('vehicle_details_page', vehicle_id=vehicle_id)` for view-details-button
- Context variables:
  - vehicles: list of dicts from vehicles.txt
  - locations: list of dicts from locations.txt
  - filters: dict with keys 'location' and 'vehicle_type' as str

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Main container
  - vehicle-name (H1): Vehicle make and model
  - vehicle-specs (Div): Engine, seats, transmission
  - daily-rate (Div): Price per day
  - book-now-button (Button): Navigates to booking_page
  - vehicle-reviews (Div): List of customer reviews
- Navigation mappings:
  - `url_for('booking_page', vehicle_id=vehicle['vehicle_id'])` for book-now-button
- Context variables:
  - vehicle: dict from vehicles.txt
  - reviews: list of dicts {reviewer:str, rating:int, comment:str}

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Main container
  - pickup-location (Dropdown): Options from locations.txt
  - dropoff-location (Dropdown): Options from locations.txt
  - pickup-date (Input): Date input
  - dropoff-date (Input): Date input
  - calculate-price-button (Button): Calculates total price
  - total-price (Div): Shows calculated price
  - proceed-to-insurance-button (Button): Navigates to insurance options page
- Navigation mappings:
  - `url_for('insurance_options_page', reservation_id=reservation_id)` after booking details
- Context variables:
  - vehicle: dict for current vehicle
  - locations: list of dicts from locations.txt
  - pickup_date: str
  - dropoff_date: str
  - total_price: float

### 5. Insurance Options Page
- Filename: templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Main container
  - insurance-options (Div): List of insurance plans
  - select-insurance-{insurance_id} (Radio): Select a plan
  - insurance-description (Div): Description of selected insurance
  - insurance-price (Div): Price of selected insurance
  - confirm-booking-button (Button): Confirm booking
- Navigation mappings:
  - Action POSTs to same URL with insurance selection
- Context variables:
  - insurance_plans: list of dicts from insurance.txt
  - selected_insurance: dict
  - reservation_id: int

### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Main container
  - rentals-table (Table): Tabular rentals list
  - view-rental-details-{rental_id} (Button): View rental details
  - status-filter (Dropdown): Filter by status (All, Active, Completed, Cancelled)
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - `url_for('dashboard_page')` for back-to-dashboard
- Context variables:
  - rentals: list of dicts from rentals.txt
  - filter_status: str

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Main container
  - reservations-list (Div): List of reservations
  - modify-reservation-button-{reservation_id} (Button): Modify reservation
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation
  - sort-by-date-button (Button): Sort reservations
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - `url_for('dashboard_page')` for back-to-dashboard
- Context variables:
  - reservations: list of dicts from reservations.txt

### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Main container
  - select-reservation (Dropdown): Select reservation
  - driver-assistance-checkbox (Checkbox): Driver assistance option
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Special notes input
  - submit-requests-button (Button): Submit requests
- Navigation mappings:
  - POST form submits to /special-requests
- Context variables:
  - reservations: list of dicts from reservations.txt
  - submitted_data: dict (optional, after POST)

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Main container
  - locations-list (Div): List of location entries
  - location-detail-button-{location_id} (Button): View location details
  - hours-filter (Dropdown): Filter locations by operating hours
  - search-location-input (Input): Search locations by city or name
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mappings:
  - `url_for('dashboard_page')` for back-to-dashboard
- Context variables:
  - locations: list of dicts from locations.txt


## Section 3: Data File Schemas

---

### 1. vehicles.txt
- **File Path:** data/vehicles.txt
- **Format:** vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- **Field Types:**
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str (Petrol, Diesel, Electric)
  - status: str (Available, Rented, Maintenance)
- **Example Lines:**
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```
- **Notes:** Stores vehicle details for rental listings and status.


### 2. customers.txt
- **File Path:** data/customers.txt
- **Format:** customer_id|name|email|phone|driver_license|license_expiry
- **Field Types:**
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- **Example Lines:**
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```
- **Notes:** Stores customer personal and driving license information.


### 3. locations.txt
- **File Path:** data/locations.txt
- **Format:** location_id|city|address|phone|hours|available_vehicles
- **Field Types:**
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., "24/7", "09:00-18:00")
  - available_vehicles: int
- **Example Lines:**
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```
- **Notes:** Stores pickup and dropoff location details.


### 4. rentals.txt
- **File Path:** data/rentals.txt
- **Format:** rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- **Field Types:**
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str (city or location name)
  - dropoff_location: str (city or location name)
  - total_price: float
  - status: str (Completed, Active, Cancelled)
- **Example Lines:**
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```
- **Notes:** Stores completed and active rental records.


### 5. insurance.txt
- **File Path:** data/insurance.txt
- **Format:** insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- **Field Types:**
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g., "50000", "Unlimited")
  - deductible: int
- **Example Lines:**
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```
- **Notes:** Stores insurance plans available for rental bookings.


### 6. reservations.txt
- **File Path:** data/reservations.txt
- **Format:** reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- **Field Types:**
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- **Example Lines:**
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```
- **Notes:** Stores user reservations linking rentals and insurance.

---

This specification ensures backend and frontend development teams can fully implement the CarRental application independently with clear and consistent interfaces.
