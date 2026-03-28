# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name           | HTTP Method(s) | Template File              | Context Variables                                                                                  |
|----------------------------|-------------------------|----------------|----------------------------|--------------------------------------------------------------------------------------------------|
| /                          | root_redirect           | GET            | N/A (redirect to /dashboard) | None                                                                                             |
| /dashboard                 | dashboard               | GET            | dashboard.html              | featured_vehicles: list[dict], promotions: list[dict]                                           |
| /search                   | vehicle_search          | GET            | search.html                 | vehicles: list[dict], locations: list[dict], vehicle_types: list[str], filters: dict[str,str]   |
| /vehicle/<int:vehicle_id> | vehicle_details         | GET            | vehicle_details.html        | vehicle: dict, reviews: list[dict]                                                              |
| /booking                  | booking                 | GET, POST      | booking.html                | pickup_locations: list[dict], dropoff_locations: list[dict], calculated_price: float or None     |
| /insurance                | insurance_options       | GET, POST      | insurance.html              | insurance_plans: list[dict], selected_insurance: dict or None                                   |
| /rental-history           | rental_history          | GET            | rental_history.html         | rentals: list[dict], status_filter: str                                                          |
| /reservations             | reservations_management | GET, POST      | reservations.html           | reservations: list[dict]                                                                         |
| /special-requests         | special_requests        | GET, POST      | special_requests.html       | reservations: list[dict], form_data: dict or None                                               |
| /locations                | locations_page          | GET            | locations.html              | locations: list[dict], hours_filter: str, search_query: str                                     |

### Route Details

- **/** (root_redirect): redirects to `/dashboard` to enforce dashboard as the start page.
- **/dashboard**: Displays main dashboard with featured vehicles and promotions.

  - featured_vehicles: List of vehicle dictionaries including vehicle_id, make, model, daily_rate, etc.
  - promotions: List of promotion dictionaries, each containing title, description.

- **/search**: Displays search page with filters and all vehicles matching filters.

  - vehicles: List of vehicle dictionaries with availability and details.
  - locations: List of location dictionaries for filtering.
  - vehicle_types: List[str] of vehicle type strings (`Economy`, `Compact`, `Sedan`, `SUV`, `Luxury`).
  - filters: Dict[str,str] current filter values for location, vehicle_type, date_range.

- **/vehicle/<int:vehicle_id>**: Shows detailed information about one vehicle.

  - vehicle: Dict with vehicle fields.
  - reviews: List of review dicts related to vehicle.

- **/booking**: Displays and processes booking form.

  - GET context: pickup_locations, dropoff_locations.
  - POST context: same + calculated_price (float) after price calculation.

- **/insurance**: Insurance options selection page.

  - insurance_plans: List of insurance dictionaries.
  - selected_insurance: Selected insurance dictionary or None.

- **/rental-history**: Displays rental history.

  - rentals: List of rental dictionaries.
  - status_filter: Current selected status filter (e.g., "All", "Active", etc.)

- **/reservations**: Manages reservations with possible actions POSTed.

  - reservations: List of reservation dictionaries.

- **/special-requests**: Add special requests to selected reservation.

  - reservations: List of current reservations.
  - form_data: Dict of submitted special requests or None.

- **/locations**: Displays locations with filters and search.

  - locations: List of location dictionaries.
  - hours_filter: Current hours filter value.
  - search_query: Current text search query string.


---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Container for full dashboard page.
  - featured-vehicles (Div): Display of featured vehicle recommendations.
  - search-vehicles-button (Button): Navigates to vehicle search page via url_for('vehicle_search').
  - my-reservations-button (Button): Navigates to reservations page via url_for('reservations_management').
  - promotions-section (Div): Displays current promotions and offers.
- Navigation:
  - search-vehicles-button: url_for('vehicle_search')
  - my-reservations-button: url_for('reservations_management')
- Context Variables:
  - featured_vehicles: list of dict with vehicle fields.
  - promotions: list of dict with promotion fields.


