from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__, template_folder='templates_candidate_b')
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Helper functions for reading and writing data files

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
            users[username] = {'username': username, 'email': email, 'phone': phone, 'address': address}
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
            parts = line.split('|')
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
    return books


def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books.values():
            line = f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}\n"
            f.write(line)


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
            borrow_id = int(parts[0])
            username = parts[1]
            book_id = int(parts[2])
            borrow_date = parts[3]
            due_date = parts[4]
            return_date = parts[5]
            status = parts[6]
            fine_amount = parts[7]
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
    return borrowings


def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            line = f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date']}|{b['status']}|{b['fine_amount']}\n"
            f.write(line)


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
    return reservations


def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n"
            f.write(line)


def read_reviews():
    reviews = {}
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
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
    return reviews


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)


def read_fines():
    fines = {}
    path = os.path.join(DATA_DIR, 'fines.txt')
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            fine_id = int(parts[0])
            username = parts[1]
            borrow_id = int(parts[2])
            amount = parts[3]
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
    return fines


def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fin in fines.values():
            line = f"{fin['fine_id']}|{fin['username']}|{fin['borrow_id']}|{fin['amount']}|{fin['status']}|{fin['date_issued']}\n"
            f.write(line)


# A fixed logged-in user for demo purposes
LOGGED_IN_USER = 'john_reader'

@app.route('/')
@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USER
    books = read_books()
    # For featured, pick books with status Available or Borrowed or Reserved (any) just limit to 3
    featured_books = []
    cnt = 0
    for b in books.values():
        featured_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']})
        cnt += 1
        if cnt >= 3:
            break
    return render_template('dashboard.html', username=username, featured_books=featured_books)


@app.route('/catalog')
def catalog():
    books = read_books()
    search_query = request.args.get('search', '').strip().lower()
    filtered_books = []
    for b in books.values():
        if search_query == '' or search_query in b['title'].lower() or search_query in b['author'].lower():
            filtered_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']})
    return render_template('catalog.html', books=filtered_books, search_query=request.args.get('search',''))


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404
    reviews_all = read_reviews()
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
    can_borrow = (book['status'] == 'Available')
    return render_template('book_details.html', book=book, reviews=reviews, can_borrow=can_borrow)


@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    username = LOGGED_IN_USER
    books = read_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404
    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    if request.method == 'POST':
        # Confirm borrow
        borrowings = read_borrowings()
        # Generate new borrow_id
        new_borrow_id = max(borrowings.keys(), default=0) + 1
        borrow_date = datetime.date.today()
        due_date = borrow_date + datetime.timedelta(days=14)
        borrowings[new_borrow_id] = {
            'borrow_id': new_borrow_id,
            'username': username,
            'book_id': book_id,
            'borrow_date': borrow_date.isoformat(),
            'due_date': due_date.isoformat(),
            'return_date': '',
            'status': 'Active',
            'fine_amount': '0'
        }
        write_borrowings(borrowings)

        # Update book status to Borrowed
        book['status'] = 'Borrowed'
        books[book_id] = book
        write_books(books)

        flash('Book borrowed successfully!')
        return redirect(url_for('my_borrows'))

    else:
        borrow_date = datetime.date.today()
        due_date = borrow_date + datetime.timedelta(days=14)
        return render_template('borrow_confirmation.html', book=book, due_date=due_date.isoformat())


