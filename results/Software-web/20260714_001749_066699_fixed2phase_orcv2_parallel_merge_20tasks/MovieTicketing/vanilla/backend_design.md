# Backend Design for MovieTicketing Web Application

---

## Section 1: Flask Routes and Backend Operations

### 1. Dashboard Page
- **Route Path:** `/dashboard`
- **HTTP Method:** GET
- **Functionality:** Render the dashboard page showing featured movies, upcoming releases, and navigation buttons.
- **Backend Operations:**
  - Read `movies.txt` to extract featured movies (e.g., movies with recent release_date or a special flag if implemented).
  - Pass featured movies data to render template.

---

### 2. Movie Catalog Page
- **Route Path:** `/movies`
- **HTTP Method:** GET
- **Query Params:** `search` (optional), `genre` (optional)
- **Functionality:** Return filtered list of all movies.
- **Backend Operations:**
  - Read `movies.txt`.
  - Filter movies by search term (match title or genre case-insensitive).
  - Filter movies by genre if provided.
  - Return JSON list or render template with movie objects containing movie_id, title, genre, rating, duration.

---

### 3. Movie Details Page
- **Route Path:** `/movie/<int:movie_id>`
- **HTTP Method:** GET
- **Functionality:** Return detailed information for a specific movie.
- **Backend Operations:**
  - Read `movies.txt`.
  - Find movie by movie_id.
  - Return or render movie details including title, director, genre, rating, duration, description, and release_date.

---

### 4. Showtime Selection Page
- **Route Path:** `/showtimes/<int:movie_id>`
- **HTTP Method:** GET
- **Query Params:** `theater_id` (optional), `date` (optional)
- **Functionality:** Show available showtimes for given movie filtered by theater and/or date.
- **Backend Operations:**
  - Read `showtimes.txt`.
  - Filter by movie_id.
  - If `theater_id` is provided, filter by theater_id.
  - If `date` is provided, filter by showtime_date.
  - Read `theaters.txt` to provide theater names in response.
  - Return list of showtimes with showtime_id, movie_id, theater_name, showtime_date, showtime_time, price, available_seats.

---

### 5. Seat Selection Page
- **Route Path:** `/seats/<int:showtime_id>`
- **HTTP Method:** GET
- **Functionality:** Return seat availability and seat map data for the theater and screen associated with the showtime.
- **Backend Operations:**
  - Read `showtimes.txt` to get theater_id for showtime_id.
  - Identify `screen_id` for the theater (assuming screen_id can be inferred or defaulted from seats.txt) - since seats.txt contains screen_id, use that.
  - Read `seats.txt` filtered by theater_id and screen_id to get all seats.
  - Read `bookings.txt` for current showtime_id to mark seats booked.
  - Construct seat map showing seat_id, row, column, seat_type, and current status (Available/Booked).
  - Return seat map data.

---

### 6. Booking Confirmation Page
- **Route Path:** `/bookings/confirm`
- **HTTP Method:** POST
- **Input JSON Payload:**
  ```json
  {
    "showtime_id": int,
    "customer_name": string,
    "customer_email": string,
    "seats": [string, ...]  // seat labels like A1, B10
  }
  ```
- **Functionality:** Create a booking for selected seats.
- **Backend Operations:**
  - Verify seat availability by cross-checking seats from `bookings.txt` for showtime_id.
  - Calculate total price = price from `showtimes.txt` * number of seats.
  - Generate new booking_id (auto-increment based on last booking_id in `bookings.txt`).
  - Append new booking record to `bookings.txt` with status `Confirmed` and seats_booked as comma-separated list.
  - Update `showtimes.txt` to decrement `available_seats` by number of seats booked.
  - Return booking confirmation details including booking_id and summary.

---

