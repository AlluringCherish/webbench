from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_candidate_b')
app.secret_key = 'secret_key_for_session'  # Needed for flash messaging

data_dir = 'data'

# Utility functions for file operations and data parsing

def read_books():
    books = []
    try:
        with open(os.path.join(data_dir, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 8:
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
        flash('Books data file not found.', 'error')
    return books


def read_categories():
    categories = []
    try:
        with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        category = {
                            'category_id': int(parts[0]),
                            'category_name': parts[1],
                            'description': parts[2]
                        }
                        categories.append(category)
    except FileNotFoundError:
        flash('Categories data file not found.', 'error')
    return categories


def read_cart():
    cart_items = []
    try:
        with open(os.path.join(data_dir, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        cart_item = {
                            'cart_id': int(parts[0]),
                            'book_id': int(parts[1]),
                            'quantity': int(parts[2]),
                            'added_date': parts[3]
                        }
                        cart_items.append(cart_item)
    except FileNotFoundError:
        pass  # No cart initially
    return cart_items


def write_cart(cart_items):
    try:
        with open(os.path.join(data_dir, 'cart.txt'), 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except Exception as e:
        flash(f'Error saving cart data: {e}', 'error')
        return False


def read_orders():
    orders = []
    try:
        with open(os.path.join(data_dir, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 6:
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


def write_order(order):
    try:
        with open(os.path.join(data_dir, 'orders.txt'), 'a', encoding='utf-8') as f:
            line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}\n"
            f.write(line)
        return True
    except Exception as e:
        flash(f'Error saving order data: {e}', 'error')
        return False


def read_order_items():
    order_items = []
    try:
        with open(os.path.join(data_dir, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        order_item = {
                            'order_item_id': int(parts[0]),
                            'order_id': int(parts[1]),
                            'book_id': int(parts[2]),
                            'quantity': int(parts[3]),
                            'price': float(parts[4])
                        }
                        order_items.append(order_item)
    except FileNotFoundError:
        pass
    return order_items


def write_order_items(new_order_items):
    try:
        with open(os.path.join(data_dir, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for item in new_order_items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}\n"
                f.write(line)
        return True
    except Exception as e:
        flash(f'Error saving order items data: {e}', 'error')
        return False


def read_reviews():
    reviews = []
    try:
        with open(os.path.join(data_dir, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 6:
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


def write_review(new_review):
    try:
        with open(os.path.join(data_dir, 'reviews.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_review['review_id']}|{new_review['book_id']}|{new_review['customer_name']}|{new_review['rating']}|{new_review['review_text']}|{new_review['review_date']}\n"
            f.write(line)
        return True
    except Exception as e:
        flash(f'Error saving review data: {e}', 'error')
        return False


def read_bestsellers():
    bestsellers = []
    try:
        with open(os.path.join(data_dir, 'bestsellers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        bs = {
                            'book_id': int(parts[0]),
                            'sales_count': int(parts[1]),
                            'period': parts[2]
                        }
                        bestsellers.append(bs)
    except FileNotFoundError:
        pass
    return bestsellers


def get_next_cart_id(cart_items):
    if not cart_items:
        return 1
    return max(item['cart_id'] for item in cart_items) + 1

def get_next_order_id(orders):
    if not orders:
        return 1
    return max(order['order_id'] for order in orders) + 1

def get_next_order_item_id(order_items):
    if not order_items:
        return 1
    return max(item['order_item_id'] for item in order_items) + 1

def get_next_review_id(reviews):
    if not reviews:
        return 1
    return max(r['review_id'] for r in reviews) + 1


def find_book_by_id(book_id):
    books = read_books()
    for book in books:
        if book['book_id'] == book_id:
            return book
    return None


def find_category_name(cat_name):
    categories = read_categories()
    for c in categories:
        if c['category_name'] == cat_name:
            return c['category_name']
    return None


def find_order_by_id(order_id):
    orders = read_orders()
    for order in orders:
        if order['order_id'] == order_id:
            return order
    return None

def find_cart_item_by_id(item_id):
    cart = read_cart()
    for item in cart:
        if item['cart_id'] == item_id:
            return item
    return None


@app.route('/')
@app.route('/dashboard')
def dashboard():
    books = read_books()
    # For featured books, select first 5 or all if less
    featured_books = books[:5]
    return render_template('dashboard.html', 
                           featured_books=featured_books, 
                           page_title='Bookstore Dashboard')


@app.route('/catalog')
def book_catalog():
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').strip().lower()
    selected_category = request.args.get('category', '')

    filtered_books = []
    for book in books:
        # Filter by category if selected
        if selected_category and selected_category != '':
            if book['category'] != selected_category:
                continue
        # Filter by search query
        if search_query:
            if (search_query not in book['title'].lower() and
                search_query not in book['author'].lower() and
                search_query not in book['isbn'].lower()):
                continue
        filtered_books.append(book)

    return render_template('catalog.html', 
                            books=filtered_books, 
                            categories=categories, 
                            search_query=search_query,
                            selected_category=selected_category, 
                            page_title='Book Catalog')


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = find_book_by_id(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('book_catalog'))

    if request.method == 'POST':
        cart_items = read_cart()
        # Check stock availability
        quantity_to_add = 1
        if book['stock'] <= 0:
            flash('Sorry, this book is out of stock.', 'error')
            return redirect(url_for('book_details', book_id=book_id))

        # Check if book already in cart
        existing = None
        for item in cart_items:
            if item['book_id'] == book_id:
                existing = item
                break

        if existing:
            if existing['quantity'] + quantity_to_add > book['stock']:
                flash('Cannot add more than available stock to cart.', 'error')
                return redirect(url_for('book_details', book_id=book_id))
            existing['quantity'] += quantity_to_add
        else:
            new_cart_id = get_next_cart_id(cart_items)
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity_to_add,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })

        if write_cart(cart_items):
            flash('Book added to cart successfully.', 'success')
        else:
            flash('Failed to add book to cart.', 'error')
        return redirect(url_for('book_details', book_id=book_id))

    # GET request: show reviews for this book
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    # Sort reviews by date descending
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)

    return render_template('book_details.html', 
                           book=book,
                           reviews=book_reviews, 
                           page_title='Book Details')


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = read_cart()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    if request.method == 'POST':
        # Update quantities
        updated = False
        for item in cart_items:
            key = f'quantity_{item["cart_id"]}'
            if key in request.form:
                try:
                    qty = int(request.form[key])
                    if qty < 1:
                        qty = 1
                    # Check stock availability
                    book_stock = book_dict.get(item['book_id'], {}).get('stock', 0)
                    if qty > book_stock:
                        flash(f'Cannot set quantity greater than stock for {book_dict[item["book_id"]]["title"]}.', 'error')
                        return redirect(url_for('shopping_cart'))
                    item['quantity'] = qty
                    updated = True
                except ValueError:
                    flash('Invalid quantity input.', 'error')
                    return redirect(url_for('shopping_cart'))

        if updated:
            if write_cart(cart_items):
                flash('Cart updated successfully.', 'success')
            else:
                flash('Failed to update cart.', 'error')

        return redirect(url_for('shopping_cart'))

    # GET request: display cart
    display_cart = []
    total_amount = 0.0
    for item in cart_items:
        book = book_dict.get(item['book_id'])
        if not book:
            continue
        subtotal = item['quantity'] * book['price']
        display_cart.append({
            'cart_id': item['cart_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal
        })
        total_amount += subtotal

    return render_template('cart.html', 
                           cart_items=display_cart, 
                           total_amount=total_amount,
                           page_title='Shopping Cart')


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_items = read_cart()
    cart_items = [item for item in cart_items if item['cart_id'] != item_id]
    if write_cart(cart_items):
        flash('Item removed from cart.', 'success')
    else:
        flash('Failed to remove item from cart.', 'error')
    return redirect(url_for('shopping_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = read_cart()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    if not cart_items:
        flash('Your cart is empty. Add items before checkout.', 'error')
        return redirect(url_for('shopping_cart'))

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '')

        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            flash('Please fill all fields and select a valid payment method.', 'error')
            return redirect(url_for('checkout'))

        # Calculate total amount
        total_amount = 0.0
        for item in cart_items:
            book = book_dict.get(item['book_id'])
            if book:
                total_amount += item['quantity'] * book['price']

        orders = read_orders()
        order_id = get_next_order_id(orders)

        order = {
            'order_id': order_id,
            'customer_name': customer_name,
            'order_date': datetime.now().strftime('%Y-%m-%d'),
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }

        if write_order(order):
            # Write order items
            order_items = read_order_items()
            next_order_item_id = get_next_order_item_id(order_items)

            new_order_items = []
            for item in cart_items:
                book = book_dict.get(item['book_id'])
                if book:
                    new_order_items.append({
                        'order_item_id': next_order_item_id,
                        'order_id': order_id,
                        'book_id': book['book_id'],
                        'quantity': item['quantity'],
                        'price': book['price']
                    })
                    next_order_item_id += 1

            write_order_items(new_order_items)

            # Clear cart
            if write_cart([]):
                flash('Order placed successfully.', 'success')
            else:
                flash('Order placed but failed to clear cart.', 'error')

            return redirect(url_for('order_history'))

        else:
            flash('Failed to place order.', 'error')
            return redirect(url_for('checkout'))

    # GET request
    return render_template('checkout.html', 
                           page_title='Checkout')


@app.route('/orders')
def order_history():
    orders = read_orders()
    status_filter = request.args.get('status', 'All')

    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]

    return render_template('orders.html', 
                           orders=orders,
                           status_filter=status_filter,
                           page_title='Order History')


@app.route('/order/<int:order_id>')
def order_details(order_id):
    order = find_order_by_id(order_id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('order_history'))

    order_items = read_order_items()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    order_items_for_order = [item for item in order_items if item['order_id'] == order_id]

    display_items = []
    for item in order_items_for_order:
        book = book_dict.get(item['book_id'])
        if book:
            display_items.append({
                'title': book['title'],
                'quantity': item['quantity'],
                'price': item['price']
            })

    return render_template('order_details.html', 
                           order=order,
                           order_items=display_items, 
                           page_title='Order Details')


@app.route('/reviews')
def reviews_page():
    reviews = read_reviews()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    rating_filter = request.args.get('rating', 'All')
    if rating_filter != 'All':
        try:
            rating_val = int(rating_filter.split()[0])
            reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass

    display_reviews = []
    for r in reviews:
        book = book_dict.get(r['book_id'])
        if book:
            display_reviews.append({
                'book_title': book['title'],
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('reviews.html', 
                           reviews=display_reviews,
                           rating_filter=rating_filter,
                           page_title='Customer Reviews')


@app.route('/write-review', methods=['GET', 'POST'])
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    if request.method == 'POST':
        book_id = request.form.get('select_book')
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()
        customer_name = 'Anonymous'

        if not book_id or not rating or not review_text:
            flash('Please complete all fields to submit a review.', 'error')
            return redirect(url_for('write_review'))

        try:
            book_id = int(book_id)
            rating_val = int(rating)
            if rating_val < 1 or rating_val > 5:
                raise ValueError
        except ValueError:
            flash('Invalid input values.', 'error')
            return redirect(url_for('write_review'))

        reviews = read_reviews()
        review_id = get_next_review_id(reviews)

        new_review = {
            'review_id': review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating_val,
            'review_text': review_text,
            'review_date': datetime.now().strftime('%Y-%m-%d')
        }

        if write_review(new_review):
            flash('Review submitted successfully.', 'success')
            return redirect(url_for('reviews_page'))
        else:
            flash('Failed to submit review.', 'error')
            return redirect(url_for('write_review'))

    return render_template('write_review.html', 
                           books=books,
                           page_title='Write a Review')


@app.route('/bestsellers')
def bestsellers_page():
    bestsellers = read_bestsellers()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}

    period_filter = request.args.get('period', 'This Month')

    filtered_bs = [bs for bs in bestsellers if bs['period'] == period_filter]
    # Sort by sales_count desc
    filtered_bs.sort(key=lambda x: x['sales_count'], reverse=True)

    display_bs = []
    rank = 1
    for bs in filtered_bs:
        book = book_dict.get(bs['book_id'])
        if book:
            display_bs.append({
                'rank': rank,
                'book_id': bs['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })
            rank += 1

    return render_template('bestsellers.html', 
                           bestsellers=display_bs, 
                           period_filter=period_filter, 
                           page_title='Bestsellers')


if __name__ == '__main__':
    app.run(debug=True)
