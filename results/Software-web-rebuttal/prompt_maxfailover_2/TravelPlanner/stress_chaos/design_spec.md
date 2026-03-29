# TravelPlanner Design Specification

---

## 1. Flask Routes Specification

| Endpoint Path                  | HTTP Methods | Function Name             | Template Filename              | Context Variables                                                             | Navigation Mappings                                                                                                   |
|-------------------------------|--------------|---------------------------|-------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| /                             | GET          | dashboard_view            | templates/dashboard.html       | featured_destinations (list of dict), upcoming_trips (list of dict)           | browse-destinations-button: url_for('destinations_view')
plan-itinerary-button: url_for('itinerary_view')               |
| /destinations                 | GET          | destinations_view         | templates/destinations.html    | destinations (list of dict), search_query (str), selected_region (str)        | view-destination-button-{{ dest.dest_id }}: url_for('destination_detail_view', dest_id=dest.dest_id)                    |
| /destination/<int:dest_id>    | GET          | destination_detail_view   | templates/destination_detail.html | destination (dict), attractions (list of str)                         | add-to-trip-button: url_for('itinerary_view')                                                                             |
| /itinerary                   | GET, POST    | itinerary_view            | templates/itinerary.html       | itineraries (list of dict), form_errors (dict)                         | add-activity-button: JavaScript adds activity dynamically; navigation buttons to edit/delete itinerary items            |
| /accommodations              | GET          | accommodations_view       | templates/accommodations.html  | hotels (list of dict), filters (dict)                                    | filter changes reload page with query params                                                                            |
| /transportation             | GET          | transportation_view       | templates/transportation.html  | flights (list of dict), filters (dict)                                  | filter changes reload page with query params                                                                            |
| /packages                   | GET          | packages_view             | templates/packages.html        | packages (list of dict), duration_filter (str)                           | view-package-details-button-{{ pkg.package_id }}: url_for('package_detail_view', pkg_id=pkg.package_id)
book-package-button-{{ pkg.package_id }}: url_for('book_package', pkg_id=pkg.package_id) |
| /trips                      | GET          | trips_view                | templates/trips.html           | trips (list of dict)                                                      | view-trip-details-button-{{ trip.trip_id }}: url_for('trip_detail_view', trip_id=trip.trip_id)
edit-trip-button-{{ trip.trip_id }}: url_for('edit_trip', trip_id=trip.trip_id)
delete-trip-button-{{ trip.trip_id }}: url_for('delete_trip', trip_id=trip.trip_id) |
| /booking-confirmation/<int:booking_id> | GET  | booking_confirmation_view | templates/booking_confirmation.html | booking (dict), trip (dict)                                         | download-itinerary-button: triggers PDF download
back-to-dashboard: url_for('dashboard_view')                          |
| /recommendations            | GET          | recommendations_view      | templates/recommendations.html | recommendations (list of dict), filters (dict)                           | back-to-dashboard: url_for('dashboard_view')                                                                             |

---

## 2. HTML Templates Specification

### 2.1 templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Elements:
  - Div `dashboard-page`: Container for the dashboard
  - Div `featured-destinations`: Displays featured destinations list
  - Div `upcoming-trips`: Displays upcoming trips
  - Button `browse-destinations-button`: Navigates to the Destinations page
  - Button `plan-itinerary-button`: Navigates to the Itinerary Planning page
- Context Variables:
  - featured_destinations: List of dictionaries each representing a destination with fields {dest_id: int, name: str, country: str, image_url: str}
  - upcoming_trips: List of dictionaries each representing a trip with fields {trip_id: int, name: str, destination: str, start_date: str}
- Navigation Mappings:
  - `browse-destinations-button`: url_for('destinations_view')
  - `plan-itinerary-button`: url_for('itinerary_view')

### 2.2 templates/destinations.html
- Page Title: Travel Destinations
- Elements:
  - Div `destinations-page`: Container
  - Input `search-destination`: Search field text input
  - Dropdown `region-filter`: Filter for region
  - Div `destinations-grid`: Grid display of destinations
  - Buttons with ID pattern `view-destination-button-{{ dest.dest_id }}`
- Context Variables:
  - destinations: List of dictionaries {dest_id: int, name: str, country: str, region: str, image_url: str}
  - search_query: string for current search input
  - selected_region: string selected region filter
- Navigation Mappings:
  - Each button `view-destination-button-{{ dest.dest_id }}`: url_for('destination_detail_view', dest_id=dest.dest_id)

### 2.3 templates/destination_detail.html
- Page Title: Destination Details
- Elements:
  - Div `destination-details-page`: Container
  - H1 `destination-name`: Destination name
  - Div `destination-country`: Destination country
  - Div `destination-description`: Detailed description
  - Div `destination-attractions`: Attractions list
  - Button `add-to-trip-button`: Button to add destination to itinerary
- Context Variables:
  - destination: Dictionary with keys {dest_id: int, name: str, country: str, region: str, description: str}
  - attractions: List of strings
- Navigation Mappings:
  - `add-to-trip-button`: url_for('itinerary_view')

### 2.4 templates/itinerary.html
- Page Title: Plan Your Itinerary
- Elements:
  - Div `itinerary-page`: Container
  - Input `itinerary-name-input`: Text input
  - Input `start-date-input`: Date input
  - Input `end-date-input`: Date input
  - Button `add-activity-button`: Adds activities
  - Div `itinerary-list`: Shows list of itineraries with edit/delete options
