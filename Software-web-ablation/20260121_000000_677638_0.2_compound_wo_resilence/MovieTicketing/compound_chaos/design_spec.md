# Design Specification Document for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name            | HTTP Method | Template Rendered           | Context Variables (type)                                                                                                                  |
|-------------------------------|--------------------------|-------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect             | GET         | Redirect to /dashboard       | None                                                                                                                                    |
| /dashboard                    | dashboard                 | GET         | dashboard.html              | featured_movies (list of dict), upcoming_releases (list of dict)                                                                         |
| /movies                      | movie_catalog             | GET         | movie_catalog.html          | movies (list of dict), genres (list of dict), selected_genre (str), search_query (str)                                                   |
| /movies/<int:movie_id>       | movie_details             | GET         | movie_details.html          | movie (dict), movie_id (int)                                                                                                            |
| /movies/<int:movie_id>/showtimes | showtime_selection        | GET         | showtime_selection.html     | movie (dict), showtimes (list of dict), theaters (list of dict), selected_theater (str), selected_date (str)                            |
| /showtimes/<int:showtime_id>/seats | seat_selection            | GET         | seat_selection.html         | showtime (dict), seats (list of dict), selected_seats (list of str)                                                                      |
| /showtimes/<int:showtime_id>/book | booking_confirmation      | GET         | booking_confirmation.html   | booking_summary (dict), available_seats (int)                                                                                          |
| /showtimes/<int:showtime_id>/book | confirm_booking           | POST        | booking_confirmation.html   | form_data (dict), booking_success (bool), errors (list of str)                                                                          |
| /bookings                    | booking_history           | GET         | booking_history.html        | bookings (list of dict), filtered_status (str)                                                                                          |
| /bookings/<int:booking_id>   | booking_details           | GET         | booking_details.html        | booking (dict)                                                                                                                          |
| /theaters                   | theater_information       | GET         | theater_information.html    | theaters (list of dict), selected_location (str)                                                                                        |

---

### Detailed Context Variable Structures

- featured_movies: List of dicts with fields:
  - movie_id (int)
  - title (str)
  - poster_url (str)
  - rating (float)
- upcoming_releases: List of dicts with fields:
  - movie_id (int)
  - title (str)
  - release_date (str) // Format: YYYY-MM-DD
- movies: List of dicts with fields:
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int) // duration in minutes
  - description (str)
  - release_date (str) // Format: YYYY-MM-DD
- genres: List of dicts with fields:
  - genre_id (int)
  - genre_name (str)
  - description (str)
- movie: Dict with fields:
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int)
  - description (str)
  - release_date (str)
- showtimes: List of dicts with fields:
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (str) // Format: YYYY-MM-DD
  - showtime_time (str) // Format: HH:MM
  - price (float)
  - available_seats (int)
- theaters: List of dicts with fields:
  - theater_id (int)
  - theater_name (str)
  - location (str)
  - city (str)
  - screens (int)
  - facilities (str)
- showtime: Dict with fields:
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (str)
  - showtime_time (str)
  - price (float)
  - available_seats (int)
- seats: List of dicts with fields:
  - seat_id (int)
  - theater_id (int)
  - screen_id (int)
  - row (str) // single character like 'A', 'B', etc.
  - column (int)
  - seat_type (str) // Standard, Premium, etc.
  - status (str) // Available, Booked
- selected_seats: List of strings (seat labels like "A1", "B3")
- booking_summary: Dict with fields:
  - movie_title (str)
  - showtime_date (str)
  - showtime_time (str)
  - theater_name (str)
  - seats (list of str)
  - total_price (float)
- bookings: List of dicts with fields:
  - booking_id (int)
  - showtime_id (int)
  - customer_name (str)
  - customer_email (str)
  - booking_date (str)
  - total_price (float)
  - status (str) // Confirmed, Cancelled, Completed
  - seats_booked (str) // comma-separated seat labels
- booking: Dict with fields:
  - booking_id (int)
  - showtime_id (int)
  - customer_name (str)
  - customer_email (str)
  - booking_date (str)
  - total_price (float)
  - status (str)
  - seats_booked (str)
- available_seats: int
- filtered_status: str
- selected_genre: str
- search_query: str
- selected_theater: str
- selected_date: str
- selected_location: str
- form_data: dict with keys customer_name (str), customer_email (str)
- booking_success: bool
- errors: list of str

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title> tag: Movie Ticketing Dashboard
- <h1> tag: Movie Ticketing Dashboard
- Elements:
  - ID: dashboard-page (Div) - Main container
  - ID: featured-movies (Div) - Displays featured movie recommendations
  - ID: browse-movies-button (Button) - Navigates to movie_catalog route
  - ID: view-bookings-button (Button) - Navigates to booking_history route
  - ID: showtimes-button (Button) - Navigates to showtime_selection or global showtimes page

