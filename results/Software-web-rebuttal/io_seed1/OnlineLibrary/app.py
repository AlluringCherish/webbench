'''
Backend implementation for OnlineLibrary web application.
Provides routing, data management, and business logic for all pages.
Data is stored in local text files under the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
DATA_DIR = 'data'
# Example data initialization for missing or empty files
EXAMPLE_USERS = [
    "john_reader|john@example.com|555-1234|123 Main St",
    "jane_doe|jane@example.com|555-5678|789 Oak St"
]
EXAMPLE_BOOKS = [
    "1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8",
    "2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6",
    "3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7",
    "4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5",
    "5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3"
]
EXAMPLE_BORROWINGS = [
    "1|john_reader|2|2024-11-01|2024-11-15||Active|0",
    "2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0",
    "3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00"
]
EXAMPLE_RESERVATIONS = [
    "1|jane_doe|4|2024-11-10|Active",
    "2|john_reader|2|2024-10-25|Cancelled"
]
EXAMPLE_REVIEWS = [
    "1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03",
    "2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20"
]
EXAMPLE_FINES = [
    "1|john_reader|3|5.00|Unpaid|2024-10-30"
]
def ensure_data_file(filename, example_lines):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w', encoding='utf-8') as f:
            for line in example_lines:
                f.write(line + '\n')
# Utility functions for reading and writing data files
def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        ensure_data_file('users.txt', EXAMPLE_USERS)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('users.txt', EXAMPLE_USERS)
            lines = EXAMPLE_USERS
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            username, email, phone, address = parts
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users
def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            f.write(line + '\n')
def read_books():
    books = {}
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        ensure_data_file('books.txt', EXAMPLE_BOOKS)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('books.txt', EXAMPLE_BOOKS)
            lines = EXAMPLE_BOOKS
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 10:
                continue
            book_id = parts[0]
            try:
                avg_rating = float(parts[9]) if parts[9] else 0.0
            except ValueError:
                avg_rating = 0.0
            books[book_id] = {
                'book_id': book_id,
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'genre': parts[4],
                'publisher': parts[5],
                'year': parts[6],
                'description': parts[7],
                'status': parts[8],
                'avg_rating': avg_rating
            }
    return books
def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books.values():
            line = '|'.join([
                b['book_id'], b['title'], b['author'], b['isbn'], b['genre'],
                b['publisher'], b['year'], b['description'], b['status'], f"{b['avg_rating']:.1f}"
            ])
            f.write(line + '\n')
def read_borrowings():
    borrowings = {}
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    if not os.path.exists(path):
        ensure_data_file('borrowings.txt', EXAMPLE_BORROWINGS)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('borrowings.txt', EXAMPLE_BORROWINGS)
            lines = EXAMPLE_BORROWINGS
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            borrow_id = parts[0]
            try:
                fine_amount = float(parts[7]) if parts[7] else 0.0
            except ValueError:
                fine_amount = 0.0
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': parts[1],
                'book_id': parts[2],
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5] if parts[5] else None,
                'status': parts[6],
                'fine_amount': fine_amount
            }
    return borrowings
def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            return_date = b['return_date'] if b['return_date'] else ''
            line = '|'.join([
                b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'],
                return_date, b['status'], f"{b['fine_amount']:.2f}"
            ])
            f.write(line + '\n')
def read_reservations():
    reservations = {}
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        ensure_data_file('reservations.txt', EXAMPLE_RESERVATIONS)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('reservations.txt', EXAMPLE_RESERVATIONS)
            lines = EXAMPLE_RESERVATIONS
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 5:
                continue
            reservation_id = parts[0]
            reservations[reservation_id] = {
                'reservation_id': reservation_id,
                'username': parts[1],
                'book_id': parts[2],
                'reservation_date': parts[3],
                'status': parts[4]
            }
    return reservations
def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = '|'.join([
                r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']
            ])
            f.write(line + '\n')
def read_reviews():
    reviews = {}
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        ensure_data_file('reviews.txt', EXAMPLE_REVIEWS)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('reviews.txt', EXAMPLE_REVIEWS)
            lines = EXAMPLE_REVIEWS
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            review_id = parts[0]
            try:
                rating = int(parts[3])
            except ValueError:
                rating = 0
            reviews[review_id] = {
                'review_id': review_id,
                'username': parts[1],
                'book_id': parts[2],
                'rating': rating,
                'review_text': parts[4],
                'review_date': parts[5]
            }
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                r['review_id'], r['username'], r['book_id'], str(r['rating']), r['review_text'], r['review_date']
            ])
            f.write(line + '\n')
def read_fines():
    fines = {}
    path = os.path.join(DATA_DIR, 'fines.txt')
    if not os.path.exists(path):
        ensure_data_file('fines.txt', EXAMPLE_FINES)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            ensure_data_file('fines.txt', EXAMPLE_FINES)
            lines = EXAMPLE_FINES
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            fine_id = parts[0]
            try:
                amount = float(parts[3])
            except ValueError:
                amount = 0.0
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': amount,
                'status': parts[4],
                'date_issued': parts[5]
            }
    return fines
def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            line = '|'.join([
                fine['fine_id'], fine['username'], fine['borrow_id'], f"{fine['amount']:.2f}", fine['status'], fine['date_issued']
            ])
            f.write(line + '\n')
# Helper functions
def get_next_id(data_dict):
    if not data_dict:
        return '1'
    max_id = max(int(k) for k in data_dict.keys())
    return str(max_id + 1)
def calculate_avg_rating(book_id, reviews):
    ratings = [r['rating'] for r in reviews.values() if r['book_id'] == book_id]
    if not ratings:
        return 0.0
    return round(sum(ratings) / len(ratings), 1)
def update_book_avg_rating(book_id):
    books = read_books()
    reviews = read_reviews()
    if book_id not in books:
        return
    avg = calculate_avg_rating(book_id, reviews)
    books[book_id]['avg_rating'] = avg
    write_books(books)
# For simplicity, assume a logged-in user is 'john_reader'
# In a real application, implement authentication and session management
LOGGED_IN_USER = 'john_reader'
# ROUTES
@app.route('/')
def dashboard():
    users = read_users()
    books = read_books()
    username = LOGGED_IN_USER
    user = users.get(username)
    # Featured books: show first 5 available books sorted by avg_rating desc
    featured_books = sorted(
        [b for b in books.values() if b['status'] == 'Available'],
        key=lambda x: x['avg_rating'], reverse=True
    )[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_books)
@app.route('/book_catalog', methods=['GET', 'POST'])
def book_catalog():
    books = read_books()
    search_query = ''
    filtered_books = list(books.values())
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            filtered_books = [b for b in books.values() if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('book_catalog.html', books=filtered_books, search_query=search_query)
@app.route('/book_details/<book_id>')
def book_details(book_id):
    books = read_books()
    reviews = read_reviews()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    # Get reviews for this book
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)
@app.route('/borrow_confirmation/<book_id>', methods=['GET', 'POST'])
def borrow_confirmation(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    if request.method == 'POST':
        if 'confirm-borrow-button' in request.form:
            borrowings = read_borrowings()
            borrow_id = get_next_id(borrowings)
            borrow_date = datetime.now().strftime('%Y-%m-%d')
            new_borrow = {
                'borrow_id': borrow_id,
                'username': LOGGED_IN_USER,
                'book_id': book_id,
                'borrow_date': borrow_date,
                'due_date': due_date,
                'return_date': None,
                'status': 'Active',
                'fine_amount': 0.0
            }
            borrowings[borrow_id] = new_borrow
            write_borrowings(borrowings)
            # Update book status to Borrowed
            book['status'] = 'Borrowed'
            books[book_id] = book
            write_books(books)
            flash('Book borrowed successfully.')
            return redirect(url_for('my_borrowings'))
        elif 'cancel-borrow-button' in request.form:
            return redirect(url_for('book_details', book_id=book_id))
    return render_template('borrow_confirmation.html', book=book, due_date=due_date)
@app.route('/my_borrowings', methods=['GET', 'POST'])
def my_borrowings():
    borrowings = read_borrowings()
    books = read_books()
    filter_status = request.args.get('filter-status', 'All')
    user_borrows = [b for b in borrowings.values() if b['username'] == LOGGED_IN_USER]
    if filter_status != 'All':
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]
    # Sort by borrow_date descending
    user_borrows.sort(key=lambda x: x['borrow_date'], reverse=True)
    # Handle return book action
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('return-book-button-'):
                borrow_id = key[len('return-book-button-'):]
                if borrow_id in borrowings:
                    borrow = borrowings[borrow_id]
                    if borrow['status'] == 'Active':
                        borrow['status'] = 'Returned'
                        borrow['return_date'] = datetime.now().strftime('%Y-%m-%d')
                        borrowings[borrow_id] = borrow
                        write_borrowings(borrowings)
                        # Update book status to Available
                        book_id = borrow['book_id']
                        if book_id in books:
                            books[book_id]['status'] = 'Available'
                            write_books(books)
                        flash('Book returned successfully.')
                    else:
                        flash('Cannot return this book.')
                return redirect(url_for('my_borrowings'))
    return render_template('my_borrowings.html', borrowings=user_borrows, books=books, filter_status=filter_status)
@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    user_reservations = [r for r in reservations.values() if r['username'] == LOGGED_IN_USER]
    user_reservations.sort(key=lambda x: x['reservation_date'], reverse=True)
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('cancel-reservation-button-'):
                reservation_id = key[len('cancel-reservation-button-'):]
                if reservation_id in reservations:
                    reservation = reservations[reservation_id]
                    if reservation['status'] == 'Active':
                        reservation['status'] = 'Cancelled'
                        reservations[reservation_id] = reservation
                        write_reservations(reservations)
                        # Update book status if needed
                        book_id = reservation['book_id']
                        # Check if book is Reserved by others
                        other_active = any(r['book_id'] == book_id and r['status'] == 'Active' and r['reservation_id'] != reservation_id for r in reservations.values())
                        if not other_active:
                            if book_id in books:
                                books[book_id]['status'] = 'Available'
                                write_books(books)
                        flash('Reservation cancelled.')
                    else:
                        flash('Cannot cancel this reservation.')
                return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations, books=books)
@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    user_reviews = [r for r in reviews.values() if r['username'] == LOGGED_IN_USER]
    user_reviews.sort(key=lambda x: x['review_date'], reverse=True)
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('delete-review-button-'):
                review_id = key[len('delete-review-button-'):]
                if review_id in reviews:
                    review = reviews[review_id]
                    if review['username'] == LOGGED_IN_USER:
                        del reviews[review_id]
                        write_reviews(reviews)
                        # Update avg rating for the book
                        update_book_avg_rating(review['book_id'])
                        flash('Review deleted.')
                    else:
                        flash('Cannot delete this review.')
                return redirect(url_for('my_reviews'))
            elif key.startswith('edit-review-button-'):
                review_id = key[len('edit-review-button-'):]
                if review_id in reviews:
                    return redirect(url_for('write_review', book_id=reviews[review_id]['book_id'], review_id=review_id))
    return render_template('my_reviews.html', reviews=user_reviews, books=books)
@app.route('/write_review/<book_id>', methods=['GET', 'POST'])
@app.route('/write_review/<book_id>/<review_id>', methods=['GET', 'POST'])
def write_review(book_id, review_id=None):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    reviews = read_reviews()
    if review_id:
        review = reviews.get(review_id)
        if not review or review['username'] != LOGGED_IN_USER:
            flash('Review not found or access denied.')
            return redirect(url_for('my_reviews'))
    else:
        review = None
    if request.method == 'POST':
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash('Please select a valid rating between 1 and 5.')
            return render_template('write_review.html', book=book, review=review, rating=rating, review_text=review_text)
        rating = int(rating)
        review_date = datetime.now().strftime('%Y-%m-%d')
        if review:
            # Update existing review
            review['rating'] = rating
            review['review_text'] = review_text
            review['review_date'] = review_date
            reviews[review_id] = review
            flash('Review updated.')
        else:
            # Create new review
            new_review_id = get_next_id(reviews)
            new_review = {
                'review_id': new_review_id,
                'username': LOGGED_IN_USER,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews[new_review_id] = new_review
            flash('Review submitted.')
        write_reviews(reviews)
        update_book_avg_rating(book_id)
        return redirect(url_for('book_details', book_id=book_id))
    # GET request
    rating_val = review['rating'] if review else None
    review_text_val = review['review_text'] if review else ''
    return render_template('write_review.html', book=book, review=review, rating=rating_val, review_text=review_text_val)
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    users = read_users()
    borrowings = read_borrowings()
    username = LOGGED_IN_USER
    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.')
            return redirect(url_for('user_profile'))
        user['email'] = email
        users[username] = user
        write_users(users)
        flash('Profile updated.')
        return redirect(url_for('user_profile'))
    # Borrow history: all borrowings for user, sorted by borrow_date desc
    history = [b for b in borrowings.values() if b['username'] == username]
    history.sort(key=lambda x: x['borrow_date'], reverse=True)
    books = read_books()
    return render_template('user_profile.html', user=user, borrow_history=history, books=books)
@app.route('/payment_confirmation/<borrow_id>', methods=['GET', 'POST'])
def payment_confirmation(borrow_id):
    fines = read_fines()
    borrowings = read_borrowings()
    fine = None
    for f in fines.values():
        if f['borrow_id'] == borrow_id and f['username'] == LOGGED_IN_USER and f['status'] == 'Unpaid':
            fine = f
            break
    if not fine:
        flash('No unpaid fine found for this borrowing.')
        return redirect(url_for('user_profile'))
    if request.method == 'POST':
        if 'confirm-payment-button' in request.form:
            # Mark fine as paid
            fine['status'] = 'Paid'
            fines[fine['fine_id']] = fine
            write_fines(fines)
            # Also update borrowings fine_amount to 0
            if borrow_id in borrowings:
                borrowings[borrow_id]['fine_amount'] = 0.0
                write_borrowings(borrowings)
            flash('Payment confirmed. Thank you!')
            return redirect(url_for('user_profile'))
        elif 'back-to-profile' in request.form:
            return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', fine_amount=fine['amount'])
# Run the app
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    # Ensure all data files exist with example data if missing or empty
    ensure_data_file('users.txt', EXAMPLE_USERS)
    ensure_data_file('books.txt', EXAMPLE_BOOKS)
    ensure_data_file('borrowings.txt', EXAMPLE_BORROWINGS)
    ensure_data_file('reservations.txt', EXAMPLE_RESERVATIONS)
    ensure_data_file('reviews.txt', EXAMPLE_REVIEWS)
    ensure_data_file('fines.txt', EXAMPLE_FINES)
    app.run(port=5000, debug=True)