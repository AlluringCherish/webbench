# TravelPlanner Application Design Specifications

---

## Section 1: Flask Routes Specification

| Route Endpoint                  | HTTP Methods | Function Name            | Template File              | Context Variables (with types & structure)                                      | Navigation Actions Triggered by Buttons/Links                                   |
|--------------------------------|--------------|--------------------------|----------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| /                              | GET          | dashboard                | dashboard.html             | featured_destinations: list of dict {dest_id:int, name:str, country:str}        | browse-destinations-button -> /destinations                                   |
|                                |              |                          |                            | upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, dates:str} | plan-itinerary-button -> /itinerary                                            |
| /destinations                  | GET, POST    | destinations             | destinations.html          | destinations: list of dict {dest_id:int, name:str, country:str, region:str}      | view-destination-button-{{ dest_id }} -> /destinations/<int:dest_id>          |
| /destinations/<int:dest_id>   | GET, POST    | destination_details      | destination_details.html   | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str, climate:str} | add-to-trip-button -> /itinerary (POST action)                               |
| /itinerary                    | GET, POST    | itinerary                | itinerary.html             | itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str} | add-activity-button -> add activity function on page                         |
| /accommodations               | GET, POST    | accommodations           | accommodations.html        | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str} | N/A - no navigation buttons specified on the page                             |
| /transportation              | GET, POST    | transportation           | transportation.html        | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str} | N/A - no navigation buttons specified on the page                             |
| /packages                   | GET, POST    | packages                 | packages.html              | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str} | view-package-details-button-{{ pkg_id }} -> /packages/<int:package_id>        |
|                             |              |                          |                            |                                                                                 | book-package-button-{{ pkg_id }} -> Book action on current page              |
| /trips                     | GET, POST    | trips                    | trips.html                 | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str} | view-trip-details-button-{{ trip_id }} -> /trips/<int:trip_id>               |
|                             |              |                          |                            |                                                                                 | edit-trip-button-{{ trip_id }} -> edit trip form/page                        |
|                             |              |                          |                            |                                                                                 | delete-trip-button-{{ trip_id }} -> delete action on current page            |
| /bookings/confirmation      | GET          | booking_confirmation     | booking_confirmation.html  | booking: dict {confirmation_number:str, booking_details:str}                    | download-itinerary-button -> download PDF action                             |
|                             |              |                          |                            |                                                                                 | share-trip-button -> share action                                           |
|                             |              |                          |                            |                                                                                 | back-to-dashboard -> /                                                      |
| /recommendations            | GET          | recommendations          | recommendations.html       | trending_destinations: list of dict {dest_id:int, name:str, popularity:int}     | back-to-dashboard -> /                                                        |

---

## Section 2: HTML Templates Specification

#### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page: Div - Main container
  - featured-destinations: Div - Displays featured destinations
  - upcoming-trips: Div - Displays upcoming trips
  - browse-destinations-button: Button - Navigates to /destinations
  - plan-itinerary-button: Button - Navigates to /itinerary
- Context Variables:
  - featured_destinations: list of dict {dest_id:int, name:str, country:str}
  - upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, dates:str}
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

#### 2. templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page: Div
  - search-destination: Input
  - region-filter: Dropdown
  - destinations-grid: Div
  - Dynamic buttons:
    - view-destination-button-{{ dest.dest_id }}: Button to view specific destination details
- Context Variables:
  - destinations: list of dict {dest_id:int, name:str, country:str, region:str}
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

#### 3. templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page: Div
  - destination-name: H1
  - destination-country: Div
  - destination-description: Div
  - add-to-trip-button: Button (form submit for POST)
  - destination-attractions: Div
- Context Variables:
  - destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str, climate:str}
- Navigation Mappings:
  - add-to-trip-button: Submits to current route POST

#### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page: Div
  - itinerary-name-input: Input
  - start-date-input: Input (date)
  - end-date-input: Input (date)
  - add-activity-button: Button
  - itinerary-list: Div
- Context Variables:
  - itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button: triggers activity addition (likely AJAX or form post)

#### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page: Div
  - destination-input: Input
  - check-in-date: Input (date)
  - check-out-date: Input (date)
  - price-filter: Dropdown
  - hotels-list: Div
- Context Variables:
  - hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
- Navigation Mappings: None specified

#### 6. templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page: Div
  - departure-city: Input
  - arrival-city: Input
  - departure-date: Input (date)
  - flight-class-filter: Dropdown
  - available-flights: Div
- Context Variables:
  - flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
- Navigation Mappings: None specified

#### 7. templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page: Div
  - packages-grid: Div
  - duration-filter: Dropdown
  - Dynamic buttons:
    - view-package-details-button-{{ pkg.package_id }}: Button
    - book-package-button-{{ pkg.package_id }}: Button
- Context Variables:
  - packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', package_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: triggers booking action

#### 8. templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page: Div
  - trips-table: Table
  - Dynamic buttons:
    - view-trip-details-button-{{ trip.trip_id }}: Button
    - edit-trip-button-{{ trip.trip_id }}: Button
    - delete-trip-button-{{ trip.trip_id }}: Button
- Context Variables:
  - trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, total_budget:float, status:str, created_date:str}
- Navigation Mappings:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: navigates to trip edit page
  - delete-trip-button-{{ trip.trip_id }}: triggers delete action

#### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page: Div
  - confirmation-number: Div
  - booking-details: Div
  - download-itinerary-button: Button
  - share-trip-button: Button
  - back-to-dashboard: Button
- Context Variables:
  - booking: dict {confirmation_number:str, booking_details:str}
- Navigation Mappings:
  - download-itinerary-button: triggers PDF download
  - share-trip-button: triggers sharing action
  - back-to-dashboard: url_for('dashboard')

#### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page: Div
  - trending-destinations: Div
  - recommendation-season-filter: Dropdown
  - budget-filter: Dropdown
  - back-to-dashboard: Button
- Context Variables:
  - trending_destinations: list of dict {dest_id:int, name:str, popularity:int}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- Fields (pipe-delimited, no header):
  dest_id|name|country|region|description|attractions|climate
- Description: Stores all travel destinations with key details.
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. data/itineraries.txt
- Fields (pipe-delimited, no header):
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Stores user-created travel itineraries.
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. data/hotels.txt
- Fields (pipe-delimited, no header):
  hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Stores hotel accommodation details.
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. data/flights.txt
- Fields (pipe-delimited, no header):
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flight information for booking.
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. data/packages.txt
- Fields (pipe-delimited, no header):
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Stores predefined travel packages.
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. data/trips.txt
- Fields (pipe-delimited, no header):
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: Stores user trips with budget and status.
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. data/bookings.txt
- Fields (pipe-delimited, no header):
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Stores booking confirmations and related financial information.
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

---