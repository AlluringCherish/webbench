'''
Main backend Python application for OnlineLibrary web application.
Implements the web server, routing, and all business logic.
Handles reading/writing local text files in 'data' directory.
Manages user sessions, page rendering, and data processing for all functionalities.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')
# Utility functions for reading and writing pipe-delimited files
def read_pipe_file(filepath):
    """Read a pipe-delimited file and return list of dicts with keys from header or known schema."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_pipe_file(filepath, lines):
    """Write list of pipe-delimited strings to file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
# Parsing functions for each data type
def parse_users():
    lines = read_pipe_file(USERS_FILE)
    users = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
    return users
def save_users(users):
    lines = []
    for u in users:
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    write_pipe_file(USERS_FILE, lines)
def parse_books():
    lines = read_pipe_file(BOOKS_FILE)
    books = []
    for line in lines:
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
def save_books(books):
    lines = []
    for b in books:
        line = '|'.join([
            b['book_id'], b['title'], b['author'], b['isbn'], b['genre'],
            b['publisher'], b['year'], b['description'], b['status'], f"{b['avg_rating']:.1f}"
        ])
        lines.append(line)
    write_pipe_file(BOOKS_FILE, lines)
def parse_borrowings():
    lines = read_pipe_file(BORROWINGS_FILE)
    borrowings = []
    for line in lines:
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
def save_borrowings(borrowings):
    lines = []
    for b in borrowings:
        line = '|'.join([
            b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'],
            b['return_date'], b['status'], f"{b['fine_amount']:.2f}"
        ])
        lines.append(line)
    write_pipe_file(BORROWINGS_FILE, lines)
def parse_reservations():
    lines = read_pipe_file(RESERVATIONS_FILE)
    reservations = []
    for line in lines:
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
def save_reservations(reservations):
    lines = []
    for r in reservations:
        line = '|'.join([r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']])
        lines.append(line)
    write_pipe_file(RESERVATIONS_FILE, lines)
def parse_reviews():
    lines = read_pipe_file(REVIEWS_FILE)
    reviews = []
    for line in lines:
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
def save_reviews(reviews):
    lines = []
    for r in reviews:
        # Escape review_text pipe characters if any (replace with space)
        safe_text = r['review_text'].replace('|', ' ')
        line = '|'.join([r['review_id'], r['username'], r['book_id'], str(r['rating']), safe_text, r['review_date']])
        lines.append(line)
    write_pipe_file(REVIEWS_FILE, lines)
def parse_fines():
    lines = read_pipe_file(FINES_FILE)
    fines = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            fines.append({
                'fine_id': parts[0],
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': float(parts[3]) if parts[3] else 0.0,
                'status': parts[4],
                'date_issued': parts[5]
            })
    return fines
def save_fines(fines):
    lines = []
    for f in fines:
        line = '|'.join([f['fine_id'], f['username'], f['borrow_id'], f"{f['amount']:.2f}", f['status'], f['date_issued']])
        lines.append(line)
    write_pipe_file(FINES_FILE, lines)
# Helper functions
def get_next_id(items, id_field):
    """Get next integer ID as string for a list of dicts with id_field."""
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def get_current_username():
    """Get current logged-in username from session."""
    return session.get('username')
def login_required(func):
    """Decorator to require login for routes."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_current_username():
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper
# For simplicity, implement a very basic login/logout system for demo purposes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = parse_users()
        user = next((u for u in users if u['username'] == username), None)
        if user:
            session['username'] = username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username.", "danger")
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))
# Route: Dashboard Page (route '/')
@app.route('/')
@login_required
def dashboard():
    username = get_current_username()
    # Featured books: show first 5 available books sorted by avg_rating desc
    books = parse_books()
    featured_books = sorted([b for b in books if b['status'] == 'Available'], key=lambda x: x['avg_rating'], reverse=True)[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_books)
# Route: Book Catalog Page
@app.route('/catalog', methods=['GET', 'POST'])
@login_required
def book_catalog():
    username = get_current_username()
    books = parse_books()
    search_query = ''
    filtered_books = books
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            filtered_books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('book_catalog.html', username=username, books=filtered_books, search_query=search_query)
# Route: Book Details Page
@app.route('/book/<book_id>')
@login_required
def book_details(book_id):
    username = get_current_username()
    books = parse_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for('book_catalog'))
    # Get reviews for this book
    reviews = parse_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    # Sort reviews by review_date descending
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    # Check if user already borrowed or reserved this book
    borrowings = parse_borrowings()
    user_borrowed = any(b['username'] == username and b['book_id'] == book_id and b['status'] == 'Active' for b in borrowings)
    reservations = parse_reservations()
    user_reserved = any(r['username'] == username and r['book_id'] == book_id and r['status'] == 'Active' for r in reservations)
    return render_template('book_details.html', username=username, book=book, reviews=book_reviews,
                           user_borrowed=user_borrowed, user_reserved=user_reserved)
# Route: Borrow Confirmation Page
@app.route('/borrow/<book_id>', methods=['GET', 'POST'])
@login_required
def borrow_confirmation(book_id):
    username = get_current_username()
    books = parse_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash("Book is not available for borrowing.", "warning")
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
            save_borrowings(borrowings)
            # Update book status to Borrowed
            for b in books:
                if b['book_id'] == book_id:
                    b['status'] = 'Borrowed'
                    break
            save_books(books)
            flash(f"You have successfully borrowed '{book['title']}'. Due date: {due_date.isoformat()}", "success")
            return redirect(url_for('my_borrowings'))
        elif 'cancel-borrow-button' in request.form:
            return redirect(url_for('book_details', book_id=book_id))
    return render_template('borrow_confirmation.html', username=username, book=book,
                           borrow_date=borrow_date.isoformat(), due_date=due_date.isoformat())
# Route: My Borrowings Page
@app.route('/my_borrowings', methods=['GET', 'POST'])
@login_required
def my_borrowings():
    username = get_current_username()
    borrowings = parse_borrowings()
    books = parse_books()
    filter_status = request.args.get('filter-status', 'All')
    user_borrowings = [b for b in borrowings if b['username'] == username]
    if filter_status != 'All':
        user_borrowings = [b for b in user_borrowings if b['status'] == filter_status]
    # Enrich borrowings with book title
    for b in user_borrowings:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        b['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        # Handle return book button
        for key in request.form:
            if key.startswith('return-book-button-'):
                borrow_id = key.replace('return-book-button-', '')
                # Process return
                borrowings = parse_borrowings()
                books = parse_books()
                borrow = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == username), None)
                if borrow and borrow['status'] == 'Active':
                    borrow['return_date'] = datetime.now().date().isoformat()
                    borrow['status'] = 'Returned'
                    borrow['fine_amount'] = 0.0  # Assume fine handled separately
                    # Update book status to Available if no active borrowings or reservations
                    book = next((bk for bk in books if bk['book_id'] == borrow['book_id']), None)
                    if book:
                        # Check if any other active borrowings for this book
                        other_active = any(bw['book_id'] == book['book_id'] and bw['status'] == 'Active' for bw in borrowings if bw['borrow_id'] != borrow_id)
                        # Check if any active reservations
                        reservations = parse_reservations()
                        active_reservations = any(r['book_id'] == book['book_id'] and r['status'] == 'Active' for r in reservations)
                        if not other_active and not active_reservations:
                            book['status'] = 'Available'
                        elif active_reservations:
                            book['status'] = 'Reserved'
                        save_books(books)
                    save_borrowings(borrowings)
                    flash(f"Book '{book['title']}' returned successfully.", "success")
                else:
                    flash("Invalid return request.", "danger")
                return redirect(url_for('my_borrowings'))
    return render_template('my_borrowings.html', username=username, borrowings=user_borrowings, filter_status=filter_status)
# Route: My Reservations Page
@app.route('/my_reservations', methods=['GET', 'POST'])
@login_required
def my_reservations():
    username = get_current_username()
    reservations = parse_reservations()
    books = parse_books()
    user_reservations = [r for r in reservations if r['username'] == username]
    # Enrich reservations with book title
    for r in user_reservations:
        book = next((bk for bk in books if bk['book_id'] == r['book_id']), None)
        r['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('cancel-reservation-button-'):
                reservation_id = key.replace('cancel-reservation-button-', '')
                reservations = parse_reservations()
                reservation = next((r for r in reservations if r['reservation_id'] == reservation_id and r['username'] == username), None)
                if reservation and reservation['status'] == 'Active':
                    reservation['status'] = 'Cancelled'
                    save_reservations(reservations)
                    # Update book status if needed
                    books = parse_books()
                    book = next((bk for bk in books if bk['book_id'] == reservation['book_id']), None)
                    if book:
                        # Check if any other active reservations for this book
                        active_reservations = any(r['book_id'] == book['book_id'] and r['status'] == 'Active' for r in reservations)
                        # Check if any active borrowings
                        borrowings = parse_borrowings()
                        active_borrowings = any(bw['book_id'] == book['book_id'] and bw['status'] == 'Active' for bw in borrowings)
                        if not active_reservations and not active_borrowings:
                            book['status'] = 'Available'
                        elif active_borrowings:
                            book['status'] = 'Borrowed'
                        save_books(books)
                    flash(f"Reservation for '{book['title']}' cancelled.", "success")
                else:
                    flash("Invalid cancellation request.", "danger")
                return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', username=username, reservations=user_reservations)
# Route: My Reviews Page
@app.route('/my_reviews', methods=['GET', 'POST'])
@login_required
def my_reviews():
    username = get_current_username()
    reviews = parse_reviews()
    books = parse_books()
    user_reviews = [r for r in reviews if r['username'] == username]
    # Enrich reviews with book title
    for r in user_reviews:
        book = next((bk for bk in books if bk['book_id'] == r['book_id']), None)
        r['title'] = book['title'] if book else 'Unknown'
    if request.method == 'POST':
        # Edit or delete review buttons
        for key in request.form:
            if key.startswith('edit-review-button-'):
                review_id = key.replace('edit-review-button-', '')
                return redirect(url_for('write_review', book_id=None, review_id=review_id))
            elif key.startswith('delete-review-button-'):
                review_id = key.replace('delete-review-button-', '')
                reviews = parse_reviews()
                review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
                if review:
                    reviews.remove(review)
                    save_reviews(reviews)
                    flash("Review deleted successfully.", "success")
                else:
                    flash("Invalid delete request.", "danger")
                return redirect(url_for('my_reviews'))
    return render_template('my_reviews.html', username=username, reviews=user_reviews)
# Route: Write Review Page
@app.route('/write_review', methods=['GET', 'POST'])
@login_required
def write_review():
    username = get_current_username()
    book_id = request.args.get('book_id')
    review_id = request.args.get('review_id')
    books = parse_books()
    book = None
    if book_id:
        book = next((b for b in books if b['book_id'] == book_id), None)
    elif review_id:
        reviews = parse_reviews()
        review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
        if review:
            book = next((b for b in books if b['book_id'] == review['book_id']), None)
            book_id = review['book_id']
        else:
            flash("Review not found.", "danger")
            return redirect(url_for('my_reviews'))
    else:
        flash("No book specified for review.", "danger")
        return redirect(url_for('dashboard'))
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for('dashboard'))
    rating = 1
    review_text = ''
    if review_id:
        reviews = parse_reviews()
        review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
        if review:
            rating = review['rating']
            review_text = review['review_text']
    if request.method == 'POST':
        rating = int(request.form.get('rating-input', 1))
        review_text = request.form.get('review-text', '').strip()
        if not review_text:
            flash("Review text cannot be empty.", "warning")
            return render_template('write_review.html', username=username, book=book, rating=rating, review_text=review_text)
        reviews = parse_reviews()
        today_str = datetime.now().date().isoformat()
        if review_id:
            # Update existing review
            review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
            if review:
                review['rating'] = rating
                review['review_text'] = review_text
                review['review_date'] = today_str
            else:
                flash("Review not found for update.", "danger")
                return redirect(url_for('my_reviews'))
        else:
            # Add new review
            new_review_id = get_next_id(reviews, 'review_id')
            reviews.append({
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': today_str
            })
        save_reviews(reviews)
        # Update book average rating
        book_reviews = [r for r in reviews if r['book_id'] == book_id]
        if book_reviews:
            avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            for b in books:
                if b['book_id'] == book_id:
                    b['avg_rating'] = round(avg_rating, 1)
                    break
            save_books(books)
        flash("Review submitted successfully.", "success")
        return redirect(url_for('book_details', book_id=book_id))
    return render_template('write_review.html', username=username, book=book, rating=rating, review_text=review_text)
# Route: User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    username = get_current_username()
    users = parse_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email:
            user['email'] = new_email
            save_users(users)
            flash("Profile updated successfully.", "success")
        else:
            flash("Email cannot be empty.", "warning")
    # Borrow history: all borrowings for user (returned or active)
    borrowings = parse_borrowings()
    books = parse_books()
    user_borrow_history = [b for b in borrowings if b['username'] == username]
    for b in user_borrow_history:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        b['title'] = book['title'] if book else 'Unknown'
    return render_template('user_profile.html', username=username, user=user, borrow_history=user_borrow_history)
# Route: Payment Confirmation Page
@app.route('/payment/<fine_id>', methods=['GET', 'POST'])
@login_required
def payment_confirmation(fine_id):
    username = get_current_username()
    fines = parse_fines()
    fine = next((f for f in fines if f['fine_id'] == fine_id and f['username'] == username), None)
    if not fine:
        flash("Fine not found.", "danger")
        return redirect(url_for('user_profile'))
    if fine['status'] == 'Paid':
        flash("This fine has already been paid.", "info")
        return redirect(url_for('user_profile'))
    if request.method == 'POST':
        if 'confirm-payment-button' in request.form:
            fine['status'] = 'Paid'
            save_fines(fines)
            # Also update borrowings fine_amount to 0 for this borrow_id
            borrowings = parse_borrowings()
            for b in borrowings:
                if b['borrow_id'] == fine['borrow_id']:
                    b['fine_amount'] = 0.0
                    break
            save_borrowings(borrowings)
            flash("Payment successful. Thank you!", "success")
            return redirect(url_for('user_profile'))
        elif 'back-to-profile' in request.form:
            return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', username=username, fine=fine)
# Additional routes for navigation buttons
@app.route('/dashboard')
@login_required
def dashboard_redirect():
    return redirect(url_for('dashboard'))
@app.route('/back_to_dashboard')
@login_required
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_catalog')
@login_required
def back_to_catalog():
    return redirect(url_for('book_catalog'))
@app.route('/back_to_book/<book_id>')
@login_required
def back_to_book(book_id):
    return redirect(url_for('book_details', book_id=book_id))
@app.route('/back_to_profile')
@login_required
def back_to_profile():
    return redirect(url_for('user_profile'))
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)