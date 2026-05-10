'''
Main backend Python file implementing the RestaurantReservation web application using Flask.
Handles routing for all nine pages, processes user inputs, reads from and writes to local text files in the 'data' directory,
and manages application logic including user sessions, data loading, and updates.
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management, in production use a secure key
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            username, email, phone, full_name = line.split('|')
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'full_name': full_name
            }
    return users
def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([u['username'], u['email'], u['phone'], u['full_name']])
            f.write(line + '\n')
def read_menu():
    menu = {}
    path = os.path.join(DATA_DIR, 'menu.txt')
    if not os.path.exists(path):
        return menu
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            dish_id = parts[0]
            menu[dish_id] = {
                'dish_id': dish_id,
                'name': parts[1],
                'category': parts[2],
                'price': float(parts[3]),
                'description': parts[4],
                'ingredients': parts[5].split(',') if parts[5] else [],
                'dietary': parts[6],
                'avg_rating': float(parts[7])
            }
    return menu
def read_reservations():
    reservations = {}
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 10:
                continue
            reservation_id = parts[0]
            reservations[reservation_id] = {
                'reservation_id': reservation_id,
                'username': parts[1],
                'guest_name': parts[2],
                'phone': parts[3],
                'email': parts[4],
                'party_size': int(parts[5]),
                'date': parts[6],
                'time': parts[7],
                'special_requests': parts[8],
                'status': parts[9]
            }
    return reservations
def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = '|'.join([
                r['reservation_id'], r['username'], r['guest_name'], r['phone'], r['email'],
                str(r['party_size']), r['date'], r['time'], r['special_requests'], r['status']
            ])
            f.write(line + '\n')
def read_waitlist():
    waitlist = {}
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if not os.path.exists(path):
        return waitlist
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            waitlist_id = parts[0]
            waitlist[waitlist_id] = {
                'waitlist_id': waitlist_id,
                'username': parts[1],
                'party_size': int(parts[2]),
                'join_time': parts[3],
                'status': parts[4]
            }
    return waitlist
def write_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist.values():
            line = '|'.join([
                w['waitlist_id'], w['username'], str(w['party_size']), w['join_time'], w['status']
            ])
            f.write(line + '\n')
def read_reviews():
    reviews = {}
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            review_id = parts[0]
            reviews[review_id] = {
                'review_id': review_id,
                'username': parts[1],
                'dish_id': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                r['review_id'], r['username'], r['dish_id'], str(r['rating']), r['review_text'], r['review_date']
            ])
            f.write(line + '\n')
# Helper to get next ID for reservations, waitlist, reviews
def get_next_id(data_dict):
    if not data_dict:
        return '1'
    max_id = max(int(k) for k in data_dict.keys())
    return str(max_id + 1)
# Dummy login for demonstration: we assume user is logged in as 'john_diner'
# In real app, implement proper authentication
@app.before_request
def ensure_logged_in():
    if 'username' not in session:
        # For demo, auto-login as john_diner
        session['username'] = 'john_diner'
@app.route('/')
def dashboard():
    username = session['username']
    users = read_users()
    user = users.get(username)
    if not user:
        flash("User not found.")
        return "User not found", 404
    menu = read_menu()
    # Featured dishes: top 3 by avg_rating descending
    featured_dishes = sorted(menu.values(), key=lambda d: d['avg_rating'], reverse=True)[:3]
    reservations = read_reservations()
    # Upcoming reservations for user, sorted by date/time ascending
    upcoming_reservations = [r for r in reservations.values() if r['username'] == username and r['status'] == 'Upcoming']
    upcoming_reservations.sort(key=lambda r: (r['date'], r['time']))
    return render_template('dashboard.html',
                           username=username,
                           full_name=user['full_name'],
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)
@app.route('/menu')
def menu():
    menu = read_menu()
    # For filtering, we can get categories from menu items
    categories = sorted(set(d['category'] for d in menu.values()))
    return render_template('menu.html', menu=menu, categories=categories)
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    menu = read_menu()
    dish = menu.get(dish_id)
    if not dish:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    username = session['username']
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        guest_name = request.form.get('guest-name', '').strip()
        party_size = request.form.get('party-size')
        reservation_date = request.form.get('reservation-date')
        reservation_time = request.form.get('reservation-time', '19:00')  # Default time if not provided
        special_requests = request.form.get('special-requests', '').strip()
        # Validate inputs
        if not guest_name or not party_size or not reservation_date:
            flash("Please fill in all required fields.")
            return redirect(url_for('make_reservation'))
        try:
            party_size = int(party_size)
            if party_size < 1 or party_size > 10:
                flash("Party size must be between 1 and 10.")
                return redirect(url_for('make_reservation'))
        except ValueError:
            flash("Invalid party size.")
            return redirect(url_for('make_reservation'))
        # Validate date format
        try:
            datetime.strptime(reservation_date, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('make_reservation'))
        # Validate time format
        try:
            datetime.strptime(reservation_time, '%H:%M')
        except ValueError:
            flash("Invalid time format.")
            return redirect(url_for('make_reservation'))
        reservations = read_reservations()
        new_id = get_next_id(reservations)
        new_reservation = {
            'reservation_id': new_id,
            'username': username,
            'guest_name': guest_name,
            'phone': user['phone'],
            'email': user['email'],
            'party_size': party_size,
            'date': reservation_date,
            'time': reservation_time,
            'special_requests': special_requests,
            'status': 'Upcoming'
        }
        reservations[new_id] = new_reservation
        write_reservations(reservations)
        flash("Reservation made successfully.")
        return redirect(url_for('dashboard'))
    # GET request
    return render_template('make_reservation.html')
@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    username = session['username']
    reservations = read_reservations()
    user_reservations = [r for r in reservations.values() if r['username'] == username]
    user_reservations.sort(key=lambda r: (r['date'], r['time']))
    if request.method == 'POST':
        # Handle cancellation
        cancel_id = request.form.get('cancel_reservation_id')
        if cancel_id and cancel_id in reservations:
            reservation = reservations[cancel_id]
            if reservation['username'] == username and reservation['status'] == 'Upcoming':
                reservation['status'] = 'Cancelled'
                write_reservations(reservations)
                flash("Reservation cancelled.")
            else:
                flash("Cannot cancel this reservation.")
        return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = session['username']
    waitlist = read_waitlist()
    # Find user's active waitlist entry if any
    user_entry = None
    active_entries = [w for w in waitlist.values() if w['status'] == 'Active']
    active_entries.sort(key=lambda w: w['join_time'])
    for w in active_entries:
        if w['username'] == username:
            user_entry = w
            break
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        if not party_size:
            flash("Please select party size.")
            return redirect(url_for('waitlist'))
        try:
            party_size = int(party_size)
            if party_size < 1:
                flash("Invalid party size.")
                return redirect(url_for('waitlist'))
        except ValueError:
            flash("Invalid party size.")
            return redirect(url_for('waitlist'))
        if user_entry:
            flash("You are already in the waitlist.")
            return redirect(url_for('waitlist'))
        new_id = get_next_id(waitlist)
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        waitlist[new_id] = {
            'waitlist_id': new_id,
            'username': username,
            'party_size': party_size,
            'join_time': join_time,
            'status': 'Active'
        }
        write_waitlist(waitlist)
        flash("You have joined the waitlist.")
        return redirect(url_for('waitlist'))
    # Calculate user's position if in waitlist
    user_position = None
    if user_entry:
        # Position is 1-based index in active_entries
        user_position = active_entries.index(user_entry) + 1
    return render_template('waitlist.html', user_position=user_position)
@app.route('/my_reviews')
def my_reviews():
    username = session['username']
    reviews = read_reviews()
    menu = read_menu()
    user_reviews = [r for r in reviews.values() if r['username'] == username]
    # Add dish name to each review for display
    for r in user_reviews:
        dish = menu.get(r['dish_id'])
        r['dish_name'] = dish['name'] if dish else 'Unknown Dish'
    user_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    username = session['username']
    menu = read_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not dish_id or dish_id not in menu:
            flash("Please select a valid dish.")
            return redirect(url_for('write_review'))
        if not rating:
            flash("Please select a rating.")
            return redirect(url_for('write_review'))
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash("Rating must be between 1 and 5.")
                return redirect(url_for('write_review'))
        except ValueError:
            flash("Invalid rating.")
            return redirect(url_for('write_review'))
        if not review_text:
            flash("Please write a review.")
            return redirect(url_for('write_review'))
        reviews = read_reviews()
        new_id = get_next_id(reviews)
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews[new_id] = {
            'review_id': new_id,
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        write_reviews(reviews)
        flash("Review submitted successfully.")
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu=menu.values())
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session['username']
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash("Email cannot be empty.")
            return redirect(url_for('profile'))
        # Update email
        user['email'] = email
        users[username] = user
        write_users(users)
        flash("Profile updated successfully.")
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)
# Additional routes for navigation buttons that refresh or redirect
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_menu')
def back_to_menu():
    return redirect(url_for('menu'))
@app.route('/back_to_reviews')
def back_to_reviews():
    return redirect(url_for('my_reviews'))
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)