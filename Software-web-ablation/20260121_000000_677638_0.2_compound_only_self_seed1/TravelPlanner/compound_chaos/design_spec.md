# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route Endpoint:** `/dashboard`
- **Allowed HTTP Methods:** GET
- **Function Name:** `dashboard`
- **Template Filename:** `templates/dashboard.html`
- **Context Variables:**
  - `featured_destinations`: List[Dict] (Example: `[{'dest_id':1, 'name':'Paris', 'country':'France'}, ...]`)
  - `upcoming_trips`: List[Dict] (Example: `[{'trip_id':1, 'trip_name':'Summer Vacation', 'destination':'Paris', 'start_date':'2025-06-01'}, ...]`)
- **Navigation Actions:**
  - `browse-destinations-button` → `url_for('destinations')`
  - `plan-itinerary-button` → `url_for('itinerary_planning')`

### 2. Destinations Page
- **Route Endpoint:** `/destinations`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `destinations`
- **Template Filename:** `templates/destinations.html`
- **Context Variables:**
  - `destinations`: List[Dict] (Example: `[{'dest_id':1, 'name':'Paris', 'country':'France', 'region':'Europe'}, ...]`)
- **Navigation Actions:**
  - `view-destination-button-{dest_id}` → `url_for('destination_details', dest_id=dest_id)`

### 3. Destination Details Page
- **Route Endpoint:** `/destinations/<int:dest_id>`
- **Allowed HTTP Methods:** GET
- **Function Name:** `destination_details`
- **Template Filename:** `templates/destination_details.html`
- **Context Variables:**
  - `destination`: Dict (Example: `{'name':'Paris','country':'France','description':'City of lights...','attractions':'Eiffel Tower, Louvre Museum'}`)
- **Navigation Actions:**
  - `add-to-trip-button` → `url_for('itinerary_planning')`

### 4. Itinerary Planning Page
- **Route Endpoint:** `/itinerary`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `itinerary_planning`
- **Template Filename:** `templates/itinerary_planning.html`
- **Context Variables:**
  - `itineraries`: List[Dict] (Example: `[{'itinerary_id':1, 'itinerary_name':'Paris Spring Break', 'destination':'Paris', 'start_date':'2025-03-20', 'end_date':'2025-03-27', 'activities':'Museum tours, River cruise, Cafe hopping', 'status':'Planned'}, ...]`)
- **Navigation Actions:**
  - `add-activity-button` triggers adding an activity (server or client handled)
  - Edit/delete actions handled on the same page via UI

### 5. Accommodations Page
- **Route Endpoint:** `/accommodations`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `accommodations`
- **Template Filename:** `templates/accommodations.html`
- **Context Variables:**
  - `hotels`: List[Dict] (Example: `[{'hotel_id':1, 'name':'Ritz Paris', 'city':'Paris', 'rating':5.0, 'price_per_night':450.00, 'amenities':'WiFi, Spa', 'category':'Luxury'}, ...]`)
- **Navigation Actions:**
  - Filtering and search reload page; no direct navigation

### 6. Transportation Page
- **Route Endpoint:** `/transportation`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `transportation`
- **Template Filename:** `templates/transportation.html`
- **Context Variables:**
  - `flights`: List[Dict] (Example: `[{'flight_id':1, 'airline':'Air France', 'departure_city':'New York', 'arrival_city':'Paris', 'departure_time':'10:00', 'arrival_time':'22:30', 'price':850.00, 'class_type':'Economy', 'duration':'7 hours 30 minutes'}, ...]`)
- **Navigation Actions:**
  - Filtering triggers page reload; no direct navigation

### 7. Travel Packages Page
- **Route Endpoint:** `/packages`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `travel_packages`
- **Template Filename:** `templates/packages.html`
- **Context Variables:**
  - `packages`: List[Dict] (Example: `[{'package_id':1, 'package_name':'Paris Classic Tour', 'destination':'Paris', 'duration_days':5, 'price':1500.00, 'included_items':'Hotel, Flights', 'difficulty_level':'Easy'}, ...]`)
- **Navigation Actions:**
  - `view-package-details-button-{pkg_id}` → `url_for('package_details', pkg_id=pkg_id)` (assumed page)
  - `book-package-button-{pkg_id}` triggers booking process (client/JS handled)

### 8. Trip Management Page
- **Route Endpoint:** `/trips`
- **Allowed HTTP Methods:** GET
- **Function Name:** `trip_management`
- **Template Filename:** `templates/trips.html`
- **Context Variables:**
  - `trips`: List[Dict] (Example: `[{'trip_id':1, 'trip_name':'Summer Vacation', 'destination':'Paris', 'start_date':'2025-06-01', 'end_date':'2025-06-15', 'status':'Booked'}, ...]`)
