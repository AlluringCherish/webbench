# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                    | HTTP Methods | Function Name                | Template File                | Context Variables                                                                                                     | Navigation Actions Triggered by Buttons/Links                                   |
|---------------------------------|--------------|-----------------------------|------------------------------|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| / (Dashboard)                   | GET          | dashboard                   | templates/dashboard.html      | featured_destinations: list of dict {dest_id:int, name:str, country:str} (e.g. featured destinations)
upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str} | browse_destinations_button -> url_for('destinations')
plan_itinerary_button -> url_for('itinerary')
|
| /destinations                  | GET, POST   | destinations                | templates/destinations.html   | destinations: list of dict {dest_id:int, name:str, country:str, region:str}                                           | view_destination_button_-_{{ dest_id }} -> url_for('destination_details', dest_id=dest_id) |
|                                 |              |                             |                              | search_query:str (POST search input)
region_filter:str (POST filter dropdown)                                                                |                                                                                 |
| /destinations/&lt;int:dest_id&gt; | GET          | destination_details         | templates/destination_details.html | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}                                | add_to_trip_button -> url_for('itinerary')                                      |
| /itinerary                    | GET, POST   | itinerary                  | templates/itinerary.html      | itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str} | add_activity_button -> adds activities client-side or POST
|
| /accommodations              | GET, POST   | accommodations             | templates/accommodations.html | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str} |                                                                                 |
|                                 |              |                             |                              | destination_query:str (POST input)
check_in_date:str (POST date)
check_out_date:str (POST date)
price_filter:str (POST dropdown)                                                                 |                                                                                 |
| /transportation              | GET, POST   | transportation             | templates/transportation.html | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str} |                                                                                 |
|                                 |              |                             |                              | departure_city:str (POST input)
arrival_city:str (POST input)
departure_date:str (POST date)
flight_class_filter:str (POST dropdown)                                                                 |                                                                                 |
| /packages                   | GET          | packages                   | templates/packages.html       | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}               | view_package_details_button_-_{{ pkg_id }} -> url_for('package_details', pkg_id=pkg_id)
book_package_button_-_{{ pkg_id }} -> url_for('booking_confirmation', pkg_id=pkg_id) |
| /trips                     | GET, POST   | trips                      | templates/trips.html          | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str} | view_trip_details_button_-_{{ trip_id }} -> url_for('trip_details', trip_id=trip_id)
edit_trip_button_-_{{ trip_id }} -> url_for('edit_trip', trip_id=trip_id)
delete_trip_button_-_{{ trip_id }} -> POST deletion |
| /booking-confirmation       | GET          | booking_confirmation       | templates/booking_confirmation.html | booking: dict {confirmation_number:str, booking_details:str}                                                           | back_to_dashboard -> url_for('dashboard')                                     |
| /recommendations            | GET, POST   | recommendations            | templates/recommendations.html | recommendations: list of dict {name:str, popularity_rank:int}
filters: dict{season:str, budget:str} (POST filters)       | back_to_dashboard -> url_for('dashboard')                                     |

Note: Additional detail routes like /packages/&lt;int:pkg_id&gt;, /trips/&lt;int:trip_id&gt; and editing routes like /edit-trip/&lt;int:trip_id&gt; are implied but not detailed here.

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page: Div, main container
  - featured-destinations: Div, displays featured destinations list
  - upcoming-trips: Div, lists upcoming trips
  - browse-destinations-button: Button, navigates to destinations page
  - plan-itinerary-button: Button, navigates to itinerary page
- Context Variables:
  - featured_destinations: list of dict with fields: dest_id (int), name (str), country (str)
  - upcoming_trips: list of dict with fields: trip_id (int), trip_name (str), destination (str), start_date (str yyyy-mm-dd), end_date (str yyyy-mm-dd), status (str)
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page: Div, main container
  - search-destination: Input, text input for search
  - region-filter: Dropdown, filter destinations by region
  - destinations-grid: Div, container displaying destination cards
  - view-destination-button-{{ dest.dest_id }}: Button (dynamic), view details for each destination
- Context Variables:
  - destinations: list of dict with fields: dest_id (int), name (str), country (str), region (str)
  - search_query: str (optional, submitted search term)
  - region_filter: str (optional, selected filter)
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page: Div, main container
  - destination-name: H1, displays destination name
  - destination-country: Div, displays country
  - destination-description: Div, displays description
  - add-to-trip-button: Button, adds this destination to itinerary
  - destination-attractions: Div, lists attractions
- Context Variables:
  - destination: dict with fields: dest_id (int), name (str), country (str), description (str), attractions (str)
