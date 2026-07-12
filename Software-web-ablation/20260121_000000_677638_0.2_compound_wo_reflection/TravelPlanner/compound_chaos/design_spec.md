# TravelPlanner Design Specification

---

## Section 1: Flask Routes Specification

| Page | Endpoint URL | HTTP Methods | Function Name | HTML Template | Context Variables | Navigation Mappings |
|-------|--------------|--------------|---------------|---------------|-------------------|---------------------|

### 1. Dashboard Page
- **Endpoint URL**: `/dashboard`
- **HTTP Methods**: GET
- **Function Name**: `dashboard_page`
- **HTML Template**: `templates/dashboard.html`
- **Context Variables**:
  - `featured_destinations`: List[Dict[str, str]]
    - Example: [{"dest_id": 1, "name": "Paris", "country": "France"}, {"dest_id": 2, "name": "Tokyo", "country": "Japan"}]
  - `upcoming_trips`: List[Dict[str, str]]
    - Example: [{"trip_id": 1, "trip_name": "Summer Vacation 2025", "start_date": "2025-06-01"}]
- **Navigation Mappings**:
  - Button `browse-destinations-button` navigates to `url_for('destinations_page')`
  - Button `plan-itinerary-button` navigates to `url_for('itinerary_planning_page')`

### 2. Destinations Page
- **Endpoint URL**: `/destinations`
- **HTTP Methods**: GET, POST (POST for search/filter submission)
- **Function Name**: `destinations_page`
- **HTML Template**: `templates/destinations.html`
- **Context Variables**:
  - `destinations`: List[Dict[str, Any]]
    - Example: [{"dest_id": 1, "name": "Paris", "country": "France", "region": "Europe"}, {"dest_id": 2, "name": "Tokyo", "country": "Japan", "region": "Asia"}]
  - `selected_region`: str
    - Example: "Europe"
  - `search_query`: str
    - Example: "Par"
- **Navigation Mappings**:
  - For each button `view-destination-button-{{ dest.dest_id }}` navigates to `url_for('destination_details_page', dest_id=dest.dest_id)`

### 3. Destination Details Page
- **Endpoint URL**: `/destinations/<int:dest_id>`
- **HTTP Methods**: GET, POST (POST for add to trip action)
- **Function Name**: `destination_details_page`
- **HTML Template**: `templates/destination_details.html`
- **Context Variables**:
  - `destination`: Dict[str, Any]
    - Example: {"dest_id": 1, "name": "Paris", "country": "France", "description": "City of lights and romance with world-class museums", "attractions": "Eiffel Tower, Louvre Museum, Notre-Dame"}
- **Navigation Mappings**:
  - Button `add-to-trip-button` submits POST to add destination to trip

### 4. Itinerary Planning Page
- **Endpoint URL**: `/itinerary`
- **HTTP Methods**: GET, POST (POST for creating/editing itinerary)
- **Function Name**: `itinerary_planning_page`
- **HTML Template**: `templates/itinerary.html`
- **Context Variables**:
  - `itineraries`: List[Dict[str, Any]]
    - Example: [{"itinerary_id": 1, "itinerary_name": "Paris Spring Break", "start_date": "2025-03-20", "end_date": "2025-03-27", "status": "Planned"}]
- **Navigation Mappings**:
  - Button `add-activity-button` triggers adding activity functionality (handled client/server)

### 5. Accommodations Page
- **Endpoint URL**: `/accommodations`
- **HTTP Methods**: GET, POST (POST for search/filter)
- **Function Name**: `accommodations_page`
- **HTML Template**: `templates/accommodations.html`
- **Context Variables**:
  - `hotels`: List[Dict[str, Any]]
    - Example: [{"hotel_id":1,"name":"Ritz Paris","city":"Paris","rating":5.0,"price_per_night":450.00,"amenities":"WiFi, Spa, Restaurant, Pool","category":"Luxury"}]
  - `search_destination`: str
    - Example: "Paris"
  - `check_in_date`: str (date in 'YYYY-MM-DD')
    - Example: "2025-06-01"
  - `check_out_date`: str (date in 'YYYY-MM-DD')
    - Example: "2025-06-10"
  - `selected_price_filter`: str
    - Example: "Mid-range"
- **Navigation Mappings**:
  - Hotels are displayed for browsing; no direct navigation buttons specified.

