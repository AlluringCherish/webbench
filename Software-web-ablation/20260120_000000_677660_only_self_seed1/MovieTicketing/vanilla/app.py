from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.txt')
THEATERS_FILE = os.path.join(DATA_DIR, 'theaters.txt')
SHOWTIMES_FILE = os.path.join(DATA_DIR, 'showtimes.txt')
SEATS_FILE = os.path.join(DATA_DIR, 'seats.txt')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.txt')
GENRES_FILE = os.path.join(DATA_DIR, 'genres.txt')

# Utility functions for file operations

def load_pipe_delimited_file(filepath, fields):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != len(fields):
                    continue
                item = {field: part for field, part in zip(fields, parts)}
                data.append(item)
    except Exception:
        # Robust error handling: just return empty list if file not found or error
        pass
    return data


def save_pipe_delimited_file(filepath, data, fields):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                line = '|'.join(str(item.get(field, '')) for field in fields)
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load specific data sets

def load_movies():
    fields = ['movie_id','title','director','genre','rating','duration','description','release_date']
    movies = load_pipe_delimited_file(MOVIES_FILE, fields)
    for m in movies:
        try:
            m['movie_id'] = int(m['movie_id'])
            m['rating'] = float(m['rating'])
            m['duration'] = int(m['duration'])
        except Exception:
            pass
    return movies


def load_genres():
    fields = ['genre_id','genre_name','description']
    genres = load_pipe_delimited_file(GENRES_FILE, fields)
    for g in genres:
        try:
            g['genre_id'] = int(g['genre_id'])
        except Exception:
            pass
    return genres


def load_theaters():
    fields = ['theater_id','theater_name','location','city','screens','facilities']
    theaters = load_pipe_delimited_file(THEATERS_FILE, fields)
    for t in theaters:
        try:
            t['theater_id'] = int(t['theater_id'])
            t['screens'] = int(t['screens'])
        except Exception:
            pass
    return theaters


def load_showtimes():
    fields = ['showtime_id','movie_id','theater_id','showtime_date','showtime_time','price','available_seats']
    showtimes = load_pipe_delimited_file(SHOWTIMES_FILE, fields)
    for s in showtimes:
        try:
            s['showtime_id'] = int(s['showtime_id'])
            s['movie_id'] = int(s['movie_id'])
            s['theater_id'] = int(s['theater_id'])
            s['price'] = float(s['price'])
            s['available_seats'] = int(s['available_seats'])
        except Exception:
            pass
    return showtimes


def load_seats():
    fields = ['seat_id','theater_id','screen_id','row','column','seat_type','status']
    seats = load_pipe_delimited_file(SEATS_FILE, fields)
    for s in seats:
        try:
            s['seat_id'] = int(s['seat_id'])
            s['theater_id'] = int(s['theater_id'])
            s['screen_id'] = int(s['screen_id'])
            s['column'] = int(s['column'])
        except Exception:
            pass
    return seats


def load_bookings():
    fields = ['booking_id','showtime_id','customer_name','customer_email','booking_date','total_price','status','seats_booked']
    bookings = load_pipe_delimited_file(BOOKINGS_FILE, fields)
    for b in bookings:
        try:
            b['booking_id'] = int(b['booking_id'])
            b['showtime_id'] = int(b['showtime_id'])
            b['total_price'] = float(b['total_price'])
            b['seats_booked'] = b['seats_booked'].split(',') if b['seats_booked'] else []
        except Exception:
            pass
    return bookings


def save_bookings(bookings):
    fields = ['booking_id','showtime_id','customer_name','customer_email','booking_date','total_price','status','seats_booked']
    # Prepare seats_booked as comma string to save
    bookings_to_save = []
    for b in bookings:
        copy_b = b.copy()
        if isinstance(copy_b.get('seats_booked'), list):
            copy_b['seats_booked'] = ','.join(copy_b['seats_booked'])
        bookings_to_save.append(copy_b)
    return save_pipe_delimited_file(BOOKINGS_FILE, bookings_to_save, fields)


# Helper functions

def get_movie_by_id(movie_id, movies=None):
    if movies is None:
        movies = load_movies()
    for m in movies:
        if m['movie_id'] == movie_id:
            return m
    return None


def get_theater_by_id(theater_id, theaters=None):
    if theaters is None:
        theaters = load_theaters()
    for t in theaters:
        if t['theater_id'] == theater_id:
            return t
    return None


def get_showtime_by_id(showtime_id, showtimes=None):
    if showtimes is None:
        showtimes = load_showtimes()
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            return s
    return None


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    today = datetime.today().date()
    featured_movies = []
    upcoming_releases = []
    for movie in movies:
        if movie['rating'] >= 8.5:
            featured_movies.append({
                'movie_id': movie['movie_id'],
                'title': movie['title'],
                'poster_url': None
            })
        try:
            rel_date = datetime.strptime(movie['release_date'], '%Y-%m-%d').date()
        except Exception:
            rel_date = None
        if rel_date and rel_date > today:
            upcoming_releases.append({
                'movie_id': movie['movie_id'],
                'title': movie['title'],
                'poster_url': None
            })

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()

    selected_genre = request.args.get('genre', '')
    search_query = request.args.get('search', '').strip()

    filtered_movies = movies

    if selected_genre:
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == selected_genre.lower()]
    if search_query:
        sq = search_query.lower()
        filtered_movies = [m for m in filtered_movies if sq in m['title'].lower() or sq in m['genre'].lower()]

    return render_template('movie_catalog.html', movies=filtered_movies, genres=genres, selected_genre=selected_genre, search_query=search_query)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return "Movie not found", 404
    genres = load_genres()
    return render_template('movie_details.html', movie=movie, genres=genres)


