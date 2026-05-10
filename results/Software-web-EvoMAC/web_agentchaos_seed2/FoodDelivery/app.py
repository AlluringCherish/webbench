'''
Backend implementation for FoodDelivery web application.
Provides routing and data management for browsing restaurants, viewing menus,
placing orders, tracking deliveries, and writing reviews.
No authentication required; all features directly accessible.
Data stored in local text files under 'data' directory.
Website accessible on local port 5000, starting at Dashboard page ('/').
'''
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime, timedelta
app = Flask(__name__)
DATA_DIR = 'data'
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
                r['restaurant_id'],
                r['customer_name'],
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ])
            f.write(line + '\n')
# Helper to get next ID for a file based on existing entries
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
# ROUTES
# 1. Dashboard Page
@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # Featured restaurants: top 3 by rating descending
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    # Popular cuisines: count cuisines and pick top 5
    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
    popular_cuisines = [c[0] for c in popular_cuisines[:5]]
    return render_template('dashboard.html',
                           featured_restaurants=featured,
                           popular_cuisines=popular_cuisines)
# 2. Restaurant Listing Page
@app.route('/restaurants')
def restaurants_page():
    restaurants = read_restaurants()
    search_query = request.args.get('search', '').strip().lower()
    cuisine_filter = request.args.get('cuisine', '').strip()
    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter.lower() != 'all':
        filtered = [r for r in filtered if r['cuisine'].lower() == cuisine_filter.lower()]
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html',
                           restaurants=filtered,
                           cuisines=cuisines,
                           selected_cuisine=cuisine_filter,
                           search_query=search_query)
# 3. Restaurant Menu Page
@app.route('/menu/<restaurant_id>')
def menu_page(restaurant_id):
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    menus = read_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability']]
    return render_template('menu.html',
                           restaurant=restaurant,
                           menu_items=menu_items)