### 6. Transportation Page
- **Endpoint URL**: `/transportation`
- **HTTP Methods**: GET, POST (POST for searching flights)
- **Function Name**: `transportation_page`
- **HTML Template**: `templates/transportation.html`
- **Context Variables**:
  - `available_flights`: List[Dict[str, Any]]
    - Example: [{"flight_id":1,"airline":"Air France","departure_city":"New York","arrival_city":"Paris","departure_time":"10:00","arrival_time":"22:30","price":850.00,"class_type":"Economy"}]
  - `departure_city`: str
    - Example: "New York"
  - `arrival_city`: str
    - Example: "Paris"
  - `departure_date`: str (date in 'YYYY-MM-DD')
    - Example: "2025-06-01"
  - `selected_class_filter`: str
    - Example: "Economy"
- **Navigation Mappings**:
  - Flights displayed; no direct navigation buttons specified.

### 7. Travel Packages Page
- **Endpoint URL**: `/packages`
- **HTTP Methods**: GET
- **Function Name**: `travel_packages_page`
- **HTML Template**: `templates/packages.html`
- **Context Variables**:
  - `packages`: List[Dict[str, Any]]
    - Example: [{"package_id":1,"package_name":"Paris Classic Tour","destination":"Paris","duration_days":5,"price":1500.00}]
  - `selected_duration_filter`: str
    - Example: "3-5 days"
- **Navigation Mappings**:
  - Button `view-package-details-button-{{ pkg.package_id }}` navigates to `url_for('package_details_page', pkg_id=pkg.package_id)`
  - Button `book-package-button-{{ pkg.package_id }}` navigates to `url_for('book_package', pkg_id=pkg.package_id)`

### 8. Trip Management Page
- **Endpoint URL**: `/trips`
- **HTTP Methods**: GET, POST (POST for edit/delete actions)
- **Function Name**: `trip_management_page`
- **HTML Template**: `templates/trips.html`
- **Context Variables**:
  - `trips`: List[Dict[str, Any]]
    - Example: [{"trip_id":1,"trip_name":"Summer Vacation 2025","destination":"Paris","start_date":"2025-06-01","end_date":"2025-06-15","status":"Booked"}]
- **Navigation Mappings**:
  - Button `view-trip-details-button-{{ trip.trip_id }}` navigates to `url_for('trip_details_page', trip_id=trip.trip_id)`
  - Button `edit-trip-button-{{ trip.trip_id }}` navigates to `url_for('edit_trip', trip_id=trip.trip_id)`
  - Button `delete-trip-button-{{ trip.trip_id }}` submits POST for deletion

### 9. Booking Confirmation Page
- **Endpoint URL**: `/booking-confirmation/<int:booking_id>`
- **HTTP Methods**: GET
- **Function Name**: `booking_confirmation_page`
- **HTML Template**: `templates/booking_confirmation.html`
- **Context Variables**:
  - `booking`: Dict[str, Any]
    - Example: {"booking_id":1,"confirmation_number":"CONF001","booking_date":"2025-01-10","amount":750.00,"details":"Hotel booking at Ritz Paris"}
- **Navigation Mappings**:
  - Button `download-itinerary-button` triggers itinerary PDF download
  - Button `share-trip-button` triggers sharing functionality
  - Button `back-to-dashboard` navigates to `url_for('dashboard_page')`

### 10. Travel Recommendations Page
- **Endpoint URL**: `/recommendations`
- **HTTP Methods**: GET, POST (POST for filters)
- **Function Name**: `travel_recommendations_page`
- **HTML Template**: `templates/recommendations.html`
- **Context Variables**:
  - `trending_destinations`: List[Dict[str, Any]]
    - Example: [{"dest_id":1,"name":"Paris","popularity_rank":1}]
  - `selected_season_filter`: str
    - Example: "Summer"
  - `selected_budget_filter`: str
    - Example: "Medium"
- **Navigation Mappings**:
  - Button `back-to-dashboard` navigates to `url_for('dashboard_page')`

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title**: Travel Planner Dashboard
- **Main Heading**: Travel Planner Dashboard
- **Element IDs and Tags**:
  - `dashboard-page` (Div): Container for the dashboard page
  - `featured-destinations` (Div): Display of featured travel destinations
  - `upcoming-trips` (Div): Display of upcoming planned trips
  - `browse-destinations-button` (Button): Navigate to destinations page
  - `plan-itinerary-button` (Button): Navigate to itinerary planning page
