# CarRental Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                | Function Name            | HTTP Method(s) | Template File                | Context Variables                                                                                          |
|---------------------------|--------------------------|----------------|------------------------------|-----------------------------------------------------------------------------------------------------------|
| /                         | root_redirect            | GET            | *Redirects to* `/dashboard`  | None                                                                                                      |
| /dashboard                | dashboard                | GET            | dashboard.html               | featured_vehicles: list[dict], promotions: list[str]                                                      |
| /vehicles                 | vehicle_search           | GET            | vehicle_search.html          | locations: list[str], vehicle_types: list[str], vehicles: list[dict]                                     |
| /vehicle/<int:vehicle_id> | vehicle_details          | GET            | vehicle_details.html         | vehicle: dict, reviews: list[dict]                                                                        |
| /booking                  | booking_page             | GET, POST      | booking.html                 | locations: list[str], pickup_location: str (POST), dropoff_location: str (POST), pickup_date: str (POST), dropoff_date: str (POST), total_price: float (calculated POST) |
| /insurance                | insurance_options        | GET, POST      | insurance_options.html       | insurance_plans: list[dict], selected_insurance: dict (POST)                                             |
| /rental-history           | rental_history           | GET            | rental_history.html          | rentals: list[dict], status_filter: str                                                                      |
| /reservations             | reservation_management   | GET            | reservations.html            | reservations: list[dict]                                                                                   |
| /reservation/modify/<int:reservation_id> | modify_reservation       | POST           | *No Template (redirects back to reservations)* | reservation_id: int (form data), modification details extracted in POST                                   |
| /reservation/cancel/<int:reservation_id> | cancel_reservation       | POST           | *No Template (redirects back to reservations)* | reservation_id: int                                                                                        |
| /special-requests         | special_requests         | GET, POST      | special_requests.html        | reservations: list[dict], selected_reservation_id: int (POST), driver_assistance: bool (POST), gps_option: bool (POST), child_seats: int (POST), special_notes: str (POST) |
| /locations                | locations                | GET            | locations.html               | locations: list[dict]                                                                                      |

**Details and Notes:**
- The root route `/` must redirect the user automatically to `/dashboard`.
- All routes support methods as needed (mostly GET, with POST for forms where data submission occurs).
- Context variables correspond exactly to the data schemas and input forms for correct rendering.
- Navigation: All pages have navigation endpoints aligned with the buttons and links described in Section 2.

---

## Section 2: HTML Template Specifications (Frontend)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Car Rental Dashboard
- Element IDs:
  - dashboard-page (Div): main container
  - featured-vehicles (Div): displays featured vehicle recommendations
  - search-vehicles-button (Button): navigates to vehicle search page (url_for 'vehicle_search')
  - my-reservations-button (Button): navigates to reservations page (url_for 'reservation_management')
  - promotions-section (Div): displays current promotions
- Navigation:
  - search-vehicles-button -> vehicle_search
  - my-reservations-button -> reservation_management
- Context Variables:
  - featured_vehicles: list of dicts {vehicle_id:int, make:str, model:str, daily_rate:float}
  - promotions: list of strings

### 2. Vehicle Search Page
- Filename: templates/vehicle_search.html
- Page Title: Search Vehicles
- Element IDs:
  - search-page (Div): main container
  - location-filter (Dropdown): filter by pickup location
  - vehicle-type-filter (Dropdown): filter by vehicle type
  - date-range-input (Input): select rental date range
  - vehicles-grid (Div): grid of vehicle cards
  - view-details-button-{vehicle_id} (Button): view vehicle details for each vehicle
- Navigation:
  - view-details-button-{vehicle_id} -> vehicle_details(vehicle_id=vehicle_id)
- Context Variables:
  - locations: list of strings
  - vehicle_types: list of strings ["Economy", "Compact", "Sedan", "SUV", "Luxury"]
  - vehicles: list of dicts {vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float}

### 3. Vehicle Details Page
- Filename: templates/vehicle_details.html
- Page Title: Vehicle Details
- Element IDs:
  - vehicle-details-page (Div): main container
  - vehicle-name (H1): vehicle make and model
  - vehicle-specs (Div): specs like engine, seats, transmission
  - daily-rate (Div): display daily rental rate
  - book-now-button (Button): proceed to booking page
  - vehicle-reviews (Div): customer reviews section
- Navigation:
  - book-now-button -> booking_page
- Context Variables:
  - vehicle: dict {vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int, transmission:str, fuel_type:str, status:str}
  - reviews: list of dicts {reviewer:str, rating:int, comment:str}

### 4. Booking Page
- Filename: templates/booking.html
- Page Title: Book Your Rental
- Element IDs:
  - booking-page (Div): main container
  - pickup-location (Dropdown): select pickup location
  - dropoff-location (Dropdown): select dropoff location
  - pickup-date (Input): select pickup date
  - dropoff-date (Input): select dropoff date
  - calculate-price-button (Button): calculate total rental price
  - total-price (Div): display calculated total price
  - proceed-to-insurance-button (Button): proceed to insurance options
- Navigation:
  - proceed-to-insurance-button -> insurance_options
- Context Variables:
  - locations: list of strings
  - pickup_location: str (when POST)
  - dropoff_location: str (when POST)
  - pickup_date: str (when POST, format YYYY-MM-DD)
  - dropoff_date: str (when POST, format YYYY-MM-DD)
  - total_price: float (calculated and shown in POST)

### 5. Insurance Options Page
- Filename: templates/insurance_options.html
- Page Title: Select Insurance Coverage
- Element IDs:
  - insurance-page (Div): main container
  - insurance-options (Div): list of insurance plans
  - select-insurance-{insurance_id} (Radio): select insurance plan
  - insurance-description (Div): description of selected insurance plan
  - insurance-price (Div): price of selected insurance
  - confirm-booking-button (Button): confirm booking with insurance
