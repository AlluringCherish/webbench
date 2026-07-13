# TravelPlanner Web Application - Unified Design Specification

## 1. Overview
This document consolidates the two design candidates for the TravelPlanner web application into a single coherent design specification. The application consists of 10 main pages with defined Flask routes, element IDs, button actions, navigation flows, and data file interactions. The site starts at the Dashboard page, with no authentication required.

---

## 2. Flask Routes and Page Titles

| Route Path                             | Page Title               | Notes                                      |
|--------------------------------------|--------------------------|--------------------------------------------|
| `/`                                  | Redirects to `/dashboard`| Root redirects to Dashboard                 |
| `/dashboard`                         | Travel Planner Dashboard | Main hub page                              |
| `/destinations`                      | Travel Destinations      | List and search destinations                |
| `/destination/<int:dest_id>`        | Destination Details      | Show one destination details                 |
| `/itinerary`                        | Plan Your Itinerary      | Create/manage itineraries                    |
| `/accommodations`                   | Search Accommodations    | Search hotels and filters                    |
| `/transportation`                   | Book Flights             | Flight search and booking                    |
| `/packages`                        | Travel Packages          | View and book travel packages                |
| `/trips`                           | My Trips                 | Manage all user trips                         |
| `/booking-confirmation/<int:booking_id>` | Booking Confirmation     | Booking details confirmation page            |
| `/recommendations`                 | Travel Recommendations   | Personalized recommendations and trends      |

---

## 3. Detailed Page Designs and Interactions

### 3.1 Dashboard Page
- Route: `/dashboard`
- Title: Travel Planner Dashboard
- Data Files Used: `destinations.txt`, `trips.txt`

**Elements:**
- `dashboard-page` (div) - Container for dashboard
- `featured-destinations` (div) - Displays featured destinations
- `upcoming-trips` (div) - Displays upcoming trips (start_date >= today, status not Cancelled)
- `browse-destinations-button` (button) - Navigates to `/destinations`
- `plan-itinerary-button` (button) - Navigates to `/itinerary`

**Button Actions:**
- `browse-destinations-button`: Redirect to `/destinations`
- `plan-itinerary-button`: Redirect to `/itinerary`

---

### 3.2 Destinations Page
- Route: `/destinations`
- Title: Travel Destinations
- Data Files Used: `destinations.txt`

**Elements:**
- `destinations-page` (div) - Container for destinations page
- `search-destination` (input) - Search field by name or country
- `region-filter` (dropdown) - Filter by region [Asia, Europe, Americas, Africa, Oceania]
- `destinations-grid` (div) - Grid showing destination cards
- `view-destination-button-{dest_id}` (button) - View details for each destination

**Button Actions:**
- Filtering/search dynamically updates `destinations-grid`
- Clicking `view-destination-button-{dest_id}` redirects to `/destination/<dest_id>`

---

### 3.3 Destination Details Page
- Route: `/destination/<int:dest_id>`
- Title: Destination Details
- Data Files Used: `destinations.txt`

**Elements:**
- `destination-details-page` (div) - Container
- `destination-name` (h1) - Destination name
- `destination-country` (div) - Country
- `destination-description` (div) - Full description
- `add-to-trip-button` (button) - Add this destination to itinerary
- `destination-attractions` (div) - Main attractions and activities

**Button Actions:**
- Clicking `add-to-trip-button` prompts itinerary addition flow (stores into `itineraries.txt` or local session)

---

### 3.4 Itinerary Planning Page
- Route: `/itinerary`
- Title: Plan Your Itinerary
- Data Files Used: `itineraries.txt`

**Elements:**
- `itinerary-page` (div) - Container
- `itinerary-name-input` (input) - Itinerary name input
- `start-date-input` (input, date) - Start date
- `end-date-input` (input, date) - End date
- `add-activity-button` (button) - Adds an activity
- `itinerary-list` (div) - List of itineraries
- Per itinerary in list:
  - Edit Button: `btn-edit-itinerary-{itinerary_id}`
  - Delete Button: `btn-delete-itinerary-{itinerary_id}`

**Button Actions:**
- `add-activity-button` adds new activity to selected itinerary
- Editing and deleting is enabled via respective buttons in `itinerary-list`

---

### 3.5 Accommodations Page
- Route: `/accommodations`
- Title: Search Accommodations
- Data Files Used: `hotels.txt`

**Elements:**
- `accommodations-page` (div) - Container
- `destination-input` (input) - Destination city
- `check-in-date` (input, date) - Check-in date
- `check-out-date` (input, date) - Check-out date
- `price-filter` (dropdown) - Price range filter [Budget, Mid-range, Luxury]
- `hotels-list` (div) - List of hotels with details

**Button Actions:**
- Search or filter updates `hotels-list`

---

### 3.6 Transportation Page
- Route: `/transportation`
- Title: Book Flights
- Data Files Used: `flights.txt`

**Elements:**
- `transportation-page` (div) - Container
- `departure-city` (input) - Departure city
- `arrival-city` (input) - Arrival city
- `departure-date` (input, date) - Departure date
- `flight-class-filter` (dropdown) - Flight class filter [Economy, Business, First Class]
- `available-flights` (div) - List of flights matching criteria

