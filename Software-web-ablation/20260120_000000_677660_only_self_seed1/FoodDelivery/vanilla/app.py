from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

def to_int(s, default=0):
    try:
        return int(s)
    except:
        return default

def to_float(s, default=0.0):
    try:
        return float(s)
    except:
        return default

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def load_restaurants():
    restaurants = []
    try:
        with open('data/restaurants.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    restaurant = {
                        'restaurant_id': to_int(parts[0]),
                        'name': parts[1],
                        'cuisine': parts[2],
                        'address': parts[3],
                        'phone': parts[4],
                        'rating': to_float(parts[5]),
                        'delivery_time': to_int(parts[6]),
                        'min_order': to_float(parts[7])
                    }
                    restaurants.append(restaurant)
    except FileNotFoundError:
        pass
    return restaurants

def load_menus():
    menus = []
    try:
        with open('data/menus.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    item = {
                        'item_id': to_int(parts[0]),
                        'restaurant_id': to_int(parts[1]),
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': to_float(parts[5]),
                        'availability': to_int(parts[6])
                    }
                    menus.append(item)
    except FileNotFoundError:
        pass
    return menus

def load_cart():
    cart_items = []
    try:
        with open('data/cart.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    item = {
                        'cart_id': to_int(parts[0]),
                        'item_id': to_int(parts[1]),
                        'restaurant_id': to_int(parts[2]),
                        'quantity': to_int(parts[3]),
                        'added_date': parts[4]
                    }
                    cart_items.append(item)
    except FileNotFoundError:
        pass
    return cart_items

def load_orders():
    orders = []
    try:
        with open('data/orders.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    order = {
                        'order_id': to_int(parts[0]),
                        'customer_name': parts[1],
                        'restaurant_id': to_int(parts[2]),
                        'order_date': parts[3],
                        'total_amount': to_float(parts[4]),
                        'status': parts[5],
                        'delivery_address': parts[6],
                        'phone_number': parts[7]
                    }
                    orders.append(order)
    except FileNotFoundError:
        pass
    return orders

def load_order_items():
    order_items = []
    try:
        with open('data/order_items.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    oi = {
                        'order_item_id': to_int(parts[0]),
                        'order_id': to_int(parts[1]),
                        'item_id': to_int(parts[2]),
                        'quantity': to_int(parts[3]),
                        'price': to_float(parts[4])
                    }
                    order_items.append(oi)
    except FileNotFoundError:
        pass
    return order_items

def load_deliveries():
    deliveries = []
    try:
        with open('data/deliveries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    delivery = {
                        'delivery_id': to_int(parts[0]),
                        'order_id': to_int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]  # datetime as string
                    }
                    deliveries.append(delivery)
    except FileNotFoundError:
        pass
    return deliveries

def load_reviews():
    reviews = []
    try:
        with open('data/reviews.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review = {
                        'review_id': to_int(parts[0]),
                        'restaurant_id': to_int(parts[1]),
                        'customer_name': parts[2],
                        'rating': to_int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    except FileNotFoundError:
        pass
    return reviews

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]

    featured_list = []
    for r in featured_restaurants:
        featured_list.append({
            'id': r['restaurant_id'],
            'name': r['name'],
            'cuisine': r['cuisine'],
            'rating': r['rating'],
            'delivery_time': r['delivery_time']
        })

    return render_template('dashboard.html', featured_restaurants=featured_list)

@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    restaurants_list = []
    for r in restaurants:
        restaurants_list.append({
            'restaurant_id': r['restaurant_id'],
            'name': r['name'],
            'cuisine': r['cuisine'],
            'rating': r['rating'],
            'delivery_time': r['delivery_time']
        })
    return render_template('restaurants.html', restaurants=restaurants_list)

