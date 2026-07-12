# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                   | Function Name               | HTTP Method(s) | Template File           | Context Variables                                                                                               |
|-----------------------------|-----------------------------|----------------|-------------------------|---------------------------------------------------------------------------------------------------------------|
| /                           | redirect_to_dashboard        | GET            | N/A (redirect)          | None                                                                                                          |
| /dashboard                  | dashboard_page              | GET            | dashboard.html          | featured_vehicles: list[dict], promotions: list[dict]                                                         |
| /search-vehicles            | search_vehicles_page        | GET            | search_vehicles.html    | locations: list[str], vehicle_types: list[str], vehicles: list[dict]                                         |
| /vehicle/<int:vehicle_id>   | vehicle_details_page        | GET            | vehicle_details.html    | vehicle: dict, reviews: list[dict]                                                                            |
| /booking/<int:vehicle_id>   | booking_page                | GET, POST      | booking.html            | pickup_locations: list[str], dropoff_locations: list[str], selected_vehicle: dict, rental_dates: dict[str, str] (POST only), calculated_price: float (POST only) |
| /insurance/<int:reservation_id> | insurance_options_page      | GET, POST      | insurance.html          | insurance_plans: list[dict], selected_insurance: dict (POST only), reservation_id: int                         |
| /rental-history            | rental_history_page         | GET            | rental_history.html     | rentals: list[dict], status_filter_options: list[str]                                                         |
| /my-reservations           | reservation_management_page | GET, POST      | reservations.html       | reservations: list[dict]                                                                                      |
| /special-requests          | special_requests_page       | GET, POST      | special_requests.html   | reservations: list[dict], submitted_requests: dict (POST only)                                               |
| /locations                | locations_page              | GET            | locations.html          | locations: list[dict], hours_filter_options: list[str]                                                       |

Notes:
- The root route `/` redirects to `/dashboard`.
- Function names are descriptive, lowercase with underscores.
- Context variables align exactly with data models or form inputs.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. templates/dashboard.html
- Page Title: "Car Rental Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-vehicles (Div): Display featured vehicles.
  - search-vehicles-button (Button): Navigate to the vehicle search page.
  - my-reservations-button (Button): Navigate to the reservations page.
  - promotions-section (Div): Display current promotions.
- Navigation:
  - search-vehicles-button: `url_for('search_vehicles_page')`
  - my-reservations-button: `url_for('reservation_management_page')`
- Context Variables:
  - featured_vehicles: list of dict
  - promotions: list of dict

### 2. templates/search_vehicles.html
- Page Title: "Search Vehicles"
- Element IDs:
  - search-page (Div): Container for the search page.
  - location-filter (Dropdown): Filter by pickup location.
  - vehicle-type-filter (Dropdown): Filter by vehicle type.
  - date-range-input (Input): Date range input for rental.
  - vehicles-grid (Div): Grid displaying vehicle cards.
  - view-details-button-{vehicle_id} (Button): View details button for each vehicle.
- Navigation:
  - view-details-button-{vehicle_id}: `url_for('vehicle_details_page', vehicle_id=vehicle_id)`
- Context Variables:
  - locations: list[str]
  - vehicle_types: list[str]
  - vehicles: list of dict

### 3. templates/vehicle_details.html
- Page Title: "Vehicle Details"
- Element IDs:
  - vehicle-details-page (Div): Container.
  - vehicle-name (H1): Vehicle name and model.
  - vehicle-specs (Div): Vehicle specifications.
  - daily-rate (Div): Daily rental rate.
  - book-now-button (Button): Book this vehicle.
  - vehicle-reviews (Div): Customer reviews.
- Navigation:
  - book-now-button: `url_for('booking_page', vehicle_id=vehicle.vehicle_id)`
- Context Variables:
  - vehicle: dict
  - reviews: list of dict

### 4. templates/booking.html
- Page Title: "Book Your Rental"
- Element IDs:
  - booking-page (Div): Container.
  - pickup-location (Dropdown): Pickup location selection.
  - dropoff-location (Dropdown): Dropoff location selection.
  - pickup-date (Input): Pickup date.
  - dropoff-date (Input): Dropoff date.
  - calculate-price-button (Button): Calculate total rental price.
  - total-price (Div): Display total price.
  - proceed-to-insurance-button (Button): Proceed to insurance options.
