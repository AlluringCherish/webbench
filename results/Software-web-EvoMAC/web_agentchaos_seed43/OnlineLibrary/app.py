'''
Backend implementation for the 'OnlineLibrary' web application.
Provides routing and functionality for user management, book catalog,
borrowings, reservations, reviews, fines, and payments.
Data is stored in local text files under the 'data' directory.
The website starts at the Dashboard page ('/').
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
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
                'avg_rating': float(parts[9])
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
                'return_date': parts[5] if parts[5] else None,
                'status': parts[6],
                'fine_amount': float(parts[7])
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
def save_users(users):
    lines = []
    for u in users:
        lines.append(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}")
    write_file_lines('users.txt', lines)
def save_books(books):
    lines = []
    for b in books:
        lines.append(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}")
    write_file_lines('books.txt', lines)
def save_borrowings(borrowings):
    lines = []
    for b in borrowings:
        return_date = b['return_date'] if b['return_date'] else ''
        lines.append(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date}|{b['status']}|{b['fine_amount']}")
    write_file_lines('borrowings.txt', lines)
def save_reservations(reservations):
    lines = []
    for r in reservations:
        lines.append(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}")
    write_file_lines('reservations.txt', lines)
def save_reviews(reviews):
    lines = []
    for r in reviews:
        lines.append(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}")
    write_file_lines('reviews.txt', lines)
def save_fines(fines):
    lines = []
    for f in fines:
        lines.append(f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']}|{f['status']}|{f['date_issued']}")
    write_file_lines('fines.txt', lines)
# Helper to get next ID for borrowings, reservations, reviews, fines
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# For simplicity, assume a fixed logged-in user for this demo
# In real app, implement authentication and session management
LOGGED_IN_USERNAME = 'john_reader'
# ROUTES
@app.route('/')
def dashboard():
    # Dashboard page: show welcome message and featured books (e.g. top 3 by avg_rating)
    books = parse_books()
    # Sort by avg_rating descending
    featured_books = sorted(books, key=lambda b: b['avg_rating'], reverse=True)[:3]
    return render_template('dashboard.html',
                           username=LOGGED_IN_USERNAME,
                           featured_books=featured_books)
@app.route('/catalog', methods=['GET', 'POST'])
def book_catalog():
    books = parse_books()
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').strip().lower()
        if search_query:
            books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower()]
    return render_template('book_catalog.html',
                           books=books,
                           search_query=search_query)
@app.route('/book/<book_id>')
def book_details(book_id):
    books = parse_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    reviews = parse_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    # Determine if user can borrow (book status must be Available)
    can_borrow = (book['status'] == 'Available')
    return render_template('book_details.html',
                           book=book,
                           reviews=book_reviews,
                           can_borrow=can_borrow,
                           username=LOGGED_IN_USERNAME)
@app.route('/borrow/<book_id>', methods=['GET', 'POST'])
def borrow_confirmation(book_id):
    books = parse_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))
    if request.method == 'POST':
        # Confirm borrow
        borrowings = parse_borrowings()
        new_borrow_id = get_next_id(borrowings, 'borrow_id')
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        new_borrow = {
            'borrow_id': new_borrow_id,
            'username': LOGGED_IN_USERNAME,
            'book_id': book_id,
            'borrow_date': borrow_date.isoformat(),
            'due_date': due_date.isoformat(),
            'return_date': None,
            'status': 'Active',
            'fine_amount': 0.0
        }
        borrowings.append(new_borrow)
        save_borrowings(borrowings)
        # Update book status to Borrowed
        for b in books:
            if b['book_id'] == book_id:
                b['status'] = 'Borrowed'
                break
        save_books(books)
        flash(f"You have successfully borrowed '{book['title']}'. Due date: {due_date.isoformat()}", 'success')
        return redirect(url_for('my_borrowings'))
    # GET: show confirmation page
    due_date = (datetime.now().date() + timedelta(days=14)).isoformat()
    return render_template('borrow_confirmation.html',
                           book=book,
                           due_date=due_date)
@app.route('/my_borrowings', methods=['GET', 'POST'])
def my_borrowings():
    borrowings = parse_borrowings()
    books = parse_books()
    filter_status = request.args.get('filter-status', 'All')
    user_borrowings = [b for b in borrowings if b['username'] == LOGGED_IN_USERNAME]
    if filter_status != 'All':
        user_borrowings = [b for b in user_borrowings if b['status'] == filter_status]
    # Enrich borrowings with book title
    for b in user_borrowings:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        b['title'] = book['title'] if book else 'Unknown'
    return render_template('my_borrowings.html',
                           borrowings=user_borrowings,
                           filter_status=filter_status)
@app.route('/return/<borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = parse_borrowings()
    books = parse_books()
    fines = parse_fines()
    borrow = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == LOGGED_IN_USERNAME), None)
    if not borrow:
        flash('Borrow record not found.', 'error')
        return redirect(url_for('my_borrowings'))
    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        flash('This book is already returned.', 'info')
        return redirect(url_for('my_borrowings'))
    # Mark return date as today
    return_date = datetime.now().date()
    borrow['return_date'] = return_date.isoformat()
    # Update status to Returned
    borrow['status'] = 'Returned'
    # Update book status to Available
    book = next((b for b in books if b['book_id'] == borrow['book_id']), None)
    if book:
        book['status'] = 'Available'
    # If overdue and fine unpaid, keep fine record
    # If overdue and fine paid or no fine, clear fine_amount
    if borrow['fine_amount'] > 0:
        # Check if fine is paid
        fine_record = next((f for f in fines if f['borrow_id'] == borrow_id and f['username'] == LOGGED_IN_USERNAME), None)
        if fine_record and fine_record['status'] == 'Paid':
            borrow['fine_amount'] = 0.0
        else:
            # Fine unpaid, keep amount
            pass
    else:
        borrow['fine_amount'] = 0.0
    save_borrowings(borrowings)
    save_books(books)
    flash(f"Book '{book['title']}' returned successfully.", 'success')
    return redirect(url_for('my_borrowings'))
@app.route('/my_reservations', methods=['GET'])
def my_reservations():
    reservations = parse_reservations()
    books = parse_books()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USERNAME]
    # Enrich with book title
    for r in user_reservations:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        r['title'] = book['title'] if book else 'Unknown'
    return render_template('my_reservations.html',
                           reservations=user_reservations)
@app.route('/cancel_reservation/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = parse_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME), None)
    if not reservation:
        flash('Reservation not found.', 'error')
        return redirect(url_for('my_reservations'))
    if reservation['status'] != 'Active':
        flash('Reservation already cancelled or inactive.', 'info')
        return redirect(url_for('my_reservations'))
    reservation['status'] = 'Cancelled'
    save_reservations(reservations)
    flash('Reservation cancelled successfully.', 'success')
    return redirect(url_for('my_reservations'))
@app.route('/my_reviews')
def my_reviews():
    reviews = parse_reviews()
    books = parse_books()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USERNAME]
    # Enrich with book title
    for r in user_reviews:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        r['title'] = book['title'] if book else 'Unknown'
    return render_template('my_reviews.html',
                           reviews=user_reviews)
@app.route('/write_review/<book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    books = parse_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    reviews = parse_reviews()
    existing_review = next((r for r in reviews if r['username'] == LOGGED_IN_USERNAME and r['book_id'] == book_id), None)
    if request.method == 'POST':
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not rating or rating not in ['1','2','3','4','5']:
            flash('Please select a valid rating.', 'error')
            return redirect(url_for('write_review', book_id=book_id))
        if not review_text:
            flash('Review text cannot be empty.', 'error')
            return redirect(url_for('write_review', book_id=book_id))
        rating_int = int(rating)
        review_date = datetime.now().date().isoformat()
        if existing_review:
            # Edit existing review
            existing_review['rating'] = rating_int
            existing_review['review_text'] = review_text
            existing_review['review_date'] = review_date
        else:
            # Add new review
            new_review_id = get_next_id(reviews, 'review_id')
            new_review = {
                'review_id': new_review_id,
                'username': LOGGED_IN_USERNAME,
                'book_id': book_id,
                'rating': rating_int,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews.append(new_review)
        save_reviews(reviews)
        # Update book average rating
        book_reviews = [r for r in reviews if r['book_id'] == book_id]
        avg_rating = round(sum(r['rating'] for r in book_reviews) / len(book_reviews), 2)
        for b in books:
            if b['book_id'] == book_id:
                b['avg_rating'] = avg_rating
                break
        save_books(books)
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('book_details', book_id=book_id))
    # GET: show write/edit review page
    rating_val = existing_review['rating'] if existing_review else None
    review_text_val = existing_review['review_text'] if existing_review else ''
    return render_template('write_review.html',
                           book=book,
                           rating=rating_val,
                           review_text=review_text_val)
@app.route('/edit_review/<review_id>', methods=['GET'])
def edit_review(review_id):
    reviews = parse_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == LOGGED_IN_USERNAME), None)
    if not review:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))
    return redirect(url_for('write_review', book_id=review['book_id']))
@app.route('/delete_review/<review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = parse_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == LOGGED_IN_USERNAME), None)
    if not review:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))
    book_id = review['book_id']
    reviews = [r for r in reviews if r['review_id'] != review_id]
    save_reviews(reviews)
    # Update book average rating
    books = parse_books()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    if book_reviews:
        avg_rating = round(sum(r['rating'] for r in book_reviews) / len(book_reviews), 2)
    else:
        avg_rating = 0.0
    for b in books:
        if b['book_id'] == book_id:
            b['avg_rating'] = avg_rating
            break
    save_books(books)
    flash('Review deleted successfully.', 'success')
    return redirect(url_for('my_reviews'))
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = parse_users()
    user = next((u for u in users if u['username'] == LOGGED_IN_USERNAME), None)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if not new_email:
            flash('Email cannot be empty.', 'error')
            return redirect(url_for('user_profile'))
        # Update email
        user['email'] = new_email
        save_users(users)
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_profile'))
    # Show borrow history (all borrowings returned or overdue)
    borrowings = parse_borrowings()
    books = parse_books()
    history = [b for b in borrowings if b['username'] == LOGGED_IN_USERNAME and b['status'] in ('Returned', 'Overdue')]
    # Enrich with book title
    for b in history:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        b['title'] = book['title'] if book else 'Unknown'
    return render_template('user_profile.html',
                           user=user,
                           borrow_history=history)
@app.route('/payment/<borrow_id>', methods=['GET', 'POST'])
def payment_confirmation(borrow_id):
    borrowings = parse_borrowings()
    fines = parse_fines()
    borrow = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == LOGGED_IN_USERNAME), None)
    if not borrow:
        flash('Borrow record not found.', 'error')
        return redirect(url_for('user_profile'))
    fine = next((f for f in fines if f['borrow_id'] == borrow_id and f['username'] == LOGGED_IN_USERNAME and f['status'] == 'Unpaid'), None)
    if not fine:
        flash('No unpaid fine found for this borrow.', 'info')
        return redirect(url_for('user_profile'))
    if request.method == 'POST':
        # Confirm payment
        fine['status'] = 'Paid'
        save_fines(fines)
        # Update borrow fine_amount to 0
        borrow['fine_amount'] = 0.0
        save_borrowings(borrowings)
        flash('Payment confirmed. Thank you!', 'success')
        return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html',
                           fine_amount=fine['amount'])
# Run the app
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)