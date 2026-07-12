from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Utility functions to load and save data files
DATA_DIR = 'data'


def load_movies():
    movies = []
    filepath = os.path.join(DATA_DIR, 'movies.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                movies.append({
                    'movie_id': int(parts[0]),
                    'title': parts[1],
                    'director': parts[2],
                    'genre': parts[3],
                    'rating': float(parts[4]),
                    'duration': int(parts[5]),
                    'description': parts[6],
                    'release_date': parts[7]
                })
    except Exception as e:
        print(f"Error loading movies: {e}")
    return movies


def load_theaters():
    theaters = []
    filepath = os.path.join(DATA_DIR, 'theaters.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                theaters.append({
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': int(parts[4]),
                    'facilities': parts[5]
                })
    except Exception as e:
        print(f"Error loading theaters: {e}")
    return theaters


def load_showtimes():
    showtimes = []
    filepath = os.path.join(DATA_DIR, 'showtimes.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                showtimes.append({
                    'showtime_id': int(parts[0]),
                    'movie_id': int(parts[1]),
                    'theater_id': int(parts[2]),
                    'showtime_date': parts[3],
                    'showtime_time': parts[4],
                    'price': float(parts[5]),
                    'available_seats': int(parts[6])
                })
    except Exception as e:
        print(f"Error loading showtimes: {e}")
    return showtimes


def load_seats():
    seats = []
    filepath = os.path.join(DATA_DIR, 'seats.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                seats.append({
                    'seat_id': int(parts[0]),
                    'theater_id': int(parts[1]),
                    'screen_id': int(parts[2]),
                    'row': parts[3],
                    'column': int(parts[4]),
                    'seat_type': parts[5],
                    'status': parts[6]
                })
    except Exception as e:
        print(f"Error loading seats: {e}")
    return seats


def load_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                seats_booked_list = parts[7].split(',') if parts[7].strip() else []
                bookings.append({
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': seats_booked_list
                })
    except Exception as e:
        print(f"Error loading bookings: {e}")
    return bookings


def load_genres():
    genres = []
    filepath = os.path.join(DATA_DIR, 'genres.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                genres.append({
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                })
    except Exception as e:
        print(f"Error loading genres: {e}")
    return genres


def save_bookings(bookings):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats_booked'])
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving bookings: {e}")


def save_seats(seats):
    filepath = os.path.join(DATA_DIR, 'seats.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for s in seats:
                line = f"{s['seat_id']}|{s['theater_id']}|{s['screen_id']}|{s['row']}|{s['column']}|{s['seat_type']}|{s['status']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving seats: {e}")


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Choose featured_movies (e.g. top rated 3) and upcoming_releases (release_date in future sorted ascending)
    today = datetime.date.today().isoformat()
    # featured_movies - select top 3 by rating (descending)
    sorted_by_rating = sorted(movies, key=lambda x: x['rating'], reverse=True)
    featured_movies = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'poster': '',  # No poster path from data schema, keep empty
            'rating': m['rating']
        } for m in sorted_by_rating[:3]
    ]

    # upcoming_releases - from movies with release_date > today, sorted soonest first
    upcoming = [m for m in movies if m['release_date'] > today]
    upcoming_sorted = sorted(upcoming, key=lambda x: x['release_date'])
    upcoming_releases = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'release_date': m['release_date']
        } for m in upcoming_sorted
    ]
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    # movies list with required fields:
    # movie_id:int, title:str, genre:str, rating:float, duration:int, poster:str
    # poster field is empty string as no poster in data
    movie_list = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster': ''
        } for m in movies
    ]
    return render_template('catalog.html', movies=movie_list)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    showtimes_all = load_showtimes()
    theaters = load_theaters()
    # Filter showtimes for movie_id
    showtimes_filtered = [s for s in showtimes_all if s['movie_id'] == movie_id]

    # Construct context lists
    showtimes_context = [
        {
            'showtime_id': s['showtime_id'],
            'movie_id': s['movie_id'],
            'theater_id': s['theater_id'],
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        } for s in showtimes_filtered
    ]

    theaters_context = [
        {
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name']
        } for t in theaters
    ]

    # Get movie title for context
    movies = load_movies()
    movie_obj = next((m for m in movies if m['movie_id'] == movie_id), None)
    movie_title = movie_obj['title'] if movie_obj else ''

    return render_template('showtime.html', showtimes=showtimes_context, theaters=theaters_context, movie_title=movie_title)


