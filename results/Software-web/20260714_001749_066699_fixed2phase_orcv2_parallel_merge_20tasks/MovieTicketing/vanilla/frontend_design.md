# Frontend Design Specification for MovieTicketing Web Application

---

## 1. Dashboard Page

- **Template Filename**: dashboard.html
- **Page Title**: Movie Ticketing Dashboard

### Element IDs and Types
- `dashboard-page` (Div): Main container for the dashboard page.
- `featured-movies` (Div): Displays featured movie recommendations.
- `browse-movies-button` (Button): Navigates to Movie Catalog page.
- `view-bookings-button` (Button): Navigates to Booking History page.
- `showtimes-button` (Button): Navigates to Showtime Selection page.

### Context Variables
- `featured_movies` (List[Dict]): List of featured movies with keys `movie_id`, `title`, `poster_url`, etc.

### Navigation Flows
- `browse-movies-button` -> `/movies` (Movie Catalog Page)
- `view-bookings-button` -> `/bookings` (Booking History Page)
- `showtimes-button` -> `/showtimes` or possibly `/showtimes?movie_id=` (Showtime Selection Page)

---

## 2. Movie Catalog Page

- **Template Filename**: movie_catalog.html
- **Page Title**: Movie Catalog

### Element IDs and Types
- `catalog-page` (Div): Container for the catalog page.
- `search-input` (Input): Search input for filtering movies by title or genre.
- `genre-filter` (Dropdown Select): Dropdown to filter movies by genre.
- `movies-grid` (Div): Grid container showing movie cards.
- `view-movie-button-{movie_id}` (Button): Button on each movie card to view movie details.

### Context Variables
- `movies` (List[Dict]): List of movie dictionaries with keys: `movie_id`, `title`, `poster_url`, `rating`, `duration`, `genre`, etc.
- `genres` (List[str]): List of genres for filter dropdown.
- `search_query` (str): Current search term.
- `selected_genre` (str): Currently selected genre filter.

### Navigation Flows
- `view-movie-button-{movie_id}` -> `/movies/{movie_id}` (Movie Details Page)

---

## 3. Movie Details Page

- **Template Filename**: movie_details.html
- **Page Title**: Movie Details

### Element IDs and Types
- `movie-details-page` (Div): Main container.
- `movie-title` (H1): Displays the movie's title.
- `movie-director` (Div): Displays movie director.
- `movie-rating` (Div): Displays movie rating.
- `movie-description` (Div): Displays movie description.
- `select-showtime-button` (Button): Proceeds to showtime selection.

### Context Variables
- `movie` (Dict): Movie details with keys: `movie_id`, `title`, `director`, `rating`, `description`, `duration`, `genre`, etc.

### Navigation Flows
- `select-showtime-button` -> `/showtimes?movie_id={movie_id}` (Showtime Selection Page for selected movie)

---

## 4. Showtime Selection Page

- **Template Filename**: showtime_selection.html
- **Page Title**: Select Showtime

### Element IDs and Types
- `showtime-page` (Div): Main container.
- `showtimes-list` (Div): List or grid showing available showtimes.
- `theater-filter` (Dropdown Select): Filter showtimes by theater.
- `date-filter` (Input type=date): Filter showtimes by date.
- `select-showtime-button-{showtime_id}` (Button): Button to select a showtime.

### Context Variables
- `showtimes` (List[Dict]): List of showtime dictionaries with keys: `showtime_id`, `movie_id`, `theater_name`, `showtime_date`, `showtime_time`, `price`.
- `theaters` (List[Dict]): List of theaters with keys: `theater_id`, `theater_name`.
- `selected_theater_id` (Optional[int]): Currently selected theater filter.
- `selected_date` (Optional[str]): Currently selected date filter in YYYY-MM-DD format.
- `movie` (Optional[Dict]): If filtering showtimes by a movie.