- Navigation:
  - confirm-booking-button -> (form submission confirms booking)
- Context Variables:
  - insurance_plans: list of dicts {insurance_id:int, plan_name:str, description:str, daily_cost:float, coverage_limit:str, deductible:int}
  - selected_insurance: dict or None

### 6. Rental History Page
- Filename: templates/rental_history.html
- Page Title: Rental History
- Element IDs:
  - history-page (Div): main container
  - rentals-table (Table): list of rentals
  - view-rental-details-{rental_id} (Button): view details of rental
  - status-filter (Dropdown): filter rentals by status
  - back-to-dashboard (Button): navigate back to dashboard
- Navigation:
  - back-to-dashboard -> dashboard
- Context Variables:
  - rentals: list of dicts {rental_id:int, vehicle_id:int, customer_id:int, pickup_date:str, dropoff_date:str, pickup_location:str, dropoff_location:str, total_price:float, status:str}
  - status_filter: str

### 7. Reservation Management Page
- Filename: templates/reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (Div): main container
  - reservations-list (Div): list of reservations
  - modify-reservation-button-{reservation_id} (Button): modify a reservation
  - cancel-reservation-button-{reservation_id} (Button): cancel a reservation
  - sort-by-date-button (Button): sort reservations by date
  - back-to-dashboard (Button): navigate back to dashboard
- Navigation:
  - back-to-dashboard -> dashboard
- Context Variables:
  - reservations: list of dicts {reservation_id:int, rental_id:int, vehicle_id:int, customer_id:int, status:str, insurance_id:int, special_requests:str}

### 8. Special Requests Page
- Filename: templates/special_requests.html
- Page Title: Special Requests
- Element IDs:
  - requests-page (Div): main container
  - select-reservation (Dropdown): select reservation to add requests
  - driver-assistance-checkbox (Checkbox): driver assistance request
  - gps-option-checkbox (Checkbox): GPS option
  - child-seat-quantity (Input): number of child seats
  - special-notes (Textarea): special notes input
  - submit-requests-button (Button): submit special requests
- Navigation:
  - submit-requests-button -> (form submission handles special requests)
- Context Variables:
  - reservations: list of dicts {reservation_id:int, rental_id:int, vehicle_id:int, customer_id:int, status:str, insurance_id:int, special_requests:str}
  - selected_reservation_id: int (when POST)
  - driver_assistance: bool (when POST)
  - gps_option: bool (when POST)
  - child_seats: int (when POST)
  - special_notes: str (when POST)

### 9. Locations Page
- Filename: templates/locations.html
- Page Title: Pickup and Dropoff Locations
- Element IDs:
  - locations-page (Div): main container
  - locations-list (Div): list of rental locations
  - location-detail-button-{location_id} (Button): view location details
  - hours-filter (Dropdown): filter by operating hours
  - search-location-input (Input): search locations by city or name
  - back-to-dashboard (Button): navigate back to dashboard
- Navigation:
  - back-to-dashboard -> dashboard
- Context Variables:
  - locations: list of dicts {location_id:int, city:str, address:str, phone:str, hours:str, available_vehicles:int}

---

## Section 3: Data File Schemas

### 1. vehicles.txt
- Filename: data/vehicles.txt
- Format (pipe-delimited):
```
vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
```
- Field Types:
  - vehicle_id: int
  - make: str
  - model: str
  - vehicle_type: str
  - daily_rate: float
  - seats: int
  - transmission: str
  - fuel_type: str
  - status: str
- Example Lines:
```
1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
```
- Description: Stores all vehicle information including type, pricing, and availability.

### 2. customers.txt
- Filename: data/customers.txt
- Format (pipe-delimited):
```
customer_id|name|email|phone|driver_license|license_expiry
```
- Field Types:
  - customer_id: int
  - name: str
  - email: str
  - phone: str
  - driver_license: str
  - license_expiry: date (ISO format YYYY-MM-DD)
- Example Lines:
```
1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
```
- Description: Stores customer details including contact and license information.

### 3. locations.txt
- Filename: data/locations.txt
- Format (pipe-delimited):
```
location_id|city|address|phone|hours|available_vehicles
```
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
- Description: Stores pickup and dropoff location details and availability.

### 4. rentals.txt
- Filename: data/rentals.txt
- Format (pipe-delimited):
```
rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
```
- Field Types:
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - pickup_date: date (ISO format YYYY-MM-DD)
  - dropoff_date: date (ISO format YYYY-MM-DD)
  - pickup_location: str
  - dropoff_location: str
  - total_price: float
  - status: str (e.g., "Active", "Completed", "Cancelled")
- Example Lines:
```
1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
```
- Description: Stores rental transaction records with dates and locations.

### 5. insurance.txt
- Filename: data/insurance.txt
- Format (pipe-delimited):
```
insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
```
- Field Types:
  - insurance_id: int
  - plan_name: str
  - description: str
  - daily_cost: float
  - coverage_limit: str
  - deductible: int
- Example Lines:
```
1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
2|Standard Coverage|Collision and theft protection|12.00|250000|500
3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
```
- Description: Stores insurance plans available for rentals.

### 6. reservations.txt
- Filename: data/reservations.txt
- Format (pipe-delimited):
```
reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
```
- Field Types:
  - reservation_id: int
  - rental_id: int
  - vehicle_id: int
  - customer_id: int
  - status: str
  - insurance_id: int
  - special_requests: str
- Example Lines:
```
1|1|1|1|Confirmed|2|Driver assistance requested
2|2|2|2|Active|1|GPS and child seat needed
```
- Description: Stores reservation states and special requests linked to rentals.

---

*End of CarRental Design Specification*