from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility functions to read and write data files

# USERS
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')


def read_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 4:
                continue
            username, email, phone, address = fields
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users


def write_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            f.write(line + '\n')


def read_books():
    books = {}
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 10:
                continue
            book_id = int(fields[0])
            books[book_id] = {
                'book_id': book_id,
                'title': fields[1],
                'author': fields[2],
                'isbn': fields[3],
                'genre': fields[4],
                'publisher': fields[5],
                'year': int(fields[6]),
                'description': fields[7],
                'status': fields[8],
                'avg_rating': float(fields[9])
            }
    return books


def write_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        for b in books.values():
            line = '|'.join([
                str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'],
                b['publisher'], str(b['year']), b['description'], b['status'],
                f"{b['avg_rating']:.1f}"
            ])
            f.write(line + '\n')


def read_borrowings():
    borrowings = {}
    if not os.path.exists(BORROWINGS_FILE):
        return borrowings
    with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 8:
                continue
            borrow_id = int(fields[0])
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': fields[1],
                'book_id': int(fields[2]),
                'borrow_date': fields[3],
                'due_date': fields[4],
                'return_date': fields[5],
                'status': fields[6],
                'fine_amount': float(fields[7])
            }
    return borrowings


def write_borrowings(borrowings):
    with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            line = '|'.join([
                str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'],
                b['due_date'], b['return_date'], b['status'], f"{b['fine_amount']:.2f}"
            ])
            f.write(line + '\n')


def read_reservations():
    reservations = {}
    if not os.path.exists(RESERVATIONS_FILE):
        return reservations
    with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 5:
                continue
            reservation_id = int(fields[0])
            reservations[reservation_id] = {
                'reservation_id': reservation_id,
                'username': fields[1],
                'book_id': int(fields[2]),
                'reservation_date': fields[3],
                'status': fields[4]
            }
    return reservations


def write_reservations(reservations):
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = '|'.join([
                str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
            ])
            f.write(line + '\n')


def read_reviews():
    reviews = {}
    if not os.path.exists(REVIEWS_FILE):
        return reviews
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 6:
                continue
            review_id = int(fields[0])
            reviews[review_id] = {
                'review_id': review_id,
                'username': fields[1],
                'book_id': int(fields[2]),
                'rating': int(fields[3]),
                'review_text': fields[4],
                'review_date': fields[5]
            }
    return reviews


def write_reviews(reviews):
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
            ])
            f.write(line + '\n')


def read_fines():
    fines = {}
    if not os.path.exists(FINES_FILE):
        return fines
    with open(FINES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) < 6:
                continue
            fine_id = int(fields[0])
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': fields[1],
                'borrow_id': int(fields[2]),
                'amount': float(fields[3]),
                'status': fields[4],
                'date_issued': fields[5]
            }
    return fines


def write_fines(fines):
    with open(FINES_FILE, 'w', encoding='utf-8') as f:
        for fn in fines.values():
            line = '|'.join([
                str(fn['fine_id']), fn['username'], str(fn['borrow_id']), f"{fn['amount']:.2f}", fn['status'], fn['date_issued']
            ])
            f.write(line + '\n')


# Helper functions

def get_logged_in_username():
    # For demo/testing, use a static username
    # In real app, this would come from session or auth
    # Change here if needed or expand auth later
    return 'john_reader'


def calculate_due_date(borrow_date_str):
    borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
    due_date = borrow_date + timedelta(days=14)
    return due_date.strftime('%Y-%m-%d')


def update_book_status(book_id, status):
    books = read_books()
    if book_id in books:
        books[book_id]['status'] = status
        write_books(books)


def calculate_overdue_fine(due_date_str, return_date_str):
    due = datetime.strptime(due_date_str, '%Y-%m-%d')
    if return_date_str:
        ret = datetime.strptime(return_date_str, '%Y-%m-%d')
    else:
        ret = datetime.now()
    if ret > due:
        days_overdue = (ret - due).days
        return float(days_overdue) * 0.5  # assuming 0.5 currency units per day overdue
    return 0


def get_avg_rating_for_book(book_id, reviews):
    ratings = [r['rating'] for r in reviews.values() if r['book_id'] == book_id]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    return 0.0


# ROUTES

# 1. Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# 2. Dashboard Page
@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username()
    return render_template('dashboard.html', username=username)


# 3. Book Catalog Page
@app.route('/catalog')
def book_catalog():
    books = read_books()
    # Determine status per book:
    # If any active borrowing for the book => Borrowed
    # Else if any active reservation => Reserved
    # Else Available
    borrowings = read_borrowings()
    reservations = read_reservations()

    book_status_map = {}
    for b in books.values():
        book_status_map[b['book_id']] = 'Available'

    for b_id in book_status_map:
        for br in borrowings.values():
            if br['book_id'] == b_id and br['status'] == 'Active':
                book_status_map[b_id] = 'Borrowed'
                break
        else:
            # Only check reservations if not borrowed
            for r in reservations.values():
                if r['book_id'] == b_id and r['status'] == 'Active':
                    book_status_map[b_id] = 'Reserved'
                    break

    # Prepare list for template
    books_list = []
    for b in books.values():
        books_list.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': book_status_map.get(b['book_id'], 'Available')
        })

    return render_template('catalog.html', books=books_list)


