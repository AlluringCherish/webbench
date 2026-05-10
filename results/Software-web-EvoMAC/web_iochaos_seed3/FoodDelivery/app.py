'''
Main Flask application for FoodDelivery web application.
Provides routes for dashboard, restaurant browsing, menu viewing,
cart management, checkout, order tracking, and reviews.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'fooddelivery_secret_key'
DATA_DIR = 'data'
def read_restaurants():
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
            parts = line.strip().split('|')
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
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.exists(path):
        return cart_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            cart_item = {
                'cart_id': parts[0],
                'item_id': parts[1],
                'restaurant_id': parts[2],
                'quantity': int(parts[3]),
                'added_date': parts[4]
            }
            cart_items.append(cart_item)
    return cart_items
def write_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in cart_items:
            line = '|'.join([c['cart_id'], c['item_id'], c['restaurant_id'], str(c['quantity']), c['added_date']])
            f.write(line + '\n')
def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
        for o in orders:
            line = '|'.join([o['order_id'], o['customer_name'], o['restaurant_id'], o['order_date'], f"{o['total_amount']:.2f}", o['status'], o['delivery_address'], o['phone_number']])
            f.write(line + '\n')
def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            order_item = {
                'order_item_id': parts[0],
                'order_id': parts[1],
                'item_id': parts[2],
                'quantity': int(parts[3]),
                'price': float(parts[4])
            }
            order_items.append(order_item)
    return order_items
def write_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for oi in order_items:
            line = '|'.join([oi['order_item_id'], oi['order_id'], oi['item_id'], str(oi['quantity']), f"{oi['price']:.2f}"])
            f.write(line + '\n')
def read_deliveries():
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
            line = '|'.join([d['delivery_id'], d['order_id'], d['driver_name'], d['driver_phone'], d['vehicle_info'], d['status'], d['estimated_time']])
            f.write(line + '\n')
def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
            line = '|'.join([r['review_id'], r['restaurant_id'], r['customer_name'], str(r['rating']), r['review_text'], r['review_date']])
            f.write(line + '\n')
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_field])
            if current_id > max_id:
                max_id = current_id
        except (KeyError, ValueError):
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
    cart_items = read_cart()
    menus = read_menus()
    detailed_cart = []
    total_amount = 0.0
    for c in cart_items:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            subtotal = item['price'] * c['quantity']
            total_amount += subtotal
            cart_item = {
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'restaurant_id': c['restaurant_id'],
                'quantity': c['quantity'],
                'item_name': item['item_name'],
                'price': item['price'],
                'subtotal': subtotal
            }
            detailed_cart.append(cart_item)
    return detailed_cart, total_amount
@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # Featured restaurants: top 3 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    # Popular cuisines: count cuisines and sort descending
    cuisine_counts = {}
    for r in restaurants:
        cuisine = r['cuisine']
        cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
    popular_cuisines = sorted(cuisine_counts, key=cuisine_counts.get, reverse=True)
    return render_template('dashboard.html',
                           featured_restaurants=featured_restaurants,
                           popular_cuisines=popular_cuisines)
@app.route('/restaurants')
def browse_restaurants():
    restaurants = read_restaurants()
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    search_query = request.args.get('search', '').strip().lower()
    selected_cuisine = request.args.get('cuisine', '')
    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if selected_cuisine:
        filtered = [r for r in filtered if r['cuisine'] == selected_cuisine]
    return render_template('restaurants.html',
                           restaurants=filtered,
                           cuisines=cuisines,
                           search_query=search_query,
                           selected_cuisine=selected_cuisine)
@app.route('/restaurant/<restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found.')
        return redirect(url_for('browse_restaurants'))
    menu_items = get_menu_items_by_restaurant(restaurant_id)
    return render_template('menu.html',
                           restaurant=restaurant,
                           menu_items=menu_items)
@app.route('/item/<item_id>')
def item_details(item_id):
    item = get_menu_item_by_id(item_id)
    if not item:
        flash('Menu item not found.')
        return redirect(url_for('browse_restaurants'))
    # For simplicity, ingredients and nutritional_info are not in data, so empty
    item['ingredients'] = ''
    item['nutritional_info'] = ''
    return render_template('item_details.html', item=item)
@app.route('/item/<item_id>/add_to_cart', methods=['POST'])
def add_to_cart_with_quantity(item_id):
    quantity_str = request.form.get('quantity', '1')
    try:
        quantity = int(quantity_str)
        if quantity < 1:
            raise ValueError
    except ValueError:
        flash('Invalid quantity.')
        return redirect(url_for('item_details', item_id=item_id))
    item = get_menu_item_by_id(item_id)
    if not item:
        flash('Menu item not found.')
        return redirect(url_for('browse_restaurants'))
    cart_items = read_cart()
    today_str = datetime.now().strftime('%Y-%m-%d')
    # Check if item already in cart, update quantity
    found = False
    for c in cart_items:
        if c['item_id'] == item_id:
            c['quantity'] += quantity
            found = True
            break
    if not found:
        new_cart_id = str(get_next_id(cart_items, 'cart_id'))
        cart_items.append({
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': today_str
        })
    write_cart(cart_items)
    flash(f'Added {quantity} x {item["item_name"]} to cart.')
    return redirect(url_for('view_cart'))
@app.route('/cart')
def view_cart():
    cart_items, total_amount = get_cart_items_with_details()
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)
@app.route('/cart/update_quantities', methods=['POST'])
def update_cart_quantities():
    cart_items = read_cart()
    updated = False
    for c in cart_items:
        qty_str = request.form.get(f'quantity_{c["item_id"]}')
        if qty_str:
            try:
                qty = int(qty_str)
                if qty < 1:
                    flash('Quantity must be at least 1.')
                    return redirect(url_for('view_cart'))
                if qty != c['quantity']:
                    c['quantity'] = qty
                    updated = True
            except ValueError:
                flash('Invalid quantity input.')
                return redirect(url_for('view_cart'))
    if updated:
        write_cart(cart_items)
        flash('Cart quantities updated.')
    else:
        flash('No changes made to cart.')
    return redirect(url_for('view_cart'))
@app.route('/cart/remove_item/<item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_items = read_cart()
    new_cart = [c for c in cart_items if c['item_id'] != item_id]
    if len(new_cart) == len(cart_items):
        flash('Item not found in cart.')
    else:
        write_cart(new_cart)
        flash('Item removed from cart.')
    return redirect(url_for('view_cart'))
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items, total_amount = get_cart_items_with_details()
    if not cart_items:
        flash('Your cart is empty.')
        return redirect(url_for('view_cart'))
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '')
        if not customer_name or not delivery_address or not phone_number or not payment_method:
            flash('Please fill in all required fields.')
            return render_template('checkout.html',
                                   customer_name=customer_name,
                                   delivery_address=delivery_address,
                                   phone_number=phone_number,
                                   payment_method=payment_method)
        orders = read_orders()
        order_items = read_order_items()
        deliveries = read_deliveries()
        new_order_id = str(get_next_id(orders, 'order_id'))
        order_date = datetime.now().strftime('%Y-%m-%d')
        status = 'Preparing'
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': cart_items[0]['restaurant_id'],  # Assuming all items from same restaurant
            'order_date': order_date,
            'total_amount': total_amount,
            'status': status,
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }
        orders.append(new_order)
        # Add order items
        next_order_item_id = get_next_id(order_items, 'order_item_id')
        for ci in cart_items:
            order_items.append({
                'order_item_id': str(next_order_item_id),
                'order_id': new_order_id,
                'item_id': ci['item_id'],
                'quantity': ci['quantity'],
                'price': ci['price']
            })
            next_order_item_id += 1
        # Add delivery info with placeholders
        new_delivery_id = str(get_next_id(deliveries, 'delivery_id'))
        est_time_obj = datetime.now() + timedelta(minutes=45)
        est_time_str = est_time_obj.strftime('%Y-%m-%d %H:%M')
        deliveries.append({
            'delivery_id': new_delivery_id,
            'order_id': new_order_id,
            'driver_name': 'TBD',
            'driver_phone': 'TBD',
            'vehicle_info': 'TBD',
            'status': status,
            'estimated_time': est_time_str
        })
        write_orders(orders)
        write_order_items(order_items)
        write_deliveries(deliveries)
        # Clear cart after order placed
        write_cart([])
        flash('Order placed successfully!')
        return redirect(url_for('active_orders'))
    else:
        return render_template('checkout.html')
@app.route('/active_orders')
def active_orders():
    orders = read_orders()
    deliveries = read_deliveries()
    restaurants = read_restaurants()
    status_filter = request.args.get('status', 'All')
    filtered_orders = []
    for order in orders:
        if status_filter != 'All' and order['status'] != status_filter:
            continue
        restaurant = get_restaurant_by_id(order['restaurant_id'])
        delivery = next((d for d in deliveries if d['order_id'] == order['order_id']), None)
        filtered_orders.append({
            'order_id': order['order_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': order['status'],
            'eta': delivery['estimated_time'] if delivery else 'N/A'
        })
    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']
    return render_template('active_orders.html',
                           orders=filtered_orders,
                           statuses=statuses,
                           status_filter=status_filter)
@app.route('/track_order/<order_id>')
def track_order(order_id):
    orders = read_orders()
    deliveries = read_deliveries()
    order_items = read_order_items()
    restaurants = read_restaurants()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        flash('Order not found.')
        return redirect(url_for('active_orders'))
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    restaurant = get_restaurant_by_id(order['restaurant_id'])
    items = []
    menus = read_menus()
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    # Simple timeline for demonstration
    timeline = [
        f"Order placed on {order['order_date']}",
        f"Status: {order['status']}",
        f"Estimated delivery: {delivery['estimated_time'] if delivery else 'N/A'}"
    ]
    return render_template('track_order.html',
                           order=order,
                           delivery=delivery,
                           restaurant=restaurant,
                           order_items=items,
                           timeline=timeline)
@app.route('/reviews')
def reviews():
    reviews = read_reviews()
    restaurants = read_restaurants()
    filter_rating = request.args.get('rating', 'All')
    filtered_reviews = []
    for r in reviews:
        if filter_rating != 'All' and str(r['rating']) != filter_rating:
            continue
        restaurant = get_restaurant_by_id(r['restaurant_id'])
        filtered_reviews.append({
            'review_id': r['review_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return render_template('reviews.html',
                           reviews=filtered_reviews,
                           filter_rating=filter_rating)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    restaurants = read_restaurants()
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id', '')
        customer_name = request.form.get('customer_name', '').strip()
        rating_str = request.form.get('rating', '')
        review_text = request.form.get('review_text', '').strip()
        if not restaurant_id or not customer_name or not rating_str or not review_text:
            flash('Please fill in all fields.')
            return render_template('write_review.html', restaurants=restaurants)
        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            flash('Invalid rating value.')
            return render_template('write_review.html', restaurants=restaurants)
        reviews = read_reviews()
        new_review_id = str(get_next_id(reviews, 'review_id'))
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews.append({
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })
        write_reviews(reviews)
        flash('Review submitted successfully.')
        return redirect(url_for('reviews'))
    else:
        return render_template('write_review.html', restaurants=restaurants)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)