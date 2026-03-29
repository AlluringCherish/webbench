from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date, datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'OnlineLibrarySecretKey'

DATA_DIR = 'data'

def read_text_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip()]

def write_text_file(filename, content):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_users():
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

def save_users(users):
    lines = []
    for user in users.values():
        lines.append(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}")
    write_text_file('users.txt', '\n'.join(lines))

def load_books():
    books = []
    for line in read_text_file('books.txt'):
        parts = line.split('|')
        if len(parts) == 10:
            book_id, title, author, isbn, genre, publisher, year, description, status, avg_rating = parts
            try:
                book_id_int = int(book_id)
                avg_rating_float = float(avg_rating) if avg_rating else None
            except:
                continue
            books.append({
                'book_id': book_id_int,
                'title': title,
                'author': author,
                'isbn': isbn,
                'genre': genre,
                'publisher': publisher,
                'year': year,
                'description': description,
                'status': status,
                'avg_rating': avg_rating_float
            })
    return books

def save_books(books):
    lines = []
    for b in books:
        avg_rating = f"{b['avg_rating']:.1f}" if b['avg_rating'] is not None else ''
        line = f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{avg_rating}"
        lines.append(line)
    write_text_file('books.txt', '\n'.join(lines))

def load_borrowings():
    borrowings = []
    for line in read_text_file('borrowings.txt'):
        parts = line.split('|')
        if len(parts) == 8:
            borrow_id, username, book_id, borrow_date, due_date, return_date, status, fine_amount = parts
            borrowings.append({
                'borrow_id': int(borrow_id),
                'username': username,
                'book_id': int(book_id),
                'borrow_date': borrow_date,
                'due_date': due_date,
                'return_date': return_date if return_date else None,
                'status': status,
                'fine_amount': float(fine_amount)
            })
    return borrowings

def save_borrowings(borrowings):
    lines = []
    for b in borrowings:
        return_date = b['return_date'] if b['return_date'] else ''
        line = f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date}|{b['status']}|{b['fine_amount']:.2f}"
        lines.append(line)
    write_text_file('borrowings.txt', '\n'.join(lines))

def load_reservations():
    reservations = []
    for line in read_text_file('reservations.txt'):
        parts = line.split('|')
        if len(parts) == 5:
            reservation_id, username, book_id, reservation_date, status = parts
            reservations.append({
                'reservation_id': int(reservation_id),
                'username': username,
                'book_id': int(book_id),
                'reservation_date': reservation_date,
                'status': status
            })
    return reservations

def save_reservations(reservations):
    lines = []
    for r in reservations:
        line = f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}"
        lines.append(line)
    write_text_file('reservations.txt', '\n'.join(lines))

def load_reviews():
    reviews = []
    for line in read_text_file('reviews.txt'):
        parts = line.split('|')
        if len(parts) >= 6:
            review_id, username, book_id, rating, review_text, review_date = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
            reviews.append({
                'review_id': int(review_id),
                'username': username,
                'book_id': int(book_id),
                'rating': int(rating),
                'review_text': review_text,
                'review_date': review_date
            })
    return reviews

def save_reviews(reviews):
    lines = []
    for r in reviews:
        line = f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}"
        lines.append(line)
    write_text_file('reviews.txt', '\n'.join(lines))

def load_fines():
    fines = []
    for line in read_text_file('fines.txt'):
        parts = line.split('|')
        if len(parts) == 6:
            fine_id, username, borrow_id, amount, status, date_issued = parts
            fines.append({
                'fine_id': int(fine_id),
                'username': username,
                'borrow_id': int(borrow_id),
                'amount': float(amount),
                'status': status,
                'date_issued': date_issued
            })
    return fines

def save_fines(fines):
    lines = []
    for f in fines:
        line = f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']:.2f}|{f['status']}|{f['date_issued']}"
        lines.append(line)
    write_text_file('fines.txt', '\n'.join(lines))

def user_logged_in():
    return 'username' in session

def get_current_user():
    if user_logged_in():
        return session['username']
    return None

def get_next_id(records, id_key):
    if not records:
        return 1
    return max(r[id_key] for r in records) + 1

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if not user_logged_in():
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    username = get_current_user()
    return render_template('dashboard.html', username=username)

