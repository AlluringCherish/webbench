# TravelPlanner Web Application Design Specification

---

## 1. Flask Routes Specification

### 1. Dashboard Page
- Route Endpoint: `/`
- HTTP Methods: GET
- Function Name: dashboard
- Template File: `templates/dashboard.html`
- Context Variables:
  - `featured_destinations`: List[Dict] - List of destination summaries. Example: [{"dest_id": 1, "name": "Paris", "country": "France"}, ...]
  - `upcoming_trips`: List[Dict] - List of upcoming trip summaries. Example: [{"trip_id": 1, "trip_name": "Summer Vacation 2025", "start_date": "2025-06-01"}, ...]
- Navigation Actions:
  - Button with ID `browse-destinations-button` navigates to `url_for('destinations')`
  - Button with ID `plan-itinerary-button` navigates to `url_for('plan_itinerary')`

### 2. Destinations Page
- Route Endpoint: `/destinations`
- HTTP Methods: GET, POST (for search/filter submissions)
- Function Name: destinations
- Template File: `templates/destinations.html`
- Context Variables:
  - `destinations`: List[Dict] - Filtered list of destination summaries. Example: [{"dest_id": 1, "name": "Paris", "country": "France", "region": "Europe"}, ...]
  - `search_query`: str - Search input from user.
  - `selected_region`: str - Selected region filter value.
- Navigation Actions:
  - Button with ID pattern `view-destination-button-{dest_id}` navigates to `url_for('destination_details', dest_id=dest_id)`
  - Other navigation as links/buttons can redirect back to Dashboard (`url_for('dashboard')`)

### 3. Destination Details Page
- Route Endpoint: `/destinations/<int:dest_id>`
- HTTP Methods: GET, POST (POST when adding destination to trip)
- Function Name: destination_details
- Template File: `templates/destination_details.html`
- Context Variables:
  - `destination`: Dict - Detailed destination info (keys: dest_id, name, country, description, attractions (List[str]), climate)
- Navigation Actions:
  - Button with ID `add-to-trip-button` triggers a POST to add this destination to itinerary/trip.
  - Link/button to return to Destinations page: `url_for('destinations')`

### 4. Itinerary Planning Page
- Route Endpoint: `/itinerary`
- HTTP Methods: GET, POST (POST to add activity or create itinerary)
- Function Name: plan_itinerary
- Template File: `templates/itinerary.html`
- Context Variables:
  - `itineraries`: List[Dict] - List of itineraries with keys (itinerary_id, itinerary_name, destination, start_date, end_date, activities (List[str]), status)
- Navigation Actions:
  - Button with ID `add-activity-button` submits form to add activity.
  - Edit and delete buttons on itinerary items post to appropriate endpoints or handled via JavaScript.
  - Navigation to Dashboard with `url_for('dashboard')`

### 5. Accommodations Page
- Route Endpoint: `/accommodations`
- HTTP Methods: GET, POST (POST for search/filter)
- Function Name: search_accommodations
- Template File: `templates/accommodations.html`
- Context Variables:
  - `hotels`: List[Dict] - List of hotel details (hotel_id, name, city, rating, price_per_night, amenities (List[str]), category)
  - `search_destination`: str
  - `check_in_date`: str (date format 'YYYY-MM-DD')
  - `check_out_date`: str
  - `selected_price_filter`: str
- Navigation Actions:
  - Navigation back to Dashboard with Button or link: `url_for('dashboard')`

### 6. Transportation Page
- Route Endpoint: `/transportation`
- HTTP Methods: GET, POST (POST for flight search/booking)
- Function Name: book_flights
- Template File: `templates/transportation.html`
- Context Variables:
  - `flights`: List[Dict] - Flight options data (flight_id, airline, departure_city, arrival_city, departure_time, arrival_time, price, class_type, duration)
  - `departure_city`: str
  - `arrival_city`: str
  - `departure_date`: str
  - `selected_class_filter`: str
- Navigation Actions:
  - Navigation back to Dashboard with link/button: `url_for('dashboard')`

### 7. Travel Packages Page
- Route Endpoint: `/packages`
- HTTP Methods: GET, POST (POST for filtering, booking)
- Function Name: travel_packages
- Template File: `templates/packages.html`
- Context Variables:
  - `packages`: List[Dict] - Travel package summaries (package_id, package_name, destination, duration_days, price, included_items (List[str]), difficulty_level)
  - `selected_duration_filter`: str
