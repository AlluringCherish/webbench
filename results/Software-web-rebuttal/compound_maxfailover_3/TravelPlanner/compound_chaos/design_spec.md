# TravelPlanner Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                   | HTTP Methods | Function Name             | Template File                    | Context Variables                                                                                                                                                                                                                | Navigation Actions Triggered by Buttons/Links                                                                                |
|---------------------------------|--------------|---------------------------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `/`                             | GET          | dashboard                 | templates/dashboard.html          | `featured_destinations`: list of dict {`dest_id` (int), `name` (str), `country` (str)}<br>`upcoming_trips`: list of dict {`trip_id` (int), `trip_name` (str), `start_date` (str), `end_date` (str)}                                 | `browse-destinations-button` → `/destinations`<br>`plan-itinerary-button` → `/itinerary`                          |
| `/destinations`                 | GET, POST    | destinations              | templates/destinations.html       | `destinations`: list of dict {`dest_id` (int), `name` (str), `country` (str), `region` (str)}<br>`search_query`: str (empty string on GET)<br>`region_filter`: str (one of Asia, Europe, Americas, Africa, Oceania or empty)            | `view-destination-button-{{ dest_id }}` → `/destinations/<int:dest_id>`                                               |
| `/destinations/<int:dest_id>`   | GET, POST   | destination_details       | templates/destination_details.html | `destination`: dict {`dest_id` (int), `name` (str), `country` (str), `description` (str), `attractions` (str), `climate` (str)}                                                                                                 | `add-to-trip-button` triggers addition to itinerary (POST to `/itinerary` or equivalent)                                    |
| `/itinerary`                   | GET, POST    | plan_itinerary            | templates/itinerary.html          | `itineraries`: list of dict {`itinerary_id` (int), `itinerary_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `activities` (str), `status` (str)}                                                          | `add-activity-button` (POST within page)<br>Editing/Deleting via actions per itinerary item                                  |
| `/accommodations`              | GET, POST    | accommodations            | templates/accommodations.html     | `hotels`: list of dict {`hotel_id` (int), `name` (str), `city` (str), `rating` (float), `price_per_night` (float), `amenities` (str), `category` (str)}<br>`filters`: dict with keys: `destination` (str), `check_in` (str), `check_out` (str), `price_range` (str) | No specified navigation links in hotels list                                                                               |
| `/transportation`              | GET, POST    | transportation            | templates/transportation.html     | `flights`: list of dict {`flight_id` (int), `airline` (str), `departure_city` (str), `arrival_city` (str), `departure_time` (str), `arrival_time` (str), `price` (float), `class_type` (str), `duration` (str)}<br>`filters`: dict {`departure_city`, `arrival_city`, `departure_date`, `flight_class`} | No specified navigation links in flights list                                                                               |
| `/packages`                   | GET, POST    | travel_packages           | templates/packages.html           | `packages`: list of dict {`package_id` (int), `package_name` (str), `destination` (str), `duration_days` (int), `price` (float)}<br>`duration_filter`: str (3-5 days, 7-10 days, 14+ days or empty)                              | `view-package-details-button-{{ pkg_id }}` → `/packages/<int:pkg_id>`<br>`book-package-button-{{ pkg_id }}` → `/packages/<int:pkg_id>/book`      |
| `/packages/<int:pkg_id>`        | GET          | package_details           | templates/package_details.html    | `package`: dict {`package_id` (int), `package_name` (str), `destination` (str), `duration_days` (int), `price` (float), `included_items` (str), `difficulty_level` (str)}                                                              | Navigation not specified                                                                                                    |
| `/packages/<int:pkg_id>/book`   | POST         | book_package              | N/A (redirect)                   | N/A                                                                                                                                                                                                                             | Redirects to `/booking_confirmation?booking_id=<id>`                                                                        |
| `/trips`                     | GET, POST    | trips                     | templates/trips.html              | `trips`: list of dict {`trip_id` (int), `trip_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `status` (str)}                                                                                              | `view-trip-details-button-{{ trip_id }}` → `/trips/<int:trip_id>`<br>`edit-trip-button-{{ trip_id }}` → `/trips/<int:trip_id>/edit`<br>`delete-trip-button-{{ trip_id }}` → `/trips/<int:trip_id>/delete` |
| `/trips/<int:trip_id>`         | GET, POST    | trip_details              | templates/trip_details.html       | `trip`: dict {`trip_id` (int), `trip_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `total_budget` (float), `status` (str), `created_date` (str)}<br>`bookings`: list of dict {`booking_id` (int), `booking_type` (str), `booking_date` (str), `amount` (float), `confirmation_number` (str), `status` (str)} | No navigation buttons specified                                                                                             |
| `/booking_confirmation`         | GET          | booking_confirmation      | templates/booking_confirmation.html | `booking`: dict {`booking_id` (int), `trip_id` (int), `booking_type` (str), `booking_date` (str), `amount` (float), `confirmation_number` (str), `status` (str)}                                                                     | `download-itinerary-button` → download PDF endpoint<br>`share-trip-button`: share functionality (implementation-specific)<br>`back-to-dashboard` → `/`              |
| `/recommendations`           | GET, POST    | travel_recommendations     | templates/recommendations.html    | `recommendations`: list of dict {`dest_id` (int), `name` (str), `country` (str), `popularity_rank` (int)}<br>`filters`: dict {`season` (str), `budget` (str)}                                                                      | `back-to-dashboard` → `/`                                                                                             |

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html

- **Page Title**: Travel Planner Dashboard

- **Element IDs:**

  | ID                          | HTML Type | Functional Description                     |
  |-----------------------------|-----------|--------------------------------------------|
  | dashboard-page              | Div       | Container for the dashboard page            |
  | featured-destinations       | Div       | Displays featured travel destinations       |
  | upcoming-trips              | Div       | Displays upcoming planned trips             |
  | browse-destinations-button | Button    | Navigates to destinations page (/destinations) |
  | plan-itinerary-button       | Button    | Navigates to itinerary planning page (/itinerary) |

- **Context Variables:**

  - `featured_destinations`: list of dicts with fields: `dest_id` (int), `name` (str), `country` (str)
  - `upcoming_trips`: list of dicts with fields: `trip_id` (int), `trip_name` (str), `start_date` (str), `end_date` (str)

- **Navigation Mappings:**

  - `browse-destinations-button` calls `url_for('destinations')`
  - `plan-itinerary-button` calls `url_for('plan_itinerary')`

---

### 2. templates/destinations.html

- **Page Title**: Travel Destinations

- **Element IDs:**

  | ID                          | HTML Type | Functional Description                          |
  |-----------------------------|-----------|------------------------------------------------|
  | destinations-page           | Div       | Container for the destinations page             |
  | search-destination          | Input     | Text input to search destinations by name or country |
  | region-filter              | Dropdown  | Dropdown to filter destinations by region       |
  | destinations-grid          | Div       | Grid displaying destination cards                |
  | view-destination-button-{{ dest.dest_id }} | Button    | Button to view details for each destination     |

- **Context Variables:**

  - `destinations`: list of dicts with fields: `dest_id` (int), `name` (str), `country` (str), `region` (str)
  - `search_query`: str
  - `region_filter`: str

- **Navigation Mappings:**

  - Each `view-destination-button-{{ dest.dest_id }}` calls `url_for('destination_details', dest_id=dest.dest_id)`

---

### 3. templates/destination_details.html

- **Page Title**: Destination Details

- **Element IDs:**

  | ID                    | HTML Type | Functional Description                     |
  |-----------------------|-----------|--------------------------------------------|
  | destination-details-page | Div       | Container for the destination details page |
  | destination-name       | H1        | Destination name                           |
  | destination-country    | Div       | Destination country                        |
  | destination-description| Div       | Detailed description                       |
  | add-to-trip-button     | Button    | Adds destination to trip                   |
  | destination-attractions| Div       | Attractions and activities                 |

- **Context Variables:**

  - `destination`: dict {`dest_id` (int), `name` (str), `country` (str), `description` (str), `attractions` (str), `climate` (str)}

- **Navigation Mappings:**

  - `add-to-trip-button`: form POST to /itinerary or a redirect after POST

---

### 4. templates/itinerary.html

- **Page Title**: Plan Your Itinerary

- **Element IDs:**

  | ID                   | HTML Type | Functional Description                          |
  |----------------------|-----------|------------------------------------------------|
  | itinerary-page       | Div       | Container for itinerary page                    |
  | itinerary-name-input | Input     | Enter itinerary name                             |
  | start-date-input     | Input (date) | Select trip start date                         |
  | end-date-input       | Input (date) | Select trip end date                           |
  | add-activity-button  | Button    | Add activity to itinerary                       |
  | itinerary-list       | Div       | List created itineraries with edit/delete      |

- **Context Variables:**

  - `itineraries`: list of dict {`itinerary_id` (int), `itinerary_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `activities` (str), `status` (str)}

