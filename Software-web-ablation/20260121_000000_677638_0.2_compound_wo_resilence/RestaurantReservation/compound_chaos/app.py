import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'
LOGGED_IN_USERNAME = 'johndoe'  # Demo logged-in user

# Utility function to get a user dict by username

def get_user(username):
    users = read_users()
    return next((u for u in users if u['username'] == username), None)

# Read data functions

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_PATH, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'full_name': parts[3]
                    })
    except FileNotFoundError:
        pass
    return users


def write_users(users):
    with open(os.path.join(DATA_PATH, 'users.txt'), 'w', encoding='utf-8') as f:
        for u in users:
            line = '|'.join([u['username'], u['email'], u['phone'], u['full_name']])
            f.write(line + '\n')


def read_menu():
    dishes = []
    try:
        with open(os.path.join(DATA_PATH, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dishes.append({
                        'dish_id': int(parts[0]),
                        'name': parts[1],
                        'category': parts[2],
                        'price': float(parts[3]),
                        'description': parts[4],
                        'ingredients': parts[5],
                        'dietary': parts[6],
                        'avg_rating': float(parts[7])
                    })
    except FileNotFoundError:
        pass
    return dishes


def write_menu(dishes):
    with open(os.path.join(DATA_PATH, 'menu.txt'), 'w', encoding='utf-8') as f:
        for d in dishes:
            line = '|'.join([
                str(d['dish_id']), d['name'], d['category'], f"{d['price']}", d['description'], d['ingredients'], d['dietary'], f"{d['avg_rating']}"
            ])
            f.write(line + '\n')


def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_PATH, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    reviews.append({
                        'review_id': int(parts[0]),
                        'username': parts[1],
                        'dish_id': int(parts[2]),
                        'rating': float(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    except FileNotFoundError:
        pass
    return reviews


def write_reviews(reviews):
    with open(os.path.join(DATA_PATH, 'reviews.txt'), 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                str(r['review_id']), r['username'], str(r['dish_id']), f"{r['rating']}", r['review_text'], r['review_date']
            ])
            f.write(line + '\n')


def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_PATH, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservations.append({
                        'reservation_id': int(parts[0]),
                        'username': parts[1],
                        'guest_name': parts[2],
                        'phone': parts[3],
                        'email': parts[4],
                        'party_size': int(parts[5]),
                        'date': parts[6],
                        'time': parts[7],
                        'special_requests': parts[8],
                        'status': parts[9]
                    })
    except FileNotFoundError:
        pass
    return reservations


def write_reservations(reservations):
    with open(os.path.join(DATA_PATH, 'reservations.txt'), 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                str(r['reservation_id']), r['username'], r['guest_name'], r['phone'], r['email'], str(r['party_size']), r['date'], r['time'], r['special_requests'], r['status']
            ])
            f.write(line + '\n')


def read_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_PATH, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist.append({
                        'waitlist_id': int(parts[0]),
                        'username': parts[1],
                        'party_size': int(parts[2]),
                        'join_time': parts[3],
                        'status': parts[4]
                    })
    except FileNotFoundError:
        pass
    return waitlist


def write_waitlist(waitlist):
    with open(os.path.join(DATA_PATH, 'waitlist.txt'), 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = '|'.join([
                str(w['waitlist_id']), w['username'], str(w['party_size']), w['join_time'], w['status']
            ])
            f.write(line + '\n')


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    dishes = read_menu()
    reservations = [r for r in read_reservations() if r['username'] == LOGGED_IN_USERNAME]
    waitlist = read_waitlist()

    # Filter active entries for waitlist position
    active_entries = [w for w in waitlist if w['status'] == 'active']
    active_entries.sort(key=lambda x: x['join_time'])
    user_waitlist = next((w for w in active_entries if w['username'] == LOGGED_IN_USERNAME), None)
    waitlist_position = None
    if user_waitlist:
        waitlist_position = active_entries.index(user_waitlist) + 1

    return render_template('dashboard.html', dishes=dishes, reservations=reservations, waitlist_position=waitlist_position)


@app.route('/menu')
def menu():
    dishes = read_menu()
    categories = sorted(set(d['category'] for d in dishes))
    return render_template('menu.html', dishes=dishes, categories=categories)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    dishes = read_menu()
    dish = next((d for d in dishes if d['dish_id'] == dish_id), None)
    if not dish:
        return "Dish not found", 404
    reviews = [r for r in read_reviews() if r['dish_id'] == dish_id]
    return render_template('dish_details.html', dish=dish, reviews=reviews)


@app.route('/my-reviews')
def my_reviews():
    reviews = [r for r in read_reviews() if r['username'] == LOGGED_IN_USERNAME]
    dishes = {d['dish_id']: d['name'] for d in read_menu()}
    for r in reviews:
        r['dish_name'] = dishes.get(r['dish_id'], 'Unknown Dish')
    return render_template('my_reviews.html', reviews=reviews)


@app.route('/write-review/<int:dish_id>', methods=['GET', 'POST'])
def write_review(dish_id):
    dishes = read_menu()
    dish = next((d for d in dishes if d['dish_id'] == dish_id), None)
    if not dish:
        return "Dish not found", 404

    reviews = read_reviews()
    existing_review = next((r for r in reviews if r['username'] == LOGGED_IN_USERNAME and r['dish_id'] == dish_id), None)

    if request.method == 'POST':
        try:
            rating = float(request.form.get('rating', ''))
        except ValueError:
            rating = None
        review_text = request.form.get('review_text', '').strip()

        if not rating or rating < 1 or rating > 5:
            error = 'Invalid rating. Please provide a value from 1 to 5.'
            return render_template('write_review.html', dish=dish, review=existing_review, error=error)

        now_str = datetime.now().strftime('%Y-%m-%d')
        if existing_review:
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = now_str
        else:
            new_id = max([r['review_id'] for r in reviews], default=0) + 1
            new_review = {
                'review_id': new_id,
                'username': LOGGED_IN_USERNAME,
                'dish_id': dish_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': now_str
            }
            reviews.append(new_review)

        write_reviews(reviews)

        # Update average rating for the dish
        dish_reviews = [r for r in reviews if r['dish_id'] == dish_id]
        avg_rating = sum(r['rating'] for r in dish_reviews) / len(dish_reviews) if dish_reviews else 0
        for d in dishes:
            if d['dish_id'] == dish_id:
                d['avg_rating'] = avg_rating
        write_menu(dishes)

        return redirect(url_for('dish_details', dish_id=dish_id))

    return render_template('write_review.html', dish=dish, review=existing_review)


@app.route('/reservations')
def reservations():
    reservations = [r for r in read_reservations() if r['username'] == LOGGED_IN_USERNAME]
    return render_template('reservations.html', reservations=reservations)


@app.route('/reservations/make', methods=['POST'])
def make_reservation():
    guest_name = request.form.get('guest_name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    party_size_str = request.form.get('party_size', '1')
    date = request.form.get('date', '').strip()
    time = request.form.get('time', '').strip()
    special_requests = request.form.get('special_requests', '').strip()

    try:
        party_size = int(party_size_str)
    except ValueError:
        party_size = 1

    reservations = read_reservations()
    new_id = max([r['reservation_id'] for r in reservations], default=0) + 1

    new_reservation = {
        'reservation_id': new_id,
        'username': LOGGED_IN_USERNAME,
        'guest_name': guest_name,
        'phone': phone,
        'email': email,
        'party_size': party_size,
        'date': date,
        'time': time,
        'special_requests': special_requests,
        'status': 'active'
    }
    reservations.append(new_reservation)
    write_reservations(reservations)
    return redirect(url_for('reservations'))


@app.route('/reservations/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME:
            r['status'] = 'cancelled'
            break
    write_reservations(reservations)
    return redirect(url_for('reservations'))


@app.route('/waitlist', methods=['GET'])
def waitlist():
    waitlist = read_waitlist()
    active_entries = [w for w in waitlist if w['status'] == 'active']
    active_entries.sort(key=lambda w: w['join_time'])
    user_entry = next((w for w in active_entries if w['username'] == LOGGED_IN_USERNAME), None)
    user_position = None
    if user_entry:
        user_position = active_entries.index(user_entry) + 1

    return render_template('waitlist.html', waitlist=waitlist, user_position=user_position)


@app.route('/waitlist/join', methods=['POST'])
def join_waitlist():
    party_size_str = request.form.get('party_size', '1')
    try:
        party_size = int(party_size_str)
    except ValueError:
        party_size = 1

    waitlist = read_waitlist()
    new_id = max([w['waitlist_id'] for w in waitlist], default=0) + 1
    now_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    new_entry = {
        'waitlist_id': new_id,
        'username': LOGGED_IN_USERNAME,
        'party_size': party_size,
        'join_time': now_str,
        'status': 'active'
    }
    waitlist.append(new_entry)
    write_waitlist(waitlist)
    return redirect(url_for('waitlist'))


@app.route('/waitlist/leave', methods=['POST'])
def leave_waitlist():
    waitlist = read_waitlist()
    for w in waitlist:
        if w['username'] == LOGGED_IN_USERNAME and w['status'] == 'active':
            w['status'] = 'left'
            break
    write_waitlist(waitlist)
    return redirect(url_for('waitlist'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = get_user(LOGGED_IN_USERNAME)
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        for u in users:
            if u['username'] == LOGGED_IN_USERNAME:
                u['full_name'] = full_name
                u['email'] = email
                u['phone'] = phone
                break
        else:
            # If user not found, add new
            users.append({
                'username': LOGGED_IN_USERNAME,
                'email': email,
                'phone': phone,
                'full_name': full_name
            })
        write_users(users)
        return redirect(url_for('dashboard'))

    return render_template('profile.html', user=user if user else {'full_name': '', 'email': '', 'phone': ''})


if __name__ == '__main__':
    app.run(debug=True)
