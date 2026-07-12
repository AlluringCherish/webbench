# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name         | HTTP Method | Template Rendered           | Context Variables Passed                                            |
|------------------------------- |--------------------- |-------------|-----------------------------|--------------------------------------------------------------------|
| /                              | root_redirect         | GET         | None (redirect to /dashboard) | None                                                               |
| /dashboard                    | dashboard            | GET         | dashboard.html              | featured_movies: list[dict] with {movie_id:int, title:str, rating:float, duration:int}
|                               |                      |             |                             | upcoming_releases: list[dict] with {movie_id:int, title:str, release_date:str}
| /movies                        | movie_catalog        | GET         | catalog.html                | movies: list[dict] with {movie_id:int, title:str, genre:str, rating:float, duration:int}
|                               |                      |             |                             | genres: list[str]
| /movies/<int:movie_id>         | movie_details        | GET         | movie_details.html          | movie: dict with {movie_id:int, title:str, director:str, rating:float, description:str}
| /showtimes/<int:movie_id>      | showtime_selection   | GET         | showtimes.html              | showtimes: list[dict] with {showtime_id:int, showtime_date:str, showtime_time:str, theater_name:str, price:float}
|                               |                      |             |                             | theaters: list[str]
| /seat-selection/<int:showtime_id> | seat_selection     | GET         | seat_selection.html         | seat_map: list[dict] with {seat_id:int, row:str, column:int, seat_type:str, status:str}
|                               |                      |             |                             | selected_showtime: dict with {showtime_id:int, movie_title:str, theater_name:str, showtime_date:str, showtime_time:str}
| /booking-confirmation          | booking_confirmation | POST        | booking_confirmation.html   | booking_summary: dict with {movie_title:str, showtime_date:str, showtime_time:str, seats:list[str], total_price:float}
|                               |                      |             |                             | error_message: str (optional)
| /booking-history              | booking_history      | GET         | bookings.html               | bookings: list[dict] with {booking_id:int, movie_title:str, booking_date:str, seats:str, status:str}
|                               |                      |             |                             | status_options: list[str] (All, Confirmed, Cancelled, Completed)
| /booking-history/<int:booking_id> | booking_details    | GET         | booking_details.html        | booking: dict with {booking_id:int, movie_title:str, showtime_date:str, seats:list[str], status:str, customer_name:str, customer_email:str, total_price:float}
| /theaters                    | theater_information  | GET         | theater_information.html    | theaters: list[dict] with {theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str}
|                               |                      |             |                             | locations: list[str]

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title>: "Movie Ticketing Dashboard"
- <h1>: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - featured-movies (Div): Display featured movie recommendations
  - browse-movies-button (Button): Button to navigate to movie catalog page
  - view-bookings-button (Button): Button to navigate to booking history page
  - showtimes-button (Button): Button to navigate to showtimes page
- Navigation:
  - browse-movies-button: url_for('movie_catalog')
  - view-bookings-button: url_for('booking_history')
  - showtimes-button: url_for('showtime_selection', movie_id=<default_movie_id>)

### 2. Movie Catalog Page
- Filename: templates/catalog.html
- Page Title: Movie Catalog
- <title>: "Movie Catalog"
- <h1>: "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container for catalog page
  - search-input (Input): Field to search by title or genre
  - genre-filter (Dropdown): Dropdown to filter by genre
  - movies-grid (Div): Grid displaying movie cards
  - view-movie-button-{movie_id} (Button): Button to view movie details
- Navigation:
  - view-movie-button-{movie_id}: url_for('movie_details', movie_id=movie_id)

### 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <title>: "Movie Details"
- <h1>: movie's title (dynamic)
- Element IDs:
  - movie-details-page (Div): Container for movie details page
  - movie-title (H1): Displays movie title
  - movie-director (Div): Displays movie director
  - movie-rating (Div): Displays movie rating
  - movie-description (Div): Displays movie description
  - select-showtime-button (Button): Button to go to showtime selection
- Navigation:
  - select-showtime-button: url_for('showtime_selection', movie_id=movie_id)

### 4. Showtime Selection Page
- Filename: templates/showtimes.html
- Page Title: Select Showtime
- <title>: "Select Showtime"
- <h1>: "Select Showtime"
- Element IDs:
  - showtime-page (Div): Container for showtime page
  - showtimes-list (Div): List of showtimes
  - theater-filter (Dropdown): Filter showtimes by theater
  - date-filter (Input): Field to filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): Button to select a showtime
- Navigation:
  - select-showtime-button-{showtime_id}: url_for('seat_selection', showtime_id=showtime_id)

### 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <title>: "Select Seats"
- <h1>: "Select Seats"
- Element IDs:
  - seat-selection-page (Div): Container for seat selection page
  - seat-map (Div): Interactive seat map
  - selected-seats-display (Div): Displays selected seats
  - seat-{row}{col} (Button): Individual seat buttons (e.g., seat-A1)
  - proceed-booking-button (Button): Button to proceed to booking confirmation
- Navigation:
  - proceed-booking-button: url_for('booking_confirmation')

### 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <title>: "Booking Confirmation"
- <h1>: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container for confirmation page
  - booking-summary (Div): Summary of booking details
  - customer-name (Input): Input for customer name
  - customer-email (Input): Input for customer email
  - confirm-booking-button (Button): Button to confirm booking
- Navigation:
  - confirm-booking-button: POST form to booking_confirmation

### 7. Booking History Page
- Filename: templates/bookings.html
- Page Title: Booking History
- <title>: "Booking History"
- <h1>: "Booking History"
- Element IDs:
  - bookings-page (Div): Container for bookings page
  - bookings-table (Table): Table displaying booking records
  - view-booking-button-{booking_id} (Button): Button to view booking details
  - status-filter (Dropdown): Filter bookings by status
  - back-to-dashboard (Button): Button to navigate back to dashboard
- Navigation:
  - view-booking-button-{booking_id}: url_for('booking_details', booking_id=booking_id)
  - back-to-dashboard: url_for('dashboard')

### 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <title>: "Theater Information"
- <h1>: "Theater Information"
- Element IDs:
  - theater-page (Div): Container for theater page
  - theaters-list (Div): List of theaters with location, screens, facilities
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Display theater facilities and amenities
  - back-to-dashboard (Button): Button to navigate back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### 1. Movies Data
- File: data/movies.txt
- Fields (pipe-delimited, exact order):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores movie details.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data
- File: data/theaters.txt
- Fields (pipe-delimited, exact order):
  theater_id|theater_name|location|city|screens|facilities
- Description: Stores theater information and facilities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data
- File: data/showtimes.txt
- Fields (pipe-delimited, exact order):
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtime details.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data
- File: data/seats.txt
- Fields (pipe-delimited, exact order):
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seat details per theater and screen including availability.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data
- File: data/bookings.txt
- Fields (pipe-delimited, exact order):
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking records including seat selections.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data
- File: data/genres.txt
- Fields (pipe-delimited, exact order):
  genre_id|genre_name|description
- Description: Stores genre categories with descriptions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
