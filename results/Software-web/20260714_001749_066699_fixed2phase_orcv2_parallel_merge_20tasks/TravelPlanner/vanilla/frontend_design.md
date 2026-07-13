# TravelPlanner Frontend Design Specification

---

## Section 1: HTML Template Specifications

### 1. Dashboard Page
- **Filename:** dashboard.html
- **Page Title:** Travel Planner Dashboard
- **Elements:**
  - `dashboard-page` (Div): Container for the dashboard page.
  - `featured-destinations` (Div): Display area for featured travel destinations.
  - `upcoming-trips` (Div): Display area showing upcoming planned trips.
  - `browse-destinations-button` (Button): Button to navigate to the Destinations page.
  - `plan-itinerary-button` (Button): Button to navigate to the Itinerary Planning page.

---

### 2. Destinations Page
- **Filename:** destinations.html
- **Page Title:** Travel Destinations
- **Elements:**
  - `destinations-page` (Div): Container for the destinations page.
  - `search-destination` (Input[type=text]): Text input to search destinations by name or country.
  - `region-filter` (Dropdown/select): Dropdown to filter destinations by region (Asia, Europe, Americas, Africa, Oceania).
  - `destinations-grid` (Div): Grid container displaying destination cards.
  - `view-destination-button-{dest_id}` (Button): Button on each destination card to view destination details.

---

### 3. Destination Details Page
- **Filename:** destination_details.html
- **Page Title:** Destination Details
- **Elements:**
  - `destination-details-page` (Div): Container for the destination details page.
  - `destination-name` (H1): Heading displaying the destination name.
  - `destination-country` (Div): Display of destination country.
  - `destination-description` (Div): Detailed description of the destination.
  - `add-to-trip-button` (Button): Button to add this destination to a trip.
  - `destination-attractions` (Div): Section showing main attractions and activities.

---

### 4. Itinerary Planning Page
- **Filename:** itinerary.html
- **Page Title:** Plan Your Itinerary
- **Elements:**
  - `itinerary-page` (Div): Container for the itinerary planning page.
  - `itinerary-name-input` (Input[type=text]): Field to enter the itinerary name.
  - `start-date-input` (Input[type=date]): Date input to select trip start date.
  - `end-date-input` (Input[type=date]): Date input to select trip end date.
  - `add-activity-button` (Button): Button to add an activity to the itinerary.
  - `itinerary-list` (Div): Display list of created itineraries with edit and delete options.

---

### 5. Accommodations Page
- **Filename:** accommodations.html
- **Page Title:** Search Accommodations
- **Elements:**
  - `accommodations-page` (Div): Container for the accommodations page.
  - `destination-input` (Input[type=text]): Field to enter destination city for hotel search.
  - `check-in-date` (Input[type=date]): Check-in date selection.
  - `check-out-date` (Input[type=date]): Check-out date selection.
  - `price-filter` (Dropdown/select): Dropdown to filter hotels by price range (Budget, Mid-range, Luxury).
  - `hotels-list` (Div): List container showing hotels with name, rating, price, and amenities.

---

### 6. Transportation Page
- **Filename:** transportation.html
- **Page Title:** Book Flights
- **Elements:**
  - `transportation-page` (Div): Container for the transportation page.
  - `departure-city` (Input[type=text]): Input field for departure city.
  - `arrival-city` (Input[type=text]): Input field for arrival city.
  - `departure-date` (Input[type=date]): Date input for departure date.
  - `flight-class-filter` (Dropdown/select): Dropdown filter for flight class (Economy, Business, First Class).
  - `available-flights` (Div): List container for flights showing airline, times, and prices.

---

### 7. Travel Packages Page
- **Filename:** packages.html
- **Page Title:** Travel Packages
- **Elements:**
  - `packages-page` (Div): Container for the packages page.
  - `packages-grid` (Div): Grid showing travel package cards.
  - `duration-filter` (Dropdown/select): Filter packages by duration (3-5 days, 7-10 days, 14+ days).
  - `view-package-details-button-{pkg_id}` (Button): Button to view details of each package.
  - `book-package-button-{pkg_id}` (Button): Button to book the corresponding package.

---

