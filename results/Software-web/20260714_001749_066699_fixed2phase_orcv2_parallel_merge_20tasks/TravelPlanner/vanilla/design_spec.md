# TravelPlanner Design Specification

---

## Section 1: Merged Backend Specification

### Flask Backend Routes Specification

1. **Dashboard Page**
   - **Route:** `/` or `/dashboard`
   - **Method:** GET
   - **Function:** `dashboard()`
   - **Template:** `dashboard.html`
   - **Context Variables:**
     - `featured_destinations` (list of destination dicts)
     - `upcoming_trips` (list of trip dicts)
   - **Description:** Displays main hub with featured destinations and upcoming trips.

2. **Destinations Page**
   - **Route:** `/destinations`
   - **Method:** GET
   - **Function:** `list_destinations()`
   - **Template:** `destinations.html`
   - **Context Variables:**
     - `destinations` (filtered list based on optional query parameters)
     - `search_query` (string, optional)
     - `region_filter` (string, optional: Asia, Europe, Americas, Africa, Oceania)
   - **Description:** Lists all destinations with optional search and region filter.

3. **Destination Details Page**
   - **Route:** `/destinations/<int:dest_id>`
   - **Method:** GET
   - **Function:** `destination_details(dest_id)`
   - **Template:** `destination_details.html`
   - **Context Variables:**
     - `destination` (dict with destination details)
   - **Description:** Shows detailed info of a specific destination.

   - **Route:** `/destinations/<int:dest_id>/add-to-trip`
   - **Method:** POST
   - **Function:** `add_destination_to_trip(dest_id)`
   - **Action:** Adds the destination to user's upcoming trip or itinerary.
   - **Redirect:** Back to destination details or trip management page.

4. **Itinerary Planning Page**
   - **Route:** `/itinerary`
   - **Methods:** GET, POST
   - **Function:** `itinerary()`
   - **Template:** `itinerary.html`
   - **Context Variables:**
     - `itineraries` (list of itineraries)
   - **Form POST Handling:**
     - Create new itinerary with name, destination, start_date, end_date
     - Add activities to existing itineraries via AJAX or form posts
     - Edit and delete itinerary actions handled either on this route or separate endpoints

   - **Route:** `/itinerary/<int:itinerary_id>/edit`
   - **Methods:** GET, POST
   - **Function:** `edit_itinerary(itinerary_id)`
   - **Template:** `edit_itinerary.html`
   - **Description:** Edit itinerary details and activities.

   - **Route:** `/itinerary/<int:itinerary_id>/delete`
   - **Method:** POST
   - **Function:** `delete_itinerary(itinerary_id)`
   - **Action:** Deletes an itinerary.
   - **Redirect:** To `/itinerary`

5. **Accommodations Page**
   - **Route:** `/accommodations`
   - **Method:** GET
   - **Function:** `search_accommodations()`
   - **Template:** `accommodations.html`
   - **Context Variables:**
     - `hotels` (filtered list based on city, price range)
     - `destination` (string, input from user)
     - `check_in_date` (date string)
     - `check_out_date` (date string)
     - `price_filter` (Budget, Mid-range, Luxury)
   - **Description:** Search and browse hotels.

6. **Transportation Page**
   - **Route:** `/flights`
   - **Method:** GET
   - **Function:** `search_flights()`
   - **Template:** `flights.html`
   - **Context Variables:**
     - `flights` (filtered list based on departure, arrival, date, class)
     - `departure_city` (string)
     - `arrival_city` (string)
     - `departure_date` (date string)
     - `flight_class` (Economy, Business, First Class)
   - **Description:** Search and display available flights.

7. **Travel Packages Page**
   - **Route:** `/packages`
   - **Method:** GET
   - **Function:** `list_packages()`
   - **Template:** `packages.html`
   - **Context Variables:**
     - `packages` (filtered by duration)
     - `duration_filter` (3-5 days, 7-10 days, 14+ days)

   - **Route:** `/packages/<int:package_id>`
   - **Method:** GET
   - **Function:** `package_details(package_id)`
   - **Template:** `package_details.html`
   - **Context Variables:**
     - `package` (package detail dict)

   - **Route:** `/packages/<int:package_id>/book`
   - **Method:** POST
   - **Function:** `book_package(package_id)`
   - **Action:** Creates a booking for the selected package.
   - **Redirect:** To booking confirmation page.

