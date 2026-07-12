# CarRental Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name              | HTTP Method(s) | Template File            | Context Variables                                                                                      |
|----------------------------|----------------------------|----------------|--------------------------|------------------------------------------------------------------------------------------------------|
| /                          | redirect_to_dashboard       | GET            | N/A (redirect)            | N/A                                                                                                  |
| /dashboard                 | dashboard                  | GET            | dashboard.html            | featured_vehicles: List[Dict[str, str]]  # List of vehicle dicts with keys: vehicle_id (int), make, model, daily_rate (float as str)
                                                    promotions: List[str]  # List of promotion strings                                                  |
| /search                   | vehicle_search             | GET            | search.html               | vehicles: List[Dict[str, str or int or float]]  # Each dict with vehicle_id (int), make, model, vehicle_type (str), daily_rate (float as str), seats (int), transmission (str), status (str), fuel_type (str)
                                                      locations: List[str]  # List of location names (str)                                                   |
| /vehicle/<int:vehicle_id>  | vehicle_details            | GET            | vehicle_details.html      | vehicle: Dict[str, str or int or float]  # vehicle data with keys vehicle_id, make, model, vehicle_type, daily_rate, seats, transmission, fuel_type, status
                                                      reviews: List[str]  # List of review strings (empty list if no reviews)                               |
| /booking/<int:vehicle_id>  | booking                   | GET, POST      | booking.html              | GET: vehicle: Dict[str, str or int or float], locations: List[str]
                                                      POST: pickup_location (str), dropoff_location (str), pickup_date (str YYYY-MM-DD), dropoff_date (str YYYY-MM-DD), total_price (float), vehicle_id (int)
                                                      
| /insurance/<int:reservation_id> | insurance_options    | GET, POST      | insurance.html            | GET: insurances: List[Dict[str, str or float or int]]  # insurance_id (int), plan_name, description, daily_cost (float), coverage_limit (str), deductible (float)
                                                      POST: selected_insurance_id (int), reservation_id (int)
                                                      
| /history                  | rental_history             | GET            | history.html              | rentals: List[Dict[str, str or int or float]]  # rental_id, vehicle info (make, model), dates, pickup_location, dropoff_location, total_price (float), status
                                                      status_filter: str  # (All, Active, Completed, Cancelled)
                                                      
| /reservations             | reservations_management    | GET, POST      | reservations.html         | GET: reservations: List[Dict[str, str or int]]  # reservation_id, rental_id, vehicle info (make, model), customer_id, status, insurance_id, special_requests
                                                      POST: modification input fields or cancellation request with reservation_id (int)                     
| /special-requests          | special_requests           | GET, POST      | requests.html             | GET: reservations: List[Dict[str, str or int]]  # reservation_id, rental_id, vehicle info, status
                                                      POST: reservation_id (int), driver_assistance (bool), gps_option (bool), child_seat_quantity (int), special_notes (str) 
| /locations                | locations                  | GET            | locations.html            | locations: List[Dict[str, str or int]]  # location_id, city, address, phone, hours, available_vehicles
                                                      hours_filter: str  # (24/7, Business Hours, Weekend)
                                                      search_query: str  # Search string for city or name

---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-vehicles (Div): Displays featured vehicle recommendations
  - search-vehicles-button (Button): Navigates to Vehicle Search page using url_for('vehicle_search')
  - my-reservations-button (Button): Navigates to Reservations page using url_for('reservations_management')
  - promotions-section (Div): Displays current promotions
- Navigation:
  - search-vehicles-button &rarr; url_for('vehicle_search')
  - my-reservations-button &rarr; url_for('reservations_management')
- Context Variables:
  - featured_vehicles: List of dicts with keys vehicle_id (int), make (str), model (str), daily_rate (float as str)
  - promotions: List of promotion strings

---

### 2. Vehicle Search Page
- Filename: templates/search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): Main container
  - location-filter (Dropdown): Filter vehicles by pickup location; populated from context 'locations'
  - vehicle-type-filter (Dropdown): Filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury)
  - date-range-input (Input): Input for rental date range selection
  - vehicles-grid (Div): Grid of vehicle cards
  - view-details-button-{vehicle_id} (Button): Button per vehicle to view details; link route url_for('vehicle_details', vehicle_id=vehicle_id)
- Navigation:
  - view-details-button-{vehicle_id} &rarr; url_for('vehicle_details', vehicle_id=vehicle_id)
- Context Variables:
  - vehicles: List of dicts with keys: vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float as str), seats (int), transmission (str), status (str), fuel_type (str)
  - locations: List of location name strings

---

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): Main container
  - vehicle-name (H1): Name and model display (e.g., Toyota Camry)
  - vehicle-specs (Div): Shows specs - engine, seats, transmission
  - daily-rate (Div): Display daily rental rate
  - book-now-button (Button): Navigates to booking page url_for('booking', vehicle_id=vehicle.vehicle_id)
  - vehicle-reviews (Div): Section for customer reviews
- Navigation:
  - book-now-button &rarr; url_for('booking', vehicle_id=vehicle.vehicle_id)
- Context Variables:
  - vehicle: Dict with keys vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float as str), seats (int), transmission (str), fuel_type (str), status (str)
  - reviews: List of review text strings

