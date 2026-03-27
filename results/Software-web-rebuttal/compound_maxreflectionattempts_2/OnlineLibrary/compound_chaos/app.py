from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a strong secret key in production

DATA_DIR = 'data'

# ----- Utilities for file operations and parsing -----

def read_text_file(filename):
    with open(f"{DATA_DIR}/{filename}", 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_text_file(filename, content):
    with open(f"{DATA_DIR}/{filename}", 'w', encoding='utf-8') as f:
        f.write(content)

# Parse users.txt

def parse_users():
    users = {}
    for line in read_text_file('users.txt'):
        parts = line.split('|')
        if len(parts) == 4:
            username, email, phone, address = parts
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users

# Parse books.txt

def parse_books():
    books = {}
    for line in read_text_file('books.txt'):
        parts = line.split('|')
        if len(parts) == 10:
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
    return books

# Parse borrowings.txt

def parse_borrowings():
    borrowings = []
    for line in read_text_file('borrowings.txt'):
        parts = line.split('|')
        if len(parts) == 8:
            borrowings.append({
                'borrow_id': int(parts[0]),
                'username': parts[1],
                'book_id': int(parts[2]),
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5] if parts[5] else None,
                'status': parts[6],
                'fine_amount': float(parts[7])
            })
    return borrowings

# Parse reservations.txt

def parse_reservations():
    reservations = []
    for line in read_text_file('reservations.txt'):
        parts = line.split('|')
        if len(parts) == 5:
            reservations.append({
                'reservation_id': int(parts[0]),
                'username': parts[1],
                'book_id': int(parts[2]),
                'reservation_date': parts[3],
                'status': parts[4]
            })
    return reservations

# Parse reviews.txt

def parse_reviews():
    reviews = []
    for line in read_text_file('reviews.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            reviews.append({
                'review_id': int(parts[0]),
                'username': parts[1],
                'book_id': int(parts[2]),
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            })
    return reviews

# Parse fines.txt

def parse_fines():
    fines = []
    for line in read_text_file('fines.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            fines.append({
                'fine_id': int(parts[0]),
                'username': parts[1],
                'borrow_id': int(parts[2]),
                'amount': float(parts[3]),
                'status': parts[4],
                'date_issued': parts[5]
            })
    return fines

# Update borrowings file

def write_borrowings(borrowings):
    lines = []
    for b in borrowings:
        line = '|'.join([
            str(b['borrow_id']),
            b['username'],
            str(b['book_id']),
            b['borrow_date'],
            b['due_date'],
            b['return_date'] if b['return_date'] else '',
            b['status'],
            f"{b['fine_amount']:.2f}"
        ])
        lines.append(line)
    write_text_file('borrowings.txt', '\n'.join(lines))

# Update books file

def write_books(books):
    lines = []
    for book in books.values():
        line = '|'.join([
            str(book['book_id']),
            book['title'],
            book['author'],
            book['isbn'],
            book['genre'],
            book['publisher'],
            str(book['year']),
            book['description'],
            book['status'],
            f"{book['avg_rating']:.1f}"
        ])
        lines.append(line)
    write_text_file('books.txt', '\n'.join(lines))

# Update reservations file

def write_reservations(reservations):
    lines = []
    for r in reservations:
        line = '|'.join([
            str(r['reservation_id']),
            r['username'],
            str(r['book_id']),
            r['reservation_date'],
            r['status']
        ])
        lines.append(line)
    write_text_file('reservations.txt', '\n'.join(lines))

# Update reviews file

def write_reviews(reviews):
    lines = []
    for r in reviews:
        line = '|'.join([
            str(r['review_id']),
            r['username'],
            str(r['book_id']),
            str(r['rating']),
            r['review_text'],
            r['review_date']
        ])
        lines.append(line)
    write_text_file('reviews.txt', '\n'.join(lines))

# Update fines file

def write_fines(fines):
    lines = []
    for f in fines:
        line = '|'.join([
            str(f['fine_id']),
            f['username'],
            str(f['borrow_id']),
            f"{f['amount']:.2f}",
            f['status'],
            f['date_issued']
        ])
        lines.append(line)
    write_text_file('fines.txt', '\n'.join(lines))

# Helper to check if username can borrow

