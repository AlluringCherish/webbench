# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                | HTTP Methods | Function Name           | Template File           | Context Variables (Type/Structure)                                                                                          | Navigation Actions from Buttons/Links                                                                                                   |
|------------------------------|--------------|------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| /dashboard                   | GET          | dashboard              | dashboard.html          | featured_destinations: List[Dict] (dest_id:int, name:str, country:str)
upcoming_trips: List[Dict] (trip_id:int, trip_name:str, start_date:str) | browse-destinations-button: navigates to /destinations
plan-itinerary-button: navigates to /itinerary                            |
| /destinations               | GET          | destinations           | destinations.html       | destinations: List[Dict] (dest_id:int, name:str, country:str, region:str)                                                     | view-destination-button-{{ dest.dest_id }}: navigates to /destinations/<int:dest_id>                                                    |
| /destinations/<int:dest_id> | GET          | destination_details    | destination_details.html| destination: Dict (dest_id:int, name:str, country:str, description:str, attractions:str)                                        | add-to-trip-button: posts to add destination to trip (implementation-specific)
                                                      |
| /itinerary                  | GET, POST   | itinerary              | itinerary.html          | itineraries: List[Dict] (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str) | add-activity-button: posts to add activity
edit/delete in itinerary-list: specific routes (not detailed here)                       |
| /accommodations             | GET          | accommodations         | accommodations.html     | hotels: List[Dict] (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str)         | (no explicit navigation from elements specified, assumed internal filtering)
                                                       |
| /transportation             | GET          | transportation         | transportation.html     | flights: List[Dict] (flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str) | (no explicit navigation specified)                                                                                                    |
| /packages                   | GET          | packages               | packages.html           | packages: List[Dict] (package_id:int, package_name:str, destination:str, duration_days:int, price:float)                      | view-package-details-button-{{ pkg.package_id }}: navigates to /packages/<int:package_id>
book-package-button-{{ pkg.package_id }}: posts booking                                   |
| /trips                     | GET          | trips                  | trips.html              | trips: List[Dict] (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str)                     | view-trip-details-button-{{ trip.trip_id }}: navigates to /trips/<int:trip_id>
edit-trip-button-{{ trip.trip_id }}: navigates to /trips/<int:trip_id>/edit
delete-trip-button-{{ trip.trip_id }}: posts to delete trip |
| /booking-confirmation       | GET          | booking_confirmation   | booking_confirmation.html| booking: Dict (confirmation_number:str, booking_details:str)                                                                  | download-itinerary-button: triggers download (implementation-specific)
share-trip-button: triggers share interaction (implementation-specific)
back-to-dashboard: navigates to /dashboard |
| /recommendations            | GET          | recommendations        | recommendations.html    | trending_destinations: List[Dict] (dest_id:int, name:str, popularity_rank:int), season_filter: str, budget_filter: str          | back-to-dashboard: navigates to /dashboard                                                                                           |

---

## Section 2: HTML Templates Specification

### templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Elements:
  - dashboard-page (Div): Container for dashboard page
  - featured-destinations (Div): Displays featured destinations
  - upcoming-trips (Div): Displays upcoming trips
  - browse-destinations-button (Button): Navigate to destinations page
  - plan-itinerary-button (Button): Navigate to itinerary planning page
- Context Variables:
  - featured_destinations: List[Dict]
    - dest_id: int
    - name: str
    - country: str
  - upcoming_trips: List[Dict]
    - trip_id: int
    - trip_name: str
    - start_date: str
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### templates/destinations.html
- Page Title: Travel Destinations
- Elements:
  - destinations-page (Div): Container for destinations page
  - search-destination (Input): Search input for destinations by name or country
  - region-filter (Dropdown): Filter destinations by region (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid (Div): Grid showing destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View details of specific destination
- Context Variables:
  - destinations: List[Dict]
    - dest_id: int
    - name: str
    - country: str
    - region: str
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### templates/destination_details.html
- Page Title: Destination Details
- Elements:
  - destination-details-page (Div): Container
  - destination-name (H1): Destination name
  - destination-country (Div): Country name
  - destination-description (Div): Detailed description
  - add-to-trip-button (Button): Add destination to trip action
  - destination-attractions (Div): Attractions and activities display
- Context Variables:
  - destination: Dict
    - dest_id: int
    - name: str
    - country: str
    - description: str
    - attractions: str
- Navigation Mappings:
  - add-to-trip-button: posts to add destination to itinerary (implementation-specific)

### templates/itinerary.html
- Page Title: Plan Your Itinerary
- Elements:
  - itinerary-page (Div): Container
  - itinerary-name-input (Input): Enter itinerary name
  - start-date-input (Input(date)): Start date selection
  - end-date-input (Input(date)): End date selection
  - add-activity-button (Button): Add activity
  - itinerary-list (Div): List of itineraries with edit/delete options
- Context Variables:
  - itineraries: List[Dict]
    - itinerary_id: int
    - itinerary_name: str
    - destination: str
    - start_date: str
    - end_date: str
    - activities: str
    - status: str
- Navigation Mappings:
  - add-activity-button: posts form data to /itinerary (implementation-specific)
  - edit/delete options: link/buttons to /itinerary/edit/<int:itinerary_id> or post delete

### templates/accommodations.html
- Page Title: Search Accommodations
- Elements:
  - accommodations-page (Div): Container
  - destination-input (Input): Destination city input
  - check-in-date (Input(date)): Check-in date
  - check-out-date (Input(date)): Check-out date
  - price-filter (Dropdown): Filter hotels by price range (Budget, Mid-range, Luxury)
  - hotels-list (Div): List hotels with name, rating, price, amenities
- Context Variables:
  - hotels: List[Dict]
    - hotel_id: int
    - name: str
    - city: str
    - rating: float
    - price_per_night: float
    - amenities: str
    - category: str
- Navigation Mappings:
  - Filtering and search handled internally; no navigation buttons specified

### templates/transportation.html
- Page Title: Book Flights
- Elements:
  - transportation-page (Div): Container
  - departure-city (Input): Departure city input
  - arrival-city (Input): Arrival city input
  - departure-date (Input(date)): Departure date
  - flight-class-filter (Dropdown): Flight class filter (Economy, Business, First Class)
  - available-flights (Div): List of available flights with airline, times, price
- Context Variables:
  - flights: List[Dict]
    - flight_id: int
    - airline: str
    - departure_city: str
    - arrival_city: str
    - departure_time: str
    - arrival_time: str
    - price: float
    - class_type: str
- Navigation Mappings:
  - No explicit navigation buttons or links specified

### templates/packages.html
- Page Title: Travel Packages
- Elements:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of package cards
  - duration-filter (Dropdown): Filter packages by duration (3-5 days, 7-10 days, 14+ days)
  - view-package-details-button-{{ pkg.package_id }} (Button): View package details
  - book-package-button-{{ pkg.package_id }} (Button): Book package
- Context Variables:
  - packages: List[Dict]
    - package_id: int
    - package_name: str
    - destination: str
    - duration_days: int
    - price: float
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', package_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: posts booking action

### templates/trips.html
- Page Title: My Trips
- Elements:
  - trips-page (Div): Container
  - trips-table (Table): Trips display
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: List[Dict]
    - trip_id: int
    - trip_name: str
    - destination: str
    - start_date: str
    - end_date: str
    - status: str
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }}: posts trip deletion

### templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Elements:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Booking confirmation number
  - booking-details (Div): Detailed booking info
  - download-itinerary-button (Button): Download itinerary PDF
  - share-trip-button (Button): Share trip details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - booking: Dict
    - confirmation_number: str
    - booking_details: str
- Navigation Mappings:
  - download-itinerary-button: triggers download (implementation-specific)
  - share-trip-button: triggers share (implementation-specific)
  - back-to-dashboard: url_for('dashboard')

### templates/recommendations.html
- Page Title: Travel Recommendations
- Elements:
  - recommendations-page (Div): Container
  - trending-destinations (Div): Trending destinations by popularity
  - recommendation-season-filter (Dropdown): Filter by season (Spring, Summer, Fall, Winter)
  - budget-filter (Dropdown): Filter by budget (Low, Medium, High)
  - back-to-dashboard (Button): Navigate to dashboard
- Context Variables:
  - trending_destinations: List[Dict]
    - dest_id: int
    - name: str
    - popularity_rank: int
  - season_filter: str
  - budget_filter: str
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### data/destinations.txt
- Fields and Order:
  1. dest_id (int)
  2. name (str)
  3. country (str)
  4. region (str)
  5. description (str)
  6. attractions (str)
  7. climate (str)
- Description: Stores travel destinations data with descriptive and geographic info.
- Example Rows:
  - 1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  - 2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  - 3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
- Note: No header row in file

### data/itineraries.txt
- Fields and Order:
  1. itinerary_id (int)
  2. itinerary_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. activities (str)
  7. status (str)
- Description: Stores user itineraries including activities and status.
- Example Rows:
  - 1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  - 2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  - 3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
- Note: No header row in file

### data/hotels.txt
- Fields and Order:
  1. hotel_id (int)
  2. name (str)
  3. city (str)
  4. rating (float)
  5. price_per_night (float)
  6. amenities (str)
  7. category (str)
- Description: Stores hotel information for accommodations search.
- Example Rows:
  - 1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  - 2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  - 3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
- Note: No header row in file

### data/flights.txt
- Fields and Order:
  1. flight_id (int)
  2. airline (str)
  3. departure_city (str)
  4. arrival_city (str)
  5. departure_time (str)
  6. arrival_time (str)
  7. price (float)
  8. class_type (str)
  9. duration (str)
- Description: Stores flight options for booking and searching.
- Example Rows:
  - 1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  - 2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  - 3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
- Note: No header row in file

### data/packages.txt
- Fields and Order:
  1. package_id (int)
  2. package_name (str)
  3. destination (str)
  4. duration_days (int)
  5. price (float)
  6. included_items (str)
  7. difficulty_level (str)
- Description: Stores travel package details.
- Example Rows:
  - 1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  - 2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  - 3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
- Note: No header row in file

### data/trips.txt
- Fields and Order:
  1. trip_id (int)
  2. trip_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. total_budget (float)
  7. status (str)
  8. created_date (str, YYYY-MM-DD)
- Description: Stores trip summary and status
- Example Rows:
  - 1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  - 2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  - 3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
- Note: No header row in file

### data/bookings.txt
- Fields and Order:
  1. booking_id (int)
  2. trip_id (int)
  3. booking_type (str)
  4. booking_date (str, YYYY-MM-DD)
  5. amount (float)
  6. confirmation_number (str)
  7. status (str)
- Description: Stores booking records linked to trips.
- Example Rows:
  - 1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  - 2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  - 3|3|Package|2025-01-12|1800.00|CONF003|Pending
- Note: No header row in file

---


