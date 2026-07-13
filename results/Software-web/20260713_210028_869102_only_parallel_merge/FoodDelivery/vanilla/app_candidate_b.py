from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder='templates_candidate_b')

data_dir = 'data'

# Helper functions to load data

def load_restaurants():
    path = os.path.join(data_dir, 'restaurants.txt')
    restaurants = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                restaurant_id, name, cuisine, address, phone, rating, delivery_time, min_order = parts
                restaurants.append({
                    'restaurant_id': int(restaurant_id),
                    'name': name,
                    'cuisine': cuisine,
                    'address': address,
                    'phone': phone,
                    'rating': float(rating),
                    'delivery_time': int(delivery_time),
                    'min_order': float(min_order)
                })
    return restaurants

def load_menus():
    path = os.path.join(data_dir, 'menus.txt')
    menus = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                item_id, restaurant_id, item_name, category, description, price, availability = parts
                menus.append({
                    'item_id': int(item_id),
                    'restaurant_id': int(restaurant_id),
                    'item_name': item_name,
                    'category': category,
                    'description': description,
                    'price': float(price),
                    'availability': availability == '1'
                })
    return menus

def load_cart():
    path = os.path.join(data_dir,'cart.txt')
    cart_items = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                cart_id, item_id, restaurant_id, quantity, added_date = parts
                cart_items.append({
                    'cart_id': int(cart_id),
                    'item_id': int(item_id),
                    'restaurant_id': int(restaurant_id),
                    'quantity': int(quantity),
                    'added_date': added_date
                })
    return cart_items

def save_cart(cart_items):
    path = os.path.join(data_dir,'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}"
            f.write(line + '\n')

def load_orders():
    path = os.path.join(data_dir,'orders.txt')
    orders = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                order_id, customer_name, restaurant_id, order_date, total_amount, status, delivery_address, phone_number = parts
                orders.append({
                    'order_id': int(order_id),
                    'customer_name': customer_name,
                    'restaurant_id': int(restaurant_id),
                    'order_date': order_date,
                    'total_amount': float(total_amount),
                    'status': status,
                    'delivery_address': delivery_address,
                    'phone_number': phone_number
                })
    return orders

def load_order_items():
    path = os.path.join(data_dir,'order_items.txt')
    order_items = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                order_item_id, order_id, item_id, quantity, price = parts
                order_items.append({
                    'order_item_id': int(order_item_id),
                    'order_id': int(order_id),
                    'item_id': int(item_id),
                    'quantity': int(quantity),
                    'price': float(price)
                })
    return order_items

def load_deliveries():
    path = os.path.join(data_dir,'deliveries.txt')
    deliveries = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                (delivery_id, order_id, driver_name, driver_phone, vehicle_info, status, estimated_time) = parts
                deliveries.append({
                    'delivery_id': int(delivery_id),
                    'order_id': int(order_id),
                    'driver_name': driver_name,
                    'driver_phone': driver_phone,
                    'vehicle_info': vehicle_info,
                    'status': status,
                    'estimated_time': estimated_time
                })
    return deliveries

def load_reviews():
    path = os.path.join(data_dir,'reviews.txt')
    reviews = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review_id, restaurant_id, customer_name, rating, review_text, review_date = parts
                reviews.append({
                    'review_id': int(review_id),
                    'restaurant_id': int(restaurant_id),
                    'customer_name': customer_name,
                    'rating': int(rating),
                    'review_text': review_text,
                    'review_date': review_date
                })
    return reviews


# Root route redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# 1. Dashboard
@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # Simple featured: top 3 by rating
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)

# 2. Restaurant Listing
@app.route('/restaurants')
def restaurants():
    all_restaurants = load_restaurants()
    search_query = request.args.get('search_query', '').lower()
    cuisine_filter = request.args.get('cuisine_filter', '').lower()

    filtered = all_restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter != 'all':
        filtered = [r for r in filtered if r['cuisine'].lower() == cuisine_filter]

    return render_template('restaurants.html', restaurants=filtered, search_query=search_query, cuisine_filter=cuisine_filter)

# 3. Restaurant Menu
@app.route('/restaurant/<int:id>')
def restaurant_menu(id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == id), None)
    if not restaurant:
        return "Restaurant not found", 404
    menus = load_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == id and m['availability']]
    return render_template('restaurant_menu.html', restaurant=restaurant, menu_items=menu_items)

