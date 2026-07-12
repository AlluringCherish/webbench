# TravelPlanner Application Design Specification


---

## Section 1: Flask Routes Specification

| Route Endpoint                   | HTTP Methods | Function Name              | Template File               | Context Variables                                                                                     | Navigation Actions Triggered                                                                                 |
|---------------------------------|--------------|----------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| /dashboard                      | GET          | dashboard                  | templates/dashboard.html     | featured_destinations: List[Dict]{dest_id:int, name:str, country:str}, upcoming_trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str} | browse-destinations-button leads to /destinations                                                           |
| /destinations                  | GET, POST    | destinations               | templates/destinations.html  | destinations: List[Dict]{dest_id:int, name:str, country:str, region:str}                              | view-destination-button-{{ dest.dest_id }} leads to /destinations/<int:dest_id>                              |
| /destinations/<int:dest_id>   | GET, POST    | destination_details        | templates/destination_details.html | destination: Dict{name:str, country:str, description:str, attractions:str}                         | add-to-trip-button leads to action of adding destination to trip                                            |
| /itinerary                    | GET, POST    | itinerary                  | templates/itinerary.html     | itineraries: List[Dict]{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str} | add-activity-button adds activity; edit/delete links in itinerary-list                                        |
| /accommodations               | GET, POST    | accommodations             | templates/accommodations.html| hotels: List[Dict]{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str} | Search and filter triggers hotels-list update                                                               |
| /transportation               | GET, POST    | transportation             | templates/transportation.html| flights: List[Dict]{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str} | Flight search updates available-flights                                                                      |
| /packages                     | GET, POST    | travel_packages            | templates/packages.html      | packages: List[Dict]{package_id:int, package_name:str, destination:str, duration_days:int, price:float} | view-package-details-button-{{ pkg.package_id }} leads to package details (endpoint not listed but implied)  |
| /trips                       | GET, POST    | trips                     | templates/trips.html         | trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str} | view-trip-details-button-{{ trip.trip_id }}, edit-trip-button-{{ trip.trip_id }}, delete-trip-button-{{ trip.trip_id }}| 
| /booking-confirmation         | GET          | booking_confirmation       | templates/booking_confirmation.html | booking: Dict{confirmation_number:str, booking_details:str}                                      | back-to-dashboard leads to /dashboard                                                                        |
| /recommendations              | GET, POST    | travel_recommendations     | templates/recommendations.html| recommendations: List[Dict], trending_destinations: List[Dict]{dest_id:int, name:str, country:str, popularity:int} | back-to-dashboard leads to /dashboard                                                                        |


---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page.
  - ID: featured-destinations (Div) - Display featured travel destinations.
  - ID: upcoming-trips (Div) - Display upcoming planned trips.
  - ID: browse-destinations-button (Button) - Navigate to destinations page.
  - ID: plan-itinerary-button (Button) - Navigate to itinerary planning page.
- Context Variables:
  - featured_destinations: List[Dict]{dest_id:int, name:str, country:str}
  - upcoming_trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str}
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. templates/destinations.html
- Page Title: Travel Destinations
- Elements:
  - ID: destinations-page (Div) - Container.
  - ID: search-destination (Input) - Search by name or country.
  - ID: region-filter (Dropdown) - Filter by region (Asia, Europe, Americas, Africa, Oceania).
  - ID: destinations-grid (Div) - Grid for destination cards.
  - ID pattern: view-destination-button-{{ dest.dest_id }} (Button) - View details for each destination.
- Context Variables:
  - destinations: List[Dict]{dest_id:int, name:str, country:str, region:str}
- Navigation Mappings:
  - view-destination-button-{{ dest.dest_id }} : url_for('destination_details', dest_id=dest.dest_id)

### 3. templates/destination_details.html
- Page Title: Destination Details
- Elements:
  - ID: destination-details-page (Div) - Container.
  - ID: destination-name (H1) - Destination name.
  - ID: destination-country (Div) - Country.
  - ID: destination-description (Div) - Description.
  - ID: add-to-trip-button (Button) - Add destination to trip.
  - ID: destination-attractions (Div) - Attractions and activities.
- Context Variables:
  - destination: Dict{name:str, country:str, description:str, attractions:str}
- Navigation Mappings:
  - add-to-trip-button: triggers action to add destination to trip (possibly via POST)

### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Elements:
  - ID: itinerary-page (Div) - Container.
  - ID: itinerary-name-input (Input) - Itinerary name field.
  - ID: start-date-input (Input date) - Start date field.
  - ID: end-date-input (Input date) - End date field.
  - ID: add-activity-button (Button) - Add activity to itinerary.
  - ID: itinerary-list (Div) - List of itineraries with edit/delete buttons.