- Context Variables:
  - itineraries: List of dictionaries {itinerary_id: int, itinerary_name: str, destination: str, start_date: str, end_date: str, activities: str, status: str}
  - form_errors: Dictionary of validation errors
- Navigation Mappings:
  - Edit/Delete buttons: link to corresponding routes handled with trip IDs

### 2.5 templates/accommodations.html
- Page Title: Search Accommodations
- Elements:
  - Div `accommodations-page`: Container
  - Input `destination-input`: Text input for city
  - Input `check-in-date`: Date input
  - Input `check-out-date`: Date input
  - Dropdown `price-filter`: Hotel price filter
  - Div `hotels-list`: List of hotel details
- Context Variables:
  - hotels: List of dictionaries {hotel_id: int, name: str, city: str, rating: float, price_per_night: float, amenities: str, category: str}
  - filters: Dictionary with current filter values
- Navigation Mappings:
  - Filtering triggers page reload with query params

### 2.6 templates/transportation.html
- Page Title: Book Flights
- Elements:
  - Div `transportation-page`: Container
  - Input `departure-city`: Text input
  - Input `arrival-city`: Text input
  - Input `departure-date`: Date input
  - Dropdown `flight-class-filter`: Flight class selector
  - Div `available-flights`: List showing flights
- Context Variables:
  - flights: List of dictionaries {flight_id: int, airline: str, departure_city: str, arrival_city: str, departure_time: str, arrival_time: str, price: float, class_type: str, duration: str}
  - filters: Dictionary for current filters
- Navigation Mappings:
  - Filtering triggers reload with query params

### 2.7 templates/packages.html
- Page Title: Travel Packages
- Elements:
  - Div `packages-page`: Container
  - Div `packages-grid`: Grid layout of packages
  - Dropdown `duration-filter`: Filter packages by duration
  - Buttons with ID patterns `view-package-details-button-{{ pkg.package_id }}` and `book-package-button-{{ pkg.package_id }}`
- Context Variables:
  - packages: List of dictionaries {package_id: int, package_name: str, destination: str, duration_days: int, price: float, included_items: str, difficulty_level: str}
  - duration_filter: Current duration filter string
- Navigation Mappings:
  - `view-package-details-button-{{ pkg.package_id }}`: url_for('package_detail_view', pkg_id=pkg.package_id)
  - `book-package-button-{{ pkg.package_id }}`: url_for('book_package', pkg_id=pkg.package_id)

### 2.8 templates/trips.html
- Page Title: My Trips
- Elements:
  - Div `trips-page`: Container
  - Table `trips-table`: Tabular listing of trips
  - Buttons with ID patterns `view-trip-details-button-{{ trip.trip_id }}`, `edit-trip-button-{{ trip.trip_id }}`, `delete-trip-button-{{ trip.trip_id }}`
- Context Variables:
  - trips: List of dictionaries {trip_id: int, trip_name: str, destination: str, start_date: str, end_date: str, total_budget: float, status: str, created_date: str}
- Navigation Mappings:
  - View/Edit/Delete buttons: url_for with respective trip_id

### 2.9 templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Elements:
  - Div `confirmation-page`: Container
  - Div `confirmation-number`: Booking number display
  - Div `booking-details`: Booking info details
  - Button `download-itinerary-button`: Initiates itinerary download (PDF)
  - Button `share-trip-button`: Share trip details
  - Button `back-to-dashboard`: Navigate to dashboard
- Context Variables:
  - booking: Dictionary of booking data
  - trip: Dictionary of related trip data
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_view')

### 2.10 templates/recommendations.html
- Page Title: Travel Recommendations
- Elements:
  - Div `recommendations-page`: Container
  - Div `trending-destinations`: Trending destinations display
  - Dropdown `recommendation-season-filter`: Filter by season
  - Dropdown `budget-filter`: Budget filter
  - Button `back-to-dashboard`: Navigate to Dashboard
- Context Variables:
  - recommendations: List of dicts with recommended trips/destinations
  - filters: Dictionary of current filters
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_view')

---

## 3. Data File Schemas

### 3.1 data/destinations.txt
- Field Order and Names:
  dest_id|name|country|region|description|attractions|climate
- Description: Information about travel destinations
- Example:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```
- No header row

### 3.2 data/itineraries.txt
- Field Order and Names:
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
- Description: User created travel itineraries
- Example:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```
- No header row

### 3.3 data/hotels.txt
- Field Order and Names:
  hotel_id|name|city|rating|price_per_night|amenities|category
- Description: Available hotels data
- Example:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```
- No header row

### 3.4 data/flights.txt
- Field Order and Names:
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
- Description: Flights data for bookings
- Example:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```
- No header row

### 3.5 data/packages.txt
- Field Order and Names:
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
- Description: Pre-designed travel packages
- Example:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```
- No header row

### 3.6 data/trips.txt
- Field Order and Names:
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
- Description: User trips data
- Example:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```
- No header row

### 3.7 data/bookings.txt
- Field Order and Names:
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
- Description: Booking confirmations data
- Example:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
  ```
- No header row

---

This detailed design specification fully supports independent backend and frontend development of the TravelPlanner web application. It provides complete Flask route definitions, template element specifications, context variables, and data file schemas.
