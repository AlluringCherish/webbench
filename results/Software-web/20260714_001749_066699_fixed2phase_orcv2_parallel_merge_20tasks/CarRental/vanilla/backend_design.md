# CarRental Backend Design

---

## Section 1: Flask Routes and Business Logic Design

### 1. Dashboard Page
**Route:** `/dashboard`  
**Methods:** GET

- Fetch featured vehicles from `vehicles.txt` where status is "Available" and select featured (could be logic to choose first N vehicles or specific criteria).
- Display current promotions (static or fetched from a config).
- No request parameters.

### 2. Vehicle Search Page
**Route:** `/vehicles/search`  
**Methods:** GET

- Query Parameters: `location` (optional), `vehicle_type` (optional), `start_date` (optional), `end_date` (optional)
- Load all vehicles from `vehicles.txt` with status="Available".
- Filter by vehicle type and location availability.
- Filter availability based on rental date range by cross-checking `rentals.txt` for existing bookings overlapping with search dates.
- Return filtered vehicle data.

### 3. Vehicle Details Page
**Route:** `/vehicles/<int:vehicle_id>`  
**Methods:** GET

- Retrieve vehicle details from `vehicles.txt` by `vehicle_id`.
- Include vehicle specs: make, model, seats, transmission, fuel type, daily rate.
- Optionally fetch and display reviews (reviews not specified in requirements, so can be empty or static).

### 4. Booking Page
**Route:** `/booking`  
**Methods:** POST

- Request Body: JSON with `vehicle_id`, `pickup_location`, `dropoff_location`, `pickup_date`, `dropoff_date`, `customer_id`
- Validate vehicle availability for the requested date range by examining `rentals.txt`.
- Calculate total price = daily_rate * number of rental days.
- Store a temporary booking detail or return price to front-end for user confirmation.

### 5. Insurance Options Page
**Route:** `/insurance`  
**Methods:** GET

- Fetch all insurance plans from `insurance.txt`.
- Return insurance plans with details including plan name, description, daily cost, coverage limit, deductible.

### 6. Confirm Booking with Insurance
**Route:** `/booking/confirm`  
**Methods:** POST

- Request Body: JSON with `vehicle_id`, `customer_id`, `pickup_location`, `dropoff_location`, `pickup_date`, `dropoff_date`, `insurance_id`, `special_requests` (optional)
- Assign new `rental_id` and `reservation_id` (increment max existing IDs).
- Calculate total price: vehicle daily_rate * days + insurance daily_cost * days.
- Save new entry into `rentals.txt` with "Active" status.
- Save reservation data into `reservations.txt` including special requests.

### 7. Rental History Page
**Route:** `/rentals/history`  
**Methods:** GET

- Query Parameter: `customer_id` (optional), `status` (optional: All, Active, Completed, Cancelled)
- Load `rentals.txt` and filter by customer_id and status.
- Return rental history list.

### 8. Reservation Management Page
**Route:** `/reservations`  
**Methods:** GET, POST, PUT, DELETE

- GET: Query Parameter: `customer_id` (optional)
   - Return all current and upcoming reservations from `reservations.txt` filtered by customer if given.
- PUT `/reservations/<int:reservation_id>`: Modify reservation details (e.g., dates or cancel)
   - Update status or details in `reservations.txt`.
- DELETE `/reservations/<int:reservation_id>`: Cancel reservation
   - Set reservation and rental status to "Cancelled".

### 9. Special Requests Page
**Route:** `/reservations/<int:reservation_id>/special_requests`  
**Methods:** POST

- Request Body: JSON containing special request fields like driver assistance, GPS, child seat quantity, special notes.
- Append or update the `special_requests` field in `reservations.txt` for the given reservation.

### 10. Locations Page
**Route:** `/locations`  
**Methods:** GET

- Query Parameters: `hours` (optional), `search` (optional)
- Load all locations from `locations.txt`.
- Filter locations based on operating hours and search by city or name.
- Return location list.

---

## Section 2: Data File Schemas and Formats

### 1. vehicles.txt
- Fields: vehicle_id (int), make (str), model (str), vehicle_type (str), daily_rate (float), seats (int), transmission (str), fuel_type (str), status (str)
- Delimiter: `|`
- Example:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. customers.txt
- Fields: customer_id (int), name (str), email (str), phone (str), driver_license (str), license_expiry (date `YYYY-MM-DD`)
- Delimiter: `|`
- Example:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. locations.txt
- Fields: location_id (int), city (str), address (str), phone (str), hours (str), available_vehicles (int)
- Delimiter: `|`
- Example:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. rentals.txt
- Fields: rental_id (int), vehicle_id (int), customer_id (int), pickup_date (date `YYYY-MM-DD`), dropoff_date (date `YYYY-MM-DD`), pickup_location (str), dropoff_location (str), total_price (float), status (str)
- Delimiter: `|`
- Example:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. insurance.txt
- Fields: insurance_id (int), plan_name (str), description (str), daily_cost (float), coverage_limit (str or float), deductible (float)
- Delimiter: `|`
- Example:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. reservations.txt
- Fields: reservation_id (int), rental_id (int), vehicle_id (int), customer_id (int), status (str), insurance_id (int), special_requests (str)
- Delimiter: `|`
- Example:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
  ```

---

### Notes on Business Logic Implementation:

- ID generation for new rentals and reservations: Parse existing file and find max ID, then increment.
- Data Read/Write:
  - Read: Open file, read lines, split by `|`, map fields.
  - Write: Rewrite entire file with updated content or append for new records.
- Availability check for vehicles: Check if requested rental dates conflict with any active rentals for the same vehicle.
- Status fields distinguish current and historical data (e.g. Active, Completed, Cancelled).
- Special requests stored as a plain string describing options; consider JSON string if backend supports parsing.

This backend design document allows a backend developer to construct the entire Flask application routes and file data management logic for the CarRental app precisely as per requirements.