- Navigation:
  - proceed-to-insurance-button: `url_for('insurance_options_page', reservation_id=reservation_id)`
- Context Variables:
  - pickup_locations: list[str]
  - dropoff_locations: list[str]
  - selected_vehicle: dict
  - rental_dates: dict[str, str] (pickup_date, dropoff_date) (POST only)
  - calculated_price: float (POST only)

### 5. templates/insurance.html
- Page Title: "Select Insurance Coverage"
- Element IDs:
  - insurance-page (Div): Container.
  - insurance-options (Div): Available insurance plans.
  - select-insurance-{insurance_id} (Radio): Insurance selection radio button.
  - insurance-description (Div): Description of selected insurance.
  - insurance-price (Div): Price of selected insurance.
  - confirm-booking-button (Button): Confirm booking.
- Navigation:
  - confirm-booking-button: Form submission.
- Context Variables:
  - insurance_plans: list of dict
  - selected_insurance: dict (POST only)
  - reservation_id: int

### 6. templates/rental_history.html
- Page Title: "Rental History"
- Element IDs:
  - history-page (Div): Container.
  - rentals-table (Table): Table listing rentals.
  - view-rental-details-{rental_id} (Button): View rental details.
  - status-filter (Dropdown): Filter rentals by status.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - rentals: list of dict
  - status_filter_options: list[str]

### 7. templates/reservations.html
- Page Title: "My Reservations"
- Element IDs:
  - reservations-page (Div): Container.
  - reservations-list (Div): List of reservations.
  - modify-reservation-button-{reservation_id} (Button): Modify reservation.
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation.
  - sort-by-date-button (Button): Sort reservations by date.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - reservations: list of dict

### 8. templates/special_requests.html
- Page Title: "Special Requests"
- Element IDs:
  - requests-page (Div): Container.
  - select-reservation (Dropdown): Select reservation for requests.
  - driver-assistance-checkbox (Checkbox): Driver assistance option.
  - gps-option-checkbox (Checkbox): GPS option.
  - child-seat-quantity (Input): Number input for child seats.
  - special-notes (Textarea): Special notes input.
  - submit-requests-button (Button): Submit requests.
- Navigation:
  - submit-requests-button: Form submission.
- Context Variables:
  - reservations: list of dict
  - submitted_requests: dict (POST only)

### 9. templates/locations.html
- Page Title: "Pickup and Dropoff Locations"
- Element IDs:
  - locations-page (Div): Container.
  - locations-list (Div): List of locations.
  - location-detail-button-{location_id} (Button): View location details.
  - hours-filter (Dropdown): Filter by operating hours.
  - search-location-input (Input): Search by city or name.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation:
  - back-to-dashboard: `url_for('dashboard_page')`
- Context Variables:
  - locations: list of dict
  - hours_filter_options: list[str]

---

## Section 3: Data File Schemas

### vehicles.txt
- File storing vehicle inventory.
- Format:
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
```
- Fields:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float
  - seats: int
  - transmission: str (Automatic, Manual)
  - fuel_type: str
  - status: str (Available, Rented, Maintenance)
- Example lines:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

### customers.txt
- File storing customer data.
- Format:
```
customer_id|name|email|phone|driver_license|license_expiry
```
- Fields:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (YYYY-MM-DD)
- Example lines:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

### locations.txt
- File storing pickup and dropoff locations.
- Format:
```
location_id|city|address|phone|hours|available_vehicles
```
- Fields:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (24/7, 09:00-18:00, Weekend)
  - available_vehicles: int
- Example lines:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

### rentals.txt
- File storing rental transactions.
- Format:
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
```
- Fields:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (YYYY-MM-DD)
  - dropoff_date: date (YYYY-MM-DD)
  - pickup_location: str
  - dropoff_location: str
  - total_price: float
  - status: str (Completed, Active, Cancelled)
- Example lines:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

### insurance.txt
- File storing insurance plans.
- Format:
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
```
- Fields:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Example lines:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

### reservations.txt
- File storing reservation details.
- Format:
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
```
- Fields:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Example lines:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

**CRITICAL SUCCESS CRITERIA:**
- Backend fully supported by Sections 1 and 3.
- Frontend fully supported by Section 2.
- No cross-dependencies.
- Strict consistency in names, routes, element IDs, variables.
- No authentication or extra features.

---

End of design_spec.md