def user_can_borrow(username):
    borrowings = parse_borrowings()
    fines = parse_fines()
    reservations = parse_reservations()

    # No overdue borrowings
    for b in borrowings:
        if b['username'] == username and b['status'] == 'Overdue':
            return False

    # No unpaid fines
    for fine in fines:
        if fine['username'] == username and fine['status'] == 'Unpaid':
            return False

    # Limit active borrowings
    active_borrows = [b for b in borrowings if b['username'] == username and b['status'] in ('Active','Overdue')]
    if len(active_borrows) >= 3:
        return False

    # Limit active reservations
    active_reservs = [r for r in reservations if r['username'] == username and r['status'] == 'Active']
    if len(active_reservs) >= 2:
        return False

    return True

# Helper to check if user can review a book
# User can review if user borrowed the book at least once and no active borrowing on the book

def user_can_review(username, book_id):
    borrowings = parse_borrowings()

    borrowed = False
    active_borrow_on_book = False
    for b in borrowings:
        if b['username'] == username and b['book_id'] == book_id:
            borrowed = True
            if b['status'] in ('Active', 'Overdue'):
                active_borrow_on_book = True
    return borrowed and not active_borrow_on_book

# Helper to generate new IDs

def get_next_id(items, id_key):
    if not items:
        return 1
    return max(item[id_key] for item in items) + 1

# --- ROUTES ---

# Route 1: Root redirect to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Route 2: Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']
    books = parse_books()

    # Provide featured_books: all with only book_id,title,author,status
    featured_books = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'status': b['status']
    } for b in books.values()]

    return render_template('dashboard.html', username=username, featured_books=featured_books)

# Route 3: Book Catalog
@app.route('/catalog')
def catalog():
    search_query = request.args.get('search_query', '').strip()
    books = parse_books()

    filtered_books = []
    if search_query:
        lower_query = search_query.lower()
        for b in books.values():
            if (lower_query in b['title'].lower() or 
                lower_query in b['author'].lower() or
                lower_query in b['genre'].lower()):
                filtered_books.append({
                    'book_id': b['book_id'],
                    'title': b['title'],
                    'author': b['author'],
                    'status': b['status']
                })
    else:
        filtered_books = [{
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        } for b in books.values()]

    return render_template('catalog.html', books=filtered_books, search_query=search_query)

