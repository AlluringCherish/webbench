# TravelPlanner Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- Route Endpoint: `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Template Filename: `dashboard.html`
- Context Variables:
  - `featured_destinations` (List[Dict[str, Any]]): Example:
    ```json
    [
      {"dest_id": 1, "name": "Paris", "country": "France"},
      {"dest_id": 2, "name": "Tokyo", "country": "Japan"}
    ]
    ```
  - `upcoming_trips` (List[Dict[str, Any]]): Example:
    ```json
    [
      {"trip_id": 1, "trip_name": "Summer Vacation 2025", "destination": "Paris", "start_date": "2025-06-01", "end_date": "2025-06-15"}
    ]
    ```
- Navigation Actions:
  - Button `browse-destinations-button` navigates to `url_for('destinations')`
  - Button `plan-itinerary-button` navigates to `url_for('plan_itinerary')`

---

### 2. Destinations Page
- Route Endpoint: `/destinations`
- HTTP Methods: GET
- Function Name: `destinations`
- Template Filename: `destinations.html`
- Context Variables:
  - `destinations` (List[Dict[str, Any]]): Each dict with `dest_id` (int), `name` (str), `country` (str). Example:
    ```json
    [
      {"dest_id": 1, "name": "Paris", "country": "France"},
      {"dest_id": 2, "name": "Tokyo", "country": "Japan"}
    ]
    ```
  - `regions` (List[str]): Fixed list `["Asia", "Europe", "Americas", "Africa", "Oceania"]`
  - `selected_region` (str or None): Currently selected region filter or None
  - `search_query` (str or None): Search input or None
- Navigation Actions:
  - Button with id `view-destination-button-{{ dest.dest_id }}` navigates to `url_for('destination_details', dest_id=dest.dest_id)`

---

### 3. Destination Details Page
- Route Endpoint: `/destinations/<int:dest_id>`
- HTTP Methods: GET
- Function Name: `destination_details`
- Template Filename: `destination_details.html`
- Context Variables:
  - `destination` (Dict[str, Any]): Example:
    ```json
    {
      "dest_id": 1,
      "name": "Paris",
      "country": "France",
      "description": "City of lights and romance with world-class museums",
      "attractions": "Eiffel Tower, Louvre Museum, Notre-Dame"
    }
    ```
- Navigation Actions:
  - Button `add-to-trip-button` triggers adding destination to trip (POST route/controller not specified)

---

### 4. Itinerary Planning Page
- Route Endpoint: `/itinerary`
- HTTP Methods: GET, POST
- Function Name: `plan_itinerary`
- Template Filename: `itinerary.html`
- Context Variables:
  - `itineraries` (List[Dict[str, Any]]): Example:
    ```json
    [
      {
        "itinerary_id": 1,
        "itinerary_name": "Paris Spring Break",
        "destination": "Paris",
        "start_date": "2025-03-20",
        "end_date": "2025-03-27",
        "activities": "Museum tours, River cruise, Cafe hopping",
        "status": "Planned"
      }
    ]
    ```
- Navigation Actions:
  - Button `add-activity-button` triggers addition of activity (handled via POST)
  - Itinerary edit/delete links for each itinerary with URLs e.g., `/edit_itinerary/<int:itinerary_id>`, `/delete_itinerary/<int:itinerary_id>`

---

### 5. Accommodations Page
- Route Endpoint: `/accommodations`
- HTTP Methods: GET, POST
- Function Name: `accommodations`
- Template Filename: `accommodations.html`
- Context Variables:
  - `hotels` (List[Dict[str, Any]]): Each dict includes keys: `hotel_id`, `name`, `city`, `rating`, `price_per_night`, `amenities`, `category`. Example:
    ```json
    [
      {"hotel_id":1,"name":"Ritz Paris","city":"Paris","rating":5.0,"price_per_night":450.00,"amenities":"WiFi, Spa, Restaurant, Pool","category":"Luxury"}
    ]
    ```
  - `price_ranges` (List[str]): `["Budget", "Mid-range", "Luxury"]`
  - `search_params` (Dict[str, Any]) with keys: `destination` (str), `check_in_date` (str), `check_out_date` (str), `price_filter` (str or None)
- Navigation Actions:
  - Hotels displayed in `hotels-list` div; no individual navigation buttons specified

---

### 6. Transportation Page
- Route Endpoint: `/flights`
- HTTP Methods: GET, POST
- Function Name: `book_flights`
- Template Filename: `flights.html`
- Context Variables:
  - `available_flights` (List[Dict[str, Any]]): Each flight dict has keys: `flight_id`, `airline`, `departure_city`, `arrival_city`, `departure_time`, `arrival_time`, `price`, `class_type`, `duration`. Example:
    ```json
    [
      {"flight_id":1,"airline":"Air France","departure_city":"New York","arrival_city":"Paris","departure_time":"10:00","arrival_time":"22:30","price":850.00,"class_type":"Economy","duration":"7 hours 30 minutes"}
    ]
    ```
  - `flight_classes` (List[str]): `["Economy", "Business", "First Class"]`
  - `search_params` (Dict[str, Any]) with keys: `departure_city`, `arrival_city`, `departure_date`, `flight_class_filter`
