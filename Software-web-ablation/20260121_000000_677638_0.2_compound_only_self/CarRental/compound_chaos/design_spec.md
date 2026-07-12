# Design Specification for CarRental Web Application

---

## SECTION 1: Flask Routes Specification (Backend)

| Route Path                      | Function Name               | HTTP Methods | Template File              | Context Variables Passed (name: type)                                                                                               |
|--------------------------------|-----------------------------|--------------|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect                | GET          | None (Redirects to /dashboard) | None                                                                                                                              |
| /dashboard                    | dashboard                   | GET          | dashboard.html             | featured_vehicles: List[Dict[str, Any]] (vehicles), promotions: List[str]                                                          |
| /search-vehicles              | search_vehicles             | GET          | search_vehicles.html       | locations: List[str], vehicle_types: List[str], vehicles: List[Dict[str, Any]]                                                    |
| /vehicle/<int:vehicle_id>     | vehicle_details             | GET          | vehicle_details.html       | vehicle: Dict[str, Any], reviews: List[Dict[str, Union[str, int, float]]]                                                         |
| /book/<int:vehicle_id>        | booking                    | GET, POST    | booking.html               | pickup_locations: List[str], dropoff_locations: List[str], booking_form: Dict[str, str] or none (POST data), total_price: float or None |
| /insurance/<int:reservation_id>| insurance_options          | GET, POST    | insurance_options.html     | insurance_plans: List[Dict[str, Any]], selected_insurance_id: int or None, insurance_details: Dict[str, Any] or None               |
| /rental-history               | rental_history             | GET          | rental_history.html        | rentals: List[Dict[str, Any]], status_filter_options: List[str], applied_status_filter: str                                         |
| /my-reservations              | reservations_page          | GET          | reservations.html          | reservations: List[Dict[str, Any]]                                                                                                |
| /modify-reservation/<int:reservation_id>| modify_reservation | GET, POST    | (if applicable; not specified) | reservation: Dict[str, Any]                                                                                                   |
| /cancel-reservation/<int:reservation_id>| cancel_reservation | POST         | None (redirect or JSON)    | reservation_id: int                                                                                                                |
| /special-requests             | special_requests           | GET, POST    | special_requests.html      | reservations: List[Dict[str, Any]], form_data: Dict[str, Any] or None                                                               |
| /locations                   | locations_page             | GET          | locations.html             | locations: List[Dict[str, Any]], hours_filter_options: List[str], applied_hours_filter: str, search_query: str                      |

Notes:
- The root route `/` redirects to `/dashboard` as mandatory.
- Navigation endpoints reflect user task buttons and links, maintaining consistency.
- Function names are lowercase_with_underscores.

---

## SECTION 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page (templates/dashboard.html)
- Page Title: Car Rental Dashboard
- Elements:
  - ID: `dashboard-page` (Div) - Container for the dashboard page
  - ID: `featured-vehicles` (Div) - Shows featured vehicle recommendations
  - ID: `search-vehicles-button` (Button) - Navigates to Vehicle Search
  - ID: `my-reservations-button` (Button) - Navigates to My Reservations
  - ID: `promotions-section` (Div) - Displays current promotions
- Navigation Mappings:
  - `search-vehicles-button` → `url_for('search_vehicles')`
  - `my-reservations-button` → `url_for('reservations_page')`
- Context Variables:
  ```jinja
  featured_vehicles: List[Dict[str, Any]]
  promotions: List[str]
  ```

### 2. Vehicle Search Page (templates/search_vehicles.html)
- Page Title: Search Vehicles
- Elements:
  - ID: `search-page` (Div) - Container
  - ID: `location-filter` (Dropdown) - Pickup locations filter
  - ID: `vehicle-type-filter` (Dropdown) - Vehicle type filter (Economy, Compact, Sedan, SUV, Luxury)
  - ID: `date-range-input` (Input) - Rental date range
  - ID: `vehicles-grid` (Div) - Container for vehicle cards
  - ID: `view-details-button-{vehicle_id}` (Button) - For each vehicle card to view details
