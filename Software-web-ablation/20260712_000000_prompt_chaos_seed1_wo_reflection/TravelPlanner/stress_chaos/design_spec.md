# TravelPlanner Application - Design Specifications

---

## Section 1: Flask Routes Specification

| Route Endpoint                  | HTTP Methods | Function Name                 | Template File               | Context Variables                                | Navigation Actions / Button Link Mappings                        |
|--------------------------------|--------------|-------------------------------|-----------------------------|-------------------------------------------------|------------------------------------------------------------------|
| /                              | GET          | dashboard                    | dashboard.html              | featured_destinations: List[dict] with fields: dest_id (int), name (str), country (str)
upcoming_trips: List[dict] with fields: trip_id (int), trip_name (str), start_date (str), end_date (str)
| "browse-destinations-button": url_for('destinations')
"plan-itinerary-button": url_for('itinerary')
"back-to-dashboard" buttons (multiple pages): url_for('dashboard')                                      |
| /destinations                  | GET          | destinations                 | destinations.html           | destinations: List[dict] with fields: dest_id (int), name (str), country (str), region (str)
| "view-destination-button-{dest_id}": url_for('destination_details', dest_id=dest_id)                                                              |
| /destinations/<int:dest_id>   | GET, POST    | destination_details          | destination_details.html    | destination: dict with fields: dest_id (int), name (str), country (str), description (str), attractions (str)
| "add-to-trip-button": Posts to add destination to trip (handled by route)
| /itinerary                    | GET, POST    | itinerary                   | itinerary.html              | itineraries: List[dict] with fields: itinerary_id (int), itinerary_name (str), destination (str), start_date (str), end_date (str), activities (str), status (str)
| "add-activity-button": JS triggered form/post to add activity
| /accommodations               | GET          | accommodations              | accommodations.html         | hotels: List[dict] with fields: hotel_id (int), name (str), city (str), rating (float), price_per_night (float), amenities (str), category (str)
| /transportation              | GET          | transportation              | transportation.html         | flights: List[dict] with fields: flight_id (int), airline (str), departure_city (str), arrival_city (str), departure_time (str), arrival_time (str), price (float), class_type (str), duration (str)
| /packages                    | GET          | travel_packages             | packages.html               | packages: List[dict] with fields: package_id (int), package_name (str), destination (str), duration_days (int), price (float), included_items (str), difficulty_level (str)
| "view-package-details-button-{pkg_id}": url_for('package_details', pkg_id=pkg_id)
"book-package-button-{pkg_id}": posts booking (or leads to booking confirmation) |
| /trips                      | GET          | trips                      | trips.html                  | trips: List[dict] with fields: trip_id (int), trip_name (str), destination (str), start_date (str), end_date (str), status (str)
| "view-trip-details-button-{trip_id}": url_for('trip_details', trip_id=trip_id)
"edit-trip-button-{trip_id}": url_for('edit_trip', trip_id=trip_id)
"delete-trip-button-{trip_id}": posts delete request to same or separate route |
| /booking_confirmation       | GET          | booking_confirmation       | booking_confirmation.html   | booking: dict with fields: booking_id (int), trip_id (int), booking_type (str), booking_date (str), amount (float), confirmation_number (str), status (str)
| "download-itinerary-button": triggers file download (PDF generation handled separately)
"share-trip-button": JS or external link share feature
"back-to-dashboard": url_for('dashboard') |
| /recommendations             | GET          | recommendations             | recommendations.html        | recommendations: List[dict], trending_destinations: List[dict] with dest_id, name, popularity rank
| "back-to-dashboard": url_for('dashboard')                                                                                                      |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page: Div - Container div for dashboard page
  - featured-destinations: Div - Displays featured travel destinations
  - upcoming-trips: Div - Displays upcoming trips
  - browse-destinations-button: Button - Navigates to /destinations
  - plan-itinerary-button: Button - Navigates to /itinerary
- Context Variables:
  - featured_destinations: List[dict] with fields: dest_id (int), name (str), country (str)
  - upcoming_trips: List[dict] with fields: trip_id (int), trip_name (str), start_date (str), end_date (str)
- Navigation:
  - browse-destinations-button uses url_for('destinations')
  - plan-itinerary-button uses url_for('itinerary')

### 2. Destinations Page
- Filename: templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page: Div - Main container
  - search-destination: Input (text) - Search filter
  - region-filter: Select (dropdown) - Region filter options [Asia, Europe, Americas, Africa, Oceania]
  - destinations-grid: Div - Displays destination cards
  - view-destination-button-{{ dest.dest_id }}: Button - View destination details
- Context Variables:
  - destinations: List[dict] with fields: dest_id (int), name (str), country (str), region (str)
- Navigation:
  - view-destination-button-{{ dest.dest_id }} uses url_for('destination_details', dest_id=dest.dest_id)

### 3. Destination Details Page
- Filename: templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page: Div - Container
  - destination-name: H1 - Destination name
  - destination-country: Div - Destination country
  - destination-description: Div - Description
  - add-to-trip-button: Button - Adds destination to trip
  - destination-attractions: Div - Attractions and activities
- Context Variables:
  - destination: dict with fields: dest_id (int), name (str), country (str), description (str), attractions (str)
- Navigation:
  - add-to-trip-button posts to current route or specified route