- **Navigation Mappings:**

  - `add-activity-button`: POST handled on this page
  - itinerary-list edit/delete: URLs not explicitly specified (assumed internal)

---

### 5. templates/accommodations.html

- **Page Title**: Search Accommodations

- **Element IDs:**

  | ID                | HTML Type | Functional Description                              |
  |-------------------|-----------|----------------------------------------------------|
  | accommodations-page | Div       | Container for accommodations page                   |
  | destination-input  | Input     | Enter destination city                               |
  | check-in-date     | Input (date) | Select check-in date                             |
  | check-out-date    | Input (date) | Select check-out date                            |
  | price-filter      | Dropdown  | Filter hotels by price range                         |
  | hotels-list       | Div       | List of hotels (name, rating, price, amenities)    |

- **Context Variables:**

  - `hotels`: list of dict {`hotel_id` (int), `name` (str), `city` (str), `rating` (float), `price_per_night` (float), `amenities` (str), `category` (str)}
  - `filters`: dict {destination (str), check_in (str), check_out (str), price_range (str)}

- **Navigation Mappings:**

  - No specified navigation buttons/links

---

### 6. templates/transportation.html

- **Page Title**: Book Flights

- **Element IDs:**

  | ID                 | HTML Type | Functional Description                              |
  |--------------------|-----------|----------------------------------------------------|
  | transportation-page | Div       | Container for transportation page                   |
  | departure-city     | Input     | Enter departure city                                |
  | arrival-city       | Input     | Enter arrival city                                  |
  | departure-date     | Input (date) | Select departure date                             |
  | flight-class-filter| Dropdown  | Filter by flight class (Economy, Business, First) |
  | available-flights  | Div       | List of available flights (airlines, times, prices)|

