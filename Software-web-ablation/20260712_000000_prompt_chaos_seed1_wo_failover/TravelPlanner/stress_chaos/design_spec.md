# TravelPlanner Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint               | HTTP Methods | Function Name          | Template File              | Context Variables                                                                                                                   | Navigation Actions                                                                                                  |
|-----------------------------|--------------|------------------------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| /                           | GET          | dashboard              | dashboard.html             | featured_destinations: List[Dict] with keys (dest_id:int, name:str, country:str)
  upcoming_trips: List[Dict] with keys (trip_id:int, trip_name:str, start_date:str, end_date:str) | browse-destinations-button: url_for('destinations')
plan-itinerary-button: url_for('itinerary')               |
| /destinations               | GET          | destinations           | destinations.html          | destinations: List[Dict] with keys (dest_id:int, name:str, country:str, region:str)
region_options: List[str] (Asia, Europe, Americas, Africa, Oceania)                     | view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)                  |
| /destinations/<int:dest_id> | GET, POST    | destination_details    | destination_details.html   | destination: Dict with keys (dest_id:int, name:str, country:str, description:str, attractions:str, climate:str)                   | add-to-trip-button: POST to url_for('add_destination_to_trip', dest_id=destination.dest_id)                         |
| /itinerary                  | GET, POST    | itinerary              | itinerary.html             | itineraries: List[Dict] with keys (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str) | add-activity-button: POST to url_for('add_itinerary_activity')                                                      |
| /accommodations             | GET, POST    | accommodations         | accommodations.html        | hotels: List[Dict] with keys (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str)  | None specified                                                                                                       |
| /transportation             | GET, POST    | transportation         | transportation.html        | flights: List[Dict] with keys (flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str) | None specified                                                                                                       |
| /packages                  | GET          | packages               | packages.html              | packages: List[Dict] with keys (package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str) | view-package-details-button-{{ pkg.package_id }}: url_for('package_details', package_id=pkg.package_id) [if implemented]
book-package-button-{{ pkg.package_id }}: url_for('book_package', package_id=pkg.package_id) [if implemented] |
| /trips                     | GET          | trips                  | trips.html                 | trips: List[Dict] with keys (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str) | view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id) [if implemented]
edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id) [if implemented]
delete-trip-button-{{ trip.trip_id }}: url_for('delete_trip', trip_id=trip.trip_id) [if implemented] |
| /booking-confirmation/<int:trip_id> | GET          | booking_confirmation    | booking_confirmation.html  | booking: Dict with keys (booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str) | download-itinerary-button: triggers file download (route not specified)
share-trip-button: triggers share action (implementation detail not specified)
back-to-dashboard: url_for('dashboard') |
| /recommendations           | GET          | recommendations        | recommendations.html       | trending_destinations: List[Dict] with keys (dest_id:int, name:str, country:str, popularity_rank:int)
recommendation_seasons: List[str] (Spring, Summer, Fall, Winter)
budget_ranges: List[str] (Low, Medium, High)                           | back-to-dashboard: url_for('dashboard')                                                                           |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - featured-destinations (Div): Displays featured destinations
  - upcoming-trips (Div): Displays upcoming trips
  - browse-destinations-button (Button): Navigates to /destinations
  - plan-itinerary-button (Button): Navigates to /itinerary
- Context Variables:
  - featured_destinations: List[Dict] (dest_id:int, name:str, country:str)
  - upcoming_trips: List[Dict] (trip_id:int, trip_name:str, start_date:str, end_date:str)