- Navigation Actions:
  - Flights displayed in `available-flights` div; no specific navigation buttons specified

---

### 7. Travel Packages Page
- Route Endpoint: `/packages`
- HTTP Methods: GET, POST
- Function Name: `travel_packages`
- Template Filename: `packages.html`
- Context Variables:
  - `packages` (List[Dict[str, Any]]): Example:
    ```json
    [
      {"package_id": 1, "package_name": "Paris Classic Tour", "destination": "Paris", "duration_days": 5, "price": 1500.00},
      {"package_id": 2, "package_name": "Tokyo Experience", "destination": "Tokyo", "duration_days": 10, "price": 2200.00}
    ]
    ```
  - `duration_filters` (List[str]): `["3-5 days", "7-10 days", "14+ days"]`
  - `selected_duration_filter` (str or None)
- Navigation Actions:
  - Button `view-package-details-button-{{ pkg.package_id }}` navigates to `url_for('package_details', package_id=pkg.package_id)`
  - Button `book-package-button-{{ pkg.package_id }}` triggers booking (POST)

---

### 8. Trip Management Page
- Route Endpoint: `/trips`
- HTTP Methods: GET, POST
- Function Name: `manage_trips`
- Template Filename: `trips.html`
- Context Variables:
  - `trips` (List[Dict[str, Any]]): Example:
    ```json
    [
      {"trip_id":1, "trip_name":"Summer Vacation 2025", "destination":"Paris", "start_date":"2025-06-01", "end_date":"2025-06-15", "status":"Booked"}
    ]
    ```
- Navigation Actions:
  - Buttons `view-trip-details-button-{{ trip.trip_id }}` link to `url_for('trip_details', trip_id=trip.trip_id)`
  - Buttons `edit-trip-button-{{ trip.trip_id }}` link to `url_for('edit_trip', trip_id=trip.trip_id)`
  - Buttons `delete-trip-button-{{ trip.trip_id }}` trigger deletion (POST)

---

### 9. Booking Confirmation Page
- Route Endpoint: `/confirmation/<int:booking_id>`
- HTTP Methods: GET
- Function Name: `booking_confirmation`
- Template Filename: `confirmation.html`
- Context Variables:
  - `booking` (Dict[str, Any]): Example:
    ```json
    {
        "booking_id": 1,
        "trip_id": 1,
        "booking_type": "Hotel",
        "booking_date": "2025-01-10",
        "amount": 750.00,
        "confirmation_number": "CONF001",
        "status": "Confirmed"
    }
    ```
- Navigation Actions:
  - Button `download-itinerary-button` triggers itinerary PDF download
  - Button `share-trip-button` triggers share function
  - Button `back-to-dashboard` navigates to `url_for('dashboard')`

---

### 10. Travel Recommendations Page
- Route Endpoint: `/recommendations`
- HTTP Methods: GET, POST
- Function Name: `travel_recommendations`
- Template Filename: `recommendations.html`
- Context Variables:
  - `trending_destinations` (List[Dict[str, Any]]): Each with `dest_id` (int), `name` (str), `popularity_rank` (int). Example:
    ```json
    [
      {"dest_id": 1, "name": "Paris", "popularity_rank": 1},
      {"dest_id": 2, "name": "Tokyo", "popularity_rank": 2}
    ]
    ```
  - `seasons` (List[str]): `["Spring", "Summer", "Fall", "Winter"]`
  - `budgets` (List[str]): `["Low", "Medium", "High"]`
  - `selected_season` (str or None)
  - `selected_budget` (str or None)
- Navigation Actions:
  - Button `back-to-dashboard` navigates to `url_for('dashboard')`

---


## Section 2: HTML Templates Specification

### templates/dashboard.html
- Page Title: "Travel Planner Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-destinations` (Div): Displays featured travel destinations
  - `upcoming-trips` (Div): Displays list of upcoming trips
  - `browse-destinations-button` (Button): Navigates to destinations page
  - `plan-itinerary-button` (Button): Navigates to itinerary planning page
- Context Variables:
  - `featured_destinations` (List[Dict]) with keys `dest_id` (int), `name` (str), `country` (str)
  - `upcoming_trips` (List[Dict]) with keys `trip_id` (int), `trip_name` (str), `destination` (str), `start_date` (str), `end_date` (str)
- Navigation Mappings:
  - `browse-destinations-button`: link/action calls `url_for('destinations')`
  - `plan-itinerary-button`: link/action calls `url_for('plan_itinerary')`

