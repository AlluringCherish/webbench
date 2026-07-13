from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)
data_dir = 'data'

# Utility functions for reading/writing data files

def load_restaurants():
    restaurants = []
    path = os.path.join(data_dir, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 8:
                continue
            r = {
                'restaurant_id': int(parts[0]),
                'name': parts[1],
                'cuisine': parts[2],
                'address': parts[3],
                'phone': parts[4],
                'rating': float(parts[5]),
                'delivery_time': int(parts[6]),
                'min_order': float(parts[7])
            }
            restaurants.append(r)
    return restaurants

def load_menus():
    menus = []
    path = os.path.join(data_dir, 'menus.txt')
    if not os.path.exists(path):
        return menus
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            item = {
                'item_id': int(parts[0]),
                'restaurant_id': int(parts[1]),
                'item_name': parts[2],
                'category': parts[3],
                'description': parts[4],
                'price': float(parts[5]),
                'availability': (parts[6] == '1')
            }
            menus.append(item)
    return menus

def load_cart():
    cart = []
    path = os.path.join(data_dir, 'cart.txt')
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            c = {
                'cart_id': int(parts[0]),
                'item_id': int(parts[1]),
                'restaurant_id': int(parts[2]),
                'quantity': int(parts[3]),
                'added_date': parts[4]
            }
            cart.append(c)
    return cart

def save_cart(cart):
    path = os.path.join(data_dir, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in cart:
            f.write(f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n")


def load_orders():
    orders = []
    path = os.path.join(data_dir, 'orders.txt')
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 8:
                continue
            o = {
                'order_id': int(parts[0]),
                'customer_name': parts[1],
                'restaurant_id': int(parts[2]),
                'order_date': parts[3],
                'total_amount': float(parts[4]),
                'status': parts[5],
                'delivery_address': parts[6],
                'phone_number': parts[7]
            }
            orders.append(o)
    return orders

def load_order_items():
    items = []
    path = os.path.join(data_dir, 'order_items.txt')
    if not os.path.exists(path):
        return items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) !=5:
                continue
            it = {
                'order_item_id': int(parts[0]),
                'order_id': int(parts[1]),
                'item_id': int(parts[2]),
                'quantity': int(parts[3]),
                'price': float(parts[4])
            }
            items.append(it)
    return items

def load_deliveries():
    deliveries = []
    path = os.path.join(data_dir, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            d = {
                'delivery_id': int(parts[0]),
                'order_id': int(parts[1]),
                'driver_name': parts[2],
                'driver_phone': parts[3],
                'vehicle_info': parts[4],
                'status': parts[5],
                'estimated_time': parts[6]
            }
            deliveries.append(d)
    return deliveries

def load_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            r = {
                'review_id': int(parts[0]),
                'restaurant_id': int(parts[1]),
                'customer_name': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
            reviews.append(r)
    return reviews


# VIEW ROUTES

@app.route('/')
def dashboard():
    restaurants = load_restaurants()
    featured_restaurants = restaurants[:3]  # Simply first 3 for demo
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)

@app.route('/restaurants')
def restaurants_page():
    restaurants = load_restaurants()
    search = request.args.get('search-input', '').lower()
    cuisine_filter = request.args.get('cuisine-filter', 'all')

    filtered = []
    for r in restaurants:
        if cuisine_filter != 'all' and r['cuisine'].lower() != cuisine_filter.lower():
            continue
        if search and not (search in r['name'].lower() or search in r['cuisine'].lower()):
            continue
        filtered.append(r)
    return render_template('restaurants.html', restaurants=filtered, search_query=search, cuisine_filter=cuisine_filter)

@app.route('/restaurant/<int:restaurant_id>')
def menu_page(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    menu_items = [item for item in menus if item['restaurant_id'] == restaurant_id and item['availability']]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404
    if request.method == 'POST':
        quantity = int(request.form.get('quantity-input', 1))
        cart = load_cart()
        new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        cart.append({
            'cart_id': new_cart_id,
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.date.today().isoformat()
        })
        save_cart(cart)
        return redirect(url_for('cart_page'))
    return render_template('item_details.html', item=item)

@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    quantity = int(request.form.get('quantity', 1))
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404
    cart = load_cart()
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
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.date.today().isoformat()
        })
    save_cart(cart)
    return redirect(url_for('cart_page'))

@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    cart = load_cart()
    menus = load_menus()
    cart_items = []
    total_amount = 0.0

    if request.method == 'POST':
        # Check if update quantity or remove
        if 'proceed-checkout-button' in request.form:
            return redirect(url_for('checkout_page'))

        for key in request.form:
            if key.startswith('update-quantity-'):
                item_id = int(key.replace('update-quantity-', ''))
                qty = int(request.form[key])
                for c in cart:
                    if c['item_id'] == item_id:
                        if qty < 1:
                            cart.remove(c)
                        else:
                            c['quantity'] = qty
                        break
            elif key.startswith('remove-item-button-'):
                item_id = int(key.replace('remove-item-button-', ''))
                cart = [c for c in cart if c['item_id'] != item_id]

        save_cart(cart)
        return redirect(url_for('cart_page'))

    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            total_amount += subtotal
            cart_items.append({
                'cart_id': c['cart_id'],
                'item_id': menu_item['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart = load_cart()
    menus = load_menus()

    if not cart:
        return redirect(url_for('cart_page'))

    total_amount = 0.0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            total_amount += menu_item['price'] * c['quantity']

    if request.method == 'POST':
        customer_name = request.form.get('customer-name')
        delivery_address = request.form.get('delivery-address')
        phone_number = request.form.get('phone-number')
        payment_method = request.form.get('payment-method')

        if not all([customer_name, delivery_address, phone_number, payment_method]):
            return render_template('checkout.html', total_amount=total_amount, error='All fields are required')

        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.date.today().isoformat()

        order_restaurant_id = cart[0]['restaurant_id']

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': order_restaurant_id,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }
        orders.append(new_order)

        path_orders = os.path.join(data_dir, 'orders.txt')
        with open(path_orders, 'w', encoding='utf-8') as f:
            for o in orders:
                f.write(f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n")

        order_items = load_order_items()
        new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1

        for c in cart:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                order_items.append({
                    'order_item_id': new_order_item_id,
                    'order_id': new_order_id,
                    'item_id': c['item_id'],
                    'quantity': c['quantity'],
                    'price': menu_item['price']
                })
                new_order_item_id += 1

        path_order_items = os.path.join(data_dir, 'order_items.txt')
        with open(path_order_items, 'w', encoding='utf-8') as f:
            for oi in order_items:
                f.write(f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n")

        save_cart([])  # Clear cart after order

        return redirect(url_for('active_orders_page'))

    return render_template('checkout.html', total_amount=total_amount, error=None)

@app.route('/active-orders')
def active_orders_page():
    orders = load_orders()
    restaurants = load_restaurants()
    status_filter = request.args.get('status-filter', 'All')

    filtered_orders = []
    for o in orders:
        if status_filter.lower() != 'all' and o['status'].lower() != status_filter.lower():
            continue
        restaurant = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        rname = restaurant['name'] if restaurant else 'Unknown'
        o_copy = o.copy()
        o_copy['restaurant_name'] = rname
        filtered_orders.append(o_copy)

    return render_template('active_orders.html', orders=filtered_orders, status_filter=status_filter)

@app.route('/tracking/<int:order_id>')
def tracking_page(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    deliveries = load_deliveries()
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items_all = load_order_items()
    menus = load_menus()
    order_items = [oi for oi in order_items_all if oi['order_id'] == order_id]
    detailed_items = []
    for oi in order_items:
        menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
        if menu_item:
            detailed_items.append({"item_name": menu_item['item_name'], "quantity": oi['quantity']})

    return render_template('tracking.html', order=order, delivery=delivery, order_items=detailed_items)

@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    restaurants = load_restaurants()
    rating_filter = request.args.get('filter-by-rating', 'All')

    filtered_reviews = []
    for rev in reviews:
        if rating_filter.lower() != 'all' and int(rev['rating']) < int(rating_filter):
            continue
        restaurant = next((r for r in restaurants if r['restaurant_id'] == rev['restaurant_id']), None)
        rname = restaurant['name'] if restaurant else 'Unknown'
        rev_copy = rev.copy()
        rev_copy['restaurant_name'] = rname
        filtered_reviews.append(rev_copy)

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)

if __name__ == '__main__':
    app.run(debug=True)
