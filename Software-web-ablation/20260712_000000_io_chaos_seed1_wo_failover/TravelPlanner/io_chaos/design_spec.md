# Design Specification for TravelPlanner Web Application

---

## Section 1: Flask Routes Specification

| Route Endpoint                      | HTTP Methods     | Function Name              | Template File               | Context Variables Passed                                                    | Navigation Actions (Button/Link IDs and Targets)                                                   |
|-----------------------------------|------------------|----------------------------|-----------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| /dashboard                        | GET              | dashboard                 | templates/dashboard.html    | featured_destinations: List[Dict] (dest_id:int, name:str, country:str)
  upcoming_trips: List[Dict] (trip_id:int, trip_name:str, start_date:str, end_date:str)            | browse-destinations-button -> url_for('destinations')
  plan-itinerary-button -> url_for('itinerary')                                                   |
| /destinations                    | GET, POST        | destinations              | templates/destinations.html | destinations: List[Dict] (dest_id:int, name:str, country:str, region:str)     | view-destination-button-{dest_id} -> url_for('destination_details', dest_id=dest_id)              |
| /destinations/&lt;int:dest_id&gt; | GET, POST        | destination_details       | templates/destination_details.html | destination: Dict (dest_id:int, name:str, country:str, description:str, attractions:str)        | add-to-trip-button -> url_for('itinerary')                                                        |
| /itinerary                      | GET, POST        | itinerary                 | templates/itinerary.html    | itineraries: List[Dict] (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str) | add-activity-button -> adds activity (AJAX or form POST)
  itinerary-list edit/delete handled in page                                       |
| /accommodations                 | GET, POST        | accommodations            | templates/accommodations.html | hotels: List[Dict] (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str) |                                                                                               |
| /transportation                 | GET, POST        | transportation            | templates/transportation.html | flights: List[Dict] (flight_id:int, airline:str, departure_city:str, arrival_city:str,
  departure_time:str, arrival_time:str, price:float, class_type:str, duration:str)               |                                                                                               |
| /packages                      | GET, POST        | packages                  | templates/packages.html     | packages: List[Dict] (package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str) | view-package-details-button-{pkg_id} -> url_for('package_details', pkg_id=pkg_id)
  book-package-button-{pkg_id} -> url_for('book_package', pkg_id=pkg_id)                            |
| /trips                         | GET, POST        | trips                     | templates/trips.html        | trips: List[Dict] (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str)                    | view-trip-details-button-{trip_id} -> url_for('trip_details', trip_id=trip_id)
  edit-trip-button-{trip_id} -> url_for('edit_trip', trip_id=trip_id)
  delete-trip-button-{trip_id} -> url_for('delete_trip', trip_id=trip_id)  |
| /booking-confirmation          | GET              | booking_confirmation      | templates/booking_confirmation.html | booking: Dict (confirmation_number:str, booking_details:str)                   | download-itinerary-button -> triggers PDF download
  share-trip-button -> triggers share mechanism
  back-to-dashboard -> url_for('dashboard')                                         |
| /recommendations               | GET              | recommendations           | templates/recommendations.html | trending_destinations: List[Dict] (dest_id:int, name:str, popularity_rank:int)
  filters: Dict (season:str, budget:str)                                          | back-to-dashboard -> url_for('dashboard')                                                          |

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Elements:
  - ID: dashboard-page (Div) - Main container for dashboard
  - ID: featured-destinations (Div) - Displays featured destinations list
  - ID: upcoming-trips (Div) - Displays upcoming trips list
  - ID: browse-destinations-button (Button) - Navigates to destinations page
  - ID: plan-itinerary-button (Button) - Navigates to itinerary planning page
- Context Variables:
  - featured_destinations: List[Dict] with fields: dest_id (int), name (str), country (str)
  - upcoming_trips: List[Dict] with fields: trip_id (int), trip_name (str), start_date (str), end_date (str)
- Navigation:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('itinerary')

### 2. templates/destinations.html
- Page Title: Travel Destinations
- Elements:
  - ID: destinations-page (Div) - Main container
  - ID: search-destination (Input) - Text input for searching destinations by name or country
  - ID: region-filter (Dropdown) - Filter destinations by region
  - ID: destinations-grid (Div) - Grid container for destination cards
  - ID: view-destination-button-{{ dest.dest_id }} (Button) - View details for each destination
- Context Variables:
  - destinations: List[Dict] with fields: dest_id (int), name (str), country (str), region (str)
- Navigation:
  - view-destination-button-{{ dest.dest_id }}: url_for('destination_details', dest_id=dest.dest_id)

### 3. templates/destination_details.html
- Page Title: Destination Details
- Elements:
  - ID: destination-details-page (Div) - Container
  - ID: destination-name (H1) - Destination name display
  - ID: destination-country (Div) - Destination country display
  - ID: destination-description (Div) - Detailed description
  - ID: add-to-trip-button (Button) - Adds destination to itinerary/trip
  - ID: destination-attractions (Div) - Main attractions and activities
- Context Variables:
  - destination: Dict with fields: dest_id (int), name (str), country (str), description (str), attractions (str)
- Navigation:
  - add-to-trip-button: url_for('itinerary')

### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Elements:
  - ID: itinerary-page (Div) - Container
  - ID: itinerary-name-input (Input) - Text input for itinerary name
  - ID: start-date-input (Input date) - Start date picker
  - ID: end-date-input (Input date) - End date picker
  - ID: add-activity-button (Button) - Add activity to itinerary
  - ID: itinerary-list (Div) - Displays created itineraries with edit/delete
