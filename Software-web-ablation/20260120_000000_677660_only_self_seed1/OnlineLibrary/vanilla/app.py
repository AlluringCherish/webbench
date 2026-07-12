from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility functions to load and save data

# USERS
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# For simplicity in this implementation, emulate a logged-in user (to be replaced with real auth)
CURRENT_USERNAME = 'john_reader'

# Load all users
# user: {username, email, phone, address}
def load_users():
    users = {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, address = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                }
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load all books
# book dict with keys per spec
# book_id:int, title:str, author:str, isbn:str, genre:str, publisher:str, year:int, description:str, status:str, avg_rating:float

def load_books():
    books = {}
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 10:
                    continue
                book_id = int(parts[0])
                title = parts[1]
                author = parts[2]
                isbn = parts[3]
                genre = parts[4]
                publisher = parts[5]
                year = int(parts[6])
                description = parts[7]
                status = parts[8]
                try:
                    avg_rating = float(parts[9])
                except Exception:
                    avg_rating = 0.0
                books[book_id] = {
                    'book_id': book_id,
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'genre': genre,
                    'publisher': publisher,
                    'year': year,
                    'description': description,
                    'status': status,
                    'avg_rating': avg_rating
                }
    except FileNotFoundError:
        pass
    return books

def save_books(books):
    try:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            for b in books.values():
                line = '|'.join([
                    str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'],
                    b['publisher'], str(b['year']), b['description'], b['status'],
                    f"{b['avg_rating']:.1f}"
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load borrowings
# borrow_id (int), username (str), book_id (int), borrow_date (str YYYY-MM-DD), due_date (str), return_date (str or empty), status (str), fine_amount (float)

def load_borrowings():
    borrowings = {}
    try:
        with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                borrow_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                borrow_date = parts[3]
                due_date = parts[4]
                return_date = parts[5] if parts[5] != '' else None
                status = parts[6]
                try:
                    fine_amount = float(parts[7])
                except:
                    fine_amount = 0.0
                borrowings[borrow_id] = {
                    'borrow_id': borrow_id,
                    'username': username,
                    'book_id': book_id,
                    'borrow_date': borrow_date,
                    'due_date': due_date,
                    'return_date': return_date,
                    'status': status,
                    'fine_amount': fine_amount
                }
    except FileNotFoundError:
        pass
    return borrowings

def save_borrowings(borrowings):
    try:
        with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
            for b in borrowings.values():
                line = '|'.join([
                    str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'], b['due_date'],
                    b['return_date'] if b['return_date'] else '', b['status'], f"{b['fine_amount']:.2f}"
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load reservations
# reservation_id (int), username (str), book_id (int), reservation_date (str), status (str)
def load_reservations():
    reservations = {}
    try:
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                reservation_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                reservation_date = parts[3]
                status = parts[4]
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': username,
                    'book_id': book_id,
                    'reservation_date': reservation_date,
                    'status': status
                }
    except FileNotFoundError:
        pass
    return reservations

def save_reservations(reservations):
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for r in reservations.values():
                line = '|'.join([
                    str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load reviews
# review_id (int), username (str), book_id (int), rating (int), review_text (str), review_date (str)
def load_reviews():
    reviews = {}
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.rstrip('\n')
                if not line:
                    continue
                # review_text might contain pipes, so we must split exactly 6 fields first 5 then rest is review_text
                parts = line.split('|', 5)
                if len(parts) != 6:
                    continue
                review_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                try:
                    rating = int(parts[3])
                except:
                    rating = 0
                review_text = parts[4]
                review_date = parts[5]
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': username,
                    'book_id': book_id,
                    'rating': rating,
                    'review_text': review_text,
                    'review_date': review_date
                }
    except FileNotFoundError:
        pass
    return reviews

def save_reviews(reviews):
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for r in reviews.values():
                line = '|'.join([
                    str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Load fines
# fine_id (int), username (str), borrow_id (int), amount (float), status (str), date_issued (str)
def load_fines():
    fines = {}
    try:
        with open(FINES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                fine_id = int(parts[0])
                username = parts[1]
                borrow_id = int(parts[2])
                try:
                    amount = float(parts[3])
                except:
                    amount = 0.0
                status = parts[4]
                date_issued = parts[5]
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': username,
                    'borrow_id': borrow_id,
                    'amount': amount,
                    'status': status,
                    'date_issued': date_issued
                }
    except FileNotFoundError:
        pass
    return fines

def save_fines(fines):
    try:
        with open(FINES_FILE, 'w', encoding='utf-8') as f:
            for fn in fines.values():
                line = '|'.join([
                    str(fn['fine_id']), fn['username'], str(fn['borrow_id']), f"{fn['amount']:.2f}", fn['status'], fn['date_issued']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Find next ID helper

def get_next_id(items: dict):
    if not items:
        return 1
    return max(items.keys()) + 1

# Helpers for dates

def parse_date(s: str):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except:
        return None

def format_date(d):
    if not d:
        return ''
    return d.strftime('%Y-%m-%d')

# Business logic helpers

def calculate_due_date(borrow_date: datetime.date):
    # due 14 days from borrow date
    return borrow_date + timedelta(days=14)

# Check if user_has_borrowed book and active

def has_user_borrowed_book(username: str, book_id: int):
    borrowings = load_borrowings()
    for b in borrowings.values():
        if b['username'] == username and b['book_id'] == book_id and b['status'] == 'Active':
            return True
    return False

# Update book status according to borrowings and reservations
# but in this design, status in books.txt is authoritative

# Calculate total unpaid fines for user

def calculate_total_unpaid_fines(username: str):
    fines = load_fines()
    total = 0.0
    for fn in fines.values():
        if fn['username'] == username and fn['status'] == 'Unpaid':
            total += fn['amount']
    return total

# Get borrow history for user

def get_borrow_history(username: str):
    borrowings = load_borrowings()
    books = load_books()
    history = []
    for b in borrowings.values():
        if b['username'] == username:
            book = books.get(b['book_id'])
            title = book['title'] if book else 'Unknown'
            history.append({
                'book_id': b['book_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })
    return history

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    # Provide username to dashboard
    return render_template('dashboard.html', username=CURRENT_USERNAME)

@app.route('/catalog')
def book_catalog_page():
    books = load_books()
    book_list = list(books.values())
    return render_template('catalog.html', books=book_list)

@app.route('/book/<int:book_id>')
def book_details_page(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    reviews = load_reviews()
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    user_has_borrowed_flag = has_user_borrowed_book(CURRENT_USERNAME, book_id)
    return render_template('book_details.html', book=book, reviews=book_reviews, user_has_borrowed=user_has_borrowed_flag)

@app.route('/borrow/<int:book_id>')
def borrow_confirmation_page(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details_page', book_id=book_id))

    # Calculate due date (today + 14 days)
    borrow_date = datetime.today().date()
    due_date = calculate_due_date(borrow_date)
    due_date_str = format_date(due_date)

    return render_template('borrow_confirmation.html', book=book, due_date=due_date_str)

@app.route('/borrow/confirm', methods=['POST'])
def confirm_borrow_book():
    book_id = request.form.get('book_id', type=int)
    if book_id is None:
        flash('Book ID missing.')
        return render_template('borrow_result.html', success=False, message='Book ID missing.')

    books = load_books()
    book = books.get(book_id)
    if not book:
        return render_template('borrow_result.html', success=False, message='Book not found.')

    if book['status'] != 'Available':
        return render_template('borrow_result.html', success=False, message='Book is not available for borrowing.')

    borrowings = load_borrowings()
    # generate new borrow_id
    next_borrow_id = get_next_id(borrowings)
    borrow_date = datetime.today().date()
    due_date = calculate_due_date(borrow_date)
    # Add borrowing record
    new_borrow = {
        'borrow_id': next_borrow_id,
        'username': CURRENT_USERNAME,
        'book_id': book_id,
        'borrow_date': format_date(borrow_date),
        'due_date': format_date(due_date),
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings[next_borrow_id] = new_borrow

    # Update book status
    book['status'] = 'Borrowed'
    books[book_id] = book

    # Save data
    if save_borrowings(borrowings) and save_books(books):
        return render_template('borrow_result.html', success=True, message='Book borrowed successfully.')
    else:
        return render_template('borrow_result.html', success=False, message='Failed to update data.')

@app.route('/my-borrows')
def my_borrowings_page():
    borrowings = load_borrowings()
    books = load_books()
    user_borrows = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USERNAME:
            book = books.get(b['book_id'])
            title = book['title'] if book else 'Unknown'
            # If overdue and still active, mark as Overdue
            if b['status'] == 'Active':
                due_dt = parse_date(b['due_date'])
                today = datetime.today().date()
                if due_dt and today > due_dt:
                    b['status'] = 'Overdue'
            borrow_entry = {
                'borrow_id': b['borrow_id'],
                'book_id': b['book_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'return_date': b['return_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            }
            user_borrows.append(borrow_entry)

    # Save borrowings back to file if any status changes
    save_borrowings(borrowings)

    return render_template('my_borrows.html', borrows=user_borrows)

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_borrowed_book(borrow_id):
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    borrow = borrowings.get(borrow_id)
    if not borrow:
        return render_template('return_result.html', success=False, message='Borrow record not found.')

    if borrow['username'] != CURRENT_USERNAME:
        return render_template('return_result.html', success=False, message='Not authorized.')

    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        return render_template('return_result.html', success=False, message='Book is not currently borrowed.')

    # Calculate if overdue and fine
    due_dt = parse_date(borrow['due_date'])
    return_dt = datetime.today().date()
    fine_amount = 0.0
    if due_dt and return_dt > due_dt:
        overdue_days = (return_dt - due_dt).days
        # For simplicity, $1 per overdue day
        fine_amount = float(overdue_days)

    borrow['return_date'] = format_date(return_dt)
    borrow['status'] = 'Returned'
    borrow['fine_amount'] = fine_amount

    # Update book status to Available
    book = books.get(borrow['book_id'])
    if book:
        book['status'] = 'Available'
        books[book['book_id']] = book

    # Save borrowings and books
    bsave = save_borrowings(borrowings)
    bksave = save_books(books)
    fsave = True

    # If fine > 0 create fine record or update existing
    if fine_amount > 0:
        # Check if fine record exists for this borrow
        existing_fine = None
        for fn in fines.values():
            if fn['borrow_id'] == borrow_id and fn['username'] == CURRENT_USERNAME and fn['status'] == 'Unpaid':
                existing_fine = fn
                break
        if existing_fine:
            existing_fine['amount'] = fine_amount
            existing_fine['date_issued'] = format_date(return_dt)
        else:
            next_fine_id = get_next_id(fines)
            fines[next_fine_id] = {
                'fine_id': next_fine_id,
                'username': CURRENT_USERNAME,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': format_date(return_dt)
            }
        fsave = save_fines(fines)

    if bsave and bksave and fsave:
        msg = 'Book returned successfully.'
        if fine_amount > 0:
            msg += f' You have a fine of ${fine_amount:.2f}.'
        return render_template('return_result.html', success=True, message=msg)
    else:
        return render_template('return_result.html', success=False, message='Failed to update records.')

@app.route('/my-reservations')
def my_reservations_page():
    reservations = load_reservations()
    books = load_books()
    user_reservations = []
    for r in reservations.values():
        if r['username'] == CURRENT_USERNAME:
            book = books.get(r['book_id'])
            title = book['title'] if book else 'Unknown'
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_id': r['book_id'],
                'title': title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    res = reservations.get(reservation_id)
    if not res:
        return render_template('cancel_reservation_result.html', success=False, message='Reservation not found.')

    if res['username'] != CURRENT_USERNAME:
        return render_template('cancel_reservation_result.html', success=False, message='Not authorized.')

    if res['status'] == 'Cancelled':
        return render_template('cancel_reservation_result.html', success=False, message='Reservation already cancelled.')

    res['status'] = 'Cancelled'
    reservations[reservation_id] = res
    if save_reservations(reservations):
        return render_template('cancel_reservation_result.html', success=True, message='Reservation cancelled successfully.')
    else:
        return render_template('cancel_reservation_result.html', success=False, message='Failed to update reservation.')

@app.route('/my-reviews')
def my_reviews_page():
    reviews = load_reviews()
    books = load_books()
    user_reviews = []
    for r in reviews.values():
        if r['username'] == CURRENT_USERNAME:
            book = books.get(r['book_id'])
            title = book['title'] if book else 'Unknown'
            user_reviews.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'title': title,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/review/write/<int:book_id>')
def write_review_page(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    reviews = load_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == CURRENT_USERNAME and r['book_id'] == book_id:
            existing_review = r
            break
    return render_template('write_review.html', book=book, existing_review=existing_review)

@app.route('/review/submit', methods=['POST'])
def submit_review():
    book_id = request.form.get('book_id', type=int)
    rating = request.form.get('rating', type=int)
    review_text = request.form.get('review_text', '').strip()

    if book_id is None or rating is None or rating < 1 or rating > 5:
        return render_template('review_submission_result.html', success=False, message='Invalid rating or book ID.')

    books = load_books()
    book = books.get(book_id)
    if not book:
        return render_template('review_submission_result.html', success=False, message='Book not found.')

    reviews = load_reviews()
    # Check if user has existing review
    existing_review_id = None
    for r in reviews.values():
        if r['username'] == CURRENT_USERNAME and r['book_id'] == book_id:
            existing_review_id = r['review_id']
            break
    today_str = format_date(datetime.today().date())
    if existing_review_id:
        # Update review
        reviews[existing_review_id]['rating'] = rating
        reviews[existing_review_id]['review_text'] = review_text
        reviews[existing_review_id]['review_date'] = today_str
    else:
        # New review
        next_review_id = get_next_id(reviews)
        reviews[next_review_id] = {
            'review_id': next_review_id,
            'username': CURRENT_USERNAME,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }
    # Save
    if save_reviews(reviews):
        return render_template('review_submission_result.html', success=True, message='Review submitted successfully.')
    else:
        return render_template('review_submission_result.html', success=False, message='Failed to save review.')

@app.route('/review/edit/<int:review_id>')
def edit_review_page(review_id):
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review:
        flash('Review not found.')
        return redirect(url_for('my_reviews_page'))

    if review['username'] != CURRENT_USERNAME:
        flash('Not authorized to edit this review.')
        return redirect(url_for('my_reviews_page'))

    books = load_books()
    book = books.get(review['book_id'])
    if not book:
        flash('Book not found.')
        return redirect(url_for('my_reviews_page'))

    return render_template('write_review.html', book=book, existing_review=review)

@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review:
        return render_template('delete_review_result.html', success=False, message='Review not found.')

    if review['username'] != CURRENT_USERNAME:
        return render_template('delete_review_result.html', success=False, message='Not authorized.')

    del reviews[review_id]
    if save_reviews(reviews):
        return render_template('delete_review_result.html', success=True, message='Review deleted successfully.')
    else:
        return render_template('delete_review_result.html', success=False, message='Failed to delete review.')

@app.route('/profile')
def user_profile_page():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        flash('User not found.')
        # For simplicity redirect to dashboard
        return redirect(url_for('dashboard_page'))
    borrow_history = get_borrow_history(CURRENT_USERNAME)
    total_fines = calculate_total_unpaid_fines(CURRENT_USERNAME)
    return render_template('profile.html', user=user, borrow_history=borrow_history, total_fines=total_fines)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not email or not phone or not address:
        return render_template('profile_update_result.html', success=False, message='Please fill all fields.')

    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        return render_template('profile_update_result.html', success=False, message='User not found.')

    user['email'] = email
    user['phone'] = phone
    user['address'] = address
    users[CURRENT_USERNAME] = user

    if save_users(users):
        return render_template('profile_update_result.html', success=True, message='Profile updated successfully.')
    else:
        return render_template('profile_update_result.html', success=False, message='Failed to update profile.')

@app.route('/payment/<int:fine_id>')
def payment_confirmation_page(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        flash('Fine not found.')
        return redirect(url_for('user_profile_page'))
    if fine['username'] != CURRENT_USERNAME:
        flash('Not authorized.')
        return redirect(url_for('user_profile_page'))
    return render_template('payment_confirmation.html', fine=fine)

@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        return render_template('payment_result.html', success=False, message='Fine not found.')
    if fine['username'] != CURRENT_USERNAME:
        return render_template('payment_result.html', success=False, message='Not authorized.')

    if fine['status'] == 'Paid':
        return render_template('payment_result.html', success=False, message='Fine already paid.')

    fine['status'] = 'Paid'
    fines[fine_id] = fine
    if save_fines(fines):
        return render_template('payment_result.html', success=True, message='Fine paid successfully.')
    else:
        return render_template('payment_result.html', success=False, message='Failed to update fine.')


if __name__ == '__main__':
    app.run(debug=True)
