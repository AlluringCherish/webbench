# TravelPlanner Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                     | HTTP Methods | Function Name                | Template File                   | Context Variables (type & structure)                                                                                             | Navigation Actions Triggered by Buttons/Links                                                                        |
|----------------------------------|--------------|-----------------------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| /                                | GET          | dashboard                   | dashboard.html                 | featured_destinations: List[Dict] fields: dest_id(int), name(str), country(str), image(str optional)
  upcoming_trips: List[Dict] fields: trip_id(int), trip_name(str), start_date(str), end_date(str), status(str)                     | browse-destinations-button -> url_for('destinations')
  plan-itinerary-button -> url_for('itinerary')             |
| /destinations                    | GET, POST    | destinations                | destinations.html              | destinations: List[Dict] fields: dest_id(int), name(str), country(str), region(str)                                               | view-destination-button-{dest_id} -> url_for('destination_details', dest_id=dest_id)                                   |
| /destinations/<int:dest_id>     | GET, POST    | destination_details         | destination_details.html       | destination: Dict with dest_id(int), name(str), country(str), description(str), attractions(str), climate(str)                    | add-to-trip-button -> POST triggers adding destination to trip                                                      |
| /itinerary                      | GET, POST    | itinerary                   | itinerary.html                 | itineraries: List[Dict] fields: itinerary_id(int), itinerary_name(str), destination(str), start_date(str), end_date(str), activities(str), status(str) | add-activity-button -> POST add activity
  form submission -> POST create/update itinerary                       |
| /accommodations                 | GET, POST    | accommodations              | accommodations.html            | hotels: List[Dict] fields: hotel_id(int), name(str), city(str), rating(float), price_per_night(float), amenities(str), category(str) | N/A (search and filter update via form POST or GET)                                                                    |
| /transportation                | GET, POST    | transportation              | transportation.html            | flights: List[Dict] fields: flight_id(int), airline(str), departure_city(str), arrival_city(str), departure_time(str), arrival_time(str), price(float), class_type(str), duration(str) | N/A (search and filter update via form POST or GET)                                                                    |
| /packages                     | GET, POST    | packages                   | packages.html                 | packages: List[Dict] fields: package_id(int), package_name(str), destination(str), duration_days(int), price(float), included_items(str), difficulty_level(str) | view-package-details-button-{pkg_id} -> url_for('package_details', pkg_id=package_id)
  book-package-button-{pkg_id} -> POST book package |
| /trips                       | GET, POST    | trips                      | trips.html                   | trips: List[Dict] fields: trip_id(int), trip_name(str), destination(str), start_date(str), end_date(str), status(str)               | view-trip-details-button-{trip_id} -> url_for('trip_details', trip_id=trip_id)
  edit-trip-button-{trip_id} -> url_for('edit_trip', trip_id=trip_id)
  delete-trip-button-{trip_id} -> POST delete trip |
| /booking-confirmation         | GET          | booking_confirmation       | booking_confirmation.html      | booking: Dict fields: booking_id(int), trip_id(int), booking_type(str), booking_date(str), amount(float), confirmation_number(str), status(str)
  trip: Dict fields: trip_id(int), trip_name(str), destination(str), start_date(str), end_date(str), total_budget(float), status(str), created_date(str) | download-itinerary-button -> download PDF
  share-trip-button -> share trip details
  back-to-dashboard -> url_for('dashboard')                     |
| /recommendations             | GET          | recommendations            | recommendations.html          | trending_destinations: List[Dict]: dest_id(int), name(str), popularity(int)
  filters: Dict season(str), budget(str)                                                                            | back-to-dashboard -> url_for('dashboard')                                                                         |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- **Page Title**: Travel Planner Dashboard
- **Element IDs and Types**:
  - dashboard-page: Div - Container for the dashboard page
  - featured-destinations: Div - Display featured travel destinations
  - upcoming-trips: Div - Display upcoming planned trips
  - browse-destinations-button: Button - Navigate to destinations page
  - plan-itinerary-button: Button - Navigate to itinerary planning page
- **Context Variables**:
  - featured_destinations: List[Dict]
    - dest_id: int
    - name: str
    - country: str
  - upcoming_trips: List[Dict]
    - trip_id: int
    - trip_name: str
    - start_date: str (YYYY-MM-DD)
    - end_date: str (YYYY-MM-DD)
    - status: str
