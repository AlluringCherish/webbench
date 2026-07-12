from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for file operations

def read_pipe_delimited_file(filename, field_count):
    path = os.path.join(DATA_DIR, filename)
    entries = []
    if not os.path.exists(path):
        return entries
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != field_count:
                    continue
                entries.append(parts)
    except Exception:
        # Graceful error handling
        return []
    return entries


def write_pipe_delimited_file(filename, rows):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for row in rows:
                line = '|'.join(str(item) for item in row)
                f.write(line + '\n')
        return True
    except Exception:
        return False


# Books data helper

def load_books():
    # Fields in order: book_id (int), title (str), author (str), isbn (str), category (str), price (float), stock (int), description (str)
    raw = read_pipe_delimited_file('books.txt', 8)
    books = []
    for r in raw:
        try:
            books.append({
                'book_id': int(r[0]),
                'title': r[1],
                'author': r[2],
                'isbn': r[3],
                'category': r[4],
                'price': float(r[5]),
                'stock': int(r[6]),
                'description': r[7]
            })
        except Exception:
            continue
    return books


def save_books(books):
    rows = []
    for b in books:
        rows.append([
            b['book_id'],
            b['title'],
            b['author'],
            b['isbn'],
            b['category'],
            b['price'],
            b['stock'],
            b['description']
        ])
    return write_pipe_delimited_file('books.txt', rows)


# Categories helper

def load_categories():
    # Fields: category_id (int), category_name (str), description (str)
    raw = read_pipe_delimited_file('categories.txt', 3)
    categories = []
    for r in raw:
        try:
            categories.append({
                'category_id': int(r[0]),
                'category_name': r[1],
                'description': r[2]
            })
        except Exception:
            continue
    return categories


# Cart helper

def load_cart():
    # Fields: cart_id (int), book_id (int), quantity (int), added_date (str)
    raw = read_pipe_delimited_file('cart.txt', 4)
    cart = []
    for r in raw:
        try:
            cart.append({
                'cart_id': int(r[0]),
                'book_id': int(r[1]),
                'quantity': int(r[2]),
                'added_date': r[3]
            })
        except Exception:
            continue
    return cart


def save_cart(cart):
    rows = []
    for item in cart:
        rows.append([
            item['cart_id'],
            item['book_id'],
            item['quantity'],
            item['added_date']
        ])
    return write_pipe_delimited_file('cart.txt', rows)


# Orders helper

def load_orders():
    # Fields: order_id (int), customer_name (str), order_date (str), total_amount (float), status (str), shipping_address (str)
    raw = read_pipe_delimited_file('orders.txt', 6)
    orders = []
    for r in raw:
        try:
            orders.append({
                'order_id': int(r[0]),
                'customer_name': r[1],
                'order_date': r[2],
                'total_amount': float(r[3]),
                'status': r[4],
                'shipping_address': r[5]
            })
        except Exception:
            continue
    return orders


def save_orders(orders):
    rows = []
    for order in orders:
        rows.append([
            order['order_id'],
            order['customer_name'],
            order['order_date'],
            order['total_amount'],
            order['status'],
            order['shipping_address']
        ])
    return write_pipe_delimited_file('orders.txt', rows)


# Order items helper

def load_order_items():
    # Fields: order_item_id (int), order_id (int), book_id (int), quantity (int), price (float)
    raw = read_pipe_delimited_file('order_items.txt', 5)
    items = []
    for r in raw:
        try:
            items.append({
                'order_item_id': int(r[0]),
                'order_id': int(r[1]),
                'book_id': int(r[2]),
                'quantity': int(r[3]),
                'price': float(r[4])
            })
        except Exception:
            continue
    return items


def save_order_items(items):
    rows = []
    for item in items:
        rows.append([
            item['order_item_id'],
            item['order_id'],
            item['book_id'],
            item['quantity'],
            item['price']
        ])
    return write_pipe_delimited_file('order_items.txt', rows)


# Reviews helper

def load_reviews():
    # Fields: review_id (int), book_id (int), customer_name (str), rating (int), review_text (str), review_date (str)
    raw = read_pipe_delimited_file('reviews.txt', 6)
    reviews = []
    for r in raw:
        try:
            reviews.append({
                'review_id': int(r[0]),
                'book_id': int(r[1]),
                'customer_name': r[2],
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            })
        except Exception:
            continue
    return reviews


