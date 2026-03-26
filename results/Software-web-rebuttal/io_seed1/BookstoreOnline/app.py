'''
Main backend application for BookstoreOnline web application.
Handles routing, business logic, reading/writing data from/to local text files,
and rendering HTML templates. Implements all required features:
- Dashboard with featured books and bestsellers
- Book catalog with search and category filter
- Book details with reviews and add to cart
- Shopping cart management
- Checkout and order placement
- Order history with filtering
- Customer reviews listing and writing new reviews
- Bestsellers listing with time period filter
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'bookstore_secret_key'  # Needed for flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing data files
def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            book = {
                'book_id': parts[0],
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'category': parts[4],
                'price': float(parts[5]),
                'stock': int(parts[6]),
                'description': parts[7]
            }
            books.append(book)
    return books
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
    return categories
def read_cart():
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            item = {
                'cart_id': parts[0],
                'book_id': parts[1],
                'quantity': int(parts[2]),
                'added_date': parts[3]
            }
            cart_items.append(item)
    return cart_items
def write_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            order = {
                'order_id': parts[0],
                'customer_name': parts[1],
                'order_date': parts[2],
                'total_amount': float(parts[3]),
                'status': parts[4],
                'shipping_address': parts[5]
            }
            orders.append(order)
    return orders
def write_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for order in orders:
            line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']:.2f}|{order['status']}|{order['shipping_address']}\n"
            f.write(line)
def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            item = {
                'order_item_id': parts[0],
                'order_id': parts[1],
                'book_id': parts[2],
                'quantity': int(parts[3]),
                'price': float(parts[4])
            }
            order_items.append(item)
    return order_items
def write_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in order_items:
            line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']:.2f}\n"
            f.write(line)
def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            review = {
                'review_id': parts[0],
                'book_id': parts[1],
                'customer_name': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
            reviews.append(review)
    return reviews
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for review in reviews:
            line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
            f.write(line)
def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if not os.path.exists(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            bestseller = {
                'book_id': parts[0],
                'sales_count': int(parts[1]),
                'period': parts[2]
            }
            bestsellers.append(bestseller)
    return bestsellers
# Helper functions
def get_book_by_id(book_id):
    books = read_books()
    for book in books:
        if book['book_id'] == book_id:
            return book
    return None
def get_category_name(category_id):
    categories = read_categories()
    for cat in categories:
        if cat['category_id'] == category_id:
            return cat['category_name']
    return None
def get_category_id_by_name(category_name):
    categories = read_categories()
    for cat in categories:
        if cat['category_name'].lower() == category_name.lower():
            return cat['category_id']
    return None
def get_reviews_for_book(book_id):
    reviews = read_reviews()
    return [r for r in reviews if r['book_id'] == book_id]
def get_cart_item_by_id(cart_id):
    cart = read_cart()
    for item in cart:
        if item['cart_id'] == cart_id:
            return item
    return None
def generate_new_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            cur_id = int(item[id_field])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    return str(max_id + 1)
def get_order_items_by_order_id(order_id):
    order_items = read_order_items()
    return [item for item in order_items if item['order_id'] == order_id]
def get_reviews_filtered_by_rating(rating_filter):
    reviews = read_reviews()
    if rating_filter == 'All':
        return reviews
    try:
        rating_int = int(rating_filter[0])  # e.g. "5 stars" -> 5
    except:
        return reviews
    return [r for r in reviews if r['rating'] == rating_int]
def get_orders_filtered_by_status(status_filter):
    orders = read_orders()
    if status_filter == 'All':
        return orders
    return [o for o in orders if o['status'].lower() == status_filter.lower()]
def get_bestsellers_filtered_by_period(period_filter):
    bestsellers = read_bestsellers()
    if period_filter == 'All Time':
        return bestsellers
    return [b for b in bestsellers if b['period'].lower() == period_filter.lower()]
# Routes
@app.route('/')
def dashboard():
    # Featured books: pick first 3 books as featured (or less if fewer)
    books = read_books()
    featured_books = books[:3]
    # Bestsellers for "This Month" by default
    bestsellers_data = get_bestsellers_filtered_by_period('This Month')
    # Join bestseller info with book info
    bestsellers = []
    for b in sorted(bestsellers_data, key=lambda x: x['sales_count'], reverse=True):
        book = get_book_by_id(b['book_id'])
        if book:
            bestsellers.append({
                'rank': len(bestsellers) + 1,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
    return render_template('dashboard.html',
                           featured_books=featured_books,
                           bestsellers=bestsellers)
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    filtered_books = books
    if search_query:
        sq = search_query.lower()
        filtered_books = [b for b in filtered_books if sq in b['title'].lower() or sq in b['author'].lower() or sq in b['isbn'].lower()]
    if category_filter and category_filter != 'All':
        filtered_books = [b for b in filtered_books if b['category'].lower() == category_filter.lower()]
    category_names = ['All'] + [cat['category_name'] for cat in categories]
    return render_template('catalog.html',
                           books=filtered_books,
                           categories=category_names,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/book/<book_id>', methods=['GET'])
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))
    reviews = get_reviews_for_book(book_id)
    # Sort reviews by date descending
    reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('book_details.html',
                           book=book,
                           reviews=reviews)
@app.route('/add_to_cart/<book_id>', methods=['POST'])
def add_to_cart(book_id):
    book = get_book_by_id(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))
    cart = read_cart()
    # Check if book already in cart, if so increase quantity by 1
    for item in cart:
        if item['book_id'] == book_id:
            item['quantity'] += 1
            break
    else:
        # Add new cart item
        new_cart_id = generate_new_id(cart, 'cart_id')
        today_str = datetime.now().strftime('%Y-%m-%d')
        cart.append({
            'cart_id': new_cart_id,
            'book_id': book_id,
            'quantity': 1,
            'added_date': today_str
        })
    write_cart(cart)
    flash(f'Added "{book["title"]}" to cart.', 'success')
    return redirect(url_for('book_details', book_id=book_id))
@app.route('/cart', methods=['GET'])
def cart():
    cart_items = read_cart()
    books = read_books()
    # Build cart display data
    display_items = []
    total_amount = 0.0
    for item in cart_items:
        book = get_book_by_id(item['book_id'])
        if not book:
            continue
        subtotal = book['price'] * item['quantity']
        total_amount += subtotal
        display_items.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal
        })
    return render_template('cart.html',
                           cart_items=display_items,
                           total_amount=total_amount)
@app.route('/update_cart_quantity/<cart_id>', methods=['POST'])
def update_cart_quantity(cart_id):
    try:
        new_quantity = int(request.form.get('quantity', '1'))
        if new_quantity < 1:
            flash('Quantity must be at least 1.', 'error')
            return redirect(url_for('cart'))
    except ValueError:
        flash('Invalid quantity.', 'error')
        return redirect(url_for('cart'))
    cart = read_cart()
    updated = False
    for item in cart:
        if item['cart_id'] == cart_id:
            item['quantity'] = new_quantity
            updated = True
            break
    if updated:
        write_cart(cart)
        flash('Cart updated.', 'success')
    else:
        flash('Cart item not found.', 'error')
    return redirect(url_for('cart'))
@app.route('/remove_cart_item/<cart_id>', methods=['POST'])
def remove_cart_item(cart_id):
    cart = read_cart()
    new_cart = [item for item in cart if item['cart_id'] != cart_id]
    if len(new_cart) == len(cart):
        flash('Cart item not found.', 'error')
    else:
        write_cart(new_cart)
        flash('Item removed from cart.', 'success')
    return redirect(url_for('cart'))
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    # POST: place order
    customer_name = request.form.get('customer-name', '').strip()
    shipping_address = request.form.get('shipping-address', '').strip()
    payment_method = request.form.get('payment-method', '').strip()
    if not customer_name or not shipping_address or not payment_method:
        flash('Please fill in all required fields.', 'error')
        return render_template('checkout.html',
                               customer_name=customer_name,
                               shipping_address=shipping_address,
                               payment_method=payment_method)
    cart = read_cart()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    books = read_books()
    # Calculate total amount and check stock availability
    total_amount = 0.0
    book_stock_map = {b['book_id']: b['stock'] for b in books}
    for item in cart:
        book_id = item['book_id']
        quantity = item['quantity']
        if book_id not in book_stock_map or book_stock_map[book_id] < quantity:
            flash(f'Not enough stock for book ID {book_id}.', 'error')
            return redirect(url_for('cart'))
        book = get_book_by_id(book_id)
        total_amount += book['price'] * quantity
    # Generate new order ID
    orders = read_orders()
    new_order_id = generate_new_id(orders, 'order_id')
    order_date = datetime.now().strftime('%Y-%m-%d')
    status = 'Pending'
    # Create new order record
    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': status,
        'shipping_address': shipping_address
    }
    orders.append(new_order)
    write_orders(orders)
    # Create order items
    order_items = read_order_items()
    next_order_item_id = int(generate_new_id(order_items, 'order_item_id'))
    for item in cart:
        book = get_book_by_id(item['book_id'])
        order_item = {
            'order_item_id': str(next_order_item_id),
            'order_id': new_order_id,
            'book_id': item['book_id'],
            'quantity': item['quantity'],
            'price': book['price']
        }
        order_items.append(order_item)
        next_order_item_id += 1
        # Decrease stock
        for b in books:
            if b['book_id'] == item['book_id']:
                b['stock'] -= item['quantity']
                break
    write_order_items(order_items)
    # Update books stock file
    path_books = os.path.join(DATA_DIR, 'books.txt')
    with open(path_books, 'w', encoding='utf-8') as f:
        for b in books:
            line = f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['category']}|{b['price']:.2f}|{b['stock']}|{b['description']}\n"
            f.write(line)
    # Clear cart
    write_cart([])
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_history'))
@app.route('/order_history', methods=['GET'])
def order_history():
    status_filter = request.args.get('status', 'All')
    orders = get_orders_filtered_by_status(status_filter)
    return render_template('order_history.html',
                           orders=orders,
                           selected_status=status_filter)
@app.route('/order/<order_id>', methods=['GET'])
def order_details(order_id):
    orders = read_orders()
    order = None
    for o in orders:
        if o['order_id'] == order_id:
            order = o
            break
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('order_history'))
    order_items = get_order_items_by_order_id(order_id)
    # Join order items with book info
    items_detail = []
    for item in order_items:
        book = get_book_by_id(item['book_id'])
        if not book:
            continue
        items_detail.append({
            'title': book['title'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': item['price'] * item['quantity']
        })
    return render_template('order_details.html',
                           order=order,
                           order_items=items_detail)
@app.route('/reviews', methods=['GET'])
def reviews():
    rating_filter = request.args.get('rating', 'All')
    reviews = get_reviews_filtered_by_rating(rating_filter)
    # Join reviews with book titles
    books = read_books()
    book_map = {b['book_id']: b['title'] for b in books}
    reviews_display = []
    for r in reviews:
        reviews_display.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'book_title': book_map.get(r['book_id'], 'Unknown'),
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date'],
            'customer_name': r['customer_name']
        })
    return render_template('reviews.html',
                           reviews=reviews_display,
                           selected_rating=rating_filter)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'GET':
        return render_template('write_review.html', books=books)
    # POST: submit review
    book_id = request.form.get('select-book', '').strip()
    rating = request.form.get('rating-select', '').strip()
    review_text = request.form.get('review-text', '').strip()
    customer_name = request.form.get('customer-name', '').strip()
    if not book_id or not rating or not review_text or not customer_name:
        flash('Please fill in all fields.', 'error')
        return render_template('write_review.html', books=books,
                               selected_book=book_id,
                               selected_rating=rating,
                               review_text=review_text,
                               customer_name=customer_name)
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError
    except ValueError:
        flash('Invalid rating selected.', 'error')
        return render_template('write_review.html', books=books,
                               selected_book=book_id,
                               selected_rating=rating,
                               review_text=review_text,
                               customer_name=customer_name)
    # Generate new review ID
    reviews = read_reviews()
    new_review_id = generate_new_id(reviews, 'review_id')
    review_date = datetime.now().strftime('%Y-%m-%d')
    new_review = {
        'review_id': new_review_id,
        'book_id': book_id,
        'customer_name': customer_name,
        'rating': rating_int,
        'review_text': review_text,
        'review_date': review_date
    }
    reviews.append(new_review)
    write_reviews(reviews)
    flash('Review submitted successfully.', 'success')
    return redirect(url_for('reviews'))
@app.route('/bestsellers', methods=['GET'])
def bestsellers():
    time_period_filter = request.args.get('period', 'This Month')
    bestsellers_data = get_bestsellers_filtered_by_period(time_period_filter)
    # Join bestseller info with book info
    bestsellers_list = []
    for b in sorted(bestsellers_data, key=lambda x: x['sales_count'], reverse=True):
        book = get_book_by_id(b['book_id'])
        if book:
            bestsellers_list.append({
                'rank': len(bestsellers_list) + 1,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
    time_periods = ['This Week', 'This Month', 'All Time']
    return render_template('bestsellers.html',
                           bestsellers=bestsellers_list,
                           selected_period=time_period_filter,
                           time_periods=time_periods)
# Navigation routes for buttons that redirect to other pages
@app.route('/go_to_catalog', methods=['POST'])
def go_to_catalog():
    return redirect(url_for('catalog'))
@app.route('/go_to_cart', methods=['POST'])
def go_to_cart():
    return redirect(url_for('cart'))
@app.route('/go_to_bestsellers', methods=['POST'])
def go_to_bestsellers():
    return redirect(url_for('bestsellers'))
@app.route('/back_to_dashboard', methods=['POST'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/write_review_page', methods=['POST'])
def write_review_page():
    return redirect(url_for('write_review'))
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)