- **Context Variables:**

  - `flights`: list of dict {`flight_id` (int), `airline` (str), `departure_city` (str), `arrival_city` (str), `departure_time` (str), `arrival_time` (str), `price` (float), `class_type` (str), `duration` (str)}
  - `filters`: dict {departure_city (str), arrival_city (str), departure_date (str), flight_class (str)}

- **Navigation Mappings:**

  - No specified navigation buttons/links

---

### 7. templates/packages.html

- **Page Title**: Travel Packages

- **Element IDs:**

  | ID                          | HTML Type | Functional Description                             |
  |-----------------------------|-----------|---------------------------------------------------|
  | packages-page               | Div       | Container for packages page                        |
  | packages-grid              | Div       | Grid showing travel package cards                  |
  | duration-filter            | Dropdown  | Filter packages by duration                        |
  | view-package-details-button-{{ pkg.package_id }} | Button    | View package details                                |
  | book-package-button-{{ pkg.package_id }}         | Button    | Book selected package                               |

- **Context Variables:**

  - `packages`: list of dict {`package_id` (int), `package_name` (str), `destination` (str), `duration_days` (int), `price` (float)}
  - `duration_filter`: str

- **Navigation Mappings:**

  - `view-package-details-button-{{ pkg.package_id }}` → `url_for('package_details', pkg_id=pkg.package_id)`
  - `book-package-button-{{ pkg.package_id }}` → `url_for('book_package', pkg_id=pkg.package_id)`

---

### 8. templates/trips.html

- **Page Title**: My Trips

- **Element IDs:**

  | ID                          | HTML Type | Functional Description                            |
  |-----------------------------|-----------|--------------------------------------------------|
  | trips-page                 | Div       | Container for trips page                           |
  | trips-table                | Table     | Table displaying all trips                        |
  | view-trip-details-button-{{ trip.trip_id }} | Button    | View trip details                                  |
  | edit-trip-button-{{ trip.trip_id }}          | Button    | Edit trip                                         |
  | delete-trip-button-{{ trip.trip_id }}        | Button    | Delete trip                                       |

- **Context Variables:**

  - `trips`: list of dict {`trip_id` (int), `trip_name` (str), `destination` (str), `start_date` (str), `end_date` (str), `status` (str)}

- **Navigation Mappings:**

  - `view-trip-details-button-{{ trip.trip_id }}` → `url_for('trip_details', trip_id=trip.trip_id)`
  - `edit-trip-button-{{ trip.trip_id }}` → `url_for('edit_trip', trip_id=trip.trip_id)`
  - `delete-trip-button-{{ trip.trip_id }}` → `url_for('delete_trip', trip_id=trip.trip_id)`

---

### 9. templates/booking_confirmation.html

- **Page Title**: Booking Confirmation

- **Element IDs:**

  | ID                       | HTML Type | Functional Description                            |
  |--------------------------|-----------|--------------------------------------------------|
  | confirmation-page       | Div       | Container for booking confirmation page           |
  | confirmation-number     | Div       | Displays booking confirmation number              |
  | booking-details         | Div       | Displays detailed booking information             |
  | download-itinerary-button| Button    | Download trip itinerary as PDF                      |
  | share-trip-button       | Button    | Share trip details                                 |
  | back-to-dashboard       | Button    | Navigate back to dashboard                         |

