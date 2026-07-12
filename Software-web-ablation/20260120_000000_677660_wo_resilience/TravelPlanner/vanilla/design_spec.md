# TravelPlanner Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Endpoint                     | HTTP Methods | Function Name                | Template File                   | Context Variables (type & structure)                                                                                             | Navigation Actions Triggered by Buttons/Links                                                                        |
|----------------------------------|--------------|-----------------------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| / (dashboard)                    | GET          | dashboard                   | dashboard.html                 | featured_destinations: list of dict {dest_id:int, name:str, country:str}                                                        
upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str}                        | browse-destinations-button → url_for('destinations') 
plan-itinerary-button → url_for('plan_itinerary')                |
| /destinations                   | GET          | destinations                | destinations.html              | destinations: list of dict {dest_id:int, name:str, country:str, region:str}                                                     | view-destination-button-{{dest_id}} → url_for('destination_details', dest_id=dest_id)                                 |
| /destinations/<int:dest_id>     | GET          | destination_details         | destination_details.html       | destination: dict {dest_id:int, name:str, country:str, description:str, attractions:str}                                        | add-to-trip-button → POST to add destination to trip or redirect; navigation stays on the same page                    |
| /itinerary                     | GET, POST    | plan_itinerary              | itinerary.html                 | GET: itineraries: list of dict {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
POST: form data to add/edit itinerary                                | add-activity-button → triggers POST request to add activity; navigation remains on itinerary page                      |
| /accommodations                | GET          | accommodations              | accommodations.html            | hotels: list of dict {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}          |                                                                                                                      |
| /transportation                | GET          | transportation              | transportation.html            | flights: list of dict {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}      |                                                                                                                      |
| /packages                      | GET          | packages                   | packages.html                  | packages: list of dict {package_id:int, package_name:str, destination:str, duration_days:int, price:float}                      | view-package-details-button-{{pkg_id}} → url_for('package_details', pkg_id=pkg_id)
book-package-button-{{pkg_id}} → POST to book package   |
| /trips                        | GET          | trips                      | trips.html                    | trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}                      | view-trip-details-button-{{trip_id}} → url_for('trip_details', trip_id=trip_id)
edit-trip-button-{{trip_id}} → url_for('edit_trip', trip_id=trip_id)
delete-trip-button-{{trip_id}} → POST to delete trip                                        |
| /booking_confirmation         | GET          | booking_confirmation       | booking_confirmation.html     | booking: dict {confirmation_number:str, booking_details:str}                                                                     | download-itinerary-button → triggers file download
share-trip-button → triggers sharing flow
back-to-dashboard → url_for('dashboard')|
| /recommendations              | GET          | recommendations            | recommendations.html           | trending_destinations: list of dict {dest_id:int, name:str, popularity_rank:int}
filters: dict {recommendation_season:str, budget:str}                  | back-to-dashboard → url_for('dashboard')                                                                              |

---

## Section 2: HTML Templates Specification

### 1. templates/dashboard.html
- Page Title: Travel Planner Dashboard
- Element IDs:
  - dashboard-page: Div, Container for the dashboard page.
  - featured-destinations: Div, Display of featured travel destinations.
  - upcoming-trips: Div, Display of upcoming planned trips.
  - browse-destinations-button: Button, Navigates to Destinations page.
  - plan-itinerary-button: Button, Navigates to Itinerary Planning page.
- Context Variables:
  - featured_destinations: List of dicts with {dest_id:int, name:str, country:str}
  - upcoming_trips: List of dicts with {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str}
- Navigation Mappings:
  - browse-destinations-button: url_for('destinations')
  - plan-itinerary-button: url_for('plan_itinerary')

### 2. templates/destinations.html
- Page Title: Travel Destinations
- Element IDs:
  - destinations-page: Div, Container for destinations page.
  - search-destination: Input, Text input for name or country search.
  - region-filter: Dropdown, Options: Asia, Europe, Americas, Africa, Oceania.
  - destinations-grid: Div, Grid displaying destination cards.
  - view-destination-button-{{dest.dest_id}}: Button, View details for each destination.
