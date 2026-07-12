from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a proper secret key in production

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# Helper functions

def read_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            username, email, phone, address = parts
            users[username] = {'username': username, 'email': email, 'phone': phone, 'address': address}
    return users

def write_users(users):
    lines = []
    for user in users.values():
        lines.append('|'.join([user['username'], user['email'], user['phone'], user['address']]))
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Similar read/write implemented for books, borrowings, reservations, reviews, fines (not repeated here for brevity)


# Logged in user simulation
LOGGED_IN_USERNAME = 'john_reader'

# Date helpers
def get_current_date():
    return datetime.utcnow().date()

def date_to_str(date_obj):
    return date_obj.strftime('%Y-%m-%d')

def str_to_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None

# Fine calculation
def calculate_fine(due_date_str, return_date_str=None):
    due_date = str_to_date(due_date_str)
    if not due_date:
        return 0.0
    if return_date_str:
        return_date = str_to_date(return_date_str)
        if not return_date:
            return 0.0
    else:
        return_date = get_current_date()
    delta = (return_date - due_date).days
    return float(delta) if delta > 0 else 0.0

# Borrowings status and fines refresh function
... # [Unchanged, assumed same as before]

# Routes and main handlers

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    users = read_users()
    if LOGGED_IN_USERNAME not in users:
        flash('User not found.', 'error')
        return redirect(url_for('root_redirect'))
    return render_template('dashboard.html', username=LOGGED_IN_USERNAME)

@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation_get(fine_id):
    fines = read_fines()
    if fine_id not in fines:
        flash('Fine record not found.', 'error')
        return redirect(url_for('user_profile'))
    fine = fines[fine_id]
    if fine['username'] != LOGGED_IN_USERNAME:
        flash('You can only pay your own fines.', 'error')
        return redirect(url_for('user_profile'))
    if fine['status'] == 'Paid':
        flash('This fine is already paid.', 'info')
        return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', fine_amount=fine['amount'], fine_id=fine_id)

@app.route('/payment/<int:fine_id>', methods=['POST'])
def payment_confirmation_post(fine_id):
    fines = read_fines()
    if fine_id not in fines:
        flash('Fine record not found.', 'error')
        return redirect(url_for('user_profile'))
    fine = fines[fine_id]
    if fine['username'] != LOGGED_IN_USERNAME:
        flash('You can only pay your own fines.', 'error')
        return redirect(url_for('user_profile'))
    if fine['status'] == 'Paid':
        flash('This fine is already paid.', 'info')
        return redirect(url_for('user_profile'))
    fine['status'] = 'Paid'
    fines[fine_id] = fine
    write_fines(fines)
    flash('Payment successful. Thank you!', 'success')
    return redirect(url_for('user_profile'))

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    if reservation_id not in reservations:
        flash('Reservation not found.', 'error')
        return redirect(url_for('my_reservations'))
    reservation = reservations[reservation_id]
    if reservation['username'] != LOGGED_IN_USERNAME:
        flash('You can only cancel your own reservations.', 'error')
        return redirect(url_for('my_reservations'))
    if reservation['status'] == 'Cancelled':
        flash('Reservation already cancelled.', 'info')
        return redirect(url_for('my_reservations'))
    reservation['status'] = 'Cancelled'
    reservations[reservation_id] = reservation
    write_reservations(reservations)
    books = read_books()
    book = books.get(reservation['book_id'])
    if book:
        has_other_active = any(r['book_id'] == book['book_id'] and r['status'] == 'Active' for r in reservations.values())
        if not has_other_active and book['status'] == 'Reserved':
            book['status'] = 'Available'
            books[book['book_id']] = book
            write_books(books)
    flash('Reservation cancelled successfully.', 'success')
    return redirect(url_for('my_reservations'))

@app.route('/profile', methods=['GET'])
def user_profile():
    users = read_users()
    borrowings = read_borrowings()
    books = read_books()
    if LOGGED_IN_USERNAME not in users:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    user = users[LOGGED_IN_USERNAME]
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == LOGGED_IN_USERNAME:
            book = books.get(b['book_id'])
            title = book['title'] if book else 'Unknown'
            borrow_history.append({'title': title, 'borrow_date': b['borrow_date'], 'return_date': b['return_date']})
    return render_template('profile.html', username=LOGGED_IN_USERNAME, email=user['email'], phone=user.get('phone', ''), address=user.get('address', ''), borrow_history=borrow_history)

@app.route('/profile', methods=['POST'])
def update_profile():
    users = read_users()
    if LOGGED_IN_USERNAME not in users:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    user = users[LOGGED_IN_USERNAME]
    new_email = request.form.get('email', '').strip()
    new_phone = request.form.get('phone', '').strip()
    new_address = request.form.get('address', '').strip()
    if not new_email:
        flash('Email cannot be empty.', 'error')
        return redirect(url_for('user_profile'))
    user['email'] = new_email
    user['phone'] = new_phone
    user['address'] = new_address
    users[LOGGED_IN_USERNAME] = user
    write_users(users)
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('user_profile'))

# Continue rest of routes unchanged ... 

if __name__ == '__main__':
    app.run(debug=True)