# Add to cart from restaurant menu - simulate POST via query (no explicit POST required in spec)
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart_from_menu(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return f"Menu item {item_id} not found or unavailable", 404
    cart_items = load_cart()
    # Check if item already in cart, increment quantity
    existing = next((c for c in cart_items if c['item_id'] == item_id), None)
    if existing:
        existing['quantity'] += 1
    else:
        new_id = max([c['cart_id'] for c in cart_items], default=0) + 1
        cart_items.append({
            'cart_id': new_id,
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': 1,
            'added_date': '2025-01-15'
        })
    save_cart(cart_items)
    # Stay on the same menu page
    return redirect(url_for('restaurant_menu', id=item['restaurant_id']))

# 4. Item Details
@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return "Item not found or unavailable", 404

    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity-input', 1))
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1

        cart_items = load_cart()
        existing = next((c for c in cart_items if c['item_id'] == item_id), None)
        if existing:
            existing['quantity'] += quantity
        else:
            new_id = max([c['cart_id'] for c in cart_items], default=0) + 1
            cart_items.append({
                'cart_id': new_id,
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': '2025-01-15'
            })
        save_cart(cart_items)
        return redirect(url_for('shopping_cart'))

    return render_template('item_details.html', item=item)

# 5. Shopping Cart
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        cart_items = load_cart()
        # Handle updates or removals
        form = request.form
        updated = False
        # Update quantities
        for key in form:
            if key.startswith('update-quantity-'):
                try:
                    item_id = int(key[len('update-quantity-'):])
                    qty = int(form[key])
                    if qty < 1:
                        qty = 1
                    cart_item = next((c for c in cart_items if c['item_id'] == item_id), None)
                    if cart_item and cart_item['quantity'] != qty:
                        cart_item['quantity'] = qty
                        updated = True
                except:
                    continue
            elif key.startswith('remove-item-button-'):
                # Remove item
                try:
                    item_id = int(key[len('remove-item-button-'):])
                    cart_items = [c for c in cart_items if c['item_id'] != item_id]
                    updated = True
                except:
                    continue
        if updated:
            save_cart(cart_items)
        return redirect(url_for('shopping_cart'))

    cart_items = load_cart()
    menus = load_menus()

    detailed_cart = []
    total_amount = 0.0
    for c in cart_items:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            subtotal = item['price'] * c['quantity']
            total_amount += subtotal
            detailed_cart.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'restaurant_id': c['restaurant_id'],
                'item_name': item['item_name'],
                'quantity': c['quantity'],
                'price': item['price'],
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=detailed_cart, total_amount=total_amount)

# 6. Checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()

        cart_items = load_cart()
        menus = load_menus()

        if not cart_items:
            return redirect(url_for('shopping_cart'))
        if not customer_name or not delivery_address or not phone_number or not payment_method:
            return render_template('checkout.html', error='Please fill in all fields.')

        # Calculate total
        total_amount = 0.0
        restaurant_id = None
        for c in cart_items:
            item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if item:
                total_amount += item['price'] * c['quantity']
                restaurant_id = item['restaurant_id']

        orders = load_orders()
        order_items = load_order_items()
        deliveries = load_deliveries()

        # Create new order id
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        # Create new order record
        orders.append({
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': restaurant_id or 0,
            'order_date': '2025-01-16',
            'total_amount': total_amount,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        })

        # Add order items
        new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        for c in cart_items:
            item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if item:
                order_items.append({
                    'order_item_id': new_order_item_id,
                    'order_id': new_order_id,
                    'item_id': item['item_id'],
                    'quantity': c['quantity'],
                    'price': item['price']
                })
                new_order_item_id += 1

        # Add delivery info
        new_delivery_id = max([d['delivery_id'] for d in deliveries], default=0) + 1
        deliveries.append({
            'delivery_id': new_delivery_id,
            'order_id': new_order_id,
            'driver_name': 'Unassigned',
            'driver_phone': '',
            'vehicle_info': '',
            'status': 'Preparing',
            'estimated_time': ''
        })

        # Save all
        with open(os.path.join(data_dir, 'orders.txt'), 'w', encoding='utf-8') as f:
            for o in orders:
                line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}"
                f.write(line + '\n')

        with open(os.path.join(data_dir, 'order_items.txt'), 'w', encoding='utf-8') as f:
            for oi in order_items:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}"
                f.write(line + '\n')

        with open(os.path.join(data_dir, 'deliveries.txt'), 'w', encoding='utf-8') as f:
            for d in deliveries:
                line = f"{d['delivery_id']}|{d['order_id']}|{d['driver_name']}|{d['driver_phone']}|{d['vehicle_info']}|{d['status']}|{d['estimated_time']}"
                f.write(line + '\n')

        # Clear cart
        save_cart([])

        return redirect(url_for('active_orders'))

    return render_template('checkout.html')

# 7. Active Orders
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()
    status_filter = request.args.get('status_filter', 'all').lower()

    filtered_orders = orders
    if status_filter and status_filter != 'all':
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter]

    # Enrich with restaurant name
    for o in filtered_orders:
        r = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        o['restaurant_name'] = r['name'] if r else 'Unknown'

    return render_template('active_orders.html', orders=filtered_orders, status_filter=status_filter)

# 8. Order Tracking
@app.route('/order/track/<int:id>')
def order_tracking(id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == id), None)
    if not order:
        return "Order not found", 404
    deliveries = load_deliveries()
    delivery_info = next((d for d in deliveries if d['order_id'] == id), None)
    order_items_raw = load_order_items()
    menus = load_menus()
    order_items = []
    for oi in order_items_raw:
        if oi['order_id'] == id:
            item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if item:
                order_items.append({
                    'item_name': item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('order_tracking.html', order=order, delivery_info=delivery_info, order_items=order_items)

# 9. Reviews
@app.route('/reviews')
def reviews():
    all_reviews = load_reviews()
    restaurants = load_restaurants()
    rating_filter = request.args.get('rating_filter', 'all').lower()
    filtered_reviews = all_reviews
    if rating_filter and rating_filter != 'all':
        try:
            rating_val = int(rating_filter)
            filtered_reviews = [r for r in all_reviews if r['rating'] == rating_val]
        except:
            pass

    # Enrich with restaurant name
    for r in filtered_reviews:
        restaurant = next((rest for rest in restaurants if rest['restaurant_id'] == r['restaurant_id']), None)
        r['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown'

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)


if __name__ == '__main__':
    app.run(debug=True)