**Button Actions:**
- Search or filter updates `available-flights`

---

### 3.7 Travel Packages Page
- Route: `/packages`
- Title: Travel Packages
- Data Files Used: `packages.txt`

**Elements:**
- `packages-page` (div) - Container
- `packages-grid` (div) - Grid of package cards
- `duration-filter` (dropdown) - Duration filter [3-5 days, 7-10 days, 14+ days]
- Per package card:
  - View Package Details Button: `view-package-details-button-{pkg_id}`
  - Book Package Button: `book-package-button-{pkg_id}`

**Button Actions:**
- Filtering updates `packages-grid`
- Clicking `view-package-details-button-{pkg_id}` opens modal or detail page
- `book-package-button-{pkg_id}` triggers booking flow, updates `bookings.txt` and `trips.txt`

---

### 3.8 Trip Management Page
- Route: `/trips`
- Title: My Trips
- Data Files Used: `trips.txt`

**Elements:**
- `trips-page` (div) - Container
- `trips-table` (table) - Listing trips (destination, dates, status)
- Per trip:
  - View Trip Details Button: `view-trip-details-button-{trip_id}`
  - Edit Trip Button: `edit-trip-button-{trip_id}`
  - Delete Trip Button: `delete-trip-button-{trip_id}`

**Button Actions:**
- `view-trip-details-button-{trip_id}` views trip details
- `edit-trip-button-{trip_id}` edits trip
- `delete-trip-button-{trip_id}` deletes trip from `trips.txt`

---

### 3.9 Booking Confirmation Page
- Route: `/booking-confirmation/<int:booking_id>`
- Title: Booking Confirmation
- Data Files Used: `bookings.txt`, `trips.txt`

**Elements:**
- `confirmation-page` (div) - Container
- `confirmation-number` (div) - Booking confirmation number
- `booking-details` (div) - Booking detail info
- `download-itinerary-button` (button) - Download itinerary PDF
- `share-trip-button` (button) - Share trip details
- `back-to-dashboard` (button) - Navigate back to `/dashboard`

**Button Actions:**
- `download-itinerary-button` triggers PDF download
- `share-trip-button` triggers share modal/action
- `back-to-dashboard` redirects to `/dashboard`

---

### 3.10 Travel Recommendations Page
- Route: `/recommendations`
- Title: Travel Recommendations
- Data Files Used: `destinations.txt`, `itineraries.txt`

**Elements:**
- `recommendations-page` (div) - Container
- `trending-destinations` (div) - Trending destinations
- `recommendation-season-filter` (dropdown) - Filter by travel season [Spring, Summer, Fall, Winter]
- `budget-filter` (dropdown) - Budget filter [Low, Medium, High]
- `back-to-dashboard` (button) - Navigate to `/dashboard`

**Button Actions:**
- Filters dynamically update shown recommendations
- `back-to-dashboard` redirects to `/dashboard`

---

## 4. Navigation Summary
- Root `/` redirects to `/dashboard`
- Dashboard buttons:
  - `browse-destinations-button` -> `/destinations`
  - `plan-itinerary-button` -> `/itinerary`
- Destinations page:
  - `view-destination-button-{dest_id}` -> `/destination/<dest_id>`
- Destination Details page:
  - `add-to-trip-button` -> triggers itinerary addition flow
- Itinerary page:
  - Edit/Delete per itinerary via `btn-edit-itinerary-{itinerary_id}` / `btn-delete-itinerary-{itinerary_id}`
- Packages page:
  - `view-package-details-button-{pkg_id}` opens details modal/page
  - `book-package-button-{pkg_id}` books package
- Trips page:
  - `view-trip-details-button-{trip_id}`, `edit-trip-button-{trip_id}`, `delete-trip-button-{trip_id}` respectively view, edit, delete trips
- Booking Confirmation page:
  - `back-to-dashboard` -> `/dashboard`
  - `download-itinerary-button` -> download PDF
  - `share-trip-button` -> sharing modal/action
- Recommendations page:
  - `back-to-dashboard` -> `/dashboard`

---

## 5. Data File Usage per Page
| Page | Data Files Used | Notes |
|----------------------|------------------------------|---------------------------------------|
| Dashboard            | `destinations.txt`, `trips.txt` | Featured destinations, upcoming trips |
| Destinations         | `destinations.txt`            | All destinations listing and filtering |
| Destination Details  | `destinations.txt`            | Specific destination details           |
| Itinerary Planning   | `itineraries.txt`             | Read/write itineraries                 |
| Accommodations       | `hotels.txt`                  | Hotels data filtering                  |
| Transportation       | `flights.txt`                 | Flights data filtering                 |
| Travel Packages      | `packages.txt`                | Packages listing and filtering         |
| Trip Management      | `trips.txt`                   | Read/edit/delete trips                 |
| Booking Confirmation | `bookings.txt`, `trips.txt`  | Booking and trip details               |
| Travel Recommendations| `destinations.txt`, `itineraries.txt` | Trends and recommendation filtering  |

---

## 6. Authentication
- No authentication or login required.
- All pages and features accessible publicly.

---

This unified specification is aligned for direct implementation, consolidating the element IDs, routes, navigation flows, and data file access strategies from both candidates.

*End of Unified Design Specification*