from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data files constants
USERS_FILE = 'data/users.txt'
BOOKS_FILE = 'data/books.txt'
BORROWINGS_FILE = 'data/borrowings.txt'
RESERVATIONS_FILE = 'data/reservations.txt'
REVIEWS_FILE = 'data/reviews.txt'
FINES_FILE = 'data/fines.txt'

DATE_FORMAT = '%Y-%m-%d'

# Utility functions to read and write pipe-delimited data

def read_file(filepath, fields):
    """Reads a pipe-delimited file and returns a list of dicts with keys from fields"""
    if not os.path.exists(filepath):
        return []
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(fields):
                continue  # skip malformed lines
            entry = dict(zip(fields, parts))
            data.append(entry)
    return data


def write_file(filepath, fields, data):
    """Writes a list of dicts to a pipe-delimited file with keys in fields order"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in data:
            line = '|'.join(entry.get(field, '') for field in fields)
            f.write(line + '\n')

# User schema fields
USER_FIELDS = ['username', 'password', 'full_name', 'email', 'phone']

# Book schema fields
BOOK_FIELDS = ['isbn', 'title', 'author', 'year', 'copies_available']

# Borrowing schema fields
BORROWING_FIELDS = ['borrow_id', 'username', 'isbn', 'borrow_date', 'due_date', 'return_date', 'status']

# Reservation schema fields
RESERVATION_FIELDS = ['reservation_id', 'username', 'isbn', 'reservation_date', 'status']

# Review schema fields
REVIEW_FIELDS = ['review_id', 'username', 'isbn', 'rating', 'comment', 'review_date']

# Fine schema fields
FINE_FIELDS = ['fine_id', 'username', 'amount', 'paid']


# Authentication and session management helpers
# This example does not employ actual session management for simplicity,
# keep a global 'logged_in_user' mimic (not thread safe or scalable - only for demonstration)
logged_in_user = {'username': None}


def get_logged_in_username():
    return logged_in_user.get('username')


def set_logged_in_username(username):
    logged_in_user['username'] = username


@app.route('/')
def root():
    # Redirect to dashboard page
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username()
    if not username:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))
    # Load user info
    users = read_file(USERS_FILE, USER_FIELDS)
    user = next((u for u in users if u['username'] == username), None)
    
    # Load borrowings for user
    borrowings = read_file(BORROWINGS_FILE, BORROWING_FIELDS)
    user_borrowings = [b for b in borrowings if b['username'] == username]

    # Load reservations
    reservations = read_file(RESERVATIONS_FILE, RESERVATION_FIELDS)
    user_reservations = [r for r in reservations if r['username'] == username]

    # Load fines
    fines = read_file(FINES_FILE, FINE_FIELDS)
    user_fines = [f for f in fines if f['username'] == username and f['paid'] == 'False']

    return render_template('dashboard.html', user=user, borrowings=user_borrowings, reservations=user_reservations, fines=user_fines)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = read_file(USERS_FILE, USER_FIELDS)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            set_logged_in_username(username)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    set_logged_in_username(None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/books')
def books():
    username = get_logged_in_username()
    if not username:
        flash('Please log in to view books.')
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip().lower()
    author_filter = request.args.get('author', '').strip().lower()
    year_filter = request.args.get('year', '').strip()

    books = read_file(BOOKS_FILE, BOOK_FIELDS)
    filtered_books = []

    for book in books:
        if search and search not in book['title'].lower() and search not in book['author'].lower():
            continue
        if author_filter and author_filter != book['author'].lower():
            continue
        if year_filter and year_filter != book['year']:
            continue
        filtered_books.append(book)

    return render_template('books.html', books=filtered_books, search=search, author=author_filter, year=year_filter)


@app.route('/borrow/<isbn>', methods=['POST'])
def borrow_book(isbn):
    username = get_logged_in_username()
    if not username:
        flash('You need to log in to borrow books.')
        return redirect(url_for('login'))

    # Load books
    books = read_file(BOOKS_FILE, BOOK_FIELDS)
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('books'))

    if int(book['copies_available']) <= 0:
        flash('No copies available to borrow.')
        return redirect(url_for('books'))

    # Load borrowings and check user borrowing rules
    borrowings = read_file(BORROWINGS_FILE, BORROWING_FIELDS)
    user_borrowings = [b for b in borrowings if b['username'] == username and b['status'] == 'Active']

    if len(user_borrowings) >= 5:
        flash('You have reached the maximum number of active borrowings.')
        return redirect(url_for('books'))

    # Reduce copy count
    book['copies_available'] = str(int(book['copies_available']) - 1)

    # Create new borrowing entry
    borrow_id = str(len(borrowings) + 1)
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)

    new_borrowing = {
        'borrow_id': borrow_id,
        'username': username,
        'isbn': isbn,
        'borrow_date': borrow_date.strftime(DATE_FORMAT),
        'due_date': due_date.strftime(DATE_FORMAT),
        'return_date': '',
        'status': 'Active'
    }

    borrowings.append(new_borrowing)

    # Write updates
    write_file(BOOKS_FILE, BOOK_FIELDS, books)
    write_file(BORROWINGS_FILE, BORROWING_FIELDS, borrowings)

    flash('Book borrowed successfully.')
    return redirect(url_for('books'))


@app.route('/return/<borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_logged_in_username()
    if not username:
        flash('You need to log in to return books.')
        return redirect(url_for('login'))

    borrowings = read_file(BORROWINGS_FILE, BORROWING_FIELDS)
    borrowing = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == username), None)
    if not borrowing:
        flash('Borrowing record not found.')
        return redirect(url_for('dashboard'))

    if borrowing['status'] != 'Active' and borrowing['status'] != 'Overdue':
        flash('Book is already returned or borrowing cancelled.')
        return redirect(url_for('dashboard'))

    # Update borrowing
    borrowing['return_date'] = datetime.now().strftime(DATE_FORMAT)
    borrowing['status'] = 'Returned'

    # Increase book copies
    books = read_file(BOOKS_FILE, BOOK_FIELDS)
    book = next((b for b in books if b['isbn'] == borrowing['isbn']), None)
    if book:
        book['copies_available'] = str(int(book['copies_available']) + 1)

    # Handle potential overdue fines
    due_date = datetime.strptime(borrowing['due_date'], DATE_FORMAT)
    return_date = datetime.strptime(borrowing['return_date'], DATE_FORMAT)
    if return_date > due_date:
        # Calculate fine
        days_late = (return_date - due_date).days
        amount = days_late * 1.0  # 1 unit fine per day late
        fines = read_file(FINES_FILE, FINE_FIELDS)
        fine_id = str(len(fines) + 1)
        new_fine = {
            'fine_id': fine_id,
            'username': username,
            'amount': str(amount),
            'paid': 'False'
        }
        fines.append(new_fine)
        write_file(FINES_FILE, FINE_FIELDS, fines)
        flash(f'Book returned late. Fine of {amount} units added.')
    else:
        flash('Book returned successfully.')

    write_file(BOOKS_FILE, BOOK_FIELDS, books)
    write_file(BORROWINGS_FILE, BORROWING_FIELDS, borrowings)

    return redirect(url_for('dashboard'))


@app.route('/reserve/<isbn>', methods=['POST'])
def reserve_book(isbn):
    username = get_logged_in_username()
    if not username:
        flash('You need to log in to reserve books.')
        return redirect(url_for('login'))

    # Load books
    books = read_file(BOOKS_FILE, BOOK_FIELDS)
    book = next((b for b in books if b['isbn'] == isbn), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('books'))

    # Load existing reservations
    reservations = read_file(RESERVATIONS_FILE, RESERVATION_FIELDS)

    # Check for duplicate active reservation
    for r in reservations:
        if r['username'] == username and r['isbn'] == isbn and r['status'] == 'Active':
            flash('You already have an active reservation for this book.')
            return redirect(url_for('books'))

    # Create reservation
    reservation_id = str(len(reservations) + 1)
    reservation_date = datetime.now().strftime(DATE_FORMAT)

    new_reservation = {
        'reservation_id': reservation_id,
        'username': username,
        'isbn': isbn,
        'reservation_date': reservation_date,
        'status': 'Active'
    }

    reservations.append(new_reservation)
    write_file(RESERVATIONS_FILE, RESERVATION_FIELDS, reservations)

    flash('Book reserved successfully.')
    return redirect(url_for('books'))


@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_logged_in_username()
    if not username:
        flash('You need to log in to cancel reservations.')
        return redirect(url_for('login'))

    reservations = read_file(RESERVATIONS_FILE, RESERVATION_FIELDS)
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id and r['username'] == username), None)
    if not reservation:
        flash('Reservation record not found.')
        return redirect(url_for('dashboard'))

    if reservation['status'] != 'Active':
        flash('Reservation already cancelled or completed.')
        return redirect(url_for('dashboard'))

    reservation['status'] = 'Cancelled'

    write_file(RESERVATIONS_FILE, RESERVATION_FIELDS, reservations)

    flash('Reservation cancelled successfully.')
    return redirect(url_for('dashboard'))


@app.route('/reviews/<isbn>', methods=['GET', 'POST'])
def book_reviews(isbn):
    username = get_logged_in_username()
    if not username:
        flash('Please log in to view or add reviews.')
        return redirect(url_for('login'))

    reviews = read_file(REVIEWS_FILE, REVIEW_FIELDS)
    book_reviews = [r for r in reviews if r['isbn'] == isbn]

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        # Validate rating
        try:
            rating_val = int(rating)
            if rating_val < 1 or rating_val > 5:
                raise ValueError()
        except:
            flash('Rating must be an integer between 1 and 5.')
            return render_template('reviews.html', isbn=isbn, reviews=book_reviews)

        # Check if user has already reviewed this book
        existing_review = next((r for r in reviews if r['isbn'] == isbn and r['username'] == username), None)
        review_date = datetime.now().strftime(DATE_FORMAT)

        if existing_review:
            # Update existing review
            existing_review['rating'] = str(rating_val)
            existing_review['comment'] = comment
            existing_review['review_date'] = review_date
            flash('Review updated successfully.')
        else:
            # Add new review
            review_id = str(len(reviews) + 1)
            new_review = {
                'review_id': review_id,
                'username': username,
                'isbn': isbn,
                'rating': str(rating_val),
                'comment': comment,
                'review_date': review_date
            }
            reviews.append(new_review)
            flash('Review added successfully.')

        write_file(REVIEWS_FILE, REVIEW_FIELDS, reviews)

        return redirect(url_for('book_reviews', isbn=isbn))

    return render_template('reviews.html', isbn=isbn, reviews=book_reviews)


@app.route('/profile')
def profile():
    username = get_logged_in_username()
    if not username:
        flash('Please log in to view profile.')
        return redirect(url_for('login'))

    users = read_file(USERS_FILE, USER_FIELDS)
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        flash('User not found.')
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    username = get_logged_in_username()
    if not username:
        flash('Please log in to edit profile.')
        return redirect(url_for('login'))

    users = read_file(USERS_FILE, USER_FIELDS)
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        flash('User not found.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        user['full_name'] = full_name
        user['email'] = email
        user['phone'] = phone

        write_file(USERS_FILE, USER_FIELDS, users)
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
