# TravelPlanner Web Application Design Specification

---

## 1. Flask Routes Specification

### 1. Dashboard Page
- **Route Endpoint:** `/dashboard`
- **HTTP Methods:** GET
- **Function Name:** `dashboard`
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_destinations`: List[Dict] - List of featured destination dictionaries each including keys such as `dest_id` (int), `name` (str), `country` (str).
  - `upcoming_trips`: List[Dict] - List of upcoming trip dictionaries each including keys such as `trip_id` (int), `trip_name` (str), `start_date` (str ISO date).
- **Navigation:**
  - Button with ID `browse-destinations-button` navigates to `url_for('destinations')`.
  - Button with ID `plan-itinerary-button` navigates to `url_for('plan_itinerary')`.

### 2. Destinations Page
- **Route Endpoint:** `/destinations`
- **HTTP Methods:** GET, POST
- **Function Name:** `destinations`
- **Template Rendered:** `destinations.html`
- **Context Variables:**
  - `destinations`: List[Dict] - List of destination dictionaries each including keys: `dest_id` (int), `name` (str), `country` (str), `region` (str).
  - `search_query`: str - Current search string entered by user.
  - `selected_region`: str or None - Currently selected region filter.
  - `regions`: List[str] - List of region options: ["Asia", "Europe", "Americas", "Africa", "Oceania"]
- **Navigation:**
  - Button with dynamic ID `view-destination-button-{{ dest.dest_id }}` navigates to `url_for('destination_details', dest_id=dest.dest_id)`.

### 3. Destination Details Page
- **Route Endpoint:** `/destinations/<int:dest_id>`
- **HTTP Methods:** GET
- **Function Name:** `destination_details`
- **Template Rendered:** `destination_details.html`
- **Context Variables:**
  - `destination`: Dict with keys `dest_id` (int), `name` (str), `country` (str), `description` (str), `attractions` (str), `climate` (str).
- **Navigation:**
  - Button with ID `add-to-trip-button` navigates to `url_for('plan_itinerary', selected_destination=destination['name'])` or triggers adding destination.

### 4. Itinerary Planning Page
- **Route Endpoint:** `/itinerary`
- **HTTP Methods:** GET, POST
- **Function Name:** `plan_itinerary`
- **Template Rendered:** `itinerary.html`
- **Context Variables:**
  - `itineraries`: List[Dict] - List of itinerary dictionaries with keys: `itinerary_id` (int), `itinerary_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `activities` (str), `status` (str).
  - `selected_destination`: Optional[str] - Destination pre-selected for new itinerary.
- **Navigation:**
  - Button with ID `add-activity-button` triggers adding activity to itinerary in current session.

### 5. Accommodations Page
- **Route Endpoint:** `/accommodations`
- **HTTP Methods:** GET, POST
- **Function Name:** `accommodations`
- **Template Rendered:** `accommodations.html`
- **Context Variables:**
  - `hotels`: List[Dict] - List of hotel dictionaries with keys: `hotel_id` (int), `name` (str), `city` (str), `rating` (float), `price_per_night` (float), `amenities` (str), `category` (str).
  - `destination_input`: str - Current destination input filter string.
  - `check_in_date`: str or None - Selected check-in date.
  - `check_out_date`: str or None - Selected check-out date.
  - `price_filter`: str or None - Selected price range filter.
  - `price_ranges`: List[str] - List of price range options: ["Budget", "Mid-range", "Luxury"]
- **Navigation:**
  - Hotels are displayed in a list with details; no specific navigation buttons defined.

### 6. Transportation Page
- **Route Endpoint:** `/transportation`
- **HTTP Methods:** GET, POST
- **Function Name:** `transportation`
- **Template Rendered:** `transportation.html`
- **Context Variables:**
  - `flights`: List[Dict] - List of flight dictionaries with keys: `flight_id` (int), `airline` (str), `departure_city` (str), `arrival_city` (str), `departure_time` (str), `arrival_time` (str), `price` (float), `class_type` (str), `duration` (str).
  - `departure_city`: str - Current departure city input.
  - `arrival_city`: str - Current arrival city input.
  - `departure_date`: str or None - Selected departure date.
  - `flight_class_filter`: str or None - Selected flight class filter.
  - `class_options`: List[str] - Flight class options: ["Economy", "Business", "First Class"]
- **Navigation:**
  - Flights are displayed with details; no specific navigation buttons defined.

### 7. Travel Packages Page
- **Route Endpoint:** `/packages`
- **HTTP Methods:** GET, POST
- **Function Name:** `packages`
- **Template Rendered:** `packages.html`
- **Context Variables:**
  - `packages`: List[Dict] - List of package dictionaries with keys: `package_id` (int), `package_name` (str), `destination` (str), `duration_days` (int), `price` (float), `included_items` (str), `difficulty_level` (str).
  - `duration_filter`: str or None - Selected duration filter.
  - `duration_options`: List[str] - Duration options: ["3-5 days", "7-10 days", "14+ days"]