- **Navigation Actions:**
  - `view-trip-details-button-{trip_id}` → `url_for('trip_details', trip_id=trip_id)` (assumed page)
  - `edit-trip-button-{trip_id}` → `url_for('edit_trip', trip_id=trip_id)` (assumed page)
  - `delete-trip-button-{trip_id}` triggers deletion (POST/ajax), no explicit route

### 9. Booking Confirmation Page
- **Route Endpoint:** `/booking-confirmation`
- **Allowed HTTP Methods:** GET
- **Function Name:** `booking_confirmation`
- **Template Filename:** `templates/booking_confirmation.html`
- **Context Variables:**
  - `booking_info`: Dict (Example: `{'confirmation_number':'CONF001', 'booking_details':'Hotel booked from 2025-06-01 to 2025-06-15'}`)
- **Navigation Actions:**
  - `download-itinerary-button` triggers PDF download (frontend handled)
  - `share-trip-button` triggers sharing UI (frontend handled)
  - `back-to-dashboard` → `url_for('dashboard')`

### 10. Travel Recommendations Page
- **Route Endpoint:** `/recommendations`
- **Allowed HTTP Methods:** GET, POST
- **Function Name:** `travel_recommendations`
- **Template Filename:** `templates/recommendations.html`
- **Context Variables:**
  - `recommendations`: List[Dict] (structure unspecified)
  - `trending_destinations`: List[Dict] (Example: `[{'dest_id':1, 'name':'Paris', 'popularity':95}, ...]`)
