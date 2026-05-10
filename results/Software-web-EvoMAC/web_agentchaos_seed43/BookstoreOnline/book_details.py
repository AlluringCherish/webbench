'''
Book Details page module for BookstoreOnline web application.
Displays detailed information about a specific book and its reviews.
'''
from flask import Blueprint, render_template, request, redirect, url_for
from utils import read_books, read_reviews, add_to_cart
book_details_bp = Blueprint('book_details', __name__, template_folder='templates')
@book_details_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    if request.method == 'POST':
        # Add to cart action
        quantity = int(request.form.get('quantity', 1))
        add_to_cart(book_id, quantity)
        return redirect(url_for('cart.view_cart'))
    reviews = read_reviews(book_id=book_id)
    return render_template('book_details.html', book=book, reviews=reviews)