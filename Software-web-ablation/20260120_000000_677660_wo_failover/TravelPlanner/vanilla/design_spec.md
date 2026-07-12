# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                   | HTTP Methods | Function Name              | Template File                 | Context Variables                                                                                     | Navigation Actions                                                                                          |
|---------------------------------|--------------|----------------------------|-------------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| / (Dashboard)                   | GET          | dashboard                  | templates/dashboard.html       | featured_destinations: List[Dict]{dest_id:int, name:str, country:str}, upcoming_trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str} | browse-destinations-button -> url_for('destinations')                                                     |
| /destinations                  | GET, POST    | destinations               | templates/destinations.html    | destinations: List[Dict]{dest_id:int, name:str, country:str, region:str}, region_filter: str (optional), search_query: str (optional)                  | view-destination-button-{dest_id} -> url_for('destination_details', dest_id=dest_id)                       |
| /destinations/<int:dest_id>    | GET, POST   | destination_details        | templates/destination_details.html | destination: Dict{dest_id:int, name:str, country:str, region:str, description:str, attractions:str, climate:str}                                  | add-to-trip-button -> functional add (possibly POST), no navigation change                                  |
| /itinerary                    | GET, POST   | itinerary                  | templates/itinerary.html       | itineraries: List[Dict]{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}            | add-activity-button -> POST to add activity, edit/delete actions on itinerary list rendered on page        |
| /accommodations               | GET          | accommodations             | templates/accommodations.html  | hotels: List[Dict]{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}, filters: dict             | hotels_list rendered with details, no specific navigation buttons                                         |
| /transportation               | GET          | transportation             | templates/transportation.html  | flights: List[Dict]{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}, filters: dict | available-flights list rendered, no specific navigation buttons                                           |
| /packages                    | GET          | packages                  | templates/packages.html        | packages: List[Dict]{package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}, filters: dict | view-package-details-button-{pkg_id} -> url_for('package_details', pkg_id=pkg_id), book-package-button-{pkg_id} -> url_for('book_package', pkg_id=pkg_id) |
| /trips                       | GET          | trips                     | templates/trips.html           | trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}                                            | view-trip-details-button-{trip_id} -> url_for('trip_details', trip_id=trip_id), edit-trip-button-{trip_id} -> url_for('edit_trip', trip_id=trip_id), delete-trip-button-{trip_id} -> POST to delete                 |
| /booking_confirmation        | GET          | booking_confirmation      | templates/booking_confirmation.html | booking: Dict{confirmation_number:str, booking_details:str (HTML or formatted string)}                                                              | download-itinerary-button -> triggers file download, share-trip-button -> open share dialog or copy link, back-to-dashboard -> url_for('dashboard')               |
| /recommendations             | GET          | recommendations           | templates/recommendations.html | trending_destinations: List[Dict]{dest_id:int, name:str, popularity:int}, filters: dict                                                               | back-to-dashboard -> url_for('dashboard')                                                                    |

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - featured-destinations (Div): Displays featured destinations list
  - upcoming-trips (Div): Displays upcoming trips list
  - browse-destinations-button (Button): Navigates to destinations page via url_for('destinations')
  - plan-itinerary-button (Button): Navigates to itinerary planning page via url_for('itinerary')
- Context Variables:
  - featured_destinations: List[Dict]{dest_id:int, name:str, country:str}
  - upcoming_trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str}

### 2. templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page (Div): Main container
  - search-destination (Input): Text input to filter destinations
  - region-filter (Dropdown): Dropdown filter for region with options (Asia, Europe, Americas, Africa, Oceania)
  - destinations-grid (Div): Grid container for destination cards
  - view-destination-button-{{ dest.dest_id }} (Button): Button for each destination to view details
- Context Variables:
  - destinations: List[Dict]{dest_id:int, name:str, country:str, region:str}
  - region_filter: str (optional)
  - search_query: str (optional)
- Navigation:
  - view-destination-button-{{ dest.dest_id }} calls url_for('destination_details', dest_id=dest.dest_id)

### 3. templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page (Div): Container
  - destination-name (H1): Destination name text
  - destination-country (Div): Destination country
  - destination-description (Div): Destination detailed description
  - add-to-trip-button (Button): POST action to add destination to trip
  - destination-attractions (Div): List or description of main attractions and activities
- Context Variables:
  - destination: Dict{dest_id:int, name:str, country:str, region:str, description:str, attractions:str, climate:str}
