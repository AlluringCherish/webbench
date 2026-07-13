# TravelPlanner Web Application Design Specification

---

## Section 1: Page Specifications

### 1. Dashboard Page
- **Title**: Travel Planner Dashboard
- **Overview**: Main hub displaying featured destinations, upcoming trips, and quick navigation to all features.
- **Container ID**: `dashboard-page`
- **UI Elements:**
  - `featured-destinations` (Div): Shows featured travel destinations.
  - `upcoming-trips` (Div): Shows upcoming planned trips.
  - `browse-destinations-button` (Button): Navigates to Destinations Page.
  - `plan-itinerary-button` (Button): Navigates to Itinerary Planning Page.

### 2. Destinations Page
- **Title**: Travel Destinations
- **Overview**: Display all travel destinations with search and filters.
- **Container ID**: `destinations-page`
- **UI Elements:**
  - `search-destination` (Input): Search destinations by name or country.
  - `region-filter` (Dropdown): Filter by region (Asia, Europe, Americas, Africa, Oceania).
  - `destinations-grid` (Div): Displays destination cards.
  - For each destination, `view-destination-button-{dest_id}` (Button): View destination details.

### 3. Destination Details Page
- **Title**: Destination Details
- **Overview**: Detailed information about one destination.
- **Container ID**: `destination-details-page`
- **UI Elements:**
  - `destination-name` (H1): Destination name.
  - `destination-country` (Div): Destination country.
  - `destination-description` (Div): Detailed description.
  - `add-to-trip-button` (Button): Adds destination to trip.
  - `destination-attractions` (Div): Main attractions and activities.

### 4. Itinerary Planning Page
- **Title**: Plan Your Itinerary
- **Overview**: Create and manage travel itineraries.
- **Container ID**: `itinerary-page`
- **UI Elements:**
  - `itinerary-name-input` (Input): Itinerary name.
  - `start-date-input` (Input, date): Trip start date.
  - `end-date-input` (Input, date): Trip end date.
  - `add-activity-button` (Button): Add activity to itinerary.
  - `itinerary-list` (Div): List of itineraries with edit/delete options.

### 5. Accommodations Page
- **Title**: Search Accommodations
- **Overview**: Search and browse hotels with filters.
- **Container ID**: `accommodations-page`
- **UI Elements:**
  - `destination-input` (Input): Destination city for hotels.
  - `check-in-date` (Input, date): Check-in date.
  - `check-out-date` (Input, date): Check-out date.
  - `price-filter` (Dropdown): Filter hotels by price range (Budget, Mid-range, Luxury).
  - `hotels-list` (Div): List hotels with name, rating, price, amenities.

### 6. Transportation Page
- **Title**: Book Flights
- **Overview**: Search and book flights.
- **Container ID**: `transportation-page`
- **UI Elements:**
  - `departure-city` (Input): Departure city.
  - `arrival-city` (Input): Arrival city.
  - `departure-date` (Input, date): Departure date.
  - `flight-class-filter` (Dropdown): Flight class filter (Economy, Business, First Class).
  - `available-flights` (Div): List flights with airline, times, prices.

### 7. Travel Packages Page
- **Title**: Travel Packages
- **Overview**: Display pre-designed travel packages.
- **Container ID**: `packages-page`
- **UI Elements:**
  - `packages-grid` (Div): Grid showing package cards.
  - `duration-filter` (Dropdown): Filter packages by duration (3-5 days, 7-10 days, 14+ days).
  - For each package:
    - `view-package-details-button-{pkg_id}` (Button): View package details.
    - `book-package-button-{pkg_id}` (Button): Book package.

### 8. Trip Management Page
- **Title**: My Trips
- **Overview**: Display all trips with options to view, edit, delete.
- **Container ID**: `trips-page`
- **UI Elements:**
  - `trips-table` (Table): Shows trips with destination, dates, status.
  - For each trip:
    - `view-trip-details-button-{trip_id}` (Button): View trip details.
    - `edit-trip-button-{trip_id}` (Button): Edit trip.
    - `delete-trip-button-{trip_id}` (Button): Delete trip.

### 9. Booking Confirmation Page
- **Title**: Booking Confirmation
- **Overview**: Show booking confirmation details.
- **Container ID**: `confirmation-page`
- **UI Elements:**
  - `confirmation-number` (Div): Confirmation/booking number.
  - `booking-details` (Div): Detailed booking information.
  - `download-itinerary-button` (Button): Download itinerary PDF.
  - `share-trip-button` (Button): Share trip details.
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

### 10. Travel Recommendations Page
- **Title**: Travel Recommendations
- **Overview**: Show personalized recommendations and trending destinations.
- **Container ID**: `recommendations-page`
- **UI Elements:**
  - `trending-destinations` (Div): Displays trending destinations.
  - `recommendation-season-filter` (Dropdown): Filter by season (Spring, Summer, Fall, Winter).
  - `budget-filter` (Dropdown): Filter by budget (Low, Medium, High).
  - `back-to-dashboard` (Button): Navigate back to Dashboard.

---

### Navigation Flow
- Dashboard buttons to: Destinations Page, Itinerary Planning Page.
- Destinations Page to Destination Details Page on `view-destination-button-{dest_id}`.
- Destination Details Page to add destination to trip.
- Itinerary Planning Page manages itineraries.
- Accommodations, Transportation, Packages pages accessible from dashboard or relevant links.
- Package buttons navigate to booking and confirmation.
- Trip Management Page to view/edit/delete trips.
- Booking Confirmation includes back to Dashboard.
- Recommendations Page includes back to Dashboard.


## Section 2: Data Storage Formats

All data stored in local text files under folder: `data/`

### 1. Destinations Data
- Filename: `data/destinations.txt`
- Format:
  ```
  dest_id|name|country|region|description|attractions|climate
  ```
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- Filename: `data/itineraries.txt`
- Format:
  ```
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
  ```
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- Filename: `data/hotels.txt`
- Format:
  ```
  hotel_id|name|city|rating|price_per_night|amenities|category
  ```
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- Filename: `data/flights.txt`
- Format:
  ```
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
  ```
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- Filename: `data/packages.txt`
- Format:
  ```
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
  ```
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- Filename: `data/trips.txt`
- Format:
  ```
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
  ```
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- Filename: `data/bookings.txt`
- Format:
  ```
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
  ```
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

---

## Section 3: Consistency and Completeness

- All UI element IDs and types exactly match the requirements document.
- Data file names, field names, and delimiters strictly follow requirements.
- Naming conventions consistent throughout: hyphen-separated UI IDs, underscore-separated data fields.
- Navigation flows explained without adding any elements beyond specification.
- Data fields cover all user requirements including destinations, itineraries, hotels, flights, packages, trips, and bookings.

---

This specification fully reflects the provided requirements for backend and frontend developers to implement the TravelPlanner application.