### Navigation Flows
- `select-showtime-button-{showtime_id}` -> `/seats?showtime_id={showtime_id}` (Seat Selection Page)

---

## 5. Seat Selection Page

- **Template Filename**: seat_selection.html
- **Page Title**: Select Seats

### Element IDs and Types
- `seat-selection-page` (Div): Main container.
- `seat-map` (Div): Interactive map of seats; each seat a button.
- `seat-{row}{col}` (Button): Individual seats, e.g. seat-A1, seat-B3.
- `selected-seats-display` (Div): Displays seats currently selected.
- `proceed-booking-button` (Button): Proceeds to booking confirmation.

### Context Variables
- `showtime` (Dict): Showtime details.
- `seats` (List[Dict]): List of seats for the showtime with keys: `seat_id`, `row`, `column`, `status` (Available/Booked), `seat_type`.
- `selected_seats` (List[str]): List of seat identifiers selected.

### Navigation Flows
- Clicking `seat-{row}{col}` toggles selection state for that seat.
- `proceed-booking-button` -> `/booking_confirmation?showtime_id={showtime_id}&seats={selected_seats_csv}` (Booking Confirmation Page)

---

## 6. Booking Confirmation Page

- **Template Filename**: booking_confirmation.html
- **Page Title**: Booking Confirmation

### Element IDs and Types
- `confirmation-page` (Div): Main container.
- `booking-summary` (Div): Summary of booking details (movie, showtime, seats, prices).
- `customer-name` (Input): Input field for customer's name.
- `customer-email` (Input): Input field for customer's email.
- `confirm-booking-button` (Button): Button to finalize booking.

### Context Variables
- `showtime` (Dict): Showtime details.
- `movie` (Dict): Movie details.
- `selected_seats` (List[str]): Selected seats.
- `total_price` (Float): Booking total price.

### Navigation Flows
- `confirm-booking-button` triggers booking save and navigates to booking history page or booking success page.

---

## 7. Booking History Page

- **Template Filename**: booking_history.html
- **Page Title**: Booking History

### Element IDs and Types
- `bookings-page` (Div): Main container.
- `bookings-table` (Table): Displays bookings.
- `view-booking-button-{booking_id}` (Button): Button to view details of a booking.
- `status-filter` (Dropdown Select): Filter by booking status.
- `back-to-dashboard` (Button): Navigates to dashboard.

### Context Variables
- `bookings` (List[Dict]): Booking entries with keys: `booking_id`, `movie_title`, `booking_date`, `seats_booked`, `status`.
- `status_options` (List[str]): e.g. [All, Confirmed, Cancelled, Completed]
- `selected_status` (str): Currently selected booking status filter.

### Navigation Flows
- `view-booking-button-{booking_id}` -> `/bookings/{booking_id}` (Booking Detail Page, if implemented)
- `back-to-dashboard` -> `/` (Dashboard Page)

---

## 8. Theater Information Page

- **Template Filename**: theater_information.html
- **Page Title**: Theater Information

### Element IDs and Types
- `theater-page` (Div): Main container.
- `theaters-list` (Div): List of theater cards.
- `theater-location-filter` (Dropdown Select): Filter theaters by location (city).
- `facilities-display` (Div): Shows theater facilities.
- `back-to-dashboard` (Button): Navigates to Dashboard.

### Context Variables
- `theaters` (List[Dict]): List of theaters including `theater_id`, `theater_name`, `location`, `city`, `screens`, `facilities`.
- `locations` (List[str]): List of cities for filtering.
- `selected_location` (str): Currently selected location filter.

### Navigation Flows
- `back-to-dashboard` -> `/` (Dashboard Page)

---

# Summary
The above frontend design specification defines all eight pages of the MovieTicketing web application with detailed element IDs, context variables necessary to render templates and data dynamically, and navigation flow mappings ensuring a coherent user experience starting at the Dashboard. This design is aligned explicitly with the provided user task description and requirements.
