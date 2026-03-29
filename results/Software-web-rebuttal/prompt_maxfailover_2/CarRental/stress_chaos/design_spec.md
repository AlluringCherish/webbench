# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                       | Function Name               | HTTP Method(s) | Template File              | Context Variables                                                                                  |
|---------------------------------|-----------------------------|----------------|----------------------------|--------------------------------------------------------------------------------------------------|
| `/`                             | root_redirect               | GET            | N/A (redirect to `/dashboard`) | None                                                                                             |
| `/dashboard`                   | dashboard_page              | GET            | dashboard.html             | featured_vehicles: list[dict], promotions: list[dict]                                            |
| `/vehicles/search`             | vehicle_search_page         | GET            | vehicle_search.html        | locations: list[str], vehicle_types: list[str], vehicles: list[dict], date_range: str or None    |
| `/vehicle/<int:vehicle_id>`   | vehicle_details_page        | GET            | vehicle_details.html       | vehicle: dict, reviews: list[dict]                                                               |
| `/booking/<int:vehicle_id>`   | booking_page                | GET, POST      | booking.html               | locations: list[str], vehicle_id: int, pickup_location: str (POST), dropoff_location: str (POST), pickup_date: str (POST), dropoff_date: str (POST), total_price: float or None |
| `/insurance/<int:reservation_id>` | insurance_options_page    | GET, POST      | insurance_options.html     | insurance_plans: list[dict], selected_plan: dict or None, reservation_id: int                     |
| `/rental/history`             | rental_history_page         | GET            | rental_history.html        | rentals: list[dict], status_filter_options: list[str], selected_status: str                      |
| `/reservations`               | reservation_management_page | GET            | reservations.html          | reservations: list[dict]                                                                           |
| `/reservation/modify/<int:reservation_id>` | modify_reservation  | POST           | N/A                        | reservation_id: int, modifications: dict                                                         |
| `/reservation/cancel/<int:reservation_id>` | cancel_reservation   | POST           | N/A                        | reservation_id: int                                                                                |
| `/special_requests`           | special_requests_page       | GET, POST      | special_requests.html      | reservations: list[dict], selected_reservation_id: int or None, special_requests_data: dict       |
| `/locations`                 | locations_page              | GET            | locations.html             | locations: list[dict], hours_filter_options: list[str], selected_hours_filter: str, search_query: str or None |
| `/location/<int:location_id>` | location_detail_page        | GET            | location_detail.html       | location: dict                                                                                   |

**Route Details:**
- Root `/` redirects to `/dashboard`.
- POST methods are for form submissions (booking, insurance selection, reservation modifications, cancellations, special requests).
- Context variables exactly reflect data schemas and form inputs.
- Navigation endpoints include dashboard, vehicle search, reservations, and back buttons as per user requirements.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container div for dashboard page
  - featured-vehicles (Div): Shows featured vehicle recommendations
  - promotions-section (Div): Shows current promotions
  - search-vehicles-button (Button): Navigates to vehicle search page (`url_for('vehicle_search_page')`)
  - my-reservations-button (Button): Navigates to reservations page (`url_for('reservation_management_page')`)
- Navigation:
  - search-vehicles-button → `vehicle_search_page`
  - my-reservations-button → `reservation_management_page`
- Context Variables:
  - featured_vehicles: list of dicts with vehicle summary info
  - promotions: list of dicts with promotion details

### 2. templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container for the search page
  - location-filter (Dropdown): Filter vehicles by pickup location
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, etc.)
  - date-range-input (Input): Select rental date range
  - vehicles-grid (Div): Grid containing vehicle cards
  - view-details-button-{vehicle_id} (Button): Button for each vehicle to view details
- Navigation:
  - view-details-button-{vehicle_id} → `vehicle_details_page(vehicle_id=vehicle_id)`
- Context Variables:
  - locations: list[str] for location dropdown
  - vehicle_types: list[str] as fixed vehicle types
  - vehicles: list of dicts with vehicle info
  - date_range: str or None for default or filter date range

### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Container for details page
  - vehicle-name (H1): Vehicle full name/model
  - vehicle-specs (Div): Engine, seats, transmission info
  - daily-rate (Div): Daily rental rate
  - book-now-button (Button): Proceeds to booking page (`url_for('booking_page', vehicle_id=vehicle.vehicle_id)`)
  - vehicle-reviews (Div): Customer reviews
- Navigation:
  - book-now-button → `booking_page(vehicle_id=vehicle.vehicle_id)`
