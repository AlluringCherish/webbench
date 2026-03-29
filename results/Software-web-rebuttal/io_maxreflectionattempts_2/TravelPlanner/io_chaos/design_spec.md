# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                | HTTP Methods | Function Name           | Template File           | Context Variables (Type/Structure)                                                                                          | Navigation Actions from Buttons/Links                                                                                                   |
|------------------------------|--------------|------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| /dashboard                   | GET          | dashboard              | dashboard.html          | featured_destinations: List[Dict] (dest_id:int, name:str, country:str)
upcoming_trips: List[Dict] (trip_id:int, trip_name:str, start_date:str) | browse-destinations-button: navigates to /destinations
plan-itinerary-button: navigates to /itinerary                            |
| /destinations               | GET          | destinations           | destinations.html       | destinations: List[Dict] (dest_id:int, name:str, country:str, region:str)                                                     | view-destination-button-{{ dest.dest_id }}: navigates to /destinations/<int:dest_id>                                                    |
| /destinations/<int:dest_id> | GET          | destination_details    | destination_details.html| destination: Dict (dest_id:int, name:str, country:str, description:str, attractions:str)                                        | add-to-trip-button: triggers add destination to trip logic (POST in actual app, but here navigation not specified)                    |
| /itinerary                  | GET, POST    | itinerary              | itinerary.html          | itineraries: List[Dict] (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str) | add-activity-button: triggers addition of activity (POST likely)                                                                       |
| /accommodations             | GET          | accommodations         | accommodations.html     | hotels: List[Dict] (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str)                      |                                                                                                                                        |
| /transportation             | GET          | transportation         | transportation.html     | flights: List[Dict] (flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str) |                                                                                                                                        |
| /packages                   | GET          | travel_packages        | packages.html           | packages: List[Dict] (package_id:int, package_name:str, destination:str, duration_days:int, price:float)                       | view-package-details-button-{{ pkg.package_id }}: navigates to /packages/<int:package_id>
book-package-button-{{ pkg.package_id }}: booking action (POST likely) |
| /trips                     | GET          | trips                  | trips.html              | trips: List[Dict] (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str)                     | view-trip-details-button-{{ trip.trip_id }}: /trips/<int:trip_id>
edit-trip-button-{{ trip.trip_id }}: /trips/<int:trip_id>/edit
delete-trip-button-{{ trip.trip_id }}: delete action (POST likely) |
| /bookings/confirmation     | GET          | booking_confirmation   | booking_confirmation.html| booking: Dict (confirmation_number:str, booking_date:str, amount:float, locations:str)                                       | download-itinerary-button: download action
share-trip-button: share action
back-to-dashboard: /dashboard                            |
| /recommendations            | GET          | recommendations        | recommendations.html    | trending_destinations: List[Dict] (dest_id:int, name:str, popularity_rank:int)
season_filter_options: List[str]
budget_filter_options: List[str] | back-to-dashboard: /dashboard                                                                                                           |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-destinations (Div): Display of featured travel destinations.
  - upcoming-trips (Div): Display of upcoming planned trips.
  - browse-destinations-button (Button): Navigate to Destinations page.
  - plan-itinerary-button (Button): Navigate to Itinerary Planning page.
- Context Variables:
  - featured_destinations: List of Dicts {dest_id:int, name:str, country:str}
  - upcoming_trips: List of Dicts {trip_id:int, trip_name:str, start_date:str}
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. Destinations Page
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Container
  - search-destination (Input): Search field
  - region-filter (Dropdown): Filter by region
  - destinations-grid (Div): Grid of destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View destination details
- Context Variables:
  - destinations: List of Dicts {dest_id:int, name:str, country:str, region:str}
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. Destination Details Page
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container
  - destination-name (H1): Destination name
  - destination-country (Div): Country
  - destination-description (Div): Description
  - add-to-trip-button (Button): Add destination to trip
  - destination-attractions (Div): Attractions section
- Context Variables:
  - destination: Dict {dest_id:int, name:str, country:str, description:str, attractions:str}
- Navigation Mappings:
  - add-to-trip-button: form POST or button action (no URL navigation specified)

### 4. Itinerary Planning Page
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Container
  - itinerary-name-input (Input): Itinerary name field
  - start-date-input (Input date): Trip start date
  - end-date-input (Input date): Trip end date
  - add-activity-button (Button): Add activity to itinerary
  - itinerary-list (Div): List of itineraries with edit/delete
- Context Variables:
  - itineraries: List of Dicts {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button: form POST or JS action (no direct URL navigation specified)

### 5. Accommodations Page
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container
  - destination-input (Input): Enter destination city
  - check-in-date (Input date): Check-in date
  - check-out-date (Input date): Check-out date
  - price-filter (Dropdown): Filter by price
  - hotels-list (Div): List of hotels
- Context Variables:
  - hotels: List of Dicts {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str}
- Navigation Mappings:
  - None explicit specified

### 6. Transportation Page
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container
  - departure-city (Input): Departure city field
  - arrival-city (Input): Arrival city field
  - departure-date (Input date): Departure date
  - flight-class-filter (Dropdown): Flight class filter
  - available-flights (Div): List available flights with details
- Context Variables:
  - flights: List of Dicts {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str}
- Navigation Mappings:
  - None explicit specified

### 7. Travel Packages Page
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of packages
  - duration-filter (Dropdown): Filter by duration
  - view-package-details-button-{{ pkg.package_id }} (Button): View package details
  - book-package-button-{{ pkg.package_id }} (Button): Book package
- Context Variables:
  - packages: List of Dicts {package_id:int, package_name:str, destination:str, duration_days:int, price:float}
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('travel_package_details', package_id=pkg.package_id)  (assuming a details page)
  - book-package-button-{{ pkg.package_id }}: booking action (POST or JS)

### 8. Trip Management Page
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container
  - trips-table (Table): Display trips with columns
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: List of Dicts {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }}: action POST or JS (no navigation URL)

### 9. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Booking confirmation number
  - booking-details (Div): Detailed booking info
  - download-itinerary-button (Button): Download trip itinerary PDF
  - share-trip-button (Button): Share trip details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - booking: Dict {confirmation_number:str, booking_date:str, amount:float, locations:str}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 10. Travel Recommendations Page
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container
  - trending-destinations (Div): Display trending destinations
  - recommendation-season-filter (Dropdown): Filter by travel season
  - budget-filter (Dropdown): Filter by budget
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - trending_destinations: List of Dicts {dest_id:int, name:str, popularity_rank:int}
  - season_filter_options: List[str] ("Spring", "Summer", "Fall", "Winter")
  - budget_filter_options: List[str] ("Low", "Medium", "High")
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited): dest_id|name|country|region|description|attractions|climate
- Description: Stores travel destination details.
- Example Rows:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited): itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Stores user itineraries with schedules and activities.
- Example Rows:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited): hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Stores hotel details for accommodations.
- Example Rows:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited): flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flight options for transportation booking.
- Example Rows:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited): package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Stores pre-designed travel packages.
- Example Rows:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited): trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: Stores trips created by the user.
- Example Rows:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited): booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Stores booking records with confirmation details.
- Example Rows:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
