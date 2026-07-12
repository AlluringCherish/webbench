from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 's3cr3tkey'

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
            f.write(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}\n")


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
            fields = line.split('|')
            if len(fields) < 10:
                continue
            (book_id, title, author, isbn, genre, publisher, year, description,
             status, avg_rating) = fields
            try:
                book_id = int(book_id)
                avg_rating = float(avg_rating)
            except ValueError:
                continue
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
    return books


def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books.values():
            f.write(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}\n")


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
            fields = line.split('|')
            if len(fields) < 8:
                continue
            borrow_id, username, book_id, borrow_date, due_date, return_date, status, fine_amount = fields
            try:
                borrow_id = int(borrow_id)
                book_id = int(book_id)
                fine_amount = float(fine_amount)
            except ValueError:
                continue
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': username,
                'book_id': book_id,
                'borrow_date': borrow_date,
                'due_date': due_date,
                'return_date': return_date if return_date != '' else None,
                'status': status,
                'fine_amount': fine_amount
            }
    return borrowings


def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            return_date = b['return_date'] if b['return_date'] is not None else ''
            f.write(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date}|{b['status']}|{b['fine_amount']}\n")


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
            reservation_id, username, book_id, reservation_date, status = line.split('|')
            try:
                reservation_id = int(reservation_id)
                book_id = int(book_id)
            except ValueError:
                continue
            reservations[reservation_id] = {
                'reservation_id': reservation_id,
                'username': username,
                'book_id': book_id,
                'reservation_date': reservation_date,
                'status': status
            }
    return reservations


