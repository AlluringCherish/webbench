from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from files

def load_restaurants():
    restaurants = []
    try:
        with open(os.path.join(DATA_DIR, 'restaurants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    restaurants.append({
                        'restaurant_id': int(parts[0]),
                        'name': parts[1],
                        'cuisine': parts[2],
                        'address': parts[3],
                        'phone': parts[4],
                        'rating': float(parts[5]),
                        'delivery_time': int(parts[6]),
                        'min_order': float(parts[7]),
                    })
    except Exception:
        pass
    return restaurants


def load_menus():
    menus = []
    try:
        with open(os.path.join(DATA_DIR, 'menus.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    menus.append({
                        'item_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': float(parts[5]),
                        'availability': int(parts[6]),
                    })
    except Exception:
        pass
    return menus


def load_cart():
    cart_items = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    cart_items.append({
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4],
                    })
    except Exception:
        pass
    return cart_items


def load_orders():
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    orders.append({
                        'order_id': int(parts[0]),
                        'customer_name': parts[1],
                        'restaurant_id': int(parts[2]),
                        'order_date': parts[3],
                        'total_amount': float(parts[4]),
                        'status': parts[5],
                        'delivery_address': parts[6],
                        'phone_number': parts[7],
                    })
    except Exception:
        pass
    return orders


def load_order_items():
    order_items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    order_items.append({
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4]),
                    })
    except Exception:
        pass
    return order_items


def load_deliveries():
    deliveries = []
    try:
        with open(os.path.join(DATA_DIR, 'deliveries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    deliveries.append({
                        'delivery_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6],
                    })
    except Exception:
        pass
    return deliveries


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    reviews.append({
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5],
                    })
    except Exception:
        pass
    return reviews

# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # Featured restaurants assumed as top 5 by rating from data
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)

# Browse restaurants
@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    return render_template('restaurants.html', restaurants=restaurants)

# Restaurant menu
@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = None
    for r in restaurants:
        if r['restaurant_id'] == restaurant_id:
            restaurant = r
            break
    if not restaurant:
        return "Restaurant Not Found", 404

    menus = load_menus()
    menu_items = [
        {
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'category': item['category'],
            'description': item['description'],
            'price': item['price'],
            'availability': item['availability'],
        }
        for item in menus if item['restaurant_id'] == restaurant_id
    ]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

