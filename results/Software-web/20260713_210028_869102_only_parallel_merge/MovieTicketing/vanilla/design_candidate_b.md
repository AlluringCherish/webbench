# MovieTicketing Web Application Design Document

---

## Overview

This design document specifies the detailed implementation plan for the MovieTicketing web application developed in Python, emphasizing local text file data handling and precise UI/UX design. The application features eight main pages with defined routes, UI element identifiers, navigation flows, and data file management details.

The starting point for all users is the Dashboard page.

---

# 1. Route and Page Definitions

| Page Name             | Route Path                  | HTTP Method | Page Title                  |
|-----------------------|-----------------------------|-------------|-----------------------------|
| Dashboard             | `/dashboard`                 | GET         | Movie Ticketing Dashboard    |
| Movie Catalog         | `/movies`                   | GET         | Movie Catalog                |
| Movie Details         | `/movies/<movie_id>`        | GET         | Movie Details                |
| Showtime Selection    | `/showtimes/select`          | GET         | Select Showtime             |
| Seat Selection        | `/seats/select`              | GET         | Select Seats                |
| Booking Confirmation  | `/booking/confirm`           | GET         | Booking Confirmation        |
| Booking History       | `/bookings`                  | GET         | Booking History              |
| Theater Information   | `/theaters`                  | GET         | Theater Information          |

## Notes on Parameters
- `<movie_id>`, `<showtime_id>`, and `<booking_id>` are dynamic path variables referencing respective entities.

---

# 2. UI Element Details per Page

---

## 2.1 Dashboard Page
- **Route:** `/dashboard` (GET)
- **Page Title:** Movie Ticketing Dashboard
- **Elements:**
  - `dashboard-page` (Div): Main container for the dashboard.
  - `featured-movies` (Div): Displays recommended movies.
  - `browse-movies-button` (Button): Navigates to Movie Catalog page.
  - `view-bookings-button` (Button): Navigates to Booking History page.
  - `showtimes-button` (Button): Navigates to Showtime Selection page.

---

## 2.2 Movie Catalog Page
- **Route:** `/movies` (GET)
- **Page Title:** Movie Catalog
- **Elements:**
  - `catalog-page` (Div): Main container of catalog.
  - `search-input` (Input): Text input for searching movies by title or genre.
  - `genre-filter` (Dropdown): Filter movies by genre.
  - `movies-grid` (Div): Grid layout containing movie cards.
  - `view-movie-button-{movie_id}` (Button): For each movie card, navigates to Movie Details page.

**Dynamic ID pattern:** `view-movie-button-{movie_id}` where `{movie_id}` is the unique ID of the movie.

---

## 2.3 Movie Details Page
- **Route:** `/movies/<movie_id>` (GET)
- **Page Title:** Movie Details
- **Elements:**
  - `movie-details-page` (Div): Container for detail page.
  - `movie-title` (H1): Shows movie title.
  - `movie-director` (Div): Displays director's name.
  - `movie-rating` (Div): Shows movie rating.
  - `movie-description` (Div): Detailed description.
  - `select-showtime-button` (Button): Navigates to Showtime Selection page with context to this movie.

---

## 2.4 Showtime Selection Page
- **Route:** `/showtimes/select` (GET)
- **Page Title:** Select Showtime
- **Elements:**
  - `showtime-page` (Div): Container.
  - `showtimes-list` (Div): List of showtimes with details (date, time, theater, price).
  - `theater-filter` (Dropdown): Filter showtimes by theater.
  - `date-filter` (Input): Filter showtimes by date.
  - `select-showtime-button-{showtime_id}` (Button): Selects specific showtime.

**Dynamic ID pattern:** `select-showtime-button-{showtime_id}` where `{showtime_id}` is the unique showtime identifier.

---

## 2.5 Seat Selection Page
- **Route:** `/seats/select` (GET)
- **Page Title:** Select Seats
- **Elements:**
  - `seat-selection-page` (Div): Container.
  - `seat-map` (Div): Interactive seat map showing seat availability.
  - `selected-seats-display` (Div): Displays currently selected seats.
  - `seat-{row}{col}` (Button): Buttons representing each seat, e.g., `seat-A1`, `seat-B3`.
  - `proceed-booking-button` (Button): Proceeds to Booking Confirmation page.

**Dynamic ID pattern:** `seat-{row}{col}` : row is a letter A-Z, col is number, e.g., `seat-C5`.

---