- **Navigation Mappings**:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

---

### 2. destinations.html
- **Page Title**: Travel Destinations
- **Element IDs and Types**:
  - destinations-page: Div
  - search-destination: Input (text) - Search destinations by name or country
  - region-filter: Dropdown - Filter by region (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid: Div - Grid of destination cards
  - view-destination-button-{{ dest.dest_id }}: Button - View destination details
- **Context Variables**:
  - destinations: List[Dict]
    - dest_id: int
    - name: str
    - country: str
    - region: str
- **Navigation Mappings**:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

---

### 3. destination_details.html
- **Page Title**: Destination Details
- **Element IDs and Types**:
  - destination-details-page: Div
  - destination-name: H1 - Destination name
  - destination-country: Div - Destination country
  - destination-description: Div
  - add-to-trip-button: Button - Add destination to trip
  - destination-attractions: Div - Main attractions and activities
- **Context Variables**:
  - destination: Dict
    - dest_id: int
    - name: str
    - country: str
    - description: str
    - attractions: str
    - climate: str
- **Navigation Mappings**:
  - add-to-trip-button: POST triggers adding destination to trip

---

### 4. itinerary.html
- **Page Title**: Plan Your Itinerary
- **Element IDs and Types**:
  - itinerary-page: Div
  - itinerary-name-input: Input (text)
  - start-date-input: Input (date)
  - end-date-input: Input (date)
  - add-activity-button: Button - Add activity to itinerary
  - itinerary-list: Div - List of created itineraries with edit/delete
- **Context Variables**:
  - itineraries: List[Dict]
    - itinerary_id: int
    - itinerary_name: str
    - destination: str
    - start_date: str (YYYY-MM-DD)
    - end_date: str (YYYY-MM-DD)
    - activities: str
    - status: str
- **Navigation Mappings**:
  - add-activity-button: POST add activity

---

### 5. accommodations.html
- **Page Title**: Search Accommodations
- **Element IDs and Types**:
  - accommodations-page: Div
  - destination-input: Input (text)
  - check-in-date: Input (date)
  - check-out-date: Input (date)
  - price-filter: Dropdown (Budget, Mid-range, Luxury)
  - hotels-list: Div - List hotels with name, rating, price, amenities
- **Context Variables**:
  - hotels: List[Dict]
    - hotel_id: int
    - name: str
    - city: str
    - rating: float
    - price_per_night: float
    - amenities: str
    - category: str
- **Navigation Mappings**:
  - No specific navigation buttons (results update on search/filter)

---

### 6. transportation.html
- **Page Title**: Book Flights
- **Element IDs and Types**:
  - transportation-page: Div
  - departure-city: Input (text)
  - arrival-city: Input (text)
  - departure-date: Input (date)
  - flight-class-filter: Dropdown (Economy, Business, First Class)
  - available-flights: Div - List flights with airline, times, prices
- **Context Variables**:
  - flights: List[Dict]
    - flight_id: int
    - airline: str
    - departure_city: str
    - arrival_city: str
    - departure_time: str
    - arrival_time: str
    - price: float
    - class_type: str
    - duration: str
- **Navigation Mappings**:
  - No specific navigation buttons (results update on search/filter)

---

### 7. packages.html
- **Page Title**: Travel Packages
- **Element IDs and Types**:
  - packages-page: Div
  - packages-grid: Div - Grid of travel package cards
  - duration-filter: Dropdown (3-5 days, 7-10 days, 14+ days)
  - view-package-details-button-{{ pkg.package_id }}: Button - View package details
  - book-package-button-{{ pkg.package_id }}: Button - Book selected package
- **Context Variables**:
  - packages: List[Dict]
    - package_id: int
    - package_name: str
    - destination: str
    - duration_days: int
    - price: float
    - included_items: str
    - difficulty_level: str
- **Navigation Mappings**:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: POST book package

---

### 8. trips.html
- **Page Title**: My Trips
- **Element IDs and Types**:
  - trips-page: Div
  - trips-table: Table - Display trips with destination, dates, status
  - view-trip-details-button-{{ trip.trip_id }}: Button - View trip details
  - edit-trip-button-{{ trip.trip_id }}: Button - Edit trip
  - delete-trip-button-{{ trip.trip_id }}: Button - Delete trip
- **Context Variables**:
  - trips: List[Dict]
    - trip_id: int
    - trip_name: str
    - destination: str
    - start_date: str (YYYY-MM-DD)
    - end_date: str (YYYY-MM-DD)
    - status: str
- **Navigation Mappings**:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }}: POST delete

