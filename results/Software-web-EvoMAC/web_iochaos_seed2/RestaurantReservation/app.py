'''
Main backend application for RestaurantReservation web application.
Defines all routes including the root '/' route serving the Dashboard page,
ensuring the website starts from the Dashboard as per requirements.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_users():
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
def read_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    dish = {
                        'dish_id': parts[0],
                        'name': parts[1],
                        'category': parts[2],
                        'price': parts[3],
                        'description': parts[4],
                        'ingredients': parts[5],
                        'dietary': parts[6],
                        'avg_rating': parts[7]
                    }
                    menu.append(dish)
    except FileNotFoundError:
        pass
    return menu
def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    reservation = {
                        'reservation_id': parts[0],
                        'username': parts[1],
                        'guest_name': parts[2],
                        'phone': parts[3],
                        'email': parts[4],
                        'party_size': parts[5],
                        'date': parts[6],
                        'time': parts[7],
                        'special_requests': parts[8],
                        'status': parts[9]
                    }
                    reservations.append(reservation)
    except FileNotFoundError:
        pass
    return reservations
def read_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    entry = {
                        'waitlist_id': parts[0],
                        'username': parts[1],
                        'party_size': parts[2],
                        'join_time': parts[3],
                        'status': parts[4]
                    }
                    waitlist.append(entry)
    except FileNotFoundError:
        pass
    return waitlist
def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    review = {
                        'review_id': parts[0],
                        'username': parts[1],
                        'dish_id': parts[2],
                        'rating': parts[3],
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    except FileNotFoundError:
        pass
    return reviews
# For demonstration, assume logged in user is 'john_diner'
LOGGED_IN_USER = 'john_diner'
@app.route('/')
def dashboard():
    '''
    Route for the Dashboard page, the starting page of the website.
    Displays welcome message, featured dishes, upcoming reservations,
    and navigation buttons to other pages.
    '''
    users = read_users()
    menu = read_menu()
    reservations = read_reservations()
    user = users.get(LOGGED_IN_USER, {})
    username = LOGGED_IN_USER
    full_name = user.get('full_name', username)
    # Featured dishes: top 3 by avg_rating descending
    featured_dishes = sorted(menu, key=lambda d: float(d['avg_rating']), reverse=True)[:3]
    # Upcoming reservations for user
    today = datetime.date.today()
    upcoming_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER and r['status'] == 'Upcoming' and r['date'] >= today.isoformat()]
    return render_template('dashboard.html',
                           username=username,
                           full_name=full_name,
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)
@app.route('/menu')
def menu_page():
    '''
    Route for the Menu page.
    Displays all menu items with filtering and navigation back to dashboard.
    '''
    menu = read_menu()
    return render_template('menu.html', menu=menu)
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    '''
    Route for Dish Details page.
    Displays detailed information about a specific dish.
    '''
    menu = read_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    if not dish:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    '''
    Route for Make Reservation page.
    GET: Show reservation form.
    POST: Process reservation submission and save to file.
    '''
    users = read_users()
    user = users.get(LOGGED_IN_USER, {})
    if request.method == 'POST':
        guest_name = request.form.get('guest-name')
        party_size = request.form.get('party-size')
        reservation_date = request.form.get('reservation-date')
        reservation_time = request.form.get('reservation-time', '18:00')  # default time if not provided
        special_requests = request.form.get('special-requests', '')
        phone = user.get('phone', '')
        email = user.get('email', '')
        # Generate new reservation_id
        reservations = read_reservations()
        if reservations:
            new_id = str(int(reservations[-1]['reservation_id']) + 1)
        else:
            new_id = '1'
        new_reservation = '|'.join([
            new_id,
            LOGGED_IN_USER,
            guest_name,
            phone,
            email,
            party_size,
            reservation_date,
            reservation_time,
            special_requests,
            'Upcoming'
        ])
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'a') as f:
            f.write(new_reservation + '\n')
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')
@app.route('/my_reservations')
def my_reservations():
    '''
    Route for My Reservations page.
    Displays all reservations made by the logged-in user.
    '''
    reservations = read_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER]
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    '''
    Route to cancel a reservation by reservation_id.
    Updates the status to 'Cancelled' in the reservations file.
    '''
    reservations = read_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USER and r['status'] == 'Upcoming':
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
    waitlist = read_waitlist()
    user_entry = next((w for w in waitlist if w['username'] == LOGGED_IN_USER and w['status'] == 'Active'), None)
    position = None
    if user_entry:
        active_waitlist = [w for w in waitlist if w['status'] == 'Active']
        active_waitlist.sort(key=lambda w: w['join_time'])
        position = active_waitlist.index(user_entry) + 1
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        if not user_entry:
            # Generate new waitlist_id
            if waitlist:
                new_id = str(int(waitlist[-1]['waitlist_id']) + 1)
            else:
                new_id = '1'
            join_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = '|'.join([
                new_id,
                LOGGED_IN_USER,
                party_size,
                join_time,
                'Active'
            ])
            with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'a') as f:
                f.write(new_entry + '\n')
            return redirect(url_for('waitlist'))
    return render_template('waitlist.html', position=position)
@app.route('/my_reviews')
def my_reviews():
    '''
    Route for My Reviews page.
    Displays all reviews written by the logged-in user.
    '''
    reviews = read_reviews()
    menu = read_menu()
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
    GET: Show form to write a review.
    POST: Save the review to file.
    '''
    menu = read_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text')
        review_date = datetime.date.today().isoformat()
        reviews = read_reviews()
        if reviews:
            new_id = str(int(reviews[-1]['review_id']) + 1)
        else:
            new_id = '1'
        new_review = '|'.join([
            new_id,
            LOGGED_IN_USER,
            dish_id,
            rating,
            review_text,
            review_date
        ])
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a') as f:
            f.write(new_review + '\n')
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu=menu)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    '''
    Route for User Profile page.
    GET: Show profile info.
    POST: Update email in users file.
    '''
    users = read_users()
    user = users.get(LOGGED_IN_USER, {})
    if request.method == 'POST':
        new_email = request.form.get('profile-email')
        if new_email:
            user['email'] = new_email
            # Update users.txt
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
                for username, info in users.items():
                    line = '|'.join([username, info['email'], info['phone'], info['full_name']])
                    f.write(line + '\n')
        return redirect(url_for('profile'))
    return render_template('profile.html', username=LOGGED_IN_USER, email=user.get('email', ''))
if __name__ == '__main__':
    app.run(debug=True)