- **Navigation:**
  - Button with ID `view-package-details-button-{{ pkg.package_id }}` navigates to `url_for('package_details', pkg_id=pkg.package_id)`.
  - Button with ID `book-package-button-{{ pkg.package_id }}` triggers booking the package.

### 8. Trip Management Page
- **Route Endpoint:** `/trips`
- **HTTP Methods:** GET, POST
- **Function Name:** `manage_trips`
- **Template Rendered:** `trips.html`
- **Context Variables:**
  - `trips`: List[Dict] - List of trip dictionaries with keys: `trip_id` (int), `trip_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `status` (str).
- **Navigation:**
  - Buttons with dynamic IDs:
    - `view-trip-details-button-{{ trip.trip_id }}` navigates to `url_for('trip_details', trip_id=trip.trip_id)`.
    - `edit-trip-button-{{ trip.trip_id }}` navigates to `url_for('edit_trip', trip_id=trip.trip_id)`.
    - `delete-trip-button-{{ trip.trip_id }}` triggers deletion of trip.

### 9. Booking Confirmation Page
- **Route Endpoint:** `/confirmation`
- **HTTP Methods:** GET
- **Function Name:** `booking_confirmation`
- **Template Rendered:** `confirmation.html`
- **Context Variables:**
  - `confirmation_number`: str - Booking confirmation number.
  - `booking_details`: Dict - Detailed booking information including dates, amounts, locations.
- **Navigation:**
  - Button with ID `download-itinerary-button` triggers download of itinerary PDF.
  - Button with ID `share-trip-button` triggers sharing of trip details.
  - Button with ID `back-to-dashboard` navigates to `url_for('dashboard')`.

### 10. Travel Recommendations Page
- **Route Endpoint:** `/recommendations`
- **HTTP Methods:** GET, POST
- **Function Name:** `recommendations`
- **Template Rendered:** `recommendations.html`
- **Context Variables:**
  - `trending_destinations`: List[Dict] - List of trending destination dictionaries.
  - `season_filter`: str or None - Selected season filter.
  - `budget_filter`: str or None - Selected budget filter.
  - `season_options`: List[str] - Season options: ["Spring", "Summer", "Fall", "Winter"]
  - `budget_options`: List[str] - Budget options: ["Low", "Medium", "High"]
- **Navigation:**
  - Button with ID `back-to-dashboard` navigates to `url_for('dashboard')`.


## 2. HTML Templates Specification

### 1. templates/dashboard.html
- **Page Title:** Travel Planner Dashboard
- **Main Headers:** `<h1 id="page-title">Travel Planner Dashboard</h1>`
- **Element IDs and Descriptions:**
  - `dashboard-page` (Div): Container for the dashboard content.
  - `featured-destinations` (Div): Displays featured destinations.
  - `upcoming-trips` (Div): Lists upcoming trips.
  - `browse-destinations-button` (Button): Navigates to destinations page.
  - `plan-itinerary-button` (Button): Navigates to itinerary planning page.
- **Context Variables:**
  - `featured_destinations` (List[Dict]) example:
    ```
    [{"dest_id": 1, "name": "Paris", "country": "France"}]
    ```
  - `upcoming_trips` (List[Dict]) example:
    ```
    [{"trip_id": 1, "trip_name": "Summer Vacation", "start_date": "2025-06-01"}]
    ```
- **Navigation:**
  - `browse-destinations-button`: `url_for('destinations')`
  - `plan-itinerary-button`: `url_for('plan_itinerary')`

### 2. templates/destinations.html
- **Page Title:** Travel Destinations
- **Main Headers:** `<h1 id="page-title">Travel Destinations</h1>`
- **Element IDs and Descriptions:**
  - `destinations-page` (Div): Container for destinations content.
  - `search-destination` (Input): Text input for searching destinations by name or country.
  - `region-filter` (Dropdown): Dropdown for filtering by region.
  - `destinations-grid` (Div): Grid displaying destination cards.
  - `view-destination-button-{{ dest.dest_id }}` (Button): Button on each card to view details.
- **Context Variables:**
  - `destinations` (List[Dict]) example:
    ```
    [{"dest_id": 1, "name": "Paris", "country": "France", "region": "Europe"}]
    ```
  - `search_query` (str)
  - `selected_region` (str or None)
  - `regions`: ["Asia", "Europe", "Americas", "Africa", "Oceania"]
- **Navigation:**
  - Dynamic buttons `view-destination-button-{{ dest.dest_id }}` navigate to details page using `url_for('destination_details', dest_id=dest.dest_id)`

### 3. templates/destination_details.html
- **Page Title:** Destination Details
- **Main Headers:** `<h1 id="destination-name">{{ destination.name }}</h1>`
- **Element IDs and Descriptions:**
  - `destination-details-page` (Div): Container for details page.
  - `destination-name` (H1): Displays the name of the destination.
  - `destination-country` (Div): Shows the country.
  - `destination-description` (Div): Detailed description.
  - `add-to-trip-button` (Button): Button to add this destination to an itinerary.
  - `destination-attractions` (Div): Section listing attractions.
- **Context Variables:**
  - `destination` (Dict) example:
    ```
    {
      "dest_id": 1,
      "name": "Paris",
      "country": "France",
      "description": "City of lights and romance with world-class museums",
      "attractions": "Eiffel Tower, Louvre Museum, Notre-Dame",
      "climate": "Temperate"
    }
    ```
- **Navigation:**
  - `add-to-trip-button`: triggers addition to itinerary or navigates to itinerary page pre-filled with this destination.

### 4. templates/itinerary.html
- **Page Title:** Plan Your Itinerary
- **Main Headers:** `<h1 id="page-title">Plan Your Itinerary</h1>`
- **Element IDs and Descriptions:**
  - `itinerary-page` (Div): Container for itinerary planning.
  - `itinerary-name-input` (Input): Field to enter itinerary name.
  - `start-date-input` (Input, date): Field to select start date.
  - `end-date-input` (Input, date): Field to select end date.
  - `add-activity-button` (Button): Button to add activities.
  - `itinerary-list` (Div): Displays created itineraries with edit/delete options.
- **Context Variables:**
  - `itineraries` (List[Dict]) example:
    ```
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
  - `selected_destination` (Optional[str]) example: "Paris"
