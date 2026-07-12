from flask import Flask, render_template, redirect, url_for, request
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# File paths
MOVIES_FILE = 'data/movies.txt'
THEATERS_FILE = 'data/theaters.txt'
SHOWTIMES_FILE = 'data/showtimes.txt'
SEATS_FILE = 'data/seats.txt'
BOOKINGS_FILE = 'data/bookings.txt'
GENRES_FILE = 'data/genres.txt'


# Utility functions for file operations and data parsing

def load_movies():
    movies = []
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 8:
                    continue
                movie = {
                    'movie_id': int(row[0]),
                    'title': row[1],
                    'director': row[2],
                    'genre': row[3],
                    'rating': float(row[4]),
                    'duration': int(row[5]),
                    'description': row[6],
                    'release_date': row[7]
                }
                movies.append(movie)
    except Exception:
        pass
    return movies


def load_theaters():
    theaters = []
    try:
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 6:
                    continue
                theater = {
                    'theater_id': int(row[0]),
                    'theater_name': row[1],
                    'location': row[2],
                    'city': row[3],
                    'screens': int(row[4]),
                    'facilities': row[5]
                }
                theaters.append(theater)
    except Exception:
        pass
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 7:
                    continue
                showtime = {
                    'showtime_id': int(row[0]),
                    'movie_id': int(row[1]),
                    'theater_id': int(row[2]),
                    'showtime_date': row[3],
                    'showtime_time': row[4],
                    'price': float(row[5]),
                    'available_seats': int(row[6])
                }
                showtimes.append(showtime)
    except Exception:
        pass
    return showtimes


def load_seats():
    seats = []
    try:
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 7:
                    continue
                seat = {
                    'seat_id': int(row[0]),
                    'theater_id': int(row[1]),
                    'screen_id': int(row[2]),
                    'row': row[3],
                    'column': int(row[4]),
                    'seat_type': row[5],
                    'status': row[6]
                }
                seats.append(seat)
    except Exception:
        pass
    return seats


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 8:
                    continue
                booking = {
                    'booking_id': int(row[0]),
                    'showtime_id': int(row[1]),
                    'customer_name': row[2],
                    'customer_email': row[3],
                    'booking_date': row[4],
                    'total_price': float(row[5]),
                    'status': row[6],
                    'seats_booked': row[7].split(",") if row[7] else []
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for b in bookings:
                row = [
                    b['booking_id'],
                    b['showtime_id'],
                    b['customer_name'],
                    b['customer_email'],
                    b['booking_date'],
                    f"{b['total_price']:.2f}",
                    b['status'],
                    ",".join(b['seats_booked'])
                ]
                writer.writerow(row)
        return True
    except Exception:
        return False


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    movies = load_movies()
    # featured_movies: list of dict: movie_id, title, genre, rating, duration
    # For demo, consider top 5 rated movies as featured
    sorted_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)
    featured_movies = []
    for m in sorted_movies[:5]:
        featured_movies.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration']
        })

    # upcoming_releases: list of dict: movie_id, title, genre, release_date
    # movies with release_date > today
    today = datetime.now().date()
    upcoming = []
    for m in movies:
        try:
            rd = datetime.strptime(m['release_date'], '%Y-%m-%d').date()
            if rd > today:
                upcoming.append({
                    'movie_id': m['movie_id'],
                    'title': m['title'],
                    'genre': m['genre'],
                    'release_date': m['release_date']
                })
        except Exception:
            continue

    # sort upcoming by release_date ascending
    upcoming_releases = sorted(upcoming, key=lambda x: x['release_date'])

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    # movies (list of dict: movie_id, title, genre, rating, duration)
    movie_list = []
    for m in movies:
        movie_list.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration']
        })
    return render_template('movie_catalog.html', movies=movie_list)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = None
    for m in movies:
        if m['movie_id'] == movie_id:
            movie = m
            break
    if movie is None:
        # Not found, show 404 or empty page
        return render_template('movie_details.html', movie=None)

    # movie (dict with all fields as per schema)
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/select/<int:movie_id>')
def select_showtime(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()

    # Filter showtimes for the given movie_id
    filtered_showtimes = []
    theater_dict = {t['theater_id']: t['theater_name'] for t in theaters}

    for s in showtimes:
        if s['movie_id'] == movie_id:
            filtered_showtimes.append({
                'showtime_id': s['showtime_id'],
                'theater_id': s['theater_id'],
                'theater_name': theater_dict.get(s['theater_id'], 'Unknown Theater'),
                'showtime_date': s['showtime_date'],
                'showtime_time': s['showtime_time'],
                'price': s['price']
            })

    return render_template('showtime_selection.html', showtimes=filtered_showtimes, theaters=theaters)


@app.route('/showtimes/select/<int:showtime_id>/seats')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    seats = load_seats()
    movies = load_movies()

    # Find showtime info
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if not showtime:
        # showtime not found
        return render_template('seat_selection.html', seats=[], selected_showtime=None)

    # Get theater name for showtime.theater_id
    theater_name = None
    for t in theaters:
        if t['theater_id'] == showtime['theater_id']:
            theater_name = t['theater_name']
            break

    # Find movie title for showtime.movie_id
    movie_title = None
    for m in movies:
        if m['movie_id'] == showtime['movie_id']:
            movie_title = m['title']
            break

    # Filter seats for this theater_id
    seats_filtered = []
    for seat in seats:
        if seat['theater_id'] == showtime['theater_id']:
            seat_dict = {
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            }
            seats_filtered.append(seat_dict)

    selected_showtime = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie_title,
        'theater_name': theater_name,
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'price': showtime['price']
    }

    return render_template('seat_selection.html', seats=seats_filtered, selected_showtime=selected_showtime)


