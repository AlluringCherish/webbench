from flask import Flask, request, session, redirect, url_for, render_template, abort, flash
from datetime import datetime, timedelta
import re
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'
DATA_DIR = 'data'

# Utilities for file IO and parsing

def read_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        records = [line.split('|') for line in lines if line]
    return records

def write_file(filename, records):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write('|'.join(str(x) for x in record) + '\n')

# Load all users
# users: dict username->(email, phone, address)
def load_users():
    users_raw = read_file('users.txt')
    users = {}
    for r in users_raw:
        if len(r) == 4:
            users[r[0]] = {'email': r[1], 'phone': r[2], 'address': r[3]}
    return users

def save_users(users):
    records = []
    for username, info in users.items():
        records.append([username, info['email'], info['phone'], info['address']])
    write_file('users.txt', records)

# Load all books
# books: dict book_id->dict with keys from spec
# book_id is int

def load_books():
    books_raw = read_file('books.txt')
    books = {}
    for r in books_raw:
        if len(r) == 10:
            try:
                book_id = int(r[0])
                books[book_id] = {
                    'book_id': book_id,
                    'title': r[1],
                    'author': r[2],
                    'isbn': r[3],
                    'genre': r[4],
                    'publisher': r[5],
                    'year': r[6],
                    'description': r[7],
                    'status': r[8],
                    'avg_rating': float(r[9])
                }
            except ValueError:
                continue
    return books

def save_books(books):
    records = []
    for book_id in sorted(books.keys()):
        b = books[book_id]
        records.append([
            b['book_id'], b['title'], b['author'], b['isbn'], b['genre'], b['publisher'], b['year'],
            b['description'], b['status'], f"{b['avg_rating']:.1f}"
        ])
    write_file('books.txt', records)

# Load borrowings
# borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
# borrow_id int

def load_borrowings():
    borrowings_raw = read_file('borrowings.txt')
    borrowings = {}
    for r in borrowings_raw:
        if len(r) == 8:
            try:
                borrow_id = int(r[0])
                borrowings[borrow_id] = {
                    'borrow_id': borrow_id,
                    'username': r[1],
                    'book_id': int(r[2]),
                    'borrow_date': r[3],
                    'due_date': r[4],
                    'return_date': r[5],
                    'status': r[6],
                    'fine_amount': float(r[7])
                }
            except ValueError:
                continue
    return borrowings

def save_borrowings(borrowings):
    records = []
    for borrow_id in sorted(borrowings.keys()):
        b = borrowings[borrow_id]
        records.append([
            b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'], b['return_date'], b['status'], f"{b['fine_amount']:.2f}"
        ])
    write_file('borrowings.txt', records)

# Load reservations
# reservation_id|username|book_id|reservation_date|status

def load_reservations():
    reservations_raw = read_file('reservations.txt')
    reservations = {}
    for r in reservations_raw:
        if len(r) == 5:
            try:
                reservation_id = int(r[0])
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': r[1],
                    'book_id': int(r[2]),
                    'reservation_date': r[3],
                    'status': r[4]
                }
            except ValueError:
                continue
    return reservations

def save_reservations(reservations):
    records = []
    for rid in sorted(reservations.keys()):
        r = reservations[rid]
        records.append([
            r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']
        ])
    write_file('reservations.txt', records)

# Load reviews
# review_id|username|book_id|rating|review_text|review_date

def load_reviews():
    reviews_raw = read_file('reviews.txt')
    reviews = {}
    for r in reviews_raw:
        if len(r) == 6:
            try:
                review_id = int(r[0])
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': r[1],
                    'book_id': int(r[2]),
                    'rating': int(r[3]),
                    'review_text': r[4],
                    'review_date': r[5]
                }
            except ValueError:
                continue
    return reviews

def save_reviews(reviews):
    records = []
    for rid in sorted(reviews.keys()):
        r = reviews[rid]
        safe_review_text = r['review_text'].replace('|', '/')
        records.append([
            r['review_id'], r['username'], r['book_id'], r['rating'], safe_review_text, r['review_date']
        ])
    write_file('reviews.txt', records)

# Load fines
# fine_id|username|borrow_id|amount|status|date_issued

def load_fines():
    fines_raw = read_file('fines.txt')
    fines = {}
    for r in fines_raw:
        if len(r) == 6:
            try:
                fine_id = int(r[0])
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': r[1],
                    'borrow_id': int(r[2]),
                    'amount': float(r[3]),
                    'status': r[4],
                    'date_issued': r[5]
                }
            except ValueError:
                continue
    return fines

def save_fines(fines):
    records = []
    for fid in sorted(fines.keys()):
        f = fines[fid]
        records.append([
            f['fine_id'], f['username'], f['borrow_id'], f['amount'], f['status'], f['date_issued']
        ])
    write_file('fines.txt', records)

# Helper functions

def validate_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

# Routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = load_users()
        if username in users:
            session['username'] = username
            return redirect(url_for('show_dashboard'))
        else:
            flash('Invalid username')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def show_dashboard():
    username = session['username']
    books = load_books()
    featured = [b for b in books.values() if b['avg_rating'] >= 4.5]
    featured_sorted = sorted(featured, key=lambda x: -x['avg_rating'])[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_sorted)

@app.route('/books')
@login_required
def list_books():
    q = request.args.get('q', '').strip().lower()
    books = load_books()
    filtered = [b for b in books.values() if q == '' or (q in b['title'].lower() or q in b['author'].lower())]
    filtered = sorted(filtered, key=lambda x: x['title'])
    return render_template('catalog.html', books=filtered, query=q)

@app.route('/books/<int:book_id>')
@login_required
def show_book_details(book_id):
    books = load_books()
    if book_id not in books:
        abort(404)
    book = books[book_id]
    reviews = load_reviews()
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/borrow/confirm/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow_confirm(book_id):
    books = load_books()
    if book_id not in books:
        abort(404)
    book = books[book_id]
    if request.method == 'GET':
        if book['status'] != 'Available':
            flash('Book is not available for borrowing.')
            return redirect(url_for('show_book_details', book_id=book_id))
        due_date = datetime.now().date() + timedelta(days=14)
        return render_template('borrow_confirmation.html', book=book, due_date=due_date)
    else:
        username = session['username']
        if book['status'] != 'Available':
            flash('Book is not available to borrow.')
            return redirect(url_for('show_book_details', book_id=book_id))
        reservations = load_reservations()
        for r in reservations.values():
            if r['book_id'] == book_id and r['status'] == 'Active' and r['username'] != username:
                flash('Book is reserved by another user.')
                return redirect(url_for('show_book_details', book_id=book_id))
        borrowings = load_borrowings()
        new_borrow_id = max(borrowings.keys(), default=0) + 1
        now_str = datetime.now().date().strftime('%Y-%m-%d')
        due_str = (datetime.now().date() + timedelta(days=14)).strftime('%Y-%m-%d')
        borrowings[new_borrow_id] = {
            'borrow_id': new_borrow_id,
            'username': username,
            'book_id': book_id,
            'borrow_date': now_str,
            'due_date': due_str,
            'return_date': '',
            'status': 'Active',
            'fine_amount': 0
        }
        book['status'] = 'Borrowed'
        save_borrowings(borrowings)
        books[book_id] = book
        save_books(books)
        flash('Book borrowed successfully.')
        return redirect(url_for('list_user_borrowings'))