- Navigation Mappings:
  - `view-details-button-{vehicle_id}` → `url_for('vehicle_details', vehicle_id=vehicle_id)`
- Context Variables:
  ```jinja
  locations: List[str]
  vehicle_types: List[str] = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
  vehicles: List[Dict[str, Any]]
  ```

### 3. Vehicle Details Page (templates/vehicle_details.html)
- Page Title: Vehicle Details
- Elements:
  - ID: `vehicle-details-page` (Div) - Container
  - ID: `vehicle-name` (H1) - Vehicle make and model
  - ID: `vehicle-specs` (Div) - Engine, seats, transmission
  - ID: `daily-rate` (Div) - Daily rental rate
  - ID: `book-now-button` (Button) - Navigate to booking page
  - ID: `vehicle-reviews` (Div) - Customer reviews
- Navigation Mappings:
  - `book-now-button` → `url_for('booking', vehicle_id=vehicle.vehicle_id)`
- Context Variables:
  ```jinja
  vehicle: Dict[str, Any]  # Including vehicle_id, make, model, vehicle_type, daily_rate, seats, transmission, fuel_type, status
  reviews: List[Dict[str, Union[str, int, float]]]  # Review data
  ```

### 4. Booking Page (templates/booking.html)
- Page Title: Book Your Rental
- Elements:
  - ID: `booking-page` (Div) - Container
  - ID: `pickup-location` (Dropdown) - Select pickup location
  - ID: `dropoff-location` (Dropdown) - Select dropoff location
  - ID: `pickup-date` (Input) - Pickup date
  - ID: `dropoff-date` (Input) - Dropoff date
  - ID: `calculate-price-button` (Button) - Calculate price
  - ID: `total-price` (Div) - Show total price
  - ID: `proceed-to-insurance-button` (Button) - Proceed to insurance
- Navigation Mappings:
  - `proceed-to-insurance-button` → `url_for('insurance_options', reservation_id=reservation_id)`
- Context Variables:
  ```jinja
  pickup_locations: List[str]
  dropoff_locations: List[str]
  booking_form: Dict[str, Optional[str]]  # Containing selected pickup_location, dropoff_location, pickup_date, dropoff_date
  total_price: Optional[float]
  ```

### 5. Insurance Options Page (templates/insurance_options.html)
- Page Title: Select Insurance Coverage
- Elements:
  - ID: `insurance-page` (Div) - Container
  - ID: `insurance-options` (Div) - All insurance plans
  - ID: `select-insurance-{insurance_id}` (Radio) - Select each insurance plan
  - ID: `insurance-description` (Div) - Selected plan description
  - ID: `insurance-price` (Div) - Selected plan price
  - ID: `confirm-booking-button` (Button) - Confirm booking
- Navigation Mappings:
  - `confirm-booking-button` triggers form POST
- Context Variables:
  ```jinja
  insurance_plans: List[Dict[str, Any]]
  selected_insurance_id: Optional[int]
  insurance_details: Optional[Dict[str, Any]]
  ```

### 6. Rental History Page (templates/rental_history.html)
- Page Title: Rental History
- Elements:
  - ID: `history-page` (Div) - Container
  - ID: `rentals-table` (Table) - Rental records
  - ID: `view-rental-details-{rental_id}` (Button) - View rental details
  - ID: `status-filter` (Dropdown) - Filter by status (All, Active, Completed, Cancelled)
  - ID: `back-to-dashboard` (Button) - Go back to dashboard
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard')`
- Context Variables:
  ```jinja
  rentals: List[Dict[str, Any]]
  status_filter_options: List[str] = ['All', 'Active', 'Completed', 'Cancelled']
  applied_status_filter: str
  ```

### 7. Reservation Management Page (templates/reservations.html)
- Page Title: My Reservations
- Elements:
  - ID: `reservations-page` (Div) - Container
  - ID: `reservations-list` (Div) - List of reservations
  - ID: `modify-reservation-button-{reservation_id}` (Button) - Modify reservation
  - ID: `cancel-reservation-button-{reservation_id}` (Button) - Cancel reservation
  - ID: `sort-by-date-button` (Button) - Sort by date
  - ID: `back-to-dashboard` (Button) - Go back to dashboard
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard')`
  - Modify and cancel buttons trigger respective routes
