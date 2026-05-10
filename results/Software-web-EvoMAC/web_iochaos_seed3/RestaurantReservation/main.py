'''
Main Flask application for RestaurantReservation web application.
Defines all routes including the root '/' route serving the Dashboard page.
Ensures all navigation uses Flask routing with url_for for consistent navigation.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Helper functions to load data from text files
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
                        'price': price,
                        'description': description,
                        'ingredients': ingredients,
                        'dietary': dietary,
                        'avg_rating': avg_rating
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
                        'party_size': party_size,
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
                        'party_size': party_size,
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
                        'rating': rating,
                        'review_text': review_text,
                        'review_date': review_date
                    })
    except FileNotFoundError:
        pass
    return reviews
# For demonstration, we assume a logged-in user 'john_diner'
current_user = 'john_diner'
@app.route('/')
def dashboard():
    '''
    Route for the Dashboard page, the main hub of the application.
    Displays welcome message, featured dishes, upcoming reservations, and navigation buttons.
    '''
    users = load_users()
    menu = load_menu()
    reservations = load_reservations()
    user_info = users.get(current_user, {})
    # Featured dishes: top 3 by avg_rating descending
    featured_dishes = sorted(menu, key=lambda d: float(d['avg_rating']), reverse=True)[:3]
    # Upcoming reservations for current user
    upcoming_reservations = [r for r in reservations if r['username'] == current_user and r['status'] == 'Upcoming']
    return render_template('dashboard.html',
                           username=current_user,
                           full_name=user_info.get('full_name', ''),
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)
@app.route('/menu')
def menu():
    '''
    Route for the Menu page.
    Displays all menu items with filtering and navigation back to dashboard.
    '''
    menu = load_menu()
    return render_template('menu.html', menu=menu)
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    '''
    Route for Dish Details page.
    Displays detailed information about a specific dish.
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
    GET: Show reservation form.
    POST: Process reservation submission and save to file.
    '''
    users = load_users()
    user_info = users.get(current_user, {})
    if request.method == 'POST':
        guest_name = request.form.get('guest-name', '').strip()
        party_size = request.form.get('party-size', '').strip()
        reservation_date = request.form.get('reservation-date', '').strip()
        reservation_time = request.form.get('reservation-time', '').strip()
        special_requests = request.form.get('special-requests', '').strip()
        # Validate required fields
        if not party_size or not reservation_date or not reservation_time:
            # Could add flash message or error handling here
            return render_template('make_reservation.html', error="Please fill in all required fields.")
        # Generate new reservation_id
        reservations = load_reservations()
        if reservations:
            new_id = str(int(max(r['reservation_id'] for r in reservations)) + 1)
        else:
            new_id = '1'
        # Save new reservation
        line = '|'.join([
            new_id,
            current_user,
            guest_name if guest_name else user_info.get('full_name', ''),
            user_info.get('phone', ''),
            user_info.get('email', ''),
            party_size,
            reservation_date,
            reservation_time,
            special_requests,
            'Upcoming'
        ])
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'a') as f:
            f.write(line + '\n')
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')
@app.route('/my_reservations')
def my_reservations():
    '''
    Route for My Reservations page.
    Displays all reservations made by the current user.
    '''
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == current_user]
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    '''
    Route to cancel a reservation by reservation_id.
    Updates the status to 'Cancelled' in the reservations file.
    '''
    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == current_user and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
            for r in reservations:
                line = '|'.join([
                    r['reservation_id'], r['username'], r['guest_name'], r['phone'], r['email'],
                    r['party_size'], r['date'], r['time'], r['special_requests'], r['status']
                ])
                f.write(line + '\n')
    return redirect(url_for('my_reservations'))
@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    '''
    Route for Waitlist page.
    GET: Show waitlist form and current position.
    POST: Add user to waitlist.
    '''
    waitlist = load_waitlist()
    user_waitlist = [w for w in waitlist if w['username'] == current_user and w['status'] == 'Active']
    user_position = None
    if user_waitlist:
        # Sort waitlist by join_time ascending
        active_waitlist = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda x: x['join_time'])
        for idx, w in enumerate(active_waitlist, start=1):
            if w['username'] == current_user:
                user_position = idx
                break
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size', '').strip()
        if not party_size:
            return render_template('waitlist.html', user_position=user_position, error="Please select party size.")
        if not user_waitlist:
            # Generate new waitlist_id
            if waitlist:
                new_id = str(int(max(w['waitlist_id'] for w in waitlist)) + 1)
            else:
                new_id = '1'
            join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            line = '|'.join([new_id, current_user, party_size, join_time, 'Active'])
            with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'a') as f:
                f.write(line + '\n')
            return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_position=user_position)
@app.route('/my_reviews')
def my_reviews():
    '''
    Route for My Reviews page.
    Displays all reviews written by the current user.
    '''
    reviews = load_reviews()
    menu = load_menu()
    user_reviews = [r for r in reviews if r['username'] == current_user]
    # Add dish name to each review
    for r in user_reviews:
        dish = next((d for d in menu if d['dish_id'] == r['dish_id']), None)
        r['dish_name'] = dish['name'] if dish else 'Unknown Dish'
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    '''
    Route for Write Review page.
    GET: Show form to write a review.
    POST: Save the review to file.
    '''
    menu = load_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish', '').strip()
        rating = request.form.get('rating-input', '').strip()
        review_text = request.form.get('review-text', '').strip()
        if not dish_id or not rating or not review_text:
            return render_template('write_review.html', menu=menu, error="Please fill in all fields.")
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews = load_reviews()
        if reviews:
            new_id = str(int(max(r['review_id'] for r in reviews)) + 1)
        else:
            new_id = '1'
        line = '|'.join([new_id, current_user, dish_id, rating, review_text, review_date])
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a') as f:
            f.write(line + '\n')
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu=menu)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    '''
    Route for User Profile page.
    GET: Show profile info.
    POST: Update email in users.txt.
    '''
    users = load_users()
    user_info = users.get(current_user, {})
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email:
            users[current_user]['email'] = new_email
            # Rewrite users.txt
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
                for username, info in users.items():
                    line = '|'.join([username, info['email'], info['phone'], info['full_name']])
                    f.write(line + '\n')
            return redirect(url_for('profile'))
    return render_template('profile.html', username=current_user, email=user_info.get('email', ''))
if __name__ == '__main__':
    app.run(debug=True)