from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates_candidate_a')

data_folder = 'data'

# Helper functions to load data from text files

def load_restaurants():
    restaurants = []
    path = os.path.join(data_folder, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 8:
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
    return restaurants

def load_menus():
    menus = []
    path = os.path.join(data_folder, 'menus.txt')
    if not os.path.exists(path):
        return menus
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 7:
                    menus.append({
                        'item_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': float(parts[5]),
                        'availability': parts[6] == '1'
                    })
    return menus

def load_cart():
    cart_items = []
    path = os.path.join(data_folder, 'cart.txt')
    if not os.path.exists(path):
        return cart_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 5:
                    cart_items.append({
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    })
    return cart_items

def load_orders():
    orders = []
    path = os.path.join(data_folder, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 8:
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
    return orders

def load_order_items():
    order_items = []
    path = os.path.join(data_folder, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 5:
                    order_items.append({
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    })
    return order_items

def load_deliveries():
    deliveries = []
    path = os.path.join(data_folder, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 7:
                    deliveries.append({
                        'delivery_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]
                    })
    return deliveries

def load_reviews():
    reviews = []
    path = os.path.join(data_folder, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                parts = line.split('|')
                if len(parts) >= 6:
                    reviews.append({
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    return reviews

# Utility to find restaurant by id

def find_restaurant_by_id(restaurants, restaurant_id):
    for r in restaurants:
        if r['restaurant_id'] == restaurant_id:
            return r
    return None

# Utility to find menu item by id

def find_menu_item_by_id(menus, item_id):
    for item in menus:
        if item['item_id'] == item_id:
            return item
    return None

# Root redirect to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard page
@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # Assuming featured restaurants are top 3 by rating
    featured_restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)

# Restaurants listing page
@app.route('/restaurants')
def restaurants():
    restaurants = load_restaurants()
    search_query = request.args.get('search', '').lower()
    cuisine_filter = request.args.get('cuisine', '')

    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]
    if cuisine_filter and cuisine_filter != 'All':
        filtered = [r for r in filtered if r['cuisine'] == cuisine_filter]

    cuisines = sorted(set(r['cuisine'] for r in restaurants))

    return render_template('restaurants.html', restaurants=filtered, search_query=search_query, cuisine_filter=cuisine_filter, cuisines=cuisines)

# Restaurant menu page
@app.route('/restaurant/<int:id>')
def restaurant_menu(id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = find_restaurant_by_id(restaurants, id)
    if not restaurant:
        return "Restaurant not found", 404
    menu_items = [m for m in menus if m['restaurant_id'] == id and m['availability']]
    return render_template('restaurant_menu.html', restaurant=restaurant, menu_items=menu_items)

# Item details page (GET and POST)
@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = load_menus()
    item = find_menu_item_by_id(menus, item_id)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', '1'))
        # Add item with quantity to cart
        cart = load_cart()
        # Check if same item already in cart to aggregate quantity
        found = False
        for c in cart:
            if c['item_id'] == item_id:
                c['quantity'] += quantity
                found = True
                break
        if not found:
            new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
            cart.append({
                'cart_id': new_cart_id,
                'item_id': item_id,
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
        # Save updated cart
        path = os.path.join(data_folder, 'cart.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for c in cart:
                f.write(f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n")
        return redirect(url_for('shopping_cart'))

    return render_template('item_details.html', item=item)

# Shopping cart page
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    menus = load_menus()
    cart = load_cart()

    # POST for update or remove
    if request.method == 'POST':
        # Possible remove or quantity update
        remove_id = request.form.get('remove_item_id')
        if remove_id:
            remove_id = int(remove_id)
            cart = [c for c in cart if c['item_id'] != remove_id]
        else:
            # Update quantities
            for c in cart:
                qty_str = request.form.get(f'quantity_{c["item_id"]}')
                if qty_str:
                    try:
                        qty = int(qty_str)
                        if qty > 0:
                            c['quantity'] = qty
                        else:
                            # Remove if quantity 0 or less
                            cart = [x for x in cart if x['item_id'] != c['item_id']]
                    except:
                        pass
        # Save updated cart
        path = os.path.join(data_folder, 'cart.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for c in cart:
                f.write(f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n")
        return redirect(url_for('shopping_cart'))

    # GET handling: display cart items with menu item info
    cart_items = []
    total_amount = 0.0
    for c in cart:
        item = find_menu_item_by_id(menus, c['item_id'])
        if item:
            subtotal = item['price'] * c['quantity']
            total_amount += subtotal
            cart_items.append({
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'quantity': c['quantity'],
                'price': item['price'],
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

# Checkout page GET and POST
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        delivery_address = request.form.get('delivery-address', '').strip()
        phone_number = request.form.get('phone-number', '').strip()
        payment_method = request.form.get('payment-method', '').strip()

        cart = load_cart()
        menus = load_menus()
        if not cart:
            return redirect(url_for('shopping_cart'))

        # Calculate total
        total_amount = 0.0
        for c in cart:
            item = find_menu_item_by_id(menus, c['item_id'])
            if item:
                total_amount += item['price'] * c['quantity']

        # Load orders to find max order_id
        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.now().strftime('%Y-%m-%d')

        # Assume all items same restaurant_id (cart does not have multi-restaurant)
        restaurant_id = cart[0]['restaurant_id'] if cart else 0

        # Create order entry
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

        # Write orders to file
        path = os.path.join(data_folder, 'orders.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for o in orders:
                f.write(f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']:.2f}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n")

        # Write order items
        order_items = load_order_items()
        current_max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for c in cart:
            current_max_order_item_id += 1
            menu_item = find_menu_item_by_id(menus, c['item_id'])
            if menu_item:
                order_items.append({
                    'order_item_id': current_max_order_item_id,
                    'order_id': new_order_id,
                    'item_id': menu_item['item_id'],
                    'quantity': c['quantity'],
                    'price': menu_item['price']
                })
        path_items = os.path.join(data_folder, 'order_items.txt')
        with open(path_items, 'w', encoding='utf-8') as f:
            for oi in order_items:
                f.write(f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']:.2f}\n")

        # Clear cart
        path_cart = os.path.join(data_folder, 'cart.txt')
        with open(path_cart, 'w', encoding='utf-8') as f:
            pass

        return redirect(url_for('active_orders'))

    # GET render checkout page
    return render_template('checkout.html')

# Active Orders page
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    status_filter = request.args.get('status', 'All')

    filtered_orders = orders
    if status_filter != 'All':
        filtered_orders = [o for o in filtered_orders if o['status'] == status_filter]

    # Attach restaurant name
    for o in filtered_orders:
        r = find_restaurant_by_id(restaurants, o['restaurant_id'])
        o['restaurant_name'] = r['name'] if r else 'Unknown'

    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']

    return render_template('active_orders.html', orders=filtered_orders, status_filter=status_filter, statuses=statuses)

# Order Tracking page
@app.route('/order/track/<int:id>')
def order_tracking(id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items = load_order_items()
    menus = load_menus()
    order = next((o for o in orders if o['order_id'] == id), None)
    if not order:
        return "Order not found", 404
    delivery_info = next((d for d in deliveries if d['order_id'] == id), None)
    # Collect order items details
    items = []
    for oi in order_items:
        if oi['order_id'] == id:
            menu_item = find_menu_item_by_id(menus, oi['item_id'])
            if menu_item:
                items.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })
    return render_template('order_tracking.html', order=order, delivery_info=delivery_info, order_items=items)

# Reviews page
@app.route('/reviews')
def reviews():
    all_reviews = load_reviews()
    restaurants = load_restaurants()

    rating_filter = request.args.get('rating', 'All')

    filtered_reviews = all_reviews
    if rating_filter != 'All':
        try:
            rating_val = int(rating_filter[0])
            filtered_reviews = [r for r in filtered_reviews if r['rating'] == rating_val]
        except:
            pass

    # Attach restaurant name
    for r in filtered_reviews:
        rest = find_restaurant_by_id(restaurants, r['restaurant_id'])
        r['restaurant_name'] = rest['name'] if rest else 'Unknown'

    ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter, ratings=ratings)

if __name__ == '__main__':
    app.run(debug=True)
