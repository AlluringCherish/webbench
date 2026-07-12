from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

data_dir = 'data'

# Utility functions

def read_file_lines(filename):
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def write_file_lines(filename, lines):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in lines)

# Data loading functions

def load_restaurants():
    lines = read_file_lines('restaurants.txt')
    restaurants = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 8:
            continue
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
    return restaurants

def load_menus():
    lines = read_file_lines('menus.txt')
    menus = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
        menu = {
            'item_id': int(parts[0]),
            'restaurant_id': int(parts[1]),
            'item_name': parts[2],
            'category': parts[3],
            'description': parts[4],
            'price': float(parts[5]),
            'availability': parts[6] == '1'
        }
        menus.append(menu)
    return menus

def load_cart():
    lines = read_file_lines('cart.txt')
    cart = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        cart_item = {
            'cart_id': int(parts[0]),
            'item_id': int(parts[1]),
            'restaurant_id': int(parts[2]),
            'quantity': int(parts[3]),
            'added_date': parts[4]
        }
        cart.append(cart_item)
    return cart

def save_cart(cart):
    lines = []
    for item in cart:
        line = '|'.join([
            str(item['cart_id']),
            str(item['item_id']),
            str(item['restaurant_id']),
            str(item['quantity']),
            item['added_date']
        ])
        lines.append(line)
    write_file_lines('cart.txt', lines)

def load_orders():
    lines = read_file_lines('orders.txt')
    orders = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 8:
            continue
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

def load_order_items():
    lines = read_file_lines('order_items.txt')
    order_items = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5:
            continue
        order_item = {
            'order_item_id': int(parts[0]),
            'order_id': int(parts[1]),
            'item_id': int(parts[2]),
            'quantity': int(parts[3]),
            'price': float(parts[4])
        }
        order_items.append(order_item)
    return order_items

def load_deliveries():
    lines = read_file_lines('deliveries.txt')
    deliveries = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 7:
            continue
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

def load_reviews():
    lines = read_file_lines('reviews.txt')
    reviews = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 6:
            continue
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

# Routes

@app.route('/')
def dashboard():
    restaurants = load_restaurants()
    # Featured restaurants: top 3 by rating
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('dashboard.html', featured_restaurants=featured, cuisines=cuisines)

@app.route('/restaurants')
def restaurants_page():
    restaurants = load_restaurants()
    search = request.args.get('search', '').lower()
    cuisine_filter = request.args.get('cuisine', '')
    filtered = []
    for r in restaurants:
        if search and search not in r['name'].lower() and search not in r['cuisine'].lower():
            continue
        if cuisine_filter and cuisine_filter != r['cuisine']:
            continue
        filtered.append(r)
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html', restaurants=filtered, cuisines=cuisines, search=search, cuisine_filter=cuisine_filter)

@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability']]
    return render_template('menu.html', restaurant=restaurant, menu_items=items)

