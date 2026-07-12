from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
BOOKS_FILE = 'data/books.txt'
CATEGORIES_FILE = 'data/categories.txt'
CART_FILE = 'data/cart.txt'
ORDERS_FILE = 'data/orders.txt'
ORDER_ITEMS_FILE = 'data/order_items.txt'
REVIEWS_FILE = 'data/reviews.txt'
BESTSELLERS_FILE = 'data/bestsellers.txt'

# Helper functions for reading and writing data with pipe-delimited format

def read_books():
    books = []
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 8:
                continue
            try:
                book = {
                    'book_id': int(fields[0]),
                    'title': fields[1],
                    'author': fields[2],
                    'isbn': fields[3],
                    'category': fields[4],
                    'price': float(fields[5]),
                    'stock': int(fields[6]),
                    'description': fields[7],
                }
                books.append(book)
            except:
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
            fields = line.split('|')
            if len(fields) != 3:
                continue
            try:
                category = {
                    'category_id': int(fields[0]),
                    'category_name': fields[1],
                    'description': fields[2],
                }
                categories.append(category)
            except:
                continue
    return categories


def read_cart():
    cart_items = []
    if not os.path.exists(CART_FILE):
        return cart_items
    with open(CART_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 4:
                continue
            try:
                item = {
                    'cart_id': int(fields[0]),
                    'book_id': int(fields[1]),
                    'quantity': int(fields[2]),
                    'added_date': fields[3],
                }
                cart_items.append(item)
            except:
                continue
    return cart_items


def write_cart(cart_items):
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except:
        return False


def read_orders():
    orders = []
    if not os.path.exists(ORDERS_FILE):
        return orders
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                order = {
                    'order_id': int(fields[0]),
                    'customer_name': fields[1],
                    'order_date': fields[2],
                    'total_amount': float(fields[3]),
                    'status': fields[4],
                    'shipping_address': fields[5],
                }
                orders.append(order)
            except:
                continue
    return orders


def write_orders(orders):
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}\n"
                f.write(line)
        return True
    except:
        return False


def read_order_items():
    order_items = []
    if not os.path.exists(ORDER_ITEMS_FILE):
        return order_items
    with open(ORDER_ITEMS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields=line.split('|')
            if len(fields) != 5:
                continue
            try:
                item = {
                    'order_item_id': int(fields[0]),
                    'order_id': int(fields[1]),
                    'book_id': int(fields[2]),
                    'quantity': int(fields[3]),
                    'price': float(fields[4]),
                }
                order_items.append(item)
            except:
                continue
    return order_items


def write_order_items(order_items):
    try:
        with open(ORDER_ITEMS_FILE, 'w', encoding='utf-8') as f:
            for item in order_items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}\n"
                f.write(line)
        return True
    except:
        return False


def read_reviews():
    reviews = []
    if not os.path.exists(REVIEWS_FILE):
        return reviews
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields=line.split('|')
            if len(fields) != 6:
                continue
            try:
                review = {
                    'review_id': int(fields[0]),
                    'book_id': int(fields[1]),
                    'customer_name': fields[2],
                    'rating': int(fields[3]),
                    'review_text': fields[4],
                    'review_date': fields[5],
                }
                reviews.append(review)
            except:
                continue
    return reviews


def write_reviews(reviews):
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for review in reviews:
                line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
                f.write(line)
        return True
    except:
        return False


def read_bestsellers():
    bestsellers = []
    if not os.path.exists(BESTSELLERS_FILE):
        return bestsellers
    with open(BESTSELLERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            fields=line.split('|')
            if len(fields) != 3:
                continue
            try:
                bs = {
                    'book_id': int(fields[0]),
                    'sales_count': int(fields[1]),
                    'period': fields[2],
                }
                bestsellers.append(bs)
            except:
                continue
    return bestsellers


# Route 1: Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route 2: Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    books = read_books()
    bestsellers = read_bestsellers()
    # Featured books: we can define as top 5 by stock > 0, else top 5 arbitrary
    featured_books = [b for b in books if b['stock'] > 0][:5]
    # bestsellers for any period - ignoring period param here, use all
    bestsellers_books = []
    if bestsellers:
        # Find books matching any bestseller book_id
        bestseller_book_ids = {bs['book_id'] for bs in bestsellers}
        bestsellers_books = [b for b in books if b['book_id'] in bestseller_book_ids]

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers_books)


# Route 3: Book Catalog Page
@app.route('/catalog')
def catalog_page():
    books = read_books()
    categories = read_categories()

    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('search', '').strip().lower()

    filtered_books = books

    if selected_category:
        filtered_books = [b for b in filtered_books if b['category'].lower() == selected_category.lower()]

    if search_query:
        filtered_books = [b for b in filtered_books if search_query in b['title'].lower() or search_query in b['author'].lower()]

    return render_template('catalog.html', books=filtered_books, categories=categories, selected_category=selected_category, search_query=search_query)


# Route 4: Book Details Page
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details_page(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        # Handle add to cart
        quantity_str = request.form.get('quantity', '1').strip()
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1

        # Read current cart
        cart_items = read_cart()

        # Check if book already in cart, increment quantity
        existing_item = next((item for item in cart_items if item['book_id'] == book_id), None)
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            new_cart_id = max([item['cart_id'] for item in cart_items], default=0) + 1
            today_str = datetime.date.today().isoformat()
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_str
            })

        success_write = write_cart(cart_items)

        if not success_write:
            return "Error saving cart", 500

        return redirect(url_for('shopping_cart_page'))

    # GET: show book details + reviews
    reviews = [r for r in read_reviews() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=reviews)


