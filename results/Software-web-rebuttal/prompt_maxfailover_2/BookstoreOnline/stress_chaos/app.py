from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_DIR = 'data'
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
CART_FILE = os.path.join(DATA_DIR, 'cart.txt')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.txt')
ORDER_ITEMS_FILE = os.path.join(DATA_DIR, 'order_items.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
BESTSELLERS_FILE = os.path.join(DATA_DIR, 'bestsellers.txt')


# Utility functions for data handling

def read_books():
    books = []
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                book = {
                    'book_id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'isbn': parts[3],
                    'category': parts[4],
                    'price': float(parts[5]),
                    'stock': int(parts[6]),
                    'description': parts[7]
                }
                books.append(book)
            except ValueError:
                continue
    return books


def read_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
            except ValueError:
                continue
    return categories


def read_cart():
    items = []
    if not os.path.exists(CART_FILE):
        return items
    with open(CART_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            try:
                item = {
                    'cart_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }
                items.append(item)
            except ValueError:
                continue
    return items


def write_cart(items):
    # items is list of dicts with keys: cart_id, book_id, quantity, added_date
    lines = []
    for item in items:
        line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
        lines.append(line)
    with open(CART_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + ('\n' if lines else ''))


def read_orders():
    orders = []
    if not os.path.exists(ORDERS_FILE):
        return orders
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': parts[4],
                    'shipping_address': parts[5]
                }
                orders.append(order)
            except ValueError:
                continue
    return orders


def write_orders(orders):
    lines = []
    for order in orders:
        line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}"
        lines.append(line)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + ('\n' if lines else ''))


def read_order_items():
    items = []
    if not os.path.exists(ORDER_ITEMS_FILE):
        return items
    with open(ORDER_ITEMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                items.append(item)
            except ValueError:
                continue
    return items


def write_order_items(items):
    lines = []
    for item in items:
        line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}"
        lines.append(line)
    with open(ORDER_ITEMS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + ('\n' if lines else ''))


def read_reviews():
    reviews = []
    if not os.path.exists(REVIEWS_FILE):
        return reviews
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                review = {
                    'review_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
            except ValueError:
                continue
    return reviews


def write_reviews(reviews):
    lines = []
    for rev in reviews:
        line = f"{rev['review_id']}|{rev['book_id']}|{rev['customer_name']}|{rev['rating']}|{rev['review_text']}|{rev['review_date']}"
        lines.append(line)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + ('\n' if lines else ''))


def read_bestsellers():
    bestsellers = []
    if not os.path.exists(BESTSELLERS_FILE):
        return bestsellers
    with open(BESTSELLERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                bestseller = {
                    'book_id': int(parts[0]),
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                }
                bestsellers.append(bestseller)
            except ValueError:
                continue
    return bestsellers


# Root route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Dashboard
@app.route('/dashboard')
def dashboard():
    books = read_books()
    # Select featured books: for example, first 5 books
    featured_books = []
    for book in books[:5]:
        featured_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price']
        })
    return render_template('dashboard.html', featured_books=featured_books)


# Catalog
@app.route('/catalog')
def catalog():
    books_all = read_books()
    categories = read_categories()

    search_query = request.args.get('search', '')
    selected_category = request.args.get('category', '')

    # Filter books by search
    def match_book(book, query):
        q = query.lower()
        if (q in book['title'].lower()) or (q in book['author'].lower()) or (q in book['isbn'].lower()):
            return True
        return False

    filtered_books = []
    for book in books_all:
        if search_query and not match_book(book, search_query):
            continue
        if selected_category and selected_category != '' and book['category'] != selected_category:
            continue
        filtered_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'category': book['category'],
            'price': book['price']
        })

    return render_template('catalog.html', books=filtered_books, categories=categories, search_query=search_query, selected_category=selected_category)


# Book Details
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = b
            break
    if book is None:
        return "Book not found", 404

    # Get reviews for this book
    all_reviews = read_reviews()
    reviews = []
    for r in all_reviews:
        if r['book_id'] == book_id:
            reviews.append(r)

    return render_template('book_details.html', book=book, reviews=reviews)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        book_id = int(request.form.get('book_id'))
    except (ValueError, TypeError):
        return redirect(url_for('cart'))

    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart_items = read_cart()
    # Check if book already in cart, increment quantity
    found = False
    for item in cart_items:
        if item['book_id'] == book_id:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        # Generate new cart_id
        max_id = max([item['cart_id'] for item in cart_items], default=0)
        new_cart_id = max_id + 1
        added_date = datetime.now().strftime('%Y-%m-%d')
        cart_items.append({'cart_id': new_cart_id, 'book_id': book_id, 'quantity': quantity, 'added_date': added_date})

    write_cart(cart_items)
    return redirect(url_for('cart'))


