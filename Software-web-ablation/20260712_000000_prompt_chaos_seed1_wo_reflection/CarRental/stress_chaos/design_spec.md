# CarRental Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                   | Function Name                | HTTP Method(s) | Template File              | Context Variables                                                                                              |
|------------------------------|------------------------------|----------------|----------------------------|----------------------------------------------------------------------------------------------------------------|
| /                            | root_redirect                | GET            | N/A (Redirect)             | None                                                                                                           |
| /dashboard                   | dashboard                   | GET            | dashboard.html             | featured_vehicles: list[dict], promotions: list[dict]                                                           |
| /vehicles                   | vehicle_search              | GET            | vehicle_search.html        | vehicles: list[dict], locations: list[dict], vehicle_types: list[str], selected_location: str or None, selected_vehicle_type: str or None, selected_date_range: tuple[str,str] or None |
| /vehicle/<int:vehicle_id>   | vehicle_details             | GET            | vehicle_details.html       | vehicle: dict, reviews: list[dict]                                                                             |
| /booking/<int:vehicle_id>   | booking                    | GET, POST      | booking.html               | vehicle: dict, locations: list[dict], total_price: float or None, form_errors: dict or None                      |
| /insurance/<int:reservation_id> | insurance_options           | GET, POST      | insurance_options.html     | insurance_plans: list[dict], selected_insurance_id: int or None, insurance_description: str or None, insurance_price: float or None, reservation_id: int, form_errors: dict or None |
| /rental-history             | rental_history              | GET            | rental_history.html        | rentals: list[dict], status_filter: str                                                                        |
| /reservations               | reservations_page           | GET            | reservations.html          | reservations: list[dict]                                                                                        |
| /reservation/modify/<int:reservation_id> | modify_reservation          | GET, POST      | modify_reservation.html (not described in requirements, so assume reservations.html handles management) None |
| /reservation/cancel/<int:reservation_id> | cancel_reservation          | POST           | N/A (Redirect /reservations) | None                                                                                                            |
| /special-requests           | special_requests            | GET, POST      | special_requests.html      | reservations: list[dict], form_data: dict or None, form_errors: dict or None                                   |
| /locations                 | locations_page              | GET            | locations.html             | locations: list[dict], filtered_hours: str or None, search_query: str or None                                  |

Notes:
- The root route '/' redirects to /dashboard.
- 'modify_reservation' and 'cancel_reservation' routes support reservation management; exact UI handled in reservations.html as per requirements (modification and cancellation buttons).
- POST methods accommodate form submissions or actions.

---

## Section 2: HTML Template Specifications (Frontend)

### templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page: Div - container for dashboard
  - featured-vehicles: Div - featured vehicle recommendations
  - search-vehicles-button: Button - navigate to /vehicles
  - my-reservations-button: Button - navigate to /reservations
  - promotions-section: Div - current promotions
- Navigation:
  - search-vehicles-button -> url_for('vehicle_search')
  - my-reservations-button -> url_for('reservations_page')
- Context Variables:
  - featured_vehicles: list of dict with keys like vehicle_id, make, model, daily_rate
  - promotions: list of dict with promotion details

### templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page: Div
  - location-filter: Dropdown
  - vehicle-type-filter: Dropdown (Economy, Compact, Sedan, SUV, Luxury)
  - date-range-input: Input
  - vehicles-grid: Div
  - view-details-button-{vehicle_id}: Button for each vehicle
- Navigation:
  - view-details-button-{vehicle_id} -> url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list of dict, each with vehicle details
  - locations: list of dict
  - vehicle_types: list[str]
  - selected_location, selected_vehicle_type: str or None
  - selected_date_range: tuple[str,str] or None

### templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page: Div
  - vehicle-name: H1
  - vehicle-specs: Div
  - daily-rate: Div
  - book-now-button: Button (navigate to booking page for this vehicle)
  - vehicle-reviews: Div