- Navigation Mappings:
  - add-to-trip-button: url_for('itinerary')

### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page: Div, main container
  - itinerary-name-input: Input, text for itinerary name
  - start-date-input: Input (date), trip start date
  - end-date-input: Input (date), trip end date
  - add-activity-button: Button, adds an activity
  - itinerary-list: Div, lists created itineraries with edit/delete options
- Context Variables:
  - itineraries: list of dict with fields: itinerary_id (int), itinerary_name (str), destination (str), start_date (str yyyy-mm-dd), end_date (str yyyy-mm-dd), activities (str), status (str)
- Navigation Mappings:
  - add-activity-button: triggers POST or client-side addition

### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page: Div, main container
  - destination-input: Input, destination city input
  - check-in-date: Input (date), check-in
  - check-out-date: Input (date), check-out
  - price-filter: Dropdown, price range filter
  - hotels-list: Div, lists available hotels
- Context Variables:
  - hotels: list of dict with fields: hotel_id (int), name (str), city (str), rating (float), price_per_night (float), amenities (str), category (str)
  - destination_query: str (optional, search input)
  - check_in_date: str (optional, yyyy-mm-dd)
  - check_out_date: str (optional, yyyy-mm-dd)
  - price_filter: str (optional, value from dropdown)

### 6. templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page: Div, main container
  - departure-city: Input, departure city
  - arrival-city: Input, arrival city
  - departure-date: Input (date), departure date
  - flight-class-filter: Dropdown, flight class filter
  - available-flights: Div, lists flights
- Context Variables:
  - flights: list of dict with fields: flight_id (int), airline (str), departure_city (str), arrival_city (str), departure_time (str), arrival_time (str), price (float), class_type (str), duration (str)
  - departure_city: str (optional)
  - arrival_city: str (optional)
  - departure_date: str (optional, yyyy-mm-dd)
  - flight_class_filter: str (optional)

### 7. templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page: Div, main container
  - packages-grid: Div, displays package cards
  - duration-filter: Dropdown, filter by duration
  - view-package-details-button-{{ pkg.package_id }}: Button (dynamic), view details
  - book-package-button-{{ pkg.package_id }}: Button (dynamic), book package
- Context Variables:
  - packages: list of dict with fields: package_id (int), package_name (str), destination (str), duration_days (int), price (float)
  - duration_filter: str (optional)
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: url_for('booking_confirmation', pkg_id=pkg.package_id)

### 8. templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page: Div, main container
  - trips-table: Table, trip listings
  - view-trip-details-button-{{ trip.trip_id }}: Button (dynamic), view trip details
  - edit-trip-button-{{ trip.trip_id }}: Button (dynamic), edit trip
  - delete-trip-button-{{ trip.trip_id }}: Button (dynamic), delete trip
- Context Variables:
  - trips: list of dict with fields: trip_id (int), trip_name (str), destination (str), start_date (str), end_date (str), total_budget (float), status (str), created_date (str)
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)

### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page: Div, main container
  - confirmation-number: Div, shows booking confirmation number
  - booking-details: Div, shows booking details
  - download-itinerary-button: Button, download itinerary as PDF
  - share-trip-button: Button, share trip
  - back-to-dashboard: Button, navigates to dashboard
- Context Variables:
  - booking: dict with fields: confirmation_number (str), booking_details (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page: Div, main container
  - trending-destinations: Div, shows trending destinations by popularity
  - recommendation-season-filter: Dropdown, filter by travel season
  - budget-filter: Dropdown, filter by budget
  - back-to-dashboard: Button, navigates to dashboard
- Context Variables:
  - recommendations: list of dict with fields: name (str), popularity_rank (int)
  - filters: dict with fields: season (str), budget (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- Field order: dest_id|name|country|region|description|attractions|climate
- Description: Stores detailed destination information
- Example rows:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
- No header row

### 2. data/itineraries.txt
- Field order: itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Stores user itineraries with activity lists and status
- Example rows:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
- No header row

### 3. data/hotels.txt
- Field order: hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Stores hotel information for accommodation search
- Example rows:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
- No header row

### 4. data/flights.txt
- Field order: flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flight details for booking
- Example rows:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
- No header row

### 5. data/packages.txt
- Field order: package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Stores travel package information
- Example rows:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
- No header row

### 6. data/trips.txt
- Field order: trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: Stores user trips with budget and status
- Example rows:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
- No header row

### 7. data/bookings.txt
- Field order: booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Stores booking information linked to trips
- Example rows:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
- No header row

---

End of TravelPlanner Design Specification.