# Shopping Cart
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Determine action by form fields
        if 'item_id' in request.form and 'quantity' in request.form:
            # Update quantity
            try:
                item_id = int(request.form.get('item_id'))
                quantity = int(request.form.get('quantity'))
            except ValueError:
                return redirect(url_for('cart'))
            if quantity < 1:
                quantity = 1
            cart_items = read_cart()
            updated = False
            for item in cart_items:
                if item['cart_id'] == item_id:
                    item['quantity'] = quantity
                    updated = True
                    break
            if updated:
                write_cart(cart_items)
            return redirect(url_for('cart'))

        elif 'remove_item_id' in request.form:
            try:
                remove_id = int(request.form.get('remove_item_id'))
            except ValueError:
                return redirect(url_for('cart'))
            cart_items = read_cart()
            cart_items = [item for item in cart_items if item['cart_id'] != remove_id]
            write_cart(cart_items)
            return redirect(url_for('cart'))

        else:
            return redirect(url_for('cart'))

    else:
        cart_items_raw = read_cart()
        books = read_books()
        book_dict = {book['book_id']: book for book in books}
        cart_items = []
        total_amount = 0.0
        for item in cart_items_raw:
            book = book_dict.get(item['book_id'])
            if book is None:
                continue
            quantity = item['quantity']
            subtotal = round(book['price'] * quantity, 2)
            total_amount += subtotal
            cart_items.append({
                'item_id': item['cart_id'],
                'book': {
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'price': book['price'],
                },
                'quantity': quantity,
                'subtotal': subtotal
            })
        total_amount = round(total_amount, 2)
        return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# Checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart_items_raw = read_cart()
        books = read_books()
        book_dict = {b['book_id']: b for b in books}

        cart_items = []
        total_amount = 0.0
        for item in cart_items_raw:
            book = book_dict.get(item['book_id'])
            if book is None:
                continue
            quantity = item['quantity']
            subtotal = round(book['price'] * quantity, 2)
            total_amount += subtotal
            cart_items.append({
                'item_id': item['cart_id'],
                'book': {
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'price': book['price'],
                },
                'quantity': quantity,
                'subtotal': subtotal
            })
        total_amount = round(total_amount, 2)
        return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

    # POST processing order
    customer_name = request.form.get('customer_name', '').strip()
    shipping_address = request.form.get('shipping_address', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if (not customer_name) or (not shipping_address) or (payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']):
        # Invalid input - redirect back to checkout
        return redirect(url_for('checkout'))

    cart_items_raw = read_cart()
    if not cart_items_raw:
        # Cart empty - redirect to cart
        return redirect(url_for('cart'))

    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    total_amount = 0.0
    # Calculate total amount
    for item in cart_items_raw:
        book = book_dict.get(item['book_id'])
        if book is None:
            continue
        total_amount += book['price'] * item['quantity']

    total_amount = round(total_amount, 2)

    # Create new order
    orders = read_orders()
    max_order_id = max([o['order_id'] for o in orders], default=0)
    new_order_id = max_order_id + 1

    order_date = datetime.now().strftime('%Y-%m-%d')
    order_status = 'Pending'

    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': order_status,
        'shipping_address': shipping_address
    }
    orders.append(new_order)
    write_orders(orders)

    # Create order items
    order_items = read_order_items()
    max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
    for item in cart_items_raw:
        book = book_dict.get(item['book_id'])
        if not book:
            continue
        max_order_item_id += 1
        order_item = {
            'order_item_id': max_order_item_id,
            'order_id': new_order_id,
            'book_id': book['book_id'],
            'quantity': item['quantity'],
            'price': book['price']
        }
        order_items.append(order_item)
    write_order_items(order_items)

    # Clear cart
    write_cart([])

    return redirect(url_for('orders'))


# Orders History
@app.route('/orders')
def orders():
    filter_status = request.args.get('status', 'All')
    all_orders = read_orders()
    if filter_status != 'All':
        filtered = [o for o in all_orders if o['status'] == filter_status]
    else:
        filtered = all_orders
    return render_template('orders.html', orders=filtered, filter_status=filter_status)


# Reviews
@app.route('/reviews')
def reviews():
    selected_rating = request.args.get('rating', '')
    all_reviews = read_reviews()
    books = read_books()
    book_titles = {b['book_id']: b['title'] for b in books}

    filtered_reviews = []
    for r in all_reviews:
        if selected_rating and selected_rating.isdigit():
            if r['rating'] != int(selected_rating):
                continue
        filtered_reviews.append({
            'book_title': book_titles.get(r['book_id'], 'Unknown'),
            'rating': r['rating'],
            'review_text': r['review_text']
        })

    return render_template('reviews.html', reviews=filtered_reviews, selected_rating=selected_rating)


# Write Review
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        books = read_books()
        books_list = []
        for b in books:
            books_list.append({'book_id': b['book_id'], 'title': b['title']})
        return render_template('write_review.html', books=books_list)

    book_id = request.form.get('book_id')
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    # Validate inputs
    try:
        book_id = int(book_id)
        rating = int(rating)
    except (ValueError, TypeError):
        return redirect(url_for('write_review'))

    if rating < 1 or rating > 5:
        return redirect(url_for('write_review'))

    if not review_text:
        return redirect(url_for('write_review'))

    reviews = read_reviews()
    max_review_id = max([r['review_id'] for r in reviews], default=0)
    new_review_id = max_review_id + 1

    # customer_name is not captured in form, use 'Anonymous'
    customer_name = 'Anonymous'
    review_date = datetime.now().strftime('%Y-%m-%d')

    new_review = {
        'review_id': new_review_id,
        'book_id': book_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }

    reviews.append(new_review)
    write_reviews(reviews)

    return redirect(url_for('reviews'))


# Bestsellers
@app.route('/bestsellers')
def bestsellers():
    period_options = ['This Week', 'This Month', 'All Time']
    selected_period = request.args.get('period', 'All Time')
    all_bestsellers = read_bestsellers()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}
    filtered_bestsellers = []

    for bs in all_bestsellers:
        if selected_period == 'All Time' or bs['period'] == selected_period:
            book = book_dict.get(bs['book_id'])
            if book:
                filtered_bestsellers.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'price': book['price'],
                    'sales_count': bs['sales_count']
                })

    # Sort by sales_count descending
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)

    return render_template('bestsellers.html', bestsellers=filtered_bestsellers, selected_period=selected_period, period_options=period_options)


if __name__ == '__main__':
    app.run(debug=True)
