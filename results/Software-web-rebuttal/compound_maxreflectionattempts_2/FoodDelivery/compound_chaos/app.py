from flask import Flask, render_template, redirect, url_for, request, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os
from datetime import datetime

DATA_DIR = 'data'

# Utility functions to load data

def load_restaurants():
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                restaurants.append({
                    'restaurant_id': int(parts[0]),
                    'name': parts[1],
                    'cuisine': parts[2],
                    'address': parts[3],
                    'phone': parts[4],
                    'rating': float(parts[5]),
                    'delivery_time': int(parts[6]),
                    'min_order': float(parts[7])
                })
    except IOError:
        pass
    return restaurants


def load_menus():
    path = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                menus.append({
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                })
    except IOError:
        pass
    return menus


def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                cart.append({
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                })
    except IOError:
        pass
    return cart


def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                orders.append({
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                })
    except IOError:
        pass
    return orders


def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                order_items.append({
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                })
    except IOError:
        pass
    return order_items


def load_deliveries():
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                deliveries.append({
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]
                })
    except IOError:
        pass
    return deliveries


def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                reviews.append({
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                })
    except IOError:
        pass
    return reviews


# Write functions to save cart and reviews (only these will be mutated)

def save_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
    except IOError:
        pass


def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for review in reviews:
                line = f"{review['review_id']}|{review['restaurant_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
                f.write(line)
    except IOError:
        pass


# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Dashboard page
@app.route('/dashboard')
def dashboard_page():
    restaurants = load_restaurants()
    # Featured restaurants: top 5 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]
    # Popular cuisines: all cuisines sorted alphabetically, unique
    cuisines = {r['cuisine'] for r in restaurants}
    popular_cuisines = sorted(cuisines)
    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)


# Browse restaurants with filter and search query
@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    cuisine_options = sorted({r['cuisine'] for r in restaurants})
    selected_cuisine = request.args.get('cuisine')
    search_query = request.args.get('search')

    filtered = restaurants
    if selected_cuisine and selected_cuisine in cuisine_options:
        filtered = [r for r in filtered if r['cuisine'] == selected_cuisine]
    if search_query:
        filtered = [r for r in filtered if search_query.lower() in r['name'].lower()]

    return render_template('restaurants.html', restaurants=filtered, cuisine_options=cuisine_options, selected_cuisine=selected_cuisine if selected_cuisine in cuisine_options else None, search_query=search_query if search_query else None)


# Restaurant menu by restaurant_id
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if restaurant is None:
        abort(404)
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


# Item details by item_id
@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if item is None:
        abort(404)
    return render_template('item_details.html', item=item)