@app.route('/booking/confirmation', methods=['GET'])
def booking_confirmation():
    # Expect booking_summary info from query parameters or session ideally
    # But here we do GET with query args for seats and showtime_id, name, email not passed yet
    # According to spec, booking_summary dict with movie_title(str), showtime_date(str), showtime_time(str), seats(list of str), total_price(float)

    # For simplicity, gather parameters from query string
    showtime_id = request.args.get('showtime_id', type=int)
    seat_list_str = request.args.get('seats', '')
    seats = seat_list_str.split(',') if seat_list_str else []

    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()

    if not showtime_id or not seats:
        # Missing info
        return render_template('booking_confirmation.html', booking_summary=None)

    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if not showtime:
        return render_template('booking_confirmation.html', booking_summary=None)

    movie_title = None
    for m in movies:
        if m['movie_id'] == showtime['movie_id']:
            movie_title = m['title']
            break

    booking_summary = {
        'movie_title': movie_title,
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'seats': seats,
        'total_price': round(showtime['price'] * len(seats), 2)
    }

    return render_template('booking_confirmation.html', booking_summary=booking_summary)


@app.route('/booking/confirmation', methods=['POST'])
def confirm_booking():
    # form data: customer_name(str), customer_email(str), seats(list of str), showtime_id(int)
    customer_name = request.form.get('customer_name', '')
    customer_email = request.form.get('customer_email', '')
    seats_str = request.form.get('seats', '')
    seats_list = seats_str.split(',') if seats_str else []
    showtime_id = request.form.get('showtime_id', type=int)

    if not (customer_name and customer_email and seats_list and showtime_id):
        # Missing data, redirect back to dashboard or error page
        return redirect(url_for('dashboard_page'))

    bookings = load_bookings()
    showtimes = load_showtimes()

    # Find showtime
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if not showtime:
        return redirect(url_for('dashboard_page'))

    # Calculate total price
    total_price = round(showtime['price'] * len(seats_list), 2)

    # Assign new booking_id
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1

    booking_date = datetime.now().strftime('%Y-%m-%d')

    # Create new booking dict
    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats_list
    }

    bookings.append(new_booking)

    # Save bookings
    if not save_bookings(bookings):
        # Error saving, redirect back or error
        return redirect(url_for('dashboard_page'))

    return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=','.join(seats_list)))


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    # bookings (list of dict: booking_id(int), movie_title(str), booking_date(str), seats(list of str), status(str))
    bookings_list = []
    movie_dict = {m['movie_id']: m['title'] for m in movies}
    for b in bookings:
        movie_title = movie_dict.get(next((s['movie_id'] for s in showtimes if s['showtime_id'] == b['showtime_id']), None), None)
        bookings_list.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title if movie_title else 'Unknown',
            'booking_date': b['booking_date'],
            'seats': b['seats_booked'],
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings_list)


@app.route('/bookings/<int:booking_id>')
def view_booking_details(booking_id):
    bookings = load_bookings()
    showtimes = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()

    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return render_template('booking_details.html', booking=None)

    # Find showtime info
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == booking['showtime_id']:
            showtime = s
            break

    theater_name = None
    if showtime:
        for t in theaters:
            if t['theater_id'] == showtime['theater_id']:
                theater_name = t['theater_name']
                break

    movie_title = None
    if showtime:
        for m in movies:
            if m['movie_id'] == showtime['movie_id']:
                movie_title = m['title']
                break

    detailed_booking = {
        'booking_id': booking['booking_id'],
        'movie_title': movie_title if movie_title else 'Unknown',
        'showtime_date': showtime['showtime_date'] if showtime else '',
        'seats': booking['seats_booked'],
        'status': booking['status'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price']
    }

    return render_template('booking_details.html', booking=detailed_booking)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    # theaters (list of dict: theater_id, theater_name, location, city, screens, facilities)
    return render_template('theater_information.html', theaters=theaters)


if __name__ == '__main__':
    app.run()
