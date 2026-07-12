# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name              | HTTP Method(s) | Template File            | Context Variables                                                                                      |
|----------------------------|----------------------------|----------------|--------------------------|------------------------------------------------------------------------------------------------------|
| /                          | redirect_to_dashboard       | GET            | N/A (redirect)            | N/A                                                                                                  |
| /dashboard                 | dashboard                  | GET            | dashboard.html            | featured_vehicles: List[Dict[str, str]]  # List of vehicle dicts with keys: vehicle_id (int as str), make, model, daily_rate (str)
|                            |                            |                |                          | promotions: List[str]  # List of promotional strings                                                   |
| /search                   | search_vehicles             | GET            | vehicle_search.html       | locations: List[str]  # List of location city names                                                    |
|                            |                            |                |                          | vehicle_types: List[str]  # List: ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']                     |
|                            |                            |                |                          | vehicles: List[Dict[str, str]]  # Filtered list of vehicles with keys: vehicle_id (int as str), make, model, daily_rate (str)                       |
| /vehicle/<int:vehicle_id> | vehicle_details             | GET            | vehicle_details.html      | vehicle: Dict[str, str]  # dict with make, model, vehicle_type, daily_rate (str), seats (str), transmission, fuel_type, status                      |
|                            |                            |                |                          | reviews: List[str]  # List of customer review strings (optional)                                     |
| /booking/<int:vehicle_id> | booking                    | GET, POST      | booking.html              | vehicle_id: int
|                            |                            |                |                          | locations: List[str]  # List of location city names                                                   |
|                            |                            | POST           |                          | booking_data: Dict[str, str] for POSTed form fields (pickup_location, dropoff_location, pickup_date, dropoff_date)                               |
| /insurance/<int:reservation_id> | insurance_options         | GET, POST      | insurance_options.html    | insurance_plans: List[Dict[str, str]]  # insurance_id, plan_name, description, daily_cost, coverage_limit, deductible                              |
|                            |                            | POST           |                          | selected_plan_id: int                                                                           |
| /rental_history            | rental_history             | GET            | rental_history.html       | rentals: List[Dict[str, str]]  # rentals with rental_id (int as str), vehicle (make+model), dates, location (pickup/dropoff), status                  |
| /reservations              | reservation_management      | GET, POST      | reservations.html         | reservations: List[Dict[str, str]]  # reservation_id (int as str), vehicle (make+model), dates, status, insurance_id, special_requests                |
|                            |                            | POST           |                          | action: str ('modify'/'cancel')
|                            |                            |                |                          | reservation_id: int                                                                            |
| /special_requests          | special_requests           | GET, POST      | special_requests.html     | reservations: List[Dict[str, str]]  # reservations with reservation_id (int as str), vehicle, dates, status                                           |
|                            |                            | POST           |                          | special_requests_form: Dict[str, str or int or bool]: keys - reservation_id, driver_assistance (bool), gps_option (bool), child_seats (int), notes (str) |
| /locations                | locations_page             | GET            | locations.html            | locations: List[Dict[str, str]]  # location_id (int as str), city, address, phone, hours, available_vehicles                                            |

Notes:
- Root route `'/'` redirects to `/dashboard`.
- Function names are in lowercase with underscores and descriptive.
- Context variables are exact and align strictly with data schemas and frontend form inputs.
- Navigation endpoints defined to match page buttons and links for seamless routing.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: `templates/dashboard.html`
- Page Title: "Car Rental Dashboard"
- Element IDs:
  - `dashboard-page` (div): Container for dashboard content.
  - `featured-vehicles` (div): Displays list of featured vehicles.
  - `search-vehicles-button` (button): Navigates to vehicle search page via `url_for('search_vehicles')`.
  - `my-reservations-button` (button): Navigates to reservations page via `url_for('reservation_management')`.
  - `promotions-section` (div): Displays current promotions and offers.
- Navigation:
  - Button `search-vehicles-button` -> `search_vehicles`
  - Button `my-reservations-button` -> `reservation_management`
