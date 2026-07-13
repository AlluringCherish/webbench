from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'
DATA_DIR = 'data'

# Utility functions to load and save data

def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 8:
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
    return books

def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    categories.append({'category_id': int(parts[0]), 'category_name': parts[1], 'description': parts[2]})
    return categories

def read_cart():
    cart = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    cart.append({
                        'cart_id': int(parts[0]),
                        'book_id': int(parts[1]),
                        'quantity': int(parts[2]),
                        'added_date': parts[3]
                    })
    return cart

def save_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart:
                f.write(f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n")
        return True
    except Exception as e:
        return False

def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    orders.append({
                        'order_id': int(parts[0]),
                        'customer_name': parts[1],
                        'order_date': parts[2],
                        'total_amount': float(parts[3]),
                        'status': parts[4],
                        'shipping_address': parts[5]
                    })
    return orders

def save_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for o in orders:
                f.write(f"{o['order_id']}|{o['customer_name']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['shipping_address']}\n")
        return True
    except Exception as e:
        return False

def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    order_items.append({
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'book_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    })
    return order_items

def save_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for oi in order_items:
                f.write(f"{oi['order_item_id']}|{oi['order_id']}|{oi['book_id']}|{oi['quantity']}|{oi['price']}\n")
        return True
    except Exception as e:
        return False

def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    reviews.append({
                        'review_id': int(parts[0]),
                        'book_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in reviews:
                f.write(f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")
        return True
    except Exception as e:
        return False

def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if not os.path.exists(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    bestsellers.append({
                        'book_id': int(parts[0]),
                        'sales_count': int(parts[1]),
                        'period': parts[2]
                    })
    return bestsellers

# Helper to get next available cart_id

def next_cart_id(cart):
    if not cart:
        return 1
    return max(item['cart_id'] for item in cart) + 1

# Helper to get next available order_id

def next_order_id(orders):
    if not orders:
        return 1
    return max(o['order_id'] for o in orders) + 1

# Helper to get next available order_item_id

def next_order_item_id(order_items):
    if not order_items:
        return 1
    return max(oi['order_item_id'] for oi in order_items) + 1

# Helper to get next available review_id

def next_review_id(reviews):
    if not reviews:
        return 1
    return max(r['review_id'] for r in reviews) + 1

@app.route('/')
@app.route('/dashboard')
def dashboard():
    try:
        books = read_books()
        featured_books = books[:5] if len(books) > 5 else books
    except Exception as e:
        featured_books = []
        flash('Error loading featured books.', 'error')
    return render_template('dashboard.html', title='Bookstore Dashboard', featured_books=featured_books)

@app.route('/catalog')
def book_catalog():
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    try:
        books = read_books()
        categories = read_categories()
    except Exception as e:
        books = []
        categories = []
        flash('Error loading catalog data.', 'error')

    filtered_books = books
    if search_query:
        filtered_books = [b for b in filtered_books if search_query in b['title'].lower() 
                          or search_query in b['author'].lower() or search_query in b['isbn'].lower()]
    if category_filter:
        filtered_books = [b for b in filtered_books if b['category'].lower() == category_filter.lower()]
    return render_template('catalog.html', title='Book Catalog', books=filtered_books, categories=categories, selected_category=category_filter, search_query=search_query)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    try:
        books = read_books()
        book = next((b for b in books if b['book_id'] == book_id), None)
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('book_catalog'))
    except Exception as e:
        flash('Error loading book details.', 'error')
        return redirect(url_for('book_catalog'))

    if request.method == 'POST':
        try:
            cart = read_cart()
            # Check if book already in cart
            existing_item = next((item for item in cart if item['book_id'] == book_id), None)
            if existing_item:
                existing_item['quantity'] += 1
            else:
                new_cart_id = next_cart_id(cart)
                cart.append({
                    'cart_id': new_cart_id,
                    'book_id': book_id,
                    'quantity': 1,
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                })
            if save_cart(cart):
                flash('Book added to cart successfully.', 'success')
            else:
                flash('Failed to add book to cart.', 'error')
        except Exception as e:
            flash('Error processing cart update.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # GET request
    try:
        reviews = read_reviews()
        book_reviews = [r for r in reviews if r['book_id'] == book_id]
    except Exception as e:
        book_reviews = []
        flash('Error loading reviews for this book.', 'error')

    return render_template('book_details.html', title='Book Details', book=book, book_reviews=book_reviews)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    try:
        cart = read_cart()
        books = read_books()
    except Exception as e:
        cart = []
        books = []
        flash('Error loading cart data.', 'error')

    # Map cart items to book details
    cart_items = []
    book_dict = {b['book_id']: b for b in books}
    total_amount = 0.0

    if request.method == 'POST':
        # Update quantities
        try:
            for item in cart:
                quantity_str = request.form.get(f'update-quantity-{item["cart_id"]}')
                if quantity_str is not None:
                    quantity = int(quantity_str)
                    if quantity <= 0:
                        quantity = 1
                    item['quantity'] = quantity
            if save_cart(cart):
                flash('Cart updated successfully.', 'success')
            else:
                flash('Failed to update cart.', 'error')
        except Exception as e:
            flash('Error updating cart.', 'error')
        return redirect(url_for('shopping_cart'))

    for item in cart:
        book = book_dict.get(item['book_id'])
        if book:
            subtotal = book['price'] * item['quantity']
            total_amount += subtotal
            cart_items.append({
                'cart_id': item['cart_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': book['price'],
                'subtotal': subtotal
            })

    return render_template('cart.html', title='Shopping Cart', cart_items=cart_items, total_amount=total_amount)

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    try:
        cart = read_cart()
        cart = [item for item in cart if item['cart_id'] != item_id]
        if save_cart(cart):
            flash('Item removed from cart.', 'success')
        else:
            flash('Failed to remove item from cart.', 'error')
    except Exception as e:
        flash('Error removing item from cart.', 'error')
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    try:
        cart = read_cart()
        books = read_books()
    except Exception as e:
        cart = []
        books = []
        flash('Error loading data for checkout.', 'error')
        return redirect(url_for('shopping_cart'))

    if not cart:
        flash('Your cart is empty. Add items before checkout.', 'error')
        return redirect(url_for('shopping_cart'))

    book_dict = {b['book_id']: b for b in books}
    total_amount = sum(book_dict[item['book_id']]['price'] * item['quantity'] for item in cart if item['book_id'] in book_dict)

    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '')

        if not customer_name:
            flash('Customer name is required.', 'error')
        elif not shipping_address:
            flash('Shipping address is required.', 'error')
        elif payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            flash('Please select a valid payment method.', 'error')
        else:
            try:
                orders = read_orders()
                order_items = read_order_items()
                new_order_id = next_order_id(orders)

                # Create order record
                new_order = {
                    'order_id': new_order_id,
                    'customer_name': customer_name,
                    'order_date': datetime.now().strftime('%Y-%m-%d'),
                    'total_amount': total_amount,
                    'status': 'Pending',
                    'shipping_address': shipping_address
                }
                orders.append(new_order)

                # Create order items and update stock
                new_order_items = []
                for item in cart:
                    book = book_dict.get(item['book_id'])
                    if book:
                        # Add order item
                        new_order_items.append({
                            'order_item_id': next_order_item_id(order_items + new_order_items),
                            'order_id': new_order_id,
                            'book_id': book['book_id'],
                            'quantity': item['quantity'],
                            'price': book['price']
                        })
                        # Reduce stock
                        if book['stock'] >= item['quantity']:
                            book['stock'] -= item['quantity']
                        else:
                            flash(f"Not enough stock for {book['title']}", 'error')
                            return redirect(url_for('shopping_cart'))

                order_items.extend(new_order_items)

                # Save orders and order items
                if not save_orders(orders) or not save_order_items(order_items):
                    flash('Failed to save order data.', 'error')
                    return redirect(url_for('shopping_cart'))

                # Save updated book stock
                if not save_books(books):
                    flash('Failed to update book stock.', 'error')
                    return redirect(url_for('shopping_cart'))

                # Clear cart
                save_cart([])

                flash('Order placed successfully!', 'success')
                return redirect(url_for('order_history'))
            except Exception as e:
                flash('Error processing order.', 'error')

    return render_template('checkout.html', title='Checkout', total_amount=total_amount)

def save_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for b in books:
                f.write(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['category']}|{b['price']}|{b['stock']}|{b['description']}\n")
        return True
    except Exception as e:
        return False

@app.route('/orders')
def order_history():
    status_filter = request.args.get('status', 'All')
    try:
        orders = read_orders()
    except Exception as e:
        orders = []
        flash('Error loading order history.', 'error')

    filtered_orders = orders
    if status_filter and status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]

    return render_template('orders.html', title='Order History', orders=filtered_orders, selected_status=status_filter)

@app.route('/order/<int:order_id>')
def order_details(order_id):
    try:
        orders = read_orders()
        order_items = read_order_items()
        books = read_books()

        order = next((o for o in orders if o['order_id'] == order_id), None)
        if not order:
            flash('Order not found.', 'error')
            return redirect(url_for('order_history'))

        items = [oi for oi in order_items if oi['order_id'] == order_id]
        book_dict = {b['book_id']: b for b in books}

        detailed_items = []
        for item in items:
            b = book_dict.get(item['book_id'])
            if b:
                detailed_items.append({
                    'title': b['title'],
                    'quantity': item['quantity'],
                    'price': item['price']
                })
    except Exception as e:
        flash('Error loading order details.', 'error')
        return redirect(url_for('order_history'))

    return render_template('order_details.html', title='Order Details', order=order, order_items=detailed_items)

@app.route('/reviews')
def reviews_page():
    rating_filter = request.args.get('rating', 'All')
    try:
        reviews = read_reviews()
        books = read_books()
    except Exception as e:
        reviews = []
        books = []
        flash('Error loading reviews.', 'error')

    if rating_filter and rating_filter != 'All':
        try:
            rating_value = int(rating_filter[0])  # e.g. '5 stars' -> 5
            reviews = [r for r in reviews if r['rating'] == rating_value]
        except Exception:
            pass

    book_dict = {b['book_id']: b for b in books}
    reviews_display = []
    for r in reviews:
        b = book_dict.get(r['book_id'])
        if b:
            reviews_display.append({
                'book_title': b['title'],
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('reviews.html', title='Customer Reviews', reviews=reviews_display, selected_rating=rating_filter)

@app.route('/write-review', methods=['GET', 'POST'])
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    try:
        # Only books that have been purchased (in orders) can be reviewed
        orders = read_orders()
        order_items = read_order_items()
        books = read_books()

        purchased_book_ids = set(oi['book_id'] for oi in order_items)
        purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]
    except Exception as e:
        purchased_books = []
        flash('Error loading books for review.', 'error')

    if request.method == 'POST':
        book_id = request.form.get('select-book')
        rating = request.form.get('rating-select')
        review_text = request.form.get('review-text', '').strip()

        errors = []
        if not book_id or not book_id.isdigit():
            errors.append('Please select a book to review.')
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            errors.append('Please select a valid rating.')
        if not review_text:
            errors.append('Review text cannot be empty.')

        if errors:
            for err in errors:
                flash(err, 'error')
        else:
            try:
                reviews = read_reviews()
                new_review_id = next_review_id(reviews)
                new_review = {
                    'review_id': new_review_id,
                    'book_id': int(book_id),
                    'customer_name': 'Anonymous',  # since no auth, anonymous user
                    'rating': int(rating),
                    'review_text': review_text,
                    'review_date': datetime.now().strftime('%Y-%m-%d')
                }
                reviews.append(new_review)
                if save_reviews(reviews):
                    flash('Review submitted successfully.', 'success')
                    return redirect(url_for('reviews_page'))
                else:
                    flash('Failed to save review.', 'error')
            except Exception as e:
                flash('Error saving review.', 'error')

    return render_template('write_review.html', title='Write a Review', purchased_books=purchased_books)

@app.route('/bestsellers')
def bestsellers_page():
    period_filter = request.args.get('period', 'This Month')
    try:
        bestsellers = read_bestsellers()
        books = read_books()
    except Exception as e:
        bestsellers = []
        books = []
        flash('Error loading bestsellers.', 'error')

    filtered_bestsellers = [b for b in bestsellers if b['period'] == period_filter]

    book_dict = {b['book_id']: b for b in books}

    bestsellers_display = []
    rank = 1
    for bs in sorted(filtered_bestsellers, key=lambda x: x['sales_count'], reverse=True):
        book = book_dict.get(bs['book_id'])
        if book:
            bestsellers_display.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })
            rank += 1

    return render_template('bestsellers.html', title='Bestsellers',
                           bestsellers=bestsellers_display, selected_period=period_filter)


if __name__ == '__main__':
    app.run(debug=True)