- **Navigation Actions:**
  - `back-to-dashboard` → `url_for('dashboard')`

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Travel Planner Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-destinations` (Div): Featured destinations display
  - `upcoming-trips` (Div): Upcoming trips display
  - `browse-destinations-button` (Button): Navigate to destinations page
  - `plan-itinerary-button` (Button): Navigate to itinerary page
- **Context Variables:**
  - `featured_destinations`, `upcoming_trips` as described
- **Navigation Mappings:**
  - `browse-destinations-button`: `url_for('destinations')`
  - `plan-itinerary-button`: `url_for('itinerary_planning')`

### 2. templates/destinations.html
- **Page Title:** Travel Destinations
- **Element IDs:**
  - `destinations-page` (Div): Container
  - `search-destination` (Input): Search field
  - `region-filter` (Dropdown): Filter dropdown
  - `destinations-grid` (Div): Grid of destination cards
  - `view-destination-button-{{ dest.dest_id }}` (Button): View details button per destination
- **Context Variables:**
  - `destinations` list
- **Navigation Mappings:**
  - `view-destination-button-{{ dest.dest_id }}`: `url_for('destination_details', dest_id=dest.dest_id)`

### 3. templates/destination_details.html
- **Page Title:** Destination Details
- **Element IDs:**
  - `destination-details-page` (Div): Container
  - `destination-name` (H1): Destination name
  - `destination-country` (Div): Country
  - `destination-description` (Div): Full description
  - `add-to-trip-button` (Button): Add to trip
  - `destination-attractions` (Div): Attractions
- **Context Variables:**
  - `destination` dict
- **Navigation Mappings:**
  - `add-to-trip-button`: `url_for('itinerary_planning')`

### 4. templates/itinerary_planning.html
- **Page Title:** Plan Your Itinerary
- **Element IDs:**
  - `itinerary-page` (Div): Container
  - `itinerary-name-input` (Input): Name field
  - `start-date-input` (Input date): Start date
  - `end-date-input` (Input date): End date
  - `add-activity-button` (Button): Add activity
  - `itinerary-list` (Div): List of itineraries
- **Context Variables:**
  - `itineraries` list
- **Navigation Mappings:**
  - Add/edit/delete handled inline or via client-side

### 5. templates/accommodations.html
- **Page Title:** Search Accommodations
- **Element IDs:**
  - `accommodations-page` (Div): Container
  - `destination-input` (Input): Destination city
  - `check-in-date` (Input date): Check-in
  - `check-out-date` (Input date): Check-out
  - `price-filter` (Dropdown): Price range
  - `hotels-list` (Div): Hotel listings
- **Context Variables:**
  - `hotels` list
- **Navigation Mappings:**
  - Filters/search trigger reload; no explicit buttons

### 6. templates/transportation.html
- **Page Title:** Book Flights
- **Element IDs:**
  - `transportation-page` (Div): Container
  - `departure-city` (Input): Departure city
  - `arrival-city` (Input): Arrival city
  - `departure-date` (Input date): Departure date
  - `flight-class-filter` (Dropdown): Flight class filter
  - `available-flights` (Div): Flights list
- **Context Variables:**
  - `flights` list
- **Navigation Mappings:**
  - Filter/search reload page

### 7. templates/packages.html
- **Page Title:** Travel Packages
- **Element IDs:**
  - `packages-page` (Div): Container
  - `packages-grid` (Div): Packages grid
  - `duration-filter` (Dropdown): Duration filter
  - `view-package-details-button-{{ pkg.package_id }}` (Button): View details
  - `book-package-button-{{ pkg.package_id }}` (Button): Book package
- **Context Variables:**
  - `packages` list
- **Navigation Mappings:**
  - `view-package-details-button-{{ pkg.package_id }}`: `url_for('package_details', pkg_id=pkg.package_id)`
  - `book-package-button-{{ pkg.package_id }}`: Booking action (frontend handled)

### 8. templates/trips.html
- **Page Title:** My Trips
- **Element IDs:**
  - `trips-page` (Div): Container
  - `trips-table` (Table): Trips table
  - `view-trip-details-button-{{ trip.trip_id }}` (Button): View trip
  - `edit-trip-button-{{ trip.trip_id }}` (Button): Edit trip
  - `delete-trip-button-{{ trip.trip_id }}` (Button): Delete trip
- **Context Variables:**
  - `trips` list
- **Navigation Mappings:**
  - `view-trip-details-button-{{ trip.trip_id }}`: `url_for('trip_details', trip_id=trip.trip_id)`
  - `edit-trip-button-{{ trip.trip_id }}`: `url_for('edit_trip', trip_id=trip.trip_id)`
  - `delete-trip-button-{{ trip.trip_id }}`: Delete action (no route)

### 9. templates/booking_confirmation.html
- **Page Title:** Booking Confirmation
- **Element IDs:**
  - `confirmation-page` (Div): Container
  - `confirmation-number` (Div): Confirmation number
  - `booking-details` (Div): Booking details
  - `download-itinerary-button` (Button): Download itinerary
  - `share-trip-button` (Button): Share trip
  - `back-to-dashboard` (Button): Back to dashboard
- **Context Variables:**
  - `booking_info` dict
- **Navigation Mappings:**
  - `back-to-dashboard`: `url_for('dashboard')`

### 10. templates/recommendations.html
- **Page Title:** Travel Recommendations
- **Element IDs:**
  - `recommendations-page` (Div): Container
  - `trending-destinations` (Div): Trending display
  - `recommendation-season-filter` (Dropdown): Season filter
  - `budget-filter` (Dropdown): Budget filter
  - `back-to-dashboard` (Button): Back to dashboard
- **Context Variables:**
  - `recommendations` list
  - `trending_destinations` list
- **Navigation Mappings:**
  - `back-to-dashboard`: `url_for('dashboard')`

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- **File Path:** `data/destinations.txt`
- **Field Names:** `dest_id|name|country|region|description|attractions|climate`
- **Description:** Stores details of travel destinations.
- **Example Rows:**
  - `1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate`
  - `2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate`
  - `3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical`
- No header row.

### 2. data/itineraries.txt
- **File Path:** `data/itineraries.txt`
- **Field Names:** `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
- **Description:** Stores planned itineraries.
- **Example Rows:**
  - `1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned`
  - `2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress`
  - `3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned`
- No header row.

### 3. data/hotels.txt
- **File Path:** `data/hotels.txt`
- **Field Names:** `hotel_id|name|city|rating|price_per_night|amenities|category`
- **Description:** Stores hotel details.
- **Example Rows:**
  - `1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury`
  - `2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range`
  - `3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range`
- No header row.

### 4. data/flights.txt
- **File Path:** `data/flights.txt`
- **Field Names:** `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
- **Description:** Stores flight information.
- **Example Rows:**
  - `1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes`
  - `2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes`
  - `3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes`
- No header row.

### 5. data/packages.txt
- **File Path:** `data/packages.txt`
- **Field Names:** `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
- **Description:** Stores travel packages.
- **Example Rows:**
  - `1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy`
  - `2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate`
  - `3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate`
- No header row.

### 6. data/trips.txt
- **File Path:** `data/trips.txt`
- **Field Names:** `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
- **Description:** Stores trip records.
- **Example Rows:**
  - `1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10`
  - `2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11`
  - `3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12`
- No header row.

### 7. data/bookings.txt
- **File Path:** `data/bookings.txt`
- **Field Names:** `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
- **Description:** Stores booking confirmations.
- **Example Rows:**
  - `1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed`
  - `2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed`
  - `3|3|Package|2025-01-12|1800.00|CONF003|Pending`
- No header row.

---

End of design_spec.md
