from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import date

app = Flask(__name__)

# Helper functions to load data files

def load_movies():
    movies = []
    path = 'data/movies.txt'
    if not os.path.exists(path):
        return movies
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) == 8:
                    movie = {
                        'movie_id': int(fields[0]),
                        'title': fields[1],
                        'director': fields[2],
                        'genre': fields[3],
                        'rating': float(fields[4]),
                        'duration': int(fields[5]),
                        'description': fields[6],
                        'release_date': fields[7]
                    }
                    movies.append(movie)
    except IOError:
        pass
    return movies


def load_theaters():
    theaters = []
    path = 'data/theaters.txt'
    if not os.path.exists(path):
        return theaters
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) == 6:
                    theater = {
                        'theater_id': int(fields[0]),
                        'theater_name': fields[1],
                        'location': fields[2],
                        'city': fields[3],
                        'screens': int(fields[4]),
                        'facilities': [f.strip() for f in fields[5].split(',')] if fields[5] else []
                    }
                    theaters.append(theater)
    except IOError:
        pass
    return theaters


def load_showtimes():
    showtimes = []
    path = 'data/showtimes.txt'
    if not os.path.exists(path):
        return showtimes
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) == 7:
                    showtime = {
                        'showtime_id': int(fields[0]),
                        'movie_id': int(fields[1]),
                        'theater_id': int(fields[2]),
                        'showtime_date': fields[3],
                        'showtime_time': fields[4],
                        'price': float(fields[5]),
                        'available_seats': int(fields[6])
                    }
                    showtimes.append(showtime)
    except IOError:
        pass
    return showtimes


def load_seats():
    seats = []
    path = 'data/seats.txt'
    if not os.path.exists(path):
        return seats
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) == 7:
                    seat = {
                        'seat_id': int(fields[0]),
                        'theater_id': int(fields[1]),
                        'screen_id': int(fields[2]),
                        'row': fields[3],
                        'column': int(fields[4]),
                        'seat_type': fields[5],
                        'status': fields[6]
                    }
                    seats.append(seat)
    except IOError:
        pass
    return seats


def load_bookings():
    bookings = []
    path = 'data/bookings.txt'
    if not os.path.exists(path):
        return bookings
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) == 8:
                    booking_id = int(fields[0])
                    showtime_id = int(fields[1])
                    customer_name = fields[2]
                    customer_email = fields[3]
                    booking_date = fields[4]
                    total_price = float(fields[5])
                    status = fields[6]
                    seats_booked = [s.strip() for s in fields[7].split(',') if s.strip()]
                    booking = {
                        'booking_id': booking_id,
                        'showtime_id': showtime_id,
                        'customer_name': customer_name,
                        'customer_email': customer_email,
                        'booking_date': booking_date,
                        'total_price': total_price,
                        'status': status,
                        'seats_booked': seats_booked
                    }
                    bookings.append(booking)
    except IOError:
        pass
    return bookings


def load_genres():
    genres = []
    path = 'data/genres.txt'
    if not os.path.exists(path):
        return genres
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                fields = line.split('|')
                if len(fields) >= 2:
                    genres.append(fields[1])
    except IOError:
        pass
    return genres


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    movies = load_movies()
    # Featured movies and upcoming releases can be assumed filtered or entire movies list for simplicity
    featured_movies = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'poster_url': f"/static/posters/{m['movie_id']}.jpg",  # Assumed path
        'rating': m['rating'],
        'duration': m['duration']
    } for m in movies]

    # Dummy upcoming releases: could filter by date after today
    upcoming_releases = featured_movies

    navigation_links = {
        'browse_movies': url_for('movie_catalog'),
        'booking_history': url_for('booking_history'),
        'showtimes': url_for('dashboard_page')  # no dedicated route for generic showtimes, so link dashboard
    }

    return render_template('dashboard.html',
                           featured_movies=featured_movies,
                           upcoming_releases=upcoming_releases,
                           navigation_links=navigation_links)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    movies_for_catalog = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'poster_url': f"/static/posters/{m['movie_id']}.jpg",
        'rating': m['rating'],
        'duration': m['duration'],
        'genre': m['genre']
    } for m in movies]
    return render_template('movie_catalog.html', movies=movies_for_catalog, genres=genres)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    showtimes_all = load_showtimes()
    theaters_all = load_theaters()

    # Filters from query params
    selected_theater_id = request.args.get('theater_id', type=int)
    selected_date = request.args.get('date')

    # Filter showtimes
    showtimes_filtered = []
    for st in showtimes_all:
        if st['movie_id'] != movie_id:
            continue
        if selected_theater_id and st['theater_id'] != selected_theater_id:
            continue
        if selected_date and st['showtime_date'] != selected_date:
            continue
        theater_name = next((t['theater_name'] for t in theaters_all if t['theater_id'] == st['theater_id']), 'Unknown')
        showtime = {
            'showtime_id': st['showtime_id'],
            'theater_name': theater_name,
            'showtime_date': st['showtime_date'],
            'showtime_time': st['showtime_time'],
            'price': st['price']
        }
        showtimes_filtered.append(showtime)

    theaters_context = [{'theater_id': t['theater_id'], 'theater_name': t['theater_name']} for t in theaters_all]

    filters = {
        'selected_theater_id': selected_theater_id,
        'selected_date': selected_date
    }

    return render_template('showtime_selection.html', showtimes=showtimes_filtered, theaters=theaters_context, filters=filters)


