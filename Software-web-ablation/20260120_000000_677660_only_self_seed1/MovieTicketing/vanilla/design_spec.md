# Design Specification Document for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name            | HTTP Method | Template Rendered           | Context Variables (type)                                                                                                                  |
|-------------------------------|--------------------------|-------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect             | GET         | Redirect to /dashboard       | None                                                                                                                                    |
| /dashboard                    | dashboard                | GET         | dashboard.html              | featured_movies (list of dict), upcoming_releases (list of dict)                                                                         |
| /movies                      | movie_catalog            | GET         | movie_catalog.html          | movies (list of dict), genres (list of dict), selected_genre (str), search_query (str)                                                   |
| /movies/<int:movie_id>       | movie_details            | GET         | movie_details.html          | movie (dict), genres (list of dict)                                                                                                    |
| /showtimes/<int:movie_id>    | showtime_selection       | GET         | showtime_selection.html     | movie (dict), showtimes (list of dict), theaters (list of dict), selected_theater (str), selected_date (str)                              |
| /select_seats/<int:showtime_id> | seat_selection          | GET         | seat_selection.html         | showtime (dict), seats (list of dict), selected_seats (list of str)                                                                      |
| /booking_confirmation         | booking_confirmation     | POST        | booking_confirmation.html   | booking_summary (dict), errors (list of str - optional)                                                                                 |
| /booking_confirmation/<int:booking_id> | booking_confirmation_get | GET  | booking_confirmation.html   | booking (dict)                                                                                                                          |
| /bookings                    | booking_history          | GET         | booking_history.html        | bookings (list of dict), filtered_status (str)                                                                                         |
| /bookings/<int:booking_id>   | booking_details          | GET         | booking_details.html        | booking (dict)                                                                                                                          |
| /theaters                    | theater_information      | GET         | theater_information.html    | theaters (list of dict), selected_location (str)                                                                                       |

### Context Variable Structures

- featured_movies, upcoming_releases (list of dict):
  - movie_id (int)
  - title (str)
  - poster_url (str) [optional for frontend display]

- movies (list of dict):
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int, minutes)
  - description (str)
  - release_date (str, yyyy-mm-dd)

- genres (list of dict):
  - genre_id (int)
  - genre_name (str)
  - description (str)

- movie (dict):
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int)
  - description (str)
  - release_date (str)

- showtimes (list of dict):
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (str, yyyy-mm-dd)
  - showtime_time (str, HH:MM)
  - price (float)
  - available_seats (int)

- theaters (list of dict):
  - theater_id (int)
  - theater_name (str)
  - location (str)
  - city (str)
  - screens (int)
  - facilities (str)

- showtime (dict):
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (str)
  - showtime_time (str)
  - price (float)
  - available_seats (int)

- seats (list of dict):
  - seat_id (int)
  - theater_id (int)
  - screen_id (int)
  - row (str) [single uppercase letter]
  - column (int)
  - seat_type (str) [e.g., Standard, Premium]
  - status (str) [Available, Booked]

- selected_seats (list of str): e.g., ['A1', 'B3']

- booking_summary (dict):
  - movie_title (str)
  - showtime_date (str)
  - showtime_time (str)
  - theater_name (str)
  - seats (list of str)
  - total_price (float)

- booking (dict):
  - booking_id (int)
  - showtime_id (int)
  - customer_name (str)
  - customer_email (str)
  - booking_date (str)
  - total_price (float)
  - status (str)
  - seats_booked (list of str)

- bookings (list of dict):
  - booking_id (int)
  - movie_title (str)
  - booking_date (str)
  - seats (list of str)
  - status (str)

- filtered_status (str): one of All, Confirmed, Cancelled, Completed

- selected_genre (str): genre filter string, or empty/None if no filter
- search_query (str): search input string, or empty if none
- selected_theater (str): theater filter string or empty
- selected_date (str): date filter string or empty
- selected_location (str): theater location filter string or empty

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title (in <title> and <h1>): "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (div): main container
  - featured-movies (div): section for featured movie recommendations
  - browse-movies-button (button): navigates to movie_catalog
  - view-bookings-button (button): navigates to booking_history
  - showtimes-button (button): navigates to showtime_selection (no default movie; should prompt user in UI to select movie first or disable)
- Navigation Mapping:
  - browse-movies-button: url_for('movie_catalog')
  - view-bookings-button: url_for('booking_history')
  - showtimes-button: url_for('showtime_selection', movie_id=some_default_or_prompt)

---