- Navigation:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. destinations.html
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Container
  - search-destination (Input): Search field for name or country
  - region-filter (Dropdown): Filter by region (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid (Div): Grid of destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View destination details
- Context Variables:
  - destinations: List[Dict] (dest_id:int, name:str, country:str, region:str)
  - region_options: List[str]
- Navigation:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. destination_details.html
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container
  - destination-name (H1): Destination name
  - destination-country (Div): Country
  - destination-description (Div): Description
  - add-to-trip-button (Button): Adds destination to trip
  - destination-attractions (Div): Attractions
- Context Variables:
  - destination: Dict (dest_id:int, name:str, country:str, description:str, attractions:str, climate:str)
- Navigation:
  - add-to-trip-button: POST to url_for('add_destination_to_trip', dest_id=destination.dest_id)

### 4. itinerary.html
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Container
  - itinerary-name-input (Input): Itinerary name
  - start-date-input (Input date): Start date
  - end-date-input (Input date): End date
  - add-activity-button (Button): Add activity
  - itinerary-list (Div): List of itineraries with edit/delete
- Context Variables:
  - itineraries: List[Dict] (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str)
- Navigation:
  - add-activity-button: POST to url_for('add_itinerary_activity')

### 5. accommodations.html
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container
  - destination-input (Input): Destination city input
  - check-in-date (Input date): Check-in date
  - check-out-date (Input date): Check-out date
  - price-filter (Dropdown): Budget, Mid-range, Luxury
  - hotels-list (Div): List of hotels
- Context Variables:
  - hotels: List[Dict] (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str)
- Navigation: None

### 6. transportation.html
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container
  - departure-city (Input): Departure city
  - arrival-city (Input): Arrival city
  - departure-date (Input date): Departure date
  - flight-class-filter (Dropdown): Economy, Business, First Class
  - available-flights (Div): List of flights
- Context Variables:
  - flights: List[Dict] (flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str)
- Navigation: None

### 7. packages.html
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of packages
  - duration-filter (Dropdown): 3-5 days, 7-10 days, 14+ days
  - view-package-details-button-{{ pkg.package_id }} (Button): View details
  - book-package-button-{{ pkg.package_id }} (Button): Book package
- Context Variables:
  - packages: List[Dict] (package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str)
- Navigation:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', package_id=pkg.package_id) [if implemented]
  - book-package-button-{{ pkg.package_id }}: url_for('book_package', package_id=pkg.package_id) [if implemented]

### 8. trips.html
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container
  - trips-table (Table): Trips list
  - view-trip-details-button-{{ trip.trip_id }} (Button): View details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: List[Dict] (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str)
- Navigation:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id) [if implemented]
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id) [if implemented]
  - delete-trip-button-{{ trip.trip_id }}: url_for('delete_trip', trip_id=trip.trip_id) [if implemented]

### 9. booking_confirmation.html
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Confirmation number
  - booking-details (Div): Booking details
  - download-itinerary-button (Button): Download itinerary PDF
  - share-trip-button (Button): Share trip
  - back-to-dashboard (Button): Navigate to dashboard
- Context Variables:
  - booking: Dict (booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### 10. recommendations.html
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container
  - trending-destinations (Div): Trending destinations listing
  - recommendation-season-filter (Dropdown): Spring, Summer, Fall, Winter
  - budget-filter (Dropdown): Low, Medium, High
  - back-to-dashboard (Button): Navigate to dashboard
- Context Variables:
  - trending_destinations: List[Dict] (dest_id:int, name:str, country:str, popularity_rank:int)
  - recommendation_seasons: List[str]
  - budget_ranges: List[str]
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, order): dest_id | name | country | region | description | attractions | climate
- Description: Stores travel destinations data including descriptions and attractions.
- Example rows:
```
1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
```

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, order): itinerary_id | itinerary_name | destination | start_date | end_date | activities | status
- Description: Stores user itineraries with activities and status.
- Example rows:
```
1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
```

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, order): hotel_id | name | city | rating | price_per_night | amenities | category
- Description: Stores hotel information including ratings and amenities.
- Example rows:
```
1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
```

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, order): flight_id | airline | departure_city | arrival_city | departure_time | arrival_time | price | class_type | duration
- Description: Stores flight details including schedules and pricing.
- Example rows:
```
1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
```

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, order): package_id | package_name | destination | duration_days | price | included_items | difficulty_level
- Description: Stores predefined travel packages data.
- Example rows:
```
1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
```

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, order): trip_id | trip_name | destination | start_date | end_date | total_budget | status | created_date
- Description: Stores user trip summaries with budget and status.
- Example rows:
```
1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
```

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, order): booking_id | trip_id | booking_type | booking_date | amount | confirmation_number | status
- Description: Stores booking records including confirmation numbers.
- Example rows:
```
1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
3|3|Package|2025-01-12|1800.00|CONF003|Pending
```

---

This design specification provides complete and unambiguous definitions for all routes, templates, element IDs, context variables, navigation mappings, and data file schemas required for the TravelPlanner application. Backend and frontend teams can independently implement their components based on this document without mutual dependencies.