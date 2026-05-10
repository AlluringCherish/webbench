'''
Main backend application for the OnlineLibrary web application.
Handles routing, data loading, and rendering of pages.
Ensures the root route '/' serves the Dashboard page as the first page.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
DATA_DIR = 'data'
# Helper functions to read and write data files
def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
    return users
def read_books():
    path = os.path.join(DATA_DIR, 'books.txt')
    books = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                        'avg_rating': parts[9]
                    })
    return books
def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books:
            line = '|'.join([
                b['book_id'], b['title'], b['author'], b['isbn'], b['genre'],
                b['publisher'], b['year'], b['description'], b['status'], b['avg_rating']
            ])
            f.write(line + '\n')
def read_borrowings():
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    borrowings = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    borrowings.append({
                        'borrow_id': parts[0],
                        'username': parts[1],
                        'book_id': parts[2],
                        'borrow_date': parts[3],
                        'due_date': parts[4],
                        'return_date': parts[5],
                        'status': parts[6],
                        'fine_amount': parts[7]
                    })
    return borrowings
def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings:
            line = '|'.join([
                b['borrow_id'], b['username'], b['book_id'], b['borrow_date'],
                b['due_date'], b['return_date'], b['status'], b['fine_amount']
            ])
            f.write(line + '\n')
def read_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    reservations.append({
                        'reservation_id': parts[0],
                        'username': parts[1],
                        'book_id': parts[2],
                        'reservation_date': parts[3],
                        'status': parts[4]
                    })
    return reservations
def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']
            ])
            f.write(line + '\n')
def read_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    reviews.append({
                        'review_id': parts[0],
                        'username': parts[1],
                        'book_id': parts[2],
                        'rating': parts[3],
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                r['review_id'], r['username'], r['book_id'], r['rating'], r['review_text'], r['review_date']
            ])
            f.write(line + '\n')
def read_fines():
    path = os.path.join(DATA_DIR, 'fines.txt')
    fines = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    fines.append({
                        'fine_id': parts[0],
                        'username': parts[1],
                        'borrow_id': parts[2],
                        'amount': parts[3],
                        'status': parts[4],
                        'date_issued': parts[5]
                    })
    return fines
def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines:
            line = '|'.join([
                fine['fine_id'], fine['username'], fine['borrow_id'], fine['amount'], fine['status'], fine['date_issued']
            ])
            f.write(line + '\n')
# Dummy current user for demonstration purposes
current_user = 'john_reader'
@app.route('/')
def home():
    # Redirect root route to dashboard page as required
    return redirect(url_for('dashboard'))
@app.route('/dashboard')
def dashboard():
    # Load featured books (for simplicity, top 3 by avg_rating descending)
    books = read_books()
    featured_books = sorted(books, key=lambda b: float(b['avg_rating']), reverse=True)[:3]
    return render_template('dashboard.html', username=current_user, featured_books=featured_books)
# Additional routes (catalog, book details, borrow confirmation, my borrowings, etc.) would be here
# For brevity, only the root and dashboard routes are shown as per the fix requirement
if __name__ == '__main__':
    app.run(debug=True)