@app.route('/borrowings')
@login_required
def list_user_borrowings():
    username = session['username']
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()
    status_filter = request.args.get('status', 'All')
    filtered = []
    for b in borrowings.values():
        if b['username'] == username and (status_filter == 'All' or b['status'] == status_filter):
            if b['status'] == 'Active':
                due_date = datetime.strptime(b['due_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                if today > due_date:
                    b['status'] = 'Overdue'
                    overdue_days = (today - due_date).days
                    b['fine_amount'] = float(overdue_days)
                    existing_fine = None
                    for f in fines.values():
                        if f['borrow_id'] == b['borrow_id'] and f['status'] == 'Unpaid':
                            existing_fine = f
                            break
                    if not existing_fine:
                        new_fine_id = max(fines.keys(), default=0) + 1
                        fines[new_fine_id] = {
                            'fine_id': new_fine_id,
                            'username': username,
                            'borrow_id': b['borrow_id'],
                            'amount': b['fine_amount'],
                            'status': 'Unpaid',
                            'date_issued': today.strftime('%Y-%m-%d')
                        }
                    save_fines(fines)
                    save_borrowings(borrowings)
            filtered.append(b)
    return render_template('my_borrowings.html', borrowings=filtered, books=books, status_filter=status_filter)

@app.route('/borrowings/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    username = session['username']
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()
    if borrow_id not in borrowings:
        abort(404)
    borrow = borrowings[borrow_id]
    if borrow['username'] != username:
        abort(403)
    if borrow['status'] == 'Returned':
        flash('Book already returned.')
        return redirect(url_for('list_user_borrowings'))
    today = datetime.now().date()
    borrow['return_date'] = today.strftime('%Y-%m-%d')
    due_date = datetime.strptime(borrow['due_date'], '%Y-%m-%d').date()
    if today > due_date:
        overdue_days = (today - due_date).days
        borrow['status'] = 'Overdue'
        borrow['fine_amount'] = float(overdue_days)
        new_fine_id = max(fines.keys(), default=0) + 1
        fines[new_fine_id] = {
            'fine_id': new_fine_id,
            'username': username,
            'borrow_id': borrow_id,
            'amount': float(overdue_days),
            'status': 'Unpaid',
            'date_issued': today.strftime('%Y-%m-%d')
        }
    else:
        borrow['status'] = 'Returned'
        borrow['fine_amount'] = 0.0
    save_fines(fines)
    book_id = borrow['book_id']
    if book_id in books:
        books[book_id]['status'] = 'Available'
        save_books(books)
    save_borrowings(borrowings)
    flash('Book returned successfully.')
    return redirect(url_for('list_user_borrowings'))

@app.route('/reservations')
@login_required
def list_user_reservations():
    username = session['username']
    reservations = load_reservations()
    books = load_books()
    user_reservations = [r for r in reservations.values() if r['username'] == username]
    return render_template('my_reservations.html', reservations=user_reservations, books=books)

@app.route('/reservations/cancel/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    username = session['username']
    reservations = load_reservations()
    if reservation_id not in reservations:
        abort(404)
    reservation = reservations[reservation_id]
    if reservation['username'] != username:
        abort(403)
    if reservation['status'] != 'Active':
        flash('Reservation already cancelled.')
        return redirect(url_for('list_user_reservations'))
    reservation['status'] = 'Cancelled'
    save_reservations(reservations)
    book_id = reservation['book_id']
    books = load_books()
    active_reservations = [r for r in reservations.values() if r['book_id'] == book_id and r['status'] == 'Active']
    if not active_reservations and book_id in books:
        books[book_id]['status'] = 'Available'
        save_books(books)
    flash('Reservation cancelled.')
    return redirect(url_for('list_user_reservations'))

@app.route('/reviews')
@login_required
def list_user_reviews():
    username = session['username']
    reviews = load_reviews()
    books = load_books()
    user_reviews = [r for r in reviews.values() if r['username'] == username]
    return render_template('my_reviews.html', reviews=user_reviews, books=books)

@app.route('/reviews/write/<int:book_id>', methods=['GET', 'POST'])
@login_required
def write_review(book_id):
    books = load_books()
    if book_id not in books:
        abort(404)
    book = books[book_id]
    username = session['username']
    reviews = load_reviews()
    user_review = None
    for r in reviews.values():
        if r['book_id'] == book_id and r['username'] == username:
            user_review = r
            break
    if request.method == 'GET':
        return render_template('write_review.html', book=book, review=user_review)
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5.')
            return render_template('write_review.html', book=book, review=user_review)
    except (ValueError, TypeError):
        flash('Invalid rating.')
        return render_template('write_review.html', book=book, review=user_review)
    today_str = datetime.now().date().strftime('%Y-%m-%d')
    if user_review:
        user_review['rating'] = rating
        user_review['review_text'] = review_text
        user_review['review_date'] = today_str
    else:
        new_review_id = max(reviews.keys(), default=0) + 1
        reviews[new_review_id] = {
            'review_id': new_review_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }
    recalc_avg_rating(book_id, reviews, books)
    save_reviews(reviews)
    save_books(books)
    flash('Review submitted.')
    return redirect(url_for('show_book_details', book_id=book_id))

@app.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    username = session['username']
    reviews = load_reviews()
    if review_id not in reviews:
        abort(404)
    review = reviews[review_id]
    if review['username'] != username:
        abort(403)
    book_id = review['book_id']
    del reviews[review_id]
    books = load_books()
    recalc_avg_rating(book_id, reviews, books)
    save_reviews(reviews)
    save_books(books)
    flash('Review deleted.')
    return redirect(url_for('list_user_reviews'))

def recalc_avg_rating(book_id, reviews, books):
    ratings = [r['rating'] for r in reviews.values() if r['book_id'] == book_id]
    if ratings:
        avg = sum(ratings) / len(ratings)
    else:
        avg = 0.0
    if book_id in books:
        books[book_id]['avg_rating'] = round(avg, 1)

@app.route('/profile')
@login_required
def show_profile():
    username = session['username']
    users = load_users()
    if username not in users:
        abort(404)
    user = users[username]
    borrowings = load_borrowings()
    user_borrow_history = [b for b in borrowings.values() if b['username'] == username]
    books = load_books()
    return render_template('profile.html', user=user, username=username, borrow_history=user_borrow_history, email=user['email'], books=books)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = session['username']
    users = load_users()
    if username not in users:
        abort(404)
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    if not validate_email(email):
        flash('Invalid email address.')
        return redirect(url_for('show_profile'))
    user = users[username]
    user['email'] = email
    user['phone'] = phone
    user['address'] = address
    save_users(users)
    flash('Profile updated successfully.')
    return redirect(url_for('show_profile'))

@app.route('/fines/payment/<int:fine_id>', methods=['GET', 'POST'])
@login_required
def payment_fines(fine_id):
    username = session['username']
    fines = load_fines()
    if fine_id not in fines:
        abort(404)
    fine = fines[fine_id]
    if fine['username'] != username:
        abort(403)
    if request.method == 'GET':
        return render_template('payment_confirmation.html', fine=fine)
    fine['status'] = 'Paid'
    fines[fine_id] = fine
    save_fines(fines)
    flash('Fine payment successful.')
    return redirect(url_for('show_profile'))

if __name__ == '__main__':
    app.run(debug=True)