## 2.6 Booking Confirmation Page
- **Route:** `/booking/confirm` (GET)
- **Page Title:** Booking Confirmation
- **Elements:**
  - `confirmation-page` (Div): Container.
  - `booking-summary` (Div): Summary including movie, showtime, selected seats, and total cost.
  - `customer-name` (Input): Input for customer name.
  - `customer-email` (Input): Input for customer email.
  - `confirm-booking-button` (Button): Confirm and finalize booking.

---

## 2.7 Booking History Page
- **Route:** `/bookings` (GET)
- **Page Title:** Booking History
- **Elements:**
  - `bookings-page` (Div): Container.
  - `bookings-table` (Table): Shows bookings with columns: Booking ID, Movie, Date, Seats, Status.
  - `view-booking-button-{booking_id}` (Button): View details for given booking.
  - `status-filter` (Dropdown): Filter bookings by status (All, Confirmed, Cancelled, Completed).
  - `back-to-dashboard` (Button): Navigates back to Dashboard page.

**Dynamic ID pattern:** `view-booking-button-{booking_id}` where `{booking_id}` is the unique booking.

---

## 2.8 Theater Information Page
- **Route:** `/theaters` (GET)
- **Page Title:** Theater Information
- **Elements:**
  - `theater-page` (Div): Container.
  - `theaters-list` (Div): List of theaters with location, screens, and descriptions.
  - `theater-location-filter` (Dropdown): Filter theaters by location.
  - `facilities-display` (Div): Shows facilities of selected theater.
  - `back-to-dashboard` (Button): Returns to Dashboard.

---

# 3. Navigation Buttons and Flow

- From **Dashboard**:
  - `browse-movies-button` → `/movies`
  - `view-bookings-button` → `/bookings`
  - `showtimes-button` → `/showtimes/select`

- From **Movie Catalog**:
  - Each `view-movie-button-{movie_id}` → `/movies/<movie_id>`

- From **Movie Details**:
  - `select-showtime-button` → `/showtimes/select` (filtered for selected movie)

- From **Showtime Selection**:
  - Each `select-showtime-button-{showtime_id}` → `/seats/select` (for that showtime)

- From **Seat Selection**:
  - `proceed-booking-button` → `/booking/confirm`

- From **Booking History**:
  - Each `view-booking-button-{booking_id}` → detailed view (not explicitly defined in reqs)
  - `back-to-dashboard` → `/dashboard`

- From **Theater Information**:
  - `back-to-dashboard` → `/dashboard`

---

# 4. Data Files Usage and Formats

All data is stored in text files within a `data/` directory. Each page uses these files to load respective data for display or updates.

---

## 4.1 Movies Data (`movies.txt`)
- **Used by:** Movie Catalog, Movie Details
- **Format:** `movie_id|title|director|genre|rating|duration|description|release_date`
- **Purpose:** Load complete movie list, search/filter by genre or title, and show detailed info.

---

## 4.2 Theaters Data (`theaters.txt`)
- **Used by:** Showtime Selection (to display theater info), Theater Information
- **Format:** `theater_id|theater_name|location|city|screens|facilities`
- **Purpose:** Display theater names, locations, filter by location, and list facilities.

---

## 4.3 Showtimes Data (`showtimes.txt`)
- **Used by:** Showtime Selection, Booking Confirmation
- **Format:** `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- **Purpose:** List showtimes per movie and theater, show pricing and availability.

---

## 4.4 Seats Data (`seats.txt`)
- **Used by:** Seat Selection
- **Format:** `seat_id|theater_id|screen_id|row|column|seat_type|status`
- **Purpose:** Render interactive seat map showing available/booked seats. Status helps disable booked seats, and seat type can influence pricing.

---

## 4.5 Bookings Data (`bookings.txt`)
- **Used by:** Booking Confirmation (to save new booking), Booking History
- **Format:** `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- **Purpose:** Maintain booking records for history display, status filtering, and confirmation management.

---

## 4.6 Genres Data (`genres.txt`)
- **Used by:** Movie Catalog (for filtering via genre-dropdown)
- **Format:** `genre_id|genre_name|description`
- **Purpose:** Populate genre filter dropdown, provide descriptions if needed.

---

# Summary

This design establishes a clear, consistent specification for the MovieTicketing web app. It aligns routes, UI elements with precise IDs and behaviors, navigation between pages, and strict local text file data usage, ensuring a robust programming foundation and predictable user experience.

All UI element IDs and page titles match the exact naming provided in requirements.

---

End of Design Document