### 7. Booking History Page
- **Route Path:** `/bookings`
- **HTTP Method:** GET
- **Query Params:** `status` (optional, values: All, Confirmed, Cancelled, Completed)
- **Functionality:** Display all past bookings, filtered by status.
- **Backend Operations:**
  - Read `bookings.txt`.
  - Filter by status if provided (else show all).
  - For each booking, read corresponding movie title and showtime date/time from `showtimes.txt` and `movies.txt`.
  - Return or render list of bookings with booking_id, movie title, showtime date, seats_booked, status.

---

### 8. Theater Information Page
- **Route Path:** `/theaters`
- **HTTP Method:** GET
- **Query Params:** `location` (optional)
- **Functionality:** Display theaters information filtered by location.
- **Backend Operations:**
  - Read `theaters.txt`.
  - Filter theaters by city/location if query param provided.
  - Return theater details including theater_id, theater_name, location, city, screens, facilities.

---

## Section 2: Data File Formats and Business Logic Contracts

### 1. Movies Data: `movies.txt`
- **Schema:** 
  ```
  movie_id (int) | title (str) | director (str) | genre (str) | rating (float) | duration (int, minutes) | description (str) | release_date (YYYY-MM-DD)
  ```
- **Example:**
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality.|1999-03-31
  ```
- **Constraints:** 
  - movie_id unique and monotonically increasing
  - rating 0.0 - 10.0
  - duration positive integer
  - release_date format YYYY-MM-DD

### 2. Theaters Data: `theaters.txt`
- **Schema:**
  ```
  theater_id (int) | theater_name (str) | location (str) | city (str) | screens (int) | facilities (str, CSV)
  ```
- **Example:**
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  ```
- **Constraints:**
  - theater_id unique
  - screens positive integer
  - facilities comma-separated string

### 3. Showtimes Data: `showtimes.txt`
- **Schema:**
  ```
  showtime_id (int) | movie_id (int) | theater_id (int) | showtime_date (YYYY-MM-DD) | showtime_time (HH:MM) | price (float) | available_seats (int)
  ```
- **Example:**
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  ```
- **Constraints:**
  - showtime_id unique
  - available_seats non-negative
  - showtime_date & time valid formats

### 4. Seats Data: `seats.txt`
- **Schema:**
  ```
  seat_id (int) | theater_id (int) | screen_id (int) | row (str) | column (int) | seat_type (str) | status (str: Available or Booked)
  ```
- **Example:**
  ```
  1|1|1|A|1|Standard|Available
  ```
- **Constraints:**
  - seat_id unique
  - status only "Available" or "Booked" representing seat default state (note: actual booked state for showtime derived from bookings data)

### 5. Bookings Data: `bookings.txt`
- **Schema:**
  ```
  booking_id (int) | showtime_id (int) | customer_name (str) | customer_email (str) | booking_date (YYYY-MM-DD) | total_price (float) | status (str: Confirmed, Cancelled, Completed) | seats_booked (CSV of seat labels like A1,A2)
  ```
- **Example:**
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  ```
- **Constraints:**
  - booking_id unique
  - status limited to given values
  - seats_booked matches seats in seats.txt for corresponding theater and screen

### 6. Genres Data: `genres.txt`
- **Schema:**
  ```
  genre_id (int) | genre_name (str) | description (str)
  ```
- **Example:**
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  ```
- **Constraints:**
  - genre_id unique

---

## Backend Logic and Business Rules

- Seat availability is dynamically calculated by comparing seats.txt (static seat map) and bookings.txt entries (seats booked for a specific showtime).
- Booking creation involves:
  1. Validating requested seats are all available for the given showtime.
  2. Calculating total price based on showtime price and seat count.
  3. Assigning new unique booking_id.
  4. Appending booking to bookings.txt.
  5. Reducing available_seats in showtimes.txt accordingly.
- No user authentication or session management is required.
- Date and time inputs and outputs must comply with ISO formats.

---

This design blueprint provides a comprehensive layout for Flask route implementation and local file data management to realize the MovieTicketing application functionalities as specified in the user requirements.