def save_reviews(reviews):
    rows = []
    for rev in reviews:
        rows.append([
            rev['review_id'],
            rev['book_id'],
            rev['customer_name'],
            rev['rating'],
            rev['review_text'],
            rev['review_date']
        ])
    return write_pipe_delimited_file('reviews.txt', rows)


# Bestsellers helper

def load_bestsellers():
    # Fields: book_id (int), sales_count (int), period (str)
    raw = read_pipe_delimited_file('bestsellers.txt', 3)
    bs = []
    for r in raw:
        try:
            bs.append({
                'book_id': int(r[0]),
                'sales_count': int(r[1]),
                'period': r[2]
            })
        except Exception:
            continue
    return bs


def save_bestsellers(bestsellers):
    rows = []
    for b in bestsellers:
        rows.append([
            b['book_id'],
            b['sales_count'],
            b['period']
        ])
    return write_pipe_delimited_file('bestsellers.txt', rows)


# Route 1 - Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route 2 - Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    # Featured books: Just top 5 books with stock > 0 (no criteria defined, will pick first 5)
    books = load_books()
    featured_books = []
    count = 0
    for b in books:
        if b['stock'] > 0:
            featured_books.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'price': b['price']
            })
            count += 1
            if count >= 5:
                break

    # Bestsellers from a will load all bestsellers for a default period 'All Time' as no other criteria given
    bestsellers_raw = load_bestsellers()
    # Map book_id-> book title, author
    books_map = {b['book_id']: b for b in books}
    bestsellers = []
    for bs in bestsellers_raw:
        # For dashboard we just take all bestsellers
        book = books_map.get(bs['book_id'])
        if book:
            bestsellers.append({
                'book_id': bs['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


# Route 3 - Book Catalog Page
@app.route('/catalog', methods=['GET'])
def book_catalog_page():
    categories = load_categories()
    books = load_books()

    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip() or None

    # Filter books
    filtered_books = []
    for b in books:
        # Filter category
        if selected_category and b['category'] != selected_category:
            continue
        # Filter search text in title or author, case insensitive
        if search_query:
            sq_lower = search_query.lower()
            if sq_lower not in b['title'].lower() and sq_lower not in b['author'].lower():
                continue
        filtered_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'category': b['category']
        })

    return render_template('catalog.html', categories=categories, books=filtered_books, search_query=search_query, selected_category=selected_category)


# Route 4 - Book Details Page
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details_page(book_id):
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        # Book not found, redirect to catalog
        return redirect(url_for('book_catalog_page'))

    reviews_all = load_reviews()
    # Filter reviews for this book
    reviews = [r for r in reviews_all if r['book_id'] == book_id]

    added_to_cart = None

    if request.method == 'POST':
        # Add one unit of this book to cart
        cart = load_cart()
        cart_item = next((c for c in cart if c['book_id'] == book_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
            today_str = datetime.today().strftime('%Y-%m-%d')
            cart.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': 1,
                'added_date': today_str
            })
        # Save updated cart
        save_cart(cart)
        added_to_cart = True

    return render_template('book_details.html', book=book, reviews=reviews, added_to_cart=added_to_cart)


# Route 5 - Shopping Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart_page():
    cart = load_cart()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    if request.method == 'POST':
        # Update quantities or remove items based on form fields
        # Remove item has button named e.g remove-item-button-{cart_id}
        remove_cart_id = None
        for key in request.form:
            if key.startswith('remove-item-button-'):
                try:
                    remove_cart_id = int(key[len('remove-item-button-'):])
                except Exception:
                    pass
                break

        if remove_cart_id is not None:
            # Remove the item
            cart = [c for c in cart if c['cart_id'] != remove_cart_id]
            save_cart(cart)
            return redirect(url_for('shopping_cart_page'))

        # Otherwise update quantities
        updated = False
        for item in cart:
            q_key = f'update-quantity-{item["cart_id"]}'
            if q_key in request.form:
                try:
                    new_qty = int(request.form[q_key])
                    if new_qty < 1:
                        # Remove if quantity less than 1
                        cart = [c for c in cart if c['cart_id'] != item['cart_id']]
                    else:
                        item['quantity'] = new_qty
                    updated = True
                except Exception:
                    continue
        if updated:
            save_cart(cart)
            return redirect(url_for('shopping_cart_page'))

    # Prepare cart_items for template
    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = books_map.get(item['book_id'])
        if not book:
            continue
        subtotal = book['price'] * item['quantity']
        cart_items.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal
        })
        total_amount += subtotal

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# Route 6 - Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart = load_cart()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    # Prepare cart_items and total_amount
    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = books_map.get(item['book_id'])
        if not book:
            continue
        subtotal = book['price'] * item['quantity']
        cart_items.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal
        })
        total_amount += subtotal

    payment_methods = ["Credit Card", "PayPal", "Bank Transfer"]

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        # Validate inputs
        if not customer_name or not shipping_address or payment_method not in payment_methods:
            # Failed validation, just re-render page with same data
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount, payment_methods=payment_methods)

        orders = load_orders()
        order_items = load_order_items()

        # Create new order
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        today_str = datetime.today().strftime('%Y-%m-%d')
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today_str,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)
        save_orders(orders)

        # Create order items
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for idx, item in enumerate(cart_items, 1):
            order_item = {
                'order_item_id': max_order_item_id + idx,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['price']
            }
            order_items.append(order_item)
        save_order_items(order_items)

        # Clear the cart
        save_cart([])

        # Redirect to order history page
        return redirect(url_for('order_history_page'))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount, payment_methods=payment_methods)


