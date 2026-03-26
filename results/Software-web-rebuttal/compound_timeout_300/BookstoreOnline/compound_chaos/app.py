from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for reading and writing pipe-delimited files

def read_pipe_file(filepath, num_fields):
    records = []
    if not os.path.exists(filepath):
        return records
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # Pad parts if line has less fields (just in case)
            if len(parts) < num_fields:
                parts += [''] * (num_fields - len(parts))
            records.append(parts[:num_fields])
    return records


def write_pipe_file(filepath, records):
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            record = [str(r) if r is not None else '' for r in record]
            f.write('|'.join(record) + '\n')


def parse_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def get_today_date_str():
    return datetime.today().strftime('%Y-%m-%d')


# Section 3: Data related helpers

# Books data
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
CART_FILE = os.path.join(DATA_DIR, 'cart.txt')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.txt')
ORDER_ITEMS_FILE = os.path.join(DATA_DIR, 'order_items.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
BESTSELLERS_FILE = os.path.join(DATA_DIR, 'bestsellers.txt')


# Load all books as list of dicts
# Fields: book_id|title|author|isbn|category|price|stock|description
def load_books():
    books = []
    raw = read_pipe_file(BOOKS_FILE, 8)
    for parts in raw:
        try:
            book = {
                'book_id': parse_int(parts[0]),
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'category': parts[4],
                'price': parse_float(parts[5]),
                'stock': parse_int(parts[6]),
                'description': parts[7]
            }
            books.append(book)
        except Exception:
            continue
    return books


def load_categories():
    categories = []
    raw = read_pipe_file(CATEGORIES_FILE, 3)
    for parts in raw:
        try:
            cat = {
                'category_id': parse_int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(cat)
        except Exception:
            continue
    return categories


def load_cart():
    cart_items = []
    raw = read_pipe_file(CART_FILE, 4)
    for parts in raw:
        try:
            item = {
                'cart_id': parse_int(parts[0]),
                'book_id': parse_int(parts[1]),
                'quantity': parse_int(parts[2]),
                'added_date': parts[3]
            }
            cart_items.append(item)
        except Exception:
            continue
    return cart_items


def write_cart(cart_items):
    records = []
    for item in cart_items:
        records.append([
            item['cart_id'],
            item['book_id'],
            item['quantity'],
            item['added_date']
        ])
    write_pipe_file(CART_FILE, records)


def load_orders():
    orders = []
    raw = read_pipe_file(ORDERS_FILE, 6)
    for parts in raw:
        try:
            order = {
                'order_id': parse_int(parts[0]),
                'customer_name': parts[1],
                'order_date': parts[2],
                'total_amount': parse_float(parts[3]),
                'status': parts[4],
                'shipping_address': parts[5]
            }
            orders.append(order)
        except Exception:
            continue
    return orders


def write_orders(orders):
    records = []
    for order in orders:
        records.append([
            order['order_id'],
            order['customer_name'],
            order['order_date'],
            order['total_amount'],
            order['status'],
            order['shipping_address']
        ])
    write_pipe_file(ORDERS_FILE, records)


def load_order_items():
    order_items = []
    raw = read_pipe_file(ORDER_ITEMS_FILE, 5)
    for parts in raw:
        try:
            oi = {
                'order_item_id': parse_int(parts[0]),
                'order_id': parse_int(parts[1]),
                'book_id': parse_int(parts[2]),
                'quantity': parse_int(parts[3]),
                'price': parse_float(parts[4])
            }
            order_items.append(oi)
        except Exception:
            continue
    return order_items


def write_order_items(order_items):
    records = []
    for oi in order_items:
        records.append([
            oi['order_item_id'],
            oi['order_id'],
            oi['book_id'],
            oi['quantity'],
            oi['price']
        ])
    write_pipe_file(ORDER_ITEMS_FILE, records)


def load_reviews():
    reviews = []
    raw = read_pipe_file(REVIEWS_FILE, 6)
    for parts in raw:
        try:
            review = {
                'review_id': parse_int(parts[0]),
                'book_id': parse_int(parts[1]),
                'customer_name': parts[2],
                'rating': parse_int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
            reviews.append(review)
        except Exception:
            continue
    return reviews


def write_reviews(reviews):
    records = []
    for rev in reviews:
        records.append([
            rev['review_id'],
            rev['book_id'],
            rev['customer_name'],
            rev['rating'],
            rev['review_text'],
            rev['review_date']
        ])
    write_pipe_file(REVIEWS_FILE, records)


def load_bestsellers():
    bestsellers = []
    raw = read_pipe_file(BESTSELLERS_FILE, 3)
    for parts in raw:
        try:
            bs = {
                'book_id': parse_int(parts[0]),
                'sales_count': parse_int(parts[1]),
                'period': parts[2]
            }
            bestsellers.append(bs)
        except Exception:
            continue
    return bestsellers


# Route implementations

# 1. Root route - redirect to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'), code=302)


# 2. Dashboard
@app.route('/dashboard')
def dashboard():
    books = load_books()
    bestsellers_raw = load_bestsellers()

    # Featured books: top 5 books with stock > 0 (arbitrary choice)
    featured_books = []
    count = 0
    for book in books:
        if book['stock'] > 0:
            featured_books.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'price': book['price']
            })
            count += 1
            if count >= 5:
                break

    # Get all time bestsellers for dashboard display (maybe top 5)
    all_time_bs = [bs for bs in bestsellers_raw if bs['period'] == 'All Time']
    # Sort descending by sales_count
    all_time_bs_sorted = sorted(all_time_bs, key=lambda x: x['sales_count'], reverse=True)[:5]

    # Prepare bestsellers info with title and author
    bestsellers = []
    # Create mapping from book_id to book
    book_map = {b['book_id']: b for b in books}
    for bs in all_time_bs_sorted:
        b = book_map.get(bs['book_id'])
        if b:
            bestsellers.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'sales_count': bs['sales_count']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


# 3. Catalog
@app.route('/catalog')
def catalog():
    books = load_books()
    categories = load_categories()

    # Get query params
    search_query = request.args.get('search', '').strip() or None
    selected_category = request.args.get('category', '').strip() or None

    filtered_books = books

    if selected_category:
        filtered_books = [b for b in filtered_books if b['category'].lower() == selected_category.lower()]

    if search_query:
        sq_lower = search_query.lower()
        filtered_books = [b for b in filtered_books if (sq_lower in b['title'].lower()) or (sq_lower in b['author'].lower()) or (sq_lower in b['isbn'].lower())]

    # Prepare minimal book info
    books_info = []
    for b in filtered_books:
        books_info.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    # Provide category_names list
    categories_info = []
    for c in categories:
        categories_info.append({
            'category_id': c['category_id'],
            'category_name': c['category_name']
        })

    return render_template('catalog.html', books=books_info, categories=categories_info, selected_category=selected_category, search_query=search_query)


# 4. Book Details page
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = load_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = b
            break

    if not book:
        # Book not found - could abort 404
        return 'Book not found', 404

    reviews_all = load_reviews()
    reviews_for_book = []
    for r in reviews_all:
        if r['book_id'] == book_id:
            reviews_for_book.append({
                'review_id': r['review_id'],
                'customer_name': r['customer_name'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    if request.method == 'POST':
        # Processing add to cart
        # The spec says triggered by 'add-to-cart-button' (button)
        # We expect the form to submit with 'book_id' in form data

        # Validate book_id matches url book_id
        form_book_id = request.form.get('book_id')
        if form_book_id and int(form_book_id) == book_id:
            cart_items = load_cart()
            # Check if item exists
            found = False
            for item in cart_items:
                if item['book_id'] == book_id:
                    # update quantity +1
                    item['quantity'] += 1
                    found = True
                    break
            if not found:
                # Generate new cart_id; one more than max or 1 if empty
                next_cart_id = 1
                if cart_items:
                    next_cart_id = max(i['cart_id'] for i in cart_items) + 1
                cart_items.append({
                    'cart_id': next_cart_id,
                    'book_id': book_id,
                    'quantity': 1,
                    'added_date': get_today_date_str()
                })
            write_cart(cart_items)
            # Redirect to same page to avoid form resubmission
            return redirect(url_for('book_details', book_id=book_id))

    return render_template('book_details.html', book=book, reviews=reviews_for_book)


# 5. Shopping Cart page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    books = load_books()
    cart_items_raw = load_cart()
    book_map = {b['book_id']: b for b in books}

    if request.method == 'POST':
        # POST handling - update quantities or remove items
        cart_items = load_cart()
        # Process removal first
        to_remove = set()

        for key in request.form.keys():
            if key.startswith('remove_'):
                try:
                    remove_id = int(key[len('remove_'):])
                    to_remove.add(remove_id)
                except Exception:
                    continue

        cart_items = [item for item in cart_items if item['cart_id'] not in to_remove]

        # Process quantity updates
        for key in request.form.keys():
            if key.startswith('quantity_'):
                try:
                    cart_id = int(key[len('quantity_'):])
                    quantity_val = int(request.form.get(key, '1'))
                    if quantity_val < 1:
                        quantity_val = 1
                    # Update quantity if cart_id found
                    for item in cart_items:
                        if item['cart_id'] == cart_id:
                            item['quantity'] = quantity_val
                            break
                except Exception:
                    continue

        write_cart(cart_items)
        return redirect(url_for('cart'))

    # Prepare context for GET
    cart_items = []
    total_amount = 0.0
    for item in cart_items_raw:
        b = book_map.get(item['book_id'])
        if b:
            quantity = item['quantity']
            price = b['price']
            subtotal = round(quantity * price, 2)
            total_amount += subtotal
            cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': b['book_id'],
                'title': b['title'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    total_amount = round(total_amount, 2)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# 6. Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    books = load_books()
    cart_items_raw = load_cart()
    book_map = {b['book_id']: b for b in books}

    # Build cart_items for template
    cart_items = []
    total_amount = 0.0
    for item in cart_items_raw:
        b = book_map.get(item['book_id'])
        if b:
            quantity = item['quantity']
            price = b['price']
            subtotal = round(quantity * price, 2)
            total_amount += subtotal
            cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': b['book_id'],
                'title': b['title'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    total_amount = round(total_amount, 2)

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        # Validate inputs
        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            # Bad request or re-render with error - for simplicity redirect to checkout
            return redirect(url_for('checkout'))

        if not cart_items:
            # No items in cart - do nothing or redirect
            return redirect(url_for('cart'))

        # Load existing orders to find next order_id
        orders = load_orders()
        next_order_id = 1
        if orders:
            next_order_id = max(o['order_id'] for o in orders) + 1

        order_date = get_today_date_str()

        # Create the new order
        new_order = {
            'order_id': next_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)

        # Write orders
        write_orders(orders)

        # Add order items
        order_items = load_order_items()
        next_order_item_id = 1
        if order_items:
            next_order_item_id = max(oi['order_item_id'] for oi in order_items) + 1

        for item in cart_items:
            order_items.append({
                'order_item_id': next_order_item_id,
                'order_id': next_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['price']
            })
            next_order_item_id += 1

        # Save order items
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        # Redirect to order history
        return redirect(url_for('order_history'))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)


# 7. Order History Page
@app.route('/order_history')
def order_history():
    orders = load_orders()
    status_filter = request.args.get('status', 'All')

    if status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter.lower()]
    else:
        filtered_orders = orders

    return render_template('order_history.html', orders=filtered_orders, status_filter=status_filter)


# 8. Order Details Page (Optional)
@app.route('/order/<int:order_id>')
def order_details(order_id):
    orders = load_orders()
    order = None
    for o in orders:
        if o['order_id'] == order_id:
            order = o
            break
    if not order:
        return 'Order not found', 404

    order_items_all = load_order_items()
    books = load_books()
    book_map = {b['book_id']: b for b in books}

    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            b = book_map.get(oi['book_id'])
            if b:
                quantity = oi['quantity']
                price = oi['price']
                subtotal = round(quantity * price, 2)
                order_items.append({
                    'order_item_id': oi['order_item_id'],
                    'book_id': oi['book_id'],
                    'title': b['title'],
                    'quantity': quantity,
                    'price': price,
                    'subtotal': subtotal
                })

    return render_template('order_details.html', order=order, order_items=order_items)


# 9. Reviews Page
@app.route('/reviews')
def reviews():
    reviews_all = load_reviews()
    books = load_books()
    book_map = {b['book_id']: b for b in books}

    rating_filter = request.args.get('rating', 'All')

    filtered_reviews = []
    for r in reviews_all:
        if rating_filter == 'All' or str(r['rating']) == rating_filter:
            book = book_map.get(r['book_id'])
            book_title = book['title'] if book else 'Unknown'
            filtered_reviews.append({
                'review_id': r['review_id'],
                'book_title': book_title,
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)


# 10. Write Review Page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    orders = load_orders()
    order_items = load_order_items()
    books = load_books()

    # We want purchasable_books - unique books from past orders
    purchased_book_ids = set(oi['book_id'] for oi in order_items)
    purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]

    # Remove duplicates if any
    unique_books = {}
    for b in purchased_books:
        unique_books[b['book_id']] = b
    purchasable_books = list(unique_books.values())

    if request.method == 'POST':
        book_id_str = request.form.get('book_id')
        rating_str = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()
        customer_name = request.form.get('customer_name', '').strip()

        # Validate inputs
        try:
            book_id = int(book_id_str)
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError('Rating out of range')
        except Exception:
            return redirect(url_for('write_review'))

        if not customer_name or not review_text:
            return redirect(url_for('write_review'))

        # Validate book_id is in purchasable_books
        if book_id not in unique_books:
            return redirect(url_for('write_review'))

        # Generate new review_id
        reviews_all = load_reviews()
        next_review_id = 1
        if reviews_all:
            next_review_id = max(r['review_id'] for r in reviews_all) + 1

        review_date = get_today_date_str()

        new_review = {
            'review_id': next_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

        reviews_all.append(new_review)
        write_reviews(reviews_all)

        return redirect(url_for('reviews'))

    return render_template('write_review.html', purchasable_books=purchasable_books)


# 11. Bestsellers Page
@app.route('/bestsellers')
def bestsellers():
    time_period = request.args.get('time_period', 'All Time')
    bestsellers_all = load_bestsellers()
    books = load_books()
    book_map = {b['book_id']: b for b in books}

    filtered_bs = [bs for bs in bestsellers_all if bs['period'] == time_period]

    # Sort descending by sales_count
    filtered_bs_sorted = sorted(filtered_bs, key=lambda x: x['sales_count'], reverse=True)

    bestsellers = []
    for bs in filtered_bs_sorted:
        b = book_map.get(bs['book_id'])
        if b:
            bestsellers.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'sales_count': bs['sales_count']
            })

    return render_template('bestsellers.html', bestsellers=bestsellers, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
