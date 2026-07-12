from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def load_movies():
    movies = []
    try:
        with open('data/movies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
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

def load_theaters():
    theaters = []
    try:
        with open('data/theaters.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
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

def load_showtimes():
    showtimes = []
    try:
        with open('data/showtimes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
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

def load_seats():
    seats = []
    try:
        with open('data/seats.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
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

def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                seats_list = parts[7].split(',') if parts[7].strip() else []
                booking = {
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': seats_list
                }
                bookings.append(booking)
    except FileNotFoundError:
        pass
    return bookings

def load_genres():
    genres = []
    try:
        with open('data/genres.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    except FileNotFoundError:
        pass
    return genres

def save_bookings(bookings):
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats_booked'])
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
                f.write(line)
    except Exception as e:
        # Could log error
        pass

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Featured movies: top rated (>8.5) limit 5
    featured_movies = []
    for m in movies:
        if m['rating'] > 8.5:
            featured_movies.append({
                'movie_id': m['movie_id'],
                'title': m['title'],
                'poster': '',  # no poster info in data
                'rating': m['rating']
            })
    featured_movies.sort(key=lambda x: x['rating'], reverse=True)
    featured_movies = featured_movies[:5]

    # Upcoming releases: movies with release_date in future
    upcoming_releases = []
    today = datetime.today().date()
    for m in movies:
        try:
            rd = datetime.strptime(m['release_date'], '%Y-%m-%d').date()
            if rd > today:
                upcoming_releases.append({'movie_id': m['movie_id'], 'title': m['title'], 'release_date': m['release_date']})
        except Exception:
            continue
    upcoming_releases.sort(key=lambda x: x['release_date'])

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)

@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres_raw = load_genres()
    genres = [{'genre_name': g['genre_name']} for g in genres_raw]

    # For catalog.html context:
    # movies: movie_id, title, genre, rating, duration, poster (empty string as no poster info)
    movies_simple = []
    for m in movies:
        movies_simple.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster': ''
        })

    return render_template('catalog.html', movies=movies_simple, genres=genres)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = None
    for m in movies:
        if m['movie_id'] == movie_id:
            movie = m
            break
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()

    # Filter showtimes by movie_id
    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]

    # Prepare theaters list
    theater_list = []
    for t in theaters:
        theater_list.append({
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name']
        })

    # showtimes context: showtime_id, theater_name, theater_id, showtime_date, showtime_time, price
    showtimes_context = []
    for s in filtered_showtimes:
        theater_name = next((t['theater_name'] for t in theaters if t['theater_id'] == s['theater_id']), '')
        showtimes_context.append({
            'showtime_id': s['showtime_id'],
            'theater_name': theater_name,
            'theater_id': s['theater_id'],
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        })

    return render_template('showtimes.html', movie_id=movie_id, showtimes=showtimes_context, theaters=theater_list)

@app.route('/seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if not showtime:
        return "Showtime not found", 404

    # Need theater_id from showtime
    theater_id = showtime['theater_id']

    seats_all = load_seats()

    # Filter seats for theater and screen. Spec says seats file has theater_id, screen_id.
    # But showtime doesn't have screen_id directly. We'll assume screen_id=1 for theater (lack of data).
    screen_id = 1

    seats = []
    available_seats_count = 0
    for seat in seats_all:
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
            seats.append(seat)
            if seat['status'].lower() == 'available':
                available_seats_count += 1

    # We'll pass selected_seats as empty list initially
    selected_seats = []

    return render_template('seat_selection.html', showtime=showtime, available_seats=available_seats_count, seats=seats, selected_seats=selected_seats)

@app.route('/booking/confirm', methods=['GET', 'POST'])
def booking_confirmation():
    if request.method == 'GET':
        # Expect booking details passed as params? Spec not explicit.
        # We will assume query params: movie, showtime_date, showtime_time, theater_name, seats (comma separated), total_price
        movie = request.args.get('movie', '')
        showtime_date = request.args.get('showtime_date', '')
        showtime_time = request.args.get('showtime_time', '')
        theater_name = request.args.get('theater_name', '')
        seats_str = request.args.get('seats', '')
        seats = []
        if seats_str:
            seats = seats_str.split(',')
        total_price_str = request.args.get('total_price', '0')
        try:
            total_price = float(total_price_str)
        except:
            total_price = 0.0

        booking_details = {
            'movie': movie,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats': seats,
            'total_price': total_price
        }

        return render_template('confirmation.html', booking_details=booking_details)
    else:
        # POST method to submit booking
        # Expected form data: showtime_id, customer_name, customer_email, seats (comma separated), total_price
        showtime_id = request.form.get('showtime_id', type=int)
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        seats_str = request.form.get('seats', '')
        seats = seats_str.split(',') if seats_str else []
        total_price = request.form.get('total_price', type=float) or 0.0

        if not showtime_id or not customer_name or not customer_email or not seats:
            return render_template('confirmation.html', success=False, error_message='Missing required booking information.')

        bookings = load_bookings()

        # Check if seats are still available -> Confirm no seat is already booked
        # We can check seats status from seats.txt
        seats_all = load_seats()
        # We don't have screen_id in booking confirmation, but we get theater_id from showtime
        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if not showtime:
            return render_template('confirmation.html', success=False, error_message='Showtime not found.')

        theater_id = showtime['theater_id']
        screen_id = 1

        seat_status_map = {(seat['row'] + str(seat['column'])): seat['status'].lower() for seat in seats_all if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id}

        for seat_label in seats:
            if seat_label not in seat_status_map or seat_status_map[seat_label] != 'available':
                return render_template('confirmation.html', success=False, error_message=f'Seat {seat_label} is not available.')

        # Assign new booking_id
        max_booking_id = max([b['booking_id'] for b in bookings], default=0)
        new_booking_id = max_booking_id + 1

        booking_date = datetime.today().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': new_booking_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats
        }

        bookings.append(new_booking)
        save_bookings(bookings)

        # Update seat statuses to 'Booked' in seats.txt
        for seat in seats_all:
            seat_label = seat['row'] + str(seat['column'])
            if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id and seat_label in seats:
                seat['status'] = 'Booked'
        # Save seats
        try:
            with open('data/seats.txt', 'w', encoding='utf-8') as f:
                for seat in seats_all:
                    line = f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n"
                    f.write(line)
        except Exception:
            # We don't fail the booking if seats file cannot be written but could log
            pass

        return render_template('confirmation.html', success=True, error_message='')

@app.route('/bookings')
def booking_history():
    bookings = load_bookings()

    # For bookings.html context:
    bookings_context = []
    movies = load_movies()
    movie_dict = {m['movie_id']: m['title'] for m in movies}

    for b in bookings:
        movie_title = movie_dict.get(b['showtime_id'], 'Unknown')
        # We need movie title from showtime
        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id'] == b['showtime_id']), None)
        if showtime:
            movie_title = movie_dict.get(showtime['movie_id'], 'Unknown')
        booking_entry = {
            'booking_id': b['booking_id'],
            'movie': movie_title,
            'date': b['booking_date'],
            'seats': b['seats_booked'],
            'status': b['status']
        }
        bookings_context.append(booking_entry)

    return render_template('bookings.html', bookings=bookings_context)

@app.route('/bookings/<int:booking_id>')
def view_booking_details(booking_id):
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
    return render_template('theater.html', theaters=theaters)

if __name__ == '__main__':
    app.run()
