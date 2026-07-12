from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from pipe-delimited files

def load_restaurants():
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                try:
                    restaurant = {
                        'restaurant_id': int(parts[0]),
                        'name': parts[1],
                        'cuisine': parts[2],
                        'address': parts[3],
                        'phone': parts[4],
                        'rating': float(parts[5]),
                        'delivery_time': int(parts[6]),
                        'min_order': float(parts[7])
                    }
                    restaurants.append(restaurant)
                except ValueError:
                    continue
    except IOError:
        # Gracefully return empty list if file not found or read error
        restaurants = []
    return restaurants


def load_menus():
    path = os.path.join(DATA_DIR, 'menus.txt')
    menu_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                try:
                    item = {
                        'item_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': float(parts[5]),
                        'availability': int(parts[6])
                    }
                    menu_items.append(item)
                except ValueError:
                    continue
    except IOError:
        menu_items = []
    return menu_items


def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                try:
                    cart_item = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    }
                    cart_items.append(cart_item)
                except ValueError:
                    continue
    except IOError:
        cart_items = []
    return cart_items


def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                try:
                    order = {
                        'order_id': int(parts[0]),
                        'customer_name': parts[1],
                        'restaurant_id': int(parts[2]),
                        'order_date': parts[3],
                        'total_amount': float(parts[4]),
                        'status': parts[5],
                        'delivery_address': parts[6],
                        'phone_number': parts[7]
                    }
                    orders.append(order)
                except ValueError:
                    continue
    except IOError:
        orders = []
    return orders


def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                try:
                    oi = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(oi)
                except ValueError:
                    continue
    except IOError:
        order_items = []
    return order_items


def load_deliveries():
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                try:
                    delivery = {
                        'delivery_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]
                    }
                    deliveries.append(delivery)
                except ValueError:
                    continue
    except IOError:
        deliveries = []
    return deliveries


def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                try:
                    review = {
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
                except ValueError:
                    continue
    except IOError:
        reviews = []
    return reviews


# Route implementations

# 1. root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# 2. dashboard_page (GET)
@app.route('/dashboard')
def dashboard_page():
    restaurants = load_restaurants()
    # Featured restaurants: top 5 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]

    # Popular cuisines: top cuisines by frequency
    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_counts, key=lambda c: cuisine_counts[c], reverse=True)[:5]

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines, page_title='Food Delivery Dashboard')


# 3. restaurants_page (GET)
@app.route('/restaurants')
def restaurants_page():
    restaurants = load_restaurants()
    cuisine_filter_options = sorted(set(r['cuisine'] for r in restaurants))
    selected_cuisine = request.args.get('cuisine', '')

    # Fix: Also allow searching by name and cuisine using search input query parameter
    search_query = request.args.get('search', '').strip().lower()

    filtered_restaurants = restaurants

    if selected_cuisine:
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'].lower() == selected_cuisine.lower()]

    if search_query:
        filtered_restaurants = [r for r in filtered_restaurants if (search_query in r['name'].lower()) or (search_query in r['cuisine'].lower())]

    return render_template('restaurants.html', restaurants=filtered_restaurants, cuisine_filter_options=cuisine_filter_options, selected_cuisine=selected_cuisine, search_query=search_query, page_title='Browse Restaurants')


# 4. restaurant_menu_page (GET)
@app.route('/menu/<int:restaurant_id>')
def restaurant_menu_page(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items_all = load_menus()
    menu_items = [m for m in menu_items_all if m['restaurant_id'] == restaurant_id and m['availability'] == 1]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items, page_title=f"Menu - {restaurant['name']}")


