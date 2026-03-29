# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                          | Function Name             | HTTP Method(s) | Template File              | Context Variables Passed to Template (with Types)                                                            |
|-----------------------------------|---------------------------|----------------|----------------------------|-------------------------------------------------------------------------------------------------------------|
| /                                 | home                      | GET            | - (redirects to /dashboard) | None                                                                                                        |
| /dashboard                        | dashboard                 | GET            | dashboard.html             | vehicles: list[dict], promotions: list[dict], (if applicable), title: str                                  |
| /search                          | vehicle_search            | GET, POST      | search-page.html           | vehicles: list[dict], filtered_vehicles: list[dict], locations: list[dict], filters: dict[str, str], title: str |
| /vehicle/<int:vehicle_id>         | vehicle_details           | GET            | vehicle-details-page.html  | vehicle: dict, title: str                                                                                    |
| /booking                         | booking                   | GET, POST      | booking-page.html          | pickup_locations: list[dict], dropoff_locations: list[dict], booking_form: dict[str, Any], total_price: float or None, title: str |
| /insurance                       | insurance_options         | GET, POST      | insurance-page.html        | insurance_plans: list[dict], selected_plan: dict or None, booking_data: dict or None, title: str             |
| /history                        | rental_history            | GET            | history-page.html          | rentals: list[dict], status_filter: str, title: str                                                        |
| /reservations                   | reservation_management    | GET, POST      | reservations-page.html     | reservations: list[dict], sorting: str, title: str                                                        |
| /special-requests               | special_requests          | GET, POST      | requests-page.html         | reservations: list[dict], special_requests_form: dict or None, title: str                                   |
| /locations                      | locations                 | GET            | locations-page.html        | locations: list[dict], hour_filter: str, search_query: str, title: str                                     |

---

## Section 2: HTML Template Specifications (Frontend)

---

### 1. dashboard.html

- Path: templates/dashboard.html
- Page Title: "Car Rental Dashboard"
- Element IDs:
  - dashboard-page (div): Container for the entire dashboard page.
  - featured-vehicles (div): Displays featured vehicle recommendations.
  - search-vehicles-button (button): Navigates to vehicle search page.
  - my-reservations-button (button): Navigates to reservations management page.
  - promotions-section (div): Shows current promotions and offers.
- Navigation:
  - search-vehicles-button: url_for('vehicle_search')
  - my-reservations-button: url_for('reservation_management')
- Context Variables:
  - vehicles: List of vehicle dicts, each with keys vehicle_id:int, make:str, model:str, etc.
  - promotions: List of promotion dicts, (if defined, based on task this may be minimal)

---

### 2. search-page.html