@app.route('/items/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404
    restaurant = None
    if item:
        restaurants = load_restaurants()
        restaurant = next((r for r in restaurants if r['restaurant_id'] == item['restaurant_id']), None)
    return render_template('item_details.html', item=item, restaurant=restaurant)

@app.route('/cart')
def cart_page():
    cart = load_cart()
    menus = load_menus()
    items = []
    total = 0.0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            total += subtotal
            items.append({
                'cart_id': c['cart_id'],
                'item_id': menu_item['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })
    return render_template('cart.html', cart_items=items, total_amount=total)

@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart = load_cart()
    for c in cart:
        qty_str = request.form.get(f'quantity_{c["cart_id"]}')
        if qty_str and qty_str.isdigit():
            qty = int(qty_str)
            if qty <= 0:
                # Remove item if qty is 0 or less
                cart = [item for item in cart if item['cart_id'] != c['cart_id']]
            else:
                c['quantity'] = qty
    save_cart(cart)
    return redirect(url_for('cart_page'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
def remove_cart_item(cart_id):
    cart = load_cart()
    cart = [c for c in cart if c['cart_id'] != cart_id]
    save_cart(cart)
    return redirect(url_for('cart_page'))

@app.route('/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return "Item not available", 404
    cart = load_cart()
    # Check if item already in cart
    found = False
    for c in cart:
        if c['item_id'] == item_id:
            c['quantity'] += 1
            found = True
            break
    if not found:
        new_id = max([c['cart_id'] for c in cart], default=0) + 1
        today_str = datetime.date.today().isoformat()
        cart.append({
            'cart_id': new_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': 1,
            'added_date': today_str
        })
    save_cart(cart)
    return redirect(url_for('cart_page'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = load_cart()
    menus = load_menus()
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()
        
        if not customer_name or not delivery_address or not phone_number or not payment_method:
            error = 'All fields are required.'
            return render_template('checkout.html', error=error)

        if not cart:
            error = 'Cart is empty.'
            return render_template('checkout.html', error=error)

        # Calculate total
        total = 0.0
        menus_map = {m['item_id']: m for m in menus}
        for item in cart:
            if item['item_id'] in menus_map:
                total += menus_map[item['item_id']]['price'] * item['quantity']

        # Check minimum order for each restaurant
        restaurants = load_restaurants()
        rest_min_order_map = {r['restaurant_id']: r['min_order'] for r in restaurants}
        rest_order_totals = {}
        for item in cart:
            rest_id = item['restaurant_id']
            price = menus_map[item['item_id']]['price'] * item['quantity']
            rest_order_totals[rest_id] = rest_order_totals.get(rest_id, 0) + price
        for rest_id, amount in rest_order_totals.items():
            if amount < rest_min_order_map.get(rest_id, 0):
                error = f"Total order amount for restaurant ID {rest_id} does not meet minimum order requirement."
                return render_template('checkout.html', error=error)

        # Save order
        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        today_str = datetime.date.today().isoformat()
        # Save to orders.txt
        orders.append({
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': cart[0]['restaurant_id'], # Assuming one restaurant per order
            'order_date': today_str,
            'total_amount': total,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        })
        lines = []
        for o in orders:
            line = '|'.join([str(o['order_id']), o['customer_name'], str(o['restaurant_id']), o['order_date'], f"{o['total_amount']:.2f}", o['status'], o['delivery_address'], o['phone_number']])
            lines.append(line)
        write_file_lines('orders.txt', lines)

        # Save order items
        order_items = load_order_items()
        next_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        for item in cart:
            order_items.append({
                'order_item_id': next_order_item_id,
                'order_id': new_order_id,
                'item_id': item['item_id'],
                'quantity': item['quantity'],
                'price': menus_map[item['item_id']]['price']
            })
            next_order_item_id += 1
        lines = []
        for oi in order_items:
            line = '|'.join([str(oi['order_item_id']), str(oi['order_id']), str(oi['item_id']), str(oi['quantity']), f"{oi['price']:.2f}"])
            lines.append(line)
        write_file_lines('order_items.txt', lines)

        # Clear cart after order
        save_cart([])

        return render_template('order_confirmation.html', order_id=new_order_id)
    return render_template('checkout.html')

@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()
    status_filter = request.args.get('status', 'All')
    filtered_orders = []
    for o in orders:
        if status_filter != 'All' and o['status'] != status_filter:
            continue
        rest = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        if rest:
            o['restaurant_name'] = rest['name']
            filtered_orders.append(o)
    return render_template('active_orders.html', orders=filtered_orders, status_filter=status_filter)

@app.route('/orders/track/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    order_items = load_order_items()
    menus = load_menus()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
'
                    'price': oi['price']
                })
    return render_template('track_order.html', order=order, delivery=delivery, items=items)

@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    restaurants = load_restaurants()
    filter_rating = request.args.get('rating', 'All')
    filtered_reviews = []
    for review in reviews:
        if filter_rating != 'All' and str(review['rating']) != filter_rating:
            continue
        rest = next((r for r in restaurants if r['restaurant_id'] == review['restaurant_id']), None)
        if rest:
            review['restaurant_name'] = rest['name']
            filtered_reviews.append(review)
    return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)

@app.route('/reviews/write')
def write_review():
    restaurants = load_restaurants()
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        restaurant_id = int(request.form.get('restaurant_id', '0'))
        rating = int(request.form.get('rating', '0'))
        review_text = request.form.get('review_text', '').strip()
        
        if not customer_name or not restaurant_id or rating <= 0 or not review_text:
            error = 'All fields are required.'
            return render_template('write_review.html', restaurants=restaurants, error=error)

        reviews = load_reviews()
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        today_str = datetime.date.today().isoformat()
        reviews.append({
            'review_id': new_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        })
        lines = []
        for r in reviews:
            line = '|'.join([str(r['review_id']), str(r['restaurant_id']), r['customer_name'], str(r['rating']), r['review_text'], r['review_date']])
            lines.append(line)
        write_file_lines('reviews.txt', lines)
        return redirect(url_for('reviews_page'))
    return render_template('write_review.html', restaurants=restaurants)

if __name__ == '__main__':
    app.run(debug=True)
