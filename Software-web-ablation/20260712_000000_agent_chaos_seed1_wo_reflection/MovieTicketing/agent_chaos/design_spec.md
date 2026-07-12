# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                          | Function Name              | HTTP Methods | Template                    | Context Variables (with Types and Structures)              |
|-----------------------------------|----------------------------|--------------|-----------------------------|-------------------------------------------------------------|
| /                                 | root_redirect               | GET          | None (Redirect to /dashboard) | None                                                        |
| /dashboard                        | dashboard                  | GET          | dashboard.html              | featured_movies (list of dict)                              |
|                                   |                            |              |                             | - Each dict: {movie_id: int, title: str, rating: float, duration: int} |
| /movies                          | movie_catalog              | GET          | movie_catalog.html          | movies (list of dict), genres (list of dict)                |
|                                   |                            |              |                             | - movies dict: {movie_id: int, title: str, genre: str, rating: float, duration: int, poster_url: str} (poster_url is optional or can be constructed)
|                                   |                            |              |                             | - genres dict: {genre_id: int, genre_name: str}              |
| /movies/search                   | movie_search               | POST         | movie_catalog.html          | filtered_movies (list of dict), genres (list of dict)       |
| /movies/<int:movie_id>           | movie_details              | GET          | movie_details.html          | movie (dict), where movie dict: {movie_id: int, title: str, director: str, genre: str, rating: float, duration: int, description: str} |
| /showtimes                     | showtime_selection         | GET          | showtime_selection.html     | showtimes (list of dict), theaters (list of dict)           |
|                                   |                            |              |                             | - showtimes dict: {showtime_id: int, movie_id: int, theater_id: int, showtime_date: str, showtime_time: str, price: float}  |
|                                   |                            |              |                             | - theaters dict: {theater_id: int, theater_name: str, location: str}  |
| /select_showtime/<int:showtime_id> | select_showtime           | GET          | seat_selection.html         | seats (list of dict), showtime (dict)                       |
|                                   |                            |              |                             | - seats dict: {seat_id: int, theater_id: int, screen_id: int, row: str, column: int, seat_type: str, status: str}
|                                   |                            |              |                             | - showtime dict: {showtime_id: int, movie_id: int, theater_id: int, showtime_date: str, showtime_time: str, price: float}  |
| /book_seats                    | book_seats                 | POST         | booking_confirmation.html   | booking_summary (dict)                                      |
|                                   |                            |              |                             | - booking_summary dict: {movie_title: str, showtime_datetime: str, seats: list of str, total_price: float}  |
| /confirm_booking                | confirm_booking            | POST         | booking_confirmation.html   | confirmation_status (str), booking_id (int, optional)       |
| /bookings                      | booking_history            | GET          | booking_history.html        | bookings (list of dict)                                     |
|                                   |                            |              |                             | - bookings dict: {booking_id: int, movie_title: str, booking_date: str, seats_booked: list of str, status: str}            |
| /bookings/<int:booking_id>       | booking_details            | GET          | booking_details.html        | booking (dict)                                             |
|                                   |                            |              |                             | - booking dict: {booking_id: int, movie_title: str, showtime_date: str, showtime_time: str, seats_booked: list of str, customer_name: str, customer_email: str, total_price: float, status: str} |
| /theaters                      | theater_information        | GET          | theater_information.html    | theaters (list of dict)                                    |
|                                   |                            |              |                             | - theaters dict: {theater_id: int, theater_name: str, location: str, city: str, screens: int, facilities: str}               |


---

## Section 2: HTML Template Specifications

### 1. Template: templates/dashboard.html
- Page Title: "Movie Ticketing Dashboard"
- <h1> Title: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - featured-movies (Div): Display featured movies
  - browse-movies-button (Button): Navigate to movie_catalog
  - view-bookings-button (Button): Navigate to booking_history
  - showtimes-button (Button): Navigate to showtime_selection

- Navigation mapping:
  - browse-movies-button => function: movie_catalog
  - view-bookings-button => function: booking_history
  - showtimes-button => function: showtime_selection

