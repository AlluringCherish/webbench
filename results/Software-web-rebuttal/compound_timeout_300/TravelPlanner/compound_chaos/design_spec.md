# TravelPlanner Web Application - Design Specification

---

## 1. Flask Routes Specification

| Page Name              | Route Endpoint           | HTTP Method(s) | Function Name                 | Template Rendered           | Context Variables Passed                                   | Navigation Mappings (Element ID -> Route Endpoint)                                    |
|------------------------|--------------------------|----------------|-------------------------------|-----------------------------|------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Dashboard              | `/`                      | GET            | `dashboard_page`              | `dashboard.html`            | `featured_destinations: List[Dict]`, `upcoming_trips: List[Dict]`                  | `browse-destinations-button` -> `destinations_page`(`/destinations`)
               | `plan-itinerary-button` -> `itinerary_page`(`/itinerary`)
                        |
| Destinations           | `/destinations`           | GET            | `destinations_page`            | `destinations.html`          | `destinations: List[Dict]`, `regions: List[str]`                                  | `view-destination-button-{dest_id}` -> `destination_details_page`(`/destination/<int:dest_id>`) |
| Destination Details    | `/destination/<int:dest_id>`| GET, POST      | `destination_details_page`     | `destination_details.html`   | `destination: Dict`                                                               | `add-to-trip-button` -> POST action stays on same page or redirects to itinerary page as per functional design |
| Itinerary Planning     | `/itinerary`              | GET, POST      | `itinerary_page`               | `itinerary.html`             | `itineraries: List[Dict]`, `regions: List[str]`                                   | `add-activity-button` updates itinerary data (POST action)
                         |
| Accommodations         | `/accommodations`         | GET            | `accommodations_page`          | `accommodations.html`        | `hotels: List[Dict]`                                                             | None explicitly stated in task, assume no internal navigation buttons
             |
| Transportation        | `/transportation`          | GET            | `transportation_page`          | `transportation.html`        | `flights: List[Dict]`                                                           | None explicitly stated
                                                               |
| Travel Packages       | `/packages`                | GET            | `packages_page`                | `packages.html`              | `packages: List[Dict]`, `durations: List[str]`                                  | `view-package-details-button-{pkg_id}` -> `package_details_page` (if exists, else undefined)
           | `book-package-button-{pkg_id}` -> `book_package` POST or page (undefined in requirement)                      |
| Trip Management       | `/trips`                   | GET            | `trips_page`                   | `trips.html`                 | `trips: List[Dict]`                                                              | `view-trip-details-button-{trip_id}` -> `trip_details_page` (undefined, assumed)
            | `edit-trip-button-{trip_id}` -> `edit_trip_page` (undefined, assumed)
            | `delete-trip-button-{trip_id}` -> DELETE or POST action to delete trip (assumed)                              |
| Booking Confirmation  | `/booking-confirmation/<int:booking_id>` | GET       | `booking_confirmation_page`   | `booking_confirmation.html`  | `booking: Dict`                                                                | `download-itinerary-button` triggers download (frontend)
                   | `share-trip-button` triggers share action
                     | `back-to-dashboard` -> `dashboard_page`(`/`)
          |
| Travel Recommendations | `/recommendations`          | GET            | `recommendations_page`          | `recommendations.html`       | `recommendations: List[Dict]`, `trending_destinations: List[Dict]`               | `back-to-dashboard` -> `dashboard_page`(`/`)
                                     |

**Critical Consistency Points:**
- All function names use lowercase with underscores as per convention.
- Each route returns its listed template with exact name.
- Context variable names are consistent across backend and frontend.
- Navigation buttons have matching element IDs and refer to exact route endpoints via `url_for()`.


---

## 2. HTML Templates Specification

### 1. `dashboard.html`
- Page Title: Travel Planner Dashboard
- Main Heading: `<h1 id="dashboard-title">Travel Planner Dashboard</h1>`
- Container Div ID: `dashboard-page` (Div)
- Element IDs and Types:
  - `featured-destinations` (Div): Displays featured travel destinations list.
  - `upcoming-trips` (Div): Displays a list of upcoming trips.
  - `browse-destinations-button` (Button): Navigates to Destinations Page.
  - `plan-itinerary-button` (Button): Navigates to Itinerary Planning Page.
- Context Variables:
  - `featured_destinations`: List of dictionaries with keys: `dest_id` (int), `name` (str), `country` (str), `image_url` (str).
  - `upcoming_trips`: List of dictionaries with keys: `trip_id` (int), `trip_name` (str), `start_date` (str YYYY-MM-DD), `end_date` (str YYYY-MM-DD).
- Navigation:
  - `browse-destinations-button` uses `url_for('destinations_page')`.
  - `plan-itinerary-button` uses `url_for('itinerary_page')`.

---

