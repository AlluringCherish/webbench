# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                     | HTTP Methods | Function Name             | Template Rendered          | Context Variables                                                                                                  | Navigation Actions Triggered                               |
|----------------------------------|--------------|--------------------------|----------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| / (Dashboard)                    | GET          | dashboard                | dashboard.html             | featured_destinations: list of dict {dest_id:int, name:str, country:str}
upcoming_trips: list of dict {trip_id:int, trip_name:str, start_date:str, end_date:str}                         | browse_destinations_button -> url_for('destinations')
plan_itinerary_button -> url_for('plan_itinerary')             |
| /destinations                   | GET, POST    | destinations             | destinations.html          | destinations: list of dict {dest_id:int, name:str, country:str, region:str}
selected_region: str (for filter)
search_query: str (for search input)                                         | view_destination_button_{{ dest_id }} -> url_for('destination_details', dest_id=dest.dest_id)                              |
| /destinations/<int:dest_id>    | GET, POST    | destination_details      | destination_details.html   | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}
add_success: bool (optional, after POST)                                                                | add_to_trip_button -> triggers destination add to trip action                                               |
| /itinerary                     | GET, POST    | plan_itinerary           | itinerary.html             | itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}                                  | add_activity_button -> add activity action
itinerary_list edit/delete buttons call respective route functions                                   |
| /accommodations                | GET, POST    | accommodations           | accommodations.html        | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
filters: dict {destination:str, check_in:str, check_out:str, price_filter:str}                     | hotels list includes no direct links, selection could be designed by frontend                                |
| /transportation                | GET, POST    | transportation           | transportation.html        | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
selected_filters: dict {departure_city:str, arrival_city:str, dep_date:str, flight_class:str}          | no direct navigation from flights list indicated                                                              |
| /packages                     | GET, POST    | travel_packages          | packages.html              | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}
package_filter: str (duration)                                                                 | view_package_details_button_{{ pkg_id }} -> url_for('package_details', pkg_id=package.package_id) 
book_package_button_{{ pkg_id }} -> url_for('book_package', pkg_id=package.package_id)        |
| /trips                       | GET, POST    | trips                   | trips.html                 | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}                                                             | view_trip_details_button_{{ trip_id }} -> url_for('trip_details', trip_id=trip.trip_id)
edit_trip_button_{{ trip_id }} -> url_for('edit_trip', trip_id=trip.trip_id)
delete_trip_button_{{ trip_id }} triggers deletion                 |
| /booking_confirmation        | GET          | booking_confirmation    | booking_confirmation.html  | booking: dict {confirmation_number:str, booking_details:str}                                                                                                         | download_itinerary_button triggers PDF download
share_trip_button triggers share action
back_to_dashboard -> url_for('dashboard')        |
| /recommendations             | GET          | travel_recommendations  | recommendations.html       | trending_destinations: list of dict {dest_id:int, name:str, popularity:int}
selected_season: str
selected_budget: str                                                | back_to_dashboard -> url_for('dashboard')                                                                          |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-destinations (Div): Displays featured travel destinations
  - upcoming-trips (Div): Displays upcoming planned trips
  - browse-destinations-button (Button): Navigate to destinations page
  - plan-itinerary-button (Button): Navigate to itinerary planning page
- Context Variables:
  - featured_destinations: list of dict {dest_id:int, name:str, country:str}
  - upcoming_trips: list of dict {trip_id:int, trip_name:str, start_date:str, end_date:str}
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('plan_itinerary')

### 2. Destinations Page
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Main container
  - search-destination (Input): Search field
  - region-filter (Dropdown): Filter by region (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid (Div): Grid displaying destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View destination details
- Context Variables:
  - destinations: list of dict {dest_id:int, name:str, country:str, region:str}
  - selected_region: str (current filter)
  - search_query: str (current search term)
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. Destination Details Page
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Main container
  - destination-name (H1): Displays destination name
  - destination-country (Div): Displays destination country
  - destination-description (Div): Displays detailed description
  - add-to-trip-button (Button): Add destination to trip
  - destination-attractions (Div): Displays main attractions
- Context Variables:
  - destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}
  - add_success: bool (optional, shows add confirmation)
- Navigation Mappings:
  - add-to-trip-button: triggers add to trip

### 4. Itinerary Planning Page
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Main container
  - itinerary-name-input (Input): Input for itinerary name
  - start-date-input (Input date): Input for start date
  - end-date-input (Input date): Input for end date
  - add-activity-button (Button): Adds activity
  - itinerary-list (Div): Lists itineraries with edit/delete
- Context Variables:
  - itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button: triggers adding activity
  - itinerary-list edit/delete buttons link to appropriate route functions

### 5. Accommodations Page
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container
  - destination-input (Input): Destination city input
  - check-in-date (Input date): Check-in date field
  - check-out-date (Input date): Check-out date field
  - price-filter (Dropdown): Price range filter (Budget, Mid-range, Luxury)
  - hotels-list (Div): List of hotels
- Context Variables:
  - hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
  - filters: dict {destination:str, check_in:str, check_out:str, price_filter:str}
- Navigation Mappings:
  - No direct navigation from hotel list specified

### 6. Transportation Page
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container
  - departure-city (Input): Departure city field
  - arrival-city (Input): Arrival city field
  - departure-date (Input date): Departure date
  - flight-class-filter (Dropdown): Flight class filter (Economy, Business, First Class)
  - available-flights (Div): List of available flights
- Context Variables:
  - flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
  - selected_filters: dict {departure_city:str, arrival_city:str, dep_date:str, flight_class:str}
- Navigation Mappings:
  - No direct navigation from flights list specified

### 7. Travel Packages Page
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of travel packages
  - duration-filter (Dropdown): Filter by duration (3-5 days, 7-10 days, 14+ days)
  - view-package-details-button-{{ pkg.package_id }} (Button): View package details
  - book-package-button-{{ pkg.package_id }} (Button): Book the package
- Context Variables:
  - packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}
  - package_filter: str (duration)
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', pkg_id=package.package_id)
  - book-package-button-{{ pkg.package_id }}: url_for('book_package', pkg_id=package.package_id)

### 8. Trip Management Page
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container
  - trips-table (Table): Table of trips
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }}: triggers delete action

### 9. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Displays confirmation number
  - booking-details (Div): Booking details
  - download-itinerary-button (Button): Download itinerary as PDF
  - share-trip-button (Button): Share trip details
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - booking: dict {confirmation_number:str, booking_details:str}
- Navigation Mappings:
  - download-itinerary-button: triggers PDF download
  - share-trip-button: triggers share
  - back-to-dashboard: url_for('dashboard')

### 10. Travel Recommendations Page
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container
  - trending-destinations (Div): Trending destinations display
  - recommendation-season-filter (Dropdown): Filter by travel season
  - budget-filter (Dropdown): Filter by budget range
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - trending_destinations: list of dict {dest_id:int, name:str, popularity:int}
  - selected_season: str
  - selected_budget: str
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  dest_id|name|country|region|description|attractions|climate
- Description: Contains travel destination metadata including id, location, description, and points of interest.
- Example:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, no header):
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Records details of travel itineraries with activities and statuses.
- Example:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, no header):
  hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Contains hotel listings with amenities and pricing.
- Example:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, no header):
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flight data including times, prices, and class.
- Example:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, no header):
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Pre-designed travel packages with details and pricing.
- Example:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, no header):
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: User created trips with budgets and statuses.
- Example:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Records booking transactions with confirmation and status.
- Example:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending

---

Design specification complete, enabling full independent backend and frontend development.