### 2. Template: templates/movie_catalog.html
- Page Title: "Movie Catalog"
- <h1> Title: "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container for movie catalog page
  - search-input (Input): Search movies by title or genre
  - genre-filter (Dropdown): Filter movies by genre
  - movies-grid (Div): Grid displaying movies
  - view-movie-button-{movie_id} (Button): View details of movie with id movie_id

- Navigation mapping:
  - view-movie-button-{movie_id} => function: movie_details (parameter: movie_id)

### 3. Template: templates/movie_details.html
- Page Title: "Movie Details"
- <h1> Title: movie title (dynamic from context variable movie.title)
- Element IDs:
  - movie-details-page (Div): Container for movie details page
  - movie-title (H1): Movie title
  - movie-director (Div): Movie director
  - movie-rating (Div): Movie rating
  - movie-description (Div): Movie description
  - select-showtime-button (Button): Proceed to select showtime

- Navigation mapping:
  - select-showtime-button => function: showtime_selection (query parameter: movie_id)

### 4. Template: templates/showtime_selection.html
- Page Title: "Select Showtime"
- <h1> Title: "Select Showtime"
- Element IDs:
  - showtime-page (Div): Container for showtime page
  - showtimes-list (Div): List of showtimes
  - theater-filter (Dropdown): Filter showtimes by theater
  - date-filter (Input): Filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): Select specific showtime

- Navigation mapping:
  - select-showtime-button-{showtime_id} => function: select_showtime (parameter: showtime_id)

### 5. Template: templates/seat_selection.html
- Page Title: "Select Seats"
- <h1> Title: "Select Seats"
- Element IDs:
  - seat-selection-page (Div): Container for seat selection
  - seat-map (Div): Interactive seat map showing seats
  - selected-seats-display (Div): Show selected seats
  - seat-{row}{col} (Button): Individual seat button (e.g., seat-A1)
  - proceed-booking-button (Button): Proceed to booking confirmation

- Navigation mapping:
  - proceed-booking-button => function: book_seats

### 6. Template: templates/booking_confirmation.html
- Page Title: "Booking Confirmation"
- <h1> Title: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container for confirmation page
  - booking-summary (Div): Summary of booking details
  - customer-name (Input): Customer name input
  - customer-email (Input): Customer email input
  - confirm-booking-button (Button): Confirm and complete booking

- Navigation mapping:
  - confirm-booking-button => function: confirm_booking

### 7. Template: templates/booking_history.html
- Page Title: "Booking History"
- <h1> Title: "Booking History"
- Element IDs:
  - bookings-page (Div): Container for bookings page
  - bookings-table (Table): Displays bookings
  - view-booking-button-{booking_id} (Button): View booking details
  - status-filter (Dropdown): Filter bookings by status
  - back-to-dashboard (Button): Return to dashboard

- Navigation mapping:
  - view-booking-button-{booking_id} => function: booking_details (parameter: booking_id)
  - back-to-dashboard => function: dashboard

### 8. Template: templates/theater_information.html
- Page Title: "Theater Information"
- <h1> Title: "Theater Information"
- Element IDs:
  - theater-page (Div): Container for theater page
  - theaters-list (Div): List of theaters
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Show theater facilities
  - back-to-dashboard (Button): Return to dashboard

- Navigation mapping:
  - back-to-dashboard => function: dashboard

---

## Section 3: Data File Schemas

### 1. Movies Data File
- Filename: data/movies.txt
- Field order: movie_id|title|director|genre|rating|duration|description|release_date
- Description: Contains all movies data including metadata and description with release dates.
- Example rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data File
- Filename: data/theaters.txt
- Field order: theater_id|theater_name|location|city|screens|facilities
- Description: Contains all theaters with location, screen count and amenities.
- Example rows:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data File
- Filename: data/showtimes.txt
- Field order: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Contains showtime schedules, pricing and availability.
- Example rows:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data File
- Filename: data/seats.txt
- Field order: seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Lists seats with location and status.
- Example rows:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data File
- Filename: data/bookings.txt
- Field order: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking records with user and seat details.
- Example rows:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data File
- Filename: data/genres.txt
- Field order: genre_id|genre_name|description
- Description: Defines movie genres with descriptions.
- Example rows:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This specification fully covers all user requirements and enables backend and frontend teams to work independently and in parallel without ambiguity.