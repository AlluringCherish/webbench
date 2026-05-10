'''
Main backend application for RestaurantReservation web app.
Defines all routes including the root '/' route serving the Dashboard page,
ensuring compliance with the requirement that the website starts from the Dashboard.
Handles data loading from local text files and renders templates accordingly.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
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
                    if len(parts) == 8:
                        dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
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
def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 10:
                        reservation_id, username, guest_name, phone, email, party_size, date, time, special_requests, status = parts
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
def read_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 5:
                        waitlist_id, username, party_size, join_time, status = parts
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
def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        review_id, username, dish_id, rating, review_text, review_date = parts
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
    Route for the Dashboard page, the main hub of the application.
    Loads featured dishes (top rated), upcoming reservations for the user,
    and renders the dashboard template.
    '''
    menu = read_menu()
    # Featured dishes: top 3 by avg_rating descending
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    reservations = read_reservations()
    # Upcoming reservations for logged in user, sorted by date and time
    upcoming_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER and r['status'] == 'Upcoming']
    upcoming_reservations.sort(key=lambda r: (r['date'], r['time']))
    users = read_users()
    user_info = users.get(LOGGED_IN_USER, {'full_name': LOGGED_IN_USER})
    return render_template('dashboard.html',
                           username=LOGGED_IN_USER,
                           full_name=user_info.get('full_name', LOGGED_IN_USER),
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)
@app.route('/menu')
def menu_page():
    '''
    Route for the Menu page.
    Displays all menu items.
    '''
    menu = read_menu()
    return render_template('menu.html', menu=menu)
@app.route('/dish/<dish_id>')
def dish_details(dish_id):
    '''
    Route for Dish Details page.
    Displays detailed info about a specific dish.
    '''
    menu = read_menu()
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
    users = read_users()
    user_info = users.get(LOGGED_IN_USER, {})
    if request.method == 'POST':
        guest_name = request.form.get('guest-name')
        party_size = request.form.get('party-size')
        reservation_date = request.form.get('reservation-date')
        reservation_time = request.form.get('reservation-time', '18:00')  # default time if not provided
        special_requests = request.form.get('special-requests', '')
        phone = user_info.get('phone', '')
        email = user_info.get('email', '')
        # Generate new reservation_id
        reservations = read_reservations()
        if reservations:
            new_id = str(int(max(r['reservation_id'] for r in reservations)) + 1)
        else:
            new_id = '1'
        new_reservation = f"{new_id}|{LOGGED_IN_USER}|{guest_name}|{phone}|{email}|{party_size}|{reservation_date}|{reservation_time}|{special_requests}|Upcoming\n"
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'a') as f:
            f.write(new_reservation)
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')
@app.route('/my_reservations')
def my_reservations():
    '''
    Route for My Reservations page.
    Displays all reservations made by the logged in user.
    '''
    reservations = read_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USER]
    user_reservations.sort(key=lambda r: (r['date'], r['time']))
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    '''
    Route to cancel a reservation by reservation_id.
    Only upcoming reservations can be cancelled.
    '''
    reservations = read_reservations()
    updated = False
    with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
        for r in reservations:
            if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USER and r['status'] == 'Upcoming':
                r['status'] = 'Cancelled'
                updated = True
            line = '|'.join([
                r['reservation_id'], r['username'], r['guest_name'], r['phone'], r['email'],
                str(r['party_size']), r['date'], r['time'], r['special_requests'], r['status']
            ]) + '\n'
            f.write(line)
    return redirect(url_for('my_reservations'))
@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    '''
    Route for Waitlist page.
    GET: display waitlist status and join form.
    POST: join waitlist.
    '''
    waitlist = read_waitlist()
    user_waitlist = [w for w in waitlist if w['username'] == LOGGED_IN_USER and w['status'] == 'Active']
    user_position = None
    if user_waitlist:
        # Sort waitlist by join_time ascending
        active_waitlist = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda w: w['join_time'])
        for idx, w in enumerate(active_waitlist, start=1):
            if w['username'] == LOGGED_IN_USER:
                user_position = idx
                break
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        waitlist_ids = [int(w['waitlist_id']) for w in waitlist] if waitlist else []
        new_id = str(max(waitlist_ids) + 1) if waitlist_ids else '1'
        new_entry = f"{new_id}|{LOGGED_IN_USER}|{party_size}|{join_time}|Active\n"
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'a') as f:
            f.write(new_entry)
        return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_position=user_position)
@app.route('/my_reviews')
def my_reviews():
    '''
    Route for My Reviews page.
    Displays all reviews written by the logged in user.
    '''
    reviews = read_reviews()
    menu = read_menu()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USER]
    # Add dish name to each review
    dish_dict = {d['dish_id']: d['name'] for d in menu}
    for r in user_reviews:
        r['dish_name'] = dish_dict.get(r['dish_id'], 'Unknown Dish')
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    '''
    Route for Write Review page.
    GET: display form.
    POST: submit review.
    '''
    menu = read_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text')
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews = read_reviews()
        review_ids = [int(r['review_id']) for r in reviews] if reviews else []
        new_id = str(max(review_ids) + 1) if review_ids else '1'
        new_review = f"{new_id}|{LOGGED_IN_USER}|{dish_id}|{rating}|{review_text}|{review_date}\n"
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a') as f:
            f.write(new_review)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', menu=menu)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    '''
    Route for User Profile page.
    GET: display profile info.
    POST: update email.
    '''
    users = read_users()
    user_info = users.get(LOGGED_IN_USER, {'email': '', 'phone': '', 'full_name': LOGGED_IN_USER})
    if request.method == 'POST':
        new_email = request.form.get('profile-email')
        # Update users.txt with new email
        updated_users = []
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, email, phone, full_name = line.split('|')
                    if username == LOGGED_IN_USER:
                        email = new_email
                    updated_users.append(f"{username}|{email}|{phone}|{full_name}\n")
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
            f.writelines(updated_users)
        return redirect(url_for('profile'))
    return render_template('profile.html', username=LOGGED_IN_USER, email=user_info.get('email', ''))
if __name__ == '__main__':
    app.run(debug=True)