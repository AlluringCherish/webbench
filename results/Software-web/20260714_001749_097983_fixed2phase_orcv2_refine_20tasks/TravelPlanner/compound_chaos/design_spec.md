# TravelPlanner Web Application Design Specification

## 1. Page Specifications

### 1. Dashboard Page
- **Page Title**: Travel Planner Dashboard
- **Overview**: Main hub showing featured destinations, upcoming trips, and quick navigation buttons.
- **Container ID**: `dashboard-page` (Div)
- **UI Elements**:
  - `featured-destinations` (Div): Display featured travel destinations.
  - `upcoming-trips` (Div): Display upcoming planned trips.
  - `browse-destinations-button` (Button): Navigates to Destinations Page.
  - `plan-itinerary-button` (Button): Navigates to Itinerary Planning Page.
- **Navigation Flows**:
  - `browse-destinations-button` leads to Destinations Page.
  - `plan-itinerary-button` leads to Itinerary Planning Page.

### 2. Destinations Page
- **Page Title**: Travel Destinations
- **Overview**: Displays all destinations with search and filters.
- **Container ID**: `destinations-page` (Div)
- **UI Elements**:
  - `search-destination` (Input): Search by name or country.
  - `region-filter` (Dropdown): Filter by region (Asia, Europe, Americas, Africa, Oceania).
  - `destinations-grid` (Div): Grid showing destination cards.
  - `view-destination-button-{dest_id}` (Button): View details for destination.
- **Navigation Flows**:
  - Each `view-destination-button-{dest_id}` navigates to Destination Details Page for that destination.

### 3. Destination Details Page
- **Page Title**: Destination Details
- **Overview**: Detailed info on a selected destination.
- **Container ID**: `destination-details-page` (Div)
- **UI Elements**:
  - `destination-name` (H1): Destination name.
  - `destination-country` (Div): Destination country.
  - `destination-description` (Div): Detailed description.
  - `add-to-trip-button` (Button): Add destination to trip.
  - `destination-attractions` (Div): Attractions and activities display.
- **Navigation Flows**:
  - `add-to-trip-button`: Adds destination to user's trip itinerary.

### 4. Itinerary Planning Page
- **Page Title**: Plan Your Itinerary
- **Overview**: Create/manage itineraries with schedules and activities.
- **Container ID**: `itinerary-page` (Div)
- **UI Elements**:
  - `itinerary-name-input` (Input): Enter itinerary name.
  - `start-date-input` (Input[type=date]): Select start date.
  - `end-date-input` (Input[type=date]): Select end date.
  - `add-activity-button` (Button): Add activity to itinerary.
  - `itinerary-list` (Div): Shows existing itineraries with edit and delete options.
- **Navigation Flows**:
  - From dashboard via `plan-itinerary-button`.
  - Edit and delete actions available per itinerary in `itinerary-list`.

### 5. Accommodations Page
- **Page Title**: Search Accommodations
- **Overview**: Search and filter hotels.
- **Container ID**: `accommodations-page` (Div)
- **UI Elements**:
  - `destination-input` (Input): Destination city.
  - `check-in-date` (Input[type=date]): Check-in date.
  - `check-out-date` (Input[type=date]): Check-out date.
  - `price-filter` (Dropdown): Filter price range (Budget, Mid-range, Luxury).
  - `hotels-list` (Div): Display list of hotels with details.
- **Navigation Flows**:
  - Accessed from main navigation or links.

### 6. Transportation Page
- **Page Title**: Book Flights
- **Overview**: Search and book flights.
- **Container ID**: `transportation-page` (Div)
- **UI Elements**:
  - `departure-city` (Input): Enter departure city.
  - `arrival-city` (Input): Enter arrival city.
  - `departure-date` (Input[type=date]): Select departure date.
  - `flight-class-filter` (Dropdown): Filter flight class (Economy, Business, First Class).
  - `available-flights` (Div): List available flights with details.
- **Navigation Flows**:
  - Accessed via menu or links.

### 7. Travel Packages Page
- **Page Title**: Travel Packages
- **Overview**: Display pre-designed travel packages.
- **Container ID**: `packages-page` (Div)
- **UI Elements**:
  - `packages-grid` (Div): Grid with package cards.
  - `duration-filter` (Dropdown): Filter by package duration (3-5 days, 7-10 days, 14+ days).
  - `view-package-details-button-{pkg_id}` (Button): View details for a package.
  - `book-package-button-{pkg_id}` (Button): Book selected package.
- **Navigation Flows**:
  - Buttons navigate to package details or booking flow.

### 8. Trip Management Page
- **Page Title**: My Trips
- **Overview**: Display all created trips with management options.
- **Container ID**: `trips-page` (Div)
- **UI Elements**:
  - `trips-table` (Table): List all trips with destination, dates, status.
  - `view-trip-details-button-{trip_id}` (Button): View trip details.
  - `edit-trip-button-{trip_id}` (Button): Edit trip.
  - `delete-trip-button-{trip_id}` (Button): Delete trip.
- **Navigation Flows**:
  - Actions open details, edit forms, or confirm deletion.

### 9. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: Show details of bookings with options to download/share.
- **Container ID**: `confirmation-page` (Div)
- **UI Elements**:
  - `confirmation-number` (Div): Booking confirmation number.
  - `booking-details` (Div): Details including dates, amounts, locations.
  - `download-itinerary-button` (Button): Download itinerary PDF.
  - `share-trip-button` (Button): Share trip details.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.
- **Navigation Flows**:
  - `back-to-dashboard` returns user to Dashboard Page.

### 10. Travel Recommendations Page
- **Page Title**: Travel Recommendations
- **Overview**: Personalized recommendations and trending destinations.
- **Container ID**: `recommendations-page` (Div)
- **UI Elements**:
  - `trending-destinations` (Div): Trending destinations by popularity.
  - `recommendation-season-filter` (Dropdown): Filter by travel season (Spring, Summer, Fall, Winter).
  - `budget-filter` (Dropdown): Filter by budget range (Low, Medium, High).
  - `back-to-dashboard` (Button): Navigate back to Dashboard.
- **Navigation Flows**:
  - `back-to-dashboard` returns to Dashboard Page.

## 2. Data Storage Formats

Data files stored under directory: `data`

### 1. Destinations Data
- File: `destinations.txt`
- Format: `dest_id|name|country|region|description|attractions|climate`
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- File: `itineraries.txt`
- Format: `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- File: `hotels.txt`
- Format: `hotel_id|name|city|rating|price_per_night|amenities|category`
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- File: `flights.txt`
- Format: `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- File: `packages.txt`
- Format: `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- File: `trips.txt`
- Format: `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- File: `bookings.txt`
- Format: `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

## 3. Consistency and Completeness
- All UI element IDs strictly follow the user requirements exactly as specified.
- Button elements that allow navigation have clear linkages documented.
- Naming conventions are consistent across pages and data files.
- Data formats use pipe ('|') delimiter as required.
- No features beyond those specified are included.
- The application starts from the Dashboard Page.
- All dynamic buttons are suffixed with IDs as specified (e.g., `view-destination-button-{dest_id}`).
- Date inputs use the HTML5 input type `date`.
- Dropdown options are enumerated where applicable exactly as specified.

This complete design_spec.md reflects all requirements from the initial user task description.
