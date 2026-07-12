# CarRental Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                  | Function Name               | HTTP Method(s) | Template File           | Context Variables                                                                                              |
|-----------------------------|-----------------------------|----------------|-------------------------|--------------------------------------------------------------------------------------------------------------|
| /                           | root_redirect               | GET            | None (Redirect)          | None                                                                                                         |
| /dashboard                  | dashboard_page              | GET            | dashboard.html          | featured_vehicles: List[dict], promotions: List[str]                                                          |
| /search                    | search_vehicles             | GET            | search.html             | locations: List[dict], vehicle_types: List[str], selected_location: str, selected_vehicle_type: str, vehicles: List[dict] |
| /vehicle/<int:vehicle_id>  | vehicle_details             | GET            | vehicle_details.html    | vehicle: dict, reviews: List[dict]                                                                           |
| /booking/<int:vehicle_id>  | booking_page                | GET, POST       | booking.html            | vehicle: dict, locations: List[dict], pickup_date: str, dropoff_date: str, total_price: float                  |
| /insurance/<int:reservation_id> | insurance_options       | GET, POST       | insurance.html          | insurance_plans: List[dict], selected_insurance_id: int, insurance_description: str, insurance_price: float, reservation_id: int |
| /history                  | rental_history              | GET            | rental_history.html     | rentals: List[dict], filter_status: str                                                                        |
| /reservations             | reservations_management     | GET            | reservations.html       | reservations: List[dict]                                                                                        |
| /reservation/modify/<int:reservation_id> | modify_reservation   | POST           | None                    | reservation_id: int, modifications: dict                                                                        |
| /reservation/cancel/<int:reservation_id> | cancel_reservation   | POST           | None                    | reservation_id: int                                                                                            |
| /special_requests          | special_requests            | GET, POST       | special_requests.html   | reservations: List[dict], selected_reservation_id: int, requests_data: dict                                    |
| /locations                | locations_page              | GET            | locations.html          | locations: List[dict], filter_hours: str, search_query: str                                                   |

Notes:
- Root path '/' redirects to '/dashboard'.
- POST routes are used for form submissions where applicable.
- Context variables correspond precisely to data fields and form inputs.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard.
  - featured-vehicles (Div): Shows featured vehicle recommendations.
  - search-vehicles-button (Button): Navigates to vehicle search page.
  - my-reservations-button (Button): Navigates to reservations page.
  - promotions-section (Div): Displays current promotions.
- Navigation:
  - search-vehicles-button -> url_for('search_vehicles')
  - my-reservations-button -> url_for('reservations_management')
- Context Variables:
  - featured_vehicles: List of dicts {vehicle_id: int, make: str, model: str, daily_rate: float}
  - promotions: List of str

### 2. Vehicle Search Page
- Filename: templates/search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container
  - location-filter (Dropdown): Select pickup location
  - vehicle-type-filter (Dropdown): Select vehicle type
  - date-range-input (Input): Rental date range selection
  - vehicles-grid (Div): Grid displaying vehicles
  - view-details-button-{vehicle_id} (Button): View details for each vehicle
- Navigation:
  - view-details-button-{vehicle_id} -> url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - locations: List of dicts {location_id: int, city: str, address: str}
  - vehicle_types: List[str]
  - selected_location: str
  - selected_vehicle_type: str
  - vehicles: List of dicts {vehicle_id: int, make: str, model: str, daily_rate: float}

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container
  - vehicle-name (H1): Vehicle name and model
  - vehicle-specs (Div): Engine, seats, transmission
  - daily-rate (Div): Daily rental rate
  - book-now-button (Button): Initiate booking
  - vehicle-reviews (Div): Customer reviews
- Navigation:
  - book-now-button -> url_for('booking_page', vehicle_id=vehicle['vehicle_id'])