# Route 4: Book Details
@app.route('/book/<int:book_id>')
def book_details(book_id):
    if 'username' not in session:
        flash('Please login to view book details.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    books = parse_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))
    book = books[book_id]

    # Get reviews for this book
    reviews_all = parse_reviews()
    book_reviews = [r for r in reviews_all if r['book_id'] == book_id]

    can_borrow = user_can_borrow(username)
    can_review = user_can_review(username, book_id)

    return render_template('book_details.html', book=book, reviews=book_reviews, 
                           user_can_borrow=can_borrow, user_can_review=can_review, username=username)

# Route 5: Borrow Confirmation (GET)
@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    if 'username' not in session:
        flash('Please login to borrow a book.', 'error')
        return redirect(url_for('root_redirect'))

    username = session['username']
    books = parse_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))

    book = books[book_id]
    if book['status'] != 'Available':
        flash('Book is not available to borrow.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # Calculate due_date: 14 days from today
    due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')

    return render_template('borrow_confirmation.html', book=book, due_date=due_date)

# Route 6: Confirm Borrow POST
@app.route('/borrow/confirm', methods=['POST'])
def confirm_borrow():
    if 'username' not in session:
        flash('Please login to confirm borrow.', 'error')
        return redirect(url_for('root_redirect'))

    username = session['username']
    book_id = request.form.get('book_id')
    if not book_id:
        flash('Invalid book.', 'error')
        return redirect(url_for('catalog'))

    try:
        book_id = int(book_id)
    except ValueError:
        flash('Invalid book ID.', 'error')
        return redirect(url_for('catalog'))

    books = parse_books()
    if book_id not in books:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))
    book = books[book_id]

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    if not user_can_borrow(username):
        flash('You cannot borrow more books at the moment.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # Create new borrowing record
    borrowings = parse_borrowings()
    new_id = get_next_id(borrowings, 'borrow_id')
    borrow_date = datetime.today().strftime('%Y-%m-%d')
    due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
    new_borrow = {
        'borrow_id': new_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings.append(new_borrow)
    write_borrowings(borrowings)

    # Update book status
    book['status'] = 'Borrowed'
    write_books(books)

    return render_template('borrow_success.html', book=book, due_date=due_date)

# Route 7: Cancel Borrow
@app.route('/borrow/cancel')
def cancel_borrow():
    return redirect(url_for('catalog'))

# Route 8: My Borrowings
@app.route('/myborrows')
def my_borrowings():
    if 'username' not in session:
        flash('Please login to view your borrowings.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']
    filter_status = request.args.get('filter_status', 'All')
    borrowings = parse_borrowings()
    books = parse_books()

    filtered = []
    for b in borrowings:
        if b['username'] == username:
            if filter_status == 'All' or b['status'] == filter_status:
                book = books.get(b['book_id'], {})
                filtered.append({
                    'borrow_id': b['borrow_id'],
                    'book_title': book.get('title', 'Unknown'),
                    'borrow_date': b['borrow_date'],
                    'due_date': b['due_date'],
                    'status': b['status'],
                    'fine_amount': b['fine_amount']
                })

    return render_template('my_borrows.html', borrowings=filtered, filter_status=filter_status)

# Route 9: Return Book POST
@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    if 'username' not in session:
        flash('Please login to return a book.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    borrowings = parse_borrowings()
    books = parse_books()
    fines = parse_fines()

    borrowing = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == username), None)
    if not borrowing:
        flash('Borrowing not found.', 'error')
        return redirect(url_for('my_borrowings'))

    if borrowing['status'] != 'Active' and borrowing['status'] != 'Overdue':
        flash('Cannot return this book.', 'error')
        return redirect(url_for('my_borrowings'))

    today = datetime.today().strftime('%Y-%m-%d')
    borrowing['return_date'] = today
    borrowing['status'] = 'Returned'

    # Update book status to Available
    book = books.get(borrowing['book_id'])
    if book:
        book['status'] = 'Available'

    # Remove any unpaid fines associated with this borrow_id
    # But spec says fines exist separately - keep fines data consistent
    # Calculate if overdue fine applies
    due_dt = datetime.strptime(borrowing['due_date'], '%Y-%m-%d')
    return_dt = datetime.strptime(today, '%Y-%m-%d')
    overdue_days = (return_dt - due_dt).days
    fine_amount = 0.0
    if overdue_days > 0:
        fine_amount = overdue_days * 1.0  # Assume $1 fine per day overdue
        borrowing['fine_amount'] = fine_amount
        # Add fine record
        new_fines = fines[:]
        fine_id = get_next_id(fines, 'fine_id')
        fine_record = {
            'fine_id': fine_id,
            'username': username,
            'borrow_id': borrow_id,
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': today
        }
        new_fines.append(fine_record)
        write_fines(new_fines)

    write_borrowings(borrowings)
    write_books(books)

    book_title = book['title'] if book else 'Unknown'
    borrowing['book_title'] = book_title

    return render_template('return_confirmation.html', borrowing=borrowing, fine_amount=fine_amount)

# Route 10: My Reservations
@app.route('/reservations')
def my_reservations():
    if 'username' not in session:
        flash('Please login to view your reservations.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']
    reservations = parse_reservations()
    books = parse_books()

    user_reservations = []
    for r in reservations:
        if r['username'] == username and r['status'] == 'Active':
            book = books.get(r['book_id'], {})
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_title': book.get('title', 'Unknown'),
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })

    return render_template('reservations.html', reservations=user_reservations)