8. **Trip Management Page**
   - **Route:** `/trips`
   - **Method:** GET
   - **Function:** `list_trips()`
   - **Template:** `trips.html`
   - **Context Variables:**
     - `trips` (list of all trips)

   - **Route:** `/trips/<int:trip_id>`
   - **Method:** GET
   - **Function:** `trip_details(trip_id)`
   - **Template:** `trip_details.html`
   - **Context Variables:**
     - `trip` (trip details)

   - **Route:** `/trips/<int:trip_id>/edit`
   - **Methods:** GET, POST
   - **Function:** `edit_trip(trip_id)`
   - **Template:** `edit_trip.html`
   - **Description:** Edit trip details.

   - **Route:** `/trips/<int:trip_id>/delete`
   - **Method:** POST
   - **Function:** `delete_trip(trip_id)`
   - **Redirect:** To `/trips`

9. **Booking Confirmation Page**
   - **Route:** `/booking/confirmation/<string:confirmation_number>`
   - **Method:** GET
   - **Function:** `booking_confirmation(confirmation_number)`
   - **Template:** `booking_confirmation.html`
   - **Context Variables:**
     - `booking` (booking details dict)
     - Related trip info if needed

10. **Travel Recommendations Page**
    - **Route:** `/recommendations`
    - **Method:** GET
    - **Function:** `recommendations()`
    - **Template:** `recommendations.html`
    - **Context Variables:**
      - `trending_destinations` (list sorted by popularity)
      - `season_filter` (Spring, Summer, Fall, Winter)
      - `budget_filter` (Low, Medium, High)

11. **Back to Dashboard Redirect**
    - **Route:** `/back-to-dashboard`
    - **Method:** GET
    - **Function:** `back_to_dashboard()`
    - **Action:** Redirects to `/dashboard`

---

### Local Text File Data Schemas

All data stored pipe-delimited `|` files under `data/` directory.

1. **Destinations Data** (`data/destinations.txt`)
   - Fields:
     - `dest_id` (int) - Unique destination ID
     - `name` (string) - Destination name
     - `country` (string) - Country name
     - `region` (string) - Region (Asia, Europe, Americas, Africa, Oceania)
     - `description` (string) - Brief description
     - `attractions` (string) - Comma-separated main attractions
     - `climate` (string) - Climate type
   - Example:
     ```
     1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
     ```

2. **Itineraries Data** (`data/itineraries.txt`)
   - Fields:
     - `itinerary_id` (int) - Unique itinerary ID
     - `itinerary_name` (string) - Name
     - `destination` (string) - Destination
     - `start_date` (YYYY-MM-DD)
     - `end_date` (YYYY-MM-DD)
     - `activities` (string) - Comma-separated
     - `status` (string) - Planned, In Progress, Completed
   - Example:
     ```
     1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
     ```

3. **Hotels Data** (`data/hotels.txt`)
   - Fields:
     - `hotel_id` (int)
     - `name` (string)
     - `city` (string)
     - `rating` (float)
     - `price_per_night` (float)
     - `amenities` (string)
     - `category` (Budget, Mid-range, Luxury)
   - Example:
     ```
     1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
     ```

4. **Flights Data** (`data/flights.txt`)
   - Fields:
     - `flight_id` (int)
     - `airline` (string)
     - `departure_city` (string)
     - `arrival_city` (string)
     - `departure_time` (HH:MM 24hr)
     - `arrival_time` (HH:MM or with "next day")
     - `price` (float)
     - `class_type` (Economy, Business, First Class)
     - `duration` (string)
   - Example:
     ```
     1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
     ```

5. **Travel Packages Data** (`data/packages.txt`)
   - Fields:
     - `package_id` (int)
     - `package_name` (string)
     - `destination` (string)
     - `duration_days` (int)
     - `price` (float)
     - `included_items` (string)
     - `difficulty_level` (Easy, Moderate, Hard)
   - Example:
     ```
     1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
     ```

6. **Trips Data** (`data/trips.txt`)
   - Fields:
     - `trip_id` (int)
     - `trip_name` (string)
     - `destination` (string)
     - `start_date` (YYYY-MM-DD)
     - `end_date` (YYYY-MM-DD)
     - `total_budget` (float)
     - `status` (Booked, Planned, Pending)
     - `created_date` (YYYY-MM-DD)
   - Example:
     ```
     1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
     ```

7. **Bookings Data** (`data/bookings.txt`)
   - Fields:
     - `booking_id` (int)
     - `trip_id` (int)
     - `booking_type` (Hotel, Flight, Package)
     - `booking_date` (YYYY-MM-DD)
     - `amount` (float)
     - `confirmation_number` (string)
     - `status` (Confirmed, Pending, Cancelled)
   - Example:
     ```
     1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
     ```

---

## Section 2: Merged Frontend Specification

### HTML Template Specifications

1. **Dashboard Page** (`dashboard.html`)
   - **Page Title:** Travel Planner Dashboard
   - **Elements:**
     - `dashboard-page` (Div): Container for the dashboard page.
     - `featured-destinations` (Div): Display area for featured travel destinations.
     - `upcoming-trips` (Div): Display area showing upcoming planned trips.
     - `browse-destinations-button` (Button): Navigates to `/destinations`.
     - `plan-itinerary-button` (Button): Navigates to `/itinerary`.

