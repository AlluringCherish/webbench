# CarRental Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name           | HTTP Methods | Template Filename           | Context Variables (Name: Type)                                                           |
|---------------------------|------------------------|--------------|----------------------------|------------------------------------------------------------------------------------------|
| /                         | root_redirect           | GET          | -                          | - Redirect to `dashboard` route                                                        |
| /dashboard                | dashboard              | GET          | dashboard.html             | featured_vehicles: List[Vehicle], promotions: List[Promotion]                           |
| /search                  | vehicle_search         | GET, POST    | search.html                | vehicles: List[Vehicle], location_filter_options: List[str], vehicle_type_filter_options: List[str], selected_location: Optional[str], selected_vehicle_type: Optional[str], selected_date_range: Optional[str] |
| /vehicle/<int:vehicle_id> | vehicle_details        | GET          | vehicle_details.html       | vehicle: Vehicle, reviews: List[Review]                                                |
| /booking/<int:vehicle_id> | booking                | GET, POST    | booking.html               | vehicle: Vehicle, pickup_location_options: List[str], dropoff_location_options: List[str], pickup_date: Optional[str], dropoff_date: Optional[str], total_price: Optional[float] |
| /insurance/<int:reservation_id> | insurance_options      | GET, POST    | insurance.html             | insurance_plans: List[Insurance], selected_plan: Optional[Insurance], reservation_id: int |
| /history                 | rental_history         | GET          | history.html               | rentals: List[Rental], status_filter_options: List[str], selected_status: str           |
| /reservations            | reservations           | GET, POST    | reservations.html          | reservations: List[Reservation]                                                        |
| /reservations/modify/<int:reservation_id> | modify_reservation     | GET, POST    | modify_reservation.html (optional) | reservation: Reservation, vehicle: Vehicle                                            |
| /reservations/cancel/<int:reservation_id> | cancel_reservation     | POST         | -                          | - Redirect to `reservations` route                                                    |
| /special_requests         | special_requests       | GET, POST    | special_requests.html      | reservations_for_selection: List[Reservation], special_request_form: Dict            |
| /locations               | locations              | GET          | locations.html             | locations: List[Location], hours_filter_options: List[str], selected_hours_filter: Optional[str], search_location_query: Optional[str] |

---

## Section 2: HTML Template Specification

### 1. templates/dashboard.html
- Page Title: "Car Rental Dashboard"
- Elements:
  - ID: dashboard-page (Div) - Container for dashboard
  - ID: featured-vehicles (Div) - Displays featured vehicles (list of vehicles with details)
  - ID: search-vehicles-button (Button) - Navigates to vehicle_search route
  - ID: my-reservations-button (Button) - Navigates to reservations route
  - ID: promotions-section (Div) - Displays current promotions
- Navigation:
  - search-vehicles-button -> url_for('vehicle_search')
  - my-reservations-button -> url_for('reservations')
- Context Variables:
  - featured_vehicles: List of Vehicle objects
  - promotions: List of Promotion objects

### 2. templates/search.html
- Page Title: "Search Vehicles"
- Elements:
  - ID: search-page (Div) - Container
  - ID: location-filter (Dropdown) - Options from location_filter_options
  - ID: vehicle-type-filter (Dropdown) - Options from vehicle_type_filter_options
  - ID: date-range-input (Input) - User input for rental date range
  - ID: vehicles-grid (Div) - Displays filtered vehicle cards
  - ID Pattern: view-details-button-{{ vehicle.vehicle_id }} (Button) - Vehicle details button
