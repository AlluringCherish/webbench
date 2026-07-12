# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                   | Function Name            | HTTP Method(s) | Template Rendered           | Context Variables (with Types and Structures)                                             |
|------------------------------|--------------------------|----------------|-----------------------------|-------------------------------------------------------------------------------------------|
| /                            | root_redirect             | GET            | Redirects to /dashboard       | None                                                                                      |
| /dashboard                   | dashboard                | GET            | dashboard.html              | featured_movies (list of dict: movie_id[int], title[str], genre[str], rating[float])       |
| /movies                     | movie_catalog            | GET            | movie_catalog.html          | movies (list of dict: movie_id[int], title[str], genre[str], rating[float], duration[int]) |
| /movies/search               | movie_search             | POST           | movie_catalog.html          | movies (list of dict like above, filtered)                                               |
| /movies/<int:movie_id>       | movie_details            | GET            | movie_details.html          | movie (dict: movie_id[int], title[str], director[str], genre[str], rating[float], duration[int], description[str], release_date[str]) |
| /showtimes/<int:movie_id>    | select_showtime          | GET            | select_showtime.html        | showtimes (list of dict: showtime_id[int], movie_id[int], theater_id[int], showtime_date[str], showtime_time[str], price[float]),
|                              |                          |                |                             | theaters (list of dict: theater_id[int], theater_name[str], location[str], city[str])       |
| /bookings/showtime/<int:showtime_id>/seats | select_seats  | GET            | seat_selection.html         | seat_map (list of dict: seat_id[int], theater_id[int], screen_id[int], row[str], column[int], seat_type[str], status[str]), available_seats[int] |
| /bookings/select             | booking_confirmation     | POST           | booking_confirmation.html   | booking_summary (dict: movie_title[str], showtime_date[str], showtime_time[str], theater_name[str], seats_selected[list of str], total_price[float]) |
| /bookings/history            | booking_history          | GET            | booking_history.html        | bookings (list of dict: booking_id[int], showtime_id[int], customer_name[str], booking_date[str], total_price[float], status[str], seats_booked[list of str]), filter_options (list[str]) |
| /bookings/<int:booking_id>   | view_booking             | GET            | booking_details.html        | booking_detail (dict: booking_id[int], showtime_id[int], movie_title[str], customer_name[str], customer_email[str], booking_date[str], total_price[float], status[str], seats_booked[list of str]]) |
| /theaters                   | theater_information      | GET            | theater_information.html    | theaters(list of dict: theater_id[int], theater_name[str], location[str], city[str], screens[int], facilities[str]) |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title>, <h1>: Movie Ticketing Dashboard
- Element IDs:
  - dashboard-page (div, container for dashboard)
  - featured-movies (div, display featured movies)
  - browse-movies-button (button, navigates to movie_catalog)
  - view-bookings-button (button, navigates to booking_history)
  - showtimes-button (button, navigates to select_showtime root or showtimes page)
- Navigation:
  - browse-movies-button: url_for('movie_catalog')
  - view-bookings-button: url_for('booking_history')
  - showtimes-button: url_for('select_showtime', movie_id=some_default_or_first_movie_id)

### 2. Movie Catalog Page
- Filename: templates/movie_catalog.html
- Page Title: Movie Catalog
- <title>, <h1>: Movie Catalog
- Element IDs:
  - catalog-page (div, container for catalog page)
  - search-input (input, search movies by title or genre)
  - genre-filter (dropdown, filter movies by genre)
  - movies-grid (div, grid showing movie cards)
  - view-movie-button-{movie_id} (button per movie card, navigates to movie_details)
- Navigation:
  - view-movie-button-{movie_id}: url_for('movie_details', movie_id=movie_id)

### 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <title>, <h1>: Movie Details
- Element IDs:
  - movie-details-page (div, container)
  - movie-title (h1, displays title)
  - movie-director (div, displays director)
  - movie-rating (div, displays rating)
  - movie-description (div, displays description)
  - select-showtime-button (button, navigates to select_showtime for given movie)
- Navigation:
  - select-showtime-button: url_for('select_showtime', movie_id=movie_id)

### 4. Showtime Selection Page
- Filename: templates/select_showtime.html
- Page Title: Select Showtime
- <title>, <h1>: Select Showtime
- Element IDs:
  - showtime-page (div, container)
  - showtimes-list (div, list of showtimes)
  - theater-filter (dropdown, filter by theater)
  - date-filter (input, filter by date)
  - select-showtime-button-{showtime_id} (button per showtime, navigates to select_seats)
- Navigation:
  - select-showtime-button-{showtime_id}: url_for('select_seats', showtime_id=showtime_id)

### 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <title>, <h1>: Select Seats
- Element IDs:
  - seat-selection-page (div, container)
  - seat-map (div, interactive seat buttons)
  - selected-seats-display (div, shows currently selected seats)
  - seat-{row}{col} (button, each seat, e.g., seat-A1, seat-B3)
  - proceed-booking-button (button, proceeds to booking_confirmation)
- Navigation:
  - proceed-booking-button: url_for('booking_confirmation')

### 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <title>, <h1>: Booking Confirmation
- Element IDs:
  - confirmation-page (div, container)
  - booking-summary (div, shows booking details: movie, showtime, seats, total)
  - customer-name (input, input customer name)
  - customer-email (input, input customer email)
  - confirm-booking-button (button, submits booking)
- Navigation:
  - confirm-booking-button: POST action to url_for('booking_confirmation')

### 7. Booking History Page
- Filename: templates/booking_history.html
- Page Title: Booking History
- <title>, <h1>: Booking History
- Element IDs:
  - bookings-page (div, container)
  - bookings-table (table, list bookings)
  - view-booking-button-{booking_id} (button per booking, view details)
  - status-filter (dropdown, filter by status)
  - back-to-dashboard (button, returns to dashboard)
- Navigation:
  - view-booking-button-{booking_id}: url_for('view_booking', booking_id=booking_id)
  - back-to-dashboard: url_for('dashboard')

### 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <title>, <h1>: Theater Information
- Element IDs:
  - theater-page (div, container)
  - theaters-list (div, list theaters)
  - theater-location-filter (dropdown, filter by location)
  - facilities-display (div, shows facilities of selected theater)
  - back-to-dashboard (button, returns to dashboard)
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

### Movies Data
- Filename: data/movies.txt
- Fields Order: movie_id|title|director|genre|rating|duration|description|release_date
- Description: Contains movie details including identifiers, descriptions, and release data.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### Theaters Data
- Filename: data/theaters.txt
- Fields Order: theater_id|theater_name|location|city|screens|facilities
- Description: Lists theaters with location, screens, and amenities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### Showtimes Data
- Filename: data/showtimes.txt
- Fields Order: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtimes for movies in theaters with pricing and seat availability.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### Seats Data
- Filename: data/seats.txt
- Fields Order: seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat specifications and current booking status.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### Bookings Data
- Filename: data/bookings.txt
- Fields Order: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Booking records including customer info, seats, and statuses.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### Genres Data
- Filename: data/genres.txt
- Fields Order: genre_id|genre_name|description
- Description: Genre categories with descriptions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

