# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name           | HTTP Method | Template Rendered          | Context Variables (name:type)                                 |
|--------------------------------|------------------------|-------------|----------------------------|--------------------------------------------------------------|
| /                              | root_redirect           | GET         | redirects to /dashboard    | none                                                         |
| /dashboard                     | dashboard              | GET         | dashboard.html             | featured_movies:list[dict{movie_id:int, title:str}]           |
| /movies                       | movie_catalog          | GET         | movie_catalog.html         | movies:list[dict{movie_id:int, title:str, genre:str, rating:float, duration:int}] |
| /movies/search                | movie_search           | POST        | movie_catalog.html         | movies:list[dict{movie_id:int, title:str, genre:str, rating:float, duration:int}] |
| /movies/<int:movie_id>         | movie_details          | GET         | movie_details.html         | movie:dict{movie_id:int, title:str, director:str, rating:float, description:str} |
| /showtimes/<int:movie_id>      | showtime_selection     | GET         | showtime_selection.html    | showtimes:list[dict{showtime_id:int, date:str, time:str, theater:str, price:float}] |
| /showtimes/filter              | showtime_filter         | POST        | showtime_selection.html    | showtimes:list[dict{showtime_id:int, date:str, time:str, theater:str, price:float}] |
| /seats/<int:showtime_id>       | seat_selection         | GET         | seat_selection.html        | seat_map:list[dict{seat_id:int, row:str, column:int, seat_type:str, status:str}], selected_seats:list[str] |
| /booking/confirm               | booking_confirmation   | GET         | booking_confirmation.html  | booking_summary:dict{movie:str, showtime:str, seats:list[str], total:float}       |
| /booking/complete              | booking_complete       | POST        | booking_confirmation.html  | booking_status:str                                            |
| /bookings                     | booking_history        | GET         | booking_history.html       | bookings:list[dict{booking_id:int, movie:str, date:str, seats:list[str], status:str}]|
| /bookings/<int:booking_id>     | booking_details        | GET         | booking_history.html       | booking:dict{booking_id:int, movie:str, date:str, seats:list[str], status:str}    |
| /theaters                     | theater_info           | GET         | theater_info.html          | theaters:list[dict{theater_id:int, theater_name:str, location:str, screens:int, facilities:str}] |

Notes:
- Root route '/' does an HTTP redirect to '/dashboard'.
- POST routes for search and filter to support form submissions.

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <h1>: id="dashboard-header"
- Container: id="dashboard-page" (div)
- Elements:
  - id="featured-movies" (div): displays featured movie recommendations
  - id="browse-movies-button" (button): navigates to movie_catalog
  - id="view-bookings-button" (button): navigates to booking_history
  - id="showtimes-button" (button): navigates to showtime_selection root or general

Navigation:
- "browse-movies-button" -> url_for('movie_catalog')
- "view-bookings-button" -> url_for('booking_history')
- "showtimes-button" -> url_for('showtime_selection') (if no movie, or to general showtimes)

### templates/movie_catalog.html
- Page Title: Movie Catalog
- <h1>: id="catalog-header"
- Container: id="catalog-page" (div)
- Elements:
  - id="search-input" (input): search by title or genre
  - id="genre-filter" (dropdown/select): filter by genre
  - id="movies-grid" (div): grid displaying movie cards
  - Buttons:
    - id pattern: "view-movie-button-{movie_id}" (button): view movie details

Navigation:
- Each "view-movie-button-{movie_id}" -> url_for('movie_details', movie_id=movie_id)

### templates/movie_details.html
- Page Title: Movie Details
- <h1>: id="movie-title"
- Container: id="movie-details-page" (div)
- Elements:
  - id="movie-director" (div): display director
  - id="movie-rating" (div): display rating
  - id="movie-description" (div): display description
  - id="select-showtime-button" (button): proceed to showtime_selection for movie

Navigation:
- "select-showtime-button" -> url_for('showtime_selection', movie_id=movie_id)

### templates/showtime_selection.html
- Page Title: Select Showtime
- <h1>: id="showtime-header"
- Container: id="showtime-page" (div)
- Elements:
  - id="showtimes-list" (div): list of showtimes
  - id="theater-filter" (dropdown/select): filter by theater
  - id="date-filter" (input): filter by date
  - Buttons:
    - id pattern: "select-showtime-button-{showtime_id}" (button): select specific showtime

Navigation:
- Each "select-showtime-button-{showtime_id}" -> url_for('seat_selection', showtime_id=showtime_id)

### templates/seat_selection.html
- Page Title: Select Seats
- <h1>: id="seat-selection-header"
- Container: id="seat-selection-page" (div)
- Elements:
  - id="seat-map" (div): interactive seat map
  - Seats:
    - id pattern: "seat-{row}{col}" (button): individual seat button
  - id="selected-seats-display" (div): display selected seats
  - id="proceed-booking-button" (button): proceed to booking_confirmation

Navigation:
- "proceed-booking-button" -> url_for('booking_confirmation')

### templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <h1>: id="confirmation-header"
- Container: id="confirmation-page" (div)
- Elements:
  - id="booking-summary" (div): summary of booking details
  - id="customer-name" (input): input customer name
  - id="customer-email" (input): input customer email
  - id="confirm-booking-button" (button): confirm booking

Navigation:
- "confirm-booking-button" -> POST to url_for('booking_complete')

### templates/booking_history.html
- Page Title: Booking History
- <h1>: id="bookings-header"
- Container: id="bookings-page" (div)
- Elements:
  - id="bookings-table" (table): displaying booking records
  - Buttons:
    - id pattern: "view-booking-button-{booking_id}" (button): view booking details
  - id="status-filter" (dropdown/select): filter by status
  - id="back-to-dashboard" (button): back to dashboard

Navigation:
- Each "view-booking-button-{booking_id}" -> url_for('booking_details', booking_id=booking_id)
- "back-to-dashboard" -> url_for('dashboard')

### templates/theater_info.html
- Page Title: Theater Information
- <h1>: id="theater-header"
- Container: id="theater-page" (div)
- Elements:
  - id="theaters-list" (div): list of theaters
  - id="theater-location-filter" (dropdown/select): filter by location
  - id="facilities-display" (div): theater facilities display
  - id="back-to-dashboard" (button): back to dashboard

Navigation:
- "back-to-dashboard" -> url_for('dashboard')

---

## Section 3: Data File Schemas

| Filename (path)        | Fields (pipe-delimited order)                                                        | Description                                 | Example Rows                                                   |
|-----------------------|-------------------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------------------------|
| data/movies.txt       | movie_id|title|director|genre|rating|duration|description|release_date                   | Movie information                            |
|                       |                                                                                     |                                             | 1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31 |
|                       |                                                                                     |                                             | 2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16 |
|                       |                                                                                     |                                             | 3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23 |

| data/theaters.txt     | theater_id|theater_name|location|city|screens|facilities                                               | Theater information                          |
|                       |                                                                                     |                                             | 1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access                            |
|                       |                                                                                     |                                             | 2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking                                 |
|                       |                                                                                     |                                             | 3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge                    |

| data/showtimes.txt    | showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats                     | Showtime information                         |
|                       |                                                                                     |                                             | 1|1|1|2025-02-01|19:00|12.99|85                                              |
|                       |                                                                                     |                                             | 2|1|1|2025-02-01|22:30|12.99|40                                              |
|                       |                                                                                     |                                             | 3|2|2|2025-02-01|18:00|14.99|95                                              |

| data/seats.txt        | seat_id|theater_id|screen_id|row|column|seat_type|status                                            | Seat details                                 |
|                       |                                                                                     |                                             | 1|1|1|A|1|Standard|Available                                    |
|                       |                                                                                     |                                             | 2|1|1|A|2|Standard|Available                                    |
|                       |                                                                                     |                                             | 3|1|1|B|5|Premium|Booked                                      |

| data/bookings.txt     | booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked               | Booking records                              |
|                       |                                                                                     |                                             | 1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2                                   |
|                       |                                                                                     |                                             | 2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10                                      |
|                       |                                                                                     |                                             | 3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4                                   |

| data/genres.txt       | genre_id|genre_name|description                                                      | Genre definitions                            |
|                       |                                                                                     |                                             | 1|Action|Fast-paced movies with exciting sequences and combat        |
|                       |                                                                                     |                                             | 2|Drama|Character-driven stories exploring complex themes               |
|                       |                                                                                     |                                             | 3|Sci-Fi|Science fiction with futuristic technology and concepts      |

---

This specification document ensures backend and frontend teams can implement their components independently with full clarity.