- Context Variables:
  - itineraries: List[Dict]{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button: triggers adding an activity (via form or modal)
  - edit/delete links/buttons in itinerary-list handled per itinerary entry

### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Elements:
  - ID: accommodations-page (Div) - Container.
  - ID: destination-input (Input) - Destination city field.
  - ID: check-in-date (Input date) - Check-in date field.
  - ID: check-out-date (Input date) - Check-out date field.
  - ID: price-filter (Dropdown) - Price range filter (Budget, Mid-range, Luxury).
  - ID: hotels-list (Div) - List hotels with details.
- Context Variables:
  - hotels: List[Dict]{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
- Navigation Mappings:
  - Filtering and search update hotels-list dynamically

### 6. templates/transportation.html
- Page Title: Book Flights
- Elements:
  - ID: transportation-page (Div) - Container.
  - ID: departure-city (Input) - Departure city field.
  - ID: arrival-city (Input) - Arrival city field.
  - ID: departure-date (Input date) - Departure date field.
  - ID: flight-class-filter (Dropdown) - Flight class filter (Economy, Business, First Class).
  - ID: available-flights (Div) - List flights with details.
- Context Variables:
  - flights: List[Dict]{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
- Navigation Mappings:
  - Flight search and filter updates available-flights dynamically

### 7. templates/packages.html
- Page Title: Travel Packages
- Elements:
  - ID: packages-page (Div) - Container.
  - ID: packages-grid (Div) - Grid of package cards.
  - ID: duration-filter (Dropdown) - Duration filter (3-5 days, 7-10 days, 14+ days).
  - ID pattern: view-package-details-button-{{ pkg.package_id }} (Button) - View package details.
  - ID pattern: book-package-button-{{ pkg.package_id }} (Button) - Book package.
- Context Variables:
  - packages: List[Dict]{package_id:int, package_name:str, destination:str, duration_days:int, price:float}
- Navigation Mappings:
  - view-package-details-button-{{ pkg.package_id }}: leads to package detail page (endpoint not specified but presumed)
  - book-package-button-{{ pkg.package_id }}: triggers booking action

### 8. templates/trips.html
- Page Title: My Trips
- Elements:
  - ID: trips-page (Div) - Container.
  - ID: trips-table (Table) - Table of all trips.
  - ID pattern: view-trip-details-button-{{ trip.trip_id }} (Button) - View trip details.
  - ID pattern: edit-trip-button-{{ trip.trip_id }} (Button) - Edit trip.
  - ID pattern: delete-trip-button-{{ trip.trip_id }} (Button) - Delete trip.
- Context Variables:
  - trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation Mappings:
  - Viewing, editing, deleting trip via respective buttons linked to routes with trip_id

### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Elements:
  - ID: confirmation-page (Div) - Container.
  - ID: confirmation-number (Div) - Booking confirmation number.
  - ID: booking-details (Div) - Detailed booking info.
  - ID: download-itinerary-button (Button) - Download trip itinerary as PDF.
  - ID: share-trip-button (Button) - Share trip details.
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - booking: Dict{confirmation_number:str, booking_details:str}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Elements:
  - ID: recommendations-page (Div) - Container.
  - ID: trending-destinations (Div) - Trending destinations by popularity.
  - ID: recommendation-season-filter (Dropdown) - Filter by travel season (Spring, Summer, Fall, Winter).
  - ID: budget-filter (Dropdown) - Filter by budget (Low, Medium, High).
  - ID: back-to-dashboard (Button) - Navigate back to dashboard.
- Context Variables:
  - recommendations: List[Dict] (structure depends on recommendations)
  - trending_destinations: List[Dict]{dest_id:int, name:str, country:str, popularity:int}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')


---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- Fields (pipe-delimited, no header):
  - dest_id (int)
  - name (str)
  - country (str)
  - region (str)
  - description (str)
  - attractions (str)
  - climate (str)
- Description: Stores travel destination details including attractions and climate.
- Example Rows:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. data/itineraries.txt
- Fields:
  - itinerary_id (int)
  - itinerary_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - activities (str)
  - status (str)
- Description: Stores itineraries with activities and status.
- Example Rows:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. data/hotels.txt
- Fields:
  - hotel_id (int)
  - name (str)
  - city (str)
  - rating (float)
  - price_per_night (float)
  - amenities (str)
  - category (str)
- Description: Contains hotel listings with prices and amenities.
- Example Rows:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. data/flights.txt
- Fields:
  - flight_id (int)
  - airline (str)
  - departure_city (str)
  - arrival_city (str)
  - departure_time (str, HH:MM or with text, e.g. "15:20 next day")
  - arrival_time (str)
  - price (float)
  - class_type (str)
  - duration (str)
- Description: Flight data with timings, pricing, and class.
- Example Rows:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. data/packages.txt
- Fields:
  - package_id (int)
  - package_name (str)
  - destination (str)
  - duration_days (int)
  - price (float)
  - included_items (str)
  - difficulty_level (str)
- Description: Stores travel packages details with pricing and items included.
- Example Rows:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. data/trips.txt
- Fields:
  - trip_id (int)
  - trip_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - total_budget (float)
  - status (str)
  - created_date (str, YYYY-MM-DD)
- Description: Holds user's trip records including budget and status.
- Example Rows:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. data/bookings.txt
- Fields:
  - booking_id (int)
  - trip_id (int)
  - booking_type (str)
  - booking_date (str, YYYY-MM-DD)
  - amount (float)
  - confirmation_number (str)
  - status (str)
- Description: Booking confirmation records for trips.
- Example Rows:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

---

This specification fully supports independent backend and frontend development, ensuring consistent naming, route mapping, and data formats across the 'TravelPlanner' application.
