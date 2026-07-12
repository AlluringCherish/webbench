from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read and write data files

def read_books():
    books = []
    try:
        with open(os.path.join(DATA_DIR, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue  # Skip malformed lines
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
    except Exception:
        pass
    return books


def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except Exception:
        pass
    return categories


def read_cart():
    cart_items = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                item = {
                    'cart_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }
                cart_items.append(item)
    except Exception:
        pass
    return cart_items


def write_cart(cart_items):
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def read_orders():
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': parts[4],
                    'shipping_address': parts[5]
                }
                orders.append(order)
    except Exception:
        pass
    return orders


def write_orders(orders):
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def read_order_items():
    order_items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(item)
    except Exception:
        pass
    return order_items


def write_order_items(items):
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'w', encoding='utf-8') as f:
            for item in items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review = {
                    'review_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    except Exception:
        pass
    return reviews


def write_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def read_bestsellers():
    bestsellers = []
    try:
        with open(os.path.join(DATA_DIR, 'bestsellers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                item = {
                    'book_id': int(parts[0]),
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                }
                bestsellers.append(item)
    except Exception:
        pass
    return bestsellers


# Route Implementations

from flask import abort

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    books = read_books()
    # Arbitrary logic: featured_books - first 5 in the list
    featured_books = books[:5]
    # Bestsellers for All Time
    bestsellers_data = read_bestsellers()
    # We prioritize bestsellers for 'All Time' period, if none then any period
    all_time_bestsellers = [b for b in bestsellers_data if b['period'] == 'All Time']
    period = 'All Time'
    if not all_time_bestsellers:
        # fallback to any period if no 'All Time' found
        all_time_bestsellers = bestsellers_data
        period = all_time_bestsellers[0]['period'] if all_time_bestsellers else 'All Time'

    # Join books info for bestsellers
    bestsellers = []
    for b in all_time_bestsellers:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        if book:
            bs = book.copy()
            bs['sales_count'] = b['sales_count']
            bestsellers.append(bs)
    # Sort descending by sales_count
    bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


@app.route('/catalog')
def book_catalog():
    books = read_books()
    categories = read_categories()
    selected_category = request.args.get('category', '')
    search_query = request.args.get('search', '').strip()

    filtered_books = books
    if selected_category:
        filtered_books = [b for b in filtered_books if b['category'] == selected_category]

    if search_query:
        sq = search_query.lower()
        filtered_books = [b for b in filtered_books if sq in b['title'].lower() or sq in b['author'].lower()]

    return render_template('catalog.html', 
                           books=filtered_books, 
                           categories=categories, 
                           selected_category=selected_category, 
                           search_query=search_query)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        abort(404)
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]

    # Sort reviews by date desc
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/book/<int:book_id>/add_to_cart', methods=['POST'])
def add_to_cart(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        abort(404)

    cart_items = read_cart()
    # Check if book already in cart, if so increase quantity
    item = next((item for item in cart_items if item['book_id'] == book_id), None)
    if item:
        item['quantity'] += 1
    else:
        new_id = max((item['cart_id'] for item in cart_items), default=0) + 1
        added_date = datetime.now().strftime('%Y-%m-%d')
        cart_items.append({'cart_id': new_id, 'book_id': book_id, 'quantity': 1, 'added_date': added_date})

    write_cart(cart_items)

    return redirect(url_for('book_details', book_id=book_id))


@app.route('/cart')
def cart():
    cart_items = read_cart()
    books = read_books()
    detailed_cart = []
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            d_item = {
                'item_id': item['cart_id'],
                'book': book,
                'quantity': item['quantity'],
                'total_price': item['quantity'] * book['price']
            }
            total_amount += d_item['total_price']
            detailed_cart.append(d_item)

    return render_template('cart.html', cart_items=detailed_cart, total_amount=total_amount)


@app.route('/cart/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    new_quantity = request.form.get('quantity')
    try:
        new_quantity = int(new_quantity)
        if new_quantity < 1:
            new_quantity = 1
    except Exception:
        new_quantity = 1

    cart_items = read_cart()
    for item in cart_items:
        if item['cart_id'] == item_id:
            item['quantity'] = new_quantity
            break

    write_cart(cart_items)
    return redirect(url_for('cart'))


@app.route('/cart/remove_item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    cart_items = read_cart()
    cart_items = [item for item in cart_items if item['cart_id'] != item_id]
    write_cart(cart_items)
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/checkout/place_order', methods=['POST'])
def place_order():
    customer_name = request.form.get('customer-name', '').strip()
    shipping_address = request.form.get('shipping-address', '').strip()
    payment_method = request.form.get('payment-method', '').strip()

    if not customer_name or not shipping_address or not payment_method:
        # Missing required fields, redirect back to checkout
        return redirect(url_for('checkout'))

    cart_items = read_cart()
    if not cart_items:
        return redirect(url_for('checkout'))

    books = read_books()

    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            total_amount += item['quantity'] * book['price']

    orders = read_orders()
    order_items = read_order_items()

    new_order_id = max((o['order_id'] for o in orders), default=0) + 1
    order_date = datetime.now().strftime('%Y-%m-%d')
    status = 'Pending'

    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': status,
        'shipping_address': shipping_address
    }
    orders.append(new_order)

    new_order_items = []
    next_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0) + 1

    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            new_item = {
                'order_item_id': next_order_item_id,
                'order_id': new_order_id,
                'book_id': book['book_id'],
                'quantity': item['quantity'],
                'price': book['price']
            }
            new_order_items.append(new_item)
            next_order_item_id += 1

    order_items.extend(new_order_items)

    success_orders = write_orders(orders)
    success_order_items = write_order_items(order_items)

    if success_orders and success_order_items:
        # Clear cart
        write_cart([])
        return redirect(url_for('order_history'))
    else:
        # On failure, redirect back to checkout
        return redirect(url_for('checkout'))


@app.route('/orders')
def order_history():
    orders = read_orders()
    status_filter = request.args.get('status', '')
    if status_filter:
        orders = [o for o in orders if o['status'].lower() == status_filter.lower()]

    return render_template('orders.html', orders=orders, status_filter=status_filter)


@app.route('/orders/<int:order_id>')
def view_order(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    order_items = read_order_items()
    books = read_books()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book:
                item = {
                    'order_item_id': oi['order_item_id'],
                    'book': book,
                    'quantity': oi['quantity'],
                    'price': oi['price']
                }
                items.append(item)

    # No template specified for order detail page; we prepare data for potential future use
    # For now, returning 404 if someone tries to access this route because no template defined is an option
    # But per spec, render_template optional, so we will do a minimal page rendering

    # For demonstration, let's render a simple template named order_details.html if exists
    # But since no template spec, we respond with abort 404
    abort(404)


@app.route('/reviews')
def reviews_page():
    reviews = read_reviews()
    rating_filter = request.args.get('rating', '')
    filtered_reviews = reviews
    if rating_filter:
        try:
            rf = int(rating_filter)
            filtered_reviews = [r for r in reviews if r['rating'] == rf]
        except Exception:
            filtered_reviews = reviews

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)


@app.route('/write_review')
def write_review_page():
    books = read_books()
    return render_template('write_review.html', books=books)


@app.route('/write_review/submit', methods=['POST'])
def submit_review():
    book_id = request.form.get('select-book')
    rating = request.form.get('rating-select')
    review_text = request.form.get('review-text', '').strip()

    try:
        book_id = int(book_id)
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except Exception:
        return redirect(url_for('write_review_page'))

    if not review_text:
        return redirect(url_for('write_review_page'))

    books = read_books()
    # Validate book_id exists
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return redirect(url_for('write_review_page'))

    reviews = read_reviews()
    new_review_id = max((r['review_id'] for r in reviews), default=0) + 1
    review_date = datetime.now().strftime('%Y-%m-%d')
    # Customer name is not specified in form, we put a default name or anonymous
    customer_name = 'Anonymous'

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

    return redirect(url_for('reviews_page'))


@app.route('/bestsellers')
def bestsellers_page():
    time_period = request.args.get('period', 'This Week')
    bestsellers_data = [b for b in read_bestsellers() if b['period'] == time_period]

    books = read_books()
    bestsellers = []
    for b in bestsellers_data:
        book = next((bk for bk in books if bk['book_id'] == b['book_id']), None)
        if book:
            bs = book.copy()
            bs['sales_count'] = b['sales_count']
            bestsellers.append(bs)

    bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)

    return render_template('bestsellers.html', bestsellers=bestsellers, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
