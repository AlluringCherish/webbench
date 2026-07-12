from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Data file paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# For demonstration, assume a fixed logged-in username
# In a real app, use session and authentication
CURRENT_USER = 'john_reader'

# Helper functions to load and save data

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
    lines = []
    for u in users.values():
        lines.append(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}")
    content = "\n".join(lines)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

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
                books[book_id] = {
                    'book_id': book_id,
                    'title': parts[1],
                    'author': parts[2],
                    'isbn': parts[3],
                    'genre': parts[4],
                    'publisher': parts[5],
                    'year': int(parts[6]),
                    'description': parts[7],
                    'status': parts[8],
                    'avg_rating': float(parts[9])
                }
    except FileNotFoundError:
        pass
    return books

def save_books(books):
    lines = []
    for b in books.values():
        lines.append(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}")
    content = "\n".join(lines)
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

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
                borrowings[borrow_id] = {
                    'borrow_id': borrow_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5] if parts[5] else None,
                    'status': parts[6],
                    'fine_amount': float(parts[7])
                }
    except FileNotFoundError:
        pass
    return borrowings

def save_borrowings(borrowings):
    lines = []
    for b in borrowings.values():
        return_date = b['return_date'] if b['return_date'] is not None else ''
        lines.append(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date}|{b['status']}|{b['fine_amount']}")
    content = "\n".join(lines)
    with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

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
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
    except FileNotFoundError:
        pass
    return reservations

def save_reservations(reservations):
    lines = []
    for r in reservations.values():
        lines.append(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}")
    content = "\n".join(lines)
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def load_reviews():
    reviews = {}
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review_id = int(parts[0])
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
    except FileNotFoundError:
        pass
    return reviews

def save_reviews(reviews):
    lines = []
    for r in reviews.values():
        lines.append(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}")
    content = "\n".join(lines)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

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
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': float(parts[3]),
                    'status': parts[4],
                    'date_issued': parts[5]
                }
    except FileNotFoundError:
        pass
    return fines

def save_fines(fines):
    lines = []
    for f in fines.values():
        lines.append(f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']}|{f['status']}|{f['date_issued']}")
    content = "\n".join(lines)
    with open(FINES_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

# Utility functions

def get_new_id(records):
    if not records:
        return 1
    return max(records.keys()) + 1

def calculate_due_date(borrow_date_str):
    borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
    due_date = borrow_date + timedelta(days=14)
    return due_date.strftime('%Y-%m-%d')

def update_book_status(book_id, new_status):
    books = load_books()
    if book_id in books:
        books[book_id]['status'] = new_status
        save_books(books)

def recalculate_avg_rating(book_id):
    reviews = load_reviews()
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    if not book_reviews:
        avg = 0.0
    else:
        avg = round(sum(r['rating'] for r in book_reviews) / len(book_reviews), 2)
    books = load_books()
    if book_id in books:
        books[book_id]['avg_rating'] = avg
        save_books(books)

# 1. Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# 2. Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    username = CURRENT_USER
    books = list(load_books().values())
    # Select featured books: Let's pick first 5 available or borrowed books as featured
    featured_books = []
    for b in books:
        if b['status'] in ['Available', 'Borrowed', 'Reserved']:
            featured_books.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'status': b['status']
            })
        if len(featured_books) >= 5:
            break
    return render_template('dashboard.html', username=username, featured_books=featured_books)

# 3. Book Catalog Page
@app.route('/catalog')
def book_catalog_page():
    search_query = request.args.get('search', '').strip()
    books = list(load_books().values())
    if search_query:
        sq = search_query.lower()
        filtered_books = []
        for b in books:
            if (sq in b['title'].lower() or
                sq in b['author'].lower() or
                sq in b['isbn'].lower() or
                sq in b['genre'].lower() or
                sq in b['publisher'].lower()):
                filtered_books.append(b)
        books = filtered_books
    # Map only required fields
    output_books = []
    for b in books:
        output_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('catalog.html', books=output_books, search_query=search_query)

# 4. Book Details Page
@app.route('/book/<int:book_id>')
def book_details_page(book_id):
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    book = books[book_id]
    reviews_all = load_reviews()
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
    return render_template('book_details.html', book=book, reviews=reviews)

# 5. Borrow Confirmation Page (GET)
@app.route('/borrow/<int:book_id>')
def borrow_confirmation_page(book_id):
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details_page', book_id=book_id))

    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = calculate_due_date(borrow_date)
    return render_template('borrow_confirmation.html', book=book, due_date=due_date)