### 2. `destinations.html`
- Page Title: Travel Destinations
- Main Heading: `<h1 id="destinations-title">Travel Destinations</h1>`
- Container Div ID: `destinations-page` (Div)
- Element IDs and Types:
  - `search-destination` (Input textbox): Text field to search destinations by name or country.
  - `region-filter` (Dropdown select): Options: Asia, Europe, Americas, Africa, Oceania.
  - `destinations-grid` (Div): Grid container for destination cards.
  - Each destination card includes button with ID pattern `view-destination-button-{{ dest.dest_id }}` (Button): View destination details.
- Context Variables:
  - `destinations`: List of dicts with keys: `dest_id` (int), `name` (str), `country` (str), `region` (str), `image_url` (str).
  - `regions`: List of strings (region names).
- Navigation:
  - Each `view-destination-button-{{ dest.dest_id }}` uses `url_for('destination_details_page', dest_id=dest.dest_id)`.

---

### 3. `destination_details.html`
- Page Title: Destination Details
- Main Heading: `<h1 id="destination-name">{{ destination.name }}</h1>`
- Container Div ID: `destination-details-page` (Div)
- Element IDs and Types:
  - `destination-country` (Div): Displays the country of the destination.
  - `destination-description` (Div): Detailed description text.
  - `add-to-trip-button` (Button): Adds this destination to user's trip itinerary.
  - `destination-attractions` (Div): Lists main attractions and activities.
- Context Variables:
  - `destination`: Dictionary with fields:
    - `dest_id` (int)
    - `name` (str)
    - `country` (str)
    - `region` (str)
    - `description` (str)
    - `attractions` (List[str])
    - `climate` (str)
- Navigation:
  - `add-to-trip-button` triggers POST to same route or redirects to itinerary.

---

### 4. `itinerary.html`
- Page Title: Plan Your Itinerary
- Main Heading: `<h1 id="itinerary-title">Plan Your Itinerary</h1>`
- Container Div ID: `itinerary-page` (Div)
- Element IDs and Types:
  - `itinerary-name-input` (Input text): For entering itinerary name.
  - `start-date-input` (Input date): Select trip start date.
  - `end-date-input` (Input date): Select trip end date.
  - `add-activity-button` (Button): Adds new activity to itinerary.
  - `itinerary-list` (Div): Displays list of itineraries with edit/delete buttons.
- Context Variables:
  - `itineraries`: List of dictionaries with fields:
    - `itinerary_id` (int)
    - `itinerary_name` (str)
    - `destination` (str)
    - `start_date` (str, YYYY-MM-DD)
    - `end_date` (str, YYYY-MM-DD)
    - `activities` (List[str])
    - `status` (str)
- Navigation:
  - Buttons inside `itinerary-list` have element IDs like `edit-itinerary-button-{{ itinerary.itinerary_id }}` and `delete-itinerary-button-{{ itinerary.itinerary_id }}` (assumed)
  - `add-activity-button` triggers POST or client-side addition.

---

### 5. `accommodations.html`
- Page Title: Search Accommodations
- Main Heading: `<h1 id="accommodations-title">Search Accommodations</h1>`
- Container Div ID: `accommodations-page` (Div)
- Element IDs and Types:
  - `destination-input` (Input text): Destination city for hotel search.
  - `check-in-date` (Input date): Check-in date.
  - `check-out-date` (Input date): Check-out date.
  - `price-filter` (Dropdown select): Options: Budget, Mid-range, Luxury.
  - `hotels-list` (Div): List of hotels showing name, rating, price, amenities.
- Context Variables:
  - `hotels`: List of dictionaries with keys:
    - `hotel_id` (int)
    - `name` (str)
    - `city` (str)
    - `rating` (float)
    - `price_per_night` (float)
    - `amenities` (List[str])
    - `category` (str)
- Navigation:
  - No explicit navigation buttons described.

---

### 6. `transportation.html`
- Page Title: Book Flights
- Main Heading: `<h1 id="transportation-title">Book Flights</h1>`
- Container Div ID: `transportation-page` (Div)
- Element IDs and Types:
  - `departure-city` (Input text): Departure city.
  - `arrival-city` (Input text): Arrival city.
  - `departure-date` (Input date): Departure date.
  - `flight-class-filter` (Dropdown select): Options: Economy, Business, First Class.
  - `available-flights` (Div): List showing flights with airline, times, prices.
- Context Variables:
  - `flights`: List of dicts with keys:
    - `flight_id` (int)
    - `airline` (str)
    - `departure_city` (str)
    - `arrival_city` (str)
    - `departure_time` (str, HH:MM or HH:MM next day)
    - `arrival_time` (str, HH:MM or HH:MM next day)
    - `price` (float)
    - `class_type` (str)
    - `duration` (str)
- Navigation:
  - No explicit button navigation described.

---

### 7. `packages.html`
- Page Title: Travel Packages
- Main Heading: `<h1 id="packages-title">Travel Packages</h1>`
- Container Div ID: `packages-page` (Div)
- Element IDs and Types:
  - `duration-filter` (Dropdown select): Filter packages by duration:
    - Options: 3-5 days, 7-10 days, 14+ days
  - `packages-grid` (Div): Grid container for package cards.
  - Each package card includes buttons:
    - `view-package-details-button-{{ pkg.package_id }}` (Button): View package details.
    - `book-package-button-{{ pkg.package_id }}` (Button): Book selected package.
