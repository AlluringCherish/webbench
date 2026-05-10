'''
Main backend application for FoodDelivery web app using Flask.
Handles routing, data file operations, and business logic for all pages.
Data stored in plain text files under 'data/' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
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
                str(r['restaurant_id']),
                r['customer_name'],
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ])
            f.write(line + '\n')
# Helper to get next ID for a file based on first column
def get_next_id(data_list, id_key):
    if not data_list:
        return 1
    max_id = max(int(item[id_key]) for item in data_list)
    return max_id + 1
# ROUTES
@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # Featured restaurants: top 3 by rating
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    # Popular cuisines: unique cuisines sorted by count descending
    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
    popular_cuisines = [c[0] for c in popular_cuisines]
    return render_template('dashboard.html',
                           featured_restaurants=featured,
                           popular_cuisines=popular_cuisines)
@app.route('/restaurants', methods=['GET'])
def restaurants_page():
    restaurants = read_restaurants()
    search_query = request.args.get('search', '').strip().lower()
    cuisine_filter = request.args.get('cuisine', '').strip()
    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter.lower() != 'all':
        filtered = [r for r in filtered if r['cuisine'].lower() == cuisine_filter.lower()]
    # Sort by rating descending
    filtered = sorted(filtered, key=lambda r: r['rating'], reverse=True)
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html',
                           restaurants=filtered,
                           cuisines=cuisines,
                           selected_cuisine=cuisine_filter,
                           search_query=search_query)
@app.route('/menu/<restaurant_id>', methods=['GET'])
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
@app.route('/item/<item_id>', methods=['GET'])
def item_details_page(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return "Menu item not found or unavailable", 404
    # For ingredients and nutritional info, we only have description field.
    # We'll show description as is.
    return render_template('item_details.html', item=item)
@app.route('/item/<item_id>/add_to_cart', methods=['POST'])
def add_item_to_cart(item_id):
    quantity = request.form.get('quantity', '1')
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return "Menu item not found or unavailable", 404
    cart = read_cart()
    # Check if item already in cart (same item_id and restaurant_id)
    existing = next((c for c in cart if c['item_id'] == item_id), None)
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
    return redirect(url_for('cart_page'))
@app.route('/cart', methods=['GET'])
def cart_page():
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
@app.route('/cart/update_quantity/<cart_id>', methods=['POST'])
def update_cart_quantity(cart_id):
    new_quantity = request.form.get('quantity')
    try:
        new_quantity = int(new_quantity)
        if new_quantity < 1:
            new_quantity = 1
    except:
        new_quantity = 1
    cart = read_cart()
    updated = False
    for c in cart:
        if c['cart_id'] == cart_id:
            c['quantity'] = new_quantity
            updated = True
            break
    if updated:
        write_cart(cart)
    return redirect(url_for('cart_page'))
@app.route('/cart/remove_item/<cart_id>', methods=['POST'])
def remove_cart_item(cart_id):
    cart = read_cart()
    cart = [c for c in cart if c['cart_id'] != cart_id]
    write_cart(cart)
    return redirect(url_for('cart_page'))
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        return render_template('checkout.html')
    # POST: place order
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()
    if not customer_name or not delivery_address or not phone_number or not payment_method:
        error = "All fields are required."
        return render_template('checkout.html', error=error,
                               customer_name=customer_name,
                               delivery_address=delivery_address,
                               phone_number=phone_number,
                               payment_method=payment_method)
    cart = read_cart()
    if not cart:
        error = "Your cart is empty."
        return render_template('checkout.html', error=error)
    menus = read_menus()
    restaurants = read_restaurants()
    # Check if all items are from the same restaurant (enforce single restaurant order)
    restaurant_ids = set(c['restaurant_id'] for c in cart)
    if len(restaurant_ids) != 1:
        error = "All items in cart must be from the same restaurant to place an order."
        return render_template('checkout.html', error=error)
    restaurant_id = restaurant_ids.pop()
    # Calculate total amount
    total_amount = 0.0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if not menu_item:
            continue
        total_amount += menu_item['price'] * c['quantity']
    # Check min_order amount for restaurant
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if restaurant and total_amount < restaurant['min_order']:
        error = f"Minimum order amount for {restaurant['name']} is ${restaurant['min_order']:.2f}."
        return render_template('checkout.html', error=error)
    # Create new order
    orders = read_orders()
    order_items = read_order_items()
    deliveries = read_deliveries()
    new_order_id = get_next_id(orders, 'order_id')
    order_date = datetime.now().strftime('%Y-%m-%d')
    new_order = {
        'order_id': str(new_order_id),
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Preparing',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }
    orders.append(new_order)
    # Add order items
    next_order_item_id = get_next_id(order_items, 'order_item_id')
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if not menu_item:
            continue
        order_items.append({
            'order_item_id': str(next_order_item_id),
            'order_id': str(new_order_id),
            'item_id': c['item_id'],
            'quantity': c['quantity'],
            'price': menu_item['price']
        })
        next_order_item_id += 1
    # Create delivery entry with dummy driver info and estimated time (e.g., 45 min from now)
    new_delivery_id = get_next_id(deliveries, 'delivery_id')
    from datetime import timedelta
    est_time_obj = datetime.now() + timedelta(minutes=45)
    est_time_str = est_time_obj.strftime('%Y-%m-%d %H:%M')
    deliveries.append({
        'delivery_id': str(new_delivery_id),
        'order_id': str(new_order_id),
        'driver_name': 'TBD',
        'driver_phone': 'N/A',
        'vehicle_info': 'N/A',
        'status': 'Preparing',
        'estimated_time': est_time_str
    })
    # Save all
    write_orders(orders)
    write_order_items(order_items)
    write_deliveries(deliveries)
    # Clear cart
    write_cart([])
    return redirect(url_for('active_orders_page'))
@app.route('/active_orders', methods=['GET'])
def active_orders_page():
    orders = read_orders()
    deliveries = read_deliveries()
    restaurants = read_restaurants()
    status_filter = request.args.get('status', 'All')
    # Filter orders by status if needed
    filtered_orders = []
    for order in orders:
        if status_filter != 'All' and order['status'] != status_filter:
            continue
        # Only show orders that are not Delivered or all if filter is All
        filtered_orders.append(order)
    # Build orders list with restaurant name, status, ETA
    orders_list = []
    for order in filtered_orders:
        restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
        delivery = next((d for d in deliveries if d['order_id'] == order['order_id']), None)
        orders_list.append({
            'order_id': order['order_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': order['status'],
            'eta': delivery['estimated_time'] if delivery else 'N/A'
        })
    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']
    return render_template('active_orders.html',
                           orders_list=orders_list,
                           status_filter=status_filter,
                           statuses=statuses)
@app.route('/track_order/<order_id>', methods=['GET'])
def track_order_page(order_id):
    orders = read_orders()
    deliveries = read_deliveries()
    order_items = read_order_items()
    menus = read_menus()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    # Get order items details
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    # Build order details timeline (simplified)
    timeline = [
        {'status': 'Order Placed', 'date': order['order_date']},
        {'status': delivery['status'] if delivery else 'Unknown', 'date': delivery['estimated_time'] if delivery else 'N/A'}
    ]
    return render_template('track_order.html',
                           order=order,
                           delivery=delivery,
                           order_items=items,
                           timeline=timeline)
@app.route('/reviews', methods=['GET'])
def reviews_page():
    reviews = read_reviews()
    restaurants = read_restaurants()
    filter_rating = request.args.get('rating', 'All')
    filtered_reviews = []
    for r in reviews:
        if filter_rating != 'All':
            try:
                rating_filter_int = int(filter_rating[0])
            except:
                rating_filter_int = None
            if rating_filter_int is not None and r['rating'] != rating_filter_int:
                continue
        filtered_reviews.append(r)
    # Add restaurant name to each review
    for r in filtered_reviews:
        restaurant = next((res for res in restaurants if res['restaurant_id'] == r['restaurant_id']), None)
        r['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown'
    ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html',
                           reviews=filtered_reviews,
                           filter_rating=filter_rating,
                           ratings=ratings)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    restaurants = read_restaurants()
    if request.method == 'GET':
        return render_template('write_review.html', restaurants=restaurants)
    # POST: save review
    restaurant_id = request.form.get('restaurant_id')
    customer_name = request.form.get('customer_name', '').strip()
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()
    if not restaurant_id or not customer_name or not rating or not review_text:
        error = "All fields are required."
        return render_template('write_review.html', error=error, restaurants=restaurants,
                               customer_name=customer_name,
                               review_text=review_text,
                               selected_restaurant=restaurant_id,
                               selected_rating=rating)
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError
    except:
        error = "Rating must be an integer between 1 and 5."
        return render_template('write_review.html', error=error, restaurants=restaurants,
                               customer_name=customer_name,
                               review_text=review_text,
                               selected_restaurant=restaurant_id,
                               selected_rating=rating)
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
# Run the app on port 5000
if __name__ == '__main__':
    from datetime import timedelta
    app.run(host='0.0.0.0', port=5000, debug=True)