# 5. Confirm Borrow (POST)
@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def confirm_borrow(book_id):
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details_page', book_id=book_id))

    borrowings = load_borrowings()
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = calculate_due_date(borrow_date)

    # Check if user already has an active borrow for this book
    for b in borrowings.values():
        if b['username'] == CURRENT_USER and b['book_id'] == book_id and b['status'] == 'Active':
            flash('You already have this book borrowed.')
            return redirect(url_for('book_details_page', book_id=book_id))

    # Create new borrow record
    borrow_id = get_new_id(borrowings)
    new_borrow = {
        'borrow_id': borrow_id,
        'username': CURRENT_USER,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings[borrow_id] = new_borrow
    save_borrowings(borrowings)

    # Update book status
    update_book_status(book_id, 'Borrowed')

    success = True
    return render_template('borrow_result.html', success=success, book=book, due_date=due_date)

# 5. Cancel Borrow (POST)
@app.route('/borrow/<int:book_id>/cancel', methods=['POST'])
def cancel_borrow(book_id):
    # Redirect back to book details
    return redirect(url_for('book_details_page', book_id=book_id))

# 6. My Borrowings Page (GET)
@app.route('/my-borrows')
def my_borrows_page():
    filter_status = request.args.get('filter', 'All')
    borrowings = load_borrowings()
    books = load_books()
    borrows_list = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            # Determine updated status for overdue
            status = b['status']
            if status == 'Active':
                due = datetime.strptime(b['due_date'], '%Y-%m-%d')
                if datetime.now() > due:
                    status = 'Overdue'
            borrows_list.append({
                'borrow_id': b['borrow_id'],
                'book_title': books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown',
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': status,
                'fine_amount': b['fine_amount']
            })
    # Apply filter
    if filter_status != 'All':
        borrows_list = [br for br in borrows_list if br['status'] == filter_status]
    return render_template('my_borrows.html', borrows=borrows_list, filter_status=filter_status)

# 6. Return Book (POST)
@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    if borrow_id not in borrowings:
        flash('Borrow record not found.')
        return redirect(url_for('my_borrows_page'))

    borrow = borrowings[borrow_id]
    if borrow['username'] != CURRENT_USER:
        flash('Unauthorized action.')
        return redirect(url_for('my_borrows_page'))

    if borrow['status'] == 'Returned':
        flash('Book already returned.')
        return redirect(url_for('my_borrows_page'))

    now_str = datetime.now().strftime('%Y-%m-%d')
    borrow['return_date'] = now_str
    due_date_dt = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
    return_date_dt = datetime.strptime(now_str, '%Y-%m-%d')

    # Check for overdue fine
    if return_date_dt > due_date_dt:
        days_late = (return_date_dt - due_date_dt).days
        fine_amount = days_late * 1.0  # $1 per day fine
        borrow['fine_amount'] = fine_amount
        borrow['status'] = 'Overdue'
        # Add fine record if not already exists for this borrow
        existing_fine = None
        for f in fines.values():
            if f['borrow_id'] == borrow_id and f['status'] == 'Unpaid':
                existing_fine = f
                break
        if existing_fine is None and fine_amount > 0:
            fine_id = get_new_id(fines)
            fine_date = now_str
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': CURRENT_USER,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': fine_date
            }
        save_fines(fines)
    else:
        borrow['status'] = 'Returned'
        borrow['fine_amount'] = 0.0

    save_borrowings(borrowings)
    # Update book status to Available
    update_book_status(borrow['book_id'], 'Available')

    success = True
    return render_template('return_confirmation.html', success=success, borrow_id=borrow_id)

# 7. My Reservations Page (GET)
@app.route('/my-reservations')
def my_reservations_page():
    reservations = load_reservations()
    books = load_books()

    user_reservations = []
    for r in reservations.values():
        if r['username'] == CURRENT_USER:
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_title': books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown',
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)

# 7. Cancel Reservation (POST)
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    if reservation_id not in reservations:
        flash('Reservation not found.')
        return redirect(url_for('my_reservations_page'))
    reservation = reservations[reservation_id]
    if reservation['username'] != CURRENT_USER:
        flash('Unauthorized action.')
        return redirect(url_for('my_reservations_page'))
    if reservation['status'] == 'Cancelled':
        flash('Reservation already cancelled.')
        return redirect(url_for('my_reservations_page'))

    reservation['status'] = 'Cancelled'
    save_reservations(reservations)

    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations_page'))

