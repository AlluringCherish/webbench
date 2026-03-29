# CarRental Web Application Design Specifications

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name           | HTTP Method(s) | Template Filename          | Context Variables                                                                                                          |
|-------------------------------|------------------------|----------------|----------------------------|---------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect          | GET            | N/A (redirect to /dashboard) | None                                                                                                                    |
| /dashboard                    | dashboard              | GET            | dashboard.html              | featured_vehicles: list[dict], promotions: list[dict]                                                                       |
| /search                      | vehicle_search         | GET            | search.html                 | vehicles: list[dict], locations: list[str], vehicle_types: list[str]                                                       |
| /vehicle/<int:vehicle_id>     | vehicle_details        | GET            | vehicle_details.html        | vehicle: dict, vehicle_reviews: list[dict]                                                                                  |
| /booking/<int:vehicle_id>     | booking                | GET, POST      | booking.html                | locations: list[str], pickup_location: str (POST), dropoff_location: str (POST), pickup_date: str (POST), dropoff_date: str (POST), total_price: float (POST) |
| /insurance/<int:reservation_id> | insurance_options   | GET, POST      | insurance.html              | insurance_plans: list[dict], selected_insurance_id: int (POST)                                                             |
| /history                     | rental_history         | GET            | rental_history.html         | rentals: list[dict], filter_status: str                                                                                     |
| /reservations                | reservation_management | GET            | reservations.html           | reservations: list[dict]                                                                                                   |
| /special_requests            | special_requests       | GET, POST      | special_requests.html       | reservations: list[dict], special_requests_form_data: dict (POST)                                                          |
| /locations                  | locations_page          | GET            | locations.html              | locations: list[dict], filtered_hours: str, search_query: str                                                              |

Notes:
- The root route `/` redirects to `/dashboard`.
- Function names are descriptive and consistent, using lowercase_with_underscores.
- Context variables are annotated with precise types.
- All navigation endpoints accommodate the navigation elements described in requirements.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: Car Rental Dashboard
- Elements:
  - dashboard-page: Div - Container for the dashboard page.
  - featured-vehicles: Div - Display of featured vehicle recommendations.
  - search-vehicles-button: Button - Navigates to vehicle_search page (`url_for('vehicle_search')`).
  - my-reservations-button: Button - Navigates to reservation_management page (`url_for('reservation_management')`).
  - promotions-section: Div - Display of current promotions and offers.
- Context Variables:
  - featured_vehicles: list[dict] (vehicle data with relevant fields)
  - promotions: list[dict] (promotion details with title: str, description: str)

### 2. templates/search.html
- Page Title: Search Vehicles
- Elements:
  - search-page: Div - Container.
  - location-filter: Dropdown - Pickup location filter, options from locations list.
  - vehicle-type-filter: Dropdown - Vehicle type filter options: Economy, Compact, Sedan, SUV, Luxury.
  - date-range-input: Input - Rental date range selection.
  - vehicles-grid: Div - Grid displaying vehicle cards.
  - view-details-button-{vehicle_id}: Button - For each vehicle, navigates to vehicle_details page using `url_for('vehicle_details', vehicle_id=vehicle_id)`.
- Context Variables:
  - vehicles: list[dict] (vehicles.txt fields)
  - locations: list[str]
  - vehicle_types: list[str]

### 3. templates/vehicle_details.html
- Page Title: Vehicle Details
- Elements:
  - vehicle-details-page: Div - Container.
  - vehicle-name: H1 - Shows vehicle make and model.
  - vehicle-specs: Div - Vehicle specifications (engine, seats, transmission).
  - daily-rate: Div - Displays daily rental rate.
  - book-now-button: Button - Navigates to booking page for this vehicle (`url_for('booking', vehicle_id=vehicle_id)`).
  - vehicle-reviews: Div - Section displaying customer reviews.
- Context Variables:
  - vehicle: dict
  - vehicle_reviews: list[dict] (each with rating: int, comment: str)

### 4. templates/booking.html
- Page Title: Book Your Rental
- Elements:
  - booking-page: Div - Container.
  - pickup-location: Dropdown - Pickup location selection.
  - dropoff-location: Dropdown - Dropoff location selection.
  - pickup-date: Input (date) - Pickup date.
  - dropoff-date: Input (date) - Dropoff date.
  - calculate-price-button: Button - Calculates total rental price.
  - total-price: Div - Displays calculated price.
  - proceed-to-insurance-button: Button - Proceeds to insurance options page.
