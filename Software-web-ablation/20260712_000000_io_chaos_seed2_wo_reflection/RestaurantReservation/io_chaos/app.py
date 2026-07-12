from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Load users from a file

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        username, email, phone, fullname = parts
                        users[username] = {
                            'username': username,
                            'email': email,
                            'phone': phone,
                            'fullname': fullname
                        }
    return users

# Load menu items from a file

def load_menu():
    menu = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 8:
                        dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
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
    return menu

# Load reservations from a file

def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 10:
                        reservation_id, username, reservation_code, email, phone, date, time, party_size, status, notes = parts
                        reservations.append({
                            'reservation_id': reservation_id,
                            'username': username,
                            'reservation_code': reservation_code,
                            'email': email,
                            'phone': phone,
                            'date': date,
                            'time': time,
                            'party_size': party_size,
                            'status': status,
                            'notes': notes
                        })
    return reservations

# Save reservations to file

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w') as f:
        for r in reservations:
            line = ','.join([r['reservation_id'], r['username'], r['reservation_code'], r['email'], r['phone'], r['date'], r['time'], r['party_size'], r['status'], r['notes']])
            f.write(line + '\n')

# Load waitlist from a file

def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        username = parts[0]
                        party_size = parts[1]
                        timestamp = parts[2]
                        status = parts[3]
                        notes = parts[4]
                        waitlist.append({
                            'username': username,
                            'party_size': party_size,
                            'timestamp': timestamp,
                            'status': status,
                            'notes': notes
                        })
    return waitlist

# Save waitlist to file

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w') as f:
        for w in waitlist:
            line = ','.join([w['username'], w['party_size'], w['timestamp'], w['status'], w['notes']])
            f.write(line + '\n')

# Load reviews from a file

def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 6:
                        review_id = parts[0]
                        username = parts[1]
                        dish_id = parts[2]
                        rating = parts[3]
                        review_text = parts[4]
                        review_date = parts[5]
                        reviews.append({
                            'review_id': review_id,
                            'username': username,
                            'dish_id': dish_id,
                            'rating': rating,
                            'review_text': review_text,
                            'review_date': review_date
                        })
    return reviews

# Save reviews to file

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w') as f:
        for r in reviews:
            line = ','.join([r['review_id'], r['username'], r['dish_id'], r['rating'], r['review_text'], r['review_date']])
            f.write(line + '\n')


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    users = load_users()
    menu = load_menu()
    reservations = load_reservations()
    username = request.args.get('username') or 'guest'

    featured_dishes = menu[:3] if menu else []
    upcoming_reservations = []

    for r in reservations:
        if r['username'] == username and r['status'].lower() == 'upcoming':
            upcoming_reservations.append(r)

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)

@app.route('/menu', methods=['GET'])
def menu_page():
    menu = load_menu()
    return render_template('menu.html', menu=menu)

@app.route('/dish/<dish_id>', methods=['GET'])
def dish_detail(dish_id):
    menu = load_menu()
    dish = next((dish for dish in menu if dish['dish_id'] == dish_id), None)
    if dish:
        return render_template('dish_detail.html', dish=dish)
    else:
        return "Dish not found", 404

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guestname = request.form.get('guestname')
        date = request.form.get('date')
        time = request.form.get('time')
        party_size = request.form.get('party_size')
        if not guestname or not date or not time or not party_size:
            flash('All fields are required', 'error')
            return render_template('make_reservation.html')

        # Load existing reservations
        reservations = load_reservations()
        # Create new reservation record
        new_id = str(len(reservations) + 1)
        new_reservation = {
            'reservation_id': new_id,
            'username': guestname,
            'reservation_code': 'N/A',
            'email': '',
            'phone': '',
            'date': date,
            'time': time,
            'party_size': party_size,
            'status': 'upcoming',
            'notes': ''
        }
        reservations.append(new_reservation)
        save_reservations(reservations)
        flash('Reservation successfully made', 'success')
        return redirect(url_for('dashboard', username=guestname))
    else:
        return render_template('make_reservation.html')

@app.route('/my_reservations', methods=['GET'])
def my_reservations():
    username = request.args.get('username') or 'guest'
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == username]
    return render_template('my_reservations.html', reservations=user_reservations, username=username)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    users = load_users()
    waitlist = load_waitlist()
    username = request.args.get('username') or 'guest'
    party_size_opts = [str(i) for i in range(1, 11)]
    user_pos = None

    active_usernames = [w['username'] for w in waitlist if w['status'].lower() == 'active']

    if request.method == 'POST':
        party_size = request.form.get('party_size')
        if username not in active_usernames:
            from datetime import datetime
            import time
            new_entry = {
                'username': username,
                'party_size': party_size,
                'timestamp': str(int(time.time())),
                'status': 'active',
                'notes': ''
            }
            waitlist.append(new_entry)
            save_waitlist(waitlist)
            flash('Added to waitlist successfully', 'success')
        else:
            flash('You are already on the waitlist', 'info')
        return redirect(url_for('waitlist', username=username))
    else:
        # Find user position in waitlist
        active_waitlist = [w for w in waitlist if w['status'].lower() == 'active']
        sorted_waitlist = sorted(active_waitlist, key=lambda x: int(x['timestamp']))
        for idx, entry in enumerate(sorted_waitlist):
            if entry['username'] == username:
                user_pos = idx + 1
                break
        return render_template('waitlist.html', waitlist=waitlist, user_pos=user_pos, party_size_opts=party_size_opts)

@app.route('/my_reviews', methods=['GET'])
def my_reviews():
    username = request.args.get('username') or 'guest'
    users = load_users()
    if username not in users:
        username = 'guest'

    reviews = load_reviews()
    menu = load_menu()
    dish_map = {dish['dish_id']: dish['name'] for dish in menu}
    user_reviews = [r for r in reviews if r['username'] == username]

    for review in user_reviews:
        review['dish_name'] = dish_map.get(review['dish_id'], 'Unknown Dish')

    return render_template('my_reviews.html', reviews=user_reviews, username=username)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    menu = load_menu()
    if request.method == 'GET':
        return render_template('write_review.html', menu=menu)
    elif request.method == 'POST':
        username = request.args.get('username') or 'guest'
        dish_id = request.form.get('dish_id')
        rating = request.form.get('rating')
        review_text = request.form.get('review_text')
        from datetime import datetime
        import uuid
        reviews = load_reviews()

        new_review = {
            'review_id': str(uuid.uuid4()),
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text.replace(',', ';'), # Avoid CSV issues
            'review_date': datetime.now().strftime('%Y-%m-%d')
        }
        reviews.append(new_review)
        save_reviews(reviews)
        flash('Review submitted successfully', 'success')
        return redirect(url_for('my_reviews', username=username))

@app.route('/profile')
def profile():
    users = load_users()
    username = request.args.get('username') or 'guest'
    user = users.get(username, None)
    if not user:
        user = {
            'username': 'guest',
            'email': '',
            'phone': '',
            'fullname': ''
        }
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
