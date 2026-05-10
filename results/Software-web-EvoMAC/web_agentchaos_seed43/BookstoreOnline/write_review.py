'''
Write Review page module for BookstoreOnline web application.
Allows users to submit reviews for purchased books.
'''
from flask import Blueprint, render_template, request, redirect, url_for
from utils import read_books, add_review
write_review_bp = Blueprint('write_review', __name__, template_folder='templates')
@write_review_bp.route('/write-review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'POST':
        book_id = int(request.form.get('select-book'))
        rating = int(request.form.get('rating-select'))
        review_text = request.form.get('review-text', '').strip()
        customer_name = "Anonymous"  # No authentication, so default name
        if not review_text:
            error = "Review text cannot be empty."
            return render_template('write_review.html', books=books, error=error)
        add_review(book_id, customer_name, rating, review_text)
        return redirect(url_for('reviews.reviews'))
    return render_template('write_review.html', books=books)