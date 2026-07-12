# TravelPlanner Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                     | HTTP Methods | Function Name                | Template File                   | Context Variables (Type & Structure)                                                                                             | Navigation Actions Triggered by Buttons/Links                                                                        |
|----------------------------------|--------------|-----------------------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| / (Dashboard)                    | GET          | dashboard                   | dashboard.html                 | featured_destinations: list of dict {dest_id:int, name:str, country:str}                                                        
upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str}                        | browse-destinations-button: url_for('destinations') 
plan-itinerary-button: url_for('plan_itinerary')                |
| /destinations                   | GET          | destinations                | destinations.html              | destinations: list of dict {dest_id:int, name:str, country:str, region:str}                                                     | view-destination-button-{{dest_id}}: url_for('destination_details', dest_id=dest_id)                                   |
| /destinations/<int:dest_id>     | GET          | destination_details         | destination_details.html       | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}                                        | add-to-trip-button: triggers adding destination to trip (handled backend)                                             |
| /itinerary                     | GET, POST    | plan_itinerary              | itinerary.html                 | GET: itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, status:str} 
POST: Form data for new itinerary or activity                                                                             | add-activity-button: triggers form submission (POST) 
View/Edit/Delete itinerary actions reflected in context and backend|
| /accommodations                | GET          | accommodations              | accommodations.html            | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}         | N/A                                                                                                                  |
| /transportation               | GET          | transportation              | transportation.html            | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}| N/A                                                                                                                  |
| /packages                    | GET          | travel_packages             | packages.html                 | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}                       | view-package-details-button-{{pkg_id}}: url_for('package_details', pkg_id=pkg_id)  
book-package-button-{{pkg_id}}: triggers booking via backend |
| /trips                      | GET          | trip_management             | trips.html                   | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}                      | view-trip-details-button-{{trip_id}}: url_for('trip_details', trip_id=trip_id)
edit-trip-button-{{trip_id}}: url_for('edit_trip', trip_id=trip_id) 
delete-trip-button-{{trip_id}}: triggers delete trip (handled backend) |
| /booking-confirmation       | GET          | booking_confirmation        | confirmation.html             | booking: dict {confirmation_number:str, booking_details:str}                                                                     | download-itinerary-button: triggers itinerary PDF download 
share-trip-button: triggers share functionality 
back-to-dashboard: url_for('dashboard')  |
| /recommendations            | GET          | travel_recommendations      | recommendations.html          | trending_destinations: list of dict {dest_id:int, name:str, popularity:int}                                                     | back-to-dashboard: url_for('dashboard')                                                                              |

---

## Section 2: HTML Templates Specification

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard.
  - featured-destinations (Div): Display featured destinations.
  - upcoming-trips (Div): Display upcoming trips.
  - browse-destinations-button (Button): Navigates to destinations page.
  - plan-itinerary-button (Button): Navigates to itinerary planning page.
- Context Variables:
  - featured_destinations: list of dict {dest_id:int, name:str, country:str}
  - upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str}
- Navigation:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('plan_itinerary')

### 2. destinations.html
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Container
  - search-destination (Input): Search input field
  - region-filter (Dropdown): Region filter dropdown
  - destinations-grid (Div): Grid of destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): View details button for each destination
- Context Variables:
  - destinations: list of dict {dest_id:int, name:str, country:str, region:str}
- Navigation:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. destination_details.html
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container
  - destination-name (H1): Destination name display
  - destination-country (Div): Destination country
  - destination-description (Div): Description
  - add-to-trip-button (Button): Adds destination to trip
  - destination-attractions (Div): Attractions display
- Context Variables:
  - destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}
- Navigation:
  - add-to-trip-button: backend action to add destination

### 4. itinerary.html
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Container
  - itinerary-name-input (Input): Enter itinerary name
  - start-date-input (Input date): Start date
  - end-date-input (Input date): End date
  - add-activity-button (Button): Add activity
  - itinerary-list (Div): List of itineraries
- Context Variables:
  - itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation:
  - add-activity-button: form submission

### 5. accommodations.html
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Container
  - destination-input (Input): Hotel destination input
  - check-in-date (Input date): Check-in
  - check-out-date (Input date): Check-out
  - price-filter (Dropdown): Price filter
  - hotels-list (Div): List of hotels
- Context Variables:
  - hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
- Navigation:
  - No explicit navigation buttons

### 6. transportation.html
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Container
  - departure-city (Input): Departure city
  - arrival-city (Input): Arrival city
  - departure-date (Input date): Departure date
  - flight-class-filter (Dropdown): Flight class filter
  - available-flights (Div): List of flights
- Context Variables:
  - flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
- Navigation:
  - No explicit navigation buttons

### 7. packages.html
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of package cards
  - duration-filter (Dropdown): Duration filter
  - view-package-details-button-{{ pkg.package_id }} (Button): View details
  - book-package-button-{{ pkg.package_id }} (Button): Book package
- Context Variables:
  - packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}
- Navigation:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', pkg_id=pkg.package_id)

### 8. trips.html
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container
  - trips-table (Table): List of trips
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)

### 9. confirmation.html
- Filename: templates/confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Confirmation number display
  - booking-details (Div): Booking information
  - download-itinerary-button (Button): Download itinerary PDF
  - share-trip-button (Button): Share trip details
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - booking: dict {confirmation_number:str, booking_details:str}
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### 10. recommendations.html
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Container
  - trending-destinations (Div): Trending destinations display
  - recommendation-season-filter (Dropdown): Season filter
  - budget-filter (Dropdown): Budget filter
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - trending_destinations: list of dict {dest_id:int, name:str, popularity:int}
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  - dest_id (int)
  - name (str)
  - country (str)
  - region (str)
  - description (str)
  - attractions (str)
  - climate (str)
- Description: Stores all travel destinations information
- Example rows:
  - 1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  - 2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  - 3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, no header):
  - itinerary_id (int)
  - itinerary_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - activities (str)
  - status (str)
- Description: Stores user-created travel itineraries
- Example rows:
  - 1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  - 2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  - 3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, no header):
  - hotel_id (int)
  - name (str)
  - city (str)
  - rating (float)
  - price_per_night (float)
  - amenities (str)
  - category (str)
- Description: Stores hotel listings for accommodations
- Example rows:
  - 1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  - 2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  - 3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, no header):
  - flight_id (int)
  - airline (str)
  - departure_city (str)
  - arrival_city (str)
  - departure_time (str, HH:MM or HH:MM next day)
  - arrival_time (str, HH:MM or HH:MM next day)
  - price (float)
  - class_type (str)
  - duration (str)
- Description: Stores flight information for booking
- Example rows:
  - 1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  - 2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  - 3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, no header):
  - package_id (int)
  - package_name (str)
  - destination (str)
  - duration_days (int)
  - price (float)
  - included_items (str)
  - difficulty_level (str)
- Description: Stores predefined travel packages
- Example rows:
  - 1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  - 2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  - 3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, no header):
  - trip_id (int)
  - trip_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - total_budget (float)
  - status (str)
  - created_date (str, YYYY-MM-DD)
- Description: Stores all user trips
- Example rows:
  - 1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  - 2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  - 3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  - booking_id (int)
  - trip_id (int)
  - booking_type (str)
  - booking_date (str, YYYY-MM-DD)
  - amount (float)
  - confirmation_number (str)
  - status (str)
- Description: Stores booking confirmation details
- Example rows:
  - 1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  - 2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  - 3|3|Package|2025-01-12|1800.00|CONF003|Pending