# 4. Book Details Page
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    reviews = read_reviews()
    reviews_list = [
        {
            'review_id': r['review_id'],
            'username': r['username'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        }
        for r in reviews.values() if r['book_id'] == book_id
    ]

    return render_template('book_details.html', book=book, reviews=reviews_list)


# 5. Borrow Confirmation Page
# GET to display confirmation
@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    today = datetime.now().strftime('%Y-%m-%d')
    due_date = calculate_due_date(today)

    # Check if book is borrowable
    book_status = book['status']
    borrowings = read_borrowings()
    reservations = read_reservations()

    for br in borrowings.values():
        if br['book_id'] == book_id and br['status'] == 'Active':
            flash('Book is currently borrowed and not available.', 'error')
            return redirect(url_for('book_details', book_id=book_id))

    for r in reservations.values():
        if r['book_id'] == book_id and r['status'] == 'Active':
            flash('Book is currently reserved and not available.', 'error')
            return redirect(url_for('book_details', book_id=book_id))

    return render_template('borrow_confirmation.html', book=book, due_date=due_date)


# POST to confirm borrow
@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def confirm_borrow(book_id):
    username = get_logged_in_username()
    books = read_books()
    borrowings = read_borrowings()

    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    # Check if book is borrowable
    for br in borrowings.values():
        if br['book_id'] == book_id and br['status'] == 'Active':
            flash('Book is currently borrowed and not available.', 'error')
            return redirect(url_for('book_details', book_id=book_id))

    reservations = read_reservations()
    for r in reservations.values():
        if r['book_id'] == book_id and r['status'] == 'Active' and r['username'] != username:
            flash('Book is currently reserved by another user.', 'error')
            return redirect(url_for('book_details', book_id=book_id))

    # Add new borrowing
    today = datetime.now().strftime('%Y-%m-%d')
    due_date = calculate_due_date(today)

    next_borrow_id = max(borrowings.keys(), default=0) + 1

    borrowings[next_borrow_id] = {
        'borrow_id': next_borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': today,
        'due_date': due_date,
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }

    # Update book status
    update_book_status(book_id, 'Borrowed')

    write_borrowings(borrowings)

    flash('Book borrowed successfully.', 'success')
    return redirect(url_for('my_borrows'))


# POST or GET to cancel borrow and return to book details
@app.route('/borrow/<int:book_id>/cancel', methods=['GET', 'POST'])
def cancel_borrow(book_id):
    return redirect(url_for('book_details', book_id=book_id))


# 6. My Borrowings Page
@app.route('/my_borrows')
def my_borrows():
    username = get_logged_in_username()
    borrowings = read_borrowings()
    books = read_books()

    # Optionally filter by status query parameter
    filter_status = request.args.get('filter', 'All')

    user_borrows = []
    for br in borrowings.values():
        if br['username'] == username:
            if filter_status != 'All' and br['status'] != filter_status:
                continue
            book_title = books.get(br['book_id'], {}).get('title', 'Unknown')
            user_borrows.append({
                'borrow_id': br['borrow_id'],
                'book_title': book_title,
                'borrow_date': br['borrow_date'],
                'due_date': br['due_date'],
                'status': br['status']
            })

    return render_template('my_borrows.html', borrowings=user_borrows, filter_status=filter_status)


# POST to return book
@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_logged_in_username()
    borrowings = read_borrowings()
    books = read_books()
    fines = read_fines()

    if borrow_id not in borrowings:
        flash('Borrowing record not found.', 'error')
        return redirect(url_for('my_borrows'))

    br = borrowings[borrow_id]

    if br['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('my_borrows'))

    if br['status'] != 'Active':
        flash('Book is not currently borrowed.', 'error')
        return redirect(url_for('my_borrows'))

    # Mark return date
    return_date = datetime.now().strftime('%Y-%m-%d')
    br['return_date'] = return_date

    # Check if overdue and calculate fine
    fine_amount = calculate_overdue_fine(br['due_date'], return_date)
    br['fine_amount'] = fine_amount

    if fine_amount > 0:
        br['status'] = 'Overdue'
        # Add to fines
        next_f_id = max(fines.keys(), default=0) + 1
        fines[next_f_id] = {
            'fine_id': next_f_id,
            'username': username,
            'borrow_id': borrow_id,
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': return_date
        }
        write_fines(fines)
    else:
        br['status'] = 'Returned'

    # Update book status to Available
    update_book_status(br['book_id'], 'Available')

    write_borrowings(borrowings)

    flash('Book returned successfully.', 'success')
    return redirect(url_for('my_borrows'))


# 7. My Reservations Page
@app.route('/my_reservations')
def my_reservations():
    username = get_logged_in_username()
    reservations = read_reservations()
    books = read_books()

    user_reservations = []
    for r in reservations.values():
        if r['username'] == username:
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_title': books.get(r['book_id'], {}).get('title', 'Unknown'),
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)


# POST to cancel reservation
@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_logged_in_username()
    reservations = read_reservations()

    if reservation_id not in reservations:
        flash('Reservation not found.', 'error')
        return redirect(url_for('my_reservations'))

    r = reservations[reservation_id]
    if r['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('my_reservations'))

    r['status'] = 'Cancelled'

    write_reservations(reservations)
    flash('Reservation cancelled.', 'success')
    return redirect(url_for('my_reservations'))


# 8. My Reviews Page
@app.route('/my_reviews')
def my_reviews():
    username = get_logged_in_username()
    reviews = read_reviews()
    books = read_books()

    user_reviews = []
    for r in reviews.values():
        if r['username'] == username:
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': books.get(r['book_id'], {}).get('title', 'Unknown'),
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)


# GET to show edit form
@app.route('/edit_review/<int:review_id>')
def edit_review(review_id):
    username = get_logged_in_username()
    reviews = read_reviews()
    books = read_books()

    if review_id not in reviews:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    review = reviews[review_id]
    if review['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('my_reviews'))

    book = books.get(review['book_id'])
    if not book:
        flash('Associated book not found.', 'error')
        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', review=review, book=book)


# POST to submit edit
@app.route('/edit_review/<int:review_id>/submit', methods=['POST'])
def submit_edit_review(review_id):
    username = get_logged_in_username()
    reviews = read_reviews()

    if review_id not in reviews:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    review = reviews[review_id]
    if review['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('my_reviews'))

    rating = int(request.form.get('rating', 0))
    review_text = request.form.get('review_text', '').strip()

    if rating < 1 or rating > 5 or not review_text:
        flash('Invalid rating or review text.', 'error')
        return redirect(url_for('edit_review', review_id=review_id))

    review['rating'] = rating
    review['review_text'] = review_text
    review['review_date'] = datetime.now().strftime('%Y-%m-%d')

    write_reviews(reviews)
    flash('Review updated successfully.', 'success')
    return redirect(url_for('my_reviews'))


# POST to delete review
@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    username = get_logged_in_username()
    reviews = read_reviews()

    if review_id not in reviews:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    review = reviews[review_id]
    if review['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('my_reviews'))

    del reviews[review_id]
    write_reviews(reviews)

    flash('Review deleted successfully.', 'success')
    return redirect(url_for('my_reviews'))


# 9. Write Review Page (New Review)
# GET to display form
@app.route('/write_review/<int:book_id>')
def write_review(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    return render_template('write_review.html', book=book)


# POST to submit new review
@app.route('/write_review/<int:book_id>/submit', methods=['POST'])
def submit_review(book_id):
    username = get_logged_in_username()
    reviews = read_reviews()

    rating = int(request.form.get('rating', 0))
    review_text = request.form.get('review_text', '').strip()

    if rating < 1 or rating > 5 or not review_text:
        flash('Invalid rating or review text.', 'error')
        return redirect(url_for('write_review', book_id=book_id))

    # Generate next review_id
    next_review_id = max(reviews.keys(), default=0) + 1

    review_date = datetime.now().strftime('%Y-%m-%d')

    reviews[next_review_id] = {
        'review_id': next_review_id,
        'username': username,
        'book_id': book_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }

    write_reviews(reviews)

    flash('Review submitted successfully.', 'success')
    return redirect(url_for('book_details', book_id=book_id))


# 10. User Profile Page
@app.route('/profile')
def user_profile():
    username = get_logged_in_username()
    users = read_users()
    borrowings = read_borrowings()
    books = read_books()

    user = users.get(username)
    if not user:
        flash('User profile not found.', 'error')
        return redirect(url_for('dashboard'))

    borrow_history = []
    for br in borrowings.values():
        if br['username'] == username:
            borrow_history.append({
                'book_title': books.get(br['book_id'], {}).get('title', 'Unknown'),
                'borrow_date': br['borrow_date'],
                'return_date': br['return_date'] or ''
            })

    return render_template('profile.html', username=username, email=user['email'], borrow_history=borrow_history)


# POST to update profile email
@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = get_logged_in_username()
    users = read_users()

    if username not in users:
        flash('User not found.', 'error')
        return redirect(url_for('user_profile'))

    email = request.form.get('email', '').strip()

    if not email:
        flash('Email cannot be empty.', 'error')
        return redirect(url_for('user_profile'))

    users[username]['email'] = email
    write_users(users)
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('user_profile'))


# 11. Payment Confirmation Page
@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    fines = read_fines()
    if fine_id not in fines:
        flash('Fine not found.', 'error')
        return redirect(url_for('user_profile'))
    fine = fines[fine_id]

    return render_template('payment_confirmation.html', fine_amount=fine['amount'], fine_id=fine_id)


@app.route('/payment/<int:fine_id>/confirm', methods=['POST'])
def confirm_payment(fine_id):
    username = get_logged_in_username()
    fines = read_fines()

    if fine_id not in fines:
        flash('Fine not found.', 'error')
        return redirect(url_for('user_profile'))

    fine = fines[fine_id]
    if fine['username'] != username:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('user_profile'))

    fine['status'] = 'Paid'
    write_fines(fines)

    flash('Payment confirmed. Thank you.', 'success')
    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True)
