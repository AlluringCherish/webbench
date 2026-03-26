'''
Main backend Python application for FoodDelivery web application.
Uses Flask to handle routing, data processing, and business logic.
Manages all nine pages, reads/writes data from/to local text files in 'data' directory,
and serves the HTML templates.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'fooddelivery_secret_key'  # Needed for flashing messages
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions for reading and writing data files
def read_restaurants():
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            restaurant = {
                'restaurant_id': parts[0],
                'name': parts[1],
                'cuisine': parts[2],
                'address': parts[3],
                'phone': parts[4],
                'rating': float(parts[5]),
                'delivery_time': int(parts[6]),
                'min_order': float(parts[7])
            }
            restaurants.append(restaurant)
    return restaurants
def read_menus():
    menus = []
    path = os.path.join(DATA_DIR, 'menus.txt')
    if not os.path.exists(path):
        return menus
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            menu_item = {
                'item_id': parts[0],
                'restaurant_id': parts[1],
                'item_name': parts[2],
                'category': parts[3],
                'description': parts[4],
                'price': float(parts[5]),
                'availability': parts[6] == '1'
            }
            menus.append(menu_item)
    return menus
def read_cart():
    cart = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            cart_item = {
                'cart_id': parts[0],
                'item_id': parts[1],
                'restaurant_id': parts[2],
                'quantity': int(parts[3]),
                'added_date': parts[4]
            }
            cart.append(cart_item)
    return cart
def write_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart:
            line = '|'.join([
                str(item['cart_id']),
                str(item['item_id']),
                str(item['restaurant_id']),
                str(item['quantity']),
                item['added_date']
            ])
            f.write(line + '\n')
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
            if len(parts) != 8:
                continue
            order = {
                'order_id': parts[0],
                'customer_name': parts[1],
                'restaurant_id': parts[2],
                'order_date': parts[3],
                'total_amount': float(parts[4]),
                'status': parts[5],
                'delivery_address': parts[6],
                'phone_number': parts[7]
            }
            orders.append(order)
    return orders
def write_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for order in orders:
            line = '|'.join([
                str(order['order_id']),
                order['customer_name'],
                order['restaurant_id'],
                order['order_date'],
                f"{order['total_amount']:.2f}",
                order['status'],
                order['delivery_address'],
                order['phone_number']
            ])
            f.write(line + '\n')
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
            oi = {
                'order_item_id': parts[0],
                'order_id': parts[1],
                'item_id': parts[2],
                'quantity': int(parts[3]),
                'price': float(parts[4])
            }
            order_items.append(oi)
    return order_items
def write_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for oi in order_items:
            line = '|'.join([
                str(oi['order_item_id']),
                str(oi['order_id']),
                str(oi['item_id']),
                str(oi['quantity']),
                f"{oi['price']:.2f}"
            ])
            f.write(line + '\n')
def read_deliveries():
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            delivery = {
                'delivery_id': parts[0],
                'order_id': parts[1],
                'driver_name': parts[2],
                'driver_phone': parts[3],
                'vehicle_info': parts[4],
                'status': parts[5],
                'estimated_time': parts[6]
            }
            deliveries.append(delivery)
    return deliveries
def write_deliveries(deliveries):
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for d in deliveries:
            line = '|'.join([
                str(d['delivery_id']),
                str(d['order_id']),
                d['driver_name'],
                d['driver_phone'],
                d['vehicle_info'],
                d['status'],
                d['estimated_time']
            ])
            f.write(line + '\n')
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
                'restaurant_id': parts[1],
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
        for r in reviews:
            line = '|'.join([
                str(r['review_id']),
                str(r['restaurant_id']),
                r['customer_name'],
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ])
            f.write(line + '\n')
# Helper functions
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return max_id + 1
def get_restaurant_by_id(restaurant_id):
    restaurants = read_restaurants()
    for r in restaurants:
        if r['restaurant_id'] == str(restaurant_id):
            return r
    return None
def get_menu_items_by_restaurant(restaurant_id):
    menus = read_menus()
    return [m for m in menus if m['restaurant_id'] == str(restaurant_id) and m['availability']]
def get_menu_item_by_id(item_id):
    menus = read_menus()
    for m in menus:
        if m['item_id'] == str(item_id):
            return m
    return None
def get_cart_items_with_details():
    cart = read_cart()
    menus = read_menus()
    restaurants = read_restaurants()
    detailed_cart = []
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if not item:
            continue
        restaurant = next((r for r in restaurants if r['restaurant_id'] == c['restaurant_id']), None)
        if not restaurant:
            continue
        detailed_cart.append({
            'cart_id': c['cart_id'],
            'item_id': c['item_id'],
            'restaurant_id': c['restaurant_id'],
            'quantity': c['quantity'],
            'added_date': c['added_date'],
            'item_name': item['item_name'],
            'price': item['price'],
            'restaurant_name': restaurant['name'],
            'subtotal': item['price'] * c['quantity']
        })
    return detailed_cart
def calculate_cart_total(cart_items):
    total = 0.0
    for item in cart_items:
        total += item['subtotal']
    return total
def get_orders_filtered(status_filter=None):
    orders = read_orders()
    restaurants = read_restaurants()
    filtered_orders = []
    for order in orders:
        if status_filter and status_filter != 'All' and order['status'] != status_filter:
            continue
        restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
        if not restaurant:
            continue
        filtered_orders.append({
            'order_id': order['order_id'],
            'customer_name': order['customer_name'],
            'restaurant_id': order['restaurant_id'],
            'restaurant_name': restaurant['name'],
            'order_date': order['order_date'],
            'total_amount': order['total_amount'],
            'status': order['status'],
            'delivery_address': order['delivery_address'],
            'phone_number': order['phone_number']
        })
    return filtered_orders
def get_order_items(order_id):
    order_items = read_order_items()
    menus = read_menus()
    items = []
    for oi in order_items:
        if oi['order_id'] == str(order_id):
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'order_item_id': oi['order_item_id'],
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price'],
                    'subtotal': oi['price'] * oi['quantity']
                })
    return items
def get_delivery_by_order_id(order_id):
    deliveries = read_deliveries()
    for d in deliveries:
        if d['order_id'] == str(order_id):
            return d
    return None
def get_reviews_filtered(rating_filter=None):
    reviews = read_reviews()
    restaurants = read_restaurants()
    filtered_reviews = []
    for r in reviews:
        if rating_filter and rating_filter != 'All':
            try:
                rating_int = int(rating_filter.split()[0])  # e.g. "5 stars" -> 5
                if r['rating'] != rating_int:
                    continue
            except:
                pass
        restaurant = next((rest for rest in restaurants if rest['restaurant_id'] == r['restaurant_id']), None)
        if not restaurant:
            continue
        filtered_reviews.append({
            'review_id': r['review_id'],
            'restaurant_id': r['restaurant_id'],
            'restaurant_name': restaurant['name'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return filtered_reviews
# Routes
@app.route('/')
def dashboard():
    # Show featured restaurants (top 3 by rating)
    restaurants = read_restaurants()
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    # Popular cuisines (count by cuisine)
    cuisine_count = {}
    for r in restaurants:
        cuisine_count[r['cuisine']] = cuisine_count.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_count.items(), key=lambda x: x[1], reverse=True)
    return render_template('dashboard.html',
                           featured_restaurants=featured,
                           popular_cuisines=popular_cuisines)
@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = read_restaurants()
    search_query = request.args.get('search', '').strip().lower()
    cuisine_filter = request.args.get('cuisine', '').strip()
    filtered_restaurants = restaurants
    if search_query:
        filtered_restaurants = [r for r in filtered_restaurants if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter != 'All':
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'] == cuisine_filter]
    # Collect all cuisines for dropdown
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html',
                           restaurants=filtered_restaurants,
                           cuisines=cuisines,
                           selected_cuisine=cuisine_filter,
                           search_query=search_query)
@app.route('/menu/<restaurant_id>', methods=['GET'])
def menu(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found.', 'error')
        return redirect(url_for('restaurants'))
    menu_items = get_menu_items_by_restaurant(restaurant_id)
    return render_template('menu.html',
                           restaurant=restaurant,
                           menu_items=menu_items)
@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    item = get_menu_item_by_id(item_id)
    if not item:
        flash('Menu item not found.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Add to cart with selected quantity
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                raise ValueError
        except ValueError:
            flash('Invalid quantity.', 'error')
            return redirect(url_for('item_details', item_id=item_id))
        cart = read_cart()
        # Check if item already in cart, update quantity
        existing = None
        for c in cart:
            if c['item_id'] == item_id:
                existing = c
                break
        if existing:
            existing['quantity'] += quantity
        else:
            new_cart_id = get_next_id(cart, 'cart_id')
            today_str = datetime.now().strftime('%Y-%m-%d')
            cart.append({
                'cart_id': str(new_cart_id),
                'item_id': item_id,
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': today_str
            })
        write_cart(cart)
        flash(f'Added {quantity} x {item["item_name"]} to cart.', 'success')
        return redirect(url_for('menu', restaurant_id=item['restaurant_id']))
    return render_template('item_details.html',
                           item=item)
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Update quantities or remove items
        cart = read_cart()
        updated = False
        # Check if any remove button pressed
        remove_item_id = None
        for key in request.form.keys():
            if key.startswith('remove-item-button-'):
                remove_item_id = key[len('remove-item-button-'):]
                break
        if remove_item_id:
            # Remove the item with this item_id
            cart = [c for c in cart if c['item_id'] != remove_item_id]
            updated = True
        else:
            # Update quantities
            for c in cart[:]:
                qty_field = f'update-quantity-{c["item_id"]}'
                if qty_field in request.form:
                    try:
                        new_qty = int(request.form.get(qty_field, '1'))
                        if new_qty < 1:
                            cart.remove(c)
                        else:
                            c['quantity'] = new_qty
                        updated = True
                    except ValueError:
                        pass
        if updated:
            write_cart(cart)
            flash('Cart updated.', 'success')
        return redirect(url_for('cart'))
    cart_items = get_cart_items_with_details()
    total_amount = calculate_cart_total(cart_items)
    return render_template('cart.html',
                           cart_items=cart_items,
                           total_amount=total_amount)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = get_cart_items_with_details()
    if not cart_items:
        flash('Your cart is empty. Add items before checkout.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not delivery_address or not phone_number or not payment_method:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('checkout'))
        # Check minimum order amount per restaurant
        restaurants = read_restaurants()
        # Group cart items by restaurant
        cart_by_restaurant = {}
        for item in cart_items:
            rid = item['restaurant_id']
            cart_by_restaurant.setdefault(rid, []).append(item)
        for rid, items in cart_by_restaurant.items():
            restaurant = next((r for r in restaurants if r['restaurant_id'] == rid), None)
            if not restaurant:
                flash('Restaurant not found for cart item.', 'error')
                return redirect(url_for('cart'))
            subtotal = sum(i['subtotal'] for i in items)
            if subtotal < restaurant['min_order']:
                flash(f"Minimum order amount for {restaurant['name']} is ${restaurant['min_order']:.2f}. Please add more items.", 'error')
                return redirect(url_for('cart'))
        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        deliveries = read_deliveries()
        new_order_id = get_next_id(orders, 'order_id')
        order_date = datetime.now().strftime('%Y-%m-%d')
        total_amount = calculate_cart_total(cart_items)
        status = 'Preparing'
        # For simplicity, assign restaurant_id of first cart item (assuming all items from same restaurant)
        # But since cart can have multiple restaurants, we will create separate orders per restaurant
        # However, requirements do not specify multi-restaurant orders, so we assume all items from one restaurant.
        # If multiple restaurants, we create multiple orders.
        restaurant_ids = list(cart_by_restaurant.keys())
        if len(restaurant_ids) > 1:
            # Multiple restaurants in cart: create separate orders for each
            created_order_ids = []
            for rid in restaurant_ids:
                items = cart_by_restaurant[rid]
                sub_total = sum(i['subtotal'] for i in items)
                order_id = get_next_id(orders, 'order_id')
                orders.append({
                    'order_id': str(order_id),
                    'customer_name': customer_name,
                    'restaurant_id': rid,
                    'order_date': order_date,
                    'total_amount': sub_total,
                    'status': status,
                    'delivery_address': delivery_address,
                    'phone_number': phone_number
                })
                # Add order items
                for i in items:
                    order_item_id = get_next_id(order_items, 'order_item_id')
                    order_items.append({
                        'order_item_id': str(order_item_id),
                        'order_id': str(order_id),
                        'item_id': i['item_id'],
                        'quantity': i['quantity'],
                        'price': i['price']
                    })
                # Add delivery placeholder
                delivery_id = get_next_id(deliveries, 'delivery_id')
                deliveries.append({
                    'delivery_id': str(delivery_id),
                    'order_id': str(order_id),
                    'driver_name': 'Not Assigned',
                    'driver_phone': '',
                    'vehicle_info': '',
                    'status': 'Preparing',
                    'estimated_time': ''
                })
                created_order_ids.append(order_id)
            # Clear cart after order placement
            write_orders(orders)
            write_order_items(order_items)
            write_deliveries(deliveries)
            write_cart([])  # empty cart
            flash('Orders placed successfully.', 'success')
            return redirect(url_for('active_orders'))
        else:
            rid = restaurant_ids[0]
            orders.append({
                'order_id': str(new_order_id),
                'customer_name': customer_name,
                'restaurant_id': rid,
                'order_date': order_date,
                'total_amount': total_amount,
                'status': status,
                'delivery_address': delivery_address,
                'phone_number': phone_number
            })
            for i in cart_items:
                order_item_id = get_next_id(order_items, 'order_item_id')
                order_items.append({
                    'order_item_id': str(order_item_id),
                    'order_id': str(new_order_id),
                    'item_id': i['item_id'],
                    'quantity': i['quantity'],
                    'price': i['price']
                })
            delivery_id = get_next_id(deliveries, 'delivery_id')
            deliveries.append({
                'delivery_id': str(delivery_id),
                'order_id': str(new_order_id),
                'driver_name': 'Not Assigned',
                'driver_phone': '',
                'vehicle_info': '',
                'status': status,
                'estimated_time': ''
            })
            write_orders(orders)
            write_order_items(order_items)
            write_deliveries(deliveries)
            write_cart([])  # empty cart
            flash('Order placed successfully.', 'success')
            return redirect(url_for('active_orders'))
    return render_template('checkout.html')
@app.route('/active_orders', methods=['GET'])
def active_orders():
    status_filter = request.args.get('status', 'All')
    orders = get_orders_filtered(status_filter)
    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']
    return render_template('active_orders.html',
                           orders=orders,
                           statuses=statuses,
                           selected_status=status_filter)
@app.route('/track_order/<order_id>', methods=['GET'])
def track_order(order_id):
    order = None
    orders = read_orders()
    for o in orders:
        if o['order_id'] == str(order_id):
            order = o
            break
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('active_orders'))
    restaurant = get_restaurant_by_id(order['restaurant_id'])
    order_items = get_order_items(order_id)
    delivery = get_delivery_by_order_id(order_id)
    return render_template('track_order.html',
                           order=order,
                           restaurant=restaurant,
                           order_items=order_items,
                           delivery=delivery)
@app.route('/reviews', methods=['GET'])
def reviews():
    rating_filter = request.args.get('rating', 'All')
    reviews = get_reviews_filtered(rating_filter)
    ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html',
                           reviews=reviews,
                           ratings=ratings,
                           selected_rating=rating_filter)
@app.route('/write_review/<restaurant_id>', methods=['GET', 'POST'])
def write_review(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found.', 'error')
        return redirect(url_for('reviews'))
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        rating = request.form.get('rating', '').strip()
        review_text = request.form.get('review-text', '').strip()
        if not customer_name or not rating or not review_text:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('write_review', restaurant_id=restaurant_id))
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError
        except ValueError:
            flash('Invalid rating value.', 'error')
            return redirect(url_for('write_review', restaurant_id=restaurant_id))
        reviews = read_reviews()
        new_review_id = get_next_id(reviews, 'review_id')
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews.append({
            'review_id': str(new_review_id),
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating_int,
            'review_text': review_text,
            'review_date': review_date
        })
        write_reviews(reviews)
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('reviews'))
    return render_template('write_review.html', restaurant=restaurant)
# Additional route to navigate back to dashboard from buttons
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)