- Context Variables:
  - `featured_vehicles`: List of dicts with keys: `vehicle_id` (int), `make` (str), `model` (str), `daily_rate` (str)
  - `promotions`: List of promotional strings

### 2. Vehicle Search Page
- Filename: `templates/vehicle_search.html`
- Page Title: "Search Vehicles"
- Element IDs:
  - `search-page` (div): Container for search page.
  - `location-filter` (select/dropdown): Filter by pickup location.
  - `vehicle-type-filter` (select/dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - `date-range-input` (input): Input for rental date range.
  - `vehicles-grid` (div): Grid displaying vehicle cards.
  - `view-details-button-{vehicle_id}` (button): Button per vehicle card to view details.
- Navigation:
  - Each `view-details-button-{vehicle_id}` -> `vehicle_details` route with vehicle_id parameter
- Context Variables:
  - `locations`: List of location city names (str)
  - `vehicle_types`: List[str] -- ["Economy", "Compact", "Sedan", "SUV", "Luxury"]
  - `vehicles`: List of dicts with keys: `vehicle_id` (int), `make`, `model`, `daily_rate` (str)

### 3. Vehicle Details Page
- Filename: `templates/vehicle_details.html`
- Page Title: "Vehicle Details"
- Element IDs:
  - `vehicle-details-page` (div): Container for details.
  - `vehicle-name` (h1): Vehicle name and model.
  - `vehicle-specs` (div): Engine, seats, transmission info.
  - `daily-rate` (div): Daily rental rate display.
  - `book-now-button` (button): Navigate to booking page for this vehicle via `url_for('booking', vehicle_id=vehicle.vehicle_id)`.
  - `vehicle-reviews` (div): Section for customer reviews.
- Navigation:
  - `book-now-button` -> `booking` route with vehicle_id
- Context Variables:
  - `vehicle`: dict with keys: make, model, vehicle_type, daily_rate (str), seats (int), transmission, fuel_type, status
  - `reviews`: List[str]

### 4. Booking Page
- Filename: `templates/booking.html`
- Page Title: "Book Your Rental"
- Element IDs:
  - `booking-page` (div): Container.
  - `pickup-location` (select/dropdown): Pickup location options.
  - `dropoff-location` (select/dropdown): Dropoff location options.
  - `pickup-date` (input): Pickup date field.
  - `dropoff-date` (input): Dropoff date field.
  - `calculate-price-button` (button): Calculates total rental price.
  - `total-price` (div): Shows calculated price.
  - `proceed-to-insurance-button` (button): Moves to insurance options page.
- Navigation:
  - `proceed-to-insurance-button` -> `insurance_options` with reservation_id parameter post-booking
- Context Variables:
  - `vehicle_id` (int)
  - `locations`: List[str]

### 5. Insurance Options Page
- Filename: `templates/insurance_options.html`
- Page Title: "Select Insurance Coverage"
- Element IDs:
  - `insurance-page` (div): Container.
  - `insurance-options` (div): Lists insurance plans.
  - `select-insurance-{insurance_id}` (radio): Select insurance plan.
  - `insurance-description` (div): Shows description of selected plan.
  - `insurance-price` (div): Shows price of selected plan.
  - `confirm-booking-button` (button): Confirms booking with insurance.
- Navigation:
  - `confirm-booking-button` triggers POST to confirm insurance selection
- Context Variables:
  - `insurance_plans`: List of dicts with keys: insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (str), deductible (str)

### 6. Rental History Page
- Filename: `templates/rental_history.html`
- Page Title: "Rental History"
- Element IDs:
  - `history-page` (div): Container.
  - `rentals-table` (table): Shows rentals with columns ID, vehicle, dates, location, status.
  - `view-rental-details-{rental_id}` (button): View details for each rental.
  - `status-filter` (select/dropdown): Filter rentals by status (All, Active, Completed, Cancelled).
  - `back-to-dashboard` (button): Navigate back to dashboard.
- Navigation:
  - `back-to-dashboard` -> `dashboard`
- Context Variables:
  - `rentals`: List of dicts with rental_id (int), vehicle (str, e.g. 'Toyota Camry'), pickup_date (str), dropoff_date (str), pickup_location (str), dropoff_location (str), status (str)

### 7. Reservation Management Page
- Filename: `templates/reservations.html`
- Page Title: "My Reservations"
- Element IDs:
  - `reservations-page` (div): Container.
  - `reservations-list` (div): List of reservations.
  - `modify-reservation-button-{reservation_id}` (button): Modify reservation button.
  - `cancel-reservation-button-{reservation_id}` (button): Cancel reservation button.
  - `sort-by-date-button` (button): Sort reservations by date.
  - `back-to-dashboard` (button): Navigate back to dashboard.
- Navigation:
  - `back-to-dashboard` -> `dashboard`
- Context Variables:
  - `reservations`: List of dicts with reservation_id (int), vehicle (str), pickup_date, dropoff_date, status, insurance_id (int), special_requests (str)

### 8. Special Requests Page
- Filename: `templates/special_requests.html`
- Page Title: "Special Requests"
- Element IDs:
  - `requests-page` (div): Container.
  - `select-reservation` (select/dropdown): Select reservation to add requests.
  - `driver-assistance-checkbox` (checkbox): Driver assistance request.
  - `gps-option-checkbox` (checkbox): GPS option.
  - `child-seat-quantity` (input): Number of child seats.
  - `special-notes` (textarea): Special notes input.
  - `submit-requests-button` (button): Submit special requests.
- Navigation: None specified.
- Context Variables:
  - `reservations`: List of dicts with reservation_id (int), vehicle (str), pickup_date, dropoff_date, status

### 9. Locations Page
- Filename: `templates/locations.html`
- Page Title: "Pickup and Dropoff Locations"
- Element IDs:
  - `locations-page` (div): Container.
  - `locations-list` (div): List with location details.
  - `location-detail-button-{location_id}` (button): Button to view details.
  - `hours-filter` (select/dropdown): Filter by hours (24/7, Business Hours, Weekend).
  - `search-location-input` (input): Search locations by city or name.
  - `back-to-dashboard` (button): Navigate back to dashboard.
- Navigation:
  - `back-to-dashboard` -> `dashboard`
- Context Variables:
  - `locations`: List of dicts with keys: location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)