@app.route('/select_seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime_obj = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime_obj is None:
        return "Showtime not found", 404

    theaters = load_theaters()
    seats = load_seats()

    # Find theater_id from showtime
    theater_id = showtime_obj['theater_id']

    # Filter seats by theater_id and (optionally screen_id if we had it for showtime - but not provided)
    # Since showtime schema does not have screen_id, but seats.txt has screen_id, we do the best guess by theater_id
    # We'll show all seats in that theater - note this is per specification (no screen info available)
    seats_filtered = [
        {
            'seat_id': seat['seat_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat['status']
        }
        for seat in seats if seat['theater_id'] == theater_id
    ]

    return render_template('seat_selection.html', seat_map=seats_filtered, selected_showtime=showtime_obj)


@app.route('/confirm_booking/<int:showtime_id>', methods=['GET', 'POST'])
def confirm_booking(showtime_id):
    if request.method == 'GET':
        # Show booking confirmation page
        showtimes = load_showtimes()
        showtime_obj = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if showtime_obj is None:
            return "Showtime not found", 404

        movies = load_movies()
        theaters = load_theaters()

        movie_obj = next((m for m in movies if m['movie_id'] == showtime_obj['movie_id']), None)
        theater_obj = next((t for t in theaters if t['theater_id'] == showtime_obj['theater_id']), None)

        seats_selected = request.args.get('seats_selected', '')
        seats_selected_list = seats_selected.split(',') if seats_selected else []

        # Calculate total price
        total_price = showtime_obj['price'] * len(seats_selected_list) if seats_selected_list else 0.0

        booking_summary = {
            'movie_title': movie_obj['title'] if movie_obj else '',
            'showtime_date': showtime_obj['showtime_date'],
            'showtime_time': showtime_obj['showtime_time'],
            'theater_name': theater_obj['theater_name'] if theater_obj else '',
            'seats_selected': seats_selected_list,
            'total_price': total_price
        }

        return render_template('confirmation.html', booking_summary=booking_summary)

    else:
        # Handle booking confirmation POST
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        seats_selected_str = request.form.get('seats_selected', '').strip()
        seats_selected = seats_selected_str.split(',') if seats_selected_str else []

        # Validate input
        if not customer_name or not customer_email or not seats_selected:
            # Re-render confirmation page with error message or redirect
            # For spec: redirect to confirmation page (GET) again
            return redirect(url_for('confirm_booking', showtime_id=showtime_id))

        # Load all data
        bookings = load_bookings()
        seats = load_seats()
        showtimes = load_showtimes()

        showtime_obj = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if showtime_obj is None:
            return "Showtime not found", 404

        # Check if requested seats are available
        theater_id = showtime_obj['theater_id']
        unavailable_seats = []
        for seat_label in seats_selected:
            # Usually seat label is Row + Column, e.g. A1
            row = seat_label[0]
            col_part = seat_label[1:]
            try:
                col = int(col_part)
            except:
                col = None
            seat_match = next((seat for seat in seats if seat['theater_id'] == theater_id and seat['row'] == row and seat['column'] == col), None)
            if seat_match is None or seat_match['status'] != 'Available':
                unavailable_seats.append(seat_label)

        if unavailable_seats:
            # Some seats are not available, redirect back to select seats
            return redirect(url_for('seat_selection', showtime_id=showtime_id))

        # Mark seats as Booked
        for seat_label in seats_selected:
            row = seat_label[0]
            col = int(seat_label[1:])
            for seat in seats:
                if seat['theater_id'] == theater_id and seat['row'] == row and seat['column'] == col:
                    seat['status'] = 'Booked'
                    break

        # Update available_seats count in showtimes
        showtime_index = next((i for i, s in enumerate(showtimes) if s['showtime_id'] == showtime_id), None)
        if showtime_index is not None:
            showtimes[showtime_index]['available_seats'] -= len(seats_selected)
            if showtimes[showtime_index]['available_seats'] < 0:
                showtimes[showtime_index]['available_seats'] = 0

        # Add new booking
        max_booking_id = max([b['booking_id'] for b in bookings], default=0)
        booking_date = datetime.date.today().isoformat()
        total_price = showtime_obj['price'] * len(seats_selected)

        new_booking = {
            'booking_id': max_booking_id + 1,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected
        }

        bookings.append(new_booking)

        # Save updates
        save_bookings(bookings)
        save_seats(seats)

        return redirect(url_for('booking_history'))


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()

    status_filter = request.args.get('status', 'All')

    # Filter bookings by status if specified and not 'All'
    if status_filter != 'All':
        bookings = [b for b in bookings if b['status'] == status_filter]

    # Construct booking dicts with keys:
    # booking_id:int, movie_title:str, booking_date:str, seats_booked (list of str), status:str
    bookings_context = []
    for b in bookings:
        movie_obj = next((m for m in movies if m['movie_id'] == load_showtimes()[[s['showtime_id'] for s in load_showtimes()].index(b['showtime_id'])]['movie_id']), None) if b['showtime_id'] in [s['showtime_id'] for s in load_showtimes()] else None
        movie_title = movie_obj['title'] if movie_obj else ''
        bookings_context.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status']
        })

    return render_template('bookings.html', bookings=bookings_context)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking is None:
        return "Booking not found", 404

    showtimes = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()

    showtime_obj = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    movie_obj = None
    if showtime_obj:
        movie_obj = next((m for m in movies if m['movie_id'] == showtime_obj['movie_id']), None)

    booking_context = booking.copy()
    movie_title = movie_obj['title'] if movie_obj else ''

    return render_template('booking_details.html', booking=booking_context, movie_title=movie_title)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()

    location_filter = request.args.get('location', None)
    if location_filter:
        theaters_filtered = [t for t in theaters if t['location'] == location_filter]
    else:
        theaters_filtered = theaters

    return render_template('theater.html', theaters=theaters_filtered)


if __name__ == '__main__':
    app.run()  