- Navigation:
  - view-details-button-{{ vehicle.vehicle_id }} -> url_for('vehicle_details', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicles: List[Vehicle]
  - location_filter_options: List[str]
  - vehicle_type_filter_options: List[str]
  - selected_location: Optional[str]
  - selected_vehicle_type: Optional[str]
  - selected_date_range: Optional[str]

### 3. templates/vehicle_details.html
- Page Title: "Vehicle Details"
- Elements:
  - ID: vehicle-details-page (Div) - Container
  - ID: vehicle-name (H1) - Displays vehicle make and model
  - ID: vehicle-specs (Div) - Displays engine, seats, transmission
  - ID: daily-rate (Div) - Shows daily rental rate
  - ID: book-now-button (Button) - Navigates to booking page
  - ID: vehicle-reviews (Div) - Shows customer reviews
- Navigation:
  - book-now-button -> url_for('booking', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: Vehicle
  - reviews: List[Review]

### 4. templates/booking.html
- Page Title: "Book Your Rental"
- Elements:
  - ID: booking-page (Div) - Container
  - ID: pickup-location (Dropdown) - Options: pickup_location_options
  - ID: dropoff-location (Dropdown) - Options: dropoff_location_options
  - ID: pickup-date (Input) - Date input
  - ID: dropoff-date (Input) - Date input
  - ID: calculate-price-button (Button) - Calculate total rental price
  - ID: total-price (Div) - Shows calculated price
  - ID: proceed-to-insurance-button (Button) - Proceeds to insurance options
- Navigation:
  - proceed-to-insurance-button -> url_for('insurance_options', reservation_id=reservation_id)
- Context Variables:
  - vehicle: Vehicle
  - pickup_location_options: List[str]
  - dropoff_location_options: List[str]
  - pickup_date: Optional[str]
  - dropoff_date: Optional[str]
  - total_price: Optional[float]
  - reservation_id: int (generated after booking submission)

### 5. templates/insurance.html
- Page Title: "Select Insurance Coverage"
- Elements:
  - ID: insurance-page (Div) - Container
  - ID: insurance-options (Div) - Displays insurance plans
  - ID Pattern: select-insurance-{{ insurance.insurance_id }} (Radio) - Select insurance plan
  - ID: insurance-description (Div) - Description of selected plan
  - ID: insurance-price (Div) - Price of selected insurance
  - ID: confirm-booking-button (Button) - Confirm booking with insurance
- Navigation:
  - confirm-booking-button -> POST to confirm booking endpoint, then redirect
- Context Variables:
  - insurance_plans: List[Insurance]
  - selected_plan: Optional[Insurance]
  - reservation_id: int

### 6. templates/history.html
- Page Title: "Rental History"
- Elements:
  - ID: history-page (Div) - Container
  - ID: rentals-table (Table) - Columns: ID, vehicle, dates, location, status
  - ID Pattern: view-rental-details-{{ rental.rental_id }} (Button) - Rental details
  - ID: status-filter (Dropdown) - Options: All, Active, Completed, Cancelled
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - rentals: List[Rental]
  - status_filter_options: List[str] = ["All", "Active", "Completed", "Cancelled"]
  - selected_status: str

### 7. templates/reservations.html
- Page Title: "My Reservations"
- Elements:
  - ID: reservations-page (Div) - Container
  - ID: reservations-list (Div) - Lists reservations
  - ID Pattern: modify-reservation-button-{{ reservation.reservation_id }} (Button) - Modify
  - ID Pattern: cancel-reservation-button-{{ reservation.reservation_id }} (Button) - Cancel
  - ID: sort-by-date-button (Button) - Sort reservations by date
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - reservations: List[Reservation]

### 8. templates/special_requests.html
- Page Title: "Special Requests"
- Elements:
  - ID: requests-page (Div) - Container
  - ID: select-reservation (Dropdown) - Select reservation
  - ID: driver-assistance-checkbox (Checkbox) - Driver assistance
  - ID: gps-option-checkbox (Checkbox) - GPS option
  - ID: child-seat-quantity (Input) - Number input
  - ID: special-notes (Textarea) - Notes input
  - ID: submit-requests-button (Button) - Submit requests
- Navigation:
  - submit-requests-button -> POST submit special requests
- Context Variables:
  - reservations_for_selection: List[Reservation]
  - special_request_form: Dict

### 9. templates/locations.html
- Page Title: "Pickup and Dropoff Locations"
- Elements:
  - ID: locations-page (Div) - Container
  - ID: locations-list (Div) - Lists all locations
  - ID Pattern: location-detail-button-{{ location.location_id }} (Button) - View location details
  - ID: hours-filter (Dropdown) - Filter options: 24/7, Business Hours, Weekend
  - ID: search-location-input (Input) - Search by city or name
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - locations: List[Location]
  - hours_filter_options: List[str] = ["24/7", "Business Hours", "Weekend"]
  - selected_hours_filter: Optional[str]
  - search_location_query: Optional[str]

---

## Section 3: Data File Schemas

### 1. Vehicles Data (`vehicles.txt`)
Format: `vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status`
- vehicle_id: int
- make: str
- model: str
- vehicle_type: str (Economy, Compact, Sedan, SUV, Luxury)
- daily_rate: float
- seats: int
- transmission: str (Automatic, Manual)
- fuel_type: str
- status: str (Available, Unavailable)

Example Data:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

### 2. Customers Data (`customers.txt`)
Format: `customer_id|name|email|phone|driver_license|license_expiry`
- customer_id: int
- name: str
- email: str
- phone: str
- driver_license: str
- license_expiry: date (YYYY-MM-DD)

Example Data:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```

### 3. Locations Data (`locations.txt`)
Format: `location_id|city|address|phone|hours|available_vehicles`
- location_id: int
- city: str
- address: str
- phone: str
- hours: str (e.g., 24/7, 09:00-18:00)
- available_vehicles: int

Example Data:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

### 4. Rentals Data (`rentals.txt`)
Format: `rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status`
- rental_id: int
- vehicle_id: int
- customer_id: int
- pickup_date: date (YYYY-MM-DD)
- dropoff_date: date (YYYY-MM-DD)
- pickup_location: str
- dropoff_location: str
- total_price: float
- status: str (Active, Completed, Cancelled)

Example Data:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

### 5. Insurance Data (`insurance.txt`)
Format: `insurance_id|plan_name|description|daily_cost|coverage_limit|deductible`
- insurance_id: int
- plan_name: str
- description: str
- daily_cost: float
- coverage_limit: str (could be number or 'Unlimited')
- deductible: int

Example Data:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

### 6. Reservations Data (`reservations.txt`)
Format: `reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests`
- reservation_id: int
- rental_id: int
- vehicle_id: int
- customer_id: int
- status: str (Confirmed, Active, Cancelled)
- insurance_id: int
- special_requests: str

Example Data:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

# End of CarRental Application Design Specification