- Navigation Actions:
  - Button with ID pattern `view-package-details-button-{pkg_id}` navigates to `url_for('package_details', pkg_id=pkg_id)`
  - Button with ID pattern `book-package-button-{pkg_id}` triggers booking action.
  - Navigation back to Dashboard: `url_for('dashboard')`

### 8. Trip Management Page
- Route Endpoint: `/trips`
- HTTP Methods: GET, POST (POST for edit/delete actions)
- Function Name: manage_trips
- Template File: `templates/trips.html`
- Context Variables:
  - `trips`: List[Dict] - Trip data (trip_id, trip_name, destination, start_date, end_date, status)
- Navigation Actions:
  - Button with ID pattern `view-trip-details-button-{trip_id}` navigates to `url_for('trip_details', trip_id=trip_id)`
  - Button with ID pattern `edit-trip-button-{trip_id}` triggers edit action.
  - Button with ID pattern `delete-trip-button-{trip_id}` triggers delete action.
  - Navigation back to Dashboard: `url_for('dashboard')`

### 9. Booking Confirmation Page
- Route Endpoint: `/booking-confirmation/<int:booking_id>`
- HTTP Methods: GET
- Function Name: booking_confirmation
- Template File: `templates/booking_confirmation.html`
- Context Variables:
  - `booking`: Dict - Booking details (booking_id, trip_id, booking_type, booking_date, amount, confirmation_number, status)
- Navigation Actions:
  - Button with ID `download-itinerary-button` triggers itinerary PDF download.
  - Button with ID `share-trip-button` triggers share functionality.
  - Button with ID `back-to-dashboard` navigates to `url_for('dashboard')`

### 10. Travel Recommendations Page
- Route Endpoint: `/recommendations`
- HTTP Methods: GET, POST (POST for filtering by season/budget)
- Function Name: travel_recommendations
- Template File: `templates/recommendations.html`
- Context Variables:
  - `trending_destinations`: List[Dict] - Trending destinations with ranking info.
  - `selected_season_filter`: str
  - `selected_budget_filter`: str
- Navigation Actions:
  - Button with ID `back-to-dashboard` navigates to `url_for('dashboard')`

---

## 2. HTML Templates Specification

### General:
- All templates are located in the `templates/` directory.
- Template files have `.html` extensions.
- Navigation urls use Jinja2 `url_for` matching flask route function names.

---

### 1. `templates/dashboard.html`
- Page Title: "Travel Planner Dashboard"
- Elements:
  - `dashboard-page` (Div): Main container for the dashboard.
  - `featured-destinations` (Div): Displays featured destination cards (dynamic list).
  - `upcoming-trips` (Div): Displays summary of upcoming trips.
  - `browse-destinations-button` (Button): Navigates to destinations page.
  - `plan-itinerary-button` (Button): Navigates to itinerary planning page.
- Context Variables:
  - `featured_destinations`: List[Dict] with keys `dest_id` (int), `name` (str), `country` (str).
  - `upcoming_trips`: List[Dict] with keys `trip_id` (int), `trip_name` (str), `start_date` (str).
- Navigation:
  - `browse-destinations-button` -> `{{ url_for('destinations') }}`
  - `plan-itinerary-button` -> `{{ url_for('plan_itinerary') }}`

---

### 2. `templates/destinations.html`
- Page Title: "Travel Destinations"
- Elements:
  - `destinations-page` (Div): Container
  - `search-destination` (Input, text): Text box for search input.
  - `region-filter` (Dropdown): Options: Asia, Europe, Americas, Africa, Oceania.
  - `destinations-grid` (Div): Contains destination cards.
  - `view-destination-button-{{ dest.dest_id }}` (Button): For each destination card.
- Context Variables:
  - `destinations`: List[Dict] with keys `dest_id` (int), `name` (str), `country` (str), `region` (str).
  - `search_query`: str
  - `selected_region`: str
- Navigation:
  - Each `view-destination-button-{{ dest.dest_id }}` triggers navigation to `{{ url_for('destination_details', dest_id=dest.dest_id) }}`
  - Links/buttons may navigate back to dashboard `{{ url_for('dashboard') }}`

---

### 3. `templates/destination_details.html`
- Page Title: "Destination Details"
- Elements:
  - `destination-details-page` (Div): Container
  - `destination-name` (H1): Destination name
  - `destination-country` (Div): Country
  - `destination-description` (Div): Detailed description
  - `add-to-trip-button` (Button): Adds destination to trip
  - `destination-attractions` (Div): List or paragraph of attractions
