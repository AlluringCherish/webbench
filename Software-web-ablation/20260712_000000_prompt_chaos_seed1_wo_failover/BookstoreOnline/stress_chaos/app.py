from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read and write data files based on schemas

def parse_books():
    books_path = os.path.join(DATA_DIR, 'books.txt')
    books = []
    if os.path.exists(books_path):
        with open(books_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
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
                except Exception:
                    continue
    return books


def parse_categories():
    categories_path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    if os.path.exists(categories_path):
        with open(categories_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
                except Exception:
                    continue
    return categories


def parse_cart():
    cart_path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    if os.path.exists(cart_path):
        with open(cart_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                try:
                    item = {
                        'cart_id': int(parts[0]),
                        'book_id': int(parts[1]),
                        'quantity': int(parts[2]),
                        'added_date': parts[3]
                    }
                    cart.append(item)
                except Exception:
                    continue
    return cart


def write_cart(cart):
    cart_path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(cart_path, 'w', encoding='utf-8') as f:
            for item in cart:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def parse_orders():
    orders_path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    if os.path.exists(orders_path):
        with open(orders_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
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
                except Exception:
                    continue
    return orders


def write_orders(orders):
    orders_path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(orders_path, 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def parse_order_items():
    order_items_path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    if os.path.exists(order_items_path):
        with open(order_items_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                try:
                    item = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'book_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(item)
                except Exception:
                    continue
    return order_items


def write_order_items(order_items):
    order_items_path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(order_items_path, 'w', encoding='utf-8') as f:
            for item in order_items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def parse_reviews():
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(reviews_path):
        with open(reviews_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
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
                except Exception:
                    continue
    return reviews


def write_reviews(reviews):
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(reviews_path, 'w', encoding='utf-8') as f:
            for review in reviews:
                line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def parse_bestsellers():
    bestsellers_path = os.path.join(DATA_DIR, 'bestsellers.txt')
    bestsellers = []
    if os.path.exists(bestsellers_path):
        with open(bestsellers_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    bs = {
                        'book_id': int(parts[0]),
                        'sales_count': int(parts[1]),
                        'period': parts[2]
                    }
                    bestsellers.append(bs)
                except Exception:
                    continue
    return bestsellers


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    books = parse_books()
    bestsellers_data = parse_bestsellers()

    # For featured_books, pick up to 5 with highest stock (arbitrary choice)
    featured_books = sorted(books, key=lambda b: b['stock'], reverse=True)[:5]
    # Simplify featured_books to required fields
    featured_books_list = []
    for b in featured_books:
        fb = {
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        }
        featured_books_list.append(fb)

    # For bestsellers on dashboard - pick bestsellers with period "All Time" or fallback
    period_bestsellers = [bs for bs in bestsellers_data if bs['period'] == 'All Time']
    # Sort by sales_count descending
    period_bestsellers = sorted(period_bestsellers, key=lambda bs: bs['sales_count'], reverse=True)[:5]
    bestsellers_list = []
    for idx, bs in enumerate(period_bestsellers):
        book = next((bk for bk in books if bk['book_id'] == bs['book_id']), None)
        if not book:
            continue
        bsentry = {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'sales_count': bs['sales_count']
        }
        bestsellers_list.append(bsentry)

    return render_template('dashboard.html', featured_books=featured_books_list, bestsellers=bestsellers_list)


@app.route('/catalog')
def catalog():
    books = parse_books()
    categories = parse_categories()

    search = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()

    filtered_books = []
    for b in books:
        if search and search not in b['title'].lower() and search not in b['author'].lower():
            continue
        if category_filter:
            # category_filter can be category_id as string, match with categories
            try:
                cat_id_int = int(category_filter)
            except Exception:
                cat_id_int = None
            if cat_id_int is not None:
                # Find category name by id
                category_obj = next((c for c in categories if c['category_id'] == cat_id_int), None)
                if category_obj:
                    if b['category'].lower() != category_obj['category_name'].lower():
                        continue
                else:
                    continue
            else:
                # category_filter is not a valid int, filter by name
                if b['category'].lower() != category_filter.lower():
                    continue
        filtered_books.append(b)

    # Prepare books for context
    books_list = [{'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'price': b['price']} for b in filtered_books]

    # Categories list for context
    categories_list = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('catalog.html', books=books_list, categories=categories_list)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = parse_books()
    reviews_all = parse_reviews()
    cart = parse_cart()

    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        # Book not found, redirect to catalog
        return redirect(url_for('catalog'))

    # Get reviews belonging to this book
    book_reviews = [r for r in reviews_all if r['book_id'] == book_id]

    if request.method == 'POST':
        # Add to cart
        quantity_str = request.form.get('quantity', '').strip()
        try:
            quantity = int(quantity_str) if quantity_str else 1
            if quantity <= 0:
                quantity = 1
        except Exception:
            quantity = 1

        # Add to cart file
        # Generate new cart_id
        max_cart_id = max((c['cart_id'] for c in cart), default=0)
        new_cart_id = max_cart_id + 1
        added_date = datetime.now().strftime('%Y-%m-%d')

        # Check if the book already exists in cart (add quantities if exists)
        existing_item = next((item for item in cart if item['book_id'] == book_id), None)
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            cart.append({'cart_id': new_cart_id, 'book_id': book_id, 'quantity': quantity, 'added_date': added_date})

        write_cart(cart)

        # Redirect back to book details page
        return redirect(url_for('book_details', book_id=book_id))

    # For GET method, render page
    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_data = parse_cart()
    books = parse_books()

    if request.method == 'POST':
        action = request.form.get('action')
        remove_ids = []
        updated = False

        if action == 'update':
            for item in cart_data:
                item_id = item['cart_id']
                qty_key = f'quantity_{item_id}'
                qty_str = request.form.get(qty_key, '').strip()
                try:
                    qty = int(qty_str)
                    if qty <= 0:
                        remove_ids.append(item_id)
                    else:
                        item['quantity'] = qty
                        updated = True
                except Exception:
                    continue
            if remove_ids:
                cart_data = [item for item in cart_data if item['cart_id'] not in remove_ids]
                updated = True

            if updated:
                write_cart(cart_data)

            return redirect(url_for('cart'))

        elif action == 'checkout':
            return redirect(url_for('checkout'))

    # For GET, prepare cart_items and total_amount
    cart_items = []
    total_amount = 0.0

    for item in cart_data:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        price = book['price']
        quantity = item['quantity']
        subtotal = price * quantity
        total_amount += subtotal

        cart_items.append({
            'item_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_data = parse_cart()
    books = parse_books()

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        # Validate required fields
        if not customer_name or not shipping_address or not payment_method:
            # Possibly render checkout with error (not specified)
            return render_template('checkout.html')

        # Calculate total_amount and prepare order items
        order_items_data = []
        total_amount = 0.0
        for item in cart_data:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book:
                continue
            price = book['price']
            quantity = item['quantity']
            subtotal = price * quantity
            total_amount += subtotal
            order_items_data.append({
                'book_id': book['book_id'],
                'quantity': quantity,
                'price': price
            })

        if total_amount <= 0:
            # No valid order
            return render_template('checkout.html')

        # Create new order id
        orders = parse_orders()
        max_order_id = max((o['order_id'] for o in orders), default=0)
        new_order_id = max_order_id + 1
        order_date = datetime.now().strftime('%Y-%m-%d')

        # Append new order
        order_entry = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(order_entry)
        write_orders(orders)

        # Append order items with order_item_id
        order_items = parse_order_items()
        max_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0)

        for item in order_items_data:
            max_order_item_id += 1
            oi_entry = {
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['price']
            }
            order_items.append(oi_entry)

        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('order_history'))

    # GET
    return render_template('checkout.html')


@app.route('/orders')
def order_history():
    orders = parse_orders()
    status_filter = request.args.get('status', 'All').strip()

    valid_statuses = ['Pending', 'Shipped', 'Delivered', 'All']
    if status_filter not in valid_statuses:
        status_filter = 'All'

    filtered_orders = []
    for o in orders:
        if status_filter == 'All' or o['status'] == status_filter:
            filtered_orders.append(o)

    return render_template('orders.html', orders=filtered_orders)


@app.route('/orders/<int:order_id>')
def order_details(order_id):
    orders = parse_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        # Order not found, redirect to order history
        return redirect(url_for('order_history'))

    order_items_all = parse_order_items()
    books = parse_books()

    order_items_list = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if not book:
                continue
            order_items_list.append({
                'order_item_id': oi['order_item_id'],
                'book_id': oi['book_id'],
                'title': book['title'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    return render_template('order_details.html', order=order, order_items=order_items_list)


@app.route('/reviews')
def reviews():
    reviews_all = parse_reviews()
    books = parse_books()

    filter_rating = request.args.get('filter_rating', '').strip()

    filtered_reviews = []
    for r in reviews_all:
        if filter_rating:
            try:
                rating_val = int(filter_rating)
                if r['rating'] != rating_val:
                    continue
            except Exception:
                # invalid filter ignore
                pass
        if r['review_text'].lower() in ['write', 'reproduction']:
            continue
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        if not book:
            continue
        filtered_reviews.append({
            'review_id': r['review_id'],
            'customer_name': r['customer_name'],
            'book_title': book['title'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = parse_books()
    reviews_all = parse_reviews()

    # For purchased_books, criteria not specified so assume all books
    purchased_books = [{'book_id': b['book_id'], 'title': b['title']} for b in books]

    if request.method == 'POST':
        try:
            selected_book_id = int(request.form.get('selected_book_id', '').strip())
            rating = int(request.form.get('rating', '').strip())
            review_text = request.form.get('review_text', '').strip()

            if rating < 1 or rating > 5 or not review_text:
                # Invalid input, ignore or reload
                return render_template('write_review.html', purchased_books=purchased_books)

        except Exception:
            return render_template('write_review.html', purchased_books=purchased_books)

        max_review_id = max((r['review_id'] for r in reviews_all), default=0)
        new_review_id = max_review_id + 1
        review_date = datetime.now().strftime('%Y-%m-%d')

        # Using default customer_name as Anonymous (not specified)
        new_review = {
            'review_id': new_review_id,
            'book_id': selected_book_id,
            'customer_name': 'Anonymous',
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews_all.append(new_review)
        write_reviews(reviews_all)

        return redirect(url_for('reviews'))

    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers')
def bestsellers():
    time_period = request.args.get('time_period', 'All Time').strip()
    bestsellers_data = parse_bestsellers()
    books = parse_books()

    filtered_bs = [bs for bs in bestsellers_data if bs['period'] == time_period]

    # Sort descending by sales_count
    filtered_bs_sorted = sorted(filtered_bs, key=lambda bs: bs['sales_count'], reverse=True)

    bestsellers_list = []
    for rank, bs in enumerate(filtered_bs_sorted, start=1):
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if not book:
            continue
        bestsellers_list.append({
            'rank': rank,
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'sales_count': bs['sales_count']
        })

    return render_template('bestsellers.html', bestsellers=bestsellers_list)


if __name__ == '__main__':
    app.run(debug=True)