---

### templates/destinations.html
- Page Title: "Travel Destinations"
- Element IDs:
  - `destinations-page` (Div): Container
  - `search-destination` (Input): Search field for destinations by name or country
  - `region-filter` (Dropdown): Filter select for region with options: Asia, Europe, Americas, Africa, Oceania
  - `destinations-grid` (Div): Grid container for destination cards
  - Destination Cards with buttons:
    - `view-destination-button-{{ dest.dest_id }}` (Button): View destination details
- Context Variables:
  - `destinations` (List[Dict]) with keys `dest_id` (int), `name` (str), `country` (str)
  - `regions` (List[str]) fixed as above
  - `selected_region` (str or None)
  - `search_query` (str or None)
- Navigation Mappings:
  - Each `view-destination-button-{{ dest.dest_id }}` calls `url_for('destination_details', dest_id=dest.dest_id)`

---

### templates/destination_details.html
- Page Title: "Destination Details"
- Element IDs:
  - `destination-details-page` (Div): Container
  - `destination-name` (H1): Displays destination name
  - `destination-country` (Div): Shows country
  - `destination-description` (Div): Shows detailed description
  - `add-to-trip-button` (Button): Adds destination to trip
  - `destination-attractions` (Div): Shows main attractions and activities
- Context Variables:
  - `destination` (Dict) keys: `dest_id` (int), `name` (str), `country` (str), `description` (str), `attractions` (str)
- Navigation Mappings:
  - `add-to-trip-button`: triggers POST action to add this destination to trip

---

### templates/itinerary.html
- Page Title: "Plan Your Itinerary"
- Element IDs:
  - `itinerary-page` (Div)
  - `itinerary-name-input` (Input)
  - `start-date-input` (Input date)
  - `end-date-input` (Input date)
  - `add-activity-button` (Button)
  - `itinerary-list` (Div): List with each itinerary having edit and delete options
- Context Variables:
  - `itineraries` (List[Dict]) each with keys as in data schema
- Navigation Mappings:
  - `add-activity-button`: triggers form submission to add an activity
  - Itinerary entries:
    - Edit link: calls `url_for('edit_itinerary', itinerary_id=itinerary.itinerary_id)`
    - Delete button: triggers POST to delete itinerary

---

### templates/accommodations.html
- Page Title: "Search Accommodations"
- Element IDs:
  - `accommodations-page` (Div)
  - `destination-input` (Input) for city
  - `check-in-date` (Input date)
  - `check-out-date` (Input date)
  - `price-filter` (Dropdown)
  - `hotels-list` (Div) displays hotel cards
- Context Variables:
  - `hotels` (List[Dict]) each with keys: `hotel_id`, `name`, `city`, `rating`, `price_per_night`, `amenities`, `category`
  - `price_ranges` (List[str]) fixed: ["Budget", "Mid-range", "Luxury"]
  - `search_params` (Dict) with `destination`, `check_in_date`, `check_out_date`, `price_filter`
- Navigation Mappings:
  - Hotels displayed, no direct navigational buttons defined

---

### templates/flights.html
- Page Title: "Book Flights"
- Element IDs:
  - `transportation-page` (Div)
  - `departure-city` (Input)
  - `arrival-city` (Input)
  - `departure-date` (Input date)
  - `flight-class-filter` (Dropdown)
  - `available-flights` (Div) list of flights
- Context Variables:
  - `available_flights` (List[Dict]) each with keys: `flight_id`, `airline`, `departure_city`, `arrival_city`, `departure_time`, `arrival_time`, `price`, `class_type`, `duration`
  - `flight_classes` (List[str]): ["Economy", "Business", "First Class"]
  - `search_params` (Dict) with `departure_city`, `arrival_city`, `departure_date`, `flight_class_filter`
- Navigation Mappings:
  - Flights displayed, no direct navigation buttons specified

---

### templates/packages.html
- Page Title: "Travel Packages"
- Element IDs:
  - `packages-page` (Div)
  - `packages-grid` (Div)
  - `duration-filter` (Dropdown)
  - Package Cards have buttons:
    - `view-package-details-button-{{ pkg.package_id }}` (Button)
    - `book-package-button-{{ pkg.package_id }}` (Button)
- Context Variables:
  - `packages` (List[Dict]) with keys: `package_id`, `package_name`, `destination`, `duration_days`, `price`
  - `duration_filters` (List[str]) fixed: ["3-5 days", "7-10 days", "14+ days"]
  - `selected_duration_filter` (str or None)
- Navigation Mappings:
  - `view-package-details-button-{{ pkg.package_id }}` navigates to `url_for('package_details', package_id=pkg.package_id)`
  - `book-package-button-{{ pkg.package_id }}` triggers POST booking

---

