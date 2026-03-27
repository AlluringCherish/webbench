from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to read/write data files with pipe-delimited fields

DATA_DIR = 'data'

# --- Data File Paths ---
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
CART_FILE = os.path.join(DATA_DIR, 'cart.txt')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.txt')
ORDER_ITEMS_FILE = os.path.join(DATA_DIR, 'order_items.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
BESTSELLERS_FILE = os.path.join(DATA_DIR, 'bestsellers.txt')

# --- Utility functions for reading and writing data ---

def read_books():
    books = []
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue  # Skip malformed lines
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
    except Exception as e:
        # Log the error, in production use logging module
        print(f"Error reading books file: {e}")
    return books


def read_categories():
    categories = []
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
    except Exception as e:
        print(f"Error reading categories file: {e}")
    return categories


def read_cart():
    cart_items = []
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                cart_item = {
                    'cart_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }
                cart_items.append(cart_item)
    except FileNotFoundError:
        # Cart file missing, treat as empty cart
        pass
    except Exception as e:
        print(f"Error reading cart file: {e}")
    return cart_items


def write_cart(cart_items):
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error writing cart file: {e}")


def read_orders():
    orders = []
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
    except Exception as e:
        print(f"Error reading orders file: {e}")
    return orders


def read_order_items():
    order_items = []
    try:
        with open(ORDER_ITEMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(item)
    except Exception as e:
        print(f"Error reading order items file: {e}")
    return order_items


def read_reviews():
    reviews = []
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
    except Exception as e:
        print(f"Error reading reviews file: {e}")
    return reviews


def write_reviews(reviews):
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error writing reviews file: {e}")


def read_bestsellers():
    bestsellers = []
    try:
        with open(BESTSELLERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
    except Exception as e:
        print(f"Error reading bestsellers file: {e}")
    return bestsellers


# --- Flask Routes Implementations ---

@app.route('/')
def root_redirect():
    # Redirect root to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load books and bestsellers for dashboard
    books = read_books()
    bestsellers_data = read_bestsellers()

    # Prepare featured_books: choose 4 featured books (e.g. first 4 from books)
    featured_books = []
    for book in books[:4]:
        featured_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price']
        })

    # Prepare bestsellers for "All Time" or latest available period (example simplification)
    # We aggregate bestsellers for 'All Time' if exist, else 'This Month' if exist else just all
    periods = ['All Time', 'This Month', 'This Week']
    selected_period = None
    for p in periods:
        filtered = [bs for bs in bestsellers_data if bs['period'] == p]
        if filtered:
            selected_period = p
            bestsellers_filtered = filtered
            break
    else:
        bestsellers_filtered = bestsellers_data

    # Sort by sales_count descending
    bestsellers_filtered.sort(key=lambda x: x['sales_count'], reverse=True)

    bestsellers = []
    book_dict = {b['book_id']: b for b in books}
    rank = 1
    for bs in bestsellers_filtered[:5]:  # Top 5
        book = book_dict.get(bs['book_id'])
        if not book:
            continue
        bestsellers.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price'],
            'rank': rank,
            'sales_count': bs['sales_count']
        })
        rank += 1

    # context vars for dashboard
    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