- Context Variables:
  - `destination`: Dict with keys `dest_id` (int), `name` (str), `country` (str), `description` (str), `attractions` (List[str]), `climate` (str)
- Navigation:
  - `add-to-trip-button` POSTs to add destination to itinerary/trip.
  - Link back to destinations page: `{{ url_for('destinations') }}`

---

### 4. `templates/itinerary.html`
- Page Title: "Plan Your Itinerary"
- Elements:
  - `itinerary-page` (Div): Container
  - `itinerary-name-input` (Input, text): For itinerary name
  - `start-date-input` (Input, date): Start date
  - `end-date-input` (Input, date): End date
  - `add-activity-button` (Button): Adds activity
  - `itinerary-list` (Div): List of itineraries with edit/delete
- Context Variables:
  - `itineraries`: List[Dict]
    - Example item keys: itinerary_id (int), itinerary_name (str), destination (str), start_date (str), end_date (str), activities (List[str]), status (str)
- Navigation:
  - Edit/delete actions typically handle via buttons or forms.
  - Navigation to dashboard: `{{ url_for('dashboard') }}`

---

### 5. `templates/accommodations.html`
- Page Title: "Search Accommodations"
- Elements:
  - `accommodations-page` (Div): Container
  - `destination-input` (Input, text): Destination city
  - `check-in-date` (Input, date): Check-in date
  - `check-out-date` (Input, date): Check-out date
  - `price-filter` (Dropdown): Options: Budget, Mid-range, Luxury
  - `hotels-list` (Div): List of hotels shown
- Context Variables:
  - `hotels`: List[Dict]
    - hotel_id (int), name (str), city (str), rating (float), price_per_night (float), amenities (List[str]), category (str)
  - `search_destination`: str
  - `check_in_date`: str
  - `check_out_date`: str
  - `selected_price_filter`: str
- Navigation:
  - Navigation back to dashboard: `{{ url_for('dashboard') }}`

---

### 6. `templates/transportation.html`
- Page Title: "Book Flights"
- Elements:
  - `transportation-page` (Div): Container
  - `departure-city` (Input, text): Departure city
  - `arrival-city` (Input, text): Arrival city
  - `departure-date` (Input, date): Departure date
  - `flight-class-filter` (Dropdown): Options: Economy, Business, First Class
  - `available-flights` (Div): List of flights
- Context Variables:
  - `flights`: List[Dict]
    - flight_id (int), airline (str), departure_city (str), arrival_city (str), departure_time (str), arrival_time (str), price (float), class_type (str), duration (str)
  - `departure_city`: str
  - `arrival_city`: str
  - `departure_date`: str
  - `selected_class_filter`: str
- Navigation:
  - Navigation back to dashboard: `{{ url_for('dashboard') }}`

---

### 7. `templates/packages.html`
- Page Title: "Travel Packages"
- Elements:
  - `packages-page` (Div): Container
  - `packages-grid` (Div): Grid of packages
  - `duration-filter` (Dropdown): Options: 3-5 days, 7-10 days, 14+ days
  - Button with ID `view-package-details-button-{{ pkg.package_id }}` for each package
  - Button with ID `book-package-button-{{ pkg.package_id }}` for booking
- Context Variables:
  - `packages`: List[Dict]
    - package_id (int), package_name (str), destination (str), duration_days (int), price (float), included_items (List[str]), difficulty_level (str)
  - `selected_duration_filter`: str
- Navigation:
  - Package details button: `{{ url_for('package_details', pkg_id=pkg.package_id) }}`
  - Navigation back to dashboard: `{{ url_for('dashboard') }}`

---

### 8. `templates/trips.html`
- Page Title: "My Trips"
- Elements:
  - `trips-page` (Div): Container
  - `trips-table` (Table): Table showing trips
  - Buttons with IDs patterned:
    - `view-trip-details-button-{{ trip.trip_id }}`
    - `edit-trip-button-{{ trip.trip_id }}`
    - `delete-trip-button-{{ trip.trip_id }}`
- Context Variables:
  - `trips`: List[Dict]
    - trip_id (int), trip_name (str), destination (str), start_date (str), end_date (str), status (str)
- Navigation:
  - View trip details button: `{{ url_for('trip_details', trip_id=trip.trip_id) }}`
  - Navigation back to dashboard: `{{ url_for('dashboard') }}`

---

