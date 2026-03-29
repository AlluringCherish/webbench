# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                   | HTTP Methods | Function Name                  | Template File                | Context Variables                                                                                     | Navigation Actions Triggered by Buttons/Links                                                |
|---------------------------------|--------------|-------------------------------|------------------------------|------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| /                               | GET          | dashboard                     | templates/dashboard.html      | featured_destinations: list of dict {dest_id:int, name:str, country:str}
upcoming_trips: list of dict {trip_id:int, trip_name:str, start_date:str, end_date:str}           | browse-destinations-button -> /destinations
plan-itinerary-button -> /itinerary                |
| /destinations                   | GET, POST    | destinations                  | templates/destinations.html   | destinations: list of dict {dest_id:int, name:str, country:str, region:str}
search_query: str (empty string on GET or last search string on POST)
region_filter: str (one of Asia, Europe, Americas, Africa, Oceania or empty)                    | view-destination-button-{{dest_id}} -> /destinations/<dest_id>                                |
| /destinations/<int:dest_id>    | GET, POST   | destination_details            | templates/destination_details.html | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str, climate:str}
add_status: str (optional message after adding to trip)                                      | add-to-trip-button -> POST to /destinations/<dest_id> (add to trip action, then rerender or redirect)
|
| /itinerary                     | GET, POST   | itinerary                     | templates/itinerary.html      | itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str (YYYY-MM-DD), end_date:str (YYYY-MM-DD), activities:str, status:str} | add-activity-button -> POST to /itinerary (add new activity)
|
| /accommodations                | GET, POST   | accommodations                | templates/accommodations.html | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
search_params: dict {destination:str, check_in_date:str, check_out_date:str, price_filter:str}       | (No explicit buttons specified for navigation beyond this page)
|
| /transportation               | GET, POST   | transportation                | templates/transportation.html | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
search_params: dict {departure_city:str, arrival_city:str, departure_date:str, flight_class_filter:str} | (No explicit buttons specified for navigation beyond this page)
|
| /packages                    | GET        | packages                     | templates/packages.html       | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}
filter_duration: str (3-5 days, 7-10 days, 14+ days, or empty)                             | view-package-details-button-{{pkg_id}} -> /packages/<pkg_id>
book-package-button-{{pkg_id}} -> POST /packages/<pkg_id>/book                               |
| /packages/<int:pkg_id>        | GET        | package_details              | templates/package_details.html| package: dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}             | book-package-button -> POST to /packages/<pkg_id>/book                                     |
| /trips                      | GET        | trips                        | templates/trips.html          | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str, total_budget:float}                      | view-trip-details-button-{{trip_id}} -> /trips/<trip_id>
edit-trip-button-{{trip_id}} -> /trips/<trip_id>/edit
delete-trip-button-{{trip_id}} -> POST /trips/<trip_id>/delete                    |
| /trips/<int:trip_id>          | GET        | trip_details                 | templates/trip_details.html   | trip: dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str}
bookings: list of dict {booking_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str} | (No explicit navigation specified)                                                        |
| /booking-confirmation/<int:booking_id> | GET     | booking_confirmation          | templates/booking_confirmation.html | booking: dict {booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str}
trip: dict (summary info)
| back-to-dashboard -> /                                                          |
| /recommendations               | GET        | recommendations              | templates/recommendations.html| trending_destinations: list of dict {dest_id:int, name:str, country:str, popularity_rank:int}
season_filter: str (Spring, Summer, Fall, Winter, or empty)
budget_filter: str (Low, Medium, High, or empty)                                  | back-to-dashboard -> /                                                              |

---

## Section 2: HTML Templates Specification

### templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-destinations (Div): Display of featured travel destinations
  - upcoming-trips (Div): Display of upcoming planned trips
  - browse-destinations-button (Button): Navigate to /destinations
  - plan-itinerary-button (Button): Navigate to /itinerary
- Context Variables:
  - featured_destinations: list of dict {dest_id:int, name:str, country:str}
  - upcoming_trips: list of dict {trip_id:int, trip_name:str, start_date:str, end_date:str}
- Navigation Mappings:
  - browse-destinations-button -> url_for('destinations')
  - plan-itinerary-button -> url_for('itinerary')

---

### templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Container for the destinations page
  - search-destination (Input): Field to search destinations by name or country
  - region-filter (Dropdown): Filter by region (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid (Div): Grid displaying destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View destination details
- Context Variables:
  - destinations: list of dict {dest_id:int, name:str, country:str, region:str}
  - search_query: str
  - region_filter: str
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }} -> url_for('destination_details', dest_id=dest.dest_id)

---

### templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container for the destination details page
  - destination-name (H1): Display destination name
  - destination-country (Div): Display destination country
  - destination-description (Div): Display detailed description
  - add-to-trip-button (Button): Add destination to trip
  - destination-attractions (Div): Display main attractions and activities
- Context Variables:
  - destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str, climate:str}
  - add_status: str (optional success or error message)
- Navigation Mappings:
  - add-to-trip-button -> POST to url_for('destination_details', dest_id=destination.dest_id)

---

### templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Container for the itinerary page
  - itinerary-name-input (Input): Enter itinerary name
  - start-date-input (Input date): Select trip start date
  - end-date-input (Input date): Select trip end date
  - add-activity-button (Button): Add activity to itinerary
  - itinerary-list (Div): List of created itineraries with edit/delete options
- Context Variables:
  - itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button -> POST to url_for('itinerary')

---

### templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container for accommodations page
  - destination-input (Input): Destination city input
  - check-in-date (Input date): Check-in date
  - check-out-date (Input date): Check-out date
  - price-filter (Dropdown): Filter hotels by price range (Budget, Mid-range, Luxury)
  - hotels-list (Div): List of hotels with details
- Context Variables:
  - hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
  - search_params: dict {destination:str, check_in_date:str, check_out_date:str, price_filter:str}
- Navigation Mappings:
  - No explicit navigation beyond this page specified

---

### templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container for transportation page
  - departure-city (Input): Departure city
  - arrival-city (Input): Arrival city
  - departure-date (Input date): Departure date
  - flight-class-filter (Dropdown): Filter by flight class (Economy, Business, First Class)
  - available-flights (Div): List of flights
- Context Variables:
  - flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
  - search_params: dict {departure_city:str, arrival_city:str, departure_date:str, flight_class_filter:str}
- Navigation Mappings:
  - No explicit navigation beyond this page specified

---

### templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container for packages page
  - packages-grid (Div): Grid displaying package cards
  - duration-filter (Dropdown): Filter packages by duration (3-5 days, 7-10 days, 14+ days)
  - view-package-details-button-{{ pkg.package_id }} (Button): View package details
  - book-package-button-{{ pkg.package_id }} (Button): Book selected package
- Context Variables:
  - packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}
  - filter_duration: str
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }} -> url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }} -> POST to url_for('package_book', pkg_id=pkg.package_id)

---

### templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container for trips page
  - trips-table (Table): Displays all trips
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str, total_budget:float}
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }} -> url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }} -> url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }} -> POST to url_for('delete_trip', trip_id=trip.trip_id)

---

### templates/trip_details.html
- Page Title: Trip Details
- Element IDs:
  - trip-details-page (Div): Container for trip details page
  - trip-name (H1): Display trip name
  - trip-destination (Div): Display destination
  - trip-dates (Div): Display start and end dates
  - total-budget (Div): Display total budget
  - status (Div): Display trip status
  - bookings-list (Div): List of bookings
- Context Variables:
  - trip: dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str}
  - bookings: list of dict {booking_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str}
- Navigation Mappings:
  - None explicitly defined

---

### templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container for confirmation page
  - confirmation-number (Div): Display booking confirmation number
  - booking-details (Div): Display booking details
  - download-itinerary-button (Button): Download trip itinerary PDF
  - share-trip-button (Button): Share trip details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - booking: dict {booking_id:int, trip_id:int, booking_type:str, booking_date:str, amount:float, confirmation_number:str, status:str}
  - trip: dict with summary trip info
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

---

### templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container for recommendations page
  - trending-destinations (Div): Trending destinations ranked by popularity
  - recommendation-season-filter (Dropdown): Filter by travel season (Spring, Summer, Fall, Winter)
  - budget-filter (Dropdown): Filter by budget range (Low, Medium, High)
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_destinations: list of dict {dest_id:int, name:str, country:str, popularity_rank:int}
  - season_filter: str
  - budget_filter: str
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  1. dest_id (int)
  2. name (str)
  3. country (str)
  4. region (str) - One of Asia, Europe, Americas, Africa, Oceania
  5. description (str)
  6. attractions (str, comma-separated)
  7. climate (str)
- Description: Stores travel destination details including key info and attractions.
- Example Rows:
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
  4. start_date (str, format YYYY-MM-DD)
  5. end_date (str, format YYYY-MM-DD)
  6. activities (str, comma-separated)
  7. status (str)
- Description: Stores user itineraries with trip details and activities.
- Example Rows:
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
  6. amenities (str, comma-separated)
  7. category (str) - Budget, Mid-range, Luxury
- Description: Stores hotel details for accommodation searches.
- Example Rows:
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
  5. departure_time (str, format HH:MM or HH:MM with next day indicator)
  6. arrival_time (str, format HH:MM or HH:MM with next day indicator)
  7. price (float)
  8. class_type (str) - Economy, Business, First Class
  9. duration (str) - e.g., "7 hours 30 minutes"
- Description: Stores flight information for booking.
- Example Rows:
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
  6. included_items (str, comma-separated)
  7. difficulty_level (str)
- Description: Stores pre-designed travel packages.
- Example Rows:
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
  4. start_date (str, format YYYY-MM-DD)
  5. end_date (str, format YYYY-MM-DD)
  6. total_budget (float)
  7. status (str)
  8. created_date (str, format YYYY-MM-DD)
- Description: Stores all created trips with status and budget.
- Example Rows:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

---

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  1. booking_id (int)
  2. trip_id (int)
  3. booking_type (str)
  4. booking_date (str, format YYYY-MM-DD)
  5. amount (float)
  6. confirmation_number (str)
  7. status (str)
- Description: Stores booking information linked to trips.
- Example Rows:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending

