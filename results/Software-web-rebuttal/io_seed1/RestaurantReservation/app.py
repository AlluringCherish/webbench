'''
Backend implementation for RestaurantReservation web application.
Implements Flask web server with routing for all nine pages,
business logic for user requests, and file operations on local
pipe-delimited text files in the 'data' directory.
The website starts from the Dashboard page at route '/'.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages
DATA_DIR = 'data'
# Helper functions for file operations and data parsing
def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
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
            if line:
                parts = line.split('|')
                if len(parts) == 8:
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
            if line:
                parts = line.split('|')
                if len(parts) == 10:
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
            if line:
                parts = line.split('|')
                if len(parts) == 5:
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
            if line:
                parts = line.split('|')
                if len(parts) == 6:
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
# For simplicity, assume a fixed logged-in user for demonstration
# In real app, implement authentication and session management
LOGGED_IN_USERNAME = 'john_diner'
# Get user info for logged-in user
def get_logged_in_user():
    users = read_users()
    return users.get(LOGGED_IN_USERNAME)
# Routes implementation
@app.route('/')
def dashboard():
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    # Featured dishes: top 3 by avg_rating descending
    menu = read_menu()
    featured_dishes = sorted(menu.values(), key=lambda d: d['avg_rating'], reverse=True)[:3]
    # Upcoming reservations for user (status == Upcoming), sorted by date/time ascending
    reservations = read_reservations()
    upcoming = [r for r in reservations.values() if r['username'] == LOGGED_IN_USERNAME and r['status'] == 'Upcoming']
    upcoming_sorted = sorted(upcoming, key=lambda r: (r['date'], r['time']))
    return render_template('dashboard.html',
                           username=user['full_name'],
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_sorted)
@app.route('/menu')
def menu():
    menu = read_menu()
    # Pass all menu items to template
    return render_template('menu.html', menu_items=menu.values())
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    menu = read_menu()
    dish = menu.get(dish_id)
    if not dish:
        flash("Dish not found.")
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    if request.method == 'POST':
        guest_name = request.form.get('guest-name', '').strip()
        party_size = request.form.get('party-size')
        reservation_date = request.form.get('reservation-date')
        reservation_time = request.form.get('reservation-time', '18:00')  # Default time if not provided
        special_requests = request.form.get('special-requests', '').strip()
        # Validate inputs
        if not guest_name:
            flash("Guest name is required.")
            return redirect(url_for('make_reservation'))
        if not party_size or not party_size.isdigit() or not (1 <= int(party_size) <= 10):
            flash("Party size must be between 1 and 10.")
            return redirect(url_for('make_reservation'))
        if not reservation_date:
            flash("Reservation date is required.")
            return redirect(url_for('make_reservation'))
        if not reservation_time:
            flash("Reservation time is required.")
            return redirect(url_for('make_reservation'))
        # Generate new reservation_id
        reservations = read_reservations()
        if reservations:
            max_id = max(int(rid) for rid in reservations.keys())
            new_id = str(max_id + 1)
        else:
            new_id = '1'
        new_reservation = {
            'reservation_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'guest_name': guest_name,
            'phone': user['phone'],
            'email': user['email'],
            'party_size': int(party_size),
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
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    reservations = read_reservations()
    user_reservations = [r for r in reservations.values() if r['username'] == LOGGED_IN_USERNAME]
    user_reservations_sorted = sorted(user_reservations, key=lambda r: (r['date'], r['time']))
    if request.method == 'POST':
        # Cancel reservation
        cancel_id = request.form.get('cancel_reservation_id')
        if cancel_id and cancel_id in reservations:
            res = reservations[cancel_id]
            if res['username'] == LOGGED_IN_USERNAME and res['status'] == 'Upcoming':
                res['status'] = 'Cancelled'
                write_reservations(reservations)
                flash(f"Reservation {cancel_id} cancelled.")
            else:
                flash("Cannot cancel this reservation.")
        else:
            flash("Invalid reservation ID.")
        return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations_sorted)
@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    waitlist = read_waitlist()
    # Filter active waitlist entries for user
    user_waitlist = [w for w in waitlist.values() if w['username'] == LOGGED_IN_USERNAME and w['status'] == 'Active']
    user_position = None
    if user_waitlist:
        # Sort all active waitlist by join_time ascending
        active_waitlist = sorted([w for w in waitlist.values() if w['status'] == 'Active'], key=lambda w: w['join_time'])
        # Find position of user's first active waitlist entry
        first_user_entry = user_waitlist[0]
        for idx, w in enumerate(active_waitlist, start=1):
            if w['waitlist_id'] == first_user_entry['waitlist_id']:
                user_position = idx
                break
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        if not party_size or not party_size.isdigit() or int(party_size) < 1:
            flash("Please select a valid party size.")
            return redirect(url_for('waitlist'))
        # Generate new waitlist_id
        if waitlist:
            max_id = max(int(wid) for wid in waitlist.keys())
            new_id = str(max_id + 1)
        else:
            new_id = '1'
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {
            'waitlist_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'party_size': int(party_size),
            'join_time': join_time,
            'status': 'Active'
        }
        waitlist[new_id] = new_entry
        write_waitlist(waitlist)
        flash("You have joined the waitlist.")
        return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_position=user_position)
@app.route('/my_reviews')
def my_reviews():
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    reviews = read_reviews()
    menu = read_menu()
    user_reviews = [r for r in reviews.values() if r['username'] == LOGGED_IN_USERNAME]
    # Attach dish name to each review
    for r in user_reviews:
        dish = menu.get(r['dish_id'])
        r['dish_name'] = dish['name'] if dish else 'Unknown Dish'
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    user = get_logged_in_user()
    if not user:
        flash("User not found.")
        return "User not found", 404
    menu = read_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not dish_id or dish_id not in menu:
            flash("Please select a valid dish.")
            return redirect(url_for('write_review'))
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            flash("Please select a rating between 1 and 5.")
            return redirect(url_for('write_review'))
        if not review_text:
            flash("Review text cannot be empty.")
            return redirect(url_for('write_review'))
        reviews = read_reviews()
        if reviews:
            max_id = max(int(rid) for rid in reviews.keys())
            new_id = str(max_id + 1)
        else:
            new_id = '1'
        review_date = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'dish_id': dish_id,
            'rating': int(rating),
            'review_text': review_text,
            'review_date': review_date
        }
        reviews[new_id] = new_review
        write_reviews(reviews)
        flash("Review submitted successfully.")
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu_items=menu.values())
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        flash("User not found.")
        return "User not found", 404
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash("Email cannot be empty.")
            return redirect(url_for('profile'))
        # Update email
        user['email'] = email
        users[LOGGED_IN_USERNAME] = user
        write_users(users)
        flash("Profile updated successfully.")
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)
# Navigation routes for buttons that refresh or redirect to dashboard or other pages
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
    app.run(host='127.0.0.1', port=5000, debug=True)