### 9. `templates/booking_confirmation.html`
- Page Title: "Booking Confirmation"
- Elements:
  - `confirmation-page` (Div): Container
  - `confirmation-number` (Div): Shows confirmation number
  - `booking-details` (Div): Shows booking info
  - `download-itinerary-button` (Button): Download itinerary PDF
  - `share-trip-button` (Button): Share trip details
  - `back-to-dashboard` (Button): Back to dashboard
- Context Variables:
  - `booking`: Dict
    - booking_id (int), trip_id (int), booking_type (str), booking_date (str), amount (float), confirmation_number (str), status (str)
- Navigation:
  - `back-to-dashboard` button -> `{{ url_for('dashboard') }}`

---

### 10. `templates/recommendations.html`
- Page Title: "Travel Recommendations"
- Elements:
  - `recommendations-page` (Div): Container
  - `trending-destinations` (Div): List of trending destinations
  - `recommendation-season-filter` (Dropdown): Options: Spring, Summer, Fall, Winter
  - `budget-filter` (Dropdown): Options: Low, Medium, High
  - `back-to-dashboard` (Button): Back to Dashboard
- Context Variables:
  - `trending_destinations`: List[Dict] with rankings
  - `selected_season_filter`: str
  - `selected_budget_filter`: str
- Navigation:
  - `back-to-dashboard` -> `{{ url_for('dashboard') }}`

---

## 3. Data File Schemas

Data files are stored in the local `data` directory. All files use pipe `|` as delimiter and have no header row.

### 1. Destinations Data
- File Name: `data/destinations.txt`
- Fields: dest_id (int) | name (str) | country (str) | region (str) | description (str) | attractions (str comma-separated) | climate (str)
- Description: Contains details of travel destinations including description and attractions.
- Example Rows:
  - `1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate`
  - `2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate`
  - `3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical`

### 2. Itineraries Data
- File Name: `data/itineraries.txt`
- Fields: itinerary_id (int) | itinerary_name (str) | destination (str) | start_date (YYYY-MM-DD) | end_date (YYYY-MM-DD) | activities (str comma-separated) | status (str)
- Description: Stores created itineraries with activities and status.
- Example Rows:
  - `1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned`
  - `2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress`
  - `3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned`

### 3. Hotels Data
- File Name: `data/hotels.txt`
- Fields: hotel_id (int) | name (str) | city (str) | rating (float) | price_per_night (float) | amenities (str comma-separated) | category (str)
- Description: Details of hotels with ratings and categories.
- Example Rows:
  - `1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury`
  - `2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range`
  - `3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range`

### 4. Flights Data
- File Name: `data/flights.txt`
- Fields: flight_id (int) | airline (str) | departure_city (str) | arrival_city (str) | departure_time (HH:MM) | arrival_time (HH:MM with optional descriptor) | price (float) | class_type (str) | duration (str)
- Description: Flight details with times and pricing.
- Example Rows:
  - `1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes`
  - `2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes`
  - `3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes`

### 5. Travel Packages Data
- File Name: `data/packages.txt`
- Fields: package_id (int) | package_name (str) | destination (str) | duration_days (int) | price (float) | included_items (str comma-separated) | difficulty_level (str)
- Description: Pre-designed packages for trips including what's included and difficulty.
- Example Rows:
  - `1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy`
  - `2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate`
  - `3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate`

### 6. Trips Data
- File Name: `data/trips.txt`
- Fields: trip_id (int) | trip_name (str) | destination (str) | start_date (YYYY-MM-DD) | end_date (YYYY-MM-DD) | total_budget (float) | status (str) | created_date (YYYY-MM-DD)
- Description: User created trips and budgets.
- Example Rows:
  - `1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10`
  - `2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11`
  - `3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12`

### 7. Bookings Data
- File Name: `data/bookings.txt`
- Fields: booking_id (int) | trip_id (int) | booking_type (str) | booking_date (YYYY-MM-DD) | amount (float) | confirmation_number (str) | status (str)
- Description: Individual booking records including confirmation numbers.
- Example Rows:
  - `1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed`
  - `2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed`
  - `3|3|Package|2025-01-12|1800.00|CONF003|Pending`

---

## Assumptions
- All date fields are in the format `YYYY-MM-DD`.
- Activities, amenities, and included items are stored as comma-separated strings but parsed into lists in the application.
- Buttons that perform POST operations (like add to trip, booking) have corresponding form actions or AJAX calls as per implementation.
- Dynamic IDs use Jinja2 templating in templates where `{}` indicate variable parts.

---

This concludes the full detailed design specification for the TravelPlanner application, enabling independent frontend and backend development with no further clarifications needed.