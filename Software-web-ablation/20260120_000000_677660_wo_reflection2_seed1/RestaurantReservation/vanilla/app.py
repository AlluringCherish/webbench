from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime, date
import re
import os
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper function to load users from users.txt
# Returns dict keyed by username

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    username, email, phone, full_name = parts
                    users[username] = {
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'full_name': full_name
                    }
    except FileNotFoundError:
        pass
    return users

# Helper function to load menu from menu.txt
# returns list of dicts

def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id_str, name, category, price_str, description, ingredients, dietary, avg_rating_str = parts
                    try:
                        dish_id = int(dish_id_str)
                        price = float(price_str)
                        avg_rating = float(avg_rating_str)
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
                    except ValueError:
                        # Skip invalid lines
                        continue
    except FileNotFoundError:
        pass
    return menu

# Helper function to load reservations from reservations.txt
# returns list of dicts

def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    (
                        reservation_id_str, username, guest_name, phone, email, party_size_str, date_str, time,
                        special_requests, status
                    ) = parts
                    try:
                        reservation_id = int(reservation_id_str)
                        party_size = int(party_size_str)
                        reservations.append({
                            'reservation_id': reservation_id,
                            'username': username,
                            'guest_name': guest_name,
                            'phone': phone,
                            'email': email,
                            'party_size': party_size,
                            'date': date_str,
                            'time': time,
                            'special_requests': special_requests,
                            'status': status
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return reservations

# Helper function to save all reservations (overwrite file)
def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper function to load waitlist from waitlist.txt
# returns list of dicts

def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id_str, username, party_size_str, join_time, status = parts
                    try:
                        waitlist_id = int(waitlist_id_str)
                        party_size = int(party_size_str)
                        waitlist.append({
                            'waitlist_id': waitlist_id,
                            'username': username,
                            'party_size': party_size,
                            'join_time': join_time,
                            'status': status
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return waitlist

# Helper function to save waitlist

def save_waitlist(waitlist):
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
            for w in waitlist:
                line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper function to load reviews
# returns list of dicts

def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id_str, username, dish_id_str, rating_str, review_text, review_date = parts
                    try:
                        review_id = int(review_id_str)
                        dish_id = int(dish_id_str)
                        rating = int(rating_str)
                        reviews.append({
                            'review_id': review_id,
                            'username': username,
                            'dish_id': dish_id,
                            'rating': rating,
                            'review_text': review_text,
                            'review_date': review_date
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return reviews

# Helper function to save reviews

def save_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception:
        pass

# Pick a static current username for demonstration since auth is not specified
# Just pick 'john_diner' if exists

def get_current_username():
    users = load_users()
    return 'john_diner' if 'john_diner' in users else (list(users.keys())[0] if users else None)

# Simple email validation regex
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    users = load_users()

    # Featured dishes: top 3 dishes by avg_rating descending
    menu = load_menu()
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    # Format output fields: dish_id:int,name:str,price:float,description:str
    featured_dishes = [{
        'dish_id': d['dish_id'],
        'name': d['name'],
        'price': d['price'],
        'description': d['description']
    } for d in featured_dishes]

    # Upcoming reservations for current user
    reservations = load_reservations()
    upcoming_reservations = []
    for r in reservations:
        if r['username'] == username and r['status'] == 'Upcoming':
            # date:str, time:str, party_size:int, status:str
            upcoming_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })

    return render_template('dashboard.html',
                           username=username, featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu():
    menu_list = load_menu()
    # context variable menus: list of dict with keys:
    # dish_id:int, name:str, category:str, price:float, description:str, ingredients:str, dietary:str, avg_rating:float
    return render_template('menu.html', menus=menu_list)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_list = load_menu()
    dish = None
    for d in menu_list:
        if d['dish_id'] == dish_id:
            dish = d
            break
    if not dish:
        # Could redirect to menu with a flash or 404, but spec does not mention error page.
        return redirect(url_for('menu'))
    return render_template('dish_details.html', dish=dish)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')

    # POST
    username = get_current_username()
    if not username:
        # If no user, redirect dashboard
        return redirect(url_for('dashboard'))

    guest_name_raw = request.form.get('guest_name','').strip()
    # Sanitize guest_name to prevent injection
    guest_name = html.escape(guest_name_raw)

    party_size_str = request.form.get('party_size','').strip()
    reservation_date = request.form.get('reservation_date','').strip()

    errors = []

    if not guest_name_raw:
        errors.append('Guest name is required.')
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size >10:
            errors.append('Party size must be between 1 and 10.')
    except Exception:
        errors.append('Invalid party size.')

    # Validate date format YYYY-MM-DD
    try:
        date_obj = datetime.strptime(reservation_date, '%Y-%m-%d').date()
    except Exception:
        errors.append('Invalid reservation date format.')
        date_obj = None

    # Validate date not in past
    if date_obj and date_obj < date.today():
        errors.append('Reservation date cannot be in the past.')

    if errors:
        # For simplicity, render page again with errors shown
        # The spec doesn't specify error display mechanism, so we just render again
        return render_template('make_reservation.html', errors=errors)

    users = load_users()
    user_profile = users.get(username, {})

    reservations = load_reservations()

    # Generate new reservation_id
    new_id = max((r['reservation_id'] for r in reservations), default=0) + 1

    # No time given on form; we must set a time. Spec only says time field is in reservation file.
    # We will use default time '19:00'
    default_time = '19:00'

    new_reservation = {
        'reservation_id': new_id,
        'username': username,
        'guest_name': guest_name,
        'phone': user_profile.get('phone',''),
        'email': user_profile.get('email',''),
        'party_size': party_size,
        'date': reservation_date,
        'time': default_time,
        'special_requests': '',
        'status': 'Upcoming'
    }
    reservations.append(new_reservation)

    save_reservations(reservations)

    return redirect(url_for('dashboard'))

@app.route('/my_reservations')
def my_reservations():
    username = get_current_username()
    reservations_all = load_reservations()
    reservations = []
    for r in reservations_all:
        if r['username'] == username:
            # Fields: reservation_id:int, date:str, time:str, party_size:int, status:str
            reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=reservations)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_current_username()
    reservations = load_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username:
            # Update status to "Cancelled"
            r['status'] = 'Cancelled'
            found = True
            break

    if found:
        save_reservations(reservations)
        # Spec: Return JSON or redirect
        # We'll return JSON indicating success
        return jsonify({"success": True, "message": "Reservation cancelled."})
    else:
        return jsonify({"success": False, "message": "Reservation not found or not authorized."}), 404

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = get_current_username()
    waitlist = load_waitlist()

    # Find current user's active waitlist position or None
    user_waitlist_entry = None
    active_waitlist = [w for w in waitlist if w['status'] == 'Active']
    active_waitlist_sorted = sorted(active_waitlist, key=lambda w: w['join_time'])
    position = None
    for idx, w in enumerate(active_waitlist_sorted, start=1):
        if w['username'] == username:
            user_waitlist_entry = w
            position = idx
            break

    if request.method == 'GET':
        party_size_options = list(range(1,11))

        # if user in waitlist active, position else None
        waitlist_position = position if user_waitlist_entry else None
        return render_template('waitlist.html', waitlist_position=waitlist_position, party_size_options=party_size_options)

    # POST: join waitlist or leave waitlist
    action = request.form.get('action')
    
    if action == 'leave':
        # Remove user from waitlist if active
        if user_waitlist_entry:
            waitlist = [w for w in waitlist if not (w['username'] == username and w['status'] == 'Active')]
            save_waitlist(waitlist)
            message = 'You have left the waitlist.'
        else:
            message = 'You are not currently on the waitlist.'
        party_size_options = list(range(1,11))
        return render_template('waitlist.html', waitlist_position=None, party_size_options=party_size_options, message=message)

    party_size_str = request.form.get('party_size','').strip()
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            raise ValueError
    except Exception:
        party_size = None

    if party_size is None:
        party_size_options = list(range(1,11))
        waitlist_position = position if user_waitlist_entry else None
        errors = ['Invalid party size selection.']
        return render_template('waitlist.html', waitlist_position=waitlist_position, party_size_options=party_size_options, errors=errors)

    # If user already in waitlist active, do not add again
    if user_waitlist_entry:
        # Just render with current position
        party_size_options = list(range(1,11))
        waitlist_position = position
        message = 'You are already in the waitlist.'
        return render_template('waitlist.html', waitlist_position=waitlist_position, party_size_options=party_size_options, message=message)

    # Generate new waitlist_id
    new_id = max((w['waitlist_id'] for w in waitlist), default=0) + 1
    join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = {
        'waitlist_id': new_id,
        'username': username,
        'party_size': party_size,
        'join_time': join_time,
        'status': 'Active'
    }
    waitlist.append(new_entry)
    save_waitlist(waitlist)

    # recalc position
    active_waitlist = [w for w in waitlist if w['status'] == 'Active']
    active_waitlist_sorted = sorted(active_waitlist, key=lambda w: w['join_time'])
    position = None
    for idx, w in enumerate(active_waitlist_sorted, start=1):
        if w['username'] == username:
            position = idx
            break

    party_size_options = list(range(1,11))
    return render_template('waitlist.html', waitlist_position=position, party_size_options=party_size_options, message='You have joined the waitlist.')


@app.route('/my_reviews')
def my_reviews():
    username = get_current_username()
    reviews_all = load_reviews()
    menu = load_menu()

    reviews = []
    for r in reviews_all:
        if r['username'] == username:
            dish_name = ''
            for d in menu:
                if d['dish_id'] == r['dish_id']:
                    dish_name = d['name']
                    break
            reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=reviews)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    username = get_current_username()
    if request.method == 'GET':
        menu = load_menu()
        dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
        return render_template('write_review.html', dishes=dishes)

    # POST
    selected_dish_id_str = request.form.get('selected_dish_id','').strip()
    rating_str = request.form.get('rating','').strip()
    review_text = request.form.get('review_text','').strip()

    errors = []

    try:
        selected_dish_id = int(selected_dish_id_str)
    except Exception:
        errors.append('Dish selection is required.')

    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            errors.append('Rating must be between 1 and 5.')
    except Exception:
        errors.append('Invalid rating value.')

    if len(review_text) == 0:
        errors.append('Review text is required.')

    if errors:
        menu = load_menu()
        dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
        return render_template('write_review.html', dishes=dishes, errors=errors)

    # Add new review
    reviews = load_reviews()
    new_id = max((r['review_id'] for r in reviews), default=0) + 1

    new_review = {
        'review_id': new_id,
        'username': username,
        'dish_id': selected_dish_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': datetime.now().strftime('%Y-%m-%d')
    }
    reviews.append(new_review)
    save_reviews(reviews)

    return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_current_username()
    users = load_users()
    user_profile = users.get(username, None)
    if not user_profile:
        # No user profile found, redirect dashboard
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('profile.html', user_profile=user_profile)

    # POST: update email
    email = request.form.get('email','').strip()
    if not email:
        # re-render with error
        error = 'Email cannot be empty.'
        return render_template('profile.html', user_profile=user_profile, error=error)

    if not EMAIL_REGEX.match(email):
        error = 'Invalid email format.'
        return render_template('profile.html', user_profile=user_profile, error=error)

    # Update user email
    # Update in the users.txt file
    updated_users = []
    for u in users.values():
        if u['username'] == username:
            u['email'] = email
        updated_users.append(u)

    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for u in updated_users:
                line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n"
                f.write(line)
    except Exception:
        pass

    # reload updated profile
    users = load_users()
    user_profile = users.get(username, user_profile)

    message = 'Profile updated successfully.'
    return render_template('profile.html', user_profile=user_profile, message=message)


if __name__ == '__main__':
    app.run(debug=True)