@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    username = LOGGED_IN_USER
    borrowings = read_borrowings()
    books = read_books()

    filter_status = request.args.get('filter_status', 'All')

    # Handle return book POST
    if request.method == 'POST':
        return_id = request.form.get('return_id')
        if return_id:
            return_id = int(return_id)
            borrowing = borrowings.get(return_id)
            if borrowing and borrowing['username'] == username and borrowing['status'] == 'Active':
                borrowing['status'] = 'Returned'
                borrowing['return_date'] = datetime.date.today().isoformat()
                borrowing['fine_amount'] = '0'
                borrowings[return_id] = borrowing
                write_borrowings(borrowings)

                # Update book status to Available
                book_id = borrowing['book_id']
                if book_id in books:
                    books[book_id]['status'] = 'Available'
                    write_books(books)

                flash('Book returned successfully.')
                return redirect(url_for('my_borrows', filter_status=filter_status))

    filtered_borrows = []
    for b in borrowings.values():
        if b['username'] != username:
            continue
        if filter_status != 'All' and b['status'] != filter_status:
            continue
        book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
        filtered_borrows.append({
            'borrow_id': b['borrow_id'],
            'book_title': book_title,
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    return render_template('my_borrowings.html', borrows=filtered_borrows, filter_status=filter_status)


@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    username = LOGGED_IN_USER
    reservations = read_reservations()
    books = read_books()

    if request.method == 'POST':
        cancel_id = request.form.get('cancel_id')
        if cancel_id:
            cancel_id = int(cancel_id)
            reservation = reservations.get(cancel_id)
            if reservation and reservation['username'] == username and reservation['status'] == 'Active':
                reservation['status'] = 'Cancelled'
                reservations[cancel_id] = reservation
                write_reservations(reservations)
                flash('Reservation cancelled successfully.')
                return redirect(url_for('my_reservations'))

    user_reservations = []
    for r in reservations.values():
        if r['username'] != username:
            continue
        book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
        user_reservations.append({
            'reservation_id': r['reservation_id'],
            'book_title': book_title,
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })

    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/my-reviews', methods=['GET', 'POST'])
def my_reviews():
    username = LOGGED_IN_USER
    reviews_all = read_reviews()
    books = read_books()

    # Handle delete review POST
    if request.method == 'POST':
        delete_id = request.form.get('delete_id')
        if delete_id:
            delete_id = int(delete_id)
            review = reviews_all.get(delete_id)
            if review and review['username'] == username:
                del reviews_all[delete_id]
                write_reviews(reviews_all)
                flash('Review deleted successfully.')
                return redirect(url_for('my_reviews'))

    user_reviews = []
    for r in reviews_all.values():
        if r['username'] != username:
            continue
        book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
        user_reviews.append({
            'review_id': r['review_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text']
        })

    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    username = LOGGED_IN_USER
    books = read_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404

    reviews_all = read_reviews()
    existing_review = None
    for r in reviews_all.values():
        if r['book_id'] == book_id and r['username'] == username:
            existing_review = r
            break

    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()
        if not rating or not review_text:
            flash('Rating and review text are required.')
            return redirect(url_for('write_review', book_id=book_id))

        rating = int(rating)
        today = datetime.date.today().isoformat()

        if existing_review:
            # Update existing
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = today
        else:
            # Create new
            new_review_id = max(reviews_all.keys(), default=0) + 1
            reviews_all[new_review_id] = {
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': today
            }
        write_reviews(reviews_all)
        flash('Review submitted successfully.')
        return redirect(url_for('book_details', book_id=book_id))

    context_existing = None
    if existing_review:
        context_existing = {
            'review_id': existing_review['review_id'],
            'rating': existing_review['rating'],
            'review_text': existing_review['review_text']
        }
    return render_template('write_review.html', book=book, existing_review=context_existing)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = LOGGED_IN_USER
    users = read_users()
    user = users.get(username)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        email = request.form.get('profile_email', '').strip()
        if not email:
            flash('Email cannot be empty.')
            return redirect(url_for('profile'))
        user['email'] = email
        users[username] = user
        write_users(users)
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))

    borrowings = read_borrowings()
    books = read_books()
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username:
            book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
            borrow_history.append({
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', username=username, email=user['email'], borrow_history=borrow_history)


@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment(fine_id):
    username = LOGGED_IN_USER
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != username:
        return "Fine not found", 404

    if request.method == 'POST':
        # Confirm payment
        fine['status'] = 'Paid'
        fines[fine_id] = fine
        write_fines(fines)
        flash('Fine payment successful.')
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine)


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
