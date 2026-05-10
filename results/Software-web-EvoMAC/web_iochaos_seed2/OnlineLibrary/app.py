'''
Main backend application for OnlineLibrary web application.
Handles routing, business logic, file I/O for local text files in data directory,
and rendering HTML templates for all pages as per requirements.
Includes user login/logout and session management for multi-user support.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from functools import wraps
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages and session management
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip()]
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
# Parsing functions for each data type
def parse_users():
    users = []
    for line in read_file_lines('users.txt'):
        parts = line.split('|')
        if len(parts) == 4:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
    return users
def parse_books():
    books = []
    for line in read_file_lines('books.txt'):
        parts = line.split('|')
        if len(parts) == 10:
            books.append({
                'book_id': parts[0],
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'genre': parts[4],
                'publisher': parts[5],
                'year': parts[6],
                'description': parts[7],
                'status': parts[8],
                'avg_rating': float(parts[9]) if parts[9] else 0.0
            })
    return books
def parse_borrowings():
    borrowings = []
    for line in read_file_lines('borrowings.txt'):
        parts = line.split('|')
        if len(parts) == 8:
            borrowings.append({
                'borrow_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5],
                'status': parts[6],
                'fine_amount': float(parts[7]) if parts[7] else 0.0
            })
    return borrowings
def parse_reservations():
    reservations = []
    for line in read_file_lines('reservations.txt'):
        parts = line.split('|')
        if len(parts) == 5:
            reservations.append({
                'reservation_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'reservation_date': parts[3],
                'status': parts[4]
            })
    return reservations
def parse_reviews():
    reviews = []
    for line in read_file_lines('reviews.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            reviews.append({
                'review_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            })
    return reviews
def parse_fines():
    fines = []
    for line in read_file_lines('fines.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            fines.append({
                'fine_id': parts[0],
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': float(parts[3]),
                'status': parts[4],
                'date_issued': parts[5]
            })
    return fines
# Writing functions for each data type
def write_users(users):
    lines = []
    for u in users:
        lines.append(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}")
    write_file_lines('users.txt', lines)
def write_books(books):
    lines = []
    for b in books:
        lines.append(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}")
    write_file_lines('books.txt', lines)
def write_borrowings(borrowings):
    lines = []
    for b in borrowings:
        lines.append(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date']}|{b['status']}|{b['fine_amount']}")
    write_file_lines('borrowings.txt', lines)
def write_reservations(reservations):
    lines = []
    for r in reservations:
        lines.append(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}")
    write_file_lines('reservations.txt', lines)
def write_reviews(reviews):
    lines = []
    for r in reviews:
        lines.append(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}")
    write_file_lines('reviews.txt', lines)
def write_fines(fines):
    lines = []
    for f in fines:
        lines.append(f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']}|{f['status']}|{f['date_issued']}")
    write_file_lines('fines.txt', lines)
# Helper functions
def get_user(username):
    users = parse_users()
    for u in users:
        if u['username'] == username:
            return u
    return None
def get_book(book_id):
    books = parse_books()
    for b in books:
        if b['book_id'] == book_id:
            return b
    return None
def get_borrowing(borrow_id):
    borrowings = parse_borrowings()
    for b in borrowings:
        if b['borrow_id'] == borrow_id:
            return b
    return None
def get_reservation(reservation_id):
    reservations = parse_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None
def get_review(review_id):
    reviews = parse_reviews()
    for r in reviews:
        if r['review_id'] == review_id:
            return r
    return None
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def update_book_status(book_id, new_status):
    books = parse_books()
    for b in books:
        if b['book_id'] == book_id:
            b['status'] = new_status
            break
    write_books(books)
def calculate_avg_rating(book_id):
    reviews = parse_reviews()
    ratings = [r['rating'] for r in reviews if r['book_id'] == book_id]
    if ratings:
        avg = round(sum(ratings) / len(ratings), 1)
    else:
        avg = 0.0
    books = parse_books()
    for b in books:
        if b['book_id'] == book_id:
            b['avg_rating'] = avg
            break
    write_books(books)
    return avg
# Decorator to require login for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
# ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash("Please enter a username.")
            return render_template('login.html')
        user = get_user(username)
        if user:
            session['username'] = username
            flash(f"Logged in as {username}.")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash("Username not found.")
            return render_template('login.html')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))
@app.route('/')
@login_required
def dashboard():
    username = session['username']
    user = get_user(username)
    if not user:
        flash("User not found.")
        return "User not found", 404
    # Featured books: show first 5 available books sorted by avg_rating desc
    books = parse_books()
    featured_books = sorted([b for b in books if b['status'] == 'Available'], key=lambda x: x['avg_rating'], reverse=True)[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_books)
@app.route('/book_catalog', methods=['GET', 'POST'])
@login_required
def book_catalog():
    username = session['username']
    books = parse_books()
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('book_catalog.html', books=books, search_query=search_query)
@app.route('/book_details/<book_id>')
@login_required
def book_details(book_id):
    username = session['username']
    book = get_book(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for('book_catalog'))
    reviews = [r for r in parse_reviews() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=reviews, username=username)
@app.route('/borrow_confirmation/<book_id>', methods=['GET', 'POST'])
@login_required
def borrow_confirmation(book_id):
    username = session['username']
    book = get_book(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash("Book is not available for borrowing.")
        return redirect(url_for('book_details', book_id=book_id))
    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=14)
    if request.method == 'POST':
        if 'confirm-borrow-button' in request.form:
            borrowings = parse_borrowings()
            new_borrow_id = get_next_id(borrowings, 'borrow_id')
            borrowings.append({
                'borrow_id': new_borrow_id,
                'username': username,
                'book_id': book_id,
                'borrow_date': borrow_date.isoformat(),
                'due_date': due_date.isoformat(),
                'return_date': '',
                'status': 'Active',
                'fine_amount': 0.0
            })
            write_borrowings(borrowings)
            update_book_status(book_id, 'Borrowed')
            flash("Book borrowed successfully.")
            return redirect(url_for('my_borrowings'))
        elif 'cancel-borrow-button' in request.form:
            return redirect(url_for('book_details', book_id=book_id))
    return render_template('borrow_confirmation.html', book=book, borrow_date=borrow_date, due_date=due_date)
@app.route('/my_borrowings', methods=['GET', 'POST'])
@login_required
def my_borrowings():
    username = session['username']
    borrowings = parse_borrowings()
    books = parse_books()
    filter_status = request.args.get('filter-status', 'All')
    user_borrowings = [b for b in borrowings if b['username'] == username]
    if filter_status != 'All':
        user_borrowings = [b for b in user_borrowings if b['status'] == filter_status]
    # Enrich borrowings with book title
    for b in user_borrowings:
        book = get_book(b['book_id'])
        b['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        # Handle return book button
        for key in request.form:
            if key.startswith('return-book-button-'):
                borrow_id = key.replace('return-book-button-', '')
                borrowings = parse_borrowings()
                for b in borrowings:
                    if b['borrow_id'] == borrow_id and b['username'] == username and b['status'] == 'Active':
                        b['return_date'] = datetime.now().date().isoformat()
                        b['status'] = 'Returned'
                        # Update book status to Available
                        update_book_status(b['book_id'], 'Available')
                        # Remove any active reservation for this book by this user
                        reservations = parse_reservations()
                        for r in reservations:
                            if r['book_id'] == b['book_id'] and r['username'] == username and r['status'] == 'Active':
                                r['status'] = 'Cancelled'
                        write_reservations(reservations)
                        write_borrowings(borrowings)
                        flash("Book returned successfully.")
                        break
                return redirect(url_for('my_borrowings', **request.args))
    return render_template('my_borrowings.html', borrowings=user_borrowings, filter_status=filter_status)
@app.route('/my_reservations', methods=['GET', 'POST'])
@login_required
def my_reservations():
    username = session['username']
    reservations = parse_reservations()
    books = parse_books()
    user_reservations = [r for r in reservations if r['username'] == username]
    # Enrich reservations with book title
    for r in user_reservations:
        book = get_book(r['book_id'])
        r['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('cancel-reservation-button-'):
                reservation_id = key.replace('cancel-reservation-button-', '')
                reservations = parse_reservations()
                for r in reservations:
                    if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] == 'Active':
                        r['status'] = 'Cancelled'
                        flash("Reservation cancelled.")
                        break
                write_reservations(reservations)
                return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations)
@app.route('/my_reviews', methods=['GET', 'POST'])
@login_required
def my_reviews():
    username = session['username']
    reviews = parse_reviews()
    books = parse_books()
    user_reviews = [r for r in reviews if r['username'] == username]
    # Enrich reviews with book title
    for r in user_reviews:
        book = get_book(r['book_id'])
        r['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        # Handle edit or delete buttons
        for key in request.form:
            if key.startswith('delete-review-button-'):
                review_id = key.replace('delete-review-button-', '')
                reviews = parse_reviews()
                reviews = [r for r in reviews if not (r['review_id'] == review_id and r['username'] == username)]
                write_reviews(reviews)
                flash("Review deleted.")
                return redirect(url_for('my_reviews'))
            elif key.startswith('edit-review-button-'):
                review_id = key.replace('edit-review-button-', '')
                review = get_review(review_id)
                if review and review['username'] == username:
                    return redirect(url_for('write_review', book_id=review['book_id'], review_id=review_id))
                else:
                    flash("Review not found or unauthorized.")
                    return redirect(url_for('my_reviews'))
    return render_template('my_reviews.html', reviews=user_reviews)
@app.route('/write_review/<book_id>', methods=['GET', 'POST'])
@app.route('/write_review/<book_id>/<review_id>', methods=['GET', 'POST'])
@login_required
def write_review(book_id, review_id=None):
    username = session['username']
    book = get_book(book_id)
    if not book:
        flash("Book not found.")
        return redirect(url_for('book_catalog'))
    reviews = parse_reviews()
    existing_review = None
    if review_id:
        for r in reviews:
            if r['review_id'] == review_id and r['username'] == username:
                existing_review = r
                break
    if request.method == 'POST':
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash("Please select a valid rating between 1 and 5.")
            return render_template('write_review.html', book=book, review=existing_review)
        if not review_text:
            flash("Review text cannot be empty.")
            return render_template('write_review.html', book=book, review=existing_review)
        rating = int(rating)
        review_date = datetime.now().date().isoformat()
        if existing_review:
            # Edit existing review
            for r in reviews:
                if r['review_id'] == review_id and r['username'] == username:
                    r['rating'] = rating
                    r['review_text'] = review_text
                    r['review_date'] = review_date
                    break
            flash("Review updated.")
        else:
            # Add new review
            new_review_id = get_next_id(reviews, 'review_id')
            reviews.append({
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            })
            flash("Review submitted.")
        write_reviews(reviews)
        calculate_avg_rating(book_id)
        return redirect(url_for('book_details', book_id=book_id))
    return render_template('write_review.html', book=book, review=existing_review)
@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    username = session['username']
    users = parse_users()
    user = None
    for u in users:
        if u['username'] == username:
            user = u
            break
    if not user:
        flash("User not found.")
        return redirect(url_for('dashboard'))
    borrowings = parse_borrowings()
    user_borrow_history = [b for b in borrowings if b['username'] == username and b['status'] == 'Returned']
    # Enrich with book titles
    for b in user_borrow_history:
        book = get_book(b['book_id'])
        b['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if not new_email:
            flash("Email cannot be empty.")
            return render_template('user_profile.html', user=user, borrow_history=user_borrow_history)
        # Update email
        for u in users:
            if u['username'] == username:
                u['email'] = new_email
                user = u
                break
        write_users(users)
        flash("Profile updated.")
    return render_template('user_profile.html', user=user, borrow_history=user_borrow_history)
@app.route('/payment_confirmation/<borrow_id>', methods=['GET', 'POST'])
@login_required
def payment_confirmation(borrow_id):
    username = session['username']
    fines = parse_fines()
    fine = None
    for f in fines:
        if f['borrow_id'] == borrow_id and f['username'] == username and f['status'] == 'Unpaid':
            fine = f
            break
    if not fine:
        flash("No unpaid fine found for this borrowing.")
        return redirect(url_for('user_profile'))
    if request.method == 'POST':
        if 'confirm-payment-button' in request.form:
            # Mark fine as paid
            for f in fines:
                if f['fine_id'] == fine['fine_id']:
                    f['status'] = 'Paid'
                    break
            write_fines(fines)
            # Also update borrowings fine_amount to 0
            borrowings = parse_borrowings()
            for b in borrowings:
                if b['borrow_id'] == borrow_id:
                    b['fine_amount'] = 0.0
                    break
            write_borrowings(borrowings)
            flash("Fine payment confirmed.")
            return redirect(url_for('user_profile'))
        elif 'back-to-profile' in request.form:
            return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', fine_amount=fine['amount'])
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)