# Route 11: Cancel Reservation POST
@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    if 'username' not in session:
        flash('Please login to cancel a reservation.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    reservations = parse_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] == 'Active':
            r['status'] = 'Cancelled'
            found = True
            break
    if found:
        write_reservations(reservations)
        flash('Reservation cancelled.', 'info')
    else:
        flash('Reservation not found or already cancelled.', 'error')
    return redirect(url_for('my_reservations'))

# Route 12: My Reviews
@app.route('/myreviews')
def my_reviews():
    if 'username' not in session:
        flash('Please login to view your reviews.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    reviews = parse_reviews()
    books = parse_books()

    user_reviews = []
    for r in reviews:
        if r['username'] == username:
            book = books.get(r['book_id'], {})
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': book.get('title', 'Unknown'),
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', reviews=user_reviews)

# Route 13: Delete Review POST
@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'username' not in session:
        flash('Please login to delete reviews.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    reviews = parse_reviews()
    found = False
    new_reviews = []
    for r in reviews:
        if r['review_id'] == review_id and r['username'] == username:
            found = True
        else:
            new_reviews.append(r)

    if found:
        write_reviews(new_reviews)
        flash('Review deleted.', 'info')
    else:
        flash('Review not found or not yours.', 'error')
    return redirect(url_for('my_reviews'))

# Route 14: Edit Review GET
@app.route('/review/edit/<int:review_id>')
def edit_review(review_id):
    if 'username' not in session:
        flash('Please login to edit reviews.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    reviews = parse_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
    if not review and review_id != 0:
        flash('Review not found or not yours.', 'error')
        return redirect(url_for('my_reviews'))

    book = None
    if review_id == 0:
        book_id = request.args.get('book_id', type=int)
        books = parse_books()
        book = books.get(book_id)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('catalog'))
    else:
        books = parse_books()
        if review:
            book = books.get(review['book_id'])

    if not book:
        flash('Book for review not found.', 'error')
        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', review=review, book=book)

# Route 15: Submit Review POST
@app.route('/review/submit', methods=['POST'])
def submit_review():
    if 'username' not in session:
        flash('Please login to submit reviews.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    review_id = request.form.get('review_id')  # for edit, may be empty if new
    book_id = request.form.get('book_id')
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not book_id or not rating or not review_text:
        flash('Missing review data.', 'error')
        return redirect(url_for('my_reviews'))

    try:
        book_id = int(book_id)
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        flash('Invalid rating or book.', 'error')
        return redirect(url_for('my_reviews'))

    reviews = parse_reviews()

    # Editing existing
    if review_id:
        try:
            review_id = int(review_id)
        except ValueError:
            flash('Invalid review ID.', 'error')
            return redirect(url_for('my_reviews'))
        updated = False
        for r in reviews:
            if r['review_id'] == review_id and r['username'] == username:
                r['rating'] = rating
                r['review_text'] = review_text
                r['review_date'] = datetime.today().strftime('%Y-%m-%d')
                updated = True
                break
        if not updated:
            flash('Review not found or not yours.', 'error')
            return redirect(url_for('my_reviews'))
    else:
        new_id = get_next_id(reviews, 'review_id')
        review_date = datetime.today().strftime('%Y-%m-%d')
        new_rev = {
            'review_id': new_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews.append(new_rev)

    write_reviews(reviews)

    return redirect(url_for('book_details', book_id=book_id))

# Route 16: User Profile GET
@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('Please login to view profile.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    users = parse_users()
    user = users.get(username)

    borrowings = parse_borrowings()
    books = parse_books()

    borrow_history = []
    for b in borrowings:
        if b['username'] == username and b['status'] == 'Returned':
            book = books.get(b['book_id'], {})
            borrow_history.append({
                'book_title': book.get('title', 'Unknown'),
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    if not user:
        flash('User profile not found.', 'error')
        return redirect(url_for('root_redirect'))

    return render_template('profile.html', username=username, email=user['email'], phone=user['phone'],
                           address=user['address'], borrow_history=borrow_history)

# Route 17: Update Profile POST
@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'username' not in session:
        flash('Please login to update profile.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not email or not phone or not address:
        flash('All profile fields are required.', 'error')
        return redirect(url_for('profile'))

    users = parse_users()
    if username not in users:
        flash('User not found.', 'error')
        return redirect(url_for('profile'))

    users[username]['email'] = email
    users[username]['phone'] = phone
    users[username]['address'] = address

    # Write back all users
    lines = []
    for u in users.values():
        lines.append('|'.join([u['username'], u['email'], u['phone'], u['address']]))
    write_text_file('users.txt', '\n'.join(lines))

    flash('Profile updated successfully.', 'info')
    return redirect(url_for('profile'))

# Route 18: Payment Confirmation
@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    if 'username' not in session:
        flash('Please login to access payments.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    fines = parse_fines()
    fine = next((f for f in fines if f['fine_id'] == fine_id and f['username'] == username), None)
    if not fine:
        flash('Fine not found.', 'error')
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine)

# Route 19: Confirm Payment POST
@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    if 'username' not in session:
        flash('Please login to confirm payment.', 'error')
        return redirect(url_for('root_redirect'))
    username = session['username']

    fines = parse_fines()
    found = False
    for fine in fines:
        if fine['fine_id'] == fine_id and fine['username'] == username:
            fine['status'] = 'Paid'
            found = True
            break
    if found:
        write_fines(fines)
        flash('Payment confirmed.', 'info')
    else:
        flash('Fine not found or unauthorized.', 'error')

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)