- Navigation:
  - book-now-button -> url_for('booking', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: dict
  - reviews: list of dict

### templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page: Div
  - pickup-location: Dropdown
  - dropoff-location: Dropdown
  - pickup-date: Input
  - dropoff-date: Input
  - calculate-price-button: Button
  - total-price: Div
  - proceed-to-insurance-button: Button
- Navigation:
  - proceed-to-insurance-button -> url_for('insurance_options', reservation_id=reservation_id) after booking created
- Context Variables:
  - vehicle: dict
  - locations: list of dict
  - total_price: float or None
  - form_errors: dict or None

### templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page: Div
  - insurance-options: Div
  - select-insurance-{insurance_id}: Radio per insurance plan
  - insurance-description: Div
  - insurance-price: Div
  - confirm-booking-button: Button
- Navigation:
  - confirm-booking-button -> Submits form to confirm booking
- Context Variables:
  - insurance_plans: list of dict
  - selected_insurance_id: int or None
  - insurance_description: str or None
  - insurance_price: float or None
  - reservation_id: int
  - form_errors: dict or None

### templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page: Div
  - rentals-table: Table
  - view-rental-details-{rental_id}: Button per rental
  - status-filter: Dropdown (All, Active, Completed, Cancelled)
  - back-to-dashboard: Button
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - rentals: list of dict
  - status_filter: str

### templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page: Div
  - reservations-list: Div
  - modify-reservation-button-{reservation_id}: Button per reservation
  - cancel-reservation-button-{reservation_id}: Button per reservation
  - sort-by-date-button: Button
  - back-to-dashboard: Button
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - reservations: list of dict

### templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page: Div
  - select-reservation: Dropdown
  - driver-assistance-checkbox: Checkbox
  - gps-option-checkbox: Checkbox
  - child-seat-quantity: Input
  - special-notes: Textarea
  - submit-requests-button: Button
- Navigation:
  - submit-requests-button -> Submits form to special_requests route
- Context Variables:
  - reservations: list of dict
  - form_data: dict or None
  - form_errors: dict or None

### templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page: Div
  - locations-list: Div
  - location-detail-button-{location_id}: Button per location
  - hours-filter: Dropdown (24/7, Business Hours, Weekend)
  - search-location-input: Input
  - back-to-dashboard: Button
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - locations: list of dict
  - filtered_hours: str or None
  - search_query: str or None

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Filename: `data/vehicles.txt`
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
  - status: str (e.g., Available, Rented)
- Example Lines:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
- Purpose:
  Stores all vehicle information for availability, pricing, and specification display.

### 2. customers.txt
- Filename: `data/customers.txt`
- Format (pipe-delimited):
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
- Purpose:
  Stores customer identity and license information for rental validation.

### 3. locations.txt
- Filename: `data/locations.txt`
- Format (pipe-delimited):
  location_id|city|address|phone|hours|available_vehicles
- Field Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., 24/7, 09:00-18:00)
  - available_vehicles: int
- Example Lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
- Purpose:
  Stores rental location details for pickup and dropoff selections.

### 4. rentals.txt
- Filename: `data/rentals.txt`
- Format (pipe-delimited):
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
  - status: str (e.g., Active, Completed, Cancelled)
- Example Lines:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
- Purpose:
  Records all rental transactions for history and status tracking.

### 5. insurance.txt
- Filename: `data/insurance.txt`
- Format (pipe-delimited):
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g., 50000, Unlimited)
  - deductible: int
- Example Lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
- Purpose:
  Stores insurance plans available for rental coverage selection.

### 6. reservations.txt
- Filename: `data/reservations.txt`
- Format (pipe-delimited):
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (e.g., Confirmed, Active)
  - insurance_id: int
  - special_requests: str
- Example Lines:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
- Purpose:
  Tracks reservation details linking rentals, vehicles, customers, insurance, and special requests.

---

This completes the detailed design specifications required for independent development of the CarRental application.
