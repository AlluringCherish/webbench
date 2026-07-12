# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                  | HTTP Methods | Function Name            | Template File                 | Context Variables                                              | Navigation Actions (from buttons/links)                                |
|--------------------------------|--------------|--------------------------|-------------------------------|---------------------------------------------------------------|------------------------------------------------------------------------|
| /dashboard                     | GET          | dashboard                | dashboard.html                | featured_destinations: List[dict{dest_id:int, name:str, country:str}], upcoming_trips: List[dict{trip_id:int, trip_name:str, start_date:str, end_date:str}] | browse-destinations-button -> /destinations; plan-itinerary-button -> /itinerary |
| /destinations                 | GET          | destinations             | destinations.html             | destinations: List[dict{dest_id:int, name:str, country:str, region:str}] | view-destination-button-{{dest_id}} -> /destinations/<int:dest_id>      |
| /destinations/<int:dest_id>   | GET, POST    | destination_details      | destination_details.html      | destination: dict{dest_id:int, name:str, country:str, description:str, attractions:str, climate:str} | add-to-trip-button -> POST adds destination to trip                      |
| /itinerary                   | GET, POST    | itinerary                | itinerary.html                | itineraries: List[dict{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}] | add-activity-button adds activity to itinerary list                     |
| /accommodations              | GET          | accommodations           | accommodations.html           | hotels: List[dict{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}] | No direct navigation buttons specified                                 |
| /transportation              | GET          | transportation           | transportation.html           | flights: List[dict{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}] | No direct navigation buttons specified                                 |
| /packages                    | GET          | packages                 | packages.html                 | packages: List[dict{package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}] | view-package-details-button-{{pkg_id}} -> /packages/<int:package_id>, book-package-button-{{pkg_id}} triggers booking |
| /packages/<int:package_id>   | GET          | package_details          | package_details.html          | package: dict{package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str} | book-package-button triggers booking                                   |
| /trips                      | GET          | trips                    | trips.html                   | trips: List[dict{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}] | view-trip-details-button-{{trip_id}} -> /trips/<int:trip_id>, edit-trip-button-{{trip_id}} -> edit trip, delete-trip-button-{{trip_id}} deletes trip |
| /trips/<int:trip_id>         | GET, POST    | trip_details             | trip_details.html             | trip: dict{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str} | POST for edits/deletes                                                 |
| /booking-confirmation        | GET          | booking_confirmation     | booking_confirmation.html     | booking: dict{booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str} | download-itinerary-button downloads PDF, share-trip-button shares trip, back-to-dashboard -> /dashboard |
| /recommendations             | GET          | recommendations          | recommendations.html          | trending_destinations: List[dict{dest_id:int, name:str, country:str, popularity:int}], filters: dict{season:str, budget:str} | back-to-dashboard -> /dashboard                                          |


---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-destinations (Div): Display of featured travel destinations
  - upcoming-trips (Div): Display of upcoming planned trips
  - browse-destinations-button (Button): Navigates to /destinations
  - plan-itinerary-button (Button): Navigates to /itinerary
- Context Variables:
  - featured_destinations: List[dict{dest_id:int, name:str, country:str}]
  - upcoming_trips: List[dict{trip_id:int, trip_name:str, start_date:str, end_date:str}]
- Navigation:
  - browse-destinations-button -> url_for('destinations')
  - plan-itinerary-button -> url_for('itinerary')

### 2. Destinations Page
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Container for the destinations page
  - search-destination (Input): Search field for destination name or country
  - region-filter (Dropdown): Filter destinations by region
  - destinations-grid (Div): Grid showing destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View details for each destination card
- Context Variables:
  - destinations: List[dict{dest_id:int, name:str, country:str, region:str}]
- Navigation:
  - view-destination-button-{{ dest.dest_id }} -> url_for('destination_details', dest_id=dest.dest_id)

### 3. Destination Details Page
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container for details page
  - destination-name (H1): Shows destination name
  - destination-country (Div): Shows destination country
  - destination-description (Div): Shows destination description
  - add-to-trip-button (Button): Adds destination to trip
  - destination-attractions (Div): Shows attractions and activities
- Context Variables:
  - destination: dict{dest_id:int, name:str, country:str, description:str, attractions:str, climate:str}
- Navigation:
  - add-to-trip-button triggers POST to add destination to trip

