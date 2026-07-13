# MovieTicketing Web Application Design Specification

---

## Section 1: Page and UI Element Specification

### 1. Dashboard Page
- **Page Title**: Movie Ticketing Dashboard
- **Container ID**: dashboard-page (Div)
- **UI Elements:**
  - featured-movies (Div): Display of featured movie recommendations.
  - browse-movies-button (Button): Navigate to Movie Catalog page.
  - view-bookings-button (Button): Navigate to Booking History page.
  - showtimes-button (Button): Navigate to Showtimes page.

### 2. Movie Catalog Page
- **Page Title**: Movie Catalog
- **Container ID**: catalog-page (Div)
- **UI Elements:**
  - search-input (Input): Search movies by title or genre.
  - genre-filter (Dropdown): Filter movies by genre (Action, Comedy, Drama, Horror, etc.).
  - movies-grid (Div): Grid showing movie cards with poster, title, rating, duration.
  - view-movie-button-{movie_id} (Button): Button on each movie card to view movie details.

### 3. Movie Details Page
- **Page Title**: Movie Details
- **Container ID**: movie-details-page (Div)
- **UI Elements:**
  - movie-title (H1): Movie title display.
  - movie-director (Div): Movie director display.
  - movie-rating (Div): Movie rating display.
  - movie-description (Div): Movie description display.
  - select-showtime-button (Button): Proceed to showtime selection page.

### 4. Showtime Selection Page
- **Page Title**: Select Showtime
- **Container ID**: showtime-page (Div)
- **UI Elements:**
  - showtimes-list (Div): List of showtimes with date, time, theater, price.
  - theater-filter (Dropdown): Filter showtimes by theater.
  - date-filter (Input): Filter showtimes by date.
  - select-showtime-button-{showtime_id} (Button): Select a specific showtime.

### 5. Seat Selection Page
- **Page Title**: Select Seats
- **Container ID**: seat-selection-page (Div)
- **UI Elements:**
  - seat-map (Div): Interactive seat map showing seats availability.
  - selected-seats-display (Div): Displays currently selected seats.
  - seat-{row}{col} (Button): Individual seat buttons (e.g. seat-A1, seat-B3).
  - proceed-booking-button (Button): Proceed to booking confirmation.

### 6. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Container ID**: confirmation-page (Div)
- **UI Elements:**
  - booking-summary (Div): Summary of booking (movie, showtime, seats, total price).
  - customer-name (Input): Input customer name.
  - customer-email (Input): Input customer email.
  - confirm-booking-button (Button): Confirm and complete booking.

### 7. Booking History Page
- **Page Title**: Booking History
- **Container ID**: bookings-page (Div)
- **UI Elements:**
  - bookings-table (Table): Table with booking ID, movie, date, seats, status.
  - view-booking-button-{booking_id} (Button): View booking details for each booking.
  - status-filter (Dropdown): Filter bookings by status (All, Confirmed, Cancelled, Completed).
  - back-to-dashboard (Button): Navigate back to Dashboard.

### 8. Theater Information Page
- **Page Title**: Theater Information
- **Container ID**: theater-page (Div)
- **UI Elements:**
  - theaters-list (Div): List of theaters with location, screens, and facilities.
  - theater-location-filter (Dropdown): Filter theaters by location.
  - facilities-display (Div): Theater facilities and amenities display.
  - back-to-dashboard (Button): Navigate back to Dashboard.

---

## Section 2: Navigation Flow

- **Dashboard Page to:**
  - Movie Catalog via browse-movies-button
  - Booking History via view-bookings-button
  - Showtime Selection via showtimes-button

- **Movie Catalog to Movie Details:**
  - view-movie-button-{movie_id} navigates to Movie Details page for selected movie

- **Movie Details to Showtime Selection:**
  - select-showtime-button navigates to Showtime Selection page for that movie

- **Showtime Selection to Seat Selection:**
  - select-showtime-button-{showtime_id} navigates to Seat Selection page

- **Seat Selection to Booking Confirmation:**
  - proceed-booking-button navigates to Booking Confirmation page

- **Booking Confirmation to Dashboard:**
  - confirm-booking-button completes booking and navigates back to Dashboard

- **Booking History:**
  - back-to-dashboard button returns to Dashboard
  - view-booking-button-{booking_id} shows details of a booking (future expansion)

- **Theater Information:**
  - back-to-dashboard button returns to Dashboard

---

## Section 3: Data Storage Formats

All data files are stored in the `data` directory with the following exact formats.

### 1. movies.txt
- Fields (pipe-delimited):
  `movie_id|title|director|genre|rating|duration|description|release_date`
- Data types:
  - movie_id: int
  - title: string
  - director: string
  - genre: string
  - rating: float
  - duration: int (minutes)
  - description: string
  - release_date: yyyy-mm-dd string
- Examples:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 2. theaters.txt
- Fields (pipe-delimited):
  `theater_id|theater_name|location|city|screens|facilities`
- Data types:
  - theater_id: int
  - theater_name: string
  - location: string
  - city: string
  - screens: int
  - facilities: string (comma-separated list)
- Examples:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 3. showtimes.txt
- Fields (pipe-delimited):
  `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- Data types:
  - showtime_id: int
  - movie_id: int
  - theater_id: int
  - showtime_date: yyyy-mm-dd string
  - showtime_time: HH:mm string
  - price: float
  - available_seats: int
- Examples:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4. seats.txt
- Fields (pipe-delimited):
  `seat_id|theater_id|screen_id|row|column|seat_type|status`
- Data types:
  - seat_id: int
  - theater_id: int
  - screen_id: int
  - row: string (alphabetic)
  - column: int
  - seat_type: string (e.g., Standard, Premium)
  - status: string (Available or Booked)
- Examples:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 5. bookings.txt
- Fields (pipe-delimited):
  `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- Data types:
  - booking_id: int
  - showtime_id: int
  - customer_name: string
  - customer_email: string
  - booking_date: yyyy-mm-dd string
  - total_price: float
  - status: string (Confirmed, Cancelled, Completed)
  - seats_booked: string (comma-separated seat labels e.g., A1,A2)
- Examples:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 6. genres.txt
- Fields (pipe-delimited):
  `genre_id|genre_name|description`
- Data types:
  - genre_id: int
  - genre_name: string
  - description: string
- Examples:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

This completes the full design specification for the MovieTicketing web application for implementation.
