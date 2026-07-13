from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions to read and write pipe-delimited data

def read_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        if not lines or lines == ['']:
            return []
        return [line.split('|') for line in lines]

def write_file(filename, rows):
    path = os.path.join(DATA_DIR, filename)
    lines = ['|'.join(str(field) for field in row) for row in rows]
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read users data into a dict by username

def get_users_dict():
    users = read_file('users.txt')
    users_dict = {}
    for u in users:
        if len(u) == 4:
            username, email, phone, full_name = u
            users_dict[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'full_name': full_name
            }
    return users_dict

# Read menu items as list of dicts

def get_menu_items():
    menu_raw = read_file('menu.txt')
    menu_items = []
    for row in menu_raw:
        if len(row) == 8:
            dish_id, name, category, price, description, ingredients, dietary, avg_rating = row
            menu_items.append({
                'dish_id': int(dish_id),
                'name': name,
                'category': category,
                'price': float(price),
                'description': description,
                'ingredients': ingredients,
                'dietary': dietary,
                'avg_rating': float(avg_rating)
            })
    return menu_items

# Read reservations list

def get_reservations():
    res_raw = read_file('reservations.txt')
    reservations = []
    for r in res_raw:
        if len(r) == 11:
            reservation_id, username, guest_name, phone, email, party_size, date, time, special_requests, status = r[:10], r[10] if len(r) > 10 else '', ''
            # The provided design_spec shows 11 fields, but the example only has 10?
            # Actually, reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status is 10 fields.
            # So adjusting accordingly.
            reservation_id, username, guest_name, phone, email, party_size, date, time, special_requests, status = r
            reservations.append({
                'reservation_id': int(reservation_id),
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
    return reservations

# Write reservations list

def write_reservations(reservations):
    rows = []
    for r in reservations:
        rows.append([
            str(r['reservation_id']), r['username'], r['guest_name'], r['phone'], r['email'], str(r['party_size']),
            r['date'], r['time'], r['special_requests'], r['status']
        ])
    write_file('reservations.txt', rows)

# Read waitlist

def get_waitlist():
    waitlist_raw = read_file('waitlist.txt')
    waitlist = []
    for w in waitlist_raw:
        if len(w) == 5:
            waitlist_id, username, party_size, join_time, status = w
            waitlist.append({
                'waitlist_id': int(waitlist_id),
                'username': username,
                'party_size': int(party_size),
                'join_time': join_time,
                'status': status
            })
    return waitlist

# Write waitlist

def write_waitlist(waitlist):
    rows = []
    for w in waitlist:
        rows.append([
            str(w['waitlist_id']), w['username'], str(w['party_size']), w['join_time'], w['status']
        ])
    write_file('waitlist.txt', rows)

# Read reviews

def get_reviews():
    reviews_raw = read_file('reviews.txt')
    reviews = []
    for r in reviews_raw:
        if len(r) == 6:
            review_id, username, dish_id, rating, review_text, review_date = r
            reviews.append({
                'review_id': int(review_id),
                'username': username,
                'dish_id': int(dish_id),
                'rating': int(rating),
                'review_text': review_text,
                'review_date': review_date
            })
    return reviews

# Write reviews

def write_reviews(reviews):
    rows = []
    for r in reviews:
        rows.append([
            str(r['review_id']), r['username'], str(r['dish_id']), str(r['rating']), r['review_text'], r['review_date']
        ])
    write_file('reviews.txt', rows)

# Dummy function to get current logged in user
# For this draft, we will use a fixed username 'john_diner'

def get_current_user():
    users = get_users_dict()
    username = 'john_diner'
    user_profile = users.get(username, {
        'username': username,
        'email': '',
        'phone': '',
        'full_name': ''
    })
    return user_profile


# ROUTES

@app.route('/')
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    return render_template('dashboard.html', username=user['username'])

@app.route('/menu')
def menu_page():
    menu_items = get_menu_items()
    return render_template('menu.html', menu_items=menu_items)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_items = get_menu_items()
    dish = next((d for d in menu_items if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')
    else:
        # POST method: submit reservation
        user = get_current_user()
        guest_name = request.form.get('guest_name', '').strip()
        party_size = request.form.get('party_size')
        reservation_date = request.form.get('reservation_date')
        if not guest_name or not party_size or not reservation_date:
            # Basic validation fail, reload form
            return render_template('make_reservation.html', error="All fields are required.")
        try:
            party_size = int(party_size)
        except:
            return render_template('make_reservation.html', error="Invalid party size.")

        # Generate new reservation id
        reservations = get_reservations()
        new_id = 1
        if reservations:
            new_id = max(r['reservation_id'] for r in reservations) + 1

        # For time and special_requests, since not provided, default to empty and fixed time
        # We do not have time input in the form according to spec, so setting a default time?
        # Spec only includes guest_name, party_size, reservation_date - time is missing?
        # The design_spec example has time field present but no input, so maybe default time: 19:00
        time = '19:00'
        special_requests = ''

        new_reservation = {
            'reservation_id': new_id,
            'username': user['username'],
            'guest_name': guest_name,
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
            'party_size': party_size,
            'date': reservation_date,
            'time': time,
            'special_requests': special_requests,
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        write_reservations(reservations)

        return redirect(url_for('dashboard'))

@app.route('/my-reservations')
def my_reservations():
    user = get_current_user()
    reservations = get_reservations()
    user_reservations = [r for r in reservations if r['username'] == user['username']]
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    user = get_current_user()
    reservations = get_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == user['username']:
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        write_reservations(reservations)
    return redirect(url_for('my_reservations'))

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_page():
    user = get_current_user()
    if request.method == 'GET':
        waitlist = get_waitlist()
        # find user's active position
        active_waitlist = [w for w in waitlist if w['status'] == 'Active']
        active_waitlist.sort(key=lambda x: x['join_time'])
        position = None
        for idx, w in enumerate(active_waitlist, start=1):
            if w['username'] == user['username']:
                position = idx
                break
        return render_template('waitlist.html', waitlist_position=position)
    else:
        # POST join waitlist
        party_size = request.form.get('party_size')
        if not party_size:
            return redirect(url_for('waitlist_page'))
        try:
            party_size = int(party_size)
        except:
            return redirect(url_for('waitlist_page'))
        waitlist = get_waitlist()
        # New waitlist id
        new_id = 1
        if waitlist:
            new_id = max(w['waitlist_id'] for w in waitlist) + 1
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {
            'waitlist_id': new_id,
            'username': user['username'],
            'party_size': party_size,
            'join_time': now_str,
            'status': 'Active'
        }
        waitlist.append(new_entry)
        write_waitlist(waitlist)
        return redirect(url_for('waitlist_page'))

@app.route('/my-reviews')
def my_reviews():
    user = get_current_user()
    reviews = get_reviews()
    my_reviews = [r for r in reviews if r['username'] == user['username']]
    menu_items = get_menu_items()
    # Attach dish name for display
    dish_dict = {d['dish_id']: d['name'] for d in menu_items}
    for review in my_reviews:
        review['dish_name'] = dish_dict.get(review['dish_id'], 'Unknown Dish')
    return render_template('my_reviews.html', reviews=my_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    user = get_current_user()
    if request.method == 'GET':
        dishes = get_menu_items()
        return render_template('write_review.html', dishes=dishes)
    else:
        # POST submit review
        dish_id = request.form.get('dish_id')
        rating = request.form.get('rating')
        review_text = request.form.get('review_text','').strip()
        if not dish_id or not rating or not review_text:
            dishes = get_menu_items()
            return render_template('write_review.html', dishes=dishes, error="All fields are required.")
        try:
            dish_id = int(dish_id)
            rating = int(rating)
        except:
            dishes = get_menu_items()
            return render_template('write_review.html', dishes=dishes, error="Invalid input for dish or rating.")

        reviews = get_reviews()
        new_id = 1
        if reviews:
            new_id = max(r['review_id'] for r in reviews) + 1

        now_date = datetime.datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_id,
            'username': user['username'],
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': now_date
        }
        reviews.append(new_review)
        write_reviews(reviews)
        return redirect(url_for('my_reviews'))

@app.route('/profile')
def user_profile():
    user = get_current_user()
    return render_template('user_profile.html', user_profile=user)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    user = get_current_user()
    email = request.form.get('email', '').strip()
    if not email:
        return redirect(url_for('user_profile'))

    users = get_users_dict()
    if user['username'] in users:
        users[user['username']]['email'] = email
    else:
        users[user['username']] = {
            'username': user['username'],
            'email': email,
            'phone': user.get('phone', ''),
            'full_name': user.get('full_name', '')
        }

    # Rewrite users.txt
    rows = []
    for u in users.values():
        rows.append([u['username'], u['email'], u['phone'], u['full_name']])
    write_file('users.txt', rows)

    return redirect(url_for('user_profile'))

if __name__ == '__main__':
    app.run(debug=True)
