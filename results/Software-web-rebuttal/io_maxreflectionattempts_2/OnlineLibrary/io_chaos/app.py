from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Paths to data files
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# Helper functions for file I/O and data parsing

def read_users():
    users = {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
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

def write_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving users file: {e}', 'error')


def read_books():
    books = {}
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 10:
                    book_id = int(parts[0])
                    title = parts[1]
                    author = parts[2]
                    isbn = parts[3]
                    genre = parts[4]
                    publisher = parts[5]
                    year = int(parts[6])
                    description = parts[7]
                    status = parts[8]
                    avg_rating = float(parts[9])
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

def write_books(books):
    try:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            for b in books.values():
                line = '|'.join([
                    str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'], 
                    b['publisher'], str(b['year']), b['description'], b['status'], f"{b['avg_rating']:.1f}"])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving books file: {e}', 'error')


def read_borrowings():
    borrowings = {}
    try:
        with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    borrow_id = int(parts[0])
                    username = parts[1]
                    book_id = int(parts[2])
                    borrow_date = parts[3]
                    due_date = parts[4]
                    return_date = parts[5] if parts[5] else None
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


def write_borrowings(borrowings):
    try:
        with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
            for b in borrowings.values():
                return_date_val = b['return_date'] if b['return_date'] else ''
                line = '|'.join([
                    str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'], 
                    b['due_date'], return_date_val, b['status'], f"{b['fine_amount']:.2f}"])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving borrowings file: {e}', 'error')


def read_reservations():
    reservations = {}
    try:
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
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


def write_reservations(reservations):
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for r in reservations.values():
                line = '|'.join([
                    str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
                ])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving reservations file: {e}', 'error')


def read_reviews():
    reviews = {}
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    review_id = int(parts[0])
                    username = parts[1]
                    book_id = int(parts[2])
                    rating = int(parts[3])
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


def write_reviews(reviews):
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for r in reviews.values():
                line = '|'.join([
                    str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
                ])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving reviews file: {e}', 'error')


def read_fines():
    fines = {}
    try:
        with open(FINES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    fine_id = int(parts[0])
                    username = parts[1]
                    borrow_id = int(parts[2])
                    amount = float(parts[3])
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


def write_fines(fines):
    try:
        with open(FINES_FILE, 'w', encoding='utf-8') as f:
            for fi in fines.values():
                line = '|'.join([
                    str(fi['fine_id']), fi['username'], str(fi['borrow_id']), f"{fi['amount']:.2f}", fi['status'], fi['date_issued']
                ])
                f.write(line + '\n')
    except Exception as e:
        flash(f'Error saving fines file: {e}', 'error')


# Dummy current logged-in user
# In real scenario, integrate proper authentication and user session
CURRENT_USER = 'john_reader'

# Util function: format date string YYYY-MM-DD

def format_date(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d')
    return dt

# Util function: calculate overdue fines
# For simplicity, assume $0.50 per day overdue

def calculate_fine(due_date_str, return_date_str=None):
    today = datetime.today()
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    actual_return = today if return_date_str is None else datetime.strptime(return_date_str, '%Y-%m-%d')
    overdue_days = (actual_return - due_date).days
    if overdue_days > 0:
        return round(overdue_days * 0.5, 2)
    return 0.0

# Route 1: Root redirect /
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Route 2: Dashboard
@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    return render_template('dashboard.html', username=username)

# Route 3: Book Catalog
@app.route('/catalog')
def book_catalog():
    books_all = read_books()
    books = []
    for book in books_all.values():
        # Only provide required fields for catalog
        books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'status': book['status']
        })
    return render_template('catalog.html', books=books)

# Route 4: Book Details
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    reviews_all = read_reviews()
    reviews = []
    for r in reviews_all.values():
        if r['book_id'] == book_id:
            reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    return render_template('book_details.html', book={
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status']
    }, reviews=reviews)

# Route 5: Borrow Confirmation Page GET
@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    borrow_date = datetime.today()
    due_date = borrow_date + timedelta(days=14)
    due_date_str = format_date(due_date)

    return render_template('borrow_confirmation.html', book={
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status']
    }, due_date=due_date_str)

# Route 6: Confirm Borrow POST
@app.route('/borrow/confirm', methods=['POST'])
def confirm_borrow():
    book_id = request.form.get('book_id')
    if not book_id:
        flash('No book specified to borrow.', 'error')
        return redirect(url_for('catalog'))
    try:
        book_id = int(book_id)
    except:
        flash('Invalid book ID.', 'error')
        return redirect(url_for('catalog'))

    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    borrowings = read_borrowings()
    # Check if user has active borrowing of this book
    for b in borrowings.values():
        if b['username'] == CURRENT_USER and b['book_id'] == book_id and b['status'] == 'Active':
            flash('You already have this book borrowed.', 'error')
            return redirect(url_for('my_borrows'))

    # New borrow_id
    borrow_id = max(borrowings.keys(), default=0) + 1
    borrow_date = datetime.today()
    due_date = borrow_date + timedelta(days=14)
    borrow_date_str = format_date(borrow_date)
    due_date_str = format_date(due_date)

    # Create borrow record
    new_borrow = {
        'borrow_id': borrow_id,
        'username': CURRENT_USER,
        'book_id': book_id,
        'borrow_date': borrow_date_str,
        'due_date': due_date_str,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    borrowings[borrow_id] = new_borrow

    # Update book status to Borrowed
    book['status'] = 'Borrowed'
    books[book_id] = book

    # Save data
    write_borrowings(borrowings)
    write_books(books)

    success = True
    return render_template('borrow_result.html', success=success, book={
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status']
    }, due_date=due_date_str)

# Route 7: My Borrowings Page GET
@app.route('/my-borrows')
def my_borrows():
    borrowings = read_borrowings()
    books = read_books()
    borrows = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            book = books.get(b['book_id'], {})
            # Update status for Overdue if needed
            if b['status'] == 'Active':
                due_date_dt = datetime.strptime(b['due_date'], '%Y-%m-%d')
                if datetime.today() > due_date_dt:
                    b['status'] = 'Overdue'
                    # Calculate fine
                    fine_amt = calculate_fine(b['due_date'])
                    b['fine_amount'] = fine_amt
                    borrowings[b['borrow_id']] = b
                else:
                    b['fine_amount'] = 0.0

            borrows.append({
                'borrow_id': b['borrow_id'],
                'title': book.get('title', 'Unknown'),
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            })
    # Save updated borrowings in case of status/fine changes
    write_borrowings(borrowings)
    return render_template('my_borrows.html', borrows=borrows)

# Route 8: Return Book POST
@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != CURRENT_USER:
        flash('Borrow record not found.', 'error')
        return render_template('return_result.html', success=False, borrow=None)

    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        flash('This borrow is not active and cannot be returned.', 'error')
        return render_template('return_result.html', success=False, borrow=borrow)

    return_date_str = format_date(datetime.today())
    borrow['return_date'] = return_date_str

    # Update status to Returned
    borrow['status'] = 'Returned'

    # Calculate fine if overdue
    fine = calculate_fine(borrow['due_date'], return_date_str)
    borrow['fine_amount'] = fine

    # Update book status to Available
    books = read_books()
    book = books.get(borrow['book_id'])
    if book:
        # Check if any active reservation for book
        reservations = read_reservations()
        has_active_reservation = any(
            r['book_id'] == book['book_id'] and r['status'] == 'Active' for r in reservations.values()
        )
        # If has active reservation, reserve book, else Available
        book['status'] = 'Reserved' if has_active_reservation else 'Available'
        books[book['book_id']] = book
        write_books(books)

    borrowings[borrow_id] = borrow
    write_borrowings(borrowings)

    # If fine issued and > 0, add fine record if not already exists
    if fine > 0:
        fines = read_fines()
        # Check if a fine already exists for this borrow_id
        fine_exists = any(fi['borrow_id'] == borrow_id for fi in fines.values())
        if not fine_exists:
            fine_id = max(fines.keys(), default=0) + 1
            fine_record = {
                'fine_id': fine_id,
                'username': CURRENT_USER,
                'borrow_id': borrow_id,
                'amount': fine,
                'status': 'Unpaid',
                'date_issued': return_date_str
            }
            fines[fine_id] = fine_record
            write_fines(fines)

    success = True
    return render_template('return_result.html', success=success, borrow={
        'borrow_id': borrow['borrow_id'],
        'book_id': borrow['book_id'],
        'borrow_date': borrow['borrow_date'],
        'due_date': borrow['due_date'],
        'return_date': borrow['return_date'],
        'status': borrow['status'],
        'fine_amount': borrow['fine_amount']
    })

# Route 9: My Reservations Page GET
@app.route('/my-reservations')
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    user_reservations = []
    for r in reservations.values():
        if r['username'] == CURRENT_USER:
            book = books.get(r['book_id'], {})
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'title': book.get('title', 'Unknown'),
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)

# Route 10: Cancel Reservation POST
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['username'] != CURRENT_USER:
        flash('Reservation not found.', 'error')
        return render_template('cancel_reservation_result.html', success=False, reservation=None)

    if reservation['status'] == 'Cancelled':
        flash('Reservation is already cancelled.', 'info')
        return render_template('cancel_reservation_result.html', success=False, reservation=reservation)

    reservation['status'] = 'Cancelled'
    reservations[reservation_id] = reservation
    write_reservations(reservations)

    success = True
    return render_template('cancel_reservation_result.html', success=success, reservation=reservation)

# Route 11: My Reviews Page GET
@app.route('/my-reviews')
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    user_reviews = []
    for r in reviews.values():
        if r['username'] == CURRENT_USER:
            book = books.get(r['book_id'], {})
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': book.get('title', 'Unknown'),
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

# Route 12: Write Review Page GET
@app.route('/write-review/<int:book_id>')
def write_review(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['book_id'] == book_id and r['username'] == CURRENT_USER:
            existing_review = {
                'review_id': r['review_id'],
                'username': r['username'],
                'book_id': r['book_id'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            }
            break

    return render_template('write_review.html', book={
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status']
    }, existing_review=existing_review)

# Route 13: Submit Review POST
@app.route('/submit-review/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating:
        flash('Rating is required.', 'error')
        return redirect(url_for('write_review', book_id=book_id))
    try:
        rating = int(rating)
    except:
        flash('Invalid rating value.', 'error')
        return redirect(url_for('write_review', book_id=book_id))

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('write_review', book_id=book_id))

    if not review_text:
        flash('Review text cannot be empty.', 'error')
        return redirect(url_for('write_review', book_id=book_id))

    reviews = read_reviews()
    # Check if user already has a review for this book; if yes, redirect to edit route
    existing_review_id = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review_id = r['review_id']
            break

    now_str = format_date(datetime.today())

    if existing_review_id:
        flash('Review already exists. Please edit your review.', 'info')
        return redirect(url_for('write_review', book_id=book_id))

    # New review id
    review_id = max(reviews.keys(), default=0) + 1
    new_review = {
        'review_id': review_id,
        'username': CURRENT_USER,
        'book_id': book_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': now_str
    }

    reviews[review_id] = new_review
    write_reviews(reviews)

    success = True
    return render_template('review_result.html', success=success, book={
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status']
    })

# Route 14: Edit Review POST
@app.route('/edit-review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USER:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating:
        flash('Rating is required.', 'error')
        return redirect(url_for('my_reviews'))
    try:
        rating = int(rating)
    except:
        flash('Invalid rating value.', 'error')
        return redirect(url_for('my_reviews'))

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('my_reviews'))

    if not review_text:
        flash('Review text cannot be empty.', 'error')
        return redirect(url_for('my_reviews'))

    # Update review
    review['rating'] = rating
    review['review_text'] = review_text
    review['review_date'] = format_date(datetime.today())
    reviews[review_id] = review
    write_reviews(reviews)
    flash('Review updated successfully.', 'success')
    return redirect(url_for('my_reviews'))

# Route 15: Delete Review POST
@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USER:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    del reviews[review_id]
    write_reviews(reviews)
    flash('Review deleted successfully.', 'success')
    return redirect(url_for('my_reviews'))

# Route 16: User Profile GET
@app.route('/profile')
def user_profile():
    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))

    borrowings = read_borrowings()
    books = read_books()
    borrow_history = []
    # Previously borrowed books include Returned or Overdue with return_date
    for b in borrowings.values():
        if b['username'] == CURRENT_USER and b['return_date'] is not None:
            book = books.get(b['book_id'], {})
            borrow_history.append({
                'title': book.get('title', 'Unknown'),
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', username=user['username'], email=user['email'], borrow_history=borrow_history)

# Route 17: Update Profile POST
@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    if not email:
        flash('Email cannot be empty.', 'error')
        return render_template('profile_update_result.html', success=False, username=CURRENT_USER, email=email)

    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        flash('User not found.', 'error')
        return render_template('profile_update_result.html', success=False, username=CURRENT_USER, email=email)

    user['email'] = email
    users[CURRENT_USER] = user
    write_users(users)

    success = True
    flash('Profile updated successfully.', 'success')
    return render_template('profile_update_result.html', success=success, username=CURRENT_USER, email=email)

# Route 18: Payment Confirmation Page GET
@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USER:
        flash('Fine record not found.', 'error')
        return redirect(url_for('user_profile'))

    return render_template('payment_confirmation.html', fine_amount=fine['amount'], fine_id=fine_id)

# Route 19: Confirm Payment POST
@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USER:
        flash('Fine record not found.', 'error')
        return render_template('payment_result.html', success=False, fine_id=fine_id)

    if fine['status'] == 'Paid':
        flash('Fine already paid.', 'info')
        return render_template('payment_result.html', success=False, fine_id=fine_id)

    fine['status'] = 'Paid'
    fines[fine_id] = fine
    write_fines(fines)

    success = True
    flash('Payment successful.', 'success')
    return render_template('payment_result.html', success=success, fine_id=fine_id)


if __name__ == '__main__':
    app.run(debug=True)
