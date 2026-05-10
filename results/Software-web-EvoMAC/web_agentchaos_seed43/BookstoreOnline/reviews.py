'''
Customer Reviews page module for BookstoreOnline web application.
Displays all reviews and allows navigation to write review page.
'''
from flask import Blueprint, render_template, request
from utils import read_reviews, read_books
reviews_bp = Blueprint('reviews', __name__, template_folder='templates')
@reviews_bp.route('/reviews')
def reviews():
    rating_filter = request.args.get('rating', 'All')
    reviews = read_reviews()
    if rating_filter != 'All':
        rating_value = int(rating_filter[0])
        reviews = [r for r in reviews if r['rating'] == rating_value]
    books = {b['book_id']: b['title'] for b in read_books()}
    return render_template('reviews.html', reviews=reviews, books=books, rating_filter=rating_filter)