- **Navigation:**
  - `add-activity-button`: triggers adding activity dynamically.

### 5. templates/accommodations.html
- **Page Title:** Search Accommodations
- **Main Headers:** `<h1 id="page-title">Search Accommodations</h1>`
- **Element IDs and Descriptions:**
  - `accommodations-page` (Div): Container for accommodations search.
  - `destination-input` (Input): Text input for destination city.
  - `check-in-date` (Input, date): Date picker for check-in.
  - `check-out-date` (Input, date): Date picker for check-out.
  - `price-filter` (Dropdown): Filter dropdown for price range.
  - `hotels-list` (Div): List displaying hotels.
- **Context Variables:**
  - `hotels` (List[Dict]) example:
    ```
    [
      {
        "hotel_id": 1,
        "name": "Ritz Paris",
        "city": "Paris",
        "rating": 5.0,
        "price_per_night": 450.00,
        "amenities": "WiFi, Spa, Restaurant, Pool",
        "category": "Luxury"
      }
    ]
    ```
  - `destination_input` (str)
  - `check_in_date` (str or None)
  - `check_out_date` (str or None)
  - `price_filter` (str or None)
  - `price_ranges`: ["Budget", "Mid-range", "Luxury"]
- **Navigation:**
  - No specific navigation elements defined.

### 6. templates/transportation.html
- **Page Title:** Book Flights
- **Main Headers:** `<h1 id="page-title">Book Flights</h1>`
- **Element IDs and Descriptions:**
  - `transportation-page` (Div): Container for transportation page.
  - `departure-city` (Input): Text input for departure city.
  - `arrival-city` (Input): Text input for arrival city.
  - `departure-date` (Input, date): Date picker for departure.
  - `flight-class-filter` (Dropdown): Filter dropdown for flight class.
  - `available-flights` (Div): List displays flights matching criteria.
- **Context Variables:**
  - `flights` (List[Dict]) example:
    ```
    [
      {
        "flight_id": 1,
        "airline": "Air France",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "10:00",
        "arrival_time": "22:30",
        "price": 850.00,
        "class_type": "Economy",
        "duration": "7 hours 30 minutes"
      }
    ]
    ```
  - `departure_city` (str)
  - `arrival_city` (str)
  - `departure_date` (str or None)
  - `flight_class_filter` (str or None)
  - `class_options`: ["Economy", "Business", "First Class"]
- **Navigation:**
  - No specific navigation buttons.

### 7. templates/packages.html
- **Page Title:** Travel Packages
- **Main Headers:** `<h1 id="page-title">Travel Packages</h1>`
- **Element IDs and Descriptions:**
  - `packages-page` (Div): Container for packages page.
  - `packages-grid` (Div): Grid displaying package cards.
  - `duration-filter` (Dropdown): Filter packages by duration.
  - `view-package-details-button-{{ pkg.package_id }}` (Button): View details button on each package card.
  - `book-package-button-{{ pkg.package_id }}` (Button): Book package button on each card.