# 8. My Reviews Page (GET)
@app.route('/my-reviews')
def my_reviews_page():
    reviews = load_reviews()
    books = load_books()

    user_reviews = []
    for r in reviews.values():
        if r['username'] == CURRENT_USER:
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown',
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

# Route for deleting a review (not explicitly listed but implied by frontend spec)
@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = load_reviews()
    if review_id not in reviews:
        flash('Review not found.')
        return redirect(url_for('my_reviews_page'))
    review = reviews[review_id]
    if review['username'] != CURRENT_USER:
        flash('Unauthorized action.')
        return redirect(url_for('my_reviews_page'))
    book_id = review['book_id']
    del reviews[review_id]
    save_reviews(reviews)
    # Recalculate avg rating for book
    recalculate_avg_rating(book_id)

    flash('Review deleted successfully.')
    return redirect(url_for('my_reviews_page'))

# 9. Write Review Page (GET)
@app.route('/write-review/<int:book_id>')
def write_review_page(book_id):
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    book = books[book_id]
    reviews = load_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break
    return render_template('write_review.html', book=book, existing_review=existing_review)

# 9. Submit Review (POST)
@app.route('/submit-review/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    rating_str = request.form.get('rating', '')
    review_text = request.form.get('review_text', '').strip()

    if not rating_str.isdigit() or not (1 <= int(rating_str) <= 5):
        flash('Invalid rating. Must be between 1 and 5.')
        return redirect(url_for('write_review_page', book_id=book_id))

    rating = int(rating_str)
    review_date = datetime.now().strftime('%Y-%m-%d')

    reviews = load_reviews()
    existing_review_id = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review_id = r['review_id']
            break

    if existing_review_id is not None:
        # Update existing review
        reviews[existing_review_id]['rating'] = rating
        reviews[existing_review_id]['review_text'] = review_text
        reviews[existing_review_id]['review_date'] = review_date
    else:
        # Create new review
        review_id = get_new_id(reviews)
        reviews[review_id] = {
            'review_id': review_id,
            'username': CURRENT_USER,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
    save_reviews(reviews)
    # Recalculate average rating
    recalculate_avg_rating(book_id)

    flash('Review submitted successfully.')
    return redirect(url_for('book_details_page', book_id=book_id))

# 10. User Profile Page (GET)
@app.route('/profile')
def user_profile_page():
    users = load_users()
    borrowings = load_borrowings()
    books = load_books()

    if CURRENT_USER not in users:
        flash('User profile not found.')
        return redirect(url_for('dashboard_page'))

    user = users[CURRENT_USER]
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            borrow_history.append({
                'book_title': books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown',
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date'],
                'status': b['status']
            })

    return render_template('profile.html', username=user['username'], email=user['email'], phone=user['phone'], 
                           address=user['address'], borrow_history=borrow_history)

# 10. Update Profile (POST)
@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    users = load_users()
    if CURRENT_USER not in users:
        flash('User profile not found.')
        return redirect(url_for('dashboard_page'))

    # Update and save
    users[CURRENT_USER]['email'] = email
    users[CURRENT_USER]['phone'] = phone
    users[CURRENT_USER]['address'] = address
    save_users(users)

    flash('Profile updated successfully.')
    return redirect(url_for('user_profile_page'))

# 11. Payment Confirmation Page (GET)
@app.route('/payment/<int:fine_id>')
def payment_confirmation_page(fine_id):
    fines = load_fines()
    if fine_id not in fines:
        flash('Fine record not found.')
        return redirect(url_for('user_profile_page'))
    fine = fines[fine_id]
    if fine['username'] != CURRENT_USER:
        flash('Unauthorized access to fine record.')
        return redirect(url_for('user_profile_page'))
    return render_template('payment_confirmation.html', fine=fine)

# 11. Confirm Payment (POST)
@app.route('/payment/<int:fine_id>/confirm', methods=['POST'])
def confirm_payment(fine_id):
    fines = load_fines()
    if fine_id not in fines:
        flash('Fine record not found.')
        return redirect(url_for('user_profile_page'))
    fine = fines[fine_id]
    if fine['username'] != CURRENT_USER:
        flash('Unauthorized access to fine record.')
        return redirect(url_for('user_profile_page'))

    fine['status'] = 'Paid'
    save_fines(fines)

    flash('Payment confirmed. Thank you!')
    return redirect(url_for('user_profile_page'))

if __name__ == '__main__':
    app.run(debug=True)
