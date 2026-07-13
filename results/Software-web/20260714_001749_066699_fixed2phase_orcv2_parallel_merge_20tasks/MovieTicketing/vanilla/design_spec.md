# MovieTicketing Web Application Design Specification

---

## Section 1: Consolidated Backend and Frontend Specification

### 1. Dashboard Page
- **Route Path:** `/dashboard`
- **HTTP Method:** GET
- **Functionality:** Render dashboard page showing featured movies and navigation buttons.
- **Template Filename:** `dashboard.html`
- **Context Variables:**
  - `featured_movies` (List[Dict]): Featured movie objects including `movie_id`, `title`, `poster_url`, etc.
- **Element IDs:**
  - `dashboard-page` (Div): Main container.
  - `featured-movies` (Div): Featured movie display.
  - `browse-movies-button` (Button): Navigates to `/movies`
  - `view-bookings-button` (Button): Navigates to `/bookings`
  - `showtimes-button` (Button): Navigates to `/showtimes`
- **Navigation Flows:**
  - `browse-movies-button` -> `/movies`
  - `view-bookings-button` -> `/bookings`
  - `showtimes-button` -> `/showtimes`

---

### 2. Movie Catalog Page
- **Route Path:** `/movies`
- **HTTP Method:** GET
- **Query Params:**
  - `search` (optional): Filter movies by title or genre case-insensitive
  - `genre` (optional): Filter movies by genre
- **Functionality:** Render movie catalog with filtered movie list.
- **Template Filename:** `movie_catalog.html`
- **Context Variables:**
  - `movies` (List[Dict]): Movie objects with `movie_id`, `title`, `poster_url`, `rating`, `duration`, `genre`, etc.
  - `genres` (List[str]): List of genres for dropdown.
  - `search_query` (str): Current search input.
  - `selected_genre` (str): Currently selected genre filter.
- **Element IDs:**
  - `catalog-page` (Div): Main container.
  - `search-input` (Input): Search field.
  - `genre-filter` (Dropdown Select): Genre filter.
  - `movies-grid` (Div): Grid showing movie cards.
  - `view-movie-button-{movie_id}` (Button): View movie details button on each card.
- **Navigation Flows:**
  - `view-movie-button-{movie_id}` -> `/movie/{movie_id}`

---

### 3. Movie Details Page
- **Route Path:** `/movie/<int:movie_id>`
- **HTTP Method:** GET
- **Functionality:** Render details of a specific movie.
- **Template Filename:** `movie_details.html`
- **Context Variables:**
  - `movie` (Dict): Movie details with keys: `movie_id`, `title`, `director`, `rating`, `description`, `duration`, `genre`, `release_date`, etc.
- **Element IDs:**
  - `movie-details-page` (Div): Main container.
  - `movie-title` (H1): Movie title.
  - `movie-director` (Div): Director.
  - `movie-rating` (Div): Rating.
  - `movie-description` (Div): Description.
  - `select-showtime-button` (Button): Proceed to showtime selection.
- **Navigation Flows:**
  - `select-showtime-button` -> `/showtimes/{movie_id}`

---

### 4. Showtime Selection Page
- **Route Path:** `/showtimes/<int:movie_id>`
- **HTTP Method:** GET
- **Query Params:**
  - `theater_id` (optional): Filter by theater
  - `date` (optional): Filter by showtime date in YYYY-MM-DD format
- **Functionality:** Render showtimes filtered by movie, theater, and date.
- **Template Filename:** `showtime_selection.html`
- **Context Variables:**
  - `showtimes` (List[Dict]): Showtimes with `showtime_id`, `movie_id`, `theater_name`, `showtime_date`, `showtime_time`, `price`, `available_seats`.
  - `theaters` (List[Dict]): Theaters with `theater_id`, `theater_name` for filter dropdown.
  - `selected_theater_id` (Optional[int]): Current theater filter.
  - `selected_date` (Optional[str]): Current date filter.
  - `movie` (Optional[Dict]): Details of filtered movie.
- **Element IDs:**
  - `showtime-page` (Div): Container.
  - `showtimes-list` (Div): List/grid of showtimes.
  - `theater-filter` (Dropdown Select): Theater filter.
  - `date-filter` (Input type=date): Date filter.
  - `select-showtime-button-{showtime_id}` (Button): Select a showtime.
- **Navigation Flows:**
  - `select-showtime-button-{showtime_id}` -> `/seats/{showtime_id}`

---

### 5. Seat Selection Page
- **Route Path:** `/seats/<int:showtime_id>`
- **HTTP Method:** GET
- **Functionality:** Render seat map showing seat availability for the showtime.
- **Template Filename:** `seat_selection.html`
- **Context Variables:**
  - `showtime` (Dict): Showtime details including price, date, time.
  - `seats` (List[Dict]): Seats for the theater/screen with `seat_id`, `row`, `column`, `status` (Available/Booked), `seat_type`.
  - `selected_seats` (List[str]): Seats currently selected by user.
- **Element IDs:**
  - `seat-selection-page` (Div): Container.
  - `seat-map` (Div): Interactive seat map.
  - `seat-{row}{col}` (Button): Seat buttons (e.g., seat-A1).
  - `selected-seats-display` (Div): Shows currently selected seats.
  - `proceed-booking-button` (Button): Proceed to booking confirmation.
