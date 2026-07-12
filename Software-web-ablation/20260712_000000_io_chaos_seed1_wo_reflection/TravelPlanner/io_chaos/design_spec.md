# TravelPlanner Application - Design Specifications

---

## Section 1: Flask Routes Specification

| Route Endpoint                       | HTTP Methods | Function Name             | Template File          | Context Variables (Name: Type, Structure)                                                                                                      | Navigation Actions Triggered By Buttons/Links                                       |
|------------------------------------|--------------|---------------------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| / (Dashboard)                      | GET          | dashboard                 | dashboard.html          | featured_destinations: List[Dict{dest_id: int, name: str, country: str}], upcoming_trips: List[Dict{trip_id: int, trip_name: str, destination: str, start_date: str}] | browse-destinations-button -> /destinations                                        |
| /destinations                     | GET          | destinations              | destinations.html       | destinations: List[Dict{dest_id: int, name: str, country: str, region: str}], search_query: str (optional), region_filter: str (optional)           | view-destination-button-{{dest_id}} -> /destinations/<int:dest_id>                  |
| /destinations/<int:dest_id>       | GET          | destination_details       | destination_details.html| destination: Dict{dest_id: int, name: str, country: str, description: str, attractions: str}                                                    | add-to-trip-button -> Add destination to trip action                                 |
| /itinerary                       | GET, POST    | itinerary                 | itinerary.html          | itineraries: List[Dict{itinerary_id: int, itinerary_name: str, destination: str, start_date: str, end_date: str, activities: str, status: str}]    | add-activity-button -> Add activity to itinerary (POST), itinerary-list edit/delete actions |
| /accommodations                  | GET          | accommodations            | accommodations.html     | hotels: List[Dict{hotel_id: int, name: str, city: str, rating: float, price_per_night: float, amenities: str, category: str}], search filters available | hotels-list items display details available                                        |
| /transportation                 | GET          | transportation            | transportation.html     | flights: List[Dict{flight_id: int, airline: str, departure_city: str, arrival_city: str, departure_time: str, arrival_time: str, price: float, class_type: str, duration: str}], filter values | available-flights items with pricing and booking options displayed                 |
| /packages                      | GET          | packages                  | packages.html           | packages: List[Dict{package_id: int, package_name: str, destination: str, duration_days: int, price: float}], duration_filter: str (optional)      | view-package-details-button-{{pkg_id}} -> /packages/<int:package_id>                |
|                                 |              |                           |                        |                                                                                                                                            | book-package-button-{{pkg_id}} -> Book selected package action                      |
| /trips                         | GET          | trips                     | trips.html              | trips: List[Dict{trip_id: int, trip_name: str, destination: str, start_date: str, end_date: str, status: str}]                                   | view-trip-details-button-{{trip_id}} -> /trips/<int:trip_id>                        |
|                                 |              |                           |                        |                                                                                                                                            | edit-trip-button-{{trip_id}} -> Edit trip action                                   |
|                                 |              |                           |                        |                                                                                                                                            | delete-trip-button-{{trip_id}} -> Delete trip action                               |
| /booking-confirmation/<int:booking_id> | GET          | booking_confirmation      | booking_confirmation.html | booking: Dict{booking_id: int, trip_id: int, booking_type: str, booking_date: str, amount: float, confirmation_number: str, status: str}             | download-itinerary-button -> Download itinerary PDF                               |
|                                 |              |                           |                        |                                                                                                                                            | share-trip-button -> Share trip details                                            |
|                                 |              |                           |                        |                                                                                                                                            | back-to-dashboard -> /                                                          |
| /recommendations               | GET          | recommendations           | recommendations.html     | recommendations: List[Dict], trending_destinations: List[Dict], filters: Dict{season: str, budget: str}                                       | back-to-dashboard -> /                                                          |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page: Div - Main container of dashboard
  - featured-destinations: Div - Lists featured destinations
  - upcoming-trips: Div - Shows upcoming trips
  - browse-destinations-button: Button - Navigates to /destinations
  - plan-itinerary-button: Button - Navigates to /itinerary
- Context Variables:
  - featured_destinations: List[Dict{dest_id: int, name: str, country: str}]
  - upcoming_trips: List[Dict{trip_id: int, trip_name: str, destination: str, start_date: str}]
- Navigation mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. destinations.html
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page: Div - Page container
  - search-destination: Input (text) - Search by name or country
  - region-filter: Dropdown - Filter by region
  - destinations-grid: Div - Grid of destination cards
  - view-destination-button-{{ dest.dest_id }}: Button each card - View detailed destination
- Context Variables:
  - destinations: List[Dict{dest_id: int, name: str, country: str, region: str}]
  - search_query: str (optional)
  - region_filter: str (optional)
- Navigation mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. destination_details.html
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page: Div - Main container
  - destination-name: H1 - Destination's name
  - destination-country: Div - Destination's country
  - destination-description: Div - Detailed description
  - add-to-trip-button: Button - Adds destination to trip
  - destination-attractions: Div - Main attractions and activities
- Context Variables:
  - destination: Dict{dest_id: int, name: str, country: str, description: str, attractions: str}
- Navigation mappings:
  - add-to-trip-button: triggers adding destination to itinerary/trip feature

### 4. itinerary.html
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page: Div - Main container
  - itinerary-name-input: Input (text) - Enter itinerary name
  - start-date-input: Input (date) - Select start date
  - end-date-input: Input (date) - Select end date
  - add-activity-button: Button - Add activity to itinerary
  - itinerary-list: Div - Lists existing itineraries with edit/delete options