- Context Variables:
  - `packages`: List of dictionaries with keys:
    - `package_id` (int)
    - `package_name` (str)
    - `destination` (str)
    - `duration_days` (int)
    - `price` (float)
    - `included_items` (List[str])
    - `difficulty_level` (str)
  - `durations`: List[str] of duration filter options
- Navigation:
  - `view-package-details-button-{{ pkg.package_id }}` uses `url_for('package_details_page', pkg_id=pkg.package_id)` if such page exists
  - `book-package-button-{{ pkg.package_id }}` triggers booking POST or page navigation

---

### 8. `trips.html`
- Page Title: My Trips
- Main Heading: `<h1 id="trips-title">My Trips</h1>`
- Container Div ID: `trips-page` (Div)
- Element IDs and Types:
  - `trips-table` (Table): Displays trips with columns for destination, dates, status.
  - Buttons with IDs per trip:
    - `view-trip-details-button-{{ trip.trip_id }}` (Button): View trip details.
    - `edit-trip-button-{{ trip.trip_id }}` (Button): Edit trip.
    - `delete-trip-button-{{ trip.trip_id }}` (Button): Delete trip.
- Context Variables:
  - `trips`: List of dicts with:
    - `trip_id` (int)
    - `trip_name` (str)
    - `destination` (str)
    - `start_date` (str YYYY-MM-DD)
    - `end_date` (str YYYY-MM-DD)
    - `total_budget` (float)
    - `status` (str)
    - `created_date` (str YYYY-MM-DD)
- Navigation:
  - Buttons use exact route endpoints related to trip management (assumed)

---

### 9. `booking_confirmation.html`
- Page Title: Booking Confirmation
- Main Heading: `<h1 id="confirmation-title">Booking Confirmation</h1>`
- Container Div ID: `confirmation-page` (Div)
- Element IDs and Types:
  - `confirmation-number` (Div): Shows booking confirmation number.
  - `booking-details` (Div): Shows detailed booking info including dates, amounts, locations.
  - `download-itinerary-button` (Button): Downloads trip itinerary as PDF.
  - `share-trip-button` (Button): Shares trip details.
  - `back-to-dashboard` (Button): Navigates back to Dashboard page.
- Context Variables:
  - `booking`: Dict with keys:
    - `booking_id` (int)
    - `trip_id` (int)
    - `booking_type` (str)
    - `booking_date` (str YYYY-MM-DD)
    - `amount` (float)
    - `confirmation_number` (str)
    - `status` (str)
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard_page')`

---

### 10. `recommendations.html`
- Page Title: Travel Recommendations
- Main Heading: `<h1 id="recommendations-title">Travel Recommendations</h1>`
- Container Div ID: `recommendations-page` (Div)
- Element IDs and Types:
  - `trending-destinations` (Div): Displays trending destinations ranked by popularity.
  - `recommendation-season-filter` (Dropdown select): Options: Spring, Summer, Fall, Winter.
  - `budget-filter` (Dropdown select): Options: Low, Medium, High.
  - `back-to-dashboard` (Button): Navigates back to Dashboard page.
- Context Variables:
  - `recommendations`: List of dicts with keys:
    - variable depending on recommendation type (assumed similar to destinations/trips)
  - `trending_destinations`: List of dicts with keys: `dest_id` (int), `name` (str), `popularity` (int).
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard_page')`


---

## 3. Data File Schemas

| File Name          | Field Names (Pipe-Delimited Order)                                              | Description                              | Example Rows                                                                                   |
|--------------------|--------------------------------------------------------------------------------|------------------------------------------|------------------------------------------------------------------------------------------------|
| `destinations.txt` | `dest_id|name|country|region|description|attractions|climate`                 | Stores destination information            | `1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate`
                      | `2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate`
                      | `3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical`

| `itineraries.txt`   | `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status` | User created travel itineraries           | `1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned`
                      | `2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress`
                      | `3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned`

| `hotels.txt`        | `hotel_id|name|city|rating|price_per_night|amenities|category`               | Hotel and accommodation details          | `1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury`
                      | `2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range`
                      | `3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range`

| `flights.txt`       | `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration` | Flight information                         | `1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes`
                      | `2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes`
                      | `3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes`

| `packages.txt`      | `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`| Pre-designed travel package details       | `1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy`
                      | `2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate`
                      | `3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate`

| `trips.txt`         | `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date` | User trip management data                  | `1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10`
                      | `2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11`
                      | `3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12`

| `bookings.txt`      | `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`| Booking confirmation details               | `1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed`
                      | `2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed`
                      | `3|3|Package|2025-01-12|1800.00|CONF003|Pending`


---

**All data rows contain no header included in the text files.**

**Ensure strict adherence to the exact pipe-delimited format and field ordering for backend file parsing.**

---

This design spec enables independent backend and frontend development with complete and unambiguous specification of routes, templates, and data files.