- Context Variables:
  - vehicle: dict, keys matching vehicles.txt fields plus specs
  - reviews: list[dict] with review details

### 4. templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Container
  - pickup-location (Dropdown): Pickup location selection
  - dropoff-location (Dropdown): Dropoff location selection
  - pickup-date (Input): Pickup date
  - dropoff-date (Input): Dropoff date
  - calculate-price-button (Button): Calculate total price
  - total-price (Div): Show calculated price
  - proceed-to-insurance-button (Button): Navigate to insurance options
- Navigation:
  - proceed-to-insurance-button → `insurance_options_page(reservation_id=reservation_id)` after booking
- Context Variables:
  - locations: list[str]
  - vehicle_id: int
  - pickup_location, dropoff_location: str (POST/GET)
  - pickup_date, dropoff_date: str (POST/GET)
  - total_price: float or None

### 5. templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Container
  - insurance-options (Div): Shows insurance plans
  - select-insurance-{insurance_id} (Radio): Each insurance plan selection
  - insurance-description (Div): Description of selected insurance
  - insurance-price (Div): Price of selected insurance
  - confirm-booking-button (Button): Finalize booking
- Navigation:
  - confirm-booking-button → POST confirms booking
- Context Variables:
  - insurance_plans: list[dict]
  - selected_plan: dict or None
  - reservation_id: int

### 6. templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Container
  - rentals-table (Table): Displays rental records
  - view-rental-details-{rental_id} (Button): View details of rental
  - status-filter (Dropdown): Filter rentals by status
  - back-to-dashboard (Button): Go back to dashboard
- Navigation:
  - back-to-dashboard → `dashboard_page`
- Context Variables:
  - rentals: list[dict]
  - status_filter_options: list[str] = ["All", "Active", "Completed", "Cancelled"]
  - selected_status: str

### 7. templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Container
  - reservations-list (Div): List all reservations
  - modify-reservation-button-{reservation_id} (Button): Modify reservation
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation
  - sort-by-date-button (Button): Sort reservations
  - back-to-dashboard (Button): Go back to dashboard
- Navigation:
  - back-to-dashboard → `dashboard_page`
- Context Variables:
  - reservations: list[dict]

### 8. templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Container
  - select-reservation (Dropdown): Select reservation to add requests to
  - driver-assistance-checkbox (Checkbox): Driver assistance
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): Number of child seats
  - special-notes (Textarea): Additional notes
  - submit-requests-button (Button): Submit requests
- Navigation:
  - submit-requests-button → POST to special_requests_page
- Context Variables:
  - reservations: list[dict]
  - selected_reservation_id: int or None
  - special_requests_data: dict

### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Container
  - locations-list (Div): List of locations
  - location-detail-button-{location_id} (Button): View location details
  - hours-filter (Dropdown): Filter by operating hours
  - search-location-input (Input): Search by city or name
  - back-to-dashboard (Button): Go back to dashboard
- Navigation:
  - back-to-dashboard → `dashboard_page`
- Context Variables:
  - locations: list[dict]
  - hours_filter_options: list[str] = ["24/7", "Business Hours", "Weekend"]
  - selected_hours_filter: str
  - search_query: str or None

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Purpose: Stores vehicle data including details and availability status.
- Format (pipe-delimited, no headers):
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Field Types:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str
  - fuel_type: str
  - status: str (Available, Unavailable, etc.)
- Example Lines:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. customers.txt
- Purpose: Stores customer personal and license information.
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
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. locations.txt
- Purpose: Stores rental pickup and dropoff location info including availability.
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Field Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., "24/7", "09:00-18:00")
  - available_vehicles: int
- Example Lines:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. rentals.txt
- Purpose: Stores rental transaction records and status.
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
  - status: str (Completed, Active, Cancelled)
- Example Lines:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. insurance.txt
- Purpose: Stores available insurance plans and costs.
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g., "50000", "Unlimited")
  - deductible: float
- Example Lines:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. reservations.txt
- Purpose: Stores reservation details linking rentals, vehicles, customers, insurance, and special requests.
- Format:
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Example Lines:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

**CRITICAL SUCCESS NOTES:**
- Backend developers will build Flask routes and handle data files precisely as specified to satisfy all page needs and data interactions.
- Frontend developers will follow template specs carefully to ensure correct UI, element IDs, and navigations.
- No authentication or additional features beyond those stated will be implemented.
- Naming conventions, dynamic element ID patterns, routing paths, and context variables are strictly consistent.
- Jinja2 syntax is implied for template variables and loops.

End of design_spec.md
