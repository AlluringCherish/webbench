# TravelPlanner Backend Design Specification

---

## Section 1: Flask Backend Routes Specification

This section defines all Flask routes, their HTTP methods, function names, template files rendered, context variables used, and any redirect or form handling behavior.

### 1. Dashboard Page
- **Route:** `/` or `/dashboard`
- **Method:** GET
- **Function:** `dashboard()`
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_destinations` (list of destination dicts)
  - `upcoming_trips` (list of trip dicts)
- **Description:** Displays main hub with featured destinations and upcoming trips.

### 2. Destinations Page
- **Route:** `/destinations`
- **Method:** GET
- **Function:** `list_destinations()`
- **Template:** `destinations.html`
- **Context Variables:**
  - `destinations` (filtered list based on optional query parameters)
  - `search_query` (string, optional)
  - `region_filter` (string, optional: Asia, Europe, Americas, Africa, Oceania)
- **Description:** Lists all destinations with optional search and region filter.

### 3. Destination Details Page
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

### 4. Itinerary Planning Page
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

### 5. Accommodations Page
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

### 6. Transportation Page
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

### 7. Travel Packages Page
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

### 8. Trip Management Page
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

### 9. Booking Confirmation Page
- **Route:** `/booking/confirmation/<string:confirmation_number>`
- **Method:** GET
- **Function:** `booking_confirmation(confirmation_number)`
- **Template:** `booking_confirmation.html`
- **Context Variables:**
  - `booking` (booking details dict)
  - Related trip info if needed

### 10. Travel Recommendations Page
- **Route:** `/recommendations`
- **Method:** GET
- **Function:** `recommendations()`
- **Template:** `recommendations.html`
- **Context Variables:**
  - `trending_destinations` (list sorted by popularity)
  - `season_filter` (Spring, Summer, Fall, Winter)
  - `budget_filter` (Low, Medium, High)

- **Route:** `/back-to-dashboard`
- **Method:** GET
- **Function:** `back_to_dashboard()`
- **Action:** Redirects to `/dashboard`

---

## Section 2: Local Text File Data Schemas

Below are detailed schemas for each text data file used in the application. All files are pipe-delimited (`|`) and stored in the `data/` directory.

---

### 1. Destinations Data
- **Filename:** `data/destinations.txt`
- **Fields:**
  - `dest_id` (int) - Unique destination ID
  - `name` (string) - Destination name
  - `country` (string) - Country name
  - `region` (string) - Geographical region (Asia, Europe, etc.)
  - `description` (string) - Brief description
  - `attractions` (string) - Comma-separated list of main attractions
  - `climate` (string) - Climate type

- **Example Row:**
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  ```

---

### 2. Itineraries Data
- **Filename:** `data/itineraries.txt`
- **Fields:**
  - `itinerary_id` (int) - Unique itinerary ID
  - `itinerary_name` (string) - Name for itinerary
  - `destination` (string) - Destination name
  - `start_date` (date string `YYYY-MM-DD`)
  - `end_date` (date string `YYYY-MM-DD`)
  - `activities` (string) - Comma-separated activities
  - `status` (string) - Status (Planned, In Progress, Completed)

- **Example Row:**
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  ```

---

### 3. Hotels Data
- **Filename:** `data/hotels.txt`
- **Fields:**
  - `hotel_id` (int) - Unique hotel ID
  - `name` (string) - Hotel name
  - `city` (string) - City where the hotel is located
  - `rating` (float) - Hotel star rating (e.g., 4.5)
  - `price_per_night` (float) - Price in USD
  - `amenities` (string) - Comma-separated list of amenities
  - `category` (string) - Hotel category (Budget, Mid-range, Luxury)

- **Example Row:**
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  ```

---

### 4. Flights Data
- **Filename:** `data/flights.txt`
- **Fields:**
  - `flight_id` (int) - Unique flight ID
  - `airline` (string) - Airline name
  - `departure_city` (string) - City of departure
  - `arrival_city` (string) - Arrival city
  - `departure_time` (string) - Departure time (HH:MM, 24hr)
  - `arrival_time` (string) - Arrival time, can include "next day" e.g., "15:20 next day"
  - `price` (float) - Price in USD
  - `class_type` (string) - Flight class (Economy, Business, First Class)
  - `duration` (string) - Flight duration text

- **Example Row:**
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  ```

---

### 5. Travel Packages Data
- **Filename:** `data/packages.txt`
- **Fields:**
  - `package_id` (int) - Unique package ID
  - `package_name` (string) - Name of package
  - `destination` (string) - Destination name
  - `duration_days` (int) - Duration in days
  - `price` (float) - Price in USD
  - `included_items` (string) - Comma-separated included items (Hotel, Flights, etc.)
  - `difficulty_level` (string) - Level (Easy, Moderate, Hard)

- **Example Row:**
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  ```

---

### 6. Trips Data
- **Filename:** `data/trips.txt`
- **Fields:**
  - `trip_id` (int) - Unique trip ID
  - `trip_name` (string) - Trip name
  - `destination` (string) - Destination name
  - `start_date` (date string `YYYY-MM-DD`)
  - `end_date` (date string `YYYY-MM-DD`)
  - `total_budget` (float) - Total budget in USD
  - `status` (string) - Status (Booked, Planned, Pending)
  - `created_date` (date string `YYYY-MM-DD`)

- **Example Row:**
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  ```

---

### 7. Bookings Data
- **Filename:** `data/bookings.txt`
- **Fields:**
  - `booking_id` (int) - Unique booking ID
  - `trip_id` (int) - Associated trip ID
  - `booking_type` (string) - Booking type (Hotel, Flight, Package)
  - `booking_date` (date string `YYYY-MM-DD`)
  - `amount` (float) - Booking price
  - `confirmation_number` (string) - Confirmation code
  - `status` (string) - Status (Confirmed, Pending, Cancelled)

- **Example Row:**
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  ```

---

# End of Backend Design Specification