# Route 5: Shopping Cart Page
@app.route('/cart')
def shopping_cart_page():
    books = read_books()
    cart_items_raw = read_cart()

    cart_items = []
    total_amount = 0.0

    for item in cart_items_raw:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        subtotal = round(book['price'] * item['quantity'], 2)
        total_amount += subtotal
        cart_items.append({
            'item_id': item['cart_id'],
            'book': book,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    total_amount = round(total_amount, 2)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# POST: Update Quantity
@app.route('/cart/update_quantity', methods=['POST'])
def update_cart_quantity():
    item_id_str = request.form.get('item_id', '').strip()
    quantity_str = request.form.get('quantity', '').strip()

    try:
        item_id = int(item_id_str)
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except:
        return redirect(url_for('shopping_cart_page'))

    cart_items = read_cart()
    updated = False

    for item in cart_items:
        if item['cart_id'] == item_id:
            item['quantity'] = quantity
            updated = True
            break

    if updated:
        write_cart(cart_items)

    return redirect(url_for('shopping_cart_page'))


# POST: Remove Item
@app.route('/cart/remove_item', methods=['POST'])
def remove_cart_item():
    item_id_str = request.form.get('item_id', '').strip()
    try:
        item_id = int(item_id_str)
    except:
        return redirect(url_for('shopping_cart_page'))

    cart_items = read_cart()
    cart_items = [item for item in cart_items if item['cart_id'] != item_id]
    write_cart(cart_items)

    return redirect(url_for('shopping_cart_page'))


# Route 6: Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    books = read_books()
    cart_items_raw = read_cart()

    cart_items = []
    total_amount = 0.0

    for item in cart_items_raw:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        subtotal = round(book['price'] * item['quantity'], 2)
        total_amount += subtotal
        cart_items.append({
            'item_id': item['cart_id'],
            'book': book,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    total_amount = round(total_amount, 2)

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            # Could re-render with error but spec not explicit
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

        if not cart_items:
            # No items to checkout
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

        # Create new order
        orders = read_orders()
        order_items = read_order_items()

        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.date.today().isoformat()

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }

        orders.append(new_order)

        # Append order items
        next_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        for ci in cart_items:
            order_item = {
                'order_item_id': next_order_item_id,
                'order_id': new_order_id,
                'book_id': ci['book']['book_id'],
                'quantity': ci['quantity'],
                'price': ci['book']['price'],
            }
            order_items.append(order_item)
            next_order_item_id += 1

        write_orders(orders)
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('order_history_page'))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)


# Route 7: Order History Page
@app.route('/orders')
def order_history_page():
    orders = read_orders()
    status_filter = request.args.get('status', 'All')

    if status_filter != 'All':
        orders = [o for o in orders if o['status'].lower() == status_filter.lower()]

    return render_template('orders.html', orders=orders, status_filter=status_filter)


# Route 8: Order Details Page
@app.route('/order/<int:order_id>')
def order_details_page(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items_all = read_order_items()
    books = read_books()
    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book:
                order_items.append({
                    'order_item_id': oi['order_item_id'],
                    'book': book,
                    'quantity': oi['quantity'],
                    'price': oi['price'],
                })

    return render_template('order_details.html', order=order, order_items=order_items)


# Route 9: Reviews Page
@app.route('/reviews')
def reviews_page():
    reviews = read_reviews()
    rating_filter = request.args.get('rating', 'All')

    if rating_filter != 'All':
        if rating_filter.endswith(' stars'):
            try:
                rating_val = int(rating_filter.split()[0])
                reviews = [r for r in reviews if r['rating'] == rating_val]
            except:
                pass

    return render_template('reviews.html', reviews=reviews, rating_filter=rating_filter)


# Route 10: Write Review Page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    books = read_books()
    orders = read_orders()
    order_items = read_order_items()

    # Determine purchased_books by orders and order_items
    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]

    if request.method == 'POST':
        book_id_str = request.form.get('book_id', '').strip() or request.form.get('select-book', '').strip()
        rating_str = request.form.get('rating', '').strip() or request.form.get('rating-select', '').strip()
        review_text = request.form.get('review_text', '').strip() or request.form.get('review-text', '').strip()

        try:
            book_id = int(book_id_str)
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError()
        except:
            # Invalid input, re-render page
            return render_template('write_review.html', purchased_books=purchased_books)

        # For simplicity, save the customer_name as Unknown or anonymous
        customer_name = 'Anonymous'

        reviews = read_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
        review_date = datetime.date.today().isoformat()

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

    return render_template('write_review.html', purchased_books=purchased_books)


# Route 11: Bestsellers Page
@app.route('/bestsellers')
def bestsellers_page():
    time_period = request.args.get('period', 'This Month')
    bestsellers = read_bestsellers()
    books = read_books()

    filtered_bestsellers = [bs for bs in bestsellers if bs['period'] == time_period]

    # Sort descending by sales_count
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)

    # Compose list of bestseller book dicts
    bestseller_books = []
    book_id_set = set([bs['book_id'] for bs in filtered_bestsellers])
    for bs in filtered_bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            bestseller_books.append(book)

    return render_template('bestsellers.html', bestsellers=bestseller_books, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