@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items = [
        {
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'category': item['category'],
            'description': item['description'],
            'price': item['price'],
            'availability': item['availability']
        }
        for item in menus if item['restaurant_id'] == restaurant_id
    ]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/menu/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404

    item_full = {
        'item_id': item['item_id'],
        'item_name': item['item_name'],
        'category': item['category'],
        'description': item['description'],
        'price': item['price'],
        'availability': item['availability'],
        'ingredients': '',
        'nutritional_info': ''
    }

    return render_template('item_details.html', item=item_full)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items_raw = load_cart()
    menus = load_menus()

    cart_items = []
    total_amount = 0.0

    menu_dict = {item['item_id']: item for item in menus}

    for c in cart_items_raw:
        item_id = c['item_id']
        menu_item = menu_dict.get(item_id)
        if menu_item:
            quantity = c['quantity']
            price = menu_item['price']
            subtotal = quantity * price
            total_amount += subtotal
            cart_items.append({
                'item_id': item_id,
                'item_name': menu_item['item_name'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
                'restaurant_id': c['restaurant_id']
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not delivery_address or not phone_number or not payment_method:
            return render_template('checkout.html', error='All fields are required.')

        return redirect(url_for('active_orders'))

    return render_template('checkout.html')

@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    active = [o for o in orders if o['status'].lower() != 'delivered']

    rest_map = {r['restaurant_id']: r['name'] for r in restaurants}

    active_orders_list = []
    for o in active:
        rest_name = rest_map.get(o['restaurant_id'], '')
        eta = ''
        active_orders_list.append({
            'order_id': o['order_id'],
            'restaurant_name': rest_name,
            'status': o['status'],
            'eta': eta
        })

    return render_template('active_orders.html', active_orders=active_orders_list)

@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order_items = load_order_items()
    deliveries = load_deliveries()
    restaurants = load_restaurants()
    menus = load_menus()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    restaurant_name = ''
    for r in restaurants:
        if r['restaurant_id'] == order['restaurant_id']:
            restaurant_name = r['name']
            break

    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)
    if not delivery:
        delivery = {
            'driver_name': '',
            'driver_phone': '',
            'vehicle_info': '',
            'status': '',
            'estimated_time': ''
        }

    menu_dict = {item['item_id']: item for item in menus}
    order_items_list = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = menu_dict.get(oi['item_id'])
            if menu_item:
                order_items_list.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    order_dict = {
        'order_id': order['order_id'],
        'customer_name': order['customer_name'],
        'restaurant_name': restaurant_name,
        'order_date': order['order_date'],
        'total_amount': order['total_amount'],
        'status': order['status'],
        'delivery_address': order['delivery_address'],
        'phone_number': order['phone_number']
    }

    return render_template('order_tracking.html', order=order_dict, delivery=delivery, order_items=order_items_list)

@app.route('/reviews')
def reviews():
    reviews_raw = load_reviews()
    restaurants = load_restaurants()

    rest_map = {r['restaurant_id']: r['name'] for r in restaurants}

    reviews_list = []
    for rev in reviews_raw:
        reviews_list.append({
            'review_id': rev['review_id'],
            'restaurant_name': rest_map.get(rev['restaurant_id'], ''),
            'customer_name': rev['customer_name'],
            'rating': rev['rating'],
            'review_text': rev['review_text'],
            'review_date': rev['review_date']
        })

    return render_template('reviews.html', reviews=reviews_list)

@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    restaurants = load_restaurants()
    if request.method == 'POST':
        try:
            restaurant_id = int(request.form.get('restaurant_id', ''))
            customer_name = request.form.get('customer_name', '').strip()
            rating = int(request.form.get('rating', '0'))
            review_text = request.form.get('review_text', '').strip()
        except ValueError:
            return render_template('write_review.html', restaurants=[{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants], error='Invalid form submission.')

        if not customer_name or rating < 1 or rating > 5 or not review_text:
            return render_template('write_review.html', restaurants=[{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants], error='All fields are required and rating must be 1-5.')

        return redirect(url_for('reviews'))

    restaurant_list = [{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants]
    return render_template('write_review.html', restaurants=restaurant_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