### 8. Trip Management Page
- **Filename:** trips.html
- **Page Title:** My Trips
- **Elements:**
  - `trips-page` (Div): Container for the trips management page.
  - `trips-table` (Table): Table displaying trips with columns for destination, dates, and status.
  - `view-trip-details-button-{trip_id}` (Button): Button to view details of a specific trip.
  - `edit-trip-button-{trip_id}` (Button): Button to edit a specific trip.
  - `delete-trip-button-{trip_id}` (Button): Button to delete a specific trip.

---

### 9. Booking Confirmation Page
- **Filename:** booking_confirmation.html
- **Page Title:** Booking Confirmation
- **Elements:**
  - `confirmation-page` (Div): Container for booking confirmation details.
  - `confirmation-number` (Div): Display the confirmation or booking number.
  - `booking-details` (Div): Display detailed booking information including dates, amounts, and locations.
  - `download-itinerary-button` (Button): Button to download the trip itinerary as a PDF.
  - `share-trip-button` (Button): Button to share trip details.
  - `back-to-dashboard` (Button): Button to navigate back to the dashboard page.

---

### 10. Travel Recommendations Page
- **Filename:** recommendations.html
- **Page Title:** Travel Recommendations
- **Elements:**
  - `recommendations-page` (Div): Container for recommendations page.
  - `trending-destinations` (Div): Display trending destinations ranked by popularity.
  - `recommendation-season-filter` (Dropdown/select): Filter by travel season (Spring, Summer, Fall, Winter).
  - `budget-filter` (Dropdown/select): Filter by budget range (Low, Medium, High).
  - `back-to-dashboard` (Button): Button to navigate back to the dashboard page.


---

## Section 2: UI Navigation and Interaction

### Dashboard Page
- `browse-destinations-button`: Navigates to `/destinations` (Destinations Page).
- `plan-itinerary-button`: Navigates to `/itinerary` (Itinerary Planning Page).

### Destinations Page
- Typing in `search-destination` filters destinations by name or country dynamically.
- Selecting a value from `region-filter` filters destinations by selected region.
- Clicking `view-destination-button-{dest_id}` navigates to `/destinations/{dest_id}` (Destination Details Page for the given destination).

### Destination Details Page
- Clicking `add-to-trip-button` triggers adding the current destination to a new or existing trip (modal or route `/itinerary`).

### Itinerary Planning Page
- Input fields `itinerary-name-input`, `start-date-input`, and `end-date-input` used to define a new itinerary.
- Clicking `add-activity-button` opens input or modal to add activities to the itinerary.
- The `itinerary-list` shows current itineraries with:
  - `edit` and `delete` buttons next to each itinerary entry for modification or removal.

### Accommodations Page
- `destination-input`, `check-in-date`, and `check-out-date` inputs filter hotel search.
- Selecting `price-filter` narrows hotels by price range.
- Hotels are displayed in `hotels-list` dynamically based on filters.

### Transportation Page
- Inputs `departure-city`, `arrival-city`, and `departure-date` define flight search parameters.
- Selecting `flight-class-filter` filters flights by class.
- Flight options displayed in `available-flights`.

### Travel Packages Page
- Selecting `duration-filter` filters packages by their duration.
- Clicking `view-package-details-button-{pkg_id}` navigates to package details (could be modal or `/packages/{pkg_id}`).
- Clicking `book-package-button-{pkg_id}` triggers booking flow for the selected package.

### Trip Management Page
- Trips listed in `trips-table` with action buttons per row:
  - `view-trip-details-button-{trip_id}` navigates to detailed trip page or modal.
  - `edit-trip-button-{trip_id}` opens edit form or modal.
  - `delete-trip-button-{trip_id}` prompts deletion confirmation.

### Booking Confirmation Page
- `download-itinerary-button`: Downloads trip itinerary PDF.
- `share-trip-button`: Opens sharing options (email, social).
- `back-to-dashboard`: Navigates back to `/dashboard`.

### Travel Recommendations Page
- Selecting `recommendation-season-filter` filters recommendations by season.
- Selecting `budget-filter` filters recommendations by budget.
- `back-to-dashboard`: Navigates back to `/dashboard`.

---

# End of Frontend Design Specification
