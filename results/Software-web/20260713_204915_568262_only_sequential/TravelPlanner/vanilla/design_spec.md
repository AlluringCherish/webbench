# TravelPlanner Web Application Design Specification

---

## Overview
This design specification provides a detailed blueprint for developing the TravelPlanner web application using Python Flask framework. It outlines Flask routes, HTML templates with precise element IDs, navigation flows, and data file contracts. The design supports independent backend and frontend development.

---

## Flask Routes and Templates

| Page Name              | Route Path               | HTTP Methods | Function Name                  | Template Filename            | Page Title             |
|------------------------|--------------------------|--------------|-------------------------------|------------------------------|------------------------|
| Dashboard              | `/`                      | GET          | `dashboard()`                 | `dashboard.html`             | Travel Planner Dashboard|
| Destinations           | `/destinations`           | GET          | `destinations()`              | `destinations.html`          | Travel Destinations     |
| Destination Details    | `/destinations/<int:dest_id>`| GET      | `destination_details(dest_id)`| `destination_details.html`   | Destination Details     |
| Itinerary Planning     | `/itinerary`              | GET, POST    | `itinerary()`                 | `itinerary.html`             | Plan Your Itinerary     |
| Accommodations         | `/accommodations`         | GET          | `accommodations()`            | `accommodations.html`        | Search Accommodations   |
| Transportation        | `/transportation`          | GET          | `transportation()`            | `transportation.html`        | Book Flights            |
| Travel Packages        | `/packages`               | GET          | `packages()`                  | `packages.html`              | Travel Packages         |
| Trip Management        | `/trips`                  | GET          | `trips()`                    | `trips.html`                 | My Trips                |
| Booking Confirmation   | `/booking-confirmation`   | GET          | `booking_confirmation()`      | `booking_confirmation.html`  | Booking Confirmation    |
| Travel Recommendations | `/recommendations`        | GET          | `recommendations()`           | `recommendations.html`       | Travel Recommendations  |


### Notes on Routes
- POST methods may be added to routes like `/itinerary` for adding activities or itinerary data.
- Dynamic parameters like `<int:dest_id>`, `<int:pkg_id>`, `<int:trip_id>` used for details and actions.
- Trip edit and delete actions are expected to be handled via additional POST/DELETE routes or AJAX endpoints (not listed as independent pages here).

---

## Page Templates and UI Element IDs

### 1. Dashboard (`dashboard.html`)
- Page Title: *Travel Planner Dashboard*
- Container Div ID: `dashboard-page`
- Featured destinations Div ID: `featured-destinations`
- Upcoming trips Div ID: `upcoming-trips`
- Navigation Buttons:
  - ID: `browse-destinations-button` (to Destinations Page)
  - ID: `plan-itinerary-button` (to Itinerary Planning Page)

---

### 2. Destinations (`destinations.html`)
- Page Title: *Travel Destinations*
- Container Div ID: `destinations-page`
- Search Input ID: `search-destination` (search by name or country)
- Region Filter Dropdown ID: `region-filter` (Options: Asia, Europe, Americas, Africa, Oceania)
- Destinations Grid Container Div ID: `destinations-grid`
- View Destination Button ID pattern: `view-destination-button-{dest_id}` (dynamic)

---

### 3. Destination Details (`destination_details.html`)
- Page Title: *Destination Details*
- Container Div ID: `destination-details-page`
- Destination Name (H1) ID: `destination-name`
- Destination Country Div ID: `destination-country`
- Destination Description Div ID: `destination-description`
- Add to Trip Button ID: `add-to-trip-button`
- Attractions Div ID: `destination-attractions`

---

### 4. Itinerary Planning (`itinerary.html`)
- Page Title: *Plan Your Itinerary*
- Container Div ID: `itinerary-page`
- Itinerary Name Input ID: `itinerary-name-input`
- Start Date Input ID: `start-date-input`
- End Date Input ID: `end-date-input`
- Add Activity Button ID: `add-activity-button`
- Itinerary List Div ID: `itinerary-list`

---

### 5. Accommodations (`accommodations.html`)
- Page Title: *Search Accommodations*
- Container Div ID: `accommodations-page`
- Destination City Input ID: `destination-input`
- Check-in Date Input ID: `check-in-date`
- Check-out Date Input ID: `check-out-date`
- Price Filter Dropdown ID: `price-filter` (Options: Budget, Mid-range, Luxury)
- Hotels List Div ID: `hotels-list`

---

### 6. Transportation (`transportation.html`)
- Page Title: *Book Flights*
- Container Div ID: `transportation-page`
- Departure City Input ID: `departure-city`
- Arrival City Input ID: `arrival-city`
- Departure Date Input ID: `departure-date`
- Flight Class Filter Dropdown ID: `flight-class-filter` (Options: Economy, Business, First Class)
- Available Flights Div ID: `available-flights`

---