- Context Variables:
  - itineraries: List[Dict{itinerary_id: int, itinerary_name: str, destination: str, start_date: str, end_date: str, activities: str, status: str}]
- Navigation mappings:
  - add-activity-button: POST to add activity
  - itinerary-list edit button: triggers editing
  - itinerary-list delete button: triggers deletion

### 5. accommodations.html
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page: Div - Main container
  - destination-input: Input (text) - Destination city input
  - check-in-date: Input (date) - Check-in date
  - check-out-date: Input (date) - Check-out date
  - price-filter: Dropdown - Filter by price range
  - hotels-list: Div - List of hotels with details
- Context Variables:
  - hotels: List[Dict{hotel_id: int, name: str, city: str, rating: float, price_per_night: float, amenities: str, category: str}]
- Navigation mappings:
  - hotels-list: displays hotel names and details (no links specified)

### 6. transportation.html
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page: Div - Main container
  - departure-city: Input (text) - Departure city
  - arrival-city: Input (text) - Arrival city
  - departure-date: Input (date) - Departure date
  - flight-class-filter: Dropdown - Flight class filter
  - available-flights: Div - List of flights
- Context Variables:
  - flights: List[Dict{flight_id: int, airline: str, departure_city: str, arrival_city: str, departure_time: str, arrival_time: str, price: float, class_type: str, duration: str}]
- Navigation mappings:
  - available-flights: display list with airlines, times, and booking link/buttons if any

### 7. packages.html
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page: Div - Main container
  - packages-grid: Div - Grid of package cards
  - duration-filter: Dropdown - Filter by trip duration
  - view-package-details-button-{{ pkg.package_id }}: Button - View package details
  - book-package-button-{{ pkg.package_id }}: Button - Book selected package
- Context Variables:
  - packages: List[Dict{package_id: int, package_name: str, destination: str, duration_days: int, price: float}]
- Navigation mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', package_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: triggers booking action

### 8. trips.html
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page: Div - Main container
  - trips-table: Table - Displays trips with columns for destination, dates, status
  - view-trip-details-button-{{ trip.trip_id }}: Button - View trip details
  - edit-trip-button-{{ trip.trip_id }}: Button - Edit trip
  - delete-trip-button-{{ trip.trip_id }}: Button - Delete trip
- Context Variables:
  - trips: List[Dict{trip_id: int, trip_name: str, destination: str, start_date: str, end_date: str, status: str}]
- Navigation mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: triggers edit action
  - delete-trip-button-{{ trip.trip_id }}: triggers delete action

### 9. booking_confirmation.html
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page: Div - Main container
  - confirmation-number: Div - Displays confirmation number
  - booking-details: Div - Detailed booking information
  - download-itinerary-button: Button - Download itinerary as PDF
  - share-trip-button: Button - Share trip details
  - back-to-dashboard: Button - Navigate back to dashboard
- Context Variables:
  - booking: Dict{booking_id: int, trip_id: int, booking_type: str, booking_date: str, amount: float, confirmation_number: str, status: str}
- Navigation mappings:
  - download-itinerary-button: triggers PDF download
  - share-trip-button: triggers sharing
  - back-to-dashboard: url_for('dashboard')

### 10. recommendations.html
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page: Div - Main container
  - trending-destinations: Div - Trending destinations ranked by popularity
  - recommendation-season-filter: Dropdown - Filter by season
  - budget-filter: Dropdown - Filter by budget
  - back-to-dashboard: Button - Navigate back to dashboard
- Context Variables:
  - recommendations: List[Dict]
  - trending_destinations: List[Dict]
  - filters: Dict{season: str, budget: str}
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. destinations.txt
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  1. dest_id (int)
  2. name (str)
  3. country (str)
  4. region (str)
  5. description (str)
  6. attractions (str)
  7. climate (str)
- Description: Stores destinations with details including attractions and climate.
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. itineraries.txt
- Path: data/itineraries.txt
- Fields:
  1. itinerary_id (int)
  2. itinerary_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. activities (str)
  7. status (str)
- Description: Stores itinerary details including dates and activities.
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. hotels.txt
- Path: data/hotels.txt
- Fields:
  1. hotel_id (int)
  2. name (str)
  3. city (str)
  4. rating (float)
  5. price_per_night (float)
  6. amenities (str)
  7. category (str)
- Description: Stores hotel listings with ratings, pricing, and amenities.
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. flights.txt
- Path: data/flights.txt
- Fields:
  1. flight_id (int)
  2. airline (str)
  3. departure_city (str)
  4. arrival_city (str)
  5. departure_time (str, HH:MM)
  6. arrival_time (str, HH:MM or with day indicator)
  7. price (float)
  8. class_type (str)
  9. duration (str)
- Description: Stores flight details including departure, arrival, price, and duration.
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. packages.txt
- Path: data/packages.txt
- Fields:
  1. package_id (int)
  2. package_name (str)
  3. destination (str)
  4. duration_days (int)
  5. price (float)
  6. included_items (str)
  7. difficulty_level (str)
- Description: Stores travel packages with inclusions and difficulty.
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. trips.txt
- Path: data/trips.txt
- Fields:
  1. trip_id (int)
  2. trip_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. total_budget (float)
  7. status (str)
  8. created_date (str, YYYY-MM-DD)
- Description: Stores user trips with budget and status.
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. bookings.txt
- Path: data/bookings.txt
- Fields:
  1. booking_id (int)
  2. trip_id (int)
  3. booking_type (str)
  4. booking_date (str, YYYY-MM-DD)
  5. amount (float)
  6. confirmation_number (str)
  7. status (str)
- Description: Stores booking information linked to trips.
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```
