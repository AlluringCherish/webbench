# TravelPlanner Web Application - Design Candidate B

## Overview
This document outlines an alternative full design candidate for the TravelPlanner Flask web application. It covers all 10 specified pages, defining routes, page titles, UI elements with element IDs, navigation control mappings, and data file usage. This design maintains the complete functionality and data needs but utilizes an alternative but consistent naming strategy and structure.

---

## 1. Route Definitions

| Route URL                      | Page Name               | Description                             |
|-------------------------------|-------------------------|----------------------------------------|
| `/`                           | Dashboard               | Main dashboard page                     |
| `/destinations`               | Destinations            | List and filter travel destinations    |
| `/destinations/<int:dest_id>` | Destination Details     | Detailed view of a single destination  |
| `/itinerary`                  | Itinerary Planning      | Create and manage itineraries           |
| `/accommodations`             | Accommodations          | Search and filter hotel options         |
| `/flights`                   | Flight Booking          | Search and book flights                  |
| `/packages`                  | Travel Packages         | Browse and book travel packages          |
| `/trips`                    | Trip Management         | Overview and manage all trips            |
| `/confirmation/<int:booking_id>` | Booking Confirmation | Show booking confirmation details       |
| `/recommendations`           | Travel Recommendations  | Personalized travel recommendation page |

---

## 2. Page Titles

| Page Name               | Page Title                |
|-------------------------|---------------------------|
| Dashboard               | Travel Planner Dashboard   |
| Destinations            | Travel Destinations        |
| Destination Details     | Destination Details        |
| Itinerary Planning      | Plan Your Itinerary        |
| Accommodations          | Search Accommodations      |
| Flight Booking          | Book Flights               |
| Travel Packages         | Travel Packages            |
| Trip Management         | My Trips                   |
| Booking Confirmation    | Booking Confirmation       |
| Travel Recommendations  | Travel Recommendations     |

---

## 3. UI Elements by Page

### 3.1 Dashboard Page (`/`)
- Container: `id="dashboard-container"` (Div)
- Featured Destinations: `id="featured-dests-container"` (Div)
- Upcoming Trips: `id="upcoming-trips-list"` (Div)
- Button to Destinations: `id="btn-go-destinations"` (Button)
- Button to Itinerary Planning: `id="btn-go-itinerary"` (Button)

### 3.2 Destinations Page (`/destinations`)
- Container: `id="destinations-main"` (Div)
- Search Input: `id="input-search-destination"` (Input Text)
- Region Filter: `id="select-region-filter"` (Dropdown)
- Destinations Grid: `id="destinations-cards-grid"` (Div)
- View Destination Button: `id="btn-view-dest-{dest_id}"` (Button per destination card)

### 3.3 Destination Details Page (`/destinations/<int:dest_id>`)
- Container: `id="dest-details-wrapper"` (Div)
- Destination Name: `id="dest-name-header"` (H1)
- Destination Country: `id="dest-country-info"` (Div)
- Destination Description: `id="dest-desc-text"` (Div)
- Destination Attractions: `id="dest-attractions-list"` (Div)
- Add to Trip Button: `id="btn-add-dest-trip"` (Button)

### 3.4 Itinerary Planning Page (`/itinerary`)
- Container: `id="itinerary-wrapper"` (Div)
- Itinerary Name Input: `id="input-itinerary-name"` (Input Text)
- Start Date Input: `id="input-start-date"` (Input Date)
- End Date Input: `id="input-end-date"` (Input Date)
- Add Activity Button: `id="btn-add-activity"` (Button)
- Itinerary List Display: `id="itinerary-list-container"` (Div)
- For each itinerary in list:
  - Edit Button: `id="btn-edit-itinerary-{itinerary_id}"` (Button)
  - Delete Button: `id="btn-delete-itinerary-{itinerary_id}"` (Button)

### 3.5 Accommodations Page (`/accommodations`)
- Container: `id="accommodations-wrapper"` (Div)
- Destination Input: `id="input-hotel-destination"` (Input Text)
- Check-in Date Input: `id="input-checkin-date"` (Input Date)
- Check-out Date Input: `id="input-checkout-date"` (Input Date)
- Price Filter Dropdown: `id="select-price-filter"` (Dropdown)
- Hotels List Display: `id="hotels-list-container"` (Div)

### 3.6 Flight Booking Page (`/flights`)
- Container: `id="flights-wrapper"` (Div)
- Departure City Input: `id="input-depart-city"` (Input Text)
- Arrival City Input: `id="input-arrival-city"` (Input Text)
- Departure Date Input: `id="input-depart-date"` (Input Date)
- Flight Class Filter: `id="select-flight-class"` (Dropdown)
- Available Flights List: `id="flights-list"` (Div)