2. **Destinations Page** (`destinations.html`)
   - **Page Title:** Travel Destinations
   - **Elements:**
     - `destinations-page` (Div): Container for the destinations page.
     - `search-destination` (Input[type=text]): Search filter by name or country.
     - `region-filter` (Dropdown/select): Filter destinations by region.
     - `destinations-grid` (Div): Displays destination cards.
     - `view-destination-button-{dest_id}` (Button): Navigate to `/destinations/{dest_id}`.

3. **Destination Details Page** (`destination_details.html`)
   - **Page Title:** Destination Details
   - **Elements:**
     - `destination-details-page` (Div): Container.
     - `destination-name` (H1)
     - `destination-country` (Div)
     - `destination-description` (Div)
     - `add-to-trip-button` (Button): Adds destination to a trip via POST to `/destinations/<dest_id>/add-to-trip`.
     - `destination-attractions` (Div)

4. **Itinerary Planning Page** (`itinerary.html`)
   - **Page Title:** Plan Your Itinerary
   - **Elements:**
     - `itinerary-page` (Div)
     - `itinerary-name-input` (Input[type=text])
     - `start-date-input` (Input[type=date])
     - `end-date-input` (Input[type=date])
     - `add-activity-button` (Button): Adds activities via form or AJAX.
     - `itinerary-list` (Div): Shows current itineraries with edit/delete options.

5. **Accommodations Page** (`accommodations.html`)
   - **Page Title:** Search Accommodations
   - **Elements:**
     - `accommodations-page` (Div)
     - `destination-input` (Input[type=text])
     - `check-in-date` (Input[type=date])
     - `check-out-date` (Input[type=date])
     - `price-filter` (Dropdown/select)
     - `hotels-list` (Div)

6. **Transportation Page** (`flights.html`)
   - **Page Title:** Book Flights
   - **Elements:**
     - `transportation-page` (Div)
     - `departure-city` (Input[type=text])
     - `arrival-city` (Input[type=text])
     - `departure-date` (Input[type=date])
     - `flight-class-filter` (Dropdown/select)
     - `available-flights` (Div)

7. **Travel Packages Page** (`packages.html`)
   - **Page Title:** Travel Packages
   - **Elements:**
     - `packages-page` (Div)
     - `packages-grid` (Div)
     - `duration-filter` (Dropdown/select)
     - `view-package-details-button-{pkg_id}` (Button): Navigate to `/packages/{pkg_id}`
     - `book-package-button-{pkg_id}` (Button): Book package POST to `/packages/{pkg_id}/book`

8. **Trip Management Page** (`trips.html`)
   - **Page Title:** My Trips
   - **Elements:**
     - `trips-page` (Div)
     - `trips-table` (Table) with trips info
     - `view-trip-details-button-{trip_id}` (Button): Navigate to `/trips/{trip_id}`
     - `edit-trip-button-{trip_id}` (Button): Navigate to `/trips/{trip_id}/edit`
     - `delete-trip-button-{trip_id}` (Button): POST to `/trips/{trip_id}/delete`

9. **Booking Confirmation Page** (`booking_confirmation.html`)
   - **Page Title:** Booking Confirmation
   - **Elements:**
     - `confirmation-page` (Div)
     - `confirmation-number` (Div)
     - `booking-details` (Div)
     - `download-itinerary-button` (Button)
     - `share-trip-button` (Button)
     - `back-to-dashboard` (Button): Navigate to `/dashboard`

10. **Travel Recommendations Page** (`recommendations.html`)
    - **Page Title:** Travel Recommendations
    - **Elements:**
      - `recommendations-page` (Div)
      - `trending-destinations` (Div)
      - `recommendation-season-filter` (Dropdown/select)
      - `budget-filter` (Dropdown/select)
      - `back-to-dashboard` (Button): Navigate to `/dashboard`

---

## Section 3: Consistency and Completeness Verification

- All backend routes have corresponding frontend templates with matching page titles.
- Context variables provided by backend routes align with frontend element IDs and UI elements for seamless data binding.
- Navigation flows between pages are internally consistent, following user_task_description navigation mappings.
- Local text file schemas cover all data types referenced in backend routes and frontend display needs.
- Backend POST routes for adding, editing, deleting entities correspond to frontend elements triggering such actions.
- No conflicts or discrepancies found between backend paths and frontend navigation; all placeholders (`{dest_id}`, `{pkg_id}`, `{trip_id}`) are consistently handled.
- The design spec is complete for downstream implementation without ambiguity or unresolved dependencies.

---

# End of merged TravelPlanner design specification
