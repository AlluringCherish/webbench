from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for file operations

def read_pipe_delimited_file(filepath, fields_count):
    """
    Read a pipe-delimited file and return list of fields_count-tuples.
    Return empty list if file not exists.
    """
    results = []
    if not os.path.exists(filepath):
        return results
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # Defensive: if less fields, skip
            if len(parts) < fields_count:
                continue
            # Truncate extra fields if any
            results.append(parts[:fields_count])
    return results


def write_pipe_delimited_file(filepath, rows):
    """
    rows: list of lists or tuples, each element to be converted to str
    Overwrites file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write('|'.join(str(x) for x in row) + '\n')


def get_books():
    # Fields: book_id|title|author|isbn|category|price|stock|description
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'books.txt'), 8)
    books = []
    for r in raw:
        try:
            book = {
                'book_id': int(r[0]),
                'title': r[1],
                'author': r[2],
                'isbn': r[3],
                'category': r[4],
                'price': float(r[5]),
                'stock': int(r[6]),
                'description': r[7]
            }
            books.append(book)
        except Exception:
            continue
    return books


def get_categories():
    # Fields: category_id|category_name|description
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'categories.txt'), 3)
    categories = []
    for r in raw:
        try:
            c = {
                'category_id': int(r[0]),
                'category_name': r[1],
                'description': r[2]
            }
            categories.append(c)
        except Exception:
            continue
    return categories


def get_cart_items():
    # Fields: cart_id|book_id|quantity|added_date
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'cart.txt'), 4)
    cart = []
    for r in raw:
        try:
            item = {
                'cart_id': int(r[0]),
                'book_id': int(r[1]),
                'quantity': int(r[2]),
                'added_date': r[3]
            }
            cart.append(item)
        except Exception:
            continue
    return cart


def save_cart_items(cart_items):
    # cart_items list of dicts
    rows = []
    for item in cart_items:
        rows.append([
            item['cart_id'],
            item['book_id'],
            item['quantity'],
            item['added_date']
        ])
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'cart.txt'), rows)


def get_orders():
    # Fields: order_id|customer_name|order_date|total_amount|status|shipping_address
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'orders.txt'), 6)
    orders = []
    for r in raw:
        try:
            order = {
                'order_id': int(r[0]),
                'customer_name': r[1],
                'order_date': r[2],
                'total_amount': float(r[3]),
                'status': r[4],
                'shipping_address': r[5]
            }
            orders.append(order)
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
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'orders.txt'), rows)


def get_order_items():
    # Fields: order_item_id|order_id|book_id|quantity|price
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'order_items.txt'), 5)
    order_items = []
    for r in raw:
        try:
            oi = {
                'order_item_id': int(r[0]),
                'order_id': int(r[1]),
                'book_id': int(r[2]),
                'quantity': int(r[3]),
                'price': float(r[4])
            }
            order_items.append(oi)
        except Exception:
            continue
    return order_items


def save_order_items(order_items):
    rows = []
    for oi in order_items:
        rows.append([
            oi['order_item_id'],
            oi['order_id'],
            oi['book_id'],
            oi['quantity'],
            oi['price']
        ])
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'order_items.txt'), rows)


def get_reviews():
    # Fields: review_id|book_id|customer_name|rating|review_text|review_date
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'reviews.txt'), 6)
    reviews = []
    for r in raw:
        try:
            review = {
                'review_id': int(r[0]),
                'book_id': int(r[1]),
                'customer_name': r[2],
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            }
            reviews.append(review)
        except Exception:
            continue
    return reviews


def save_reviews(reviews):
    rows = []
    for rv in reviews:
        rows.append([
            rv['review_id'],
            rv['book_id'],
            rv['customer_name'],
            rv['rating'],
            rv['review_text'],
            rv['review_date']
        ])
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'reviews.txt'), rows)


def get_bestsellers():
    # Fields: book_id|sales_count|period
    raw = read_pipe_delimited_file(os.path.join(DATA_DIR, 'bestsellers.txt'), 3)
    bestsellers = []
    for r in raw:
        try:
            b = {
                'book_id': int(r[0]),
                'sales_count': int(r[1]),
                'period': r[2]
            }
            bestsellers.append(b)
        except Exception:
            continue
    return bestsellers


### Routes Implementation ###

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Display featured_books and bestsellers
    books = get_books()
    bestsellers_all = get_bestsellers()

    # Define featured_books as books where stock > 20 (arbitrary simple criteria)
    featured_books = []
    for b in books:
        if b['stock'] > 20:
            featured_books.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'price': b['price']
            })

    # Prepare bestsellers for dashboard: period All Time
    dashboard_bestsellers = []
    # Filter bestsellers for period "All Time"
    for bs in bestsellers_all:
        if bs['period'].lower() == 'all time':
            # find book
            b = next((bk for bk in books if bk['book_id'] == bs['book_id']), None)
            if b:
                dashboard_bestsellers.append({
                    'book_id': b['book_id'],
                    'title': b['title'],
                    'author': b['author'],
                    'sales_count': bs['sales_count']
                })
    # fallback if none found, show all period bestsellers top 5
    if not dashboard_bestsellers:
        # sort all desc sales_count
        sorted_bs = sorted(bestsellers_all, key=lambda x: x['sales_count'], reverse=True)[:5]
        for bs in sorted_bs:
            b = next((bk for bk in books if bk['book_id'] == bs['book_id']), None)
            if b:
                dashboard_bestsellers.append({
                    'book_id': b['book_id'],
                    'title': b['title'],
                    'author': b['author'],
                    'sales_count': bs['sales_count']
                })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=dashboard_bestsellers)


@app.route('/catalog')
def catalog_page():
    categories = get_categories()
    books = get_books()

    # For categories to list only category_id and category_name
    simple_categories = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    # For books list only book_id, title, author, price
    simple_books = [{'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'price': b['price']} for b in books]

    return render_template('catalog.html', categories=simple_categories, books=simple_books)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = get_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    reviews_all = get_reviews()
    # Filter reviews for this book
    book_reviews = []
    for rv in reviews_all:
        if rv['book_id'] == book_id:
            book_reviews.append({
                'review_id': rv['review_id'],
                'customer_name': rv['customer_name'],
                'rating': rv['rating'],
                'review_text': rv['review_text'],
                'review_date': rv['review_date']
            })

    if request.method == 'POST':
        # Handle add to cart
        if request.form.get('add_to_cart_button') is not None:
            cart_items = get_cart_items()

            # Check if already in cart
            existing_item = next((ci for ci in cart_items if ci['book_id'] == book_id), None)
            if existing_item:
                existing_item['quantity'] += 1
            else:
                # New entry
                max_id = max((ci['cart_id'] for ci in cart_items), default=0)
                new_cart_id = max_id + 1
                added_date = datetime.date.today().isoformat()
                cart_items.append({
                    'cart_id': new_cart_id,
                    'book_id': book_id,
                    'quantity': 1,
                    'added_date': added_date
                })
            save_cart_items(cart_items)
            # Redirect back to book details page
            return redirect(url_for('book_details', book_id=book_id))

    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = get_cart_items()
    books = get_books()

    if request.method == 'POST':
        # Check for removal first
        remove_prefix = 'remove-item-button-'
        update_prefix = 'update-quantity-'

        # Try to remove items
        removed = False
        for key in request.form:
            if key.startswith(remove_prefix):
                # Extract cart_id
                try:
                    cart_id = int(key[len(remove_prefix):])
                    cart_items = [ci for ci in cart_items if ci['cart_id'] != cart_id]
                    removed = True
                    break
                except Exception:
                    pass
        if removed:
            save_cart_items(cart_items)
            return redirect(url_for('shopping_cart'))

        # Update quantities
        updated = False
        for key in request.form:
            if key.startswith(update_prefix):
                try:
                    cart_id = int(key[len(update_prefix):])
                    new_quantity_str = request.form.get(key, '').strip()
                    new_quantity = int(new_quantity_str)
                    if new_quantity <= 0:
                        # Remove the item
                        cart_items = [ci for ci in cart_items if ci['cart_id'] != cart_id]
                    else:
                        for ci in cart_items:
                            if ci['cart_id'] == cart_id:
                                ci['quantity'] = new_quantity
                    updated = True
                except Exception:
                    continue
        if updated:
            save_cart_items(cart_items)
            return redirect(url_for('shopping_cart'))

    # Compose cart_items for template
    display_items = []
    total_amount = 0.0
    for ci in cart_items:
        book = next((b for b in books if b['book_id'] == ci['book_id']), None)
        if not book:
            continue
        price = book['price']
        qty = ci['quantity']
        subtotal = price * qty
        total_amount += subtotal
        display_items.append({
            'cart_id': ci['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': qty,
            'price': price,
            'subtotal': subtotal
        })

    total_amount = round(total_amount, 2)
    return render_template('cart.html', cart_items=display_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            # Simple validation fail, render back with error (Could expand with flash messages)
            return render_template('checkout.html')

        cart_items = get_cart_items()
        books = get_books()

        if not cart_items:
            # Nothing in cart
            return render_template('checkout.html')

        # Calculate total amount
        total_amount = 0.0
        for ci in cart_items:
            b = next((bk for bk in books if bk['book_id'] == ci['book_id']), None)
            if b:
                total_amount += b['price'] * ci['quantity']

        total_amount = round(total_amount, 2)

        orders = get_orders()
        order_items = get_order_items()

        # New order_id
        max_order_id = max((o['order_id'] for o in orders), default=0)
        new_order_id = max_order_id + 1

        # Create new order
        today_date = datetime.date.today().isoformat()
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)

        # Add order items
        max_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0)
        order_items_to_add = []
        for ci in cart_items:
            b = next((bk for bk in books if bk['book_id'] == ci['book_id']), None)
            if b:
                max_order_item_id += 1
                oi = {
                    'order_item_id': max_order_item_id,
                    'order_id': new_order_id,
                    'book_id': ci['book_id'],
                    'quantity': ci['quantity'],
                    'price': b['price']
                }
                order_items.append(oi)

        # Save all
        save_orders(orders)
        save_order_items(order_items)

        # Clear cart
        save_cart_items([])

        return redirect(url_for('order_history'))

    # GET
    return render_template('checkout.html')


@app.route('/orders')
def order_history():
    status_filter = request.args.get('status_filter', 'All')

    orders = get_orders()

    if status_filter != 'All':
        orders = [o for o in orders if o['status'].lower() == status_filter.lower()]

    return render_template('orders.html', orders=orders, status_filter=status_filter)


@app.route('/orders/<int:order_id>')
def order_details(order_id):
    orders = get_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items_all = get_order_items()
    books = get_books()

    # Filter order items
    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book:
                order_items.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('order_details.html', order=order, order_items=order_items)


@app.route('/reviews')
def reviews_page():
    rating_filter = request.args.get('rating_filter', 'All')

    reviews_all = get_reviews()
    books = get_books()

    filtered_reviews = []
    for rv in reviews_all:
        if rating_filter != 'All':
            try:
                rfilter = int(rating_filter)
                if rv['rating'] != rfilter:
                    continue
            except Exception:
                # If invalid filter, show all
                pass
        book = next((b for b in books if b['book_id'] == rv['book_id']), None)
        if book:
            filtered_reviews.append({
                'review_id': rv['review_id'],
                'book_title': book['title'],
                'rating': rv['rating'],
                'review_text': rv['review_text'],
                'review_date': rv['review_date']
            })

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    # Purchased books assumed as all books for simplicity (spec doesn't specify user info)
    books = get_books()
    purchased_books = [{'book_id': b['book_id'], 'title': b['title']} for b in books]

    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id'))
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review_text', '').strip()
            # customer_name not specified, assume anonymous
            customer_name = 'Anonymous'

            if rating < 1 or rating > 5 or not review_text or book_id not in [b['book_id'] for b in books]:
                # Invalid input
                return render_template('write_review.html', purchased_books=purchased_books)

            reviews = get_reviews()
            max_review_id = max((rv['review_id'] for rv in reviews), default=0)
            new_review_id = max_review_id + 1
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
            save_reviews(reviews)

            return redirect(url_for('reviews_page'))
        except Exception:
            # On failure, just reload page
            return render_template('write_review.html', purchased_books=purchased_books)

    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers')
def bestsellers_page():
    period_filter = request.args.get('period_filter', 'All Time')

    bestsellers_all = get_bestsellers()
    books = get_books()

    filtered_bestsellers = []
    if period_filter == 'All Time':
        filtered_bestsellers = [bs for bs in bestsellers_all if bs['period'].lower() == 'all time']
    elif period_filter == 'This Week':
        filtered_bestsellers = [bs for bs in bestsellers_all if bs['period'].lower() == 'this week']
    elif period_filter == 'This Month':
        filtered_bestsellers = [bs for bs in bestsellers_all if bs['period'].lower() == 'this month']
    else:
        # default show all
        filtered_bestsellers = bestsellers_all

    # Sort descending sales_count
    filtered_bestsellers = sorted(filtered_bestsellers, key=lambda x: x['sales_count'], reverse=True)

    # Prepare list with book details
    result = []
    for bs in filtered_bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            result.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period']
            })

    return render_template('bestsellers.html', bestsellers=result, period_filter=period_filter)


if __name__ == '__main__':
    app.run(debug=True)