### 2. templates/search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Container
  - location-filter (Dropdown): Filter by pickup location
  - vehicle-type-filter (Dropdown): Filter by vehicle type
  - date-range-input (Input): Rental date range input
  - vehicles-grid (Div): Grid container for vehicle cards
  - view-details-button-{vehicle_id} (Button): Each vehicle's details button with dynamic id, where {vehicle_id} is vehicle's ID
- Navigation:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list of dict
  - locations: list of dict
  - vehicle_types: list of str
  - filters: dict with keys "location", "vehicle_type", "date_range"


### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div)
  - vehicle-name (H1)
  - vehicle-specs (Div)
  - daily-rate (Div)
  - book-now-button (Button): navigates to /booking page with preselected vehicle?
  - vehicle-reviews (Div)
- Navigation:
  - book-now-button: url_for('booking')
- Context Variables:
  - vehicle: dict
  - reviews: list of dict


### 4. templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div)
  - pickup-location (Dropdown)
  - dropoff-location (Dropdown)
  - pickup-date (Input)
  - dropoff-date (Input)
  - calculate-price-button (Button): triggers price calculation
  - total-price (Div): shows calculated price
  - proceed-to-insurance-button (Button): navigates to insurance options
- Navigation:
  - proceed-to-insurance-button: url_for('insurance_options')
- Context Variables:
  - pickup_locations: list of dict
  - dropoff_locations: list of dict
  - calculated_price: float or None


### 5. templates/insurance.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div)
  - insurance-options (Div): container for insurance plans
  - select-insurance-{insurance_id} (Radio): select insurance plan
  - insurance-description (Div): shows selected insurance description
  - insurance-price (Div): shows selected insurance price
  - confirm-booking-button (Button)
- Navigation:
  - confirm-booking-button: submits insurance selection, possibly redirects
- Context Variables:
  - insurance_plans: list of dict
  - selected_insurance: dict or None


### 6. templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div)
  - rentals-table (Table): columns: ID, vehicle, dates, location, status
  - view-rental-details-{rental_id} (Button): view details of rental
  - status-filter (Dropdown)
  - back-to-dashboard (Button): url_for('dashboard')
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - rentals: list of dict
  - status_filter: str


### 7. templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div)
  - reservations-list (Div): list all reservations
  - modify-reservation-button-{reservation_id} (Button)
  - cancel-reservation-button-{reservation_id} (Button)
  - sort-by-date-button (Button)
  - back-to-dashboard (Button): url_for('dashboard')
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - reservations: list of dict


### 8. templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div)
  - select-reservation (Dropdown)
  - driver-assistance-checkbox (Checkbox)
  - gps-option-checkbox (Checkbox)
  - child-seat-quantity (Input)
  - special-notes (Textarea)
  - submit-requests-button (Button)
- Navigation:
  - submit-requests-button: submits form data
- Context Variables:
  - reservations: list of dict
  - form_data: dict or None


### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div)
  - locations-list (Div)
  - location-detail-button-{location_id} (Button)
  - hours-filter (Dropdown)
  - search-location-input (Input)
  - back-to-dashboard (Button): url_for('dashboard')
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - locations: list of dict
  - hours_filter: str
  - search_query: str


---

## Section 3: Data File Schemas

### vehicles.txt
- Stores: All vehicle details for renting, availability and pricing.
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
  - fuel_type: str (Petrol, Diesel, Electric, Hybrid)
  - status: str (Available, Unavailable)
- Example lines:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available


### customers.txt
- Stores: All customer personal and license info.
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


### locations.txt
- Stores: Rental locations and availability
- Format:
  location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (24/7, 09:00-18:00, etc.)
  - available_vehicles: int
- Examples:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8


### rentals.txt
- Stores: Rental transactions with dates, locations, pricing, status
- Format:
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Fields:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str (city or specific location name)
  - dropoff_location: str
  - total_price: float
  - status: str (Completed, Active, Cancelled)
- Examples:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active


### insurance.txt
- Stores: Insurance plan options for rentals
- Format:
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str|int (e.g., 50000 or "Unlimited")
  - deductible: int or float
- Examples:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0


### reservations.txt
- Stores: Reservation details tied to rentals with insurance and special requests
- Format:
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str (free text)
- Examples:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed


---

END OF DESIGN SPECIFICATIONS