---

### 9. booking_confirmation.html
- **Page Title**: Booking Confirmation
- **Element IDs and Types**:
  - confirmation-page: Div
  - confirmation-number: Div - Booking confirmation number
  - booking-details: Div - Detailed booking info
  - download-itinerary-button: Button - Download itinerary PDF
  - share-trip-button: Button - Share trip details
  - back-to-dashboard: Button - Navigate back to dashboard
- **Context Variables**:
  - booking: Dict
    - booking_id: int
    - trip_id: int
    - booking_type: str
    - booking_date: str (YYYY-MM-DD)
    - amount: float
    - confirmation_number: str
    - status: str
  - trip: Dict
    - trip_id: int
    - trip_name: str
    - destination: str
    - start_date: str
    - end_date: str
    - total_budget: float
    - status: str
    - created_date: str
- **Navigation Mappings**:
  - download-itinerary-button: trigger file download
  - share-trip-button: trigger share function
  - back-to-dashboard: url_for('dashboard')

---

### 10. recommendations.html
- **Page Title**: Travel Recommendations
- **Element IDs and Types**:
  - recommendations-page: Div
  - trending-destinations: Div - Display trending destinations by popularity
  - recommendation-season-filter: Dropdown (Spring, Summer, Fall, Winter)
  - budget-filter: Dropdown (Low, Medium, High)
  - back-to-dashboard: Button - Navigate back to dashboard
- **Context Variables**:
  - trending_destinations: List[Dict]
    - dest_id: int
    - name: str
    - popularity: int
  - filters: Dict
    - season: str
    - budget: str
- **Navigation Mappings**:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  1. dest_id (int)
  2. name (str)
  3. country (str)
  4. region (str)
  5. description (str)
  6. attractions (str) - comma-separated
  7. climate (str)
- Description: Stores all travel destination details
- Example rows:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

---

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, no header):
  1. itinerary_id (int)
  2. itinerary_name (str)
  3. destination (str)
  4. start_date (YYYY-MM-DD)
  5. end_date (YYYY-MM-DD)
  6. activities (str) - comma separated list of activities
  7. status (str) - e.g., Planned, In Progress
- Description: Stores user-created itineraries with schedules
- Example rows:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

---

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, no header):
  1. hotel_id (int)
  2. name (str)
  3. city (str)
  4. rating (float)
  5. price_per_night (float)
  6. amenities (str) - comma separated
  7. category (str) - Budget, Mid-range, Luxury
- Description: Stores hotel listings for accommodations
- Example rows:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

---

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, no header):
  1. flight_id (int)
  2. airline (str)
  3. departure_city (str)
  4. arrival_city (str)
  5. departure_time (str) - format HH:MM or HH:MM next day
  6. arrival_time (str) - format HH:MM or HH:MM next day
  7. price (float)
  8. class_type (str) - Economy, Business, First Class
  9. duration (str) - format like '7 hours 30 minutes'
- Description: Stores flight information for booking
- Example rows:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

---

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, no header):
  1. package_id (int)
  2. package_name (str)
  3. destination (str)
  4. duration_days (int)
  5. price (float)
  6. included_items (str) - comma separated items
  7. difficulty_level (str) - Easy, Moderate, Hard
- Description: Stores pre-designed travel packages
- Example rows:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

---

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, no header):
  1. trip_id (int)
  2. trip_name (str)
  3. destination (str)
  4. start_date (YYYY-MM-DD)
  5. end_date (YYYY-MM-DD)
  6. total_budget (float)
  7. status (str)
  8. created_date (YYYY-MM-DD)
- Description: Stores all created trips
- Example rows:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

---

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  1. booking_id (int)
  2. trip_id (int)
  3. booking_type (str) - Hotel, Flight, Package
  4. booking_date (YYYY-MM-DD)
  5. amount (float)
  6. confirmation_number (str)
  7. status (str) - Confirmed, Pending
- Description: Stores all booking records
- Example rows:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending

---