- Context Variables:
  - destinations: List of dicts with {dest_id:int, name:str, country:str, region:str}
- Navigation Mappings:
  - view-destination-button-{{dest.dest_id}}: url_for('destination_details', dest_id=dest.dest_id)

### 3. templates/destination_details.html
- Page Title: Destination Details
- Element IDs:
  - destination-details-page: Div, Container for destination details.
  - destination-name: H1, Displays destination name.
  - destination-country: Div, Displays destination country.
  - destination-description: Div, Displays detailed description.
  - add-to-trip-button: Button, Adds destination to trip.
  - destination-attractions: Div, Shows main attractions.
- Context Variables:
  - destination: Dict {dest_id:int, name:str, country:str, description:str, attractions:str}
- Navigation Mappings:
  - add-to-trip-button: POST action to add destination to itinerary; stays on this page.

### 4. templates/itinerary.html
- Page Title: Plan Your Itinerary
- Element IDs:
  - itinerary-page: Div, Container for itinerary planning.
  - itinerary-name-input: Input, Text input for itinerary name.
  - start-date-input: Input (date), Start date selector.
  - end-date-input: Input (date), End date selector.
  - add-activity-button: Button, Adds new activity to itinerary.
  - itinerary-list: Div, Lists created itineraries with edit/delete.