- Path: templates/search-page.html
- Page Title: "Search Vehicles"
- Element IDs:
  - search-page (div): Container for search vehicles page.
  - location-filter (select/dropdown): Filter vehicles by pickup location.
  - vehicle-type-filter (select/dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - date-range-input (input): Field for selecting rental date range.
  - vehicles-grid (div): Grid display of vehicle cards.
  - view-details-button-{vehicle_id} (button): View details button for each vehicle.
- Navigation:
  - view-details-button-{vehicle_id}: url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: list of all vehicle dicts.
  - filtered_vehicles: list of filtered vehicle dicts.
  - locations: list of location dicts.
  - filters: dict containing currently selected filters (location, vehicle type, dates).

---

### 3. vehicle-details-page.html

- Path: templates/vehicle-details-page.html
- Page Title: "Vehicle Details"
- Element IDs:
  - vehicle-details-page (div): Container for vehicle details page.
  - vehicle-name (h1): Displays vehicle make and model.
  - vehicle-specs (div): Displays vehicle specs such as engine, seats, transmission, fuel type.
  - daily-rate (div): Shows daily rental price.
  - book-now-button (button): Button to start booking process for this vehicle.
  - vehicle-reviews (div): Section for customer reviews.
- Navigation:
  - book-now-button: url_for('booking') with vehicle selection context
- Context Variables:
  - vehicle: dict with detailed vehicle info.

---

### 4. booking-page.html

- Path: templates/booking-page.html
- Page Title: "Book Your Rental"
- Element IDs:
  - booking-page (div): Container for booking page.
  - pickup-location (dropdown): Select pickup location.
  - dropoff-location (dropdown): Select dropoff location.
  - pickup-date (input): Date picker for pickup date.
  - dropoff-date (input): Date picker for dropoff date.
  - calculate-price-button (button): Button to calculate rental price.
  - total-price (div): Display calculated total price.
  - proceed-to-insurance-button (button): Proceeds to insurance options.
- Navigation:
  - proceed-to-insurance-button: url_for('insurance_options')
- Context Variables:
  - pickup_locations: list of location dicts.
  - dropoff_locations: list of location dicts.
  - booking_form: dict holding current booking data inputs.
  - total_price: float or None

---

### 5. insurance-page.html

- Path: templates/insurance-page.html
- Page Title: "Select Insurance Coverage"
- Element IDs:
  - insurance-page (div): Container for insurance selection.
  - insurance-options (div): Displays available insurance plans.
  - select-insurance-{insurance_id} (radio.Button): Select insurance plan.
  - insurance-description (div): Description of selected insurance.
  - insurance-price (div): Price of selected insurance.
  - confirm-booking-button (button): Confirm booking with insurance.
- Navigation:
  - confirm-booking-button: Submission to finalize booking
- Context Variables:
  - insurance_plans: list of insurance dicts.
  - selected_plan: dict or None
  - booking_data: dict or None

---

### 6. history-page.html

- Path: templates/history-page.html
- Page Title: "Rental History"
- Element IDs:
  - history-page (div): Container for rental history page.
  - rentals-table (table): Table displaying rental records.
  - view-rental-details-{rental_id} (button): Button for rental detailed view.
  - status-filter (dropdown): Filter rentals by status.
  - back-to-dashboard (button): Navigate back to dashboard.
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - rentals: list of rental dicts.
  - status_filter: str current filter applied.

---

### 7. reservations-page.html

- Path: templates/reservations-page.html
- Page Title: "My Reservations"
- Element IDs:
  - reservations-page (div): Container for reservations page.
  - reservations-list (div): List showing all reservations.
  - modify-reservation-button-{reservation_id} (button): Modify button per reservation.
  - cancel-reservation-button-{reservation_id} (button): Cancel button per reservation.
  - sort-by-date-button (button): Button to sort reservations by date.
  - back-to-dashboard (button): Navigate back to dashboard.
- Navigation:
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - reservations: list of reservation dicts.
  - sorting: str current sorting order.

---

### 8. requests-page.html

- Path: templates/requests-page.html
- Page Title: "Special Requests"
- Element IDs:
  - requests-page (div): Container for special requests.
  - select-reservation (dropdown): Select reservation to add requests.
  - driver-assistance-checkbox (checkbox): Checkbox for driver assistance.
  - gps-option-checkbox (checkbox): Checkbox for GPS option.
  - child-seat-quantity (input): Input for number of child seats.
  - special-notes (textarea): Textarea for extra notes.
  - submit-requests-button (button): Submit special requests.
- Navigation:
  - submit-requests-button: POST handler for submitting requests
- Context Variables:
  - reservations: list of reservation dicts.
  - special_requests_form: dict or None

---

### 9. locations-page.html

- Path: templates/locations-page.html
- Page Title: "Pickup and Dropoff Locations"
- Element IDs:
  - locations-page (div): Container for locations page.
  - locations-list (div): List all rental locations.
  - location-detail-button-{location_id} (button): Button for each location details.
  - hours-filter (dropdown): Filter locations by hours.
  - search-location-input (input): Search box for location names or cities.
  - back-to-dashboard (button): Navigate to dashboard.
- Navigation:
  - location-detail-button-{location_id}: url_for('location_detail', location_id=location_id)
  - back-to-dashboard: url_for('dashboard')
- Context Variables:
  - locations: list of location dicts.
  - hour_filter: str
  - search_query: str

---

## Section 3: Data File Schemas

### General
- All data files are located in the `data/` folder.
- Files are pipe (`|`) delimited plain text, no header rows.
- Each line represents one record.

---

### vehicles.txt
- Path: data/vehicles.txt
- Format: vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
- Fields & Types:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str (Petrol, Diesel, Electric, Hybrid)
  - status: str (Available, Rented, Maintenance)
- Examples:
  - 1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  - 2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  - 3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available

---

### customers.txt
- Path: data/customers.txt
- Format: customer_id|name|email|phone|driver_license|license_expiry
- Fields & Types:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD string)
- Examples:
  - 1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  - 2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20

---

### locations.txt
- Path: data/locations.txt
- Format: location_id|city|address|phone|hours|available_vehicles
- Fields & Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., "24/7", "09:00-18:00", "Weekend")
  - available_vehicles: int
- Examples:
  - 1|New York|123 Main St, NYC|555-1000|24/7|12
  - 2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8

---

### rentals.txt
- Path: data/rentals.txt
- Format:
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
- Fields & Types:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD string)
  - dropoff_date: date (YYYY-MM-DD string)
  - pickup_location: str
  - dropoff_location: str
  - total_price: float
  - status: str (Active, Completed, Cancelled)
- Examples:
  - 1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  - 2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active

---

### insurance.txt
- Path: data/insurance.txt
- Format: insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
- Fields & Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str (e.g. "50000", "Unlimited")
  - deductible: int
- Examples:
  - 1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  - 2|Standard Coverage|Collision and theft protection|12.00|250000|500
  - 3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0

---

### reservations.txt
- Path: data/reservations.txt
- Format: reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
- Fields & Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Examples:
  - 1|1|1|1|Confirmed|2|Driver assistance requested
  - 2|2|2|2|Active|1|GPS and child seat needed

---

# End of design_spec.md