- Context Variables:
  - locations: list[str]
  - pickup_location: str (POST)
  - dropoff_location: str (POST)
  - pickup_date: str (POST, format YYYY-MM-DD)
  - dropoff_date: str (POST, format YYYY-MM-DD)
  - total_price: float (POST)

### 5. templates/insurance.html
- Page Title: Select Insurance Coverage
- Elements:
  - insurance-page: Div - Container.
  - insurance-options: Div - Lists insurance plans.
  - select-insurance-{insurance_id}: Radio - Radio button for each insurance plan.
  - insurance-description: Div - Displays description of selected plan.
  - insurance-price: Div - Displays insurance price.
  - confirm-booking-button: Button - Confirms booking with insurance selection.
- Context Variables:
  - insurance_plans: list[dict] (fields as per insurance.txt)
  - selected_insurance_id: int (POST, optional)

### 6. templates/rental_history.html
- Page Title: Rental History
- Elements:
  - history-page: Div - Container.
  - rentals-table: Table - Showing rental_id, vehicle, dates, pickup/dropoff locations, status.
  - view-rental-details-{rental_id}: Button - For each rental.
  - status-filter: Dropdown - Filter by All, Active, Completed, Cancelled.
  - back-to-dashboard: Button - Navigation back to dashboard.
- Context Variables:
  - rentals: list[dict]
  - filter_status: str

### 7. templates/reservations.html
- Page Title: My Reservations
- Elements:
  - reservations-page: Div - Container.
  - reservations-list: Div - List of reservations.
  - modify-reservation-button-{reservation_id}: Button - Modify reservation.
  - cancel-reservation-button-{reservation_id}: Button - Cancel reservation.
  - sort-by-date-button: Button - Sort reservations by date.
  - back-to-dashboard: Button - Navigation back to dashboard.
- Context Variables:
  - reservations: list[dict]

### 8. templates/special_requests.html
- Page Title: Special Requests
- Elements:
  - requests-page: Div - Container.
  - select-reservation: Dropdown - Select reservation to add requests.
  - driver-assistance-checkbox: Checkbox - Driver assistance option.
  - gps-option-checkbox: Checkbox - GPS option.
  - child-seat-quantity: Input - Number of child seats.
  - special-notes: Textarea - Special notes.
  - submit-requests-button: Button - Submit requests.
- Context Variables:
  - reservations: list[dict]
  - special_requests_form_data: dict (POST data)

### 9. templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Elements:
  - locations-page: Div - Container.
  - locations-list: Div - List of locations with address and hours.
  - location-detail-button-{location_id}: Button - View location details.
  - hours-filter: Dropdown - Filter by operating hours (24/7, Business Hours, Weekend).
  - search-location-input: Input - Search by city or name.
  - back-to-dashboard: Button - Navigate back to dashboard.
- Context Variables:
  - locations: list[dict]
  - filtered_hours: str
  - search_query: str

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- File: data/vehicles.txt
- Description: Stores vehicle data for rental management.
- Format: vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic or Manual)
  - fuel_type: str
  - status: str (Available, Unavailable)
- Example lines:
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

### 2. customers.txt
- File: data/customers.txt
- Description: Stores customer information.
- Format: customer_id|name|email|phone|driver_license|license_expiry
- Fields:
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
- File: data/locations.txt
- Description: Stores rental pickup/dropoff locations.
- Format: location_id|city|address|phone|hours|available_vehicles
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (24/7, Business Hours, Weekend, or custom hours e.g., 09:00-18:00)
  - available_vehicles: int
- Example lines:
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

### 4. rentals.txt
- File: data/rentals.txt
- Description: Stores rental transactions.
- Format: rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
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
- Example lines:
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

### 5. insurance.txt
- File: data/insurance.txt
- Description: Stores insurance plan details.
- Format: insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g., "Unlimited") or int
  - deductible: float or int
- Example lines:
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

### 6. reservations.txt
- File: data/reservations.txt
- Description: Stores reservation data with insurance and special requests.
- Format: reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Example lines:
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed

---

# End of design_spec.md