### 2. templates/movie_catalog.html
- Page Title: "Movie Catalog"
- Element IDs:
  - catalog-page (div): container
  - search-input (input): movie title or genre search
  - genre-filter (dropdown select): options include genres from context variable
  - movies-grid (div): displays movies in grid layout
  - view-movie-button-{movie_id} (button): each movie has a button to view details
- Navigation Mapping:
  - view-movie-button-{movie_id}: url_for('movie_details', movie_id=movie_id)

---

### 3. templates/movie_details.html
- Page Title: "Movie Details"
- Element IDs:
  - movie-details-page (div): container
  - movie-title (h1): displays movie title
  - movie-director (div): displays director
  - movie-rating (div): displays rating
  - movie-description (div): displays movie description
  - select-showtime-button (button): navigates to showtime_selection
- Navigation Mapping:
  - select-showtime-button: url_for('showtime_selection', movie_id=movie.movie_id)

---

### 4. templates/showtime_selection.html
- Page Title: "Select Showtime"
- Element IDs:
  - showtime-page (div): main container
  - showtimes-list (div): list of showtime entries
  - theater-filter (dropdown select): filter by theater
  - date-filter (input, type=date): filter by date
  - select-showtime-button-{showtime_id} (button): select specific showtime
- Navigation Mapping:
  - select-showtime-button-{showtime_id}: url_for('seat_selection', showtime_id=showtime_id)

---

### 5. templates/seat_selection.html
- Page Title: "Select Seats"
- Element IDs:
  - seat-selection-page (div): container
  - seat-map (div): interactive seat map
  - selected-seats-display (div): display of selected seat labels
  - seat-{row}{col} (button): seat buttons, example seat-A1, seat-B3
  - proceed-booking-button (button): proceeds to booking_confirmation
- Navigation Mapping:
  - proceed-booking-button: url_for('booking_confirmation')

---

### 6. templates/booking_confirmation.html
- Page Title: "Booking Confirmation"
- Element IDs:
  - confirmation-page (div): container
  - booking-summary (div): displays movie, showtime, seats, total price
  - customer-name (input): text input for customer name
  - customer-email (input): text input for customer email
  - confirm-booking-button (button): confirms and completes booking
- Navigation Mapping:
  - confirm-booking-button: form POST to url_for('booking_confirmation')

---

### 7. templates/booking_history.html
- Page Title: "Booking History"
- Element IDs:
  - bookings-page (div): container
  - bookings-table (table): shows booking id, movie, date, seats, status
  - view-booking-button-{booking_id} (button): view details of booking
  - status-filter (dropdown select): filter bookings by status
  - back-to-dashboard (button): navigate back to dashboard
- Navigation Mapping:
  - view-booking-button-{booking_id}: url_for('booking_details', booking_id=booking_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. templates/theater_information.html
- Page Title: "Theater Information"
- Element IDs:
  - theater-page (div): container
  - theaters-list (div): list of theaters
  - theater-location-filter (dropdown select): filter theaters by location
  - facilities-display (div): shows selected theater facilities
  - back-to-dashboard (button): navigate back to dashboard
- Navigation Mapping:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

1. Filename: data/movies.txt
- Fields (pipe-delimited): movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores all movie details including rating and release info.
- Examples:
  - 1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  - 2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  - 3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

2. Filename: data/theaters.txt
- Fields (pipe-delimited): theater_id|theater_name|location|city|screens|facilities
- Description: Stores theaters information including location and amenities.
- Examples:
  - 1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  - 2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  - 3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

3. Filename: data/showtimes.txt
- Fields (pipe-delimited): showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtimes for movies in various theaters.
- Examples:
  - 1|1|1|2025-02-01|19:00|12.99|85
  - 2|1|1|2025-02-01|22:30|12.99|40
  - 3|2|2|2025-02-01|18:00|14.99|95

4. Filename: data/seats.txt
- Fields (pipe-delimited): seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seat layouts and status for theaters/screens.
- Examples:
  - 1|1|1|A|1|Standard|Available
  - 2|1|1|A|2|Standard|Available
  - 3|1|1|B|5|Premium|Booked

5. Filename: data/bookings.txt
- Fields (pipe-delimited): booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores user bookings and booking details.
- Examples:
  - 1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  - 2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  - 3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

6. Filename: data/genres.txt
- Fields (pipe-delimited): genre_id|genre_name|description
- Description: Stores all genres available.
- Examples:
  - 1|Action|Fast-paced movies with exciting sequences and combat
  - 2|Drama|Character-driven stories exploring complex themes
  - 3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This design specification document comprehensively defines all routes, templates, and data files to allow parallel and independent work by backend and frontend teams without further communication. All identifiers, routes, and context variables are aligned consistently to facilitate seamless integration.
