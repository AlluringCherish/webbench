# TravelPlanner Design Specification - Revised Round 2

---

## Section 1: Flask Routes and HTTP Methods

- **Route:** `/`  
  **HTTP Methods:** GET  
  **Description:** Entry point rendering the Dashboard page.

- **Route:** `/dashboard`  
  **HTTP Methods:** GET  
  **Description:** Explicit route rendering the Dashboard, per peer suggestion.

- **Route:** `/destinations`  
  **HTTP Methods:** GET, POST  
  **Description:** Displays all available travel destinations with search and filter capabilities. POST used to submit search/filter forms.

- **Route:** `/destinations/<int:dest_id>`  
  **HTTP Methods:** GET, POST  
  **Description:** Shows detailed information for a specific destination identified by `dest_id`. POST used to add destination to trip.

- **Route:** `/itinerary`  
  **HTTP Methods:** GET, POST  
  **Description:** Plan and manage travel itineraries. POST for creating and updating itineraries and adding activities.

- **Route:** `/accommodations`  
  **HTTP Methods:** GET, POST  
  **Description:** Search and browse hotels. POST to submit search/filter forms.

- **Route:** `/transportation`  
  **HTTP Methods:** GET, POST  
  **Description:** Search and book flights. POST to submit flight search/filter.

- **Route:** `/packages`  
  **HTTP Methods:** GET  
  **Description:** Displays travel packages with filtering.

- **Route:** `/packages/<int:pkg_id>`  
  **HTTP Methods:** GET  
  **Description:** Displays detailed package information.

- **Route:** `/packages/<int:pkg_id>/book`  
  **HTTP Methods:** POST  
  **Description:** Booking action for travel packages.

- **Route:** `/trips`  
  **HTTP Methods:** GET, POST  
  **Description:** Displays all created trips; POST used for trip edits, updates or deletions.

- **Route:** `/trips/<int:trip_id>`  
  **HTTP Methods:** GET  
  **Description:** Displays detailed information about a specific trip.

- **Route:** `/booking/confirmation/<int:booking_id>`  
  **HTTP Methods:** GET  
  **Description:** Displays booking confirmation details.

- **Route:** `/recommendations`  
  **HTTP Methods:** GET, POST  
  **Description:** Displays personalized travel recommendations with filters.

---

## Section 2: Template Files and HTML Elements

### 1. Dashboard Page
- Templates: `dashboard.html`
- Page Title: "Travel Planner Dashboard"
- Element IDs:
  - `dashboard-page` (Div)
  - `featured-destinations` (Div)
  - `upcoming-trips` (Div)
  - `browse-destinations-button` (Button) - navigates to `/destinations`
  - `plan-itinerary-button` (Button) - navigates to `/itinerary`

### 2. Destinations Page
- Template: `destinations.html`
- Page Title: "Travel Destinations"
- Element IDs:
  - `destinations-page` (Div)
  - `search-destination` (Input)
  - `region-filter` (Dropdown)
  - `destinations-grid` (Div)
  - `view-destination-button-{dest_id}` (Button)

### 3. Destination Details Page
- Template: `destination_details.html`
- Page Title: "Destination Details"
- Element IDs:
  - `destination-details-page` (Div)
  - `destination-name` (H1)
  - `destination-country` (Div)
  - `destination-description` (Div)
  - `add-to-trip-button` (Button)
  - `destination-attractions` (Div)

### 4. Itinerary Planning Page
- Template: `itinerary.html`
- Page Title: "Plan Your Itinerary"
- Element IDs:
  - `itinerary-page` (Div)
  - `itinerary-name-input` (Input)
  - `start-date-input` (Input type=date)
  - `end-date-input` (Input type=date)
  - `add-activity-button` (Button)
  - `itinerary-list` (Div)

### 5. Accommodations Page
- Template: `accommodations.html`
- Page Title: "Search Accommodations"
- Element IDs:
  - `accommodations-page` (Div)
  - `destination-input` (Input)
  - `check-in-date` (Input type=date)
  - `check-out-date` (Input type=date)
  - `price-filter` (Dropdown)
  - `hotels-list` (Div)

### 6. Transportation Page
- Template: `transportation.html`
- Page Title: "Book Flights"
- Element IDs:
  - `transportation-page` (Div)
  - `departure-city` (Input)
  - `arrival-city` (Input)
  - `departure-date` (Input type=date)
  - `flight-class-filter` (Dropdown)
  - `available-flights` (Div)

### 7. Travel Packages Page
- Template: `packages.html`
- Page Title: "Travel Packages"
- Element IDs:
  - `packages-page` (Div)
  - `packages-grid` (Div)
  - `duration-filter` (Dropdown)
  - `view-package-details-button-{pkg_id}` (Button)
  - `book-package-button-{pkg_id}` (Button)

### 8. Trip Management Page
- Template: `trips.html`
- Page Title: "My Trips"
- Element IDs:
  - `trips-page` (Div)
  - `trips-table` (Table)
  - `view-trip-details-button-{trip_id}` (Button)
  - `edit-trip-button-{trip_id}` (Button)
  - `delete-trip-button-{trip_id}` (Button)

### 9. Trip Details Page
- Template: `trip_details.html`
- Page Title: "Trip Details"
- Element IDs:
  - (Not specified by user, we only declare template and title here, no element IDs detailed)

### 10. Booking Confirmation Page
- Template: `booking_confirmation.html`
- Page Title: "Booking Confirmation"
- Element IDs:
  - `confirmation-page` (Div)
  - `confirmation-number` (Div)
  - `booking-details` (Div)
  - `download-itinerary-button` (Button)
  - `share-trip-button` (Button)
  - `back-to-dashboard` (Button) - navigates to `/dashboard`

### 11. Travel Recommendations Page
- Template: `recommendations.html`
- Page Title: "Travel Recommendations"
- Element IDs:
  - `recommendations-page` (Div)
  - `trending-destinations` (Div)
  - `recommendation-season-filter` (Dropdown)
  - `budget-filter` (Dropdown)
  - `back-to-dashboard` (Button) - navigates to `/dashboard`

---

## Section 3: Data Storage File Formats

- `data/destinations.txt`
  - Format: `dest_id|name|country|region|description|attractions|climate`
  - Example: `1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate`

- `data/itineraries.txt`
  - Format: `itinerary_id|itinerary_name|destination|start_date|end_date|activities|status`
  - Example: `1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned`

- `data/hotels.txt`
  - Format: `hotel_id|name|city|rating|price_per_night|amenities|category`
  - Example: `1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury`

- `data/flights.txt`
  - Format: `flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration`
  - Example: `1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes`

- `data/packages.txt`
  - Format: `package_id|package_name|destination|duration_days|price|included_items|difficulty_level`
  - Example: `1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy`

- `data/trips.txt`
  - Format: `trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date`
  - Example: `1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10`

- `data/bookings.txt`
  - Format: `booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status`
  - Example: `1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed`

---

End of Design Document Revised Round 2
