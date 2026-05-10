'''
Main backend application for RestaurantReservation web application.
Defines routes for all pages, including the root '/' route serving the Dashboard page.
Handles data loading from local text files and renders templates accordingly.
Ensures route names are consistent and intuitive for frontend navigation.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, email, phone, full_name = line.split('|')
                    users[username] = {
                        'email': email,
                        'phone': phone,
                        'full_name': full_name
                    }
    except FileNotFoundError:
        pass
    return users
def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    dish_id, name, category, price, description, ingredients, dietary, avg_rating = line.split('|')
                    menu.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': float(price),
                        'description': description,
                        'ingredients': ingredients.split(','),
                        'dietary': dietary,
                        'avg_rating': float(avg_rating)
                    })
    except FileNotFoundError:
        pass
    return menu
def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    (reservation_id, username, guest_name, phone, email, party_size, date, time, special_requests, status) = line.split('|')
                    reservations.append({
                        'reservation_id': reservation_id,
                        'username': username,
                        'guest_name': guest_name,
                        'phone': phone,
                        'email': email,
                        'party_size': int(party_size),
                        'date': date,
                        'time': time,
                        'special_requests': special_requests,
                        'status': status
                    })
    except FileNotFoundError:
        pass
    return reservations
def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    waitlist_id, username, party_size, join_time, status = line.split('|')
                    waitlist.append({
                        'waitlist_id': waitlist_id,
                        'username': username,
                        'party_size': int(party_size),
                        'join_time': join_time,
                        'status': status
                    })
    except FileNotFoundError:
        pass
    return waitlist
def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    review_id, username, dish_id, rating, review_text, review_date = line.split('|')
                    reviews.append({
                        'review_id': review_id,
                        'username': username,
                        'dish_id': dish_id,
                        'rating': int(rating),
                        'review_text': review_text,
                        'review_date': review_date
                    })
    except FileNotFoundError:
        pass
    return reviews
# For demonstration, assume logged in user is 'john_diner'
LOGGED_IN_USER = 'john_diner'
@app.route('/')
def dashboard():
    '''
    Route for the root URL '/' serving the Dashboard page.
    Loads featured dishes and upcoming reservations for the logged-in user.
    '''
    users = load_users()
    menu = load_menu()
    reservations = load_reservations()
    user_info = users.get(LOGGED_IN_USER, {})
    welcome_name = user_info.get('full_name', LOGGED_IN_USER)
    # Featured dishes: top 3 by avg_rating
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    # Upcoming reservations for user
    upcoming_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER and r['status'] == 'Upcoming']
    return render_template('dashboard.html',
                           username=welcome_name,
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)
@app.route('/menu')
def menu_page():
    '''
    Route for the Menu page.
    Displays all menu items.
    '''
    menu = load_menu()
    return render_template('menu.html', menu=menu)
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    '''
    Route for Dish Details page.
    Displays detailed info for a specific dish.
    '''
    menu = load_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    '''
    Route for Make Reservation page.
    GET: display form.
    POST: process reservation submission.
    '''
    users = load_users()
    user_info = users.get(LOGGED_IN_USER, {})
    if request.method == 'POST':
        guest_name = request.form.get('guest-name')
        party_size = request.form.get('party-size')
        reservation_date = request.form.get('reservation-date')
        # For simplicity, time and special requests omitted here
        # Generate new reservation_id
        reservations = load_reservations()
        new_id = str(max([int(r['reservation_id']) for r in reservations], default=0) + 1)
        new_reservation = {
            'reservation_id': new_id,
            'username': LOGGED_IN_USER,
            'guest_name': guest_name,
            'phone': user_info.get('phone', ''),
            'email': user_info.get('email', ''),
            'party_size': int(party_size),
            'date': reservation_date,
            'time': '18:00',  # default time for demo
            'special_requests': '',
            'status': 'Upcoming'
        }
        # Append to file
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'a') as f:
            f.write('|'.join([
                new_reservation['reservation_id'],
                new_reservation['username'],
                new_reservation['guest_name'],
                new_reservation['phone'],
                new_reservation['email'],
                str(new_reservation['party_size']),
                new_reservation['date'],
                new_reservation['time'],
                new_reservation['special_requests'],
                new_reservation['status']
            ]) + '\n')
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')
@app.route('/my_reservations')
def my_reservations():
    '''
    Route for My Reservations page.
    Displays all reservations made by the logged-in user.
    '''
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER]
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    '''
    Route to cancel a reservation by reservation_id.
    '''
    reservations = load_reservations()
    updated_reservations = []
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USER:
            r['status'] = 'Cancelled'
        updated_reservations.append(r)
    # Write back updated reservations
    with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
        for r in updated_reservations:
            f.write('|'.join([
                r['reservation_id'],
                r['username'],
                r['guest_name'],
                r['phone'],
                r['email'],
                str(r['party_size']),
                r['date'],
                r['time'],
                r['special_requests'],
                r['status']
            ]) + '\n')
    return redirect(url_for('my_reservations'))
@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    '''
    Route for Waitlist page.
    GET: display waitlist status and join form.
    POST: join waitlist.
    '''
    waitlist = load_waitlist()
    user_position = None
    active_waitlist = [w for w in waitlist if w['status'] == 'Active']
    active_waitlist_sorted = sorted(active_waitlist, key=lambda w: datetime.strptime(w['join_time'], '%Y-%m-%d %H:%M:%S'))
    for idx, w in enumerate(active_waitlist_sorted, start=1):
        if w['username'] == LOGGED_IN_USER:
            user_position = idx
            break
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        # Generate new waitlist_id
        new_id = str(max([int(w['waitlist_id']) for w in waitlist], default=0) + 1)
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {
            'waitlist_id': new_id,
            'username': LOGGED_IN_USER,
            'party_size': int(party_size),
            'join_time': join_time,
            'status': 'Active'
        }
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'a') as f:
            f.write('|'.join([
                new_entry['waitlist_id'],
                new_entry['username'],
                str(new_entry['party_size']),
                new_entry['join_time'],
                new_entry['status']
            ]) + '\n')
        return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_position=user_position)
@app.route('/my_reviews')
def my_reviews():
    '''
    Route for My Reviews page.
    Displays all reviews written by the logged-in user.
    '''
    reviews = load_reviews()
    menu = load_menu()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USER]
    # Add dish name to each review
    for r in user_reviews:
        dish = next((d for d in menu if d['dish_id'] == r['dish_id']), None)
        r['dish_name'] = dish['name'] if dish else 'Unknown Dish'
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    '''
    Route for Write Review page.
    GET: display form.
    POST: submit review.
    '''
    menu = load_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text')
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews = load_reviews()
        new_id = str(max([int(r['review_id']) for r in reviews], default=0) + 1)
        new_review = {
            'review_id': new_id,
            'username': LOGGED_IN_USER,
            'dish_id': dish_id,
            'rating': int(rating),
            'review_text': review_text,
            'review_date': review_date
        }
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a') as f:
            f.write('|'.join([
                new_review['review_id'],
                new_review['username'],
                new_review['dish_id'],
                str(new_review['rating']),
                new_review['review_text'],
                new_review['review_date']
            ]) + '\n')
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu=menu)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    '''
    Route for User Profile page.
    GET: display profile info.
    POST: update email.
    '''
    users = load_users()
    user_info = users.get(LOGGED_IN_USER, {})
    if request.method == 'POST':
        new_email = request.form.get('profile-email')
        # Update users.txt
        updated_users = []
        for username, info in users.items():
            if username == LOGGED_IN_USER:
                info['email'] = new_email
            updated_users.append((username, info))
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
            for username, info in updated_users:
                f.write('|'.join([
                    username,
                    info['email'],
                    info['phone'],
                    info['full_name']
                ]) + '\n')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', username=LOGGED_IN_USER, email=user_info.get('email', ''))
if __name__ == '__main__':
    app.run(debug=True)