### 4. Itinerary Planning Page
- Filename: templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page: Div - Container
  - itinerary-name-input: Input (text) - Itinerary name
  - start-date-input: Input (date) - Start date
  - end-date-input: Input (date) - End date
  - add-activity-button: Button - Adds activity
  - itinerary-list: Div - List of itineraries with edit/delete options
- Context Variables:
  - itineraries: List[dict] with fields: itinerary_id (int), itinerary_name (str), destination (str), start_date (str), end_date (str), activities (str), status (str)
- Navigation:
  - add-activity-button: Posts or triggers form submit

### 5. Accommodations Page
- Filename: templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page: Div - Container
  - destination-input: Input (text) - Destination city
  - check-in-date: Input (date) - Check-in
  - check-out-date: Input (date) - Check-out
  - price-filter: Select (dropdown) - Price range filter [Budget, Mid-range, Luxury]
  - hotels-list: Div - List of hotels
- Context Variables:
  - hotels: List[dict] with fields: hotel_id (int), name (str), city (str), rating (float), price_per_night (float), amenities (str), category (str)

### 6. Transportation Page
- Filename: templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page: Div - Container
  - departure-city: Input (text) - Departure city
  - arrival-city: Input (text) - Arrival city
  - departure-date: Input (date) - Departure date
  - flight-class-filter: Select (dropdown) - Flight class filter [Economy, Business, First Class]
  - available-flights: Div - List of flights
- Context Variables:
  - flights: List[dict] with fields: flight_id (int), airline (str), departure_city (str), arrival_city (str), departure_time (str), arrival_time (str), price (float), class_type (str), duration (str)

### 7. Travel Packages Page
- Filename: templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page: Div - Container
  - packages-grid: Div - Grid of package cards
  - duration-filter: Select (dropdown) - Duration filter [3-5 days, 7-10 days, 14+ days]
  - view-package-details-button-{{ pkg.package_id }}: Button - View package details
  - book-package-button-{{ pkg.package_id }}: Button - Book package
- Context Variables:
  - packages: List[dict] with fields: package_id (int), package_name (str), destination (str), duration_days (int), price (float), included_items (str), difficulty_level (str)
- Navigation:
  - view-package-details-button-{{ pkg.package_id }} uses url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{ pkg.package_id }} posts or navigates to booking confirmation

### 8. Trip Management Page
- Filename: templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page: Div - Container
  - trips-table: Table - Displays trips
  - view-trip-details-button-{{ trip.trip_id }}: Button - View trip details
  - edit-trip-button-{{ trip.trip_id }}: Button - Edit trip
  - delete-trip-button-{{ trip.trip_id }}: Button - Delete trip
- Context Variables:
  - trips: List[dict] with fields: trip_id (int), trip_name (str), destination (str), start_date (str), end_date (str), status (str)
- Navigation:
  - view-trip-details-button-{{ trip.trip_id }} uses url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{ trip.trip_id }} uses url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{ trip.trip_id }} posts to route handling deletion

### 9. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page: Div - Container
  - confirmation-number: Div - Booking confirmation number
  - booking-details: Div - Booking details (dates, amounts, locations)
  - download-itinerary-button: Button - Downloads itinerary PDF
  - share-trip-button: Button - Shares trip details
  - back-to-dashboard: Button - Goes back to dashboard
- Context Variables:
  - booking: dict with fields: booking_id (int), trip_id (int), booking_type (str), booking_date (str), amount (float), confirmation_number (str), status (str)
- Navigation:
  - back-to-dashboard uses url_for('dashboard')

### 10. Travel Recommendations Page
- Filename: templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page: Div - Container
  - trending-destinations: Div - Trending destinations by popularity
  - recommendation-season-filter: Select (dropdown) - Season filter [Spring, Summer, Fall, Winter]
  - budget-filter: Select (dropdown) - Budget filter [Low, Medium, High]
  - back-to-dashboard: Button - Navigates back to dashboard
- Context Variables:
  - recommendations: List[dict] (personalized recommendations representation)
  - trending_destinations: List[dict] with dest_id (int), name (str), popularity rank (int)
- Navigation:
  - back-to-dashboard uses url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Destinations Data
- Path: data/destinations.txt
- Fields (pipe-delimited, no header):
  dest_id|name|country|region|description|attractions|climate
- Description: Stores available travel destinations with details.
- Example Rows:
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical

### 2. Itineraries Data
- Path: data/itineraries.txt
- Fields (pipe-delimited, no header):
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: Stores user-created itineraries.
- Example Rows:
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned

### 3. Hotels Data
- Path: data/hotels.txt
- Fields (pipe-delimited, no header):
  hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Stores hotel data with ratings and amenities.
- Example Rows:
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range

### 4. Flights Data
- Path: data/flights.txt
- Fields (pipe-delimited, no header):
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Stores flights information for booking.
- Example Rows:
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes

### 5. Travel Packages Data
- Path: data/packages.txt
- Fields (pipe-delimited, no header):
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Stores pre-designed travel packages.
- Example Rows:
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate

### 6. Trips Data
- Path: data/trips.txt
- Fields (pipe-delimited, no header):
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: Stores user trips and overall info.
- Example Rows:
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12

### 7. Bookings Data
- Path: data/bookings.txt
- Fields (pipe-delimited, no header):
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Stores booking confirmations with status.
- Example Rows:
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending

---

End of design_spec.md