@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return "Movie not found", 404

    showtimes = load_showtimes()
    theaters = load_theaters()

    selected_theater = request.args.get('theater', '')
    selected_date = request.args.get('date', '')

    relevant_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]

    if selected_theater:
        theater_ids = [t['theater_id'] for t in theaters if selected_theater.lower() in t['theater_name'].lower()]
        relevant_showtimes = [s for s in relevant_showtimes if s['theater_id'] in theater_ids]

    if selected_date:
        relevant_showtimes = [s for s in relevant_showtimes if s['showtime_date'] == selected_date]

    return render_template('showtime_selection.html', movie=movie, showtimes=relevant_showtimes, theaters=theaters, selected_theater=selected_theater, selected_date=selected_date)


@app.route('/select_seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        return "Showtime not found", 404
    seats = load_seats()

    theater_id = showtime['theater_id']
    screen_seats = [s for s in seats if s['theater_id'] == theater_id]

    for seat in screen_seats:
        seat['seat_label'] = f"{seat['row']}{seat['column']}"

    selected_seats = request.args.getlist('selected_seats')

    return render_template('seat_selection.html', showtime=showtime, seats=screen_seats, selected_seats=selected_seats)


def seats_available(seats_db, selected_seats_labels, theater_id):
    for sel in selected_seats_labels:
        found = False
        for seat in seats_db:
            if seat['theater_id'] == theater_id and seat.get('seat_label') == sel:
                found = True
                if seat['status'] != 'Available':
                    return False
                break
        if not found:
            return False
    return True


@app.route('/booking_confirmation', methods=['POST'])
def booking_confirmation():
    errors = []

    showtime_id = request.form.get('showtime_id', type=int)
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    selected_seats = request.form.getlist('selected_seats')

    if not showtime_id:
        errors.append('Showtime ID is required.')
    if not customer_name:
        errors.append('Customer name is required.')
    if not customer_email:
        errors.append('Customer email is required.')
    if not selected_seats:
        errors.append('At least one seat must be selected.')

    if errors:
        return render_template('booking_confirmation.html', booking_summary=None, errors=errors)

    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        errors.append('Showtime not found.')
        return render_template('booking_confirmation.html', booking_summary=None, errors=errors)

    theater = get_theater_by_id(showtime['theater_id'])
    movie = get_movie_by_id(showtime['movie_id'])

    seats_db = load_seats()
    for seat in seats_db:
        seat['seat_label'] = f"{seat['row']}{seat['column']}"

    if not seats_available(seats_db, selected_seats, showtime['theater_id']):
        errors.append('One or more selected seats are not available.')
        return render_template('booking_confirmation.html', booking_summary=None, errors=errors)

    total_price = showtime['price'] * len(selected_seats)

    booking_summary = {
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'theater_name': theater['theater_name'],
        'seats': selected_seats,
        'total_price': total_price
    }

    bookings = load_bookings()
    new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1
    booking_date = datetime.now().strftime('%Y-%m-%d')

    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': selected_seats
    }

    bookings.append(new_booking)
    if not save_bookings(bookings):
        errors.append('Failed to save booking.')
        return render_template('booking_confirmation.html', booking_summary=None, errors=errors)

    # Mark seats as booked
    for seat in seats_db:
        if seat['theater_id'] == showtime['theater_id'] and seat['seat_label'] in selected_seats:
            seat['status'] = 'Booked'
    save_pipe_delimited_file(SEATS_FILE, seats_db, ['seat_id','theater_id','screen_id','row','column','seat_type','status'])

    return render_template('booking_confirmation.html', booking_summary=booking_summary, errors=None)


@app.route('/booking_confirmation/<int:booking_id>')
def booking_confirmation_get(booking_id):
    bookings = load_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return "Booking not found", 404
    return render_template('booking_confirmation.html', booking=booking)


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    movie_map = {m['movie_id']: m for m in movies}
    # Map showtime_id to showtime
    showtime_map = {s['showtime_id']: s for s in showtimes}

    bookings_context = []
    for b in bookings:
        showtime = showtime_map.get(b['showtime_id'])
        movie_title = movie_map[showtime['movie_id']]['title'] if showtime else 'Unknown'
        bookings_context.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats': b['seats_booked'],
            'status': b['status']
        })

    filtered_status = request.args.get('status', 'All')
    if filtered_status != 'All':
        bookings_context = [b for b in bookings_context if b['status'].lower() == filtered_status.lower()]

    return render_template('booking_history.html', bookings=bookings_context, filtered_status=filtered_status)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return "Booking not found", 404
    return render_template('booking_details.html', booking=booking)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    selected_location = request.args.get('location', '')
    filtered_theaters = theaters
    if selected_location:
        filtered_theaters = [t for t in theaters if t['location'].lower() == selected_location.lower()]
    return render_template('theater_information.html', theaters=filtered_theaters, selected_location=selected_location)


if __name__ == '__main__':
    app.run()