- Context Variables:
  - itineraries: List of dicts {itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
- Navigation Mappings:
  - add-activity-button: POST form submission on the same page.

### 5. templates/accommodations.html
- Page Title: Search Accommodations
- Element IDs:
  - accommodations-page: Div, Container for accommodations.
  - destination-input: Input, Destination city input.
  - check-in-date: Input (date), Check-in date selector.
  - check-out-date: Input (date), Check-out date selector.
  - price-filter: Dropdown, Options: Budget, Mid-range, Luxury.
  - hotels-list: Div, List of hotels with details.
- Context Variables:
  - hotels: List of dicts {hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
- Navigation Mappings: None applicable.

### 6. templates/transportation.html
- Page Title: Book Flights
- Element IDs:
  - transportation-page: Div, Container for flight booking.
  - departure-city: Input, Departure city input.
  - arrival-city: Input, Arrival city input.
  - departure-date: Input (date), Departure date selector.
  - flight-class-filter: Dropdown, Options: Economy, Business, First Class.
  - available-flights: Div, List of flights with details.
- Context Variables:
  - flights: List of dicts {flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
- Navigation Mappings: None applicable.

### 7. templates/packages.html
- Page Title: Travel Packages
- Element IDs:
  - packages-page: Div, Container for packages.
  - packages-grid: Div, Grid of package cards.
  - duration-filter: Dropdown, Options: 3-5 days, 7-10 days, 14+ days.
  - view-package-details-button-{{pkg.package_id}}: Button, View package details.
  - book-package-button-{{pkg.package_id}}: Button, Book package.
- Context Variables:
  - packages: List of dicts {package_id:int, package_name:str, destination:str, duration_days:int, price:float}
- Navigation Mappings:
  - view-package-details-button-{{pkg.package_id}}: url_for('package_details', pkg_id=pkg.package_id)
  - book-package-button-{{pkg.package_id}}: POST action to book package

### 8. templates/trips.html
- Page Title: My Trips
- Element IDs:
  - trips-page: Div, Container for trips.
  - trips-table: Table, Displays trips with columns: Destination, Dates, Status.
  - view-trip-details-button-{{trip.trip_id}}: Button, View trip details.
  - edit-trip-button-{{trip.trip_id}}: Button, Edit trip.
  - delete-trip-button-{{trip.trip_id}}: Button, Delete trip.
- Context Variables:
  - trips: List of dicts {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
- Navigation Mappings:
  - view-trip-details-button-{{trip.trip_id}}: url_for('trip_details', trip_id=trip.trip_id)
  - edit-trip-button-{{trip.trip_id}}: url_for('edit_trip', trip_id=trip.trip_id)
  - delete-trip-button-{{trip.trip_id}}: POST action to delete trip

### 9. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page: Div, Container for confirmation page.
  - confirmation-number: Div, Displays booking confirmation number.
  - booking-details: Div, Detailed booking info.
  - download-itinerary-button: Button, Downloads itinerary PDF.
  - share-trip-button: Button, Shares trip details.
  - back-to-dashboard: Button, Navigates back to Dashboard.
- Context Variables:
  - booking: Dict {confirmation_number:str, booking_details:str}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
  - download-itinerary-button and share-trip-button: triggers actions (no route)

### 10. templates/recommendations.html
- Page Title: Travel Recommendations
- Element IDs:
  - recommendations-page: Div, Container for recommendations.
  - trending-destinations: Div, Displays trending destinations ranked.
  - recommendation-season-filter: Dropdown, Options: Spring, Summer, Fall, Winter.
  - budget-filter: Dropdown, Options: Low, Medium, High.
  - back-to-dashboard: Button, Navigates back to Dashboard.
- Context Variables:
  - trending_destinations: List of dicts {dest_id:int, name:str, popularity_rank:int}
  - filters: Dict {recommendation_season:str, budget:str}
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. data/destinations.txt
- Fields (pipe-delimited):
  - dest_id (int)
  - name (str)
  - country (str)
  - region (str)
  - description (str)
  - attractions (str)
  - climate (str)
- Description: Stores travel destination details including attractions and climate.
- Examples:
  - 1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  - 2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  - 3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
- Note: No header row present.

### 2. data/itineraries.txt
- Fields (pipe-delimited):
  - itinerary_id (int)
  - itinerary_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - activities (str)
  - status (str)
- Description: Stores user-created itineraries with activities and status.
- Examples:
  - 1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  - 2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  - 3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
- Note: No header row present.

### 3. data/hotels.txt
- Fields (pipe-delimited):
  - hotel_id (int)
  - name (str)
  - city (str)
  - rating (float)
  - price_per_night (float)
  - amenities (str)
  - category (str)
- Description: Stores hotel data with ratings, prices, and amenities.
- Examples:
  - 1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  - 2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  - 3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
- Note: No header row present.

### 4. data/flights.txt
- Fields (pipe-delimited):
  - flight_id (int)
  - airline (str)
  - departure_city (str)
  - arrival_city (str)
  - departure_time (str)
  - arrival_time (str)
  - price (float)
  - class_type (str)
  - duration (str)
- Description: Stores flight details including schedules, prices, and class type.
- Examples:
  - 1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  - 2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  - 3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
- Note: No header row present.

### 5. data/packages.txt
- Fields (pipe-delimited):
  - package_id (int)
  - package_name (str)
  - destination (str)
  - duration_days (int)
  - price (float)
  - included_items (str)
  - difficulty_level (str)
- Description: Stores pre-designed travel packages with inclusions and difficulty.
- Examples:
  - 1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  - 2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  - 3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
- Note: No header row present.

### 6. data/trips.txt
- Fields (pipe-delimited):
  - trip_id (int)
  - trip_name (str)
  - destination (str)
  - start_date (str, YYYY-MM-DD)
  - end_date (str, YYYY-MM-DD)
  - total_budget (float)
  - status (str)
  - created_date (str, YYYY-MM-DD)
- Description: Stores all user trips with budget, dates, and status.
- Examples:
  - 1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  - 2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  - 3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
- Note: No header row present.

### 7. data/bookings.txt
- Fields (pipe-delimited):
  - booking_id (int)
  - trip_id (int)
  - booking_type (str)
  - booking_date (str, YYYY-MM-DD)
  - amount (float)
  - confirmation_number (str)
  - status (str)
- Description: Stores booking information including confirmations and statuses.
- Examples:
  - 1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  - 2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  - 3|3|Package|2025-01-12|1800.00|CONF003|Pending
- Note: No header row present.

---

This specification fully supports backend and frontend development independently with consistent naming, exact element IDs, and precise data formats.