- **Context Variables**:
  - `featured_destinations`: List[Dict[str, str]]
  - `upcoming_trips`: List[Dict[str, str]]
- **Navigation**:
  - `browse-destinations-button` uses `url_for('destinations_page')`
  - `plan-itinerary-button` uses `url_for('itinerary_planning_page')`

### 2. templates/destinations.html
- **Page Title**: Travel Destinations
- **Main Heading**: Travel Destinations
- **Element IDs and Tags**:
  - `destinations-page` (Div): Container for destinations page
  - `search-destination` (Input): Search field for destinations
  - `region-filter` (Dropdown): Filter by region
  - `destinations-grid` (Div): Grid displaying destination cards
  - `view-destination-button-{{ dest.dest_id }}` (Button): View details for each destination
- **Context Variables**:
  - `destinations`: List[Dict[str, Any]] (dest_id, name, country, region)
  - `selected_region`: str
  - `search_query`: str
- **Navigation**:
  - Each `view-destination-button-{{ dest.dest_id }}` navigates to `url_for('destination_details_page', dest_id=dest.dest_id)`

### 3. templates/destination_details.html
- **Page Title**: Destination Details
- **Main Heading**: Destination Details
- **Element IDs and Tags**:
  - `destination-details-page` (Div): Container
  - `destination-name` (H1): Destination name
  - `destination-country` (Div): Destination country
  - `destination-description` (Div): Detailed description
  - `add-to-trip-button` (Button): Add destination to trip
  - `destination-attractions` (Div): Attractions and activities
- **Context Variables**:
  - `destination`: Dict with keys dest_id, name, country, description, attractions
- **Navigation**:
  - `add-to-trip-button` triggers POST to add destination to trip

### 4. templates/itinerary.html
- **Page Title**: Plan Your Itinerary
- **Main Heading**: Plan Your Itinerary
- **Element IDs and Tags**:
  - `itinerary-page` (Div): Container
  - `itinerary-name-input` (Input): Input for itinerary name
  - `start-date-input` (Input date): Start date
  - `end-date-input` (Input date): End date
  - `add-activity-button` (Button): Add activity
  - `itinerary-list` (Div): List of itineraries
- **Context Variables**:
  - `itineraries`: List of dicts with keys itinerary_id, itinerary_name, start_date, end_date, status
- **Navigation**:
  - `add-activity-button` triggers adding activity feature

### 5. templates/accommodations.html
- **Page Title**: Search Accommodations
- **Main Heading**: Search Accommodations
- **Element IDs and Tags**:
  - `accommodations-page` (Div): Container
  - `destination-input` (Input): Destination city
  - `check-in-date` (Input date): Check-in
  - `check-out-date` (Input date): Check-out
  - `price-filter` (Dropdown): Price range
  - `hotels-list` (Div): List of hotels
- **Context Variables**:
  - `hotels`: List with hotel data
  - `search_destination`: str
  - `check_in_date`: str
  - `check_out_date`: str
  - `selected_price_filter`: str
- **Navigation**:
  - Hotel listings do not have navigation buttons

### 6. templates/transportation.html
- **Page Title**: Book Flights
- **Main Heading**: Book Flights
- **Element IDs and Tags**:
  - `transportation-page` (Div): Container
  - `departure-city` (Input): Departure city
  - `arrival-city` (Input): Arrival city
  - `departure-date` (Input date): Departure date
  - `flight-class-filter` (Dropdown): Flight class
  - `available-flights` (Div): List of flights
- **Context Variables**:
  - `available_flights`: List with flight data
  - `departure_city`: str
  - `arrival_city`: str
  - `departure_date`: str
  - `selected_class_filter`: str
- **Navigation**:
  - Flights do not have direct navigation buttons

### 7. templates/packages.html
- **Page Title**: Travel Packages
- **Main Heading**: Travel Packages
- **Element IDs and Tags**:
  - `packages-page` (Div): Container
  - `packages-grid` (Div): Grid of packages
  - `duration-filter` (Dropdown): Filter by duration
  - `view-package-details-button-{{ pkg.package_id }}` (Button): View package details
  - `book-package-button-{{ pkg.package_id }}` (Button): Book package
- **Context Variables**:
  - `packages`: List with package data
  - `selected_duration_filter`: str