- Context Variables:
  - itineraries: List[Dict] with fields: itinerary_id (int), itinerary_name (str), destination (str), start_date (str), end_date (str), activities (str), status (str)
- Navigation:
  - add-activity-button: triggers add activity POST

### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Elements:
  - ID: accommodations-page (Div) - Container
  - ID: destination-input (Input) - Destination city input
  - ID: check-in-date (Input date) - Check-in date picker
  - ID: check-out-date (Input date) - Check-out date picker
  - ID: price-filter (Dropdown) - Filter hotels by price range
  - ID: hotels-list (Div) - List available hotels
- Context Variables:
  - hotels: List[Dict] with fields: hotel_id (int), name (str), city (str), rating (float), price_per_night (float), amenities (str), category (str)
- Navigation: None specific

### 6. templates/transportation.html
- Page Title: Book Flights
- Elements:
  - ID: transportation-page (Div) - Container
  - ID: departure-city (Input) - Departure city input
  - ID: arrival-city (Input) - Arrival city input
  - ID: departure-date (Input date) - Departure date picker
  - ID: flight-class-filter (Dropdown) - Filter flights by class
  - ID: available-flights (Div) - List available flights
- Context Variables:
  - flights: List[Dict] with fields: flight_id (int), airline (str), departure_city (str), arrival_city (str), departure_time (str), arrival_time (str), price (float), class_type (str), duration (str)
- Navigation: None specific

### 7. templates/packages.html
- Page Title: Travel Packages
- Elements:
  - ID: packages-page (Div) - Container
  - ID: packages-grid (Div) - Grid of package cards
  - ID: duration-filter (Dropdown) - Filter by duration
  - ID: view-package-details-button-{{ pkg.package_id }} (Button) - View package details
  - ID: book-package-button-{{ pkg.package_id }} (Button) - Book package
- Context Variables:
  - packages: List[Dict] with fields: package_id (int), package_name (str), destination (str), duration_days (int), price (float), included_items (str)
- Navigation:
  - view-package-details-button-{{ pkg.package_id }}: url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }}: url_for('book_package', pkg_id=pkg.package_id)

### 8. templates/trips.html
- Page Title: My Trips
- Elements:
  - ID: trips-page (Div) - Container
  - ID: trips-table (Table) - Table listing trips
  - ID: view-trip-details-button-{{ trip.trip_id }} (Button) - View trip details
  - ID: edit-trip-button-{{ trip.trip_id }} (Button) - Edit trip
  - ID: delete-trip-button-{{ trip.trip_id }} (Button) - Delete trip
- Context Variables:
  - trips: List[Dict] with fields: trip_id (int), trip_name (str), destination (str), start_date (str), end_date (str), status (str)
- Navigation:
  - view-trip-details-button-{{ trip.trip_id }}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }}: url_for('delete_trip', trip_id=trip.trip_id)

### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Elements:
  - ID: confirmation-page (Div) - Container
  - ID: confirmation-number (Div) - Booking confirmation number display
  - ID: booking-details (Div) - Booking details display
  - ID: download-itinerary-button (Button) - Download itinerary as PDF
  - ID: share-trip-button (Button) - Share trip details
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - booking: Dict with fields: confirmation_number (str), booking_details (str)
- Navigation:
  - download-itinerary-button: triggers PDF download
  - share-trip-button: triggers sharing
  - back-to-dashboard: url_for('dashboard')

### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Elements:
  - ID: recommendations-page (Div) - Container
  - ID: trending-destinations (Div) - Displays trending destinations ranked
  - ID: recommendation-season-filter (Dropdown) - Filter by travel season
  - ID: budget-filter (Dropdown) - Filter by budget
  - ID: back-to-dashboard (Button) - Navigate to dashboard
- Context Variables:
  - trending_destinations: List[Dict] with fields: dest_id (int), name (str), popularity_rank (int)
  - filters: Dict with keys: season (str), budget (str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

1. Data File: data/destinations.txt
- Fields: dest_id|name|country|region|description|attractions|climate
- Description: Stores travel destination data including name, region, description, and attractions.
- Example Rows:
  - 1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  - 2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  - 3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
- Note: No header row.

2. Data File: data/itineraries.txt
- Fields: itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Stores planned itineraries with activities and statuses.
- Example Rows:
  - 1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  - 2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  - 3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
- Note: No header row.

3. Data File: data/hotels.txt
- Fields: hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Stores hotel information including amenities and rating.
- Example Rows:
  - 1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  - 2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  - 3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
- Note: No header row.

4. Data File: data/flights.txt
- Fields: flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flight details including times, price, and class
- Example Rows:
  - 1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  - 2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  - 3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
- Note: No header row.

5. Data File: data/packages.txt
- Fields: package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Stores travel packages with durations and included items.
- Example Rows:
  - 1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  - 2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  - 3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
- Note: No header row.

6. Data File: data/trips.txt
- Fields: trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: Stores all created trip data with budgets and statuses.
- Example Rows:
  - 1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  - 2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  - 3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
- Note: No header row.

7. Data File: data/bookings.txt
- Fields: booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Stores booking records associated with trips.
- Example Rows:
  - 1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  - 2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  - 3|3|Package|2025-01-12|1800.00|CONF003|Pending
- Note: No header row.

---

End of Design Specification.