### 4. Itinerary Planning Page
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Container for itinerary planning
  - itinerary-name-input (Input): Enter itinerary name
  - start-date-input (Input date): Select start date
  - end-date-input (Input date): Select end date
  - add-activity-button (Button): Add an activity
  - itinerary-list (Div): Shows list of itineraries with edit/delete
- Context Variables:
  - itineraries: List[dict{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}]
- Navigation:
  - add-activity-button adds activity (handled in frontend logic)

### 5. Accommodations Page
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container for accommodations
  - destination-input (Input): Enter hotel destination city
  - check-in-date (Input date): Select check-in date
  - check-out-date (Input date): Select check-out date
  - price-filter (Dropdown): Filter hotels by price range
  - hotels-list (Div): Lists hotels with name, rating, price, amenities
- Context Variables:
  - hotels: List[dict{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}]
- Navigation: none specified

### 6. Transportation Page
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container for transportation
  - departure-city (Input): Input departure city
  - arrival-city (Input): Input arrival city
  - departure-date (Input date): Select departure date
  - flight-class-filter (Dropdown): Filter flights by class
  - available-flights (Div): List available flights with airline, times, price
- Context Variables:
  - flights: List[dict{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}]
- Navigation: none specified

### 7. Travel Packages Page
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container for packages
  - packages-grid (Div): Grid with package cards
  - duration-filter (Dropdown): Filter packages by duration
  - view-package-details-button-{{ pkg.package_id }} (Button): View details
  - book-package-button-{{ pkg.package_id }} (Button): Book package
- Context Variables:
  - packages: List[dict{package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}]
- Navigation:
  - view-package-details-button-{{ pkg.package_id }} -> url_for('package_details', package_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }} triggers booking

### 8. Trip Management Page
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container for trips
  - trips-table (Table): Table listing all trips
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: List[dict{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}]
- Navigation:
  - view-trip-details-button-{{ trip.trip_id }} -> url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }} triggers edit
  - delete-trip-button-{{ trip.trip_id }} triggers delete

### 9. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container for confirmation page
  - confirmation-number (Div): Shows booking confirmation number
  - booking-details (Div): Shows booking details
  - download-itinerary-button (Button): Downloads itinerary PDF
  - share-trip-button (Button): Shares trip details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - booking: dict{booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str}
- Navigation:
  - download-itinerary-button triggers PDF download
  - share-trip-button triggers sharing
  - back-to-dashboard -> url_for('dashboard')

### 10. Travel Recommendations Page
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container for recommendations
  - trending-destinations (Div): Displays trending destinations by popularity
  - recommendation-season-filter (Dropdown): Filter by season
  - budget-filter (Dropdown): Filter by budget
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_destinations: List[dict{dest_id:int, name:str, country:str, popularity:int}]
  - filters: dict{season:str, budget:str}
- Navigation:
  - back-to-dashboard -> url_for('dashboard')


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
  6. attractions (str)
  7. climate (str)
- Description: Stores all available travel destinations with details.
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, no header):
  1. itinerary_id (int)
  2. itinerary_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. activities (str)
  7. status (str)
- Description: Stores user created itineraries with activities and statuses.
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, no header):
  1. hotel_id (int)
  2. name (str)
  3. city (str)
  4. rating (float)
  5. price_per_night (float)
  6. amenities (str)
  7. category (str)
- Description: Stores hotel information for accommodations.
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, no header):
  1. flight_id (int)
  2. airline (str)
  3. departure_city (str)
  4. arrival_city (str)
  5. departure_time (str)
  6. arrival_time (str)
  7. price (float)
  8. class_type (str)
  9. duration (str)
- Description: Stores flight options available for booking.
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, no header):
  1. package_id (int)
  2. package_name (str)
  3. destination (str)
  4. duration_days (int)
  5. price (float)
  6. included_items (str)
  7. difficulty_level (str)
- Description: Stores pre-designed travel packages.
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, no header):
  1. trip_id (int)
  2. trip_name (str)
  3. destination (str)
  4. start_date (str, YYYY-MM-DD)
  5. end_date (str, YYYY-MM-DD)
  6. total_budget (float)
  7. status (str)
  8. created_date (str, YYYY-MM-DD)
- Description: Stores user trips with status and budget.
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  1. booking_id (int)
  2. trip_id (int)
  3. booking_type (str)
  4. booking_date (str, YYYY-MM-DD)
  5. amount (float)
  6. confirmation_number (str)
  7. status (str)
- Description: Stores booking transactions and their confirmation.
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

---

End of design_spec.md