def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            f.write(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n")


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
            review_id, username, book_id, rating, review_text, review_date = line.split('|', 5)
            try:
                review_id = int(review_id)
                book_id = int(book_id)
                rating = int(rating)
            except ValueError:
                continue
            reviews[review_id] = {
                'review_id': review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
    return reviews


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            f.write(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")


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
            fine_id, username, borrow_id, amount, status, date_issued = line.split('|')
            try:
                fine_id = int(fine_id)
                borrow_id = int(borrow_id)
                amount = float(amount)
            except ValueError:
                continue
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': username,
                'borrow_id': borrow_id,
                'amount': amount,
                'status': status,
                'date_issued': date_issued
            }
    return fines


def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fn in fines.values():
            f.write(f"{fn['fine_id']}|{fn['username']}|{fn['borrow_id']}|{fn['amount']}|{fn['status']}|{fn['date_issued']}\n")


# For this implementation we assume current logged in username is fixed for demonstration
# In real app, user session management must be properly implemented
CURRENT_USER = 'john_reader'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    return render_template('dashboard.html', username=username)


@app.route('/catalog')
def book_catalog():
    books_data = read_books()
    # Provide books as list of dicts with needed fields
    books = []
    for b in books_data.values():
        books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('catalog.html', books=books)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    # reviews for book
    reviews_data = read_reviews()
    book_reviews = []
    for r in reviews_data.values():
        if r['book_id'] == book_id:
            book_reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/borrow/<int:book_id>', methods=['GET'])
def borrow_confirm(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    minimal_book = {'book_id': book['book_id'], 'title': book['title'], 'author': book['author']}

    return render_template('borrow_confirmation.html', book=minimal_book, due_date=due_date)


@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def borrow_confirm_post(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]
    minimal_book = {'book_id': book['book_id'], 'title': book['title'], 'author': book['author']}

    action = request.form.get('confirm')
    if action != 'yes':
        # Cancelled
        confirmation_status = 'cancelled'
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        return render_template('borrow_confirmation.html', book=minimal_book, due_date=due_date, confirmation_status=confirmation_status)

    # Confirm borrow
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    borrowings = read_borrowings()
    # Generate new borrow_id
    new_borrow_id = 1
    if borrowings:
        new_borrow_id = max(borrowings.keys()) + 1

    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

    borrowings[new_borrow_id] = {
        'borrow_id': new_borrow_id,
        'username': CURRENT_USER,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    # Update book status
    books[book_id]['status'] = 'Borrowed'

    # Save updated data
    write_borrowings(borrowings)
    write_books(books)

    confirmation_status = 'success'
    return render_template('borrow_confirmation.html', book=minimal_book, due_date=due_date, confirmation_status=confirmation_status)


@app.route('/my-borrows', methods=['GET'])
def my_borrowings():
    borrowings = read_borrowings()
    books = read_books()
    # Filter borrowings by CURRENT_USER
    user_borrows = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            book_title = books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown'
            user_borrows.append({
                'borrow_id': b['borrow_id'],
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            })
    return render_template('my_borrowings.html', borrows=user_borrows)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    books = read_books()
    fines = read_fines()

    if borrow_id not in borrowings:
        borrow = None
        return_status = 'failure'
        flash('Borrow record not found.')
        return render_template('return_confirmation.html', borrow=borrow, return_status=return_status)

    borrow = borrowings[borrow_id]
    if borrow['username'] != CURRENT_USER:
        borrow = None
        return_status = 'failure'
        flash('Unauthorized access to borrow record.')
        return render_template('return_confirmation.html', borrow=borrow, return_status=return_status)

    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        # Already returned
        book_title = books[borrow['book_id']]['title'] if borrow['book_id'] in books else 'Unknown'
        borrow_info = {'borrow_id': borrow_id, 'book_title': book_title}
        return_status = 'failure'
        flash('Book already returned or borrowing not active.')
        return render_template('return_confirmation.html', borrow=borrow_info, return_status=return_status)

    # Process return
    return_date = datetime.now().strftime('%Y-%m-%d')
    borrowings[borrow_id]['return_date'] = return_date
    borrowings[borrow_id]['status'] = 'Returned'

    # Update book status
    book_id = borrow['book_id']
    if book_id in books:
        books[book_id]['status'] = 'Available'

    # Check if fine is applicable (for overdue)
    due_date_obj = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
    return_date_obj = datetime.strptime(return_date, '%Y-%m-%d')

    late_days = (return_date_obj - due_date_obj).days
    if late_days > 0:
        fine_amount = late_days * 1.0  # Assuming 1.0 currency unit per day
        borrowings[borrow_id]['fine_amount'] = fine_amount

        # Add new fine
        new_fine_id = 1
        if fines:
            new_fine_id = max(fines.keys()) + 1
        fines[new_fine_id] = {
            'fine_id': new_fine_id,
            'username': CURRENT_USER,
            'borrow_id': borrow_id,
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': return_date
        }

        write_fines(fines)

    else:
        borrowings[borrow_id]['fine_amount'] = 0.0

    # Save updates
    write_borrowings(borrowings)
    write_books(books)

    book_title = books[book_id]['title'] if book_id in books else 'Unknown'
    borrow_info = {'borrow_id': borrow_id, 'book_title': book_title}
    return_status = 'success'

    return render_template('return_confirmation.html', borrow=borrow_info, return_status=return_status)


@app.route('/my-reservations', methods=['GET'])
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    user_reservations = []
    for r in reservations.values():
        if r['username'] == CURRENT_USER:
            book_title = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    if reservation_id not in reservations:
        cancel_status = 'failure'
        flash('Reservation not found.')
        # Get user's reservations anyway for template
        user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]
        books = read_books()
        user_reservations_out = []
        for r in user_reservations:
            book_title = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
            user_reservations_out.append({
                'reservation_id': r['reservation_id'],
                'book_title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
        return render_template('my_reservations.html', reservations=user_reservations_out, cancel_status=cancel_status)

    reservation = reservations[reservation_id]
    if reservation['username'] != CURRENT_USER:
        cancel_status = 'failure'
        flash('Unauthorized access to reservation.')
        user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]
        books = read_books()
        user_reservations_out = []
        for r in user_reservations:
            book_title = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
            user_reservations_out.append({
                'reservation_id': r['reservation_id'],
                'book_title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
        return render_template('my_reservations.html', reservations=user_reservations_out, cancel_status=cancel_status)

    # Cancel reservation
    if reservation['status'] == 'Cancelled':
        cancel_status = 'failure'
        flash('Reservation already cancelled.')
    else:
        reservation['status'] = 'Cancelled'
        write_reservations(reservations)
        cancel_status = 'success'

    user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]
    books = read_books()
    user_reservations_out = []
    for r in user_reservations:
        book_title = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
        user_reservations_out.append({
            'reservation_id': r['reservation_id'],
            'book_title': book_title,
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=user_reservations_out, cancel_status=cancel_status)


@app.route('/my-reviews', methods=['GET'])
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    user_reviews = []
    for r in reviews.values():
        if r['username'] == CURRENT_USER:
            book_title = books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown'
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': book_title,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/review/write/<int:book_id>', methods=['GET'])
def write_review(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    minimal_book = {'book_id': book['book_id'], 'title': book['title'], 'author': book['author']}
    return render_template('write_review.html', book=minimal_book, existing_review=existing_review)


@app.route('/review/submit/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        submission_status = 'failure'
        minimal_book = {'book_id': book_id, 'title': '', 'author': ''}
        return render_template('write_review.html', submission_status=submission_status, book=minimal_book)

    rating_raw = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating_raw or not rating_raw.isdigit():
        flash('Invalid rating.')
        submission_status = 'failure'
        minimal_book = {'book_id': book_id, 'title': books[book_id]['title'], 'author': books[book_id]['author']}
        return render_template('write_review.html', submission_status=submission_status, book=minimal_book)

    rating = int(rating_raw)
    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.')
        submission_status = 'failure'
        minimal_book = {'book_id': book_id, 'title': books[book_id]['title'], 'author': books[book_id]['author']}
        return render_template('write_review.html', submission_status=submission_status, book=minimal_book)

    reviews = read_reviews()
    # Check if existing review by user for this book
    found_review_id = None
    for r_id, r in reviews.items():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            found_review_id = r_id
            break

    review_date = datetime.now().strftime('%Y-%m-%d')

    if found_review_id is not None:
        # Update existing review
        reviews[found_review_id]['rating'] = rating
        reviews[found_review_id]['review_text'] = review_text
        reviews[found_review_id]['review_date'] = review_date
    else:
        # New review
        new_review_id = 1
        if reviews:
            new_review_id = max(reviews.keys()) + 1
        reviews[new_review_id] = {
            'review_id': new_review_id,
            'username': CURRENT_USER,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

    write_reviews(reviews)

    # update avg_rating of book
    books = read_books()  # reload to be safe
    # calculate avg
    total_rating = 0
    count = 0
    for r in reviews.values():
        if r['book_id'] == book_id:
            total_rating += r['rating']
            count += 1
    avg_rating = (total_rating / count) if count > 0 else 0.0
    books[book_id]['avg_rating'] = round(avg_rating, 1)
    write_books(books)

    submission_status = 'success'
    minimal_book = {'book_id': book_id, 'title': books[book_id]['title'], 'author': books[book_id]['author']}
    return render_template('write_review.html', submission_status=submission_status, book=minimal_book)


@app.route('/review/edit/<int:review_id>', methods=['GET'])
def edit_review(review_id):
    reviews = read_reviews()
    if review_id not in reviews:
        flash('Review not found.')
        return redirect(url_for('my_reviews'))
    review = reviews[review_id]
    if review['username'] != CURRENT_USER:
        flash('Unauthorized access to review.')
        return redirect(url_for('my_reviews'))

    books = read_books()
    book_id = review['book_id']
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('my_reviews'))

    minimal_book = {'book_id': book_id, 'title': books[book_id]['title'], 'author': books[book_id]['author']}
    return render_template('write_review.html', review=review, book=minimal_book)


@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    if review_id not in reviews:
        deletion_status = 'failure'
        flash('Review not found.')
        return render_template('my_reviews.html', deletion_status=deletion_status)
    review = reviews[review_id]
    if review['username'] != CURRENT_USER:
        deletion_status = 'failure'
        flash('Unauthorized access to review.')
        return render_template('my_reviews.html', deletion_status=deletion_status)

    book_id = review['book_id']
    del reviews[review_id]
    write_reviews(reviews)

    # update avg_rating of book
    books = read_books()
    total_rating = 0
    count = 0
    for r in reviews.values():
        if r['book_id'] == book_id:
            total_rating += r['rating']
            count += 1
    avg_rating = (total_rating / count) if count > 0 else 0.0
    if book_id in books:
        books[book_id]['avg_rating'] = round(avg_rating, 1)
        write_books(books)

    deletion_status = 'success'
    return render_template('my_reviews.html', deletion_status=deletion_status)


@app.route('/profile', methods=['GET'])
def user_profile():
    users = read_users()
    username = CURRENT_USER
    if username not in users:
        flash('User profile not found.')
        email = ''
        phone = ''
        address = ''
    else:
        profile = users[username]
        email = profile['email']
        phone = profile['phone']
        address = profile['address']

    borrowings = read_borrowings()
    books = read_books()
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username and b['status'] == 'Returned':
            book_title = books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown'
            borrow_history.append({
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', username=username, email=email, phone=phone, address=address, borrow_history=borrow_history)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    users = read_users()
    username = CURRENT_USER
    if username not in users:
        update_status = 'failure'
        flash('User profile not found.')
        email = ''
        phone = ''
        address = ''
        return render_template('profile.html', update_status=update_status, username=username, email=email, phone=phone, address=address)

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    users[username]['email'] = email
    users[username]['phone'] = phone
    users[username]['address'] = address

    try:
        write_users(users)
        update_status = 'success'
    except Exception:
        update_status = 'failure'

    return render_template('profile.html', update_status=update_status, username=username, email=email, phone=phone, address=address)


@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation(fine_id):
    fines = read_fines()
    if fine_id not in fines:
        flash('Fine record not found.')
        return redirect(url_for('user_profile'))
    fine = fines[fine_id]

    fine_data = {'fine_id': fine['fine_id'], 'amount': fine['amount']}
    return render_template('payment_confirmation.html', fine=fine_data)


@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    fines = read_fines()
    if fine_id not in fines:
        payment_status = 'failure'
        flash('Fine record not found.')
        return render_template('payment_confirmation.html', payment_status=payment_status, fine={'fine_id': fine_id, 'amount': 0.0})

    fine = fines[fine_id]
    if fine['status'] == 'Paid':
        payment_status = 'failure'
        flash('Fine already paid.')
        return render_template('payment_confirmation.html', payment_status=payment_status, fine={'fine_id': fine_id, 'amount': fine['amount']})

    fine['status'] = 'Paid'
    try:
        write_fines(fines)
        payment_status = 'success'
    except Exception:
        payment_status = 'failure'

    return render_template('payment_confirmation.html', payment_status=payment_status, fine={'fine_id': fine_id, 'amount': fine['amount']})


if __name__ == '__main__':
    app.run(debug=True)
