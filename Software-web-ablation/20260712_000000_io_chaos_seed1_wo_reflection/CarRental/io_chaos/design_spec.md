# CarRental Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                   | Function Name             | HTTP Method(s) | Template File             | Context Variables                                                                                              |
|-----------------------------|---------------------------|----------------|---------------------------|---------------------------------------------------------------------------------------------------------------|
| /                           | root_redirect             | GET            | None (redirect to /dashboard) | None                                                                                                         |
| /dashboard                  | dashboard                 | GET            | dashboard.html            | featured_vehicles: list of dict, current_promotions: list of str                                             |
| /vehicles                   | vehicle_search            | GET            | vehicle_search.html       | vehicles: list of dict, locations: list of dict, vehicle_types: list of str                                   |
| /vehicle/<int:vehicle_id>   | vehicle_details           | GET            | vehicle_details.html      | vehicle: dict, reviews: list of dict                                                                           |
| /booking/<int:vehicle_id>   | booking                  | GET, POST       | booking.html              | pickup_locations: list of dict, dropoff_locations: list of dict, calculated_price: float or None, booking_data: dict (POST) |
| /insurance/<int:reservation_id> | insurance_options     | GET, POST       | insurance_options.html     | insurance_plans: list of dict, selected_insurance: dict or None                                              |
| /history                   | rental_history            | GET            | rental_history.html       | rentals: list of dict, status_filter_options: list of str                                                    |
| /reservations              | reservations_management   | GET, POST       | reservations_management.html | reservations: list of dict                                                                                     |
| /special_requests          | special_requests          | GET, POST       | special_requests.html     | reservations: list of dict, submitted_request_status: str or None                                             |
| /locations                 | locations_page            | GET            | locations.html            | locations: list of dict, hours_filter_options: list of str                                                   |

Navigation endpoints:
- From dashboard: vehicle_search (/vehicles), reservations_management (/reservations)
- From vehicle_search: vehicle_details (/vehicle/<vehicle_id>)
- From vehicle_details: booking (/booking/<vehicle_id>)
- From booking: insurance_options (/insurance/<reservation_id>)
- From insurance_options: rental_history (/history)
- From rental_history: dashboard (/dashboard)
- From reservations_management: dashboard (/dashboard)
- From special_requests: dashboard (/dashboard)
- From locations_page: dashboard (/dashboard)

---

## Section 2: HTML Template Specifications (Frontend)

### templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-vehicles (Div): Display of featured vehicle recommendations
  - search-vehicles-button (Button): Navigate to vehicle search page
  - my-reservations-button (Button): Navigate to reservations page
  - promotions-section (Div): Current promotions and offers
- Navigation:
  - search-vehicles-button -> url_for('vehicle_search')
  - my-reservations-button -> url_for('reservations_management')
- Context Variables:
  - featured_vehicles: list of dict {vehicle_id: int, make: str, model: str, daily_rate: float}
  - current_promotions: list of str

### templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for search page
  - location-filter (Dropdown): To filter vehicles by pickup location
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury)
  - date-range-input (Input): Rental date range selection
  - vehicles-grid (Div): Grid showing vehicles
  - view-details-button-{vehicle_id} (Button): Button per vehicle for details
- Navigation:
  - view-details-button-{vehicle_id} -> url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list of dict {vehicle_id, make, model, vehicle_type, daily_rate}
  - locations: list of dict {location_id, city, address}
  - vehicle_types: list of str

### templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container
  - vehicle-name (H1): Vehicle name and model
  - vehicle-specs (Div): Engine, seats, transmission
  - daily-rate (Div): Daily rental rate
  - book-now-button (Button): To book vehicle
  - vehicle-reviews (Div): Customer reviews
- Navigation:
  - book-now-button -> url_for('booking', vehicle_id=vehicle['vehicle_id'])
- Context Variables:
  - vehicle: dict {vehicle_id, make, model, vehicle_type, seats, transmission, fuel_type, daily_rate, status}
  - reviews: list of dict {reviewer_name, rating, comment}

### templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container
  - pickup-location (Dropdown): Select pickup location
  - dropoff-location (Dropdown): Select dropoff location
  - pickup-date (Input): Select pickup date
  - dropoff-date (Input): Select dropoff date
  - calculate-price-button (Button): Calculate rental price
  - total-price (Div): Display calculated price
  - proceed-to-insurance-button (Button): Proceed to insurance page
- Navigation:
  - proceed-to-insurance-button -> url_for('insurance_options', reservation_id=reservation_id)
- Context Variables:
  - pickup_locations: list of dict {location_id, city, address}
  - dropoff_locations: list of dict {location_id, city, address}
  - calculated_price: float or None
  - booking_data: dict {pickup_location_id, dropoff_location_id, pickup_date, dropoff_date} (POST form data)

### templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container
  - insurance-options (Div): Available insurance plans
  - select-insurance-{insurance_id} (Radio): Radio button per insurance plan
  - insurance-description (Div): Description of selected plan
  - insurance-price (Div): Price of selected insurance
  - confirm-booking-button (Button): Confirm booking
- Navigation:
  - confirm-booking-button -> url_for('rental_history')
- Context Variables:
  - insurance_plans: list of dict {insurance_id, plan_name, description, daily_cost, coverage_limit, deductible}
  - selected_insurance: dict or None

### templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container
  - rentals-table (Table): Display rentals
  - view-rental-details-{rental_id} (Button): View details per rental
  - status-filter (Dropdown): Filter by status (All, Active, Completed, Cancelled)
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - rentals: list of dict {rental_id, vehicle_id, customer_id, pickup_date, dropoff_date, pickup_location, dropoff_location, total_price, status}
  - status_filter_options: list of str

### templates/reservations_management.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container
  - reservations-list (Div): List all reservations
  - modify-reservation-button-{reservation_id} (Button): Modify reservation
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation
  - sort-by-date-button (Button): Sort reservations by date
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - reservations: list of dict {reservation_id, rental_id, vehicle_id, customer_id, status, insurance_id, special_requests}

### templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container
  - select-reservation (Dropdown): Select reservation
  - driver-assistance-checkbox (Checkbox): Driver assistance request
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Special notes and requests
  - submit-requests-button (Button): Submit special requests
- Navigation:
  - submit-requests-button -> url_for('special_requests')
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - reservations: list of dict {reservation_id, rental_id, vehicle_id, customer_id, status, insurance_id, special_requests}
  - submitted_request_status: str or None

### templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container
  - locations-list (Div): List of locations
  - location-detail-button-{location_id} (Button): View location details
  - hours-filter (Dropdown): Filter by operating hours
  - search-location-input (Input): Search locations
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - locations: list of dict {location_id, city, address, phone, hours, available_vehicles}
  - hours_filter_options: list of str

---

## Section 3: Data File Schemas

### vehicles.txt
- Format:
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
- Example Lines:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```
- Description: Stores vehicle details used for search, display, and booking.

### customers.txt
- Format:
  customer_id|name|email|phone|driver_license|license_expiry
- Fields:
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
- Description: Stores customer contact and license information.

### locations.txt
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str
  - available_vehicles: int
- Example Lines:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```
- Description: Stores pickup and dropoff location info.

### rentals.txt
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
  - status: str
- Example Lines:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```
- Description: Stores rental transactions and statuses.

### insurance.txt
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Example Lines:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```
- Description: Stores insurance plan details.

### reservations.txt
- Format:
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str
  - insurance_id: int
  - special_requests: str
- Example Lines:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```
- Description: Stores reservation management data including special requests.

---

This completes the comprehensive design specification for the CarRental web application to support fully independent backend and frontend development.