@app.route('/catalog')
def book_catalog():
    # Get query parameters for filtering
    search_query = request.args.get('search_query', '', type=str).strip()
    selected_category_id = request.args.get('selected_category_id', '', type=str)
    try:
        selected_category_id_int = int(selected_category_id) if selected_category_id else None
    except ValueError:
        selected_category_id_int = None

    books = read_books()
    categories = read_categories()

    # Filter books by category if selected_category_id is not None
    if selected_category_id_int is not None:
        # Map category name from categories
        category_map = {c['category_id']: c['category_name'] for c in categories}
        category_name = category_map.get(selected_category_id_int)
        if category_name:
            books = [b for b in books if b['category'] == category_name]
        else:
            # No matching category, empty result
            books = []

    # Filter books by search query: search in title, author, isbn (case-insensitive)
    if search_query:
        search_lower = search_query.lower()
        books = [b for b in books if (search_lower in b['title'].lower() or
                                        search_lower in b['author'].lower() or
                                        search_lower in b['isbn'].lower())]

    # Prepare books list dicts with required keys
    books_out = []
    for b in books:
        entry = {
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'category': b['category']
        }
        books_out.append(entry)

    # categories exclude description in template context
    categories_out = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('catalog.html', books=books_out, categories=categories_out,
                           search_query=search_query, selected_category_id=selected_category_id_int)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = b
            break
    if book is None:
        # Book not found: could render 404 or redirect to catalog
        return redirect(url_for('book_catalog'))

    if request.method == 'POST':
        # Handle adding to cart
        quantity_str = request.form.get('quantity', '0').strip()
        try:
            quantity = int(quantity_str)
        except ValueError:
            quantity = 0

        if quantity < 1 or quantity > book['stock']:
            # Invalid quantity, we could flash message or ignore
            return render_template('book_details.html', book=book, reviews=[], error='Invalid quantity')

        # Add to cart logic
        cart_items = read_cart()
        # Check if book already in cart
        existing_item = None
        for item in cart_items:
            if item['book_id'] == book_id:
                existing_item = item
                break

        if existing_item:
            # Update existing quantity
            new_quantity = existing_item['quantity'] + quantity
            if new_quantity > book['stock']:
                # Cap to stock
                new_quantity = book['stock']
            existing_item['quantity'] = new_quantity
        else:
            # Add new cart item - find next cart_id
            max_cart_id = max([item['cart_id'] for item in cart_items], default=0)
            new_cart_id = max_cart_id + 1
            today_date = datetime.now().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_date
            })

        write_cart(cart_items)

        # Redirect to cart after adding
        return redirect(url_for('shopping_cart'))

    # GET method
    reviews_data = read_reviews()
    # Filter reviews for this book
    book_reviews = [r for r in reviews_data if r['book_id'] == book_id]

    # Sort by review_date descending
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)

    context_reviews = []
    for r in book_reviews:
        context_reviews.append({
            'review_id': r['review_id'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    # Prepare book dict with required keys for template
    book_out = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'price': book['price'],
        'description': book['description'],
        'stock': book['stock']
    }

    return render_template('book_details.html', book=book_out, reviews=context_reviews)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        # Handle updates or removals
        cart_items = read_cart()
        form = request.form

        # To detect removal action, we check if any remove button submitted
        # Remove buttons named 'remove_{cart_id}' are submitted on removal

        # Collect removal cart_ids
        removals = []
        updates = {}
        # Form keys: cart_id, quantity, remove buttons
        # We check keys that start with 'remove_item_'
        for key in form.keys():
            if key.startswith('remove_item_'):
                val = form.get(key)
                if val:
                    try:
                        rcid = int(key[len('remove_item_'):])
                        removals.append(rcid)
                    except Exception:
                        pass

        # If no removals, process quantity update
        if removals:
            # Remove those items
            cart_items = [ci for ci in cart_items if ci['cart_id'] not in removals]
        else:
            # Update quantities
            for key in form.keys():
                if key.startswith('quantity_'):
                    try:
                        cid = int(key[len('quantity_'):])
                        qty_str = form.get(key).strip()
                        qty = int(qty_str)
                        if qty < 1:
                            qty = 1
                        updates[cid] = qty
                    except Exception:
                        continue
            # Apply updates
            for ci in cart_items:
                if ci['cart_id'] in updates:
                    # Cap quantity to stock
                    books = read_books()
                    book_for_item = next((b for b in books if b['book_id'] == ci['book_id']), None)
                    if book_for_item:
                        if updates[ci['cart_id']] > book_for_item['stock']:
                            ci['quantity'] = book_for_item['stock']
                        else:
                            ci['quantity'] = updates[ci['cart_id']]

        write_cart(cart_items)

        return redirect(url_for('shopping_cart'))

    # GET method
    cart_items = read_cart()
    books = read_books()

    # Build cart_items with details
    cart_display = []
    total_amount = 0.0
    for item in cart_items:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book is None:
            continue
        subtotal = item['quantity'] * book['price']
        total_amount += subtotal
        cart_display.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': round(subtotal, 2)
        })

    total_amount = round(total_amount, 2)

    return render_template('cart.html', cart_items=cart_display, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            # Invalid inputs, re-render form or show error
            return render_template('checkout.html', error='Invalid input')

        cart_items = read_cart()
        books = read_books()

        # Calculate order total
        total_amount = 0.0
        for item in cart_items:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if book:
                total_amount += item['quantity'] * book['price']

        total_amount = round(total_amount, 2)

        if total_amount == 0.0:
            # Cart empty or no valid items
            return render_template('checkout.html', error='Cart is empty')

        orders = read_orders()
        order_items = read_order_items()

        # Assign new order_id
        max_order_id = max((o['order_id'] for o in orders), default=0)
        new_order_id = max_order_id + 1

        today_date = datetime.now().strftime('%Y-%m-%d')

        # Add new order
        orders.append({
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        })

        # Add order items
        max_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0)
        current_order_item_id = max_order_item_id + 1
        for item in cart_items:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if book:
                order_items.append({
                    'order_item_id': current_order_item_id,
                    'order_id': new_order_id,
                    'book_id': book['book_id'],
                    'quantity': item['quantity'],
                    'price': book['price']
                })
                current_order_item_id += 1

        # Write updated orders and order items
        try:
            with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
                for o in orders:
                    line = f"{o['order_id']}|{o['customer_name']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['shipping_address']}\n"
                    f.write(line)
        except Exception as e:
            print(f"Error writing orders file: {e}")

        try:
            with open(ORDER_ITEMS_FILE, 'w', encoding='utf-8') as f:
                for oi in order_items:
                    line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['book_id']}|{oi['quantity']}|{oi['price']}\n"
                    f.write(line)
        except Exception as e:
            print(f"Error writing order items file: {e}")

        # Clear cart after order
        write_cart([])

        # Redirect to order history page
        return redirect(url_for('order_history'))

    # GET method
    return render_template('checkout.html')


