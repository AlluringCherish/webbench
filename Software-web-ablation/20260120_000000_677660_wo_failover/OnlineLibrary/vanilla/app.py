from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key in production

# Define data file paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# Simulate logged in user (for this spec we assume only one active user context)
# In real app, session or authentication system is needed.
CURRENT_USERNAME = 'john_reader'

# Helper functions to read/write and parse data files

# Users

def read_users():
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
                username,email,phone,address = parts
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
        print(f"Error writing users: {e}")

# Books

def read_books():
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
                    b['publisher'], str(b['year']), b['description'], b['status'], f"{b['avg_rating']:.1f}"
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing books: {e}")

# Borrowings

def read_borrowings():
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
                return_date = parts[5] if parts[5] else None
                status = parts[6]
                fine_amount = float(parts[7])
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
            for brw in borrowings.values():
                return_date = brw['return_date'] if brw['return_date'] is not None else ''
                line = '|'.join([
                    str(brw['borrow_id']), brw['username'], str(brw['book_id']), brw['borrow_date'],
                    brw['due_date'], return_date, brw['status'], f"{brw['fine_amount']:.2f}"
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing borrowings: {e}")

# Reservations

def read_reservations():
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

def write_reservations(reservations):
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for res in reservations.values():
                line = '|'.join([
                    str(res['reservation_id']), res['username'], str(res['book_id']), res['reservation_date'], res['status']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing reservations: {e}")

# Reviews

def read_reviews():
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
            for rev in reviews.values():
                line = '|'.join([
                    str(rev['review_id']), rev['username'], str(rev['book_id']), str(rev['rating']), rev['review_text'], rev['review_date']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing reviews: {e}")

# Fines

def read_fines():
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
            for fine in fines.values():
                line = '|'.join([
                    str(fine['fine_id']), fine['username'], str(fine['borrow_id']), f"{fine['amount']:.2f}", fine['status'], fine['date_issued']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error writing fines: {e}")

# Utility functions

def get_next_id(items_dict):
    if not items_dict:
        return 1
    return max(items_dict.keys()) + 1

# Check and update statuses on borrowed books to reflect overdue

def update_borrow_statuses(borrowings):
    today = datetime.date.today()
    changed = False
    for brw in borrowings.values():
        if brw['status'] == 'Active':
            due = datetime.datetime.strptime(brw['due_date'], '%Y-%m-%d').date()
            if today > due:
                brw['status'] = 'Overdue'
                # potentially calculate fine here or in view
                changed = True
    if changed:
        write_borrowings(borrowings)

# Calculate fine amount for overdue days

def calculate_fine(due_date_str, return_date_str):
    try:
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        return_date = datetime.datetime.strptime(return_date_str, '%Y-%m-%d').date()
        overdue_days = (return_date - due_date).days
        if overdue_days > 0:
            return float(overdue_days)  # 1 unit fine per day
        return 0.0
    except:
        return 0.0

# Routes implementation

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = CURRENT_USERNAME
    return render_template('dashboard.html', username=username)

@app.route('/catalog', methods=['GET'])
def book_catalog():
    books = list(read_books().values())
    # For each book, show book_id, title, author, status
    catalog_books = []
    for b in books:
        catalog_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('catalog.html', books=catalog_books)

@app.route('/book/<int:book_id>', methods=['GET'])
def book_details(book_id):
    books = read_books()
    reviews = read_reviews()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    # Collect reviews for this book
    book_reviews = []
    for rev in reviews.values():
        if rev['book_id'] == book_id:
            book_reviews.append({
                'review_id': rev['review_id'],
                'username': rev['username'],
                'rating': rev['rating'],
                'review_text': rev['review_text'],
                'review_date': rev['review_date']
            })
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/borrow/<int:book_id>', methods=['GET'])
def borrow_confirm_get(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))
    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    book_info = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author']
    }
    return render_template('borrow_confirm.html', book=book_info, due_date=due_date)

@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def borrow_confirm_post(book_id):
    books = read_books()
    borrowings = read_borrowings()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    # Confirm borrow
    borrow_id = get_next_id(borrowings)
    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(days=14)
    borrow_entry = {
        'borrow_id': borrow_id,
        'username': CURRENT_USERNAME,
        'book_id': book_id,
        'borrow_date': borrow_date.strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings[borrow_id] = borrow_entry

    # Update book status to Borrowed
    book['status'] = 'Borrowed'
    write_books(books)
    write_borrowings(borrowings)

    due_date_str = due_date.strftime('%Y-%m-%d')
    book_info = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author']
    }
    flash('Book borrowed successfully.')
    return render_template('borrow_confirm.html', book=book_info, due_date=due_date_str)

@app.route('/borrow/<int:book_id>/cancel', methods=['POST', 'GET'])
def borrow_cancel(book_id):
    return redirect(url_for('book_details', book_id=book_id))

@app.route('/my_borrows', methods=['GET'])
def my_borrows():
    borrowings = read_borrowings()
    books = read_books()
    update_borrow_statuses(borrowings)  # Update any overdue status if needed
    user_borrows = []
    for brw in borrowings.values():
        if brw['username'] == CURRENT_USERNAME:
            book = books.get(brw['book_id'], None)
            title = book['title'] if book else 'Unknown'
            user_borrows.append({
                'borrow_id': brw['borrow_id'],
                'title': title,
                'borrow_date': brw['borrow_date'],
                'due_date': brw['due_date'],
                'status': brw['status'],
                'fine_amount': brw['fine_amount']
            })
    return render_template('my_borrows.html', borrows=user_borrows)

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    books = read_books()
    fines = read_fines()

    brw = borrowings.get(borrow_id)
    if not brw or brw['username'] != CURRENT_USERNAME:
        flash('Borrow record not found or unauthorized.')
        return redirect(url_for('my_borrows'))

    if brw['status'] == 'Returned':
        flash('Book already returned.')
        return redirect(url_for('my_borrows'))

    return_date = datetime.date.today()
    brw['return_date'] = return_date.strftime('%Y-%m-%d')
    # Calculate fine if overdue
    fine_amount = calculate_fine(brw['due_date'], brw['return_date'])
    brw['fine_amount'] = fine_amount

    if fine_amount > 0.0:
        brw['status'] = 'Overdue'
        # add fine record if none exists for this borrow
        existing_fine = next((f for f in fines.values() if f['borrow_id'] == borrow_id and f['username'] == CURRENT_USERNAME and f['status'] == 'Unpaid'), None)
        if not existing_fine:
            fine_id = get_next_id(fines)
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': CURRENT_USERNAME,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': return_date.strftime('%Y-%m-%d')
            }
    else:
        brw['status'] = 'Returned'

    # Update book status to Available
    book = books.get(brw['book_id'])
    if book:
        book['status'] = 'Available'

    write_borrowings(borrowings)
    write_books(books)
    write_fines(fines)

    flash('Book returned successfully.')

    # Prepare updated user borrows
    user_borrows = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USERNAME:
            book = books.get(b['book_id'], None)
            title = book['title'] if book else 'Unknown'
            user_borrows.append({
                'borrow_id': b['borrow_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            })
    return render_template('my_borrows.html', borrows=user_borrows)

@app.route('/my_reservations', methods=['GET'])
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    user_reservations = []
    for res in reservations.values():
        if res['username'] == CURRENT_USERNAME:
            book = books.get(res['book_id'], None)
            title = book['title'] if book else 'Unknown'
            user_reservations.append({
                'reservation_id': res['reservation_id'],
                'title': title,
                'reservation_date': res['reservation_date'],
                'status': res['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    res = reservations.get(reservation_id)
    if not res or res['username'] != CURRENT_USERNAME:
        flash('Reservation not found or unauthorized.')
        return redirect(url_for('my_reservations'))
    if res['status'] == 'Cancelled':
        flash('Reservation already cancelled.')
        return redirect(url_for('my_reservations'))
    res['status'] = 'Cancelled'
    write_reservations(reservations)
    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations'))

@app.route('/my_reviews', methods=['GET'])
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    user_reviews = []
    for rev in reviews.values():
        if rev['username'] == CURRENT_USERNAME:
            book = books.get(rev['book_id'], None)
            title = book['title'] if book else 'Unknown'
            user_reviews.append({
                'review_id': rev['review_id'],
                'title': title,
                'rating': rev['rating'],
                'review_text': rev['review_text'],
                'review_date': rev['review_date']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/review/edit/<int:review_id>', methods=['GET'])
def edit_review_get(review_id):
    reviews = read_reviews()
    books = read_books()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USERNAME:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))
    book = books.get(review['book_id'])
    if not book:
        flash('Book not found for this review.')
        return redirect(url_for('my_reviews'))
    review_info = {
        'review_id': review['review_id'],
        'book_id': review['book_id'],
        'rating': review['rating'],
        'review_text': review['review_text']
    }
    book_info = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author']
    }
    return render_template('write_review.html', review=review_info, book=book_info)

@app.route('/review/edit/<int:review_id>', methods=['POST'])
def edit_review_post(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USERNAME:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))
    
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        flash('Rating must be an integer between 1 and 5.')
        return redirect(url_for('edit_review_get', review_id=review_id))
    if not review_text:
        flash('Review text cannot be empty.')
        return redirect(url_for('edit_review_get', review_id=review_id))
    rating = int(rating)

    # Update review
    review['rating'] = rating
    review['review_text'] = review_text
    # Update review_date to today
    review['review_date'] = datetime.date.today().strftime('%Y-%m-%d')

    write_reviews(reviews)
    flash('Review updated successfully.')
    return redirect(url_for('my_reviews'))

@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USERNAME:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))
    del reviews[review_id]
    write_reviews(reviews)
    flash('Review deleted successfully.')
    return redirect(url_for('my_reviews'))

@app.route('/review/write/<int:book_id>', methods=['GET'])
def write_review_get(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book_info = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status'],
        'description': book['description'],
        'avg_rating': book['avg_rating']
    }
    return render_template('write_review.html', book=book_info)

@app.route('/review/write/<int:book_id>', methods=['POST'])
def write_review_post(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews = read_reviews()
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        flash('Rating must be an integer between 1 and 5.')
        return redirect(url_for('write_review_get', book_id=book_id))
    if not review_text:
        flash('Review text cannot be empty.')
        return redirect(url_for('write_review_get', book_id=book_id))
    rating = int(rating)

    review_id = get_next_id(reviews)
    new_review = {
        'review_id': review_id,
        'username': CURRENT_USERNAME,
        'book_id': book_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': datetime.date.today().strftime('%Y-%m-%d')
    }
    reviews[review_id] = new_review
    write_reviews(reviews)

    # Update average rating on book
    book = books[book_id]
    # gather all ratings
    ratings = [rev['rating'] for rev in reviews.values() if rev['book_id'] == book_id]
    if ratings:
        avg_rating = round(sum(ratings) / len(ratings), 1)
    else:
        avg_rating = 0.0
    book['avg_rating'] = avg_rating
    write_books(books)

    flash('Review added successfully.')
    return redirect(url_for('book_details', book_id=book_id))

@app.route('/profile', methods=['GET'])
def user_profile():
    users = read_users()
    borrowings = read_borrowings()
    books = read_books()
    user = users.get(CURRENT_USERNAME)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    borrow_history = []
    for brw in borrowings.values():
        if brw['username'] == CURRENT_USERNAME:
            book_title = books.get(brw['book_id'], {}).get('title', 'Unknown')
            borrow_history.append({
                'title': book_title,
                'borrow_date': brw['borrow_date'],
                'return_date': brw['return_date']
            })
    return render_template('profile.html', username=CURRENT_USERNAME, email=user['email'], borrow_history=borrow_history)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    users = read_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    email = request.form.get('email')
    # phone and address not exposed/updated per spec
    if not email or '@' not in email:
        flash('Invalid email address.')
        return redirect(url_for('user_profile'))
    user['email'] = email
    users[CURRENT_USERNAME] = user
    write_users(users)
    flash('Profile updated successfully.')
    return redirect(url_for('user_profile'))

@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation_get(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USERNAME:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))
    if fine['status'] == 'Paid':
        flash('Fine already paid.')
        return redirect(url_for('user_profile'))
    return render_template('payment_confirmation.html', fine_amount=fine['amount'], fine_id=fine_id)

@app.route('/payment/<int:fine_id>/confirm', methods=['POST'])
def payment_confirmation_post(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USERNAME:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))
    if fine['status'] == 'Paid':
        flash('Fine already paid.')
        return redirect(url_for('user_profile'))
    fine['status'] = 'Paid'
    write_fines(fines)
    flash('Payment successful. Thank you!')
    return redirect(url_for('user_profile'))

# Run the app if executed directly
if __name__ == '__main__':
    app.run(debug=True)