### 7. Travel Packages (`packages.html`)
- Page Title: *Travel Packages*
- Container Div ID: `packages-page`
- Packages Grid Div ID: `packages-grid`
- Duration Filter Dropdown ID: `duration-filter` (Options: 3-5 days, 7-10 days, 14+ days)
- View Package Details Button ID pattern: `view-package-details-button-{pkg_id}`
- Book Package Button ID pattern: `book-package-button-{pkg_id}`

---

### 8. Trip Management (`trips.html`)
- Page Title: *My Trips*
- Container Div ID: `trips-page`
- Trips Table ID: `trips-table`
- View Trip Details Button ID pattern: `view-trip-details-button-{trip_id}`
- Edit Trip Button ID pattern: `edit-trip-button-{trip_id}`
- Delete Trip Button ID pattern: `delete-trip-button-{trip_id}`

---

### 9. Booking Confirmation (`booking_confirmation.html`)
- Page Title: *Booking Confirmation*
- Container Div ID: `confirmation-page`
- Confirmation Number Div ID: `confirmation-number`
- Booking Details Div ID: `booking-details`
- Download Itinerary Button ID: `download-itinerary-button`
- Share Trip Button ID: `share-trip-button`
- Back to Dashboard Button ID: `back-to-dashboard`

---

### 10. Travel Recommendations (`recommendations.html`)
- Page Title: *Travel Recommendations*
- Container Div ID: `recommendations-page`
- Trending Destinations Div ID: `trending-destinations`
- Season Filter Dropdown ID: `recommendation-season-filter` (Options: Spring, Summer, Fall, Winter)
- Budget Filter Dropdown ID: `budget-filter` (Options: Low, Medium, High)
- Back to Dashboard Button ID: `back-to-dashboard`

---

## Navigation Mappings

| From Page               | Button ID                           | Leads to Route / Function                 |
|-------------------------|-----------------------------------|------------------------------------------|
| Dashboard               | `browse-destinations-button`      | `url_for('destinations')`                 |
| Dashboard               | `plan-itinerary-button`            | `url_for('itinerary')`                    |
| Booking Confirmation    | `back-to-dashboard`                | `url_for('dashboard')`                    |
| Travel Recommendations  | `back-to-dashboard`                | `url_for('dashboard')`                    |
| Destinations            | `view-destination-button-{dest_id}`| `url_for('destination_details', dest_id=dest_id)` |
| Travel Packages         | `view-package-details-button-{pkg_id}`| Package details view (functionality to be defined as needed)
| Travel Packages         | `book-package-button-{pkg_id}`    | Booking process then to booking confirmation (may include intermediate route)
| Trip Management         | `view-trip-details-button-{trip_id}`| Trip details view (functionality embedded or separate route)
| Trip Management         | `edit-trip-button-{trip_id}`      | Edit trip form/page (may integrate with itinerary planning)
| Trip Management         | `delete-trip-button-{trip_id}`    | Delete trip action (POST/DELETE method)
| Destination Details     | `add-to-trip-button`               | Add destination to user's trip (back-end update)
| Booking Confirmation    | `download-itinerary-button`        | Download itinerary PDF
| Booking Confirmation    | `share-trip-button`                | Share trip details

---

## Data File Contracts

All data files are pipe-delimited (`|`). Fields are ordered and must be consistent for proper parsing and storage.

### 1. Destinations Data (`data/destinations.txt`)
- Fields: `dest_id|name|country|region|description|attractions|climate`
- Example:
```
1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
```

### 2. Itineraries Data (`data/itineraries.txt`)
- Fields: `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
- Dates formatted as `YYYY-MM-DD`
- Example:
```
1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
```

### 3. Hotels Data (`data/hotels.txt`)
- Fields: `hotel_id|name|city|rating|price_per_night|amenities|category`
- Rating is numeric (e.g., 5.0)
- Price in decimal format
- Example:
```
1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
```

### 4. Flights Data (`data/flights.txt`)
- Fields: `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
- Times are strings (e.g., "10:00", "15:20 next day")
- Price in decimal
- Example:
```
1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
```

### 5. Travel Packages Data (`data/packages.txt`)
- Fields: `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
- Duration days as integer
- Price in decimal
- Example:
```
1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
```

### 6. Trips Data (`data/trips.txt`)
- Fields: `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
- Dates formatted as `YYYY-MM-DD`
- Budget as decimal
- Example:
```
1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
```

### 7. Bookings Data (`data/bookings.txt`)
- Fields: `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
- Dates as `YYYY-MM-DD`
- Amount as decimal
- Example:
```
1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
3|3|Package|2025-01-12|1800.00|CONF003|Pending
```

---

## Summary
This design spec details all essential aspects to build the TravelPlanner application:
- Flask route endpoints and function names
- Corresponding templates with exact element IDs
- Navigation button-to-route mappings
- Data file formats and field orders

Developers can independently implement backend and frontend based on this document.

---

*End of design_spec.md*