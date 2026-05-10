'''
Main Flask application for MovieTicketing web application.
Defines all routes starting from '/' for Dashboard and other pages.
Ensures all navigation uses Flask routing URLs for consistent navigation.
Includes robust error handling and fallback mechanisms for missing or incomplete data files.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_movies():
    movies = []
    path = os.path.join(DATA_DIR, 'movies.txt')
    if not os.path.exists(path):
        return movies
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        try:
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
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return movies
def read_theaters():
    theaters = []
    path = os.path.join(DATA_DIR, 'theaters.txt')
    if not os.path.exists(path):
        return theaters
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        try:
                            theater = {
                                'theater_id': int(parts[0]),
                                'theater_name': parts[1],
                                'location': parts[2],
                                'city': parts[3],
                                'screens': int(parts[4]),
                                'facilities': parts[5]
                            }
                            theaters.append(theater)
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return theaters
def read_showtimes():
    showtimes = []
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    if not os.path.exists(path):
        return showtimes
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        try:
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
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return showtimes
def read_seats():
    seats = []
    path = os.path.join(DATA_DIR, 'seats.txt')
    if not os.path.exists(path):
        return seats
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        try:
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
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return seats
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        try:
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
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return bookings
def read_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        try:
                            genre = {
                                'genre_id': int(parts[0]),
                                'genre_name': parts[1],
                                'description': parts[2]
                            }
                            genres.append(genre)
                        except (ValueError, IndexError):
                            continue
    except Exception:
        pass
    return genres
@app.route('/')
def dashboard():
    movies = read_movies()
    # For featured movies, pick top 3 by rating descending
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    # Upcoming releases: movies with release_date in future or recent (for simplicity, next 3 by release_date ascending)
    today = datetime.today().date()
    upcoming = [m for m in movies if datetime.strptime(m['release_date'], '%Y-%m-%d').date() >= today]
    upcoming_releases = sorted(upcoming, key=lambda m: m['release_date'])[:3]
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)
@app.route('/catalog')
def movie_catalog():
    movies = read_movies()
    genres = read_genres()
    search_query = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')
    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower() or search_query in m['genre'].lower()]
    if genre_filter and genre_filter != 'All':
        filtered_movies = [m for m in filtered_movies if m['genre'] == genre_filter]
    return render_template('movie_catalog.html', movies=filtered_movies, genres=genres, selected_genre=genre_filter, search_query=search_query)
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movies = read_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)
@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    showtimes = read_showtimes()
    theaters = read_theaters()
    # Filter showtimes for the movie
    movie_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    theater_filter = request.args.get('theater', '')
    date_filter = request.args.get('date', '')
    if theater_filter and theater_filter != 'All':
        # Find theater_id by name
        theater_ids = [t['theater_id'] for t in theaters if t['theater_name'] == theater_filter]
        if theater_ids:
            movie_showtimes = [s for s in movie_showtimes if s['theater_id'] in theater_ids]
    if date_filter:
        movie_showtimes = [s for s in movie_showtimes if s['showtime_date'] == date_filter]
    # Map theater_id to theater_name for display
    theater_dict = {t['theater_id']: t['theater_name'] for t in theaters}
    return render_template('showtime_selection.html', showtimes=movie_showtimes, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter, theater_dict=theater_dict, movie_id=movie_id)
@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtimes = read_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    seats = read_seats()
    # Filter seats for the theater and screen (assuming screen_id=1 for simplicity)
    theater_id = showtime['theater_id']
    screen_id = 1  # Assuming screen_id=1 as no screen info in showtime
    theater_seats = [s for s in seats if s['theater_id'] == theater_id and s['screen_id'] == screen_id]
    # Build seat map by rows and columns
    seat_map = {}
    for seat in theater_seats:
        row = seat['row']
        if row not in seat_map:
            seat_map[row] = []
        seat_map[row].append(seat)
    # Sort seats in each row by column
    for row in seat_map:
        seat_map[row] = sorted(seat_map[row], key=lambda s: s['column'])
    selected_seats = []
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            error = "Please select at least one seat."
            return render_template('seat_selection.html', showtime=showtime, seat_map=seat_map, selected_seats=selected_seats, error=error)
        # Redirect to booking confirmation with selected seats
        seats_str = ','.join(selected_seats)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=seats_str))
    return render_template('seat_selection.html', showtime=showtime, seat_map=seat_map, selected_seats=selected_seats)
@app.route('/booking_confirmation/<int:showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtimes = read_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    movies = read_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404
    seats_str = request.args.get('seats', '')
    selected_seats = seats_str.split(',') if seats_str else []
    total_price = len(selected_seats) * showtime['price']
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            error = "Please enter your name and email."
            return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price, error=error)
        # Save booking
        bookings = read_bookings()
        new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1
        booking_date = datetime.today().strftime('%Y-%m-%d')
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
        # Write back to bookings.txt
        path = os.path.join(DATA_DIR, 'bookings.txt')
        try:
            with open(path, 'a', encoding='utf-8') as f:
                seats_joined = ','.join(selected_seats)
                line = f"{new_booking_id}|{showtime_id}|{customer_name}|{customer_email}|{booking_date}|{total_price:.2f}|Confirmed|{seats_joined}\n"
                f.write(line)
        except Exception:
            # If writing fails, show error
            error = "Failed to save booking. Please try again."
            return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price, error=error)
        # Update seats status to Booked in seats.txt
        seats = read_seats()
        updated = False
        for seat in seats:
            seat_code = f"{seat['row']}{seat['column']}"
            if seat['theater_id'] == showtime['theater_id'] and seat_code in selected_seats and seat['status'] == 'Available':
                seat['status'] = 'Booked'
                updated = True
        if updated:
            # Rewrite seats.txt
            path_seats = os.path.join(DATA_DIR, 'seats.txt')
            try:
                with open(path_seats, 'w', encoding='utf-8') as f:
                    for seat in seats:
                        line = f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n"
                        f.write(line)
            except Exception:
                # If writing fails, ignore but log could be added
                pass
        # Update available seats in showtimes.txt
        showtimes = read_showtimes()
        for s in showtimes:
            if s['showtime_id'] == showtime_id:
                s['available_seats'] = max(0, s['available_seats'] - len(selected_seats))
        path_showtimes = os.path.join(DATA_DIR, 'showtimes.txt')
        try:
            with open(path_showtimes, 'w', encoding='utf-8') as f:
                for s in showtimes:
                    line = f"{s['showtime_id']}|{s['movie_id']}|{s['theater_id']}|{s['showtime_date']}|{s['showtime_time']}|{s['price']:.2f}|{s['available_seats']}\n"
                    f.write(line)
        except Exception:
            # If writing fails, ignore but log could be added
            pass
        return redirect(url_for('booking_history'))
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price)
@app.route('/bookings')
def booking_history():
    bookings = read_bookings()
    movies = read_movies()
    status_filter = request.args.get('status', 'All')
    filtered_bookings = bookings
    if status_filter != 'All':
        filtered_bookings = [b for b in bookings if b['status'] == status_filter]
    # Map movie_id to title
    movie_dict = {m['movie_id']: m['title'] for m in movies}
    return render_template('booking_history.html', bookings=filtered_bookings, movie_dict=movie_dict, status_filter=status_filter)
@app.route('/booking/<int:booking_id>')
def booking_details(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    movies = read_movies()
    showtimes = read_showtimes()
    movie = None
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == booking['showtime_id']:
            showtime = s
            break
    if showtime:
        for m in movies:
            if m['movie_id'] == showtime['movie_id']:
                movie = m
                break
    return render_template('booking_details.html', booking=booking, movie=movie, showtime=showtime)
@app.route('/theaters')
def theater_information():
    theaters = read_theaters()
    location_filter = request.args.get('location', '')
    filtered_theaters = theaters
    if location_filter and location_filter != 'All':
        filtered_theaters = [t for t in theaters if t['city'] == location_filter]
    # Get unique locations for filter dropdown
    locations = sorted(set(t['city'] for t in theaters))
    return render_template('theater_information.html', theaters=filtered_theaters, locations=locations, selected_location=location_filter)
if __name__ == '__main__':
    app.run(debug=True)