- **Context Variables:**
  - `packages` (List[Dict]) example:
    ```
    [
      {
        "package_id": 1,
        "package_name": "Paris Classic Tour",
        "destination": "Paris",
        "duration_days": 5,
        "price": 1500.00,
        "included_items": "Hotel, Flights, Guided tours, Meals",
        "difficulty_level": "Easy"
      }
    ]
    ```
  - `duration_filter` (str or None)
  - `duration_options`: ["3-5 days", "7-10 days", "14+ days"]
- **Navigation:**
  - Dynamic buttons navigate or perform booking using corresponding URLs/function.

### 8. templates/trips.html
- **Page Title:** My Trips
- **Main Headers:** `<h1 id="page-title">My Trips</h1>`
- **Element IDs and Descriptions:**
  - `trips-page` (Div): Container for trips page.
  - `trips-table` (Table): Displays trips data with columns such as Trip Name, Destination, Dates, Status.
  - `view-trip-details-button-{{ trip.trip_id }}` (Button): Button to view trip details.
  - `edit-trip-button-{{ trip.trip_id }}` (Button): Button to edit trip.
  - `delete-trip-button-{{ trip.trip_id }}` (Button): Button to delete trip.
- **Context Variables:**
  - `trips` (List[Dict]) example:
    ```
    [
      {
        "trip_id": 1,
        "trip_name": "Summer Vacation 2025",
        "destination": "Paris",
        "start_date": "2025-06-01",
        "end_date": "2025-06-15",
        "status": "Booked"
      }
    ]
    ```
- **Navigation:**
  - Buttons navigate to view/edit/delete routes using trip_id.

### 9. templates/confirmation.html
- **Page Title:** Booking Confirmation
- **Main Headers:** `<h1 id="page-title">Booking Confirmation</h1>`
- **Element IDs and Descriptions:**
  - `confirmation-page` (Div): Container for confirmation details.
  - `confirmation-number` (Div): Displays booking confirmation number.
  - `booking-details` (Div): Shows detailed booking information.
  - `download-itinerary-button` (Button): Button to download itinerary PDF.
  - `share-trip-button` (Button): Button to share trip details.
  - `back-to-dashboard` (Button): Button to navigate back to dashboard.
- **Context Variables:**
  - `confirmation_number` (str)
  - `booking_details` (Dict)
- **Navigation:**
  - Buttons trigger respective functions/navigation as described.

### 10. templates/recommendations.html
- **Page Title:** Travel Recommendations
- **Main Headers:** `<h1 id="page-title">Travel Recommendations</h1>`
- **Element IDs and Descriptions:**
  - `recommendations-page` (Div): Container for recommendations.
  - `trending-destinations` (Div): Displays trending destinations.
  - `recommendation-season-filter` (Dropdown): Dropdown for season filter.
  - `budget-filter` (Dropdown): Dropdown for budget filter.
  - `back-to-dashboard` (Button): Button to navigate back to dashboard.
- **Context Variables:**
  - `trending_destinations` (List[Dict])
  - `season_filter` (str or None)
  - `budget_filter` (str or None)
  - `season_options`: ["Spring", "Summer", "Fall", "Winter"]
  - `budget_options`: ["Low", "Medium", "High"]
- **Navigation:**
  - `back-to-dashboard` navigates to dashboard.


## 3. Data File Schemas

### 1. data/destinations.txt
- **Field Names and Order:**
  `dest_id|name|country|region|description|attractions|climate`
- **Purpose:** Stores travel destination data with details and characteristics.
- **Example Rows:**
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. data/itineraries.txt
- **Field Names and Order:**
  `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
- **Purpose:** Stores user-created itineraries with schedule and activity details.
- **Example Rows:**
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. data/hotels.txt
- **Field Names and Order:**
  `hotel_id|name|city|rating|price_per_night|amenities|category`
- **Purpose:** Stores hotel information available for accommodation searches.
- **Example Rows:**
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. data/flights.txt
- **Field Names and Order:**
  `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
- **Purpose:** Stores flight options with scheduling, pricing, and class information.
- **Example Rows:**
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. data/packages.txt
- **Field Names and Order:**
  `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
- **Purpose:** Stores pre-designed travel packages with details.
- **Example Rows:**
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. data/trips.txt
- **Field Names and Order:**
  `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
- **Purpose:** Stores user trips with overall budget and status.
- **Example Rows:**
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. data/bookings.txt
- **Field Names and Order:**
  `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
- **Purpose:** Stores booking details associated with trips.
- **Example Rows:**
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

---

This design specification document fully describes the Flask routes, HTML templates, and data file schemas necessary for the independent implementation of the 'TravelPlanner' web application as per the user requirements.