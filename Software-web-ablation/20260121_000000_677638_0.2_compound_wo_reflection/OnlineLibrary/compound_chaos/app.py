from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility functions for data file handling and parsing

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                users[parts[0]] = {
                    'username': parts[0],
                    'email': parts[1],
                    'phone': parts[2],
                    'address': parts[3]
                }
    return users

def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users.values():
            f.write(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}\n")

def read_books():
    path = os.path.join(DATA_DIR, 'books.txt')
    books = {}
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                books[int(parts[0])] = {
                    'book_id': int(parts[0]),
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
    return books

def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for book in books.values():
            f.write(f"{book['book_id']}|{book['title']}|{book['author']}|{book['isbn']}|{book['genre']}|{book['publisher']}|{book['year']}|{book['description']}|{book['status']}|{book['avg_rating']}\n")

def read_borrowings():
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    borrowings = {}
    if not os.path.exists(path):
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                borrowings[int(parts[0])] = {
                    'borrow_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5] if parts[5] else None,
                    'status': parts[6],
                    'fine_amount': float(parts[7])
                }
    return borrowings

def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            return_date_str = b['return_date'] if b['return_date'] is not None else ''
            f.write(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date_str}|{b['status']}|{b['fine_amount']}\n")

def read_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = {}
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                reservations[int(parts[0])] = {
                    'reservation_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
    return reservations

def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            f.write(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n")

def read_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = {}
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                reviews[int(parts[0])] = {
                    'review_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
    return reviews

def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            f.write(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")

def read_fines():
    path = os.path.join(DATA_DIR, 'fines.txt')
    fines = {}
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                fines[int(parts[0])] = {
                    'fine_id': int(parts[0]),
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': float(parts[3]),
                    'status': parts[4],
                    'date_issued': parts[5]
                }
    return fines

def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            f.write(f"{fine['fine_id']}|{fine['username']}|{fine['borrow_id']}|{fine['amount']}|{fine['status']}|{fine['date_issued']}\n")

# Helper for generating new IDs

def get_next_id(items):
    if items:
        return max(items.keys()) + 1
    else:
        return 1

# Helper to get current username (assumed session or request context, simplified here as 'john_reader')
def get_current_username():
    # For this spec, assume a static logged-in username for demonstration
    # In real app this would use session/cookies
    return 'john_reader'


# ROUTE IMPLEMENTATIONS

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    return render_template('dashboard.html', username=username)

@app.route('/catalog')
def book_catalog():
    books_raw = read_books()
    books = []
    for book in books_raw.values():
        books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'status': book['status']
        })
    return render_template('catalog.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    username = get_current_username()
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews_all = read_reviews()
    reviews = []
    for review in reviews_all.values():
        if review['book_id'] == book_id:
            reviews.append({
                'review_id': review['review_id'],
                'username': review['username'],
                'rating': review['rating'],
                'review_text': review['review_text'],
                'review_date': review['review_date']
            })

    return render_template('book_details.html', book=book, reviews=reviews, username=username)

@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    username = get_current_username()
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    return render_template('borrow_confirmation.html', book=book, due_date=due_date, username=username)

@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def confirm_borrow(book_id):
    username = get_current_username()
    books = read_books()
    borrowings = read_borrowings()

    book = books.get(book_id)
    if not book:
        message = 'Book not found.'
        return render_template('borrow_confirmation.html', message=message, book={'book_id': book_id}, username=username)

    if book['status'] != 'Available':
        message = 'Book is not available.'
        return render_template('borrow_confirmation.html', message=message, book=book, username=username)

    # Create new borrow record
    next_borrow_id = get_next_id(borrowings)
    borrow_date = datetime.date.today().strftime('%Y-%m-%d')
    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    borrowings[next_borrow_id] = {
        'borrow_id': next_borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    # Update book status
    book['status'] = 'Borrowed'

    # Write data back
    write_borrowings(borrowings)
    write_books(books)

    message = f'Borrow confirmed. Due date is {due_date}.'
    return render_template('borrow_confirmation.html', message=message, book=book, due_date=due_date, username=username)

@app.route('/borrows')
def my_borrowings():
    username = get_current_username()
    borrowings = read_borrowings()
    books = read_books()

    # Update statuses if overdue and status still Active
    today = datetime.date.today()
    updated = False
    for b in borrowings.values():
        if b['username'] == username and b['status'] == 'Active':
            due = datetime.datetime.strptime(b['due_date'], '%Y-%m-%d').date()
            if due < today:
                b['status'] = 'Overdue'
                # calculate fine amount
                days_overdue = (today - due).days
                fine_amount = days_overdue * 1.0  # Assuming $1 per day overdue
                b['fine_amount'] = fine_amount
                updated = True
    if updated:
        write_borrowings(borrowings)

    borrows = []
    for b in borrowings.values():
        if b['username'] == username:
            book = books.get(b['book_id'])
            borrows.append({
                'borrow_id': b['borrow_id'],
                'book_title': book['title'] if book else 'Unknown',
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status']
            })

    return render_template('my_borrows.html', borrows=borrows, username=username)

@app.route('/borrow/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_current_username()
    borrowings = read_borrowings()
    books = read_books()

    borrow = borrowings.get(borrow_id)
    if not borrow:
        message = 'Borrow record not found.'
        borrows_list = []
        return render_template('my_borrows.html', message=message, borrows=borrows_list, username=username)

    if borrow['username'] != username:
        message = 'Unauthorized action.'
        borrows_list = []
        return render_template('my_borrows.html', message=message, borrows=borrows_list, username=username)

    if borrow['status'] not in ['Active', 'Overdue']:
        message = 'This borrow is already returned.'
        borrows_list = []
        return render_template('my_borrows.html', message=message, borrows=borrows_list, username=username)

    # Mark as returned
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    borrow['return_date'] = today_str
    borrow['status'] = 'Returned'

    # Update book status to Available
    book = books.get(borrow['book_id'])
    if book:
        book['status'] = 'Available'

    # Write back updated data
    write_borrowings(borrowings)
    write_books(books)

    message = 'Book returned successfully.'

    # Return updated borrow list
    borrows = []
    for b in borrowings.values():
        if b['username'] == username:
            book = books.get(b['book_id'])
            borrows.append({
                'borrow_id': b['borrow_id'],
                'book_title': book['title'] if book else 'Unknown',
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status']
            })

    return render_template('my_borrows.html', message=message, borrows=borrows, username=username)

@app.route('/reservations')
def my_reservations():
    username = get_current_username()
    reservations = read_reservations()
    books = read_books()

    reservations_list = []
    for r in reservations.values():
        if r['username'] == username:
            book = books.get(r['book_id'])
            reservations_list.append({
                'reservation_id': r['reservation_id'],
                'book_title': book['title'] if book else 'Unknown',
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })

    return render_template('my_reservations.html', reservations=reservations_list, username=username)

@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_current_username()
    reservations = read_reservations()

    reservation = reservations.get(reservation_id)
    if not reservation:
        message = 'Reservation not found.'
    elif reservation['username'] != username:
        message = 'Unauthorized action.'
    elif reservation['status'] != 'Active':
        message = 'Reservation already cancelled.'
    else:
        reservation['status'] = 'Cancelled'
        write_reservations(reservations)
        message = 'Reservation cancelled successfully.'

    # Show updated reservations
    reservations_list = []
    books = read_books()
    for r in reservations.values():
        if r['username'] == username:
            book = books.get(r['book_id'])
            reservations_list.append({
                'reservation_id': r['reservation_id'],
                'book_title': book['title'] if book else 'Unknown',
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })

    return render_template('my_reservations.html', message=message, reservations=reservations_list, username=username)

@app.route('/reviews')
def my_reviews():
    username = get_current_username()
    reviews = read_reviews()
    books = read_books()

    reviews_list = []
    for r in reviews.values():
        if r['username'] == username:
            book = books.get(r['book_id'])
            reviews_list.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'book_title': book['title'] if book else 'Unknown',
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', reviews=reviews_list, username=username)

# Add route to delete review
@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    username = get_current_username()
    reviews = read_reviews()
    review = reviews.get(review_id)

    if not review or review['username'] != username:
        message = 'Review not found or unauthorized.'
    else:
        del reviews[review_id]

        # After deletion, recalculate avg_rating for the book
        books = read_books()
        book_id = review['book_id']
        book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
        if book_reviews:
            avg = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            books[book_id]['avg_rating'] = round(avg, 1)
        else:
            books[book_id]['avg_rating'] = 0.0
        write_books(books)
        write_reviews(reviews)
        message = 'Review deleted successfully.'

    # Return updated review list
    updated_reviews = []
    books = read_books()
    for r in reviews.values():
        if r['username'] == username:
            book = books.get(r['book_id'])
            updated_reviews.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'book_title': book['title'] if book else 'Unknown',
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', message=message, reviews=updated_reviews, username=username)

@app.route('/review/write/<int:book_id>')
def write_review(book_id):
    username = get_current_username()
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    return render_template('write_review.html', book=book, existing_review=existing_review, username=username)

@app.route('/review/submit/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    username = get_current_username()
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')

    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError
    except (ValueError, TypeError):
        message = 'Rating must be an integer between 1 and 5.'
        books = read_books()
        book = books.get(book_id, {})
        existing_review = None
        reviews = read_reviews()
        for r in reviews.values():
            if r['username'] == username and r['book_id'] == book_id:
                existing_review = {
                    'review_id': r['review_id'],
                    'rating': r['rating'],
                    'review_text': r['review_text']
                }
                break
        return render_template('write_review.html', message=message, book=book, existing_review=existing_review, username=username)

    # Either add new or update existing review
    reviews = read_reviews()
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    found = False
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            r['rating'] = rating_int
            r['review_text'] = review_text
            r['review_date'] = current_date
            found = True
            break
    if not found:
        new_id = get_next_id(reviews)
        reviews[new_id] = {
            'review_id': new_id,
            'username': username,
            'book_id': book_id,
            'rating': rating_int,
            'review_text': review_text,
            'review_date': current_date
        }

    # Update average rating of book
    books = read_books()
    if book_id in books:
        # Recalculate avg_rating
        book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
        if book_reviews:
            avg = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            books[book_id]['avg_rating'] = round(avg, 1)
        else:
            books[book_id]['avg_rating'] = 0.0
        write_books(books)

    write_reviews(reviews)

    message = 'Review submitted successfully.'
    book = books.get(book_id, {})
    existing_review = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break
    return render_template('write_review.html', message=message, book=book, existing_review=existing_review, username=username)

@app.route('/profile')
def user_profile():
    username = get_current_username()
    users = read_users()
    user = users.get(username, {'email': '', 'phone': '', 'address': ''})

    borrowings = read_borrowings()
    books = read_books()

    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username:
            book = books.get(b['book_id'])
            borrow_history.append({
                'book_title': book['title'] if book else 'Unknown',
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', username=username, email=user['email'], borrow_history=borrow_history)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = get_current_username()
    email = request.form.get('email', '')
    users = read_users()
    if username not in users:
        flash('User not found.')
        return redirect(url_for('user_profile'))

    users[username]['email'] = email
    write_users(users)

    message = 'Profile updated successfully.'
    user_profile_data = users[username]

    borrowings = read_borrowings()
    books = read_books()

    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username:
            book = books.get(b['book_id'])
            borrow_history.append({
                'book_title': book['title'] if book else 'Unknown',
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', message=message, username=username, email=user_profile_data['email'], borrow_history=borrow_history)

@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    username = get_current_username()
    fines = read_fines()
    fine = fines.get(fine_id)

    if not fine or fine['username'] != username:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))

    return render_template('payment_confirmation.html', fine=fine, username=username)

@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    username = get_current_username()
    fines = read_fines()

    fine = fines.get(fine_id)
    if not fine or fine['username'] != username:
        message = 'Fine not found or unauthorized.'
        return render_template('payment_confirmation.html', message=message, fine=fine, username=username)

    if fine['status'] == 'Paid':
        message = 'Fine is already paid.'
    else:
        fine['status'] = 'Paid'
        write_fines(fines)
        message = 'Payment confirmed successfully.'

    return render_template('payment_confirmation.html', message=message, fine=fine, username=username)

if __name__ == '__main__':
    app.run(debug=True)
