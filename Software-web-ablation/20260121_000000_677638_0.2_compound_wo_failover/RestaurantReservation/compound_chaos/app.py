import os
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    username, email, phone, full_name = parts
                    users[username] = {'username': username, 'email': email, 'phone': phone, 'full_name': full_name}
    except FileNotFoundError:
        pass
    return users


def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8:
                    dish_id = int(parts[0])
                    name = parts[1]
                    category = parts[2]
                    ingredients = parts[3]
                    dietary = parts[4]
                    description = parts[5]
                    price = float(parts[6])
                    avg_rating = float(parts[7])
                    menu.append({'dish_id': dish_id, 'name': name, 'category': category, 'ingredients': ingredients, 'dietary': dietary, 'description': description, 'price': price, 'avg_rating': avg_rating})
    except FileNotFoundError:
        pass
    return menu


def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id = int(parts[0])
                    username = parts[1]
                    guest_name = parts[2]
                    phone = parts[3]
                    email = parts[4]
                    party_size = int(parts[5])
                    date = parts[6]
                    time = parts[7]
                    special_requests = parts[8]
                    status = parts[9]
                    reservations.append({'reservation_id': reservation_id, 'username': username, 'guest_name': guest_name, 'phone': phone, 'email': email, 'party_size': party_size, 'date': date, 'time': time, 'special_requests': special_requests, 'status': status})
    except FileNotFoundError:
        pass
    return reservations


def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass


def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id = int(parts[0])
                    username = parts[1]
                    party_size = int(parts[2])
                    join_time = parts[3]
                    status = parts[4]
                    waitlist.append({'waitlist_id': waitlist_id, 'username': username, 'party_size': party_size, 'join_time': join_time, 'status': status})
    except FileNotFoundError:
        pass
    return waitlist


def save_waitlist(waitlist):
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
            for w in waitlist:
                line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n"
                f.write(line)
    except Exception:
        pass


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id = int(parts[0])
                    username = parts[1]
                    dish_id = int(parts[2])
                    rating = int(parts[3])
                    review_text = parts[4]
                    review_date = parts[5]
                    reviews.append({'review_id': review_id, 'username': username, 'dish_id': dish_id, 'rating': rating, 'review_text': review_text, 'review_date': review_date})
    except FileNotFoundError:
        pass
    return reviews


def save_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception as e:
        pass


def get_logged_in_username():
    # simplification for test/demo purpose
    username = request.args.get('username')
    if not username:
        username = 'john_diner'  # fallback for testing
    return username


@app.route('/')
def dashboard():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    menu = load_menu()
    reservations = load_reservations()

    featured_dishes = []
    for dish in menu:
        featured_dishes.append({'dish_id': dish['dish_id'], 'name': dish['name'], 'price': dish['price'], 'description': dish['description']})

    upcoming_reservations = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    for r in reservations:
        if r['username'] == username and r['status'] == 'Upcoming' and r['date'] >= today:
            upcoming_reservations.append({'reservation_id': r['reservation_id'], 'date': r['date'], 'time': r['time'], 'party_size': r['party_size'], 'status': r['status']})

    return render_template('dashboard.html', featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations, user=user)


