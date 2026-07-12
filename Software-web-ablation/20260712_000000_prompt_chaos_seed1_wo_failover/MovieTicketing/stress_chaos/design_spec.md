# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name           | HTTP Method | Template Rendered        | Context Variables (type)                                                                                                               |
| ------------------------- | -----------------------| ------------| ------------------------| --------------------------------------------------------------------------------------------------------------------------------------|
| /                         | root_redirect           | GET         | N/A (redirect to dashboard) | N/A                                                                                                                                |
| /dashboard                | dashboard_page          | GET         | dashboard.html           | featured_movies (list of dict: movie_id:int, title:str, genre:str, rating:float), upcoming_releases (list of dict: movie_id:int, title:str, release_date:str) |
| /movies                  | movie_catalog           | GET         | movie_catalog.html       | movies (list of dict: movie_id:int, title:str, genre:str, rating:float, duration:int)                                                |
| /movies/<int:movie_id>    | movie_details           | GET         | movie_details.html       | movie (dict: movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str)         |
| /movies/<int:movie_id>/showtimes | showtime_selection | GET         | showtime_selection.html  | showtimes (list of dict: showtime_id:int, theater_id:int, theater_name:str, showtime_date:str, showtime_time:str, price:float), theaters (list of dict: theater_id:int, theater_name:str) |
| /showtimes/<int:showtime_id>/seats | seat_selection | GET         | seat_selection.html      | seat_map (list of dict: seat_id:int, row:str, column:int, seat_type:str, status:str), selected_seats (list of str seat IDs)           |
| /bookings/confirm        | booking_confirmation    | GET, POST   | booking_confirmation.html| booking_summary (dict: movie_title:str, showtime_date:str, showtime_time:str, theater_name:str, seats_selected (list of str), total_price:float), error_message (str, optional) |
| /bookings/history        | booking_history         | GET         | booking_history.html     | bookings (list of dict: booking_id:int, movie_title:str, booking_date:str, seats_booked (list of str), status:str)                     |
| /bookings/<int:booking_id> | booking_details        | GET         | booking_details.html     | booking (dict: booking_id:int, movie_title:str, showtime_date:str, showtime_time:str, theater_name:str, customer_name:str, customer_email:str, seats_booked (list of str), status:str) |
| /theaters                | theater_information     | GET         | theater_information.html | theaters (list of dict: theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str)                        |


---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title> and <h1>: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-movies (Div): Display area for featured movie recommendations.
  - browse-movies-button (Button): Navigates to movie_catalog (function name: movie_catalog).
  - view-bookings-button (Button): Navigates to booking_history (function name: booking_history).
  - showtimes-button (Button): Navigates to showtime_selection root (function name: showtime_selection or route to select movie's showtimes).

### 2. Movie Catalog Page
- Filename: templates/movie_catalog.html
- Page Title: Movie Catalog
- <title> and <h1>: "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container for catalog page.
  - search-input (Input): Text input for searching movies by title or genre.
  - genre-filter (Dropdown): Filter movies by genre.
  - movies-grid (Div): Grid for displaying movie cards.
  - view-movie-button-{movie_id} (Button): Button on each movie card to view details; dynamic ID pattern.
- Navigation:
  - view-movie-button-{movie_id} triggers route movie_details with movie_id.

### 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <title> and <h1>: "Movie Details"
- Element IDs:
  - movie-details-page (Div): Container.
  - movie-title (H1): Displays movie title.
  - movie-director (Div): Displays director.
  - movie-rating (Div): Displays rating.
  - movie-description (Div): Movie description.
  - select-showtime-button (Button): Navigate to showtime_selection page for this movie.
- Navigation:
  - select-showtime-button triggers route showtime_selection with movie_id.

### 4. Showtime Selection Page
- Filename: templates/showtime_selection.html
- Page Title: Select Showtime
- <title> and <h1>: "Select Showtime"
- Element IDs:
  - showtime-page (Div): Container.
  - showtimes-list (Div): List of showtimes with date, time, theater, price.
  - theater-filter (Dropdown): Filter showtimes by theater.
  - date-filter (Input): Filter showtimes by date.
  - select-showtime-button-{showtime_id} (Button): For each showtime; selects showtime.
- Navigation:
  - select-showtime-button-{showtime_id} triggers seat_selection route with showtime_id.

### 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <title> and <h1>: "Select Seats"
- Element IDs:
  - seat-selection-page (Div): Container.
  - seat-map (Div): Interactive seat map.
  - selected-seats-display (Div): Shows currently selected seats.
  - seat-{row}{col} (Button): Individual seats, e.g., seat-A1, seat-B3.
  - proceed-booking-button (Button): Proceed to booking confirmation.
- Navigation:
  - proceed-booking-button triggers booking_confirmation route.

### 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <title> and <h1>: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container.
  - booking-summary (Div): Summary of booking details.
  - customer-name (Input): Input for customer name.
  - customer-email (Input): Input for customer email.
  - confirm-booking-button (Button): Confirm and complete booking.
- Navigation:
  - confirm-booking-button triggers POST to booking_confirmation route.

### 7. Booking History Page
- Filename: templates/booking_history.html
- Page Title: Booking History
- <title> and <h1>: "Booking History"
- Element IDs:
  - bookings-page (Div): Container.
  - bookings-table (Table): Displays booking details.
  - view-booking-button-{booking_id} (Button): View booking details; dynamic ID.
  - status-filter (Dropdown): Filter bookings by status.
  - back-to-dashboard (Button): Navigate to dashboard_page route.

### 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <title> and <h1>: "Theater Information"
- Element IDs:
  - theater-page (Div): Container.
  - theaters-list (Div): List all theaters.
  - theater-location-filter (Dropdown): Filter theaters by location.
  - facilities-display (Div): Display facilities.
  - back-to-dashboard (Button): Navigate to dashboard_page route.


---

## Section 3: Data File Schemas

### 1. Movies Data
- Filename: data/movies.txt
- Fields (pipe '|' separated):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores movie details including title, director, genre, rating, duration in minutes, description, and release date.
- Example rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data
- Filename: data/theaters.txt
- Fields:
  theater_id|theater_name|location|city|screens|facilities
- Description: Contains theater info including location, number of screens, and facilities available.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data
- Filename: data/showtimes.txt
- Fields:
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtimes for movies including date/time, theater, price, and seats available.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data
- Filename: data/seats.txt
- Fields:
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat layout and booking status per theater screen.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data
- Filename: data/bookings.txt
- Fields:
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Customer booking records including seats and status.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data
- Filename: data/genres.txt
- Fields:
  genre_id|genre_name|description
- Description: Movie genres with descriptive text.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This design specification document provides full details for backend and frontend development in parallel, ensuring clear boundaries and consistent naming for seamless integration.