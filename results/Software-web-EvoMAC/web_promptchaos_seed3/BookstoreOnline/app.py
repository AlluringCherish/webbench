'''
Main backend application for BookstoreOnline web application.
Handles routing, business logic, reading/writing local text files in data/,
and rendering HTML templates for all nine pages.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
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
# Helper to get next ID for cart, orders, order_items, reviews
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Route: Dashboard page ("/")
@app.route('/')
def dashboard():
    # Featured books: Let's pick first 3 books as featured (or less if fewer)
    books = read_books()
    featured_books = books[:3]
    # Bestsellers for "This Month" period
    bestsellers_data = read_bestsellers()
    bestsellers_this_month = [b for b in bestsellers_data if b['period'] == 'This Month']
    # Sort descending by sales_count
    bestsellers_this_month.sort(key=lambda x: x['sales_count'], reverse=True)
    # Join with book info
    books_dict = {b['book_id']: b for b in books}
    bestsellers = []
    for b in bestsellers_this_month:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
    return render_template('dashboard.html',
                           featured_books=featured_books,
                           bestsellers=bestsellers)
# Route: Book Catalog page
@app.route('/catalog', methods=['GET'])
def catalog():
    books = read_books()
    categories = read_categories()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_books = books
    if search_query:
        filtered_books = [b for b in filtered_books if
                          search_query in b['title'].lower() or
                          search_query in b['author'].lower() or
                          search_query in b['isbn'].lower()]
    if category_filter and category_filter != 'All':
        filtered_books = [b for b in filtered_books if b['category'] == category_filter]
    return render_template('catalog.html',
                           books=filtered_books,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
# Route: Book Details page
@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    if request.method == 'POST':
        # Add to cart action
        quantity = request.form.get('quantity', '1')
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1
        cart_items = read_cart()
        # Check if book already in cart, update quantity
        existing_item = None
        for item in cart_items:
            if item['book_id'] == book_id:
                existing_item = item
                break
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            new_cart_id = get_next_id(cart_items, 'cart_id')
            added_date = datetime.now().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': added_date
            })
        write_cart(cart_items)
        return redirect(url_for('cart'))
    return render_template('book_details.html',
                           book=book,
                           reviews=book_reviews)
# Route: Shopping Cart page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    books = read_books()
    cart_items = read_cart()
    books_dict = {b['book_id']: b for b in books}
    if request.method == 'POST':
        # Handle update quantities or remove items
        form = request.form
        cart_changed = False
        # Update quantities
        for item in cart_items[:]:
            qty_field = f'update-quantity-{item["cart_id"]}'
            remove_field = f'remove-item-button-{item["cart_id"]}'
            if remove_field in form:
                # Remove this item
                cart_items.remove(item)
                cart_changed = True
                continue
            if qty_field in form:
                try:
                    new_qty = int(form[qty_field])
                    if new_qty < 1:
                        # Remove item if quantity less than 1
                        cart_items.remove(item)
                    else:
                        item['quantity'] = new_qty
                    cart_changed = True
                except:
                    pass
        if cart_changed:
            write_cart(cart_items)
        return redirect(url_for('cart'))
    # Prepare cart display data
    display_items = []
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
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
# Route: Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = read_cart()
    if not cart_items:
        # No items in cart, redirect to catalog or dashboard
        return redirect(url_for('catalog'))
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    # Calculate total amount
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if book:
            total_amount += book['price'] * item['quantity']
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not shipping_address or not payment_method:
            error = "Please fill in all required fields."
            return render_template('checkout.html',
                                   total_amount=total_amount,
                                   error=error,
                                   customer_name=customer_name,
                                   shipping_address=shipping_address,
                                   payment_method=payment_method)
        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        new_order_id = get_next_id(orders, 'order_id')
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
        write_orders(orders)
        # Add order items
        next_order_item_id = int(get_next_id(order_items, 'order_item_id'))
        for item in cart_items:
            book = books_dict.get(item['book_id'])
            if not book:
                continue
            order_item = {
                'order_item_id': str(next_order_item_id),
                'order_id': new_order_id,
                'book_id': book['book_id'],
                'quantity': item['quantity'],
                'price': book['price']
            }
            order_items.append(order_item)
            next_order_item_id += 1
        write_order_items(order_items)
        # Clear cart after order placed
        write_cart([])
        return redirect(url_for('order_history'))
    return render_template('checkout.html',
                           total_amount=total_amount)
# Route: Order History page
@app.route('/orders', methods=['GET'])
def order_history():
    orders = read_orders()
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]
    else:
        filtered_orders = orders
    return render_template('order_history.html',
                           orders=filtered_orders,
                           selected_status=status_filter)
# Route: View Order Details page (not explicitly in requirements but needed for view-order-button)
@app.route('/order/<order_id>', methods=['GET'])
def order_details(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    order_items = read_order_items()
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    items = []
    for item in order_items:
        if item['order_id'] == order_id:
            book = books_dict.get(item['book_id'])
            if book:
                items.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'subtotal': item['price'] * item['quantity']
                })
    return render_template('order_details.html',
                           order=order,
                           items=items)
# Route: Reviews page
@app.route('/reviews', methods=['GET'])
def reviews():
    reviews = read_reviews()
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    rating_filter = request.args.get('rating', 'All')
    filtered_reviews = reviews
    if rating_filter != 'All':
        try:
            rating_val = int(rating_filter[0])  # e.g. "5 stars" -> 5
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    # Prepare display list with book title
    display_reviews = []
    for r in filtered_reviews:
        book = books_dict.get(r['book_id'])
        if book:
            display_reviews.append({
                'review_id': r['review_id'],
                'book_title': book['title'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'customer_name': r['customer_name'],
                'review_date': r['review_date']
            })
    return render_template('reviews.html',
                           reviews=display_reviews,
                           selected_rating=rating_filter)
# Route: Write Review page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'POST':
        book_id = request.form.get('select-book', '').strip()
        rating = request.form.get('rating-select', '').strip()
        review_text = request.form.get('review-text', '').strip()
        customer_name = "Anonymous"  # Since no authentication, use generic or could ask user
        if not book_id or not rating or not review_text:
            error = "Please fill in all fields."
            return render_template('write_review.html',
                                   books=books,
                                   error=error,
                                   selected_book=book_id,
                                   selected_rating=rating,
                                   review_text=review_text)
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError
        except:
            error = "Invalid rating value."
            return render_template('write_review.html',
                                   books=books,
                                   error=error,
                                   selected_book=book_id,
                                   selected_rating=rating,
                                   review_text=review_text)
        reviews = read_reviews()
        new_review_id = get_next_id(reviews, 'review_id')
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
        return redirect(url_for('reviews'))
    return render_template('write_review.html', books=books)
# Route: Bestsellers page
@app.route('/bestsellers', methods=['GET'])
def bestsellers():
    books = read_books()
    bestsellers_data = read_bestsellers()
    time_period = request.args.get('time_period', 'This Month')
    filtered_bestsellers = [b for b in bestsellers_data if b['period'] == time_period]
    # Sort descending by sales_count
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)
    books_dict = {b['book_id']: b for b in books}
    bestsellers_list = []
    rank = 1
    for b in filtered_bestsellers:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers_list.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
            rank += 1
    return render_template('bestsellers.html',
                           bestsellers=bestsellers_list,
                           selected_period=time_period)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)