- Navigation Mapping:
  - browse-movies-button -> movie_catalog
  - view-bookings-button -> booking_history
  - showtimes-button -> showtime_selection (may require selecting movie — backend design allows initial showtime page)

---

### 2. templates/movie_catalog.html
- Page Title: Movie Catalog
- <title> tag: Movie Catalog
- <h1> tag: Movie Catalog
- Elements:
  - ID: catalog-page (Div) - Container for movie catalog
  - ID: search-input (Input) - Search box for movie title or genre
  - ID: genre-filter (Dropdown) - Filter dropdown by genres
  - ID: movies-grid (Div) - Grid layout container for movie cards
  - Dynamic Element IDs:
    - view-movie-button-{movie_id} (Button) - Button for each movie to view details

- Navigation Mapping:
  - view-movie-button-{movie_id} -> movie_details(movie_id)

---

### 3. templates/movie_details.html
- Page Title: Movie Details
- <title> tag: Movie Details
- <h1> tag: Contains movie title dynamically
- Elements:
  - ID: movie-details-page (Div) - Container
  - ID: movie-title (H1) - Movie title
  - ID: movie-director (Div) - Movie director
  - ID: movie-rating (Div) - Movie rating
  - ID: movie-description (Div) - Movie description
  - ID: select-showtime-button (Button) - Navigate to showtime_selection for this movie

- Navigation Mapping:
  - select-showtime-button -> showtime_selection(movie_id)

---

### 4. templates/showtime_selection.html
- Page Title: Select Showtime
- <title> tag: Select Showtime
- <h1> tag: Select Showtime
- Elements:
  - ID: showtime-page (Div) - Container
  - ID: showtimes-list (Div) - List of showtimes with details
  - ID: theater-filter (Dropdown) - Filter showtimes by theater
  - ID: date-filter (Input) - Filter showtimes by date
  - Dynamic Element IDs:
    - select-showtime-button-{showtime_id} (Button) - Button to select showtime

- Navigation Mapping:
  - select-showtime-button-{showtime_id} -> seat_selection(showtime_id)

---

### 5. templates/seat_selection.html
- Page Title: Select Seats
- <title> tag: Select Seats
- <h1> tag: Select Seats
- Elements:
  - ID: seat-selection-page (Div) - Container
  - ID: seat-map (Div) - Interactive seat map
  - ID: selected-seats-display (Div) - Display selected seat labels
  - Dynamic Element IDs:
    - seat-{row}{column} (Button) - Buttons for each seat
  - ID: proceed-booking-button (Button) - Proceed to booking confirmation

- Navigation Mapping:
  - proceed-booking-button -> booking_confirmation(showtime_id)

---

### 6. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <title> tag: Booking Confirmation
- <h1> tag: Booking Confirmation
- Elements:
  - ID: confirmation-page (Div) - Container
  - ID: booking-summary (Div) - Summary of booking details
  - ID: customer-name (Input) - Input for customer name
  - ID: customer-email (Input) - Input for customer email
  - ID: confirm-booking-button (Button) - Confirm booking

- Navigation Mapping:
  - confirm-booking-button -> confirm_booking (POST)

---

### 7. templates/booking_history.html
- Page Title: Booking History
- <title> tag: Booking History
- <h1> tag: Booking History
- Elements:
  - ID: bookings-page (Div) - Container
  - ID: bookings-table (Table) - Table to display bookings
  - Dynamic Element IDs:
    - view-booking-button-{booking_id} (Button) - For each booking
  - ID: status-filter (Dropdown) - Filter by booking status
  - ID: back-to-dashboard (Button) - Navigate back to dashboard

- Navigation Mapping:
  - view-booking-button-{booking_id} -> booking_details(booking_id)
  - back-to-dashboard -> dashboard

---

### 8. templates/theater_information.html
- Page Title: Theater Information
- <title> tag: Theater Information
- <h1> tag: Theater Information
- Elements:
  - ID: theater-page (Div) - Container
  - ID: theaters-list (Div) - List of theaters
  - ID: theater-location-filter (Dropdown) - Filter theaters by location
  - ID: facilities-display (Div) - Display facilities of selected theater
  - ID: back-to-dashboard (Button) - Navigate back to dashboard

- Navigation Mapping:
  - back-to-dashboard -> dashboard

---

## Section 3: Data File Schemas

### data/movies.txt
- Fields (pipe-delimited): movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores all movie details
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### data/theaters.txt
- Fields (pipe-delimited): theater_id|theater_name|location|city|screens|facilities
- Description: Stores theater information
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### data/showtimes.txt
- Fields (pipe-delimited): showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtime info for movies
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### data/seats.txt
- Fields (pipe-delimited): seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seat details per theater screen
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### data/bookings.txt
- Fields (pipe-delimited): booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking information
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### data/genres.txt
- Fields (pipe-delimited): genre_id|genre_name|description
- Description: Stores movie genres
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

*End of Design Specification.*
