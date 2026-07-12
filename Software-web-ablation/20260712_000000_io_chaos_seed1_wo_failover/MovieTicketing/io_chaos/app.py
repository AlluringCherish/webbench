from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def read_movies():
    movies = []
    try:
        with open('data/movies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        movie = {
                            'movie_id': int(parts[0]),
                            'title': parts[1],
                            'director': parts[2],
                            'genre': parts[3],
                            'rating': float(parts[4]),
                            'duration': int(parts[5]),
                            'description': parts[6],
                            'release_date': parts[7]
                        }
                        movies.append(movie)
    except FileNotFoundError:
        pass
    return movies

def read_theaters():
    theaters = []
    try:
        with open('data/theaters.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        theater = {
                            'theater_id': int(parts[0]),
                            'theater_name': parts[1],
                            'location': parts[2],
                            'city': parts[3],
                            'screens': int(parts[4]),
                            'facilities': parts[5]
                        }
                        theaters.append(theater)
    except FileNotFoundError:
        pass
    return theaters

def read_showtimes():
    showtimes = []
    try:
        with open('data/showtimes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        showtime = {
                            'showtime_id': int(parts[0]),
                            'movie_id': int(parts[1]),
                            'theater_id': int(parts[2]),
                            'showtime_date': parts[3],
                            'showtime_time': parts[4],
                            'price': float(parts[5]),
                            'available_seats': int(parts[6])
                        }
                        showtimes.append(showtime)
    except FileNotFoundError:
        pass
    return showtimes

def read_seats():
    seats = []
    try:
        with open('data/seats.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        seat = {
                            'seat_id': int(parts[0]),
                            'theater_id': int(parts[1]),
                            'screen_id': int(parts[2]),
                            'row': parts[3],
                            'column': int(parts[4]),
                            'seat_type': parts[5],
                            'status': parts[6]
                        }
                        seats.append(seat)
    except FileNotFoundError:
        pass
    return seats

def read_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        booking = {
                            'booking_id': int(parts[0]),
                            'showtime_id': int(parts[1]),
                            'customer_name': parts[2],
                            'customer_email': parts[3],
                            'booking_date': parts[4],
                            'total_price': float(parts[5]),
                            'status': parts[6],
                            'seats_booked': parts[7].split(',') if parts[7] else []
                        }
                        bookings.append(booking)
    except FileNotFoundError:
        pass
    return bookings

def save_bookings(bookings):
    lines = []
    for b in bookings:
        seats_str = ','.join(b['seats_booked']) if b['seats_booked'] else ''
        line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}"
        lines.append(line)
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f'Error saving bookings: {e}')


def read_genres():
    genres = []
    try:
        with open('data/genres.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        genre = {
                            'genre_id': int(parts[0]),
                            'genre_name': parts[1],
                            'description': parts[2]
                        }
                        genres.append(genre)
    except FileNotFoundError:
        pass
    return genres


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = read_movies()
    # Featured movies: let's assume top 3 by rating as featured
    sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:3]
    # Prepare featured_movies list as per spec fields
    featured_movies = []
    for m in sorted_movies:
        featured_movies.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration']
        })
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/movies')
def movie_catalog():
    movies_all = read_movies()
    genres_all = read_genres()

    # Prepare movies list with extra 'poster_url' field (not in data, so can be empty string or placeholder)
    movies = []
    for m in movies_all:
        movies.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster_url': ''  # No poster URL provided in data
        })

    genres = []
    for g in genres_all:
        genres.append({
            'genre_id': g['genre_id'],
            'genre_name': g['genre_name']
        })

    return render_template('movie_catalog.html', movies=movies, genres=genres)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = read_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    # Prepare movie dict as per spec
    movie_dict = {
        'movie_id': movie['movie_id'],
        'title': movie['title'],
        'director': movie['director'],
        'genre': movie['genre'],
        'rating': movie['rating'],
        'duration': movie['duration'],
        'description': movie['description']
    }
    return render_template('movie_details.html', movie=movie_dict)