- **Context Variables:**

  - `booking`: dict {`booking_id` (int), `trip_id` (int), `booking_type` (str), `booking_date` (str), `amount` (float), `confirmation_number` (str), `status` (str)}

- **Navigation Mappings:**

  - `download-itinerary-button` → `url_for('download_itinerary', booking_id=booking.booking_id)` (assumed endpoint)
  - `share-trip-button`: share functionality (implementation-specific)
  - `back-to-dashboard` → `url_for('dashboard')`

---

### 10. templates/recommendations.html

- **Page Title**: Travel Recommendations

- **Element IDs:**

  | ID                          | HTML Type | Functional Description                           |
  |-----------------------------|-----------|-------------------------------------------------|
  | recommendations-page       | Div       | Container for recommendations page               |
  | trending-destinations      | Div       | Displays trending destinations ranked popularity |
  | recommendation-season-filter | Dropdown  | Filter by travel season                           |
  | budget-filter              | Dropdown  | Filter by budget range                            |
  | back-to-dashboard          | Button    | Navigate back to dashboard                        |

- **Context Variables:**

  - `recommendations`: list of dict {`dest_id` (int), `name` (str), `country` (str), `popularity_rank` (int)}
  - `filters`: dict {`season` (str), `budget` (str)}

- **Navigation Mappings:**

  - `back-to-dashboard` → `url_for('dashboard')`

---

## Section 3: Data File Schemas

### 1. data/destinations.txt

- **Fields and Order:**

  1. dest_id (int)

  2. name (str)

  3. country (str)

  4. region (str)

  5. description (str)

  6. attractions (str)

  7. climate (str)

- **Description:** Stores travel destinations with detailed descriptions and attractions.

- **Example rows:**

  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

- **Note:** No header row exists.

---

### 2. data/itineraries.txt

- **Fields and Order:**

  1. itinerary_id (int)

  2. itinerary_name (str)

  3. destination (str)

  4. start_date (str, date formatted YYYY-MM-DD)

  5. end_date (str, date formatted YYYY-MM-DD)

  6. activities (str)

  7. status (str) [Planned, In Progress, Completed]

- **Description:** Stores user-created itineraries including activities and statuses.

- **Example rows:**

  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

- **Note:** No header row exists.

---

### 3. data/hotels.txt

- **Fields and Order:**

  1. hotel_id (int)

  2. name (str)

  3. city (str)

  4. rating (float)

  5. price_per_night (float)

  6. amenities (str, comma separated)

  7. category (str) [Budget, Mid-range, Luxury]

- **Description:** Stores hotel information including rating, price, and amenities.

- **Example rows:**

  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

- **Note:** No header row exists.

---

### 4. data/flights.txt

- **Fields and Order:**

  1. flight_id (int)

  2. airline (str)

  3. departure_city (str)

  4. arrival_city (str)

  5. departure_time (str, e.g., 10:00)

  6. arrival_time (str, e.g., 22:30, or with "next day" suffix)

  7. price (float)

  8. class_type (str) [Economy, Business, First Class]

  9. duration (str, e.g., "7 hours 30 minutes")

- **Description:** Stores flights with schedules and prices.

- **Example rows:**

  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

- **Note:** No header row exists.

---

### 5. data/packages.txt

- **Fields and Order:**

  1. package_id (int)

  2. package_name (str)

  3. destination (str)

  4. duration_days (int)

  5. price (float)

  6. included_items (str, comma separated)

  7. difficulty_level (str) [Easy, Moderate, Difficult]

- **Description:** Stores travel packages with pricing, duration, and included items.

- **Example rows:**

  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

- **Note:** No header row exists.

---

### 6. data/trips.txt

- **Fields and Order:**

  1. trip_id (int)

  2. trip_name (str)

  3. destination (str)

  4. start_date (str, date formatted YYYY-MM-DD)

  5. end_date (str, date formatted YYYY-MM-DD)

  6. total_budget (float)

  7. status (str) [Booked, Planned, Pending]

  8. created_date (str, date formatted YYYY-MM-DD)

- **Description:** Stores user trips with budget and status.

- **Example rows:**

  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

- **Note:** No header row exists.

---

### 7. data/bookings.txt

- **Fields and Order:**

  1. booking_id (int)

  2. trip_id (int)

  3. booking_type (str) [Hotel, Flight, Package]

  4. booking_date (str, date formatted YYYY-MM-DD)

  5. amount (float)

  6. confirmation_number (str)

  7. status (str) [Confirmed, Pending]

- **Description:** Stores booking records with confirmation and status.

- **Example rows:**

  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```

- **Note:** No header row exists.

---

This design specification document provides complete and clear definitions for routes, templates, and data files required for independent backend and frontend development of the TravelPlanner web application. All IDs, variable types, and navigation mappings are explicitly defined as detailed above.