@app.route('/menu')
def menu_page():
    menu = load_menu()
    return render_template('menu.html', menu=menu)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = None
    for d in menu:
        if d['dish_id'] == dish_id:
            dish = d
            break
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        guest_name = request.form.get('guest_name')
        party_size_raw = request.form.get('party_size')
        reservation_date = request.form.get('reservation_date')

        # Validate party size
        try:
            party_size = int(party_size_raw)
            if party_size < 1:
                flash('Party size must be 1 or greater.', 'error')
                return redirect(url_for('make_reservation'))
        except Exception:
            flash('Party size must be an integer.', 'error')
            return redirect(url_for('make_reservation'))

        # Validate date
        try:
            dt_res_date = datetime.datetime.strptime(reservation_date, '%Y-%m-%d')
            if dt_res_date.date() < datetime.datetime.now().date():
                flash('Reservation date must be today or in the future.', 'error')
                return redirect(url_for('make_reservation'))
        except Exception:
            flash('Invalid reservation date.', 'error')
            return redirect(url_for('make_reservation'))

        if not guest_name or guest_name.strip() == '':
            flash('Guest name is required.', 'error')
            return redirect(url_for('make_reservation'))

        reservations = load_reservations()
        if reservations:
            new_id = max(r['reservation_id'] for r in reservations) + 1
        else:
            new_id = 1

        # Default time for simplicity
        default_time = '19:00'

        new_reservation = {
            'reservation_id': new_id,
            'username': username,
            'guest_name': guest_name.strip(),
            'phone': user['phone'],
            'email': user['email'],
            'party_size': party_size,
            'date': reservation_date,
            'time': default_time,
            'special_requests': '',
            'status': 'Upcoming'
        }

        reservations.append(new_reservation)
        save_reservations(reservations)
        flash('Reservation made successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('make_reservation.html')


@app.route('/my_reservations')
def my_reservations():
    username = get_logged_in_username()
    reservations = load_reservations()
    user_reservations = []
    for r in reservations:
        if r['username'] == username:
            user_reservations.append(r)
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_logged_in_username()
    reservations = load_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            found = True
            break
    if found:
        save_reservations(reservations)
        flash('Reservation cancelled successfully.', 'success')
    else:
        flash('Reservation not found or cannot be cancelled.', 'error')
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = get_logged_in_username()
    waitlist_entries = load_waitlist()
    active_waitlist = [w for w in waitlist_entries if w['status'] == 'Active']
    user_entries = [w for w in waitlist_entries if w['username'] == username and w['status'] == 'Active']
    user_position = None

    sorted_waitlist = sorted(active_waitlist, key=lambda x: x['join_time'])

    for idx, w in enumerate(sorted_waitlist):
        if w['username'] == username:
            user_position = idx + 1
            break

    if request.method == 'POST':
        party_size_raw = request.form.get('party_size')
        try:
            party_size = int(party_size_raw)
            if party_size < 1:
                flash('Party size must be 1 or greater.', 'error')
                return redirect(url_for('waitlist'))
        except Exception:
            flash('Party size must be an integer.', 'error')
            return redirect(url_for('waitlist'))

        if user_entries:
            flash('You are already on the waitlist.', 'info')
            return redirect(url_for('waitlist'))

        if waitlist_entries:
            new_id = max(w['waitlist_id'] for w in waitlist_entries) + 1
        else:
            new_id = 1

        join_time = datetime.datetime.now().isoformat()

        new_waitlist_entry = {
            'waitlist_id': new_id,
            'username': username,
            'party_size': party_size,
            'join_time': join_time,
            'status': 'Active'
        }
        waitlist_entries.append(new_waitlist_entry)
        save_waitlist(waitlist_entries)
        flash('Added to waitlist successfully!', 'success')
        return redirect(url_for('waitlist'))

    return render_template('waitlist.html', waitlist_entries=active_waitlist, user_position=user_position)


@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    menu = load_menu()
    reviews = load_reviews()

    user_reviews = [r for r in reviews if r['username'] == username]

    dish_map = {d['dish_id']: d['name'] for d in menu}

    if request.method == 'POST':
        dish_id_raw = request.form.get('dish_id')
        rating_raw = request.form.get('rating', '5')
        review_text = request.form.get('review_text', '').strip()

        if not dish_id_raw or not dish_id_raw.isdigit():
            flash('Please select a dish.', 'error')
            return redirect(url_for('my_reviews'))
        dish_id = int(dish_id_raw)

        try:
            rating = int(rating_raw)
            if rating < 1 or rating > 5:
                flash('Rating must be between 1 and 5.', 'error')
                return redirect(url_for('my_reviews'))
        except Exception:
            flash('Invalid rating.', 'error')
            return redirect(url_for('my_reviews'))

        if not review_text:
            flash('Review text cannot be empty.', 'error')
            return redirect(url_for('my_reviews'))

        reviews = load_reviews()
        if reviews:
            new_id = max(r['review_id'] for r in reviews) + 1
        else:
            new_id = 1
        today_str = datetime.datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_id,
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }

        reviews.append(new_review)
        save_reviews(reviews)
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('my_reviews'))

    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
    return render_template('my_reviews.html', reviews=user_reviews, dishes=dishes)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')

        if not email or email.strip() == '':
            flash('Email is required.', 'error')
            return render_template('profile.html', profile=user)

        # Update user's email
        user['email'] = email.strip()

        # Save users back
        try:
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n"
                    f.write(line)
            flash('Profile updated successfully!', 'success')
        except Exception:
            flash('Failed to save user profile.', 'error')

        return render_template('profile.html', profile=user)
    else:
        return render_template('profile.html', profile=user)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