@app.route('/catalog')
def book_catalog():
    books = load_books()
    # Only include required keys
    books_simple = [{'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']} for b in books]
    return render_template('catalog.html', books=books_simple)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))
    reviews = load_reviews()
    book_reviews = [
        {k:r[k] for k in ('review_id','username','rating','review_text','review_date')}
        for r in reviews if r['book_id'] == book_id
    ]
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/borrow/<int:book_id>', methods=['GET','POST'])
def borrow_confirm(book_id):
    if not user_logged_in():
        flash('Please log in to borrow books.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    if request.method == 'GET':
        due_date = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        return render_template('borrow_confirm.html', book=book, due_date=due_date)

    # POST handling: borrow confirmation
    borrowings = load_borrowings()
    # Check if user already borrowed this book and the status is Active or Overdue
    for b in borrowings:
        if b['username'] == username and b['book_id'] == book_id and b['status'] in ['Active','Overdue']:
            flash('You currently have this book borrowed. Return it before borrowing again.', 'error')
            return redirect(url_for('my_borrowings'))

    # Check availability
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_catalog'))

    new_borrow_id = get_next_id(borrowings, 'borrow_id')
    borrow_date_str = date.today().strftime('%Y-%m-%d')
    due_date_str = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
    new_borrow = {
        'borrow_id': new_borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date_str,
        'due_date': due_date_str,
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

    flash('Book borrowed successfully.', 'success')
    return redirect(url_for('my_borrowings'))

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    if not user_logged_in():
        flash('Please log in to return books.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    borrowing = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == username), None)
    if not borrowing:
        flash('Borrowing record not found.', 'error')
        return redirect(url_for('my_borrowings'))

    if borrowing['status'] not in ['Active','Overdue']:
        flash('Cannot return this book.', 'error')
        return redirect(url_for('my_borrowings'))

    today_str = date.today().strftime('%Y-%m-%d')
    borrowing['return_date'] = today_str
    # Update status
    if borrowing['due_date'] < today_str:
        borrowing['status'] = 'Returned'
        # Calculate fine
        d_due = datetime.strptime(borrowing['due_date'], '%Y-%m-%d').date()
        d_return = datetime.strptime(today_str, '%Y-%m-%d').date()
        days_overdue = (d_return - d_due).days
        fine_amount = max(days_overdue * 1.0, 0.0) # $1 per day overdue
        borrowing['fine_amount'] = fine_amount
        if fine_amount > 0:
            # Add to fines
            fine_records = load_fines()
            new_fine_id = get_next_id(fine_records, 'fine_id')
            fine_record = {
                'fine_id': new_fine_id,
                'username': username,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': today_str
            }
            fine_records.append(fine_record)
            save_fines(fine_records)
    else:
        borrowing['status'] = 'Returned'
        borrowing['fine_amount'] = 0.0

    # Update book status to Available
    for b in books:
        if b['book_id'] == borrowing['book_id']:
            b['status'] = 'Available'
            break

    save_borrowings(borrowings)
    save_books(books)
    flash('Book returned successfully.', 'success')
    return redirect(url_for('my_borrowings'))

@app.route('/my-borrows')
def my_borrowings():
    if not user_logged_in():
        flash('Please log in to view your borrowings.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    borrowings = load_borrowings()
    books = load_books()

    # Filter user borrowings
    user_borrows = [b for b in borrowings if b['username'] == username]

    # Handle filter param
    filter_status = request.args.get('filter_status', 'All')
    if filter_status in ['Active', 'Returned', 'Overdue']:
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]

    # Prepare list with book title
    borrows_display = []
    book_dict = {b['book_id']: b for b in books}
    for b in user_borrows:
        borrows_display.append({
            'borrow_id': b['borrow_id'],
            'title': book_dict[b['book_id']]['title'] if b['book_id'] in book_dict else '',
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    return render_template('my_borrows.html', borrowings=borrows_display, filter_status=filter_status)

@app.route('/my-reservations')
def my_reservations():
    if not user_logged_in():
        flash('Please log in to view your reservations.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    reservations = load_reservations()
    books = load_books()

    user_reservations = [r for r in reservations if r['username'] == username]

    book_dict = {b['book_id']: b for b in books}
    reservations_display = []
    for r in user_reservations:
        reservations_display.append({
            'reservation_id': r['reservation_id'],
            'title': book_dict[r['book_id']]['title'] if r['book_id'] in book_dict else '',
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })

    return render_template('my_reservations.html', reservations=reservations_display)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    if not user_logged_in():
        flash('Please log in to cancel reservations.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    reservations = load_reservations()

    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id and r['username'] == username), None)
    if reservation and reservation['status'] == 'Active':
        reservation['status'] = 'Cancelled'
        save_reservations(reservations)
        flash('Reservation cancelled.', 'success')
    else:
        flash('Reservation cannot be cancelled.', 'error')
    return redirect(url_for('my_reservations'))

@app.route('/my-reviews')
def my_reviews():
    if not user_logged_in():
        flash('Please log in to view your reviews.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    reviews = load_reviews()
    books = load_books()

    user_reviews = [r for r in reviews if r['username'] == username]
    book_dict = {b['book_id']: b for b in books}
    reviews_display = []
    for r in user_reviews:
        reviews_display.append({
            'review_id': r['review_id'],
            'book_title': book_dict[r['book_id']]['title'] if r['book_id'] in book_dict else '',
            'rating': r['rating'],
            'review_text': r['review_text'],
            'book_id': r['book_id']
        })

    return render_template('my_reviews.html', reviews=reviews_display)

@app.route('/write-review/<int:book_id>', methods=['GET','POST'])
def write_review(book_id):
    if not user_logged_in():
        flash('Please log in to write a review.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()

    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    reviews = load_reviews()
    existing_review = next((r for r in reviews if r['username'] == username and r['book_id'] == book_id), None)

    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()
        if rating is None or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash('Rating must be an integer between 1 and 5.', 'error')
            return render_template('write_review.html', book=book, existing_review=existing_review)
        rating = int(rating)

        if not review_text:
            flash('Review text cannot be empty.', 'error')
            return render_template('write_review.html', book=book, existing_review=existing_review)

        review_date = date.today().strftime('%Y-%m-%d')

        if existing_review:
            for r in reviews:
                if r['review_id'] == existing_review['review_id']:
                    r['rating'] = rating
                    r['review_text'] = review_text
                    r['review_date'] = review_date
                    break
            flash('Review updated successfully.', 'success')
        else:
            new_review_id = get_next_id(reviews, 'review_id')
            new_review = {
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews.append(new_review)
            flash('Review submitted successfully.', 'success')
        save_reviews(reviews)
        return redirect(url_for('book_details', book_id=book_id))

    # GET
    existing_review_simple = None
    if existing_review:
        existing_review_simple = {
            'review_id': existing_review['review_id'],
            'rating': existing_review['rating'],
            'review_text': existing_review['review_text']
        }
    return render_template('write_review.html', book=book, existing_review=existing_review_simple)

@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if not user_logged_in():
        flash('Please log in to delete reviews.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    reviews = load_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == username), None)
    if review:
        reviews.remove(review)
        save_reviews(reviews)
        flash('Review deleted.', 'success')
    else:
        flash('Review not found.', 'error')
    return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET','POST'])
def user_profile():
    if not user_logged_in():
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            user['email'] = email
            users[username] = user
            save_users(users)
            flash('Profile updated.', 'success')
        else:
            flash('Email cannot be empty.', 'error')

    borrowings = load_borrowings()
    books = load_books()
    book_dict = {b['book_id']: b for b in books}

    # List borrow history (Returned) for user
    borrow_history = []
    for b in borrowings:
        if b['username'] == username and b['status'] == 'Returned':
            borrow_history.append({
                'title': book_dict[b['book_id']]['title'] if b['book_id'] in book_dict else '',
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', username=username, email=user['email'], borrow_history=borrow_history)

@app.route('/payment/<int:fine_id>', methods=['GET','POST'])
def payment_confirmation(fine_id):
    if not user_logged_in():
        flash('Please log in to make payments.', 'error')
        return redirect(url_for('dashboard'))
    username = get_current_user()
    fines = load_fines()
    fine = next((f for f in fines if f['fine_id'] == fine_id and f['username'] == username), None)
    if not fine:
        flash('Fine not found.', 'error')
        return redirect(url_for('user_profile'))

    if request.method == 'POST':
        # Mark fine as Paid
        fine['status'] = 'Paid'
        save_fines(fines)
        flash('Payment confirmed.', 'success')
        return redirect(url_for('user_profile'))

    return render_template('payment_confirm.html', fine_amount=fine['amount'], fine_id=fine_id)

# For session management and login/logout (minimal implementation)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            users = load_users()
            if username in users:
                session['username'] = username
                flash(f'Welcome, {username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('User not found.', 'error')
        else:
            flash('Please enter a username.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