- Navigation:
  - add-to-trip-button is a form submission (POST), no navigation event

### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page (Div): Main container
  - itinerary-name-input (Input): Text input for itinerary name
  - start-date-input (Input date): Start date selector
  - end-date-input (Input date): End date selector
  - add-activity-button (Button): POST to add new activities
  - itinerary-list (Div): Displays created itineraries with edit/delete controls
- Context Variables:
  - itineraries: List[Dict]{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation:
  - Edit/Delete itinerary actions embedded per itinerary entry (links or buttons linking to or calling edit/delete routes or methods)

### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page (Div): Main container
  - destination-input (Input): Destination city input
  - check-in-date (Input date): Check-in selector
  - check-out-date (Input date): Check-out selector
  - price-filter (Dropdown): Filter by price range options (Budget, Mid-range, Luxury)
  - hotels-list (Div): List container for hotels with details (name, rating, price, amenities)
- Context Variables:
  - hotels: List[Dict]{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
- Navigation:
  - Filter controls affect displayed hotels, no explicit navigation buttons

### 6. templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page (Div): Main container
  - departure-city (Input): Departure city input
  - arrival-city (Input): Arrival city input
  - departure-date (Input date): Departure date selector
  - flight-class-filter (Dropdown): Flight class filter with options (Economy, Business, First Class)
  - available-flights (Div): List container for flights with airline, time, price
- Context Variables:
  - flights: List[Dict]{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
- Navigation:
  - Flights list is informational, no navigation buttons

### 7. templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page (Div): Container
  - packages-grid (Div): Grid of package cards
  - duration-filter (Dropdown): Duration filter with options (3-5 days,7-10 days,14+ days)
  - view-package-details-button-{{ pkg.package_id }} (Button): View package details
  - book-package-button-{{ pkg.package_id }} (Button): Book selected package
- Context Variables:
  - packages: List[Dict]{package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str, difficulty_level:str}
- Navigation:
  - view-package-details-button-{{ pkg.package_id }} -> url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }} -> url_for('book_package', pkg_id=pkg.package_id)

### 8. templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page (Div): Container
  - trips-table (Table): Table listing trips with columns for destination, dates, status
  - view-trip-details-button-{{ trip.trip_id }} (Button): View trip details
  - edit-trip-button-{{ trip.trip_id }} (Button): Edit trip
  - delete-trip-button-{{ trip.trip_id }} (Button): Delete trip
- Context Variables:
  - trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation:
  - Viewing, editing, deleting trip call respective URL endpoints

### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - confirmation-number (Div): Shows booking confirmation number
  - booking-details (Div): Detailed booking info
  - download-itinerary-button (Button): Triggers itinerary PDF download
  - share-trip-button (Button): Triggers share dialog
  - back-to-dashboard (Button): Navigates back to dashboard
- Context Variables:
  - booking: Dict{confirmation_number:str, booking_details:str}
- Navigation:
  - back-to-dashboard -> url_for('dashboard')

### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page (Div): Main container
  - trending-destinations (Div): Shows list ranked by popularity
  - recommendation-season-filter (Dropdown): Filter trips by season (Spring, Summer, Fall, Winter)
  - budget-filter (Dropdown): Filter by budget (Low, Medium, High)
  - back-to-dashboard (Button): Navigates to dashboard
- Context Variables:
  - trending_destinations: List[Dict]{dest_id:int, name:str, popularity:int}
- Navigation:
  - back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- Fields (pipe-delimited, no header):
  dest_id|name|country|region|description|attractions|climate
- Description: Travel destinations data including basic info, description, and tourist attractions
- Example:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

### 2. data/itineraries.txt
- Fields (pipe-delimited, no header):
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: User itineraries with names, dates, activities, and status
- Example:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

### 3. data/hotels.txt
- Fields (pipe-delimited, no header):
  hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Hotels data with rating, pricing, and amenities
- Example:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

### 4. data/flights.txt
- Fields (pipe-delimited, no header):
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Flight options with times, prices, and class
- Example:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

### 5. data/packages.txt
- Fields (pipe-delimited, no header):
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Pre-designed travel packages
- Example:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

### 6. data/trips.txt
- Fields (pipe-delimited, no header):
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: User created trips with budget and dates
- Example:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

### 7. data/bookings.txt
- Fields (pipe-delimited, no header):
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Booking records linked to trips
- Example:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