- Context Variables:
  - vehicle: dict {vehicle_id: int, make: str, model: str, daily_rate: float, seats: int, transmission: str, fuel_type: str, status: str}
  - reviews: List of dicts {reviewer: str, rating: int, comment: str}

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container
  - pickup-location (Dropdown): Select pickup location
  - dropoff-location (Dropdown): Select dropoff location
  - pickup-date (Input): Pickup date
  - dropoff-date (Input): Dropoff date
  - calculate-price-button (Button): Calculate total price
  - total-price (Div): Display total price
  - proceed-to-insurance-button (Button): Proceed to insurance
- Navigation:
  - proceed-to-insurance-button -> url_for('insurance_options', reservation_id=some_reservation_id)
- Context Variables:
  - vehicle: dict
  - locations: List of dicts
  - pickup_date: str
  - dropoff_date: str
  - total_price: float

### 5. Insurance Options Page
- Filename: templates/insurance.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container
  - insurance-options (Div): Available plans
  - select-insurance-{insurance_id} (Radio): Radio for each plan
  - insurance-description (Div): Description of selected plan
  - insurance-price (Div): Price of selected insurance
  - confirm-booking-button (Button): Confirm booking
- Navigation:
  - confirm-booking-button -> url_for('dashboard_page') or confirmation
- Context Variables:
  - insurance_plans: List of dicts {insurance_id: int, plan_name: str, description: str, daily_cost: float, coverage_limit: str, deductible: int}
  - selected_insurance_id: int
  - insurance_description: str
  - insurance_price: float
  - reservation_id: int

### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container
  - rentals-table (Table): Rental list
  - view-rental-details-{rental_id} (Button): Rental detail button
  - status-filter (Dropdown): Filter by status
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - rentals: List of dicts {rental_id: int, vehicle: str, pickup_date: str, dropoff_date: str, pickup_location: str, dropoff_location: str, total_price: float, status: str}
  - filter_status: str

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container
  - reservations-list (Div): Reservation entries
  - modify-reservation-button-{reservation_id} (Button): Modify button
  - cancel-reservation-button-{reservation_id} (Button): Cancel button
  - sort-by-date-button (Button): Sort by date
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - reservations: List of dicts {reservation_id: int, rental_id: int, vehicle: str, pickup_date: str, dropoff_date: str, status: str, insurance_id: int, special_requests: str}

### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container
  - select-reservation (Dropdown): Select reservation
  - driver-assistance-checkbox (Checkbox): Driver assistance
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Special notes
  - submit-requests-button (Button): Submit requests
- Navigation:
  - submit-requests-button -> url_for('special_requests')
- Context Variables:
  - reservations: List of dicts {reservation_id: int, rental_id: int, vehicle: str, pickup_date: str, dropoff_date: str, status: str}
  - selected_reservation_id: int
  - requests_data: dict {driver_assistance: bool, gps_option: bool, child_seat_quantity: int, special_notes: str}

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container
  - locations-list (Div): List of locations
  - location-detail-button-{location_id} (Button): Location details button
  - hours-filter (Dropdown): Filter by operating hours
  - search-location-input (Input): Search input
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - locations: List of dicts {location_id: int, city: str, address: str, phone: str, hours: str, available_vehicles: int}
  - filter_hours: str
  - search_query: str

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Stores vehicle details including availability and pricing.
- Format (pipe-delimited):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str
  - status: str (Available, Unavailable)
- Examples:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

### 2. customers.txt
- Stores customer personal and license details.
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
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

### 3. locations.txt
- Stores rental pickup/dropoff locations.
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., 24/7, 09:00-18:00)
  - available_vehicles: int
- Examples:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

### 4. rentals.txt
- Stores rental transaction records.
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
  - status: str (Active, Completed, Cancelled)
- Examples:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

### 5. insurance.txt
- Stores insurance plans details.
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Examples:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

### 6. reservations.txt
- Stores user reservations with status and special requests.
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
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed

---

This design specification provides a clear and consistent foundation for developers to implement the CarRental application independently, fully covering backend routes, frontend templates, and data file schemas as per the user requirements.