@app.route('/orders')
def order_history():
    status_filter = request.args.get('status', 'All')
    orders = read_orders()

    # Filter by status if not 'All'
    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]

    # Prepare orders for template
    orders_out = []
    for o in orders:
        orders_out.append({
            'order_id': o['order_id'],
            'customer_name': o['customer_name'],
            'order_date': o['order_date'],
            'total_amount': o['total_amount'],
            'status': o['status']
        })

    return render_template('orders.html', orders=orders_out, status_filter=status_filter)


@app.route('/reviews')
def reviews_page():
    rating_filter = request.args.get('rating', 'All')
    reviews = read_reviews()
    books = read_books()

    # Build book id to title mapping
    book_title_map = {b['book_id']: b['title'] for b in books}

    # Filter reviews by rating if not 'All'
    filtered_reviews = []
    if rating_filter == 'All':
        filtered_reviews = reviews
    else:
        try:
            rating_int = int(rating_filter)
            filtered_reviews = [r for r in reviews if r['rating'] == rating_int]
        except ValueError:
            # Invalid rating filter, default to all
            filtered_reviews = reviews

    # Prepare context reviews
    reviews_out = []
    for r in filtered_reviews:
        book_title = book_title_map.get(r['book_id'], 'Unknown')
        reviews_out.append({
            'review_id': r['review_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('reviews.html', reviews=reviews_out, rating_filter=rating_filter)


@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    # For simplicity, assume the customer name is anonymous or hardcoded (not specified in spec)
    # To find purchased_books eligible for review, we consider books from past orders
    orders = read_orders()
    order_items = read_order_items()
    books = read_books()

    # Gather all purchased book_ids
    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    # Prepare purchased_books list
    purchased_books = []
    book_map = {b['book_id']: b for b in books}
    for book_id in purchased_book_ids:
        book = book_map.get(book_id)
        if book:
            purchased_books.append({'book_id': book_id, 'title': book['title']})

    if request.method == 'POST':
        # Handle submitted review
        book_id_str = request.form.get('book_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        try:
            book_id = int(book_id_str)
            rating = int(rating_str)
        except ValueError:
            return render_template('write_review.html', purchased_books=purchased_books, error='Invalid input')

        if rating < 1 or rating > 5 or not review_text:
            return render_template('write_review.html', purchased_books=purchased_books, error='Invalid rating or empty review')

        # Generate new review_id
        reviews = read_reviews()
        max_review_id = max((r['review_id'] for r in reviews), default=0)
        new_review_id = max_review_id + 1

        today_date = datetime.now().strftime('%Y-%m-%d')

        # Assume anonymous customer name (not specified)
        customer_name = 'Anonymous'

        reviews.append({
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_date
        })

        write_reviews(reviews)

        return redirect(url_for('reviews_page'))

    # GET method
    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers')
def bestsellers_page():
    # Get time period filter from query param
    time_period = request.args.get('period', 'All Time')

    bestsellers_data = read_bestsellers()
    books = read_books()

    # Filter bestsellers by period
    filtered_bs = [bs for bs in bestsellers_data if bs['period'] == time_period]
    if not filtered_bs:
        # If none for requested period, show all
        filtered_bs = bestsellers_data

    # Sort by sales_count descending
    filtered_bs.sort(key=lambda x: x['sales_count'], reverse=True)

    book_map = {b['book_id']: b for b in books}

    bestsellers_out = []
    rank = 1
    for bs in filtered_bs:
        book = book_map.get(bs['book_id'])
        if not book:
            continue
        bestsellers_out.append({
            'rank': rank,
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'sales_count': bs['sales_count']
        })
        rank += 1

    return render_template('bestsellers.html', bestsellers=bestsellers_out, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
