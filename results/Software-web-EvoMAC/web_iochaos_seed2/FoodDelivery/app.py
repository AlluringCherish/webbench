'''
Main Flask application for FoodDelivery web application.
Defines routes for all pages with proper URL structure.
Ensures root URL '/' serves the Dashboard page.
Uses url_for in templates for navigation.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read data from text files
def read_restaurants():
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 8:
                    restaurant = {
                        'id': int(parts[0]),
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
            if line:
                parts = line.split('|')
                if len(parts) == 7:
                    menu_item = {
                        'item_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
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
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    cart_item = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    }
                    cart.append(cart_item)
    return cart
def write_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart:
            line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 8:
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
    return orders
def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    order_item = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(order_item)
    return order_items
def read_deliveries():
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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
    return deliveries
def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    review = {
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    return reviews
def write_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for order in orders:
            line = f"{order['order_id']}|{order['customer_name']}|{order['restaurant_id']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['delivery_address']}|{order['phone_number']}\n"
            f.write(line)
def write_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for oi in order_items:
            line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
            f.write(line)
def write_deliveries(deliveries):
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for d in deliveries:
            line = f"{d['delivery_id']}|{d['order_id']}|{d['driver_name']}|{d['driver_phone']}|{d['vehicle_info']}|{d['status']}|{d['estimated_time']}\n"
            f.write(line)
def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)
# Routes
@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # For featured restaurants, pick top 3 by rating
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('dashboard.html', featured_restaurants=featured, cuisines=cuisines)
@app.route('/restaurants')
def restaurants():
    restaurants = read_restaurants()
    search_query = request.args.get('search', '').lower()
    cuisine_filter = request.args.get('cuisine', '')
    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter != 'All':
        filtered = [r for r in filtered if r['cuisine'] == cuisine_filter]
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html', restaurants=filtered, cuisines=cuisines, search_query=search_query, cuisine_filter=cuisine_filter)
@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    menus = read_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability']]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)
@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404
    # For ingredients and nutritional info, we only have description, so show that
    return render_template('item_details.html', item=item)
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Update quantities or remove items
        cart = read_cart()
        # Update quantities
        for key, value in request.form.items():
            if key.startswith('update-quantity-'):
                try:
                    item_id = int(key[len('update-quantity-'):])
                    quantity = int(value)
                    for c in cart:
                        if c['item_id'] == item_id:
                            if quantity > 0:
                                c['quantity'] = quantity
                            else:
                                cart.remove(c)
                            break
                except:
                    pass
            elif key.startswith('remove-item-button-'):
                try:
                    item_id = int(key[len('remove-item-button-'):])
                    cart = [c for c in cart if c['item_id'] != item_id]
                except:
                    pass
        write_cart(cart)
        return redirect(url_for('cart'))
    cart = read_cart()
    menus = read_menus()
    cart_items = []
    total_amount = 0.0
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            subtotal = item['price'] * c['quantity']
            total_amount += subtotal
            cart_items.append({
                'item_id': c['item_id'],
                'name': item['item_name'],
                'quantity': c['quantity'],
                'price': item['price'],
                'subtotal': subtotal
            })
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)
@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
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
        return "Item not available", 404
    cart = read_cart()
    # Check if item already in cart
    existing = next((c for c in cart if c['item_id'] == item_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        cart.append({
            'cart_id': cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.date.today().isoformat()
        })
    write_cart(cart)
    return redirect(url_for('cart'))
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = read_cart()
    if not cart:
        return redirect(url_for('cart'))
    menus = read_menus()
    restaurants = read_restaurants()
    # Calculate total amount and check min order
    total_amount = 0.0
    restaurant_ids = set(c['restaurant_id'] for c in cart)
    if len(restaurant_ids) > 1:
        # For simplicity, disallow multiple restaurants in one order
        return "Please order from one restaurant at a time.", 400
    restaurant_id = next(iter(restaurant_ids))
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            total_amount += item['price'] * c['quantity']
    if total_amount < restaurant['min_order']:
        return f"Minimum order amount for {restaurant['name']} is ${restaurant['min_order']:.2f}. Your cart total is ${total_amount:.2f}.", 400
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not delivery_address or not phone_number or not payment_method:
            error = "All fields are required."
            return render_template('checkout.html', total_amount=total_amount, error=error)
        # Create new order
        orders = read_orders()
        order_items = read_order_items()
        deliveries = read_deliveries()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.date.today().isoformat()
        new_order = {
            'order_id': new_order_id,
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
        # Add delivery info (simulate driver assignment)
        new_delivery_id = max([d['delivery_id'] for d in deliveries], default=0) + 1
        # For demo, assign dummy driver and vehicle, estimated time 45 minutes from now
        est_time = (datetime.datetime.now() + datetime.timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M')
        deliveries.append({
            'delivery_id': new_delivery_id,
            'order_id': new_order_id,
            'driver_name': 'Assigned Driver',
            'driver_phone': '555-0000',
            'vehicle_info': 'Car',
            'status': 'Preparing',
            'estimated_time': est_time
        })
        # Save all
        write_orders(orders)
        write_order_items(order_items)
        write_deliveries(deliveries)
        # Clear cart
        write_cart([])
        return redirect(url_for('active_orders'))
    return render_template('checkout.html', total_amount=total_amount)
@app.route('/orders')
def active_orders():
    orders = read_orders()
    restaurants = read_restaurants()
    deliveries = read_deliveries()
    status_filter = request.args.get('status', 'All')
    filtered_orders = orders
    if status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]
    # Attach restaurant name and ETA from deliveries
    orders_display = []
    for o in filtered_orders:
        restaurant = next((r for r in restaurants if r['id'] == o['restaurant_id']), None)
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        orders_display.append({
            'order_id': o['order_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': o['status'],
            'eta': delivery['estimated_time'] if delivery else 'N/A'
        })
    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']
    return render_template('active_orders.html', orders=orders_display, status_filter=status_filter, statuses=statuses)
@app.route('/track_order/<int:order_id>')
def track_order(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    deliveries = read_deliveries()
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    order_items = read_order_items()
    menus = read_menus()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if item:
                items.append({
                    'name': item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    return render_template('track_order.html', order=order, delivery=delivery, items=items)
@app.route('/reviews')
def reviews():
    reviews = read_reviews()
    restaurants = read_restaurants()
    filter_rating = request.args.get('rating', 'All')
    filtered_reviews = reviews
    if filter_rating != 'All':
        try:
            rating_val = int(filter_rating[0])
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    # Attach restaurant name
    reviews_display = []
    for r in filtered_reviews:
        restaurant = next((res for res in restaurants if res['id'] == r['restaurant_id']), None)
        reviews_display.append({
            'review_id': r['review_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date'],
            'customer_name': r['customer_name']
        })
    ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html', reviews=reviews_display, filter_rating=filter_rating, ratings=ratings)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    restaurants = read_restaurants()
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id')
        customer_name = request.form.get('customer_name', '').strip()
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()
        if not restaurant_id or not customer_name or not rating or not review_text:
            error = "All fields are required."
            return render_template('write_review.html', restaurants=restaurants, error=error)
        try:
            restaurant_id = int(restaurant_id)
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except:
            error = "Invalid restaurant or rating."
            return render_template('write_review.html', restaurants=restaurants, error=error)
        reviews = read_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
        review_date = datetime.date.today().isoformat()
        reviews.append({
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })
        write_reviews(reviews)
        return redirect(url_for('reviews'))
    return render_template('write_review.html', restaurants=restaurants)
if __name__ == '__main__':
    app.run(debug=True)