### 3.7 Travel Packages Page (`/packages`)
- Container: `id="packages-container"` (Div)
- Packages Grid: `id="packages-grid"` (Div)
- Duration Filter Dropdown: `id="select-duration-filter"` (Dropdown)
- Per Package Card:
  - View Details Button: `id="btn-view-package-{package_id}"` (Button)
  - Book Package Button: `id="btn-book-package-{package_id}"` (Button)

### 3.8 Trip Management Page (`/trips`)
- Container: `id="trips-container"` (Div)
- Trips Table: `id="trips-data-table"` (Table)
- Per Trip:
  - View Details Button: `id="btn-view-trip-{trip_id}"` (Button)
  - Edit Trip Button: `id="btn-edit-trip-{trip_id}"` (Button)
  - Delete Trip Button: `id="btn-delete-trip-{trip_id}"` (Button)

### 3.9 Booking Confirmation Page (`/confirmation/<int:booking_id>`)
- Container: `id="confirmation-wrapper"` (Div)
- Confirmation Number Display: `id="conf-number"` (Div)
- Booking Details Display: `id="booking-info"` (Div)
- Download Itinerary Button: `id="btn-download-itinerary"` (Button)
- Share Trip Button: `id="btn-share-trip"` (Button)
- Back to Dashboard Button: `id="btn-back-dashboard"` (Button)

### 3.10 Travel Recommendations Page (`/recommendations`)
- Container: `id="recommendations-wrapper"` (Div)
- Trending Destinations Display: `id="trending-dests"` (Div)
- Season Filter Dropdown: `id="select-season-filter"` (Dropdown)
- Budget Filter Dropdown: `id="select-budget-filter"` (Dropdown)
- Back to Dashboard Button: `id="btn-back-dashboard"` (Button)

---

## 4. Navigation Elements Mapping

- Dashboard Buttons:
  - `btn-go-destinations` -> `/destinations`
  - `btn-go-itinerary` -> `/itinerary`

- On Destinations page:
  - `btn-view-dest-{dest_id}` -> `/destinations/<dest_id>`

- On Destination Details page:
  - `btn-add-dest-trip` adds current destination to an active itinerary or opens itinerary page (design to prompt user)

- On Itinerary Page:
  - `btn-edit-itinerary-{itinerary_id}` edits selected itinerary
  - `btn-delete-itinerary-{itinerary_id}` deletes selected itinerary

- On Travel Packages Page:
  - `btn-view-package-{package_id}` -> package detail modal or page
  - `btn-book-package-{package_id}` books package and possibly redirects to confirmation page

- On Trip Management Page:
  - `btn-view-trip-{trip_id}` -> show trip details
  - `btn-edit-trip-{trip_id}` -> edit trip
  - `btn-delete-trip-{trip_id}` -> deletes trip with confirmation

- On Booking Confirmation Page:
  - `btn-back-dashboard` -> `/`
  - `btn-download-itinerary` triggers itinerary PDF download
  - `btn-share-trip` facilitates sharing via email or social media

- On Recommendations Page:
  - `btn-back-dashboard` -> `/`

---

## 5. Data Access and File Usage per Page

| Page Name             | Data Files Utilized           | Data Access Type              |
|-----------------------|------------------------------|------------------------------|
| Dashboard             | `destinations.txt`, `itineraries.txt` | Read featured destinations and upcoming trips from stored data
| Destinations          | `destinations.txt`            | Read all destinations for listing and filtering
| Destination Details   | `destinations.txt`            | Read detailed info for specific destination
| Itinerary Planning    | `itineraries.txt`             | Read and write itineraries
| Accommodations        | `hotels.txt`                  | Read hotel data filtered by destination and price
| Flight Booking        | `flights.txt`                 | Read flights filtered by cities, date, and class
| Travel Packages       | `packages.txt`                | Read packages data, filter by duration
| Trip Management       | `trips.txt`                   | Read, edit, delete trip records
| Booking Confirmation  | `bookings.txt`, `trips.txt`  | Read booking details for confirmation
| Travel Recommendations| `destinations.txt`, `itineraries.txt` | Read destinations for trends and recommendations filtering

---

## 6. Authentication

- This alternative design explicitly excludes any authentication or user session mechanisms.
- All pages and functionalities are publicly accessible without login or user identification.

---

# Summary
This design candidate provides a consistent complete alternative for TravelPlanner. All routes, UI control IDs, navigation links, and data file interactions are defined to fulfill the functional requirements strictly. The naming strategy differs to demonstrate alternative but equivalent implementation possibilities.

---

*End of Design Candidate B*