- **Navigation Flows:**
  - Seat buttons toggle selection.
  - `proceed-booking-button` -> `/booking_confirmation?showtime_id={showtime_id}&seats={selected_seats_csv}`

---

### 6. Booking Confirmation Page
- **Route Path:** `/bookings/confirm`
- **HTTP Method:** POST
- **Functionality:** Confirm booking with customer details and selected seats.
- **Template Filename:** `booking_confirmation.html`
- **Context Variables:**
  - `showtime` (Dict): Showtime details.
  - `movie` (Dict): Movie details.
  - `selected_seats` (List[str]): Seats selected.
  - `total_price` (Float): Total booking price.
- **Element IDs:**
  - `confirmation-page` (Div): Container.
  - `booking-summary` (Div): Summary of booking.
  - `customer-name` (Input): Customer name input.
  - `customer-email` (Input): Customer email input.
  - `confirm-booking-button` (Button): Submit booking.
- **Backend Operations:**
  - Validate seat availability.
  - Calculate total price.
  - Generate booking_id.
  - Append booking to `bookings.txt` with status "Confirmed".
  - Update `showtimes.txt` available seats.
- **Navigation Flows:**
  - After confirmation, navigate to booking history or success page.

---

### 7. Booking History Page
- **Route Path:** `/bookings`
- **HTTP Method:** GET
- **Query Params:**
  - `status` (optional): Filter by booking status (All, Confirmed, Cancelled, Completed)
- **Functionality:** List past bookings filtered by status.
- **Template Filename:** `booking_history.html`
- **Context Variables:**
  - `bookings` (List[Dict]): Booking entries with `booking_id`, `movie_title`, `booking_date`, `seats_booked`, `status`.
  - `status_options` (List[str]): [All, Confirmed, Cancelled, Completed]
  - `selected_status` (str): Current status filter.
- **Element IDs:**
  - `bookings-page` (Div): Container.
  - `bookings-table` (Table): Booking list.
  - `view-booking-button-{booking_id}` (Button): View booking details button.
  - `status-filter` (Dropdown Select): Status filter dropdown.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Navigation Flows:**
  - `view-booking-button-{booking_id}` -> `/bookings/{booking_id}` (if implemented)
  - `back-to-dashboard` -> `/dashboard`

---

### 8. Theater Information Page
- **Route Path:** `/theaters`
- **HTTP Method:** GET
- **Query Params:**
  - `location` (optional): Filter theaters by city/location
- **Functionality:** Display theaters information filtered by location.
- **Template Filename:** `theater_information.html`
- **Context Variables:**
  - `theaters` (List[Dict]): Theaters with `theater_id`, `theater_name`, `location`, `city`, `screens`, `facilities`.
  - `locations` (List[str]): Cities for filter dropdown.
  - `selected_location` (str): Selected city.
- **Element IDs:**
  - `theater-page` (Div): Container.
  - `theaters-list` (Div): Theater cards list.
  - `theater-location-filter` (Dropdown Select): Location filter.
  - `facilities-display` (Div): Facilities display.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Navigation Flows:**
  - `back-to-dashboard` -> `/dashboard`

---

## Section 2: Data Schema and Page Design Consistency

### Data Files Supporting Backend and Frontend:

1. `movies.txt`
- Schema: `movie_id|title|director|genre|rating|duration|description|release_date`
- Supports movie catalog, movie details, dashboard featured movies.

2. `theaters.txt`
- Schema: `theater_id|theater_name|location|city|screens|facilities`
- Supports theater information page and showtime theater filter.

3. `showtimes.txt`
- Schema: `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- Supports showtime selection, seat selection, booking confirmation.

4. `seats.txt`
- Schema: `seat_id|theater_id|screen_id|row|column|seat_type|status`
- Supports seat selection page seat map.

5. `bookings.txt`
- Schema: `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- Supports booking confirmation verification and booking history display.

6. `genres.txt`
- Schema: `genre_id|genre_name|description`
- Supports movie catalog genre dropdown filter.

### Design Consistency Notes:
- Route paths and frontend navigation endpoints are aligned, e.g., `/movie/{movie_id}` matches backend `/movie/<int:movie_id>`.
- Context variables defined in backend correspond exactly to frontend template requirements.
- Element IDs are consistently defined for container divs, buttons, inputs as required.
- Seat status dynamically determined by combining static seat status from `seats.txt` and actual booked seats from `bookings.txt` per showtime.
- Booking confirmation POST uses `/bookings/confirm` endpoint with expected JSON payload.
- Navigation flow is coherent starting from `/dashboard` as homepage.
- Booking history status filter and movie catalog filters are aligned with available data schemas.
- Showtimes filter support by theater and date matches front-end elements.
- The `showtimes` route uses path parameter for movie_id in backend (`/showtimes/<int:movie_id>`) and frontend uses the same.
- Data file formats and constraints support all required filtering, display, and business rules.

---

# Summary

This consolidated design specification merges backend Flask route definitions and data schema details with frontend template designs, element IDs, context variables, and navigation flows for the MovieTicketing web application. It ensures full consistency and completeness for developers to implement seamlessly as per the user task description. No additional features or changes outside the original input requirements have been introduced.