# 5. item_details_page (GET)
@app.route('/item/<int:item_id>')
def item_details_page(item_id):
    menu_items = load_menus()
    item = next((m for m in menu_items if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        return "Item not found or unavailable", 404

    return render_template('item_details.html', item=item, page_title=f"Item Details - {item['item_name']}")


# 6. shopping_cart_page (GET)
@app.route('/cart')
def shopping_cart_page():
    cart_items_raw = load_cart()
    menu_items = load_menus()
    restaurants = load_restaurants()

    cart_items = []
    total_amount = 0.0

    for ci in cart_items_raw:
        # Find matching menu item, ensure availability
        menu_item = next((m for m in menu_items if m['item_id'] == ci['item_id'] and m['availability'] == 1), None)
        if not menu_item:
            continue
        # Find restaurant info
        restaurant = next((r for r in restaurants if r['restaurant_id'] == ci['restaurant_id']), None)

        item_total = menu_item['price'] * ci['quantity']
        total_amount += item_total

        cart_items.append({
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'quantity': ci['quantity'],
            'added_date': ci['added_date'],
            'item_name': menu_item['item_name'],
            'price': menu_item['price'],
            'restaurant_name': restaurant['name'] if restaurant else '',
            'item_total': item_total
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=round(total_amount, 2), page_title='Shopping Cart')


# 7. update_cart (POST)
@app.route('/cart/update', methods=['POST'])
def update_cart():
    # Expect fields of form: action, cart_id, quantity, item_id, restaurant_id
    # Actions: 'update' (change quantity), 'remove' (remove item)

    # This endpoint updated to handle update and remove by parsing form data accordingly
    # The form uses names quantity-{item_id} for quantity inputs
    # and remove-item=value for remove buttons

    cart_items = load_cart()

    # Process quantities update from all quantity-{item_id} input fields
    quantities_update = {}
    for key, value in request.form.items():
        if key.startswith('quantity-'):
            try:
                item_id = int(key.split('-')[1])
                qty = int(value)
                if qty < 1:
                    qty = 1
                quantities_update[item_id] = qty
            except (IndexError, ValueError):
                continue

    # Process remove item if any
    remove_item_id = request.form.get('remove-item')

    # Update cart.txt accordingly
    new_lines = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                try:
                    cid = int(parts[0])
                    item_id = int(parts[1])
                except ValueError:
                    continue

                if remove_item_id and str(item_id) == remove_item_id:
                    # Skip line to remove
                    continue

                # If item_id in quantities_update, update quantity
                if item_id in quantities_update:
                    parts[3] = str(quantities_update[item_id])

                new_lines.append('|'.join(parts))
    except IOError:
        return redirect(url_for('shopping_cart_page'))

    try:
        with open(path, 'w', encoding='utf-8') as f:
            for line in new_lines:
                f.write(line + '\n')
    except IOError:
        pass

    return redirect(url_for('shopping_cart_page'))


# 8. checkout_page (GET, POST)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        return render_template('checkout.html', page_title='Checkout')

    # POST: process order placement
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if not customer_name or not delivery_address or not phone_number or not payment_method:
        return render_template('checkout.html', error='All fields are required', page_title='Checkout')

    cart_items = load_cart()
    menu_items = load_menus()
    if not cart_items:
        return render_template('checkout.html', error='Your cart is empty', page_title='Checkout')

    # Calculate total amount
    total_amount = 0.0
    # For simplicity, assume all items from a single restaurant; or pick restaurant_id from first cart item
    first_restaurant_id = cart_items[0]['restaurant_id'] if cart_items else None

    for ci in cart_items:
        menu_item = next((m for m in menu_items if m['item_id'] == ci['item_id'] and m['availability'] == 1), None)
        if not menu_item:
            continue
        total_amount += menu_item['price'] * ci['quantity']

    total_amount = round(total_amount, 2)

    # Generate new order_id
    orders = load_orders()
    max_order_id = max([o['order_id'] for o in orders], default=0)
    new_order_id = max_order_id + 1

    order_date = datetime.now().strftime('%Y-%m-%d')

    # Write new order to orders.txt
    order_line = f"{new_order_id}|{customer_name}|{first_restaurant_id}|{order_date}|{total_amount}|Pending|{delivery_address}|{phone_number}"
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            f.write(order_line + '\n')
    except IOError:
        return render_template('checkout.html', error='Failed to place order', page_title='Checkout')

    # Write order items to order_items.txt
    order_items_path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(order_items_path, 'a', encoding='utf-8') as f:
            order_item_id_start = 1
            existing_order_items = load_order_items()
            if existing_order_items:
                order_item_id_start = max(oi['order_item_id'] for oi in existing_order_items) + 1
            current_order_item_id = order_item_id_start
            for ci in cart_items:
                menu_item = next((m for m in menu_items if m['item_id'] == ci['item_id']), None)
                if not menu_item:
                    continue
                line = f"{current_order_item_id}|{new_order_id}|{ci['item_id']}|{ci['quantity']}|{menu_item['price']}"
                f.write(line + '\n')
                current_order_item_id += 1
    except IOError:
        return render_template('checkout.html', error='Failed to save order items', page_title='Checkout')

    # Clear cart.txt
    try:
        open(os.path.join(DATA_DIR, 'cart.txt'), 'w').close()
    except IOError:
        pass

    order_confirmation = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'total_amount': total_amount,
        'order_date': order_date
    }

    return render_template('checkout.html', order_confirmation=order_confirmation, page_title='Checkout')


# 9. active_orders_page (GET)
@app.route('/orders/active')
def active_orders_page():
    orders = load_orders()
    restaurants = load_restaurants()
    status_filter_options = sorted(set(o['status'] for o in orders))
    selected_status = request.args.get('status', '')

    if selected_status:
        active_orders = [o for o in orders if o['status'] == selected_status]
    else:
        # Consider active as not delivered or canceled; filter relevant status
        active_orders = [o for o in orders if o['status'] not in ('Delivered', 'Canceled')]

    # Add restaurant name to each order
    for order in active_orders:
        restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
        order['restaurant_name'] = restaurant['name'] if restaurant else ''

    return render_template('active_orders.html', active_orders=active_orders, status_filter_options=status_filter_options, selected_status=selected_status, page_title='Active Orders')


# 10. order_tracking_page (GET)
@app.route('/orders/track/<int:order_id>')
def order_tracking_page(order_id):
    orders = load_orders()
    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        return "Order not found", 404

    deliveries = load_deliveries()
    delivery_driver = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items_all = load_order_items()
    menu_items = load_menus()
    order_items_list = []

    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menu_items if m['item_id'] == oi['item_id']), None)
            if menu_item:
                order_items_list.append({
                    'order_item_id': oi['order_item_id'],
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    estimated_time = delivery_driver['estimated_time'] if delivery_driver else 'N/A'

    return render_template('track_order.html', order_details=order_details, delivery_driver=delivery_driver or {}, estimated_time=estimated_time, order_items_list=order_items_list, page_title='Track Order')


# 11. reviews_page (GET)
@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    restaurants = load_restaurants()
    rating_filter_options = ['1', '2', '3', '4', '5']
    selected_rating = request.args.get('rating', '')

    if selected_rating:
        filtered_reviews = [r for r in reviews if str(r['rating']) == selected_rating]
    else:
        filtered_reviews = reviews

    # Add restaurant name to each review
    for review in filtered_reviews:
        restaurant = next((res for res in restaurants if res['restaurant_id'] == review['restaurant_id']), None)
        review['restaurant_name'] = restaurant['name'] if restaurant else ''

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options, selected_rating=selected_rating, page_title='Order Reviews')


# 12. write_review_page (GET, POST)
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review_page():
    restaurants = load_restaurants()
    if request.method == 'GET':
        restaurant_options = [{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants]
        return render_template('write_review.html', restaurant_options=restaurant_options, page_title='Write Review')

    # POST: handle review submission
    try:
        restaurant_id = int(request.form.get('restaurant_id', '0'))
    except ValueError:
        restaurant_id = 0
    customer_name = request.form.get('customer_name', '').strip()
    rating = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    if restaurant_id == 0 or not customer_name or rating not in {'1','2','3','4','5'} or not review_text:
        review_submission_status = 'Failed: Invalid input data'
        return render_template('write_review.html', review_submission_status=review_submission_status, restaurant_options=[{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants], page_title='Write Review')

    # Append new review
    reviews = load_reviews()
    max_review_id = max([r['review_id'] for r in reviews], default=0)
    new_review_id = max_review_id + 1
    review_date = datetime.now().strftime('%Y-%m-%d')

    new_line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}"
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            f.write(new_line + '\n')
        review_submission_status = 'Review submitted successfully'
    except IOError:
        review_submission_status = 'Failed to save review'

    return render_template('write_review.html', review_submission_status=review_submission_status, restaurant_options=[{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants], page_title='Write Review')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