---

## Section 3: Data File Schemas

| Filename         | Field Names and Types                                                                                         |
|------------------|--------------------------------------------------------------------------------------------------------------|
| vehicles.txt     | vehicle_id (int) | make (str) | model (str) | vehicle_type (str) | daily_rate (float) | seats (int) | transmission (str) | fuel_type (str) | status (str)       |
| customers.txt    | customer_id (int) | name (str) | email (str) | phone (str) | driver_license (str) | license_expiry (date in YYYY-MM-DD)                              |
| locations.txt    | location_id (int) | city (str) | address (str) | phone (str) | hours (str) | available_vehicles (int)                                   |
| rentals.txt      | rental_id (int) | vehicle_id (int) | customer_id (int) | pickup_date (YYYY-MM-DD) | dropoff_date (YYYY-MM-DD) | pickup_location (str) | dropoff_location (str) | total_price (float) | status (str) |
| insurance.txt    | insurance_id (int) | plan_name (str) | description (str) | daily_cost (float) | coverage_limit (str) | deductible (str)             |
| reservations.txt | reservation_id (int) | rental_id (int) | vehicle_id (int) | customer_id (int) | status (str) | insurance_id (int) | special_requests (str)                  |


---

data/vehicles.txt
Format:
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status

Example:
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

---
data/customers.txt
Format:
customer_id|name|email|phone|driver_license|license_expiry

Example:
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

---
data/locations.txt
Format:
location_id|city|address|phone|hours|available_vehicles

Example:
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

---
data/rentals.txt
Format:
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status

Example:
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

---
data/insurance.txt
Format:
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible

Example:
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

---
data/reservations.txt
Format:
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests

Example:
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed

---

# End of CarRental Design Specification
