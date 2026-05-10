'''
Main backend application for OnlineLibrary web application.
Implements routing, business logic, and data file operations.
Uses Flask framework to serve pages and handle user interactions.
Data stored in local text files under 'data/' directory.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
DATA_DIR = 'data'
# Helper functions for file operations and data parsing
def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            username, email, phone, address = line.split('|')
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
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 10:
                continue
            book_id = parts[0]
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
                'avg_rating': float(parts[9]) if parts[9] else 0.0
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
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            borrow_id = parts[0]
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': parts[1],
                'book_id': parts[2],
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5] if parts[5] else None,
                'status': parts[6],
                'fine_amount': float(parts[7]) if parts[7] else 0.0
            }
    return borrowings
def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            return_date = b['return_date'] if b['return_date'] else ''
            line = '|'.join([
                b['borrow_id'], b['username'], b['book_id'], b['borrow_date'],
                b['due_date'], return_date, b['status'], f"{b['fine_amount']:.2f}"
            ])
            f.write(line + '\n')
def read_reservations():
    reservations = {}
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
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
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            review_id = parts[0]
            reviews[review_id] = {
                'review_id': review_id,
                'username': parts[1],
                'book_id': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                r['review_id'], r['username'], r['book_id'], str(r['rating']),
                r['review_text'], r['review_date']
            ])
            f.write(line + '\n')
def read_fines():
    fines = {}
    path = os.path.join(DATA_DIR, 'fines.txt')
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            fine_id = parts[0]
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': float(parts[3]),
                'status': parts[4],
                'date_issued': parts[5]
            }
    return fines
def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            line = '|'.join([
                fine['fine_id'], fine['username'], fine['borrow_id'],
                f"{fine['amount']:.2f}", fine['status'], fine['date_issued']
            ])
            f.write(line + '\n')
# Utility functions
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
def get_username():
    # For simplicity, assume a fixed logged-in user for this demo
    # In real app, implement proper authentication and session management
    return 'john_reader'
# Routes
@app.route('/')
def dashboard():
    username = get_username()
    books = read_books()
    # Featured books: top 3 by avg_rating and status Available or Reserved or Borrowed
    featured_books = sorted(books.values(), key=lambda b: b['avg_rating'], reverse=True)[:3]
    return render_template('dashboard.html', username=username, featured_books=featured_books)
@app.route('/book_catalog', methods=['GET', 'POST'])
def book_catalog():
    username = get_username()
    books = read_books()
    search_query = ''
    filtered_books = list(books.values())
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            filtered_books = [b for b in books.values()
                              if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('book_catalog.html', username=username, books=filtered_books, search_query=search_query)
@app.route('/book_details/<book_id>')
def book_details(book_id):
    username = get_username()
    books = read_books()
    reviews = read_reviews()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    # Sort reviews by date descending
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('book_details.html', username=username, book=book, reviews=book_reviews)
@app.route('/borrow_confirmation/<book_id>', methods=['GET', 'POST'])
def borrow_confirmation(book_id):
    username = get_username()
    books = read_books()
    borrowings = read_borrowings()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))
    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=14)
    if request.method == 'POST':
        if 'confirm-borrow-button' in request.form:
            # Create new borrowing record
            borrow_id = get_next_id(borrowings)
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': username,
                'book_id': book_id,
                'borrow_date': borrow_date.isoformat(),
                'due_date': due_date.isoformat(),
                'return_date': None,
                'status': 'Active',
                'fine_amount': 0.0
            }
            write_borrowings(borrowings)
            # Update book status to Borrowed
            book['status'] = 'Borrowed'
            books[book_id] = book
            write_books(books)
            flash(f'You have successfully borrowed "{book["title"]}".', 'success')
            return redirect(url_for('my_borrowings'))
        elif 'cancel-borrow-button' in request.form:
            return redirect(url_for('book_details', book_id=book_id))
    return render_template('borrow_confirmation.html', username=username, book=book,
                           borrow_date=borrow_date.isoformat(), due_date=due_date.isoformat())
@app.route('/my_borrowings', methods=['GET', 'POST'])
def my_borrowings():
    username = get_username()
    borrowings = read_borrowings()
    books = read_books()
    filter_status = request.args.get('filter-status', 'All')
    user_borrows = [b for b in borrowings.values() if b['username'] == username]
    if filter_status != 'All':
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]
    # Sort by borrow_date descending
    user_borrows.sort(key=lambda b: b['borrow_date'], reverse=True)
    # Attach book title for display
    for b in user_borrows:
        b['book_title'] = books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown'
    if request.method == 'POST':
        # Handle return book button
        for borrow in user_borrows:
            btn_name = f'return-book-button-{borrow["borrow_id"]}'
            if btn_name in request.form:
                # Process return
                borrowings = read_borrowings()  # reload to avoid conflicts
                if borrow['borrow_id'] not in borrowings:
                    flash('Borrow record not found.', 'error')
                    return redirect(url_for('my_borrowings'))
                b_record = borrowings[borrow['borrow_id']]
                if b_record['status'] != 'Active':
                    flash('Book is not currently borrowed.', 'error')
                    return redirect(url_for('my_borrowings'))
                return_date = datetime.now().date()
                b_record['return_date'] = return_date.isoformat()
                # Determine if overdue
                due_date = datetime.fromisoformat(b_record['due_date']).date()
                if return_date > due_date:
                    b_record['status'] = 'Overdue'
                    # Calculate fine: $1 per day overdue
                    days_overdue = (return_date - due_date).days
                    fine_amount = float(days_overdue) * 1.0
                    b_record['fine_amount'] = fine_amount
                    # Add fine record
                    fines = read_fines()
                    fine_id = get_next_id(fines)
                    fines[fine_id] = {
                        'fine_id': fine_id,
                        'username': username,
                        'borrow_id': b_record['borrow_id'],
                        'amount': fine_amount,
                        'status': 'Unpaid',
                        'date_issued': return_date.isoformat()
                    }
                    write_fines(fines)
                    flash(f'Book returned late. Fine of ${fine_amount:.2f} issued.', 'warning')
                else:
                    b_record['status'] = 'Returned'
                    b_record['fine_amount'] = 0.0
                    flash('Book returned successfully.', 'success')
                borrowings[b_record['borrow_id']] = b_record
                write_borrowings(borrowings)
                # Update book status to Available
                books = read_books()
                if b_record['book_id'] in books:
                    books[b_record['book_id']]['status'] = 'Available'
                    write_books(books)
                return redirect(url_for('my_borrowings'))
    return render_template('my_borrowings.html', username=username, borrows=user_borrows, filter_status=filter_status)
@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    username = get_username()
    reservations = read_reservations()
    books = read_books()
    user_reservations = [r for r in reservations.values() if r['username'] == username]
    # Sort by reservation_date descending
    user_reservations.sort(key=lambda r: r['reservation_date'], reverse=True)
    # Attach book title for display
    for r in user_reservations:
        r['book_title'] = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
    if request.method == 'POST':
        for res in user_reservations:
            btn_name = f'cancel-reservation-button-{res["reservation_id"]}'
            if btn_name in request.form:
                reservations = read_reservations()
                if res['reservation_id'] not in reservations:
                    flash('Reservation not found.', 'error')
                    return redirect(url_for('my_reservations'))
                r_record = reservations[res['reservation_id']]
                if r_record['status'] != 'Active':
                    flash('Reservation already cancelled or inactive.', 'error')
                    return redirect(url_for('my_reservations'))
                r_record['status'] = 'Cancelled'
                reservations[r_record['reservation_id']] = r_record
                write_reservations(reservations)
                # Update book status if needed
                books = read_books()
                if r_record['book_id'] in books:
                    # Only update if book status is Reserved and no other active reservations
                    book = books[r_record['book_id']]
                    if book['status'] == 'Reserved':
                        # Check if other active reservations exist
                        active_res = [r for r in reservations.values()
                                      if r['book_id'] == r_record['book_id'] and r['status'] == 'Active']
                        if not active_res:
                            book['status'] = 'Available'
                            books[r_record['book_id']] = book
                            write_books(books)
                flash('Reservation cancelled.', 'success')
                return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', username=username, reservations=user_reservations)
@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    username = get_username()
    reviews = read_reviews()
    books = read_books()
    user_reviews = [r for r in reviews.values() if r['username'] == username]
    # Attach book title for display
    for r in user_reviews:
        r['book_title'] = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
    if request.method == 'POST':
        # Check for edit or delete buttons
        for review in user_reviews:
            edit_btn = f'edit-review-button-{review["review_id"]}'
            delete_btn = f'delete-review-button-{review["review_id"]}'
            if edit_btn in request.form:
                return redirect(url_for('write_review', book_id=review['book_id'], review_id=review['review_id']))
            if delete_btn in request.form:
                reviews = read_reviews()
                if review['review_id'] in reviews:
                    del reviews[review['review_id']]
                    write_reviews(reviews)
                    # Update avg rating for book
                    update_book_avg_rating(review['book_id'])
                    flash('Review deleted.', 'success')
                else:
                    flash('Review not found.', 'error')
                return redirect(url_for('my_reviews'))
    return render_template('my_reviews.html', username=username, reviews=user_reviews)
@app.route('/write_review/<book_id>', methods=['GET', 'POST'])
@app.route('/write_review/<book_id>/<review_id>', methods=['GET', 'POST'])
def write_review(book_id, review_id=None):
    username = get_username()
    books = read_books()
    reviews = read_reviews()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    existing_review = None
    if review_id:
        existing_review = reviews.get(review_id)
        if not existing_review or existing_review['username'] != username:
            flash('Review not found or access denied.', 'error')
            return redirect(url_for('my_reviews'))
    if request.method == 'POST':
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash('Please select a valid rating between 1 and 5.', 'error')
            return render_template('write_review.html', username=username, book=book,
                                   review=existing_review, rating_input=rating, review_text=review_text)
        rating = int(rating)
        review_date = datetime.now().date().isoformat()
        if existing_review:
            # Update existing review
            reviews[review_id]['rating'] = rating
            reviews[review_id]['review_text'] = review_text
            reviews[review_id]['review_date'] = review_date
            flash('Review updated successfully.', 'success')
        else:
            # Create new review
            new_review_id = get_next_id(reviews)
            reviews[new_review_id] = {
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            flash('Review submitted successfully.', 'success')
        write_reviews(reviews)
        update_book_avg_rating(book_id)
        return redirect(url_for('book_details', book_id=book_id))
    # GET request
    rating_input = existing_review['rating'] if existing_review else ''
    review_text = existing_review['review_text'] if existing_review else ''
    return render_template('write_review.html', username=username, book=book,
                           review=existing_review, rating_input=rating_input, review_text=review_text)
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    username = get_username()
    users = read_users()
    borrowings = read_borrowings()
    if username not in users:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    user = users[username]
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if not new_email:
            flash('Email cannot be empty.', 'error')
            return render_template('user_profile.html', username=username, user=user, borrow_history=[])
        user['email'] = new_email
        users[username] = user
        write_users(users)
        flash('Profile updated successfully.', 'success')
    # Borrow history: all borrowings for user with status Returned or Overdue
    history = [b for b in borrowings.values() if b['username'] == username and b['status'] in ('Returned', 'Overdue')]
    books = read_books()
    for b in history:
        b['book_title'] = books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown'
    # Sort history by borrow_date descending
    history.sort(key=lambda b: b['borrow_date'], reverse=True)
    return render_template('user_profile.html', username=username, user=user, borrow_history=history)
@app.route('/payment_confirmation/<fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    username = get_username()
    fines = read_fines()
    if fine_id not in fines:
        flash('Fine record not found.', 'error')
        return redirect(url_for('user_profile'))
    fine = fines[fine_id]
    if fine['username'] != username:
        flash('Access denied.', 'error')
        return redirect(url_for('user_profile'))
    if request.method == 'POST':
        if 'confirm-payment-button' in request.form:
            # Mark fine as Paid
            fine['status'] = 'Paid'
            fines[fine_id] = fine
            write_fines(fines)
            # Also update borrowings fine_amount to 0 if applicable
            borrowings = read_borrowings()
            borrow_id = fine['borrow_id']
            if borrow_id in borrowings:
                borrowings[borrow_id]['fine_amount'] = 0.0
                # If borrow status was Overdue, update to Returned after payment
                if borrowings[borrow_id]['status'] == 'Overdue':
                    borrowings[borrow_id]['status'] = 'Returned'
                write_borrowings(borrowings)
            flash('Payment confirmed. Thank you!', 'success')
            return redirect(url_for('user_profile'))
        elif 'back-to-profile' in request.form:
            return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', username=username, fine=fine)
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)