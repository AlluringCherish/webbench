from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Utility functions to read/write data files

# Read books.txt

def read_books():
    books = []
    try:
        with open(os.path.join(DATA_DIR, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return books

# Write books.txt
# Note: This is needed only if stock adjustment immediately on add to cart is chosen
# Not used here because stock adjusted on checkout

def write_books(books):
    lines = []
    for book in books:
        line = f"{book['book_id']}|{book['title']}|{book['author']}|{book['isbn']}|{book['category']}|{book['price']:.2f}|{book['stock']}|{book['description']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'books.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read categories.txt

def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except FileNotFoundError:
        pass
    return categories

# Read cart.txt

def read_cart():
    cart_items = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                item = {
                    'cart_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3],
                }
                cart_items.append(item)
    except FileNotFoundError:
        pass
    return cart_items

# Write cart.txt

def write_cart(cart_items):
    lines = []
    for item in cart_items:
        line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read orders.txt

def read_orders():
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except FileNotFoundError:
        pass
    return orders

# Write orders.txt

def write_orders(orders):
    lines = []
    for order in orders:
        line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']:.2f}|{order['status']}|{order['shipping_address']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'orders.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read order_items.txt

def read_order_items():
    order_items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                oi = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(oi)
    except FileNotFoundError:
        pass
    return order_items

# Write order_items.txt

def write_order_items(order_items):
    lines = []
    for oi in order_items:
        line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['book_id']}|{oi['quantity']}|{oi['price']:.2f}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'order_items.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read reviews.txt

def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except FileNotFoundError:
        pass
    return reviews

# Write reviews.txt

def write_reviews(reviews):
    lines = []
    for r in reviews:
        line = f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read bestsellers.txt

def read_bestsellers():
    bestsellers = []
    try:
        with open(os.path.join(DATA_DIR, 'bestsellers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                bs = {
                    'book_id': int(parts[0]),
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                }
                bestsellers.append(bs)
    except FileNotFoundError:
        pass
    return bestsellers

# Write bestsellers.txt
# Not needed (read only)

# Helper function to get book by id

def get_book_by_id(book_id):
    books = read_books()
    for book in books:
        if book['book_id'] == book_id:
            return book
    return None

# Helper function to filter books by search and category

def filter_books(books, search=None, category=None):
    results = books
    if search:
        search_lower = search.lower()
        results = [b for b in results if 
                   search_lower in b['title'].lower() or 
                   search_lower in b['author'].lower() or 
                   search_lower in b['isbn'].lower()]
    if category:
        results = [b for b in results if b['category'] == category]
    return results

# Helper to get categories list

def get_categories():
    return read_categories()

# Helper to get cart with book info

def get_cart_items_full():
    cart_items = read_cart()
    books = {b['book_id']: b for b in read_books()}
    cart_full = []
    for item in cart_items:
        book = books.get(item['book_id'])
        if not book:
            continue
        entry = item.copy()
        entry['book'] = book
        cart_full.append(entry)
    return cart_full

# Helper to calculate total amount of cart

def calculate_cart_total(cart_items_full):
    total = 0.0
    for item in cart_items_full:
        total += item['quantity'] * item['book']['price']
    return total

# Helper to get reviews for a book

def get_reviews_for_book(book_id):
    reviews = read_reviews()
    filtered = [r for r in reviews if r['book_id'] == book_id]
    return filtered

# Helper to filter reviews by rating or all

def filter_reviews(reviews, rating_filter=None):
    if rating_filter and rating_filter != 'All':
        try:
            rating_value = int(rating_filter)
            return [r for r in reviews if r['rating'] == rating_value]
        except Exception:
            return reviews
    return reviews

# Helper to get next unique ID

def get_next_id(items, id_field):
    if not items:
        return 1
    return max(item[id_field] for item in items) + 1

# Routes Implementation

@app.route('/')
def dashboard():
    books = read_books()
    # Featured books: select first 5 or all if less
    featured_books = books[:5]

    # Bestsellers all time
    bestsellers_all = read_bestsellers()
    # Filter 'All Time' period
    bestsellers_list = [bs for bs in bestsellers_all if bs['period'] == 'All Time']
    # Enhance bestsellers with book info and sales_count
    books_map = {b['book_id']: b for b in books}
    bestsellers = []
    for bs in bestsellers_list:
        book = books_map.get(bs['book_id'])
        if book:
            b = book.copy()
            b['sales_count'] = bs['sales_count']
            bestsellers.append(b)

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)

@app.route('/catalog')
def catalog():
    search = request.args.get('search', type=str)
    category = request.args.get('category', type=str)

    books = read_books()
    filtered_books = filter_books(books, search, category)
    categories = get_categories()

    return render_template('catalog.html', books=filtered_books, categories=categories)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        flash('Book not found')
        return redirect(url_for('catalog'))

    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        # Add to cart logic
        cart_items = read_cart()
        max_cart_id = get_next_id(cart_items, 'cart_id')

        # Check if book already in cart
        existing_item = None
        for item in cart_items:
            if item['book_id'] == book_id:
                existing_item = item
                break

        if existing_item:
            # Update quantity
            existing_item['quantity'] += quantity
        else:
            # Create new cart item
            new_item = {
                'cart_id': max_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            }
            cart_items.append(new_item)

        write_cart(cart_items)
        flash('Added to cart successfully')
        return redirect(url_for('cart'))

    reviews = get_reviews_for_book(book_id)
    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        cart_items = read_cart()
        # Check for removals
        remove_item_id = request.form.get('remove_item', type=int)
        if remove_item_id is not None:
            cart_items = [item for item in cart_items if item['cart_id'] != remove_item_id]
            write_cart(cart_items)
            flash('Item removed from cart')
            return redirect(url_for('cart'))

        # Update quantities
        updated = False
        for item in cart_items:
            form_key = f'update-quantity-{item["cart_id"]}'
            quantity_str = request.form.get(form_key)
            if quantity_str is not None:
                try:
                    quantity_val = int(quantity_str)
                    if quantity_val < 1:
                        quantity_val = 1
                    if quantity_val != item['quantity']:
                        item['quantity'] = quantity_val
                        updated = True
                except Exception:
                    pass

        if updated:
            write_cart(cart_items)
            flash('Cart updated successfully')

        return redirect(url_for('cart'))

    cart_items_full = get_cart_items_full()
    total_amount = calculate_cart_total(cart_items_full)
    return render_template('cart.html', cart_items=cart_items_full, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items_full = get_cart_items_full()
    if not cart_items_full:
        flash('Your cart is empty. Add items before checkout.')
        return redirect(url_for('cart'))
    total_amount = calculate_cart_total(cart_items_full)

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or not payment_method:
            flash('All fields are required.')
            return render_template('checkout.html', cart_items=cart_items_full, total_amount=total_amount)

        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        new_order_id = get_next_id(orders, 'order_id')
        order_date = datetime.now().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)

        # Create order items
        max_order_item_id = get_next_id(order_items, 'order_item_id')
        current_order_item_id = max_order_item_id

        for item in cart_items_full:
            order_item = {
                'order_item_id': current_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['book']['price']
            }
            order_items.append(order_item)
            current_order_item_id += 1

        # Write orders and order items data
        write_orders(orders)
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        # Decrement stock in books
        books = read_books()
        for book in books:
            for item in cart_items_full:
                if book['book_id'] == item['book_id']:
                    book['stock'] = max(0, book['stock'] - item['quantity'])
        write_books(books)

        flash('Order placed successfully!')
        return redirect(url_for('orders'))

    return render_template('checkout.html', cart_items=cart_items_full, total_amount=total_amount)

@app.route('/orders')
def orders():
    status_filter = request.args.get('status', 'All')
    orders_list = read_orders()
    if status_filter != 'All':
        orders_list = [o for o in orders_list if o['status'] == status_filter]

    return render_template('orders.html', orders=orders_list)

@app.route('/orders/<int:order_id>')
def order_details(order_id):
    orders_list = read_orders()
    order = next((o for o in orders_list if o['order_id'] == order_id), None)
    if not order:
        flash('Order not found')
        return redirect(url_for('orders'))

    order_items_list = read_order_items()
    items = [item for item in order_items_list if item['order_id'] == order_id]

    # Add book info to order items
    books_map = {b['book_id']: b for b in read_books()}
    for i in items:
        i['book'] = books_map.get(i['book_id'])

    return render_template('order_details.html', order=order, order_items=items)

@app.route('/reviews')
def reviews():
    rating_filter = request.args.get('rating_filter', 'All')
    all_reviews = read_reviews()
    filtered_reviews = filter_reviews(all_reviews, rating_filter)
    return render_template('reviews.html', reviews=filtered_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id'))
            customer_name = request.form.get('customer_name', '').strip()
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review_text', '').strip()
        except Exception:
            flash('Invalid input')
            return render_template('write_review.html', books=books)

        if not customer_name or rating < 1 or rating > 5 or not review_text:
            flash('All fields are required and rating must be 1-5')
            return render_template('write_review.html', books=books)

        reviews = read_reviews()
        new_review_id = get_next_id(reviews, 'review_id')
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

        flash('Review submitted successfully')
        return redirect(url_for('reviews'))

    return render_template('write_review.html', books=books)

@app.route('/bestsellers')
def bestsellers():
    period = request.args.get('period', 'All Time')
    bestsellers_all = read_bestsellers()
    filtered_bs = [bs for bs in bestsellers_all if bs['period'] == period]

    # If period not found, fallback to all time
    if not filtered_bs:
        filtered_bs = [bs for bs in bestsellers_all if bs['period'] == 'All Time']

    books_map = {b['book_id']: b for b in read_books()}
    result = []
    for bs in filtered_bs:
        book = books_map.get(bs['book_id'])
        if book:
            b = book.copy()
            b['sales_count'] = bs['sales_count']
            result.append(b)

    return render_template('bestsellers.html', bestsellers=result)

if __name__ == '__main__':
    app.run(debug=True)