@app.route('/select-seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)

    seats_all = load_seats()

    # Filter seats for theater and screen
    seats = [seat for seat in seats_all if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == theater['screens']]  # Using theater['screens'] as screen number might be incorrect, but given no screen info in showtime, assume screen 1

    selected_seats = []  # Initially none selected

    showtime_info = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'] if movie else '',
        'theater_name': theater['theater_name'] if theater else '',
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time']
    }

    # Prepare seats context for template
    seats_context = []
    for seat in seats:
        seats_context.append({
            'seat_id': seat['seat_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat['status']
        })

    return render_template('seat_selection.html', seats=seats_context, selected_seats=selected_seats, showtime_info=showtime_info)


@app.route('/booking-confirmation/<int:showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)

    showtime_info = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'] if movie else '',
        'theater_name': theater['theater_name'] if theater else '',
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'price': showtime['price']
    }

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '')
        customer_email = request.form.get('customer_email', '')
        selected_seats = request.form.getlist('selected_seats')

        if not customer_name or not customer_email or not selected_seats:
            return render_template('booking_confirmation.html',
                                   showtime_info=showtime_info,
                                   selected_seats=selected_seats,
                                   customer_name=customer_name,
                                   customer_email=customer_email,
                                   error='All fields are required.')

        total_price = len(selected_seats) * showtime['price']

        # Load existing bookings, compute new booking_id
        bookings = load_bookings()
        next_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

        booking_date = date.today().isoformat()
        seats_booked_str = ','.join(selected_seats)

        booking_line = f"{next_booking_id}|{showtime_id}|{customer_name}|{customer_email}|{booking_date}|{total_price:.2f}|Confirmed|{seats_booked_str}\n"

        try:
            with open('data/bookings.txt', 'a', encoding='utf-8') as f:
                f.write(booking_line)
        except IOError:
            return render_template('booking_confirmation.html',
                                   showtime_info=showtime_info,
                                   selected_seats=selected_seats,
                                   customer_name=customer_name,
                                   customer_email=customer_email,
                                   error='Failed to save booking. Please try again.')

        return redirect(url_for('booking_history'))

    return render_template('booking_confirmation.html',
                           showtime_info=showtime_info,
                           selected_seats=[],
                           customer_name='',
                           customer_email='')


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()
    # Prepare bookings with movie title
    bookings_with_title = []
    for booking in bookings:
        movie_title = ''
        showtime_id = booking['showtime_id']
        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if showtime:
            movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
            if movie:
                movie_title = movie['title']
        booking_copy = booking.copy()
        booking_copy['movie_title'] = movie_title
        bookings_with_title.append(booking_copy)

    status_filter = request.args.get('status_filter', 'All')
    if status_filter != 'All':
        bookings_with_title = [b for b in bookings_with_title if b['status'] == status_filter]

    status_filter_options = ['All', 'Confirmed', 'Cancelled', 'Completed']

    return render_template('booking_history.html',
                           bookings=bookings_with_title,
                           status_filter_options=status_filter_options)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    movies = load_movies()
    showtimes = load_showtimes()
    movie_title = ''
    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    if showtime:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        if movie:
            movie_title = movie['title']
    booking['movie_title'] = movie_title
    return render_template('booking_detail.html', booking=booking)


@app.route('/theaters')
def theater_info():
    theaters = load_theaters()
    cities = sorted(list({t['city'] for t in theaters}))
    selected_location = request.args.get('location')
    if selected_location:
        filtered_theaters = [t for t in theaters if t['city'] == selected_location]
    else:
        filtered_theaters = theaters

    location_filter_options = cities

    return render_template('theater_info.html',
                           theaters=filtered_theaters,
                           location_filter_options=location_filter_options)


if __name__ == '__main__':
    app.run()