---

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): Main container
  - pickup-location (Dropdown): List of location names
  - dropoff-location (Dropdown): List of location names
  - pickup-date (Input): Date picker input
  - dropoff-date (Input): Date picker input
  - calculate-price-button (Button): Button to calculate price
  - total-price (Div): Display calculated price
  - proceed-to-insurance-button (Button): Button to proceed to insurance options
- Navigation:
  - proceed-to-insurance-button &rarr; url_for('insurance_options', reservation_id=reservation_id)
- Context Variables:
  - vehicle: Dict with keys vehicle_id (int), make (str), model (str), daily_rate (float as str)
  - locations: List of location name strings

---

### 5. Insurance Options Page
- Filename: templates/insurance.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): Main container
  - insurance-options (Div): Displays insurance plans
  - select-insurance-{insurance_id} (Radio): Radio button per plan
  - insurance-description (Div): Description of selected plan
  - insurance-price (Div): Daily cost of selected insurance
  - confirm-booking-button (Button): Confirm booking with insurance
- Navigation:
  - confirm-booking-button &rarr; Confirm final booking action (POST)
- Context Variables:
  - insurances: List of dicts with keys insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (str), deductible (float)
  - selected_insurance_id: int (for POST)

---

### 6. Rental History Page
- Filename: templates/history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): Main container
  - rentals-table (Table): Columns for ID, Vehicle, Dates, Pickup Location, Dropoff Location, Total Price, Status
  - view-rental-details-{rental_id} (Button): View details button per rental
  - status-filter (Dropdown): Filter rentals by status (All, Active, Completed, Cancelled)
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard &rarr; url_for('dashboard')
- Context Variables:
  - rentals: List of dicts with keys rental_id (int), vehicle_make (str), vehicle_model(str), pickup_date (str), dropoff_date (str), pickup_location (str), dropoff_location (str), total_price (float as str), status (str)
  - status_filter: str

---

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): Main container
  - reservations-list (Div): List all reservations
  - modify-reservation-button-{reservation_id} (Button): Modify reservation button per reservation
  - cancel-reservation-button-{reservation_id} (Button): Cancel reservation button per reservation
  - sort-by-date-button (Button): Sort reservations by date
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard &rarr; url_for('dashboard')
- Context Variables:
  - reservations: List of dicts with keys reservation_id (int), rental_id (int), vehicle_make (str), vehicle_model (str), customer_id (int), status (str), insurance_id (int), special_requests (str)

---

### 8. Special Requests Page
- Filename: templates/requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): Main container
  - select-reservation (Dropdown): Select a reservation by reservation_id
  - driver-assistance-checkbox (Checkbox): Request driver assistance
  - gps-option-checkbox (Checkbox): Request GPS
  - child-seat-quantity (Input): Number input for child seats
  - special-notes (Textarea): Free text notes
  - submit-requests-button (Button): Submit requests
- Navigation:
  - submit-requests-button &rarr; POST to update special requests
- Context Variables:
  - reservations: List of dicts with keys reservation_id (int), rental_id (int), vehicle_make (str), vehicle_model (str), status (str)

---

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): Main container
  - locations-list (Div): List of locations with city, address, phone, hours, available vehicles
  - location-detail-button-{location_id} (Button): View location details button per location
  - hours-filter (Dropdown): Filter by operating hours (24/7, Business Hours, Weekend)
  - search-location-input (Input): Search by city or name
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation:
  - back-to-dashboard &rarr; url_for('dashboard')
- Context Variables:
  - locations: List of dicts with keys location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)
  - hours_filter: str
  - search_query: str

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Description: Stores all vehicle information with pricing, capacity, and status.
- Format (pipe-delimited):
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
```
- Field Types:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str (e.g., Economy, Compact, Sedan, SUV, Luxury)
  - daily_rate: float (price per day)
  - seats: int
  - transmission: str (e.g., Automatic, Manual)
  - fuel_type: str (e.g., Petrol, Diesel, Electric)
  - status: str (e.g., Available, Rented, Maintenance)
- Example lines:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```

---

### 2. customers.txt
- Description: Stores customer information including contact and license details.
- Format:
```
customer_id|name|email|phone|driver_license|license_expiry
```
- Field Types:
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

---

### 3. locations.txt
- Description: Lists pickup and dropoff locations with contact and operating hours.
- Format:
```
location_id|city|address|phone|hours|available_vehicles
```
- Field Types:
  - location_id: int
  - city: str
  - address: str
  - phone: str
  - hours: str (e.g., 24/7, 09:00-18:00)
  - available_vehicles: int
- Example lines:
```
1|New York|123 Main St, NYC|555-1000|24/7|12
2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
```

---

### 4. rentals.txt
- Description: Records rental transactions with vehicle, customer, dates, locations, price and status.
- Format:
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
```
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
- Example lines:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```

---

### 5. insurance.txt
- Description: Contains insurance plans with pricing and coverage details.
- Format:
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
```
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: float
- Example lines:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```

---

### 6. reservations.txt
- Description: Tracks reservations linked to rentals with insurance and special requests.
- Format:
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
```
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str (e.g., Confirmed, Active, Cancelled)
  - insurance_id: int
  - special_requests: str
- Example lines:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```

---

# End of Design Specification