# Route 7 - Order History Page
@app.route('/orders', methods=['GET'])
def order_history_page():
    selected_status = request.args.get('status', 'All')
    orders = load_orders()
    if selected_status != 'All':
        orders = [o for o in orders if o['status'] == selected_status]

    return render_template('orders.html', orders=orders, selected_status=selected_status)


# Route 8 - Order Details Page
@app.route('/order/<int:order_id>', methods=['GET'])
def order_details_page(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return redirect(url_for('order_history_page'))

    order_items_all = load_order_items()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = books_map.get(oi['book_id'])
            title = book['title'] if book else 'Unknown'
            order_items.append({
                'order_item_id': oi['order_item_id'],
                'book_id': oi['book_id'],
                'title': title,
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    return render_template('order_details.html', order=order, order_items=order_items)


# Route 9 - Reviews Page
@app.route('/reviews', methods=['GET'])
def reviews_page():
    filter_rating = request.args.get('rating', 'All')
    reviews_all = load_reviews()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    filtered_reviews = []
    for r in reviews_all:
        if filter_rating != 'All' and filter_rating:
            try:
                int_rating = int(filter_rating)
                if r['rating'] != int_rating:
                    continue
            except Exception:
                pass
        book = books_map.get(r['book_id'])
        filtered_reviews.append({
            'review_id': r['review_id'],
            'book_title': book['title'] if book else 'Unknown',
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text']
        })
    return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)


# Route 10 - Write Review Page
@app.route('/write-review', methods=['GET', 'POST'])
def write_review_page():
    # Books eligible for review: those that are in orders placed by any customer (not tied to customer here, so we show all books in past orders)
    order_items = load_order_items()
    books = load_books()
    purchased_book_ids = set(oi['book_id'] for oi in order_items)
    purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]

    error = None

    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id'))
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review_text', '').strip()
        except Exception:
            book_id = None
            rating = None
            review_text = ''

        # Validate
        if not book_id or rating not in range(1, 6) or not review_text:
            error = 'Invalid input. Please fill all fields correctly.'
        else:
            # Add review
            reviews = load_reviews()
            new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
            today_str = datetime.today().strftime('%Y-%m-%d')
            new_review = {
                'review_id': new_review_id,
                'book_id': book_id,
                'customer_name': 'Anonymous',  # No customer login info
                'rating': rating,
                'review_text': review_text,
                'review_date': today_str
            }
            reviews.append(new_review)
            save_reviews(reviews)
            # Redirect to reviews page
            return redirect(url_for('reviews_page'))

    return render_template('write_review.html', purchased_books=purchased_books)


# Route 11 - Bestsellers Page
@app.route('/bestsellers', methods=['GET'])
def bestsellers_page():
    selected_period = request.args.get('period', 'This Month')
    bestsellers_raw = load_bestsellers()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    filtered_bestsellers = [bs for bs in bestsellers_raw if bs['period'] == selected_period]

    bs_list = []
    for bs in filtered_bestsellers:
        book = books_map.get(bs['book_id'])
        if book:
            bs_list.append({
                'book_id': bs['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period']
            })

    return render_template('bestsellers.html', bestsellers=bs_list, selected_period=selected_period)


if __name__ == '__main__':
    app.run(debug=True)