@app.route('/movies/<int:movie_id>/showtimes')
def select_showtime(movie_id):
    showtimes_all = read_showtimes()
    theaters_all = read_theaters()
    # Filter showtimes for given movie_id
    showtimes = [s for s in showtimes_all if s['movie_id'] == movie_id]

    # Prepare theaters list as per spec
    theaters = []
    for t in theaters_all:
        theaters.append({
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name']
        })

    # Prepare showtimes list as per spec fields
    showtimes_list = []
    for s in showtimes:
        theater_name = next((t['theater_name'] for t in theaters_all if t['theater_id'] == s['theater_id']), '')
        showtimes_list.append({
            'showtime_id': s['showtime_id'],
            'theater_name': theater_name,
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        })

    return render_template('showtime_selection.html', movie_id=movie_id, showtimes=showtimes_list, theaters=theaters)


@app.route('/showtimes/<int:showtime_id>/seats')
def select_seats(showtime_id):
    showtimes = read_showtimes()
    seats_all = read_seats()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    # Need to find theater_id from showtime
    theater_id = showtime['theater_id']
    screen_id = 1  # Not provided, assume screen_id=1 as example or all seats for theater

    # Filter seats by theater_id and screen_id
    seat_map = []
    for seat in seats_all:
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
            seat_map.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })

    # Get selected_seats query param or empty list
    selected_seats = request.args.getlist('selected_seats')

    return render_template('seat_selection.html', showtime_id=showtime_id, seat_map=seat_map, selected_seats=selected_seats)


@app.route('/bookings/confirm', methods=['GET', 'POST'])
def booking_confirmation():
    if request.method == 'GET':
        # Booking summary data should come from query parameters or session in real app; here we mock retrieval from query params
        movie_title = request.args.get('movie_title', '')
        showtime_date = request.args.get('showtime_date', '')
        showtime_time = request.args.get('showtime_time', '')
        seats = request.args.getlist('seats')
        total_price = request.args.get('total_price', type=float, default=0.0)

        booking_summary = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'seats': seats,
            'total_price': total_price
        }
        return render_template('booking_confirmation.html', booking_summary=booking_summary)
    else:
        # POST: form submission to confirm booking
        # Extract form data
        movie_title = request.form.get('movie_title')
        showtime_date = request.form.get('showtime_date')
        showtime_time = request.form.get('showtime_time')
        seats = request.form.getlist('seats')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        total_price = request.form.get('total_price', type=float)

        # Validate required fields
        if not (movie_title and showtime_date and showtime_time and seats and customer_name and customer_email and total_price is not None):
            return "Missing booking information", 400

        # Read existing bookings
        bookings = read_bookings()
        showtimes = read_showtimes()

        # Find showtime_id by matching movie & date & time
        matched_showtime = None
        for s in showtimes:
            if s['showtime_date'] == showtime_date and s['showtime_time'] == showtime_time:
                # We do not check movie_title here because movie_title is not stored in showtimes, match by movie_id?
                # Instead we find showtime with matching showtime_id?
                # We'll find by showtime_date + showtime_time only given data limitations
                matched_showtime = s
                break
        if not matched_showtime:
            return "Showtime mismatch", 400

        new_id = 1
        if bookings:
            new_id = max(b['booking_id'] for b in bookings) + 1

        booking_date = datetime.now().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': new_id,
            'showtime_id': matched_showtime['showtime_id'],
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats
        }

        bookings.append(new_booking)
        save_bookings(bookings)

        return redirect(url_for('booking_history'))


@app.route('/bookings')
def booking_history():
    bookings_all = read_bookings()
    movies_all = read_movies()

    # Prepare bookings list with fields as spec
    bookings = []
    for b in bookings_all:
        showtime_id = b['showtime_id']
        movie_title = ''
        # Find movie title by showtime's movie_id
        showtimes = read_showtimes()
        st = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if st:
            mv = next((m for m in movies_all if m['movie_id'] == st['movie_id']), None)
            if mv:
                movie_title = mv['title']

        bookings.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats': b['seats_booked'],
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = read_showtimes()
    movies = read_movies()

    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    if not showtime:
        return "Showtime for booking not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie for booking not found", 404

    booking_dict = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'seats': booking['seats_booked'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price'],
        'status': booking['status']
    }

    return render_template('booking_details.html', booking=booking_dict)


@app.route('/theaters')
def theater_information():
    theaters_all = read_theaters()

    theaters = []
    for t in theaters_all:
        theaters.append({
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name'],
            'location': t['location'],
            'city': t['city'],
            'screens': t['screens'],
            'facilities': t['facilities']
        })

    return render_template('theater_information.html', theaters=theaters)


if __name__ == '__main__':
    app.run()