# Add item to cart (item_id path param) POST
@app.route('/item/<int:item_id>/add_to_cart', methods=['POST'])
def add_item_to_cart(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if item is None:
        abort(404)

    quantity_raw = request.form.get('quantity')
    try:
        quantity = int(quantity_raw) if quantity_raw else 1
    except ValueError:
        quantity = 1
    if quantity < 1:
        quantity = 1

    cart = load_cart()

    # Check if this item already in cart (by item_id and restaurant_id)
    existing = None
    for c in cart:
        if c['item_id'] == item_id and c['restaurant_id'] == item['restaurant_id']:
            existing = c
            break

    if existing:
        existing['quantity'] += quantity
    else:
        new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        added_date = datetime.now().strftime('%Y-%m-%d')
        cart.append({'cart_id': new_cart_id, 'item_id': item_id, 'restaurant_id': item['restaurant_id'], 'quantity': quantity, 'added_date': added_date})

    save_cart(cart)

    return redirect(url_for('shopping_cart'))


# Shopping cart GET and POST
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        # To update quantities maybe? But there's a separate update route specified
        return redirect(url_for('shopping_cart'))

    cart = load_cart()
    menus = load_menus()
    cart_items = []
    total_amount = 0.0
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item is None:
            continue
        subtotal = item['price'] * c['quantity']
        total_amount += subtotal
        cart_items.append({
            'cart_id': c['cart_id'],
            'item_id': c['item_id'],
            'restaurant_id': c['restaurant_id'],
            'item_name': item['item_name'],
            'category': item['category'],
            'quantity': c['quantity'],
            'price': item['price'],
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# Update cart quantity POST
@app.route('/cart/update_quantity', methods=['POST'])
def update_cart_quantity():
    item_id_raw = request.form.get('item_id')
    quantity_raw = request.form.get('quantity')

    try:
        item_id = int(item_id_raw)
        quantity = int(quantity_raw)
    except (ValueError, TypeError):
        return redirect(url_for('shopping_cart'))

    cart = load_cart()

    # Find the cart item with this item_id
    found = False
    for c in cart:
        if c['item_id'] == item_id:
            found = True
            if quantity > 0:
                c['quantity'] = quantity
            else:
                # Remove item if quantity <= 0
                cart.remove(c)
            break

    if found:
        save_cart(cart)
    return redirect(url_for('shopping_cart'))


# Remove cart item POST
@app.route('/cart/remove_item/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart = load_cart()
    cart = [c for c in cart if c['item_id'] != item_id]
    save_cart(cart)
    return redirect(url_for('shopping_cart'))


# Checkout page GET
@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')


# Place order POST
@app.route('/checkout/place_order', methods=['POST'])
def place_order():
    customer_name = request.form.get('customer_name')
    delivery_address = request.form.get('delivery_address')
    phone_number = request.form.get('phone_number')
    payment_method = request.form.get('payment_method')

    # Validate minimal inputs
    if not customer_name or not delivery_address or not phone_number or not payment_method:
        # Could optionally flash error, but per spec no extra
        return redirect(url_for('checkout_page'))

    cart = load_cart()
    if not cart:
        # Empty cart, redirect back
        return redirect(url_for('shopping_cart'))

    menus = load_menus()
    restaurants = load_restaurants()

    # Collect unique restaurant_ids from cart
    restaurant_ids = {c['restaurant_id'] for c in cart}

    # Per spec no split orders, so allow only one restaurant in cart
    if len(restaurant_ids) > 1:
        # Redirect back to cart with no change
        return redirect(url_for('shopping_cart'))

    restaurant_id = restaurant_ids.pop()

    # Calculate total_amount
    total_amount = 0.0
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            total_amount += item['price'] * c['quantity']

    orders = load_orders()
    order_items = load_order_items()

    new_order_id = max([o['order_id'] for o in orders], default=0) + 1
    order_date_str = datetime.now().strftime('%Y-%m-%d')
    status = 'Received'

    # Append new order
    orders.append({
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date_str,
        'total_amount': total_amount,
        'status': status,
        'delivery_address': delivery_address,
        'phone_number': phone_number
    })

    # Append order items
    new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            order_items.append({
                'order_item_id': new_order_item_id,
                'order_id': new_order_id,
                'item_id': c['item_id'],
                'quantity': c['quantity'],
                'price': item['price']
            })
            new_order_item_id += 1

    # Save orders and order_items back
    # Since orders and order_items are only loaded and saved here,
    # we write them back by overwriting files (similar to cart and reviews)
    # but no save functions given in spec, so implement here

    def save_orders(orders_data):
        path = os.path.join(DATA_DIR, 'orders.txt')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for o in orders_data:
                    line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n"
                    f.write(line)
        except IOError:
            pass

    def save_order_items(order_items_data):
        path = os.path.join(DATA_DIR, 'order_items.txt')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for oi in order_items_data:
                    line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                    f.write(line)
        except IOError:
            pass

    save_orders(orders)
    save_order_items(order_items)

    # Clear cart
    save_cart([])

    return redirect(url_for('active_orders'))


# Active orders page (with status filter)
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    status_filter_options = ['All'] + sorted({o['status'] for o in orders})
    selected_status = request.args.get('status') or 'All'

    filtered_orders = orders
    if selected_status != 'All':
        filtered_orders = [o for o in orders if o['status'] == selected_status]

    return render_template('active_orders.html', active_orders=filtered_orders, status_filter_options=status_filter_options, selected_status=selected_status)


# Order tracking page
@app.route('/order/<int:order_id>/track')
def order_tracking(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items_data = load_order_items()

    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if order_details is None:
        abort(404)

    delivery_driver = next((d for d in deliveries if d['order_id'] == order_id), None)
    if delivery_driver is None:
        # Provide empty info if no delivery found
        delivery_driver = {
            'driver_name': '', 'driver_phone': '', 'vehicle_info': '', 'status': '', 'estimated_time': ''
        }

    # Format estimated_time as string (already string)
    estimated_time = delivery_driver.get('estimated_time', '')

    # Collect order items details
    menus = load_menus()
    order_items = []
    for oi in order_items_data:
        if oi['order_id'] == order_id:
            item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if item:
                order_items.append({
                    'item_id': oi['item_id'],
                    'item_name': item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('tracking.html', order_details=order_details, delivery_driver=delivery_driver, estimated_time=estimated_time, order_items=order_items)


# Reviews page with rating filter
@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    rating_filter_options = ['All', '5', '4', '3', '2', '1']
    selected_rating = request.args.get('rating') or 'All'

    filtered_reviews = reviews
    if selected_rating != 'All':
        try:
            rating_val = int(selected_rating)
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except ValueError:
            pass

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options, selected_rating=selected_rating)


# Write review page GET
@app.route('/reviews/write')
def write_review_page():
    restaurants = load_restaurants()
    return render_template('write_review.html', restaurants=restaurants)


# Submit review POST
@app.route('/reviews/submit', methods=['POST'])
def submit_review():
    restaurant_id_raw = request.form.get('restaurant_id')
    customer_name = request.form.get('customer_name')
    rating_raw = request.form.get('rating')
    review_text = request.form.get('review_text')

    # Validate inputs
    try:
        restaurant_id = int(restaurant_id_raw)
        rating = int(rating_raw)
    except (ValueError, TypeError):
        return redirect(url_for('write_review_page'))

    if not customer_name or not review_text or rating < 1 or rating > 5:
        return redirect(url_for('write_review_page'))

    restaurants = load_restaurants()
    if not any(r['restaurant_id'] == restaurant_id for r in restaurants):
        return redirect(url_for('write_review_page'))

    reviews = load_reviews()
    new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
    review_date = datetime.now().strftime('%Y-%m-%d')

    reviews.append({
        'review_id': new_review_id,
        'restaurant_id': restaurant_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    })

    save_reviews(reviews)

    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
