'''
Main backend Python application for BookstoreOnline web application.
Implements all routing, data handling, and user actions using Flask.
Data is stored in local text files under 'data/' directory.
No authentication; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
app = Flask(__name__)
app.secret_key = 'evomac_secret_key_for_flash_messages'  # Needed for flashing messages
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
                'description': parts[7],
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
                'description': parts[2],
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
                'added_date': parts[3],
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
                'shipping_address': parts[5],
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
                'price': float(parts[4]),
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
                'review_date': parts[5],
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
                'period': parts[2],
            }
            bestsellers.append(bestseller)
    return bestsellers
# Helper to get next ID for a file based on existing IDs
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Route: Dashboard page
@app.route('/')
def dashboard():
    books = read_books()
    bestsellers = read_bestsellers()
    # Featured books: pick first 3 books as example
    featured_books = books[:3] if len(books) >= 3 else books
    # For bestsellers, join with book info
    bestsellers_books = []
    for bs in bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            bestsellers_books.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period'],
            })
    return render_template('dashboard.html',
                           featured_books=featured_books,
                           bestsellers=bestsellers_books)
# Route: Book Catalog page
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    filtered_books = books
    # Filter by search query (title, author, isbn)
    if search_query:
        sq_lower = search_query.lower()
        filtered_books = [b for b in filtered_books if
                          sq_lower in b['title'].lower() or
                          sq_lower in b['author'].lower() or
                          sq_lower in b['isbn'].lower()]
    # Filter by category name
    if category_filter and category_filter != 'All':
        filtered_books = [b for b in filtered_books if b['category'] == category_filter]
    return render_template('catalog.html',
                           books=filtered_books,
                           categories=categories,
                           search_query=search_query,
                           category_filter=category_filter)
# Route: Book Details page
@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('catalog'))
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    if request.method == 'POST':
        # Add to cart action
        quantity_str = request.form.get('quantity', '1').strip()
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                raise ValueError
            if quantity > book['stock']:
                flash(f'Quantity exceeds available stock ({book["stock"]}).', 'error')
                return redirect(url_for('book_details', book_id=book_id))
        except:
            flash('Invalid quantity.', 'error')
            return redirect(url_for('book_details', book_id=book_id))
        # Read cart and add/update item
        cart_items = read_cart()
        # Check if book already in cart
        existing_item = next((item for item in cart_items if item['book_id'] == book_id), None)
        if existing_item:
            new_quantity = existing_item['quantity'] + quantity
            if new_quantity > book['stock']:
                flash(f'Total quantity in cart exceeds available stock ({book["stock"]}).', 'error')
                return redirect(url_for('book_details', book_id=book_id))
            existing_item['quantity'] = new_quantity
        else:
            new_cart_id = get_next_id(cart_items, 'cart_id')
            today_str = datetime.date.today().isoformat()
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_str,
            })
        write_cart(cart_items)
        flash(f'Added {quantity} copy(ies) of "{book["title"]}" to cart.', 'success')
        return redirect(url_for('book_details', book_id=book_id))
    return render_template('book_details.html',
                           book=book,
                           reviews=book_reviews)
# Route: Shopping Cart page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    books = read_books()
    cart_items = read_cart()
    # Join cart items with book info
    cart_display = []
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        subtotal = book['price'] * item['quantity']
        total_amount += subtotal
        cart_display.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal,
            'stock': book['stock'],
        })
    if request.method == 'POST':
        # Handle update quantities and remove items
        form = request.form
        updated_cart = []
        cart_changed = False
        # Remove items
        remove_ids = form.getlist('remove')
        # Update quantities
        for item in cart_display:
            cid = item['cart_id']
            if cid in remove_ids:
                cart_changed = True
                continue  # skip this item (remove)
            qty_str = form.get(f'update-quantity-{cid}', str(item['quantity']))
            try:
                qty = int(qty_str)
                if qty < 1:
                    qty = 1
                if qty > item['stock']:
                    flash(f'Quantity for "{item["title"]}" exceeds available stock ({item["stock"]}). Adjusted to max stock.', 'warning')
                    qty = item['stock']
            except:
                qty = item['quantity']
            if qty != item['quantity']:
                cart_changed = True
            updated_cart.append({
                'cart_id': cid,
                'book_id': item['book_id'],
                'quantity': qty,
                'added_date': next((ci['added_date'] for ci in cart_items if ci['cart_id'] == cid), datetime.date.today().isoformat()),
            })
        if cart_changed:
            write_cart(updated_cart)
            flash('Cart updated successfully.', 'success')
        else:
            flash('No changes made to cart.', 'info')
        # Check if proceed to checkout button pressed
        if 'proceed-checkout' in form:
            if len(updated_cart) == 0:
                flash('Your cart is empty. Add items before checkout.', 'error')
                return redirect(url_for('cart'))
            return redirect(url_for('checkout'))
        return redirect(url_for('cart'))
    return render_template('cart.html',
                           cart_items=cart_display,
                           total_amount=total_amount)
# Route: Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = read_cart()
    if not cart_items:
        flash('Your cart is empty. Add items before checkout.', 'error')
        return redirect(url_for('dashboard'))
    books = read_books()
    # Calculate total amount
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            total_amount += book['price'] * item['quantity']
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name:
            flash('Customer name is required.', 'error')
            return redirect(url_for('checkout'))
        if not shipping_address:
            flash('Shipping address is required.', 'error')
            return redirect(url_for('checkout'))
        if payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            flash('Invalid payment method selected.', 'error')
            return redirect(url_for('checkout'))
        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        new_order_id = get_next_id(orders, 'order_id')
        order_date = datetime.date.today().isoformat()
        status = 'Pending'
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': status,
            'shipping_address': shipping_address,
        }
        orders.append(new_order)
        write_orders(orders)
        # Create order items
        next_order_item_id = int(get_next_id(order_items, 'order_item_id'))
        for item in cart_items:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book:
                continue
            order_item = {
                'order_item_id': str(next_order_item_id),
                'order_id': new_order_id,
                'book_id': book['book_id'],
                'quantity': item['quantity'],
                'price': book['price'],
            }
            order_items.append(order_item)
            next_order_item_id += 1
        write_order_items(order_items)
        # Clear cart after order placed
        write_cart([])
        flash(f'Order #{new_order_id} placed successfully!', 'success')
        return redirect(url_for('order_history'))
    return render_template('checkout.html',
                           total_amount=total_amount)
# Route: Order History page
@app.route('/orders', methods=['GET'])
def order_history():
    orders = read_orders()
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]
    return render_template('order_history.html',
                           orders=orders,
                           status_filter=status_filter)
# Route: View Order Details page
@app.route('/orders/<order_id>')
def order_details(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('order_history'))
    order_items = read_order_items()
    books = read_books()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book:
                items.append({
                    'order_item_id': oi['order_item_id'],
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'quantity': oi['quantity'],
                    'price': oi['price'],
                    'subtotal': oi['price'] * oi['quantity'],
                })
    return render_template('order_details.html',
                           order=order,
                           items=items)
# Route: Reviews page
@app.route('/reviews', methods=['GET'])
def reviews():
    reviews = read_reviews()
    books = read_books()
    rating_filter = request.args.get('rating', 'All')
    filtered_reviews = reviews
    if rating_filter != 'All':
        try:
            rating_val = int(rating_filter[0])  # e.g. "5 stars" -> 5
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    # Join reviews with book titles
    reviews_display = []
    for r in filtered_reviews:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        if book:
            reviews_display.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'book_title': book['title'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'customer_name': r['customer_name'],
                'review_date': r['review_date'],
            })
    return render_template('reviews.html',
                           reviews=reviews_display,
                           rating_filter=rating_filter)
# Route: Write Review page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'POST':
        book_id = request.form.get('select-book', '').strip()
        rating_str = request.form.get('rating-select', '').strip()
        review_text = request.form.get('review-text', '').strip()
        customer_name = 'Anonymous'  # Since no authentication, use generic or could ask user
        if not book_id or not rating_str or not review_text:
            flash('All fields are required to submit a review.', 'error')
            return redirect(url_for('write_review'))
        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError
        except:
            flash('Invalid rating selected.', 'error')
            return redirect(url_for('write_review'))
        reviews = read_reviews()
        new_review_id = get_next_id(reviews, 'review_id')
        review_date = datetime.date.today().isoformat()
        new_review = {
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date,
        }
        reviews.append(new_review)
        write_reviews(reviews)
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('reviews'))
    return render_template('write_review.html',
                           books=books)
# Route: Bestsellers page
@app.route('/bestsellers', methods=['GET'])
def bestsellers():
    bestsellers = read_bestsellers()
    books = read_books()
    time_period_filter = request.args.get('period', 'This Month')
    filtered_bestsellers = [bs for bs in bestsellers if bs['period'] == time_period_filter]
    # Sort by sales_count descending
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)
    # Join with book info
    bestsellers_display = []
    rank = 1
    for bs in filtered_bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            bestsellers_display.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period'],
            })
            rank += 1
    time_periods = ['This Week', 'This Month', 'All Time']
    return render_template('bestsellers.html',
                           bestsellers=bestsellers_display,
                           time_period_filter=time_period_filter,
                           time_periods=time_periods)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)