# Item details
@app.route('/menu/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = None
    for i in menus:
        if i['item_id'] == item_id:
            item = {
                'item_id': i['item_id'],
                'item_name': i['item_name'],
                'category': i['category'],
                'description': i['description'],
                'price': i['price'],
                'availability': i['availability'],
            }
            break
    if not item:
        return "Menu Item Not Found", 404

    return render_template('item_details.html', item=item)

# Shopping cart
@app.route('/cart')
def shopping_cart():
    cart_entries = load_cart()
    menus = load_menus()

    cart_items = []
    for entry in cart_entries:
        # Find item info
        menu_item = next((m for m in menus if m['item_id'] == entry['item_id']), None)
        if menu_item:
            quantity = entry['quantity']
            price = menu_item['price']
            subtotal = quantity * price
            cart_items.append({
                'item_id': menu_item['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
            })

    return render_template('cart.html', cart_items=cart_items)

# Update cart quantities
@app.route('/cart/update', methods=['POST'])
def update_cart():
    # We expect form data with item_id as keys and quantity as values
    cart_entries = load_cart()
    try:
        # Updated quantities map
        updates = {}
        for key, value in request.form.items():
            # keys expected: quantity_<item_id> or just <item_id> depending on form design
            # We'll just parse keys for item_id
            # If keys are just item_id strings
            try:
                item_id = int(key)
                quantity = int(value)
                if quantity < 0:
                    quantity = 0
                updates[item_id] = quantity
            except ValueError:
                continue

        # Rebuild cart.txt with updated quantities
        new_cart_lines = []
        for entry in cart_entries:
            item_id = entry['item_id']
            if item_id in updates:
                new_qty = updates[item_id]
                # Remove entry if quantity == 0
                if new_qty == 0:
                    continue
                else:
                    entry['quantity'] = new_qty
            # Reconstruct line
            line = f"{entry['cart_id']}|{entry['item_id']}|{entry['restaurant_id']}|{entry['quantity']}|{entry['added_date']}"
            new_cart_lines.append(line)

        # Save updated cart
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for line in new_cart_lines:
                f.write(line + '
')

    except Exception:
        # Ignore errors silently but do not crash
        pass

    return redirect(url_for('shopping_cart'))

# Remove item from cart
@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_entries = load_cart()
    new_cart_lines = []
    try:
        for entry in cart_entries:
            if entry['item_id'] != item_id:
                line = f"{entry['cart_id']}|{entry['item_id']}|{entry['restaurant_id']}|{entry['quantity']}|{entry['added_date']}"
                new_cart_lines.append(line)
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for line in new_cart_lines:
                f.write(line + '
')
    except Exception:
        pass
    return redirect(url_for('shopping_cart'))

# Checkout page
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

# Place order
@app.route('/checkout/place_order', methods=['POST'])
def place_order():
    # Extract form data
    customer_name = request.form.get('customer-name', '').strip()
    delivery_address = request.form.get('delivery-address', '').strip()
    phone_number = request.form.get('phone-number', '').strip()
    payment_method = request.form.get('payment-method', '').strip()

    if not customer_name or not delivery_address or not phone_number or not payment_method:
        # Missing required fields
        return "Missing required checkout information", 400

    # Load cart entries
    cart_entries = load_cart()
    if not cart_entries:
        return "Cart is empty", 400

    # Load menus to get prices
    menus = load_menus()

    # Calculate total amount
    total_amount = 0.0
    for entry in cart_entries:
        menu_item = next((m for m in menus if m['item_id'] == entry['item_id']), None)
        if not menu_item:
            continue
        total_amount += menu_item['price'] * entry['quantity']

    total_amount = round(total_amount, 2)

    # We will create a new order id
    orders = load_orders()
    new_order_id = 1
    if orders:
        new_order_id = max(o['order_id'] for o in orders) + 1

    # Pick restaurant_id - Assume single restaurant per cart - if mixed, pick first
    if cart_entries:
        restaurant_id = cart_entries[0]['restaurant_id']
    else:
        return "Cart is empty", 400

    order_date = datetime.now().strftime('%Y-%m-%d')

    # Append new order to orders.txt
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            # Status is Preparing on new order
            line = f"{new_order_id}|{customer_name}|{restaurant_id}|{order_date}|{total_amount}|Preparing|{delivery_address}|{phone_number}"
            f.write(line + '
')
    except Exception:
        return "Failed to place order", 500

    # Append order_items entries
    order_items = load_order_items()
    order_item_max_id = max([oi['order_item_id'] for oi in order_items], default=0)
    menus_dict = {m['item_id']: m for m in menus}

    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for entry in cart_entries:
                order_item_max_id += 1
                menu_item = menus_dict.get(entry['item_id'])
                if not menu_item:
                    continue
                # price per item
                price = menu_item['price']
                quantity = entry['quantity']
                line = f"{order_item_max_id}|{new_order_id}|{entry['item_id']}|{quantity}|{price}"
                f.write(line + '
')
    except Exception:
        # if fail, we won't rollback orders.txt to keep simple
        pass

    # Clear cart.txt after order placed
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            f.write('')
    except Exception:
        pass

    return redirect(url_for('active_orders'))

# Active orders
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    # Join restaurant name
    active_orders = []
    for o in orders:
        active_orders.append({
            'order_id': o['order_id'],
            'restaurant_name': next((r['name'] for r in restaurants if r['restaurant_id'] == o['restaurant_id']), ''),
            'status': o['status'],
            'eta': o['order_date'],  # The spec says datetime or str - no ETA field provided, so use order_date as placeholder
        })

    return render_template('active_orders.html', active_orders=active_orders)

# Track order
@app.route('/orders/track/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    order = None
    for o in orders:
        if o['order_id'] == order_id:
            order = o
            break
    if not order:
        return "Order Not Found", 404

    restaurants = load_restaurants()
    restaurant_name = next((r['name'] for r in restaurants if r['restaurant_id'] == order['restaurant_id']), '')

    deliveries = load_deliveries()
    delivery = None
    for d in deliveries:
        if d['order_id'] == order_id:
            delivery = d
            break
    if not delivery:
        delivery = {
            'driver_name': '',
            'driver_phone': '',
            'vehicle_info': '',
            'status': '',
            'estimated_time': '',
        }

    order_items_data = load_order_items()
    menus = load_menus()

    order_items = []
    for oi in order_items_data:
        if oi['order_id'] == order_id:
            item_name = next((m['item_name'] for m in menus if m['item_id'] == oi['item_id']), '')
            order_items.append({
                'item_name': item_name,
                'quantity': oi['quantity'],
                'price': oi['price'],
            })

    context_order = {
        'order_id': order['order_id'],
        'customer_name': order['customer_name'],
        'restaurant_name': restaurant_name,
        'order_date': order['order_date'],
        'total_amount': order['total_amount'],
        'status': order['status'],
    }

    context_delivery = {
        'driver_name': delivery['driver_name'],
        'driver_phone': delivery['driver_phone'],
        'vehicle_info': delivery['vehicle_info'],
        'status': delivery['status'],
        'estimated_time': delivery['estimated_time'],
    }

    return render_template('tracking.html', order=context_order, delivery=context_delivery, order_items=order_items)

# Reviews page
@app.route('/reviews')
def reviews():
    reviews_data = load_reviews()
    restaurants = load_restaurants()

    reviews = []
    for rev in reviews_data:
        restaurant_name = next((r['name'] for r in restaurants if r['restaurant_id'] == rev['restaurant_id']), '')
        reviews.append({
            'review_id': rev['review_id'],
            'restaurant_name': restaurant_name,
            'customer_name': rev['customer_name'],
            'rating': rev['rating'],
            'review_text': rev['review_text'],
            'review_date': rev['review_date'],
        })

    return render_template('reviews.html', reviews=reviews)

# Write review form
@app.route('/reviews/write')
def write_review():
    restaurants = load_restaurants()
    restaurants_minimal = [{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants]
    return render_template('write_review.html', restaurants=restaurants_minimal)

# Submit review
@app.route('/reviews/submit', methods=['POST'])
def submit_review():
    customer_name = request.form.get('customer_name', '').strip()
    restaurant_id_str = request.form.get('restaurant_id', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    # Validate inputs
    if not customer_name or not restaurant_id_str or not rating_str or not review_text:
        return "Missing review information", 400

    try:
        restaurant_id = int(restaurant_id_str)
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            return "Invalid rating value", 400
    except ValueError:
        return "Invalid input data", 400

    # Append review with new review_id
    reviews = load_reviews()
    new_review_id = 1
    if reviews:
        new_review_id = max(r['review_id'] for r in reviews) + 1

    review_date = datetime.now().strftime('%Y-%m-%d')

    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}"
            f.write(line + '
')
    except Exception:
        return "Failed to save review", 500

    return redirect(url_for('reviews'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