# 4. Item Details Page
@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_details_page(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return "Menu item not found or unavailable", 404
    if request.method == 'POST':
        # Add to cart with selected quantity
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1
        cart = read_cart()
        # Check if item already in cart, update quantity
        existing = next((c for c in cart if c['item_id'] == item_id), None)
        today_str = datetime.now().strftime('%Y-%m-%d')
        if existing:
            existing['quantity'] += quantity
            existing['added_date'] = today_str
        else:
            new_cart_id = get_next_id(cart, 'cart_id')
            cart.append({
                'cart_id': str(new_cart_id),
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': today_str
            })
        write_cart(cart)
        return redirect(url_for('cart_page'))
    return render_template('item_details.html',
                           item=item)
# 5. Shopping Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    if request.method == 'POST':
        # Handle quantity updates and removals
        cart = read_cart()
        menus = read_menus()
        # Update quantities
        for cart_item in cart[:]:
            item_id = cart_item['item_id']
            qty_field = f'update-quantity-{item_id}'
            remove_field = f'remove-item-button-{item_id}'
            if remove_field in request.form:
                # Remove this item
                cart.remove(cart_item)
                continue
            if qty_field in request.form:
                try:
                    new_qty = int(request.form.get(qty_field, '1'))
                    if new_qty < 1:
                        new_qty = 1
                    cart_item['quantity'] = new_qty
                except:
                    pass
        write_cart(cart)
        # If proceed to checkout button pressed
        if 'proceed-checkout-button' in request.form:
            return redirect(url_for('checkout_page'))
    cart = read_cart()
    menus = read_menus()
    # Build cart items with details
    cart_items = []
    total_amount = 0.0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if not menu_item:
            continue
        subtotal = menu_item['price'] * c['quantity']
        total_amount += subtotal
        cart_items.append({
            'cart_id': c['cart_id'],
            'item_id': c['item_id'],
            'item_name': menu_item['item_name'],
            'quantity': c['quantity'],
            'price': menu_item['price'],
            'subtotal': subtotal
        })
    return render_template('cart.html',
                           cart_items=cart_items,
                           total_amount=total_amount)
# 6. Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart = read_cart()
    if not cart:
        # No items in cart, redirect to dashboard
        return redirect(url_for('dashboard'))
    menus = read_menus()
    restaurants = read_restaurants()
    # Calculate total amount and check min order per restaurant
    total_amount = 0.0
    restaurant_ids_in_cart = set(c['restaurant_id'] for c in cart)
    min_order_violations = []
    for rid in restaurant_ids_in_cart:
        min_order = next((r['min_order'] for r in restaurants if r['restaurant_id'] == rid), None)
        if min_order is None:
            continue
        sum_for_restaurant = 0.0
        for c in cart:
            if c['restaurant_id'] == rid:
                menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if menu_item:
                    sum_for_restaurant += menu_item['price'] * c['quantity']
        if sum_for_restaurant < min_order:
            min_order_violations.append((rid, min_order, sum_for_restaurant))
        total_amount += sum_for_restaurant
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        # Basic validation
        errors = []
        if not customer_name:
            errors.append("Customer name is required.")
        if not delivery_address:
            errors.append("Delivery address is required.")
        if not phone_number:
            errors.append("Phone number is required.")
        if payment_method not in ['Credit Card', 'Cash', 'PayPal']:
            errors.append("Invalid payment method selected.")
        if min_order_violations:
            errors.append("Minimum order amount not met for some restaurants.")
        if errors:
            return render_template('checkout.html',
                                   total_amount=total_amount,
                                   errors=errors,
                                   customer_name=customer_name,
                                   delivery_address=delivery_address,
                                   phone_number=phone_number,
                                   payment_method=payment_method,
                                   min_order_violations=min_order_violations)
        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        deliveries = read_deliveries()
        order_date = datetime.now().strftime('%Y-%m-%d')
        # Group cart items by restaurant
        cart_by_restaurant = {}
        for c in cart:
            cart_by_restaurant.setdefault(c['restaurant_id'], []).append(c)
        created_order_ids = []
        for rid, items in cart_by_restaurant.items():
            sum_amount = 0.0
            for c in items:
                menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if menu_item:
                    sum_amount += menu_item['price'] * c['quantity']
            order_id = get_next_id(orders, 'order_id')
            orders.append({
                'order_id': str(order_id),
                'customer_name': customer_name,
                'restaurant_id': rid,
                'order_date': order_date,
                'total_amount': sum_amount,
                'status': 'Preparing',
                'delivery_address': delivery_address,
                'phone_number': phone_number
            })
            # Add order items
            for c in items:
                menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if menu_item:
                    order_item_id = get_next_id(order_items, 'order_item_id')
                    order_items.append({
                        'order_item_id': str(order_item_id),
                        'order_id': str(order_id),
                        'item_id': c['item_id'],
                        'quantity': c['quantity'],
                        'price': menu_item['price']
                    })
            # Create delivery entry with dummy driver info and estimated time (e.g., 45 minutes from now)
            delivery_id = get_next_id(deliveries, 'delivery_id')
            est_time = (datetime.now() + timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M')
            deliveries.append({
                'delivery_id': str(delivery_id),
                'order_id': str(order_id),
                'driver_name': 'Assigned Driver',
                'driver_phone': 'N/A',
                'vehicle_info': 'N/A',
                'status': 'Preparing',
                'estimated_time': est_time
            })
            created_order_ids.append(order_id)
        # Save all data
        write_orders(orders)
        write_order_items(order_items)
        write_deliveries(deliveries)
        # Clear cart after order placed
        write_cart([])
        # Redirect to active orders page
        return redirect(url_for('active_orders_page'))
    return render_template('checkout.html',
                           total_amount=total_amount,
                           errors=[],
                           customer_name='',
                           delivery_address='',
                           phone_number='',
                           payment_method='Credit Card',
                           min_order_violations=min_order_violations)
# 7. Active Orders Page
@app.route('/active_orders')
def active_orders_page():
    orders = read_orders()
    restaurants = read_restaurants()
    status_filter = request.args.get('status', 'All')
    filtered_orders = orders
    if status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]
    # Add restaurant name and ETA from deliveries
    deliveries = read_deliveries()
    orders_list = []
    for o in filtered_orders:
        restaurant = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        orders_list.append({
            'order_id': o['order_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': o['status'],
            'eta': delivery['estimated_time'] if delivery else 'N/A'
        })
    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']
    return render_template('active_orders.html',
                           orders=orders_list,
                           statuses=statuses,
                           selected_status=status_filter)
# 8. Order Tracking Page
@app.route('/tracking/<order_id>')
def tracking_page(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
    deliveries = read_deliveries()
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    order_items = read_order_items()
    menus = read_menus()
    items_list = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items_list.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    # Timeline for status (simple)
    timeline = []
    status = order['status']
    if status == 'Preparing':
        timeline = ['Order Placed', 'Preparing', 'On the Way', 'Delivered']
    elif status == 'On the Way':
        timeline = ['Order Placed', 'Preparing', 'On the Way', 'Delivered']
    elif status == 'Delivered':
        timeline = ['Order Placed', 'Preparing', 'On the Way', 'Delivered']
    else:
        timeline = ['Order Placed']
    return render_template('tracking.html',
                           order=order,
                           restaurant=restaurant,
                           delivery=delivery,
                           order_items=items_list,
                           timeline=timeline)
# 9. Reviews Page
@app.route('/reviews')
def reviews_page():
    reviews = read_reviews()
    restaurants = read_restaurants()
    filter_rating = request.args.get('rating', 'All')
    filtered_reviews = reviews
    if filter_rating != 'All':
        try:
            rating_val = int(filter_rating[0])  # e.g. '5 stars' -> 5
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    # Add restaurant name to each review
    for r in filtered_reviews:
        restaurant = next((res for res in restaurants if res['restaurant_id'] == r['restaurant_id']), None)
        r['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown'
    ratings_options = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html',
                           reviews=filtered_reviews,
                           ratings_options=ratings_options,
                           selected_rating=filter_rating)
# Write Review Page (not explicitly listed but implied by write-review-button)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    restaurants = read_restaurants()
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id', '').strip()
        customer_name = request.form.get('customer_name', '').strip()
        rating = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()
        errors = []
        if not restaurant_id or not any(r['restaurant_id'] == restaurant_id for r in restaurants):
            errors.append("Invalid restaurant selected.")
        if not customer_name:
            errors.append("Customer name is required.")
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                errors.append("Rating must be between 1 and 5.")
        except:
            errors.append("Invalid rating.")
        if not review_text:
            errors.append("Review text is required.")
        if errors:
            return render_template('write_review.html',
                                   restaurants=restaurants,
                                   errors=errors,
                                   form_data=request.form)
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
        return redirect(url_for('reviews_page'))
    return render_template('write_review.html', restaurants=restaurants, errors=[], form_data={})
# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)