### templates/trips.html
- Page Title: "My Trips"
- Element IDs:
  - `trips-page` (Div)
  - `trips-table` (Table)
  - Table Buttons with IDs:
    - `view-trip-details-button-{{ trip.trip_id }}` (Button)
    - `edit-trip-button-{{ trip.trip_id }}` (Button)
    - `delete-trip-button-{{ trip.trip_id }}` (Button)
- Context Variables:
  - `trips` (List[Dict]) with keys: `trip_id`, `trip_name`, `destination`, `start_date`, `end_date`, `status`
- Navigation Mappings:
  - View buttons -> `url_for('trip_details', trip_id=trip.trip_id)`
  - Edit buttons -> `url_for('edit_trip', trip_id=trip.trip_id)`
  - Delete buttons trigger POST delete

---

### templates/confirmation.html
- Page Title: "Booking Confirmation"
- Element IDs:
  - `confirmation-page` (Div)
  - `confirmation-number` (Div)
  - `booking-details` (Div)
  - `download-itinerary-button` (Button)
  - `share-trip-button` (Button)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `booking` (Dict) with keys: `booking_id`, `trip_id`, `booking_type`, `booking_date`, `amount`, `confirmation_number`, `status`
- Navigation Mappings:
  - `back-to-dashboard` button -> `url_for('dashboard')`

---

### templates/recommendations.html
- Page Title: "Travel Recommendations"
- Element IDs:
  - `recommendations-page` (Div)
  - `trending-destinations` (Div)
  - `recommendation-season-filter` (Dropdown)
  - `budget-filter` (Dropdown)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `trending_destinations` (List[Dict]) with `dest_id`, `name`, `popularity_rank`
  - `seasons` (List[str]): ["Spring", "Summer", "Fall", "Winter"]
  - `budgets` (List[str]): ["Low", "Medium", "High"]
  - `selected_season` (str or None)
  - `selected_budget` (str or None)
- Navigation Mappings:
  - `back-to-dashboard` button -> `url_for('dashboard')`

---

## Section 3: Data File Schemas

### 1. Destinations Data
- File: `data/destinations.txt`
- Fields (pipe-delimited):
  - `dest_id` (int)
  - `name` (str)
  - `country` (str)
  - `region` (str)
  - `description` (str)
  - `attractions` (str)
  - `climate` (str)
- Description: Contains details about travel destinations and main attractions.
- Example Rows:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

---

### 2. Itineraries Data
- File: `data/itineraries.txt`
- Fields:
  - `itinerary_id` (int)
  - `itinerary_name` (str)
  - `destination` (str)
  - `start_date` (YYYY-MM-DD)
  - `end_date` (YYYY-MM-DD)
  - `activities` (str)
  - `status` (str)
- Description: Contains user-created itineraries with activities and status.
- Example Rows:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

---

### 3. Hotels Data
- File: `data/hotels.txt`
- Fields:
  - `hotel_id` (int)
  - `name` (str)
  - `city` (str)
  - `rating` (float)
  - `price_per_night` (float)
  - `amenities` (str)
  - `category` (str) (price range category: Budget, Mid-range, Luxury)
- Description: Hotel listings with ratings, prices and amenities.
- Example Rows:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

---

### 4. Flights Data
- File: `data/flights.txt`
- Fields:
  - `flight_id` (int)
  - `airline` (str)
  - `departure_city` (str)
  - `arrival_city` (str)
  - `departure_time` (str, format HH:MM or with "next day")
  - `arrival_time` (str)
  - `price` (float)
  - `class_type` (str) (Economy, Business, First Class)
  - `duration` (str)
- Description: Flight schedule and pricing details.
- Example Rows:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

---

### 5. Travel Packages Data
- File: `data/packages.txt`
- Fields:
  - `package_id` (int)
  - `package_name` (str)
  - `destination` (str)
  - `duration_days` (int)
  - `price` (float)
  - `included_items` (str)
  - `difficulty_level` (str)
- Description: Pre-designed travel packages with included services.
- Example Rows:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

---

### 6. Trips Data
- File: `data/trips.txt`
- Fields:
  - `trip_id` (int)
  - `trip_name` (str)
  - `destination` (str)
  - `start_date` (YYYY-MM-DD)
  - `end_date` (YYYY-MM-DD)
  - `total_budget` (float)
  - `status` (str)
  - `created_date` (YYYY-MM-DD)
- Description: User trips with status and budget.
- Example Rows:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

---

### 7. Bookings Data
- File: `data/bookings.txt`
- Fields:
  - `booking_id` (int)
  - `trip_id` (int)
  - `booking_type` (str) (Hotel, Flight, Package)
  - `booking_date` (YYYY-MM-DD)
  - `amount` (float)
  - `confirmation_number` (str)
  - `status` (str)
- Description: Booking records associated with trips.
- Example Rows:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```