- **Navigation**:
  - `view-package-details-button-{{ pkg.package_id }}` to `url_for('package_details_page', pkg_id=pkg.package_id)`
  - `book-package-button-{{ pkg.package_id }}` to `url_for('book_package', pkg_id=pkg.package_id)`

### 8. templates/trips.html
- **Page Title**: My Trips
- **Main Heading**: My Trips
- **Element IDs and Tags**:
  - `trips-page` (Div): Container
  - `trips-table` (Table): Table with all trips
  - `view-trip-details-button-{{ trip.trip_id }}` (Button): View trip details
  - `edit-trip-button-{{ trip.trip_id }}` (Button): Edit trip
  - `delete-trip-button-{{ trip.trip_id }}` (Button): Delete trip
- **Context Variables**:
  - `trips`: List with trip data
- **Navigation**:
  - `view-trip-details-button-{{ trip.trip_id }}` to `url_for('trip_details_page', trip_id=trip.trip_id)`
  - `edit-trip-button-{{ trip.trip_id }}` to `url_for('edit_trip', trip_id=trip.trip_id)`
  - `delete-trip-button-{{ trip.trip_id }}` submits POST for deletion

### 9. templates/booking_confirmation.html
- **Page Title**: Booking Confirmation
- **Main Heading**: Booking Confirmation
- **Element IDs and Tags**:
  - `confirmation-page` (Div): Container
  - `confirmation-number` (Div): Display confirmation number
  - `booking-details` (Div): Booking information
  - `download-itinerary-button` (Button): Download itinerary PDF
  - `share-trip-button` (Button): Share trip details
  - `back-to-dashboard` (Button): Back to dashboard
- **Context Variables**:
  - `booking`: Dict with booking data
- **Navigation**:
  - `download-itinerary-button` triggers itinerary PDF download
  - `share-trip-button` triggers sharing
  - `back-to-dashboard` uses `url_for('dashboard_page')`

### 10. templates/recommendations.html
- **Page Title**: Travel Recommendations
- **Main Heading**: Travel Recommendations
- **Element IDs and Tags**:
  - `recommendations-page` (Div): Container
  - `trending-destinations` (Div): Trending destinations
  - `recommendation-season-filter` (Dropdown): Filter by season
  - `budget-filter` (Dropdown): Filter by budget
  - `back-to-dashboard` (Button): Back to dashboard
- **Context Variables**:
  - `trending_destinations`: List with trending destination data
  - `selected_season_filter`: str
  - `selected_budget_filter`: str
- **Navigation**:
  - `back-to-dashboard` uses `url_for('dashboard_page')`

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- **Fields (pipe-delimited)**:
  - dest_id|name|country|region|description|attractions|climate
- **Description**: Stores travel destination data
- **Example Rows**:
  - 1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  - 2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  - 3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
- **Note**: File does NOT contain header row

### 2. data/itineraries.txt
- **Fields (pipe-delimited)**:
  - itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- **Description**: Stores itinerary information
- **Example Rows**:
  - 1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  - 2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  - 3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
- **Note**: File does NOT contain header row

### 3. data/hotels.txt
- **Fields (pipe-delimited)**:
  - hotel_id|name|city|rating|price_per_night|amenities|category
- **Description**: Stores hotel data
- **Example Rows**:
  - 1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  - 2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  - 3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
- **Note**: File does NOT contain header row

### 4. data/flights.txt
- **Fields (pipe-delimited)**:
  - flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- **Description**: Stores flight data
- **Example Rows**:
  - 1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  - 2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  - 3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
- **Note**: File does NOT contain header row

### 5. data/packages.txt
- **Fields (pipe-delimited)**:
  - package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- **Description**: Stores travel package details
- **Example Rows**:
  - 1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  - 2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  - 3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
- **Note**: File does NOT contain header row

### 6. data/trips.txt
- **Fields (pipe-delimited)**:
  - trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- **Description**: Stores trips data
- **Example Rows**:
  - 1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  - 2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  - 3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
- **Note**: File does NOT contain header row

### 7. data/bookings.txt
- **Fields (pipe-delimited)**:
  - booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- **Description**: Stores booking information
- **Example Rows**:
  - 1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  - 2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  - 3|3|Package|2025-01-12|1800.00|CONF003|Pending
- **Note**: File does NOT contain header row