- Context Variables:
  ```jinja
  reservations: List[Dict[str, Any]]
  ```

### 8. Special Requests Page (templates/special_requests.html)
- Page Title: Special Requests
- Elements:
  - ID: `requests-page` (Div) - Container
  - ID: `select-reservation` (Dropdown) - Select reservation
  - ID: `driver-assistance-checkbox` (Checkbox) - Driver assistance
  - ID: `gps-option-checkbox` (Checkbox) - GPS option
  - ID: `child-seat-quantity` (Input) - Number of child seats
  - ID: `special-notes` (Textarea) - Special notes
  - ID: `submit-requests-button` (Button) - Submit requests
- Navigation Mappings:
  - Submit triggers POST to special requests route
- Context Variables:
  ```jinja
  reservations: List[Dict[str, Any]]
  submitted_data: Optional[Dict[str, Any]]
  ```

### 9. Locations Page (templates/locations.html)
- Page Title: Pickup and Dropoff Locations
- Elements:
  - ID: `locations-page` (Div) - Container
  - ID: `locations-list` (Div) - List of locations
  - ID: `location-detail-button-{location_id}` (Button) - View location details
  - ID: `hours-filter` (Dropdown) - Operating hours filter (24/7, Business Hours, Weekend)
  - ID: `search-location-input` (Input) - Search by city or name
  - ID: `back-to-dashboard` (Button) - Go back to dashboard
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard')`
  - `location-detail-button-{location_id}` - Link to location details (if implemented)
- Context Variables:
  ```jinja
  locations: List[Dict[str, Any]]
  hours_filter_options: List[str] = ['24/7', 'Business Hours', 'Weekend']
  applied_hours_filter: str
  search_query: str
  ```

---

## SECTION 3: Data File Schemas

### 1. vehicles.txt
- File Name: vehicles.txt
- Purpose: Stores vehicles available for rental with specifications and status.
- Fields:
  1. vehicle_id (int)
  2. make (str)
  3. model (str)
  4. vehicle_type (str)
  5. daily_rate (float)
  6. seats (int)
  7. transmission (str)
  8. fuel_type (str)
  9. status (str)
- Example Lines:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

### 2. customers.txt
- File Name: customers.txt
- Purpose: Stores customers' contact and license data.
- Fields:
  1. customer_id (int)
  2. name (str)
  3. email (str)
  4. phone (str)
  5. driver_license (str)
  6. license_expiry (date: YYYY-MM-DD)
- Example Lines:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

### 3. locations.txt
- File Name: locations.txt
- Purpose: Stores pickup/dropoff location info.
- Fields:
  1. location_id (int)
  2. city (str)
  3. address (str)
  4. phone (str)
  5. hours (str)
  6. available_vehicles (int)
- Example Lines:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

### 4. rentals.txt
- File Name: rentals.txt
- Purpose: Stores rental transactions with dates, locations, price, and status.
- Fields:
  1. rental_id (int)
  2. vehicle_id (int)
  3. customer_id (int)
  4. pickup_date (date: YYYY-MM-DD)
  5. dropoff_date (date: YYYY-MM-DD)
  6. pickup_location (str)
  7. dropoff_location (str)
  8. total_price (float)
  9. status (str)
- Example Lines:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

### 5. insurance.txt
- File Name: insurance.txt
- Purpose: Stores insurance plan details.
- Fields:
  1. insurance_id (int)
  2. plan_name (str)
  3. description (str)
  4. daily_cost (float)
  5. coverage_limit (str or int)
  6. deductible (int)
- Example Lines:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

### 6. reservations.txt
- File Name: reservations.txt
- Purpose: Stores reservation info linked with rental, insurance, special requests.
- Fields:
  1. reservation_id (int)
  2. rental_id (int)
  3. vehicle_id (int)
  4. customer_id (int)
  5. status (str)
  6. insurance_id (int)
  7. special_requests (str)
- Example Lines:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

End of Design Specification
