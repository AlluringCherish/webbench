from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username,email,phone,address = line.split('|')
                users[username] = {'username': username, 'email': email, 'phone': phone, 'address': address}
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for user in users.values():
                f.write(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}\n")
    except Exception as e:
        print(f"Error saving users: {e}")


def load_books():
    books = {}
    try:
        with open(os.path.join(DATA_DIR, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                book_id = int(parts[0])
                book = {
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
                books[book_id] = book
    except FileNotFoundError:
        pass
    return books

def save_books(books):
    try:
        with open(os.path.join(DATA_DIR, 'books.txt'), 'w', encoding='utf-8') as f:
            for book in books.values():
                line = f"{book['book_id']}|{book['title']}|{book['author']}|{book['isbn']}|{book['genre']}|{book['publisher']}|{book['year']}|{book['description']}|{book['status']}|{book['avg_rating']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving books: {e}")


def load_borrowings():
    borrowings = {}
    try:
        with open(os.path.join(DATA_DIR, 'borrowings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                borrow_id = int(parts[0])
                borrow = {
                    'borrow_id': borrow_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5],
                    'status': parts[6],
                    'fine_amount': float(parts[7])
                }
                borrowings[borrow_id] = borrow
    except FileNotFoundError:
        pass
    return borrowings

def save_borrowings(borrowings):
    try:
        with open(os.path.join(DATA_DIR, 'borrowings.txt'), 'w', encoding='utf-8') as f:
            for borrow in borrowings.values():
                line = f"{borrow['borrow_id']}|{borrow['username']}|{borrow['book_id']}|{borrow['borrow_date']}|{borrow['due_date']}|{borrow['return_date']}|{borrow['status']}|{borrow['fine_amount']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving borrowings: {e}")


def load_reservations():
    reservations = {}
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                reservation_id = int(parts[0])
                reservation = {
                    'reservation_id': reservation_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
                reservations[reservation_id] = reservation
    except FileNotFoundError:
        pass
    return reservations

def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for res in reservations.values():
                line = f"{res['reservation_id']}|{res['username']}|{res['book_id']}|{res['reservation_date']}|{res['status']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving reservations: {e}")


def load_reviews():
    reviews = {}
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                review_id = int(parts[0])
                review = {
                    'review_id': review_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews[review_id] = review
    except FileNotFoundError:
        pass
    return reviews

def save_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for rev in reviews.values():
                line = f"{rev['review_id']}|{rev['username']}|{rev['book_id']}|{rev['rating']}|{rev['review_text']}|{rev['review_date']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving reviews: {e}")


def load_fines():
    fines = {}
    try:
        with open(os.path.join(DATA_DIR, 'fines.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                fine_id = int(parts[0])
                fine = {
                    'fine_id': fine_id,
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': float(parts[3]),
                    'status': parts[4],
                    'date_issued': parts[5]
                }
                fines[fine_id] = fine
    except FileNotFoundError:
        pass
    return fines

def save_fines(fines):
    try:
        with open(os.path.join(DATA_DIR, 'fines.txt'), 'w', encoding='utf-8') as f:
            for fine in fines.values():
                line = f"{fine['fine_id']}|{fine['username']}|{fine['borrow_id']}|{fine['amount']}|{fine['status']}|{fine['date_issued']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving fines: {e}")


# For simplicity, we assume a logged-in user with username 'john_reader'
# In real applications, implement authentication and session management
LOGGED_IN_USERNAME = 'john_reader'

# 1. Root route: redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# 2. Dashboard page
@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USERNAME
    welcome_message = f"Welcome back, {username}!"
    return render_template('dashboard.html', username=username, welcome_message=welcome_message)

# 3. Book Catalog page
@app.route('/catalog')
def book_catalog():
    books = load_books()
    search_query = request.args.get('q', '').strip()
    book_list = list(books.values())
    if search_query:
        sq = search_query.lower()
        book_list = [b for b in book_list if sq in b['title'].lower() or sq in b['author'].lower()]
    return render_template('catalog.html', books=book_list, search_query=search_query)

# 4. Book Details page
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('book_catalog'))
    reviews_all = load_reviews()
    reviews = [r for r in reviews_all.values() if r['book_id'] == book_id]
    username = LOGGED_IN_USERNAME
    return render_template('book_details.html', book=book, reviews=reviews, username=username)

# 5. Borrow Confirmation page (GET for form display, POST to process borrow)
@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_confirmation(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('book_catalog'))

    username = LOGGED_IN_USERNAME

    if request.method == 'GET':
        # Show confirmation page
        borrow_date_obj = datetime.today()
        due_date_obj = borrow_date_obj + timedelta(days=14)
        due_date = due_date_obj.strftime('%Y-%m-%d')
        return render_template('borrow_confirmation.html', book=book, due_date=due_date, username=username)

    elif request.method == 'POST':
        # Not allowed here; borrow confirm is in different route
        return redirect(url_for('confirm_borrow', book_id=book_id))

# 6. Borrow Book Action (POST)
@app.route('/borrow/confirm/<int:book_id>', methods=['POST'])
def confirm_borrow(book_id):
    books = load_books()
    borrowings = load_borrowings()

    book = books.get(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('book_catalog'))

    username = LOGGED_IN_USERNAME

    # Check if book is available
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # Check if user already has borrowed this book and not returned
    user_active_borrows = [b for b in borrowings.values() if b['username'] == username and b['book_id'] == book_id and b['status'] == 'Active']
    if user_active_borrows:
        flash('You already have this book borrowed.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # Generate new borrow_id
    new_borrow_id = max(borrowings.keys(), default=0) + 1

    borrow_date = datetime.today()
    due_date = borrow_date + timedelta(days=14)

    # New borrow record
    borrow_record = {
        'borrow_id': new_borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date.strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }

    borrowings[new_borrow_id] = borrow_record

    # Mark book as Borrowed
    book['status'] = 'Borrowed'

    # Save updates
    save_borrowings(borrowings)
    save_books(books)

    flash('Borrow confirmed successfully.', 'success')
    return redirect(url_for('my_borrowings'))

# 7. Cancel Borrow Action (POST)
@app.route('/borrow/cancel/<int:book_id>', methods=['POST'])
def cancel_borrow(book_id):
    return redirect(url_for('book_details', book_id=book_id))

# 8. My Borrowings page
@app.route('/my-borrows')
def my_borrowings():
    borrowings = load_borrowings()
    books = load_books()
    username = LOGGED_IN_USERNAME

    filter_status = request.args.get('filter', 'All')

    user_borrows = [b for b in borrowings.values() if b['username'] == username]

    # Update borrowing statuses for overdue
    today = datetime.today().date()
    changed = False
    for b in user_borrows:
        if b['status'] == 'Active':
            due_date_obj = datetime.strptime(b['due_date'], '%Y-%m-%d').date()
            if due_date_obj < today:
                b['status'] = 'Overdue'
                # Add fine if not already added
                if b['fine_amount'] == 0:
                    b['fine_amount'] = 5.0  # Flat fine amount
                    changed = True
    if changed:
        # Save borrowings updates
        save_borrowings(borrowings)

    if filter_status != 'All':
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]

    borrows_display = []
    for b in user_borrows:
        borrows_display.append({
            'borrow_id': b['borrow_id'],
            'book_title': books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown',
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    return render_template('my_borrows.html', borrowings=borrows_display, filter_status=filter_status)

# 9. Return Book Confirmation page
@app.route('/return/<int:borrow_id>', methods=['GET', 'POST'])
def return_book_confirmation(borrow_id):
    borrowings = load_borrowings()
    books = load_books()
    borrow = borrowings.get(borrow_id)
    if not borrow:
        flash('Borrow record not found.', 'error')
        return redirect(url_for('my_borrowings'))

    book = books.get(borrow['book_id'], None)
    if book is None:
        flash('Book record not found.', 'error')
        return redirect(url_for('my_borrows'))

    username = LOGGED_IN_USERNAME

    if request.method == 'GET':
        return render_template('return_confirmation.html', borrow=borrow, book=book, username=username)

    if request.method == 'POST':
        return redirect(url_for('confirm_return', borrow_id=borrow_id))

# 10. Confirm Return Action
@app.route('/return/confirm/<int:borrow_id>', methods=['POST'])
def confirm_return(borrow_id):
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    borrow = borrowings.get(borrow_id)
    if not borrow:
        flash('Borrow record not found.', 'error')
        return redirect(url_for('my_borrowings'))

    book = books.get(borrow['book_id'])
    if not book:
        flash('Book record not found.', 'error')
        return redirect(url_for('my_borrowings'))

    username = LOGGED_IN_USERNAME

    # Only Active or Overdue can be returned
    if borrow['status'] not in ['Active', 'Overdue']:
        flash('This borrow record cannot be returned.', 'error')
        return redirect(url_for('my_borrowings'))

    return_date = datetime.today()
    is_overdue = (borrow['status'] == 'Overdue')

    borrow['return_date'] = return_date.strftime('%Y-%m-%d')
    borrow['status'] = 'Returned'

    # Update book status
    book['status'] = 'Available'

    # If borrow was overdue and fine_amount > 0 create fine record if not exist
    if is_overdue and borrow['fine_amount'] > 0:
        # Check if fine already exists
        existing_fine = None
        for fine in fines.values():
            if fine['borrow_id'] == borrow_id:
                existing_fine = fine
                break
        if not existing_fine:
            new_fine_id = max(fines.keys(), default=0) + 1
            fine_record = {
                'fine_id': new_fine_id,
                'username': username,
                'borrow_id': borrow_id,
                'amount': borrow['fine_amount'],
                'status': 'Unpaid',
                'date_issued': return_date.strftime('%Y-%m-%d')
            }
            fines[new_fine_id] = fine_record
            save_fines(fines)

    save_borrowings(borrowings)
    save_books(books)

    flash('Book returned successfully.', 'success')
    return redirect(url_for('my_borrowings'))

# 11. Cancel Return Action
@app.route('/return/cancel/<int:borrow_id>', methods=['POST'])
def cancel_return(borrow_id):
    return redirect(url_for('my_borrowings'))

# 12. My Reservations Page
@app.route('/my-reservations')
def my_reservations():
    reservations = load_reservations()
    books = load_books()
    username = LOGGED_IN_USERNAME

    user_reservations = [r for r in reservations.values() if r['username'] == username and r['status'] == 'Active']

    res_display = []
    for r in user_reservations:
        res_display.append({
            'reservation_id': r['reservation_id'],
            'book_title': books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown',
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })

    return render_template('my_reservations.html', reservations=res_display)

# 13. Cancel Reservation Action
@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation:
        flash('Reservation not found.', 'error')
        return redirect(url_for('my_reservations'))

    if reservation['status'] != 'Active':
        flash('Reservation is not active.', 'error')
        return redirect(url_for('my_reservations'))

    reservation['status'] = 'Cancelled'
    save_reservations(reservations)

    flash('Reservation cancelled successfully.', 'success')
    return redirect(url_for('my_reservations'))

# 14. My Reviews page
@app.route('/my-reviews')
def my_reviews():
    reviews = load_reviews()
    books = load_books()
    username = LOGGED_IN_USERNAME

    user_reviews = [r for r in reviews.values() if r['username'] == username]

    reviews_display = []
    for r in user_reviews:
        reviews_display.append({
            'review_id': r['review_id'],
            'book_title': books[r['book_id']]['title'] if r['book_id'] in books else 'Unknown',
            'rating': r['rating'],
            'review_text': r['review_text']
        })

    return render_template('my_reviews.html', reviews=reviews_display)

# 15. Write Review page (GET and POST)
@app.route('/review/write/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    reviews = load_reviews()
    username = LOGGED_IN_USERNAME

    # Check for existing review by user for this book
    existing_review = None
    for review in reviews.values():
        if review['username'] == username and review['book_id'] == book_id:
            existing_review = review
            break

    if request.method == 'GET':
        return render_template('write_review.html', book=book, existing_review=existing_review)

    if request.method == 'POST':
        rating = int(request.form.get('rating', '0'))
        review_text = request.form.get('review_text', '').strip()
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5.', 'error')
            return redirect(url_for('write_review', book_id=book_id))
        if not review_text:
            flash('Review text cannot be empty.', 'error')
            return redirect(url_for('write_review', book_id=book_id))

        review_date = datetime.today().strftime('%Y-%m-%d')

        if existing_review:
            # Update existing review
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = review_date
        else:
            # Add new review
            new_review_id = max(reviews.keys(), default=0) + 1
            new_review = {
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews[new_review_id] = new_review

        # Save reviews
        save_reviews(reviews)

        # Update avg_rating in book
        book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
        if book_reviews:
            avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            book['avg_rating'] = round(avg_rating, 1)
        else:
            book['avg_rating'] = 0.0
        save_books(books)

        flash('Review submitted successfully.', 'success')
        return redirect(url_for('book_details', book_id=book_id))

# 16. Edit Review Action (GET and POST)
@app.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    books = load_books()
    book = books.get(review['book_id'])
    if not book:
        flash('Book for review not found.', 'error')
        return redirect(url_for('my_reviews'))

    username = LOGGED_IN_USERNAME
    if review['username'] != username:
        flash('You can only edit your own reviews.', 'error')
        return redirect(url_for('my_reviews'))

    if request.method == 'GET':
        return render_template('write_review.html', existing_review=review, book=book)

    if request.method == 'POST':
        rating = int(request.form.get('rating', '0'))
        review_text = request.form.get('review_text', '').strip()

        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5.', 'error')
            return redirect(url_for('edit_review', review_id=review_id))
        if not review_text:
            flash('Review text cannot be empty.', 'error')
            return redirect(url_for('edit_review', review_id=review_id))

        review['rating'] = rating
        review['review_text'] = review_text
        review['review_date'] = datetime.today().strftime('%Y-%m-%d')

        save_reviews(reviews)

        # Update avg_rating in book
        book_reviews = [r for r in reviews.values() if r['book_id'] == book['book_id']]
        if book_reviews:
            avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            book['avg_rating'] = round(avg_rating, 1)
        else:
            book['avg_rating'] = 0.0
        save_books(books)

        flash('Review edited successfully.', 'success')
        return redirect(url_for('my_reviews'))

# 17. Delete Review Action (POST)
@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review:
        flash('Review not found.', 'error')
        return redirect(url_for('my_reviews'))

    username = LOGGED_IN_USERNAME
    if review['username'] != username:
        flash('You can only delete your own reviews.', 'error')
        return redirect(url_for('my_reviews'))

    book_id = review['book_id']
    del reviews[review_id]
    save_reviews(reviews)

    # Update avg_rating in book
    books = load_books()
    book = books.get(book_id)
    if book:
        book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
        if book_reviews:
            avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            book['avg_rating'] = round(avg_rating, 1)
        else:
            book['avg_rating'] = 0.0
        save_books(books)

    flash('Review deleted successfully.', 'success')
    return redirect(url_for('my_reviews'))

# 18. User Profile Page (GET and POST)
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = load_users()
    username = LOGGED_IN_USERNAME

    if username not in users:
        flash('User profile not found.', 'error')
        return redirect(url_for('dashboard'))

    user = users[username]
    borrowings = load_borrowings()
    books = load_books()

    if request.method == 'GET':
        # Prepare borrow history
        borrow_history = []
        for b in borrowings.values():
            if b['username'] == username:
                book_title = books[b['book_id']]['title'] if b['book_id'] in books else 'Unknown'
                borrow_history.append({
                    'book_title': book_title,
                    'borrow_date': b['borrow_date'],
                    'return_date': b['return_date'] if b['return_date'] else ''
                })
        return render_template('profile.html', user=user, borrow_history=borrow_history)

    if request.method == 'POST':
        # Process profile update
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not email or not phone or not address:
            flash('All fields are required.', 'error')
            return redirect(url_for('user_profile'))

        user['email'] = email
        user['phone'] = phone
        user['address'] = address

        users[username] = user
        save_users(users)

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_profile'))

# 19. Payment Confirmation page (GET and POST)
@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        flash('Fine record not found.', 'error')
        return redirect(url_for('user_profile'))

    username = LOGGED_IN_USERNAME

    if fine['username'] != username:
        flash('You can only pay your own fines.', 'error')
        return redirect(url_for('user_profile'))

    if request.method == 'GET':
        return render_template('payment_confirmation.html', fine=fine)

    if request.method == 'POST':
        # Process payment
        if fine['status'] == 'Paid':
            flash('Fine is already paid.', 'info')
            return redirect(url_for('user_profile'))

        fine['status'] = 'Paid'
        fines[fine_id] = fine
        save_fines(fines)

        flash('Payment processed successfully.', 'success')
        return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True)
