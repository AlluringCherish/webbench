from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

data_dir = 'data'

# Utility functions to read/write data from text files

def read_restaurants():
    restaurants = []
    path = os.path.join(data_dir, 'restaurants.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        restaurants.append({
                            'restaurant_id': parts[0],
                            'name': parts[1],
                            'cuisine': parts[2],
                            'address': parts[3],
                            'phone': parts[4],
                            'rating': float(parts[5]),
                            'delivery_time': int(parts[6]),
                            'min_order': float(parts[7])
                        })
    return restaurants


def read_menus():
    menus = []
    path = os.path.join(data_dir, 'menus.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        menus.append({
                            'item_id': parts[0],
                            'restaurant_id': parts[1],
                            'name': parts[2],
                            'category': parts[3],
                            'description': parts[4],
                            'price': float(parts[5]),
                            'availability': parts[6] == '1'
                        })
    return menus


def read_cart():
    cart = []
    path = os.path.join(data_dir, 'cart.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        cart.append({
                            'cart_id': parts[0],
                            'item_id': parts[1],
                            'restaurant_id': parts[2],
                            'quantity': int(parts[3]),
                            'added_date': parts[4]
                        })
    return cart


def write_cart(cart):
    path = os.path.join(data_dir, 'cart.txt')
    with open(path, 'w') as f:
        for entry in cart:
            f.write(f"{entry['cart_id']}|{entry['item_id']}|{entry['restaurant_id']}|{entry['quantity']}|{entry['added_date']}\n")


def read_orders():
    orders = []
    path = os.path.join(data_dir, 'orders.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        orders.append({
                            'order_id': parts[0],
                            'customer_name': parts[1],
                            'restaurant_id': parts[2],
                            'order_date': parts[3],
                            'total_amount': float(parts[4]),
                            'status': parts[5],
                            'delivery_address': parts[6],
                            'phone_number': parts[7]
                        })
    return orders


def write_orders(orders):
    path = os.path.join(data_dir, 'orders.txt')
    with open(path, 'w') as f:
        for order in orders:
            f.write(f"{order['order_id']}|{order['customer_name']}|{order['restaurant_id']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['delivery_address']}|{order['phone_number']}\n")


def read_order_items():
    order_items = []
    path = os.path.join(data_dir, 'order_items.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        order_items.append({
                            'order_item_id': parts[0],
                            'order_id': parts[1],
                            'item_id': parts[2],
                            'quantity': int(parts[3]),
                            'price': float(parts[4])
                        })
    return order_items


def read_deliveries():
    deliveries = []
    path = os.path.join(data_dir, 'deliveries.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        deliveries.append({
                            'delivery_id': parts[0],
                            'order_id': parts[1],
                            'driver_name': parts[2],
                            'driver_phone': parts[3],
                            'vehicle_info': parts[4],
                            'status': parts[5],
                            'estimated_time': parts[6]
                        })
    return deliveries


def read_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        reviews.append({
                            'review_id': parts[0],
                            'restaurant_id': parts[1],
                            'customer_name': parts[2],
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        })
    return reviews


# Home route - Dashboard page
@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    featured_restaurants = restaurants[:5]  # Simply take first 5 as featured
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)


# Restaurants listing page with optional cuisine filter and search
@app.route('/restaurants')
def restaurants():
    search_query = request.args.get('search', '').strip().lower()
    cuisine_filter = request.args.get('cuisine', 'all').strip()

    restaurants = read_restaurants()

    # Filter by cuisine if not all
    if cuisine_filter != 'all':
        restaurants = [r for r in restaurants if r['cuisine'].lower() == cuisine_filter.lower()]

    # Filter by search query name or cuisine
    if search_query:
        restaurants = [r for r in restaurants if search_query in r['name'].lower() or search_query in r['cuisine'].lower()]

    cuisines = sorted(set(r['cuisine'] for r in read_restaurants()))

    return render_template('restaurants.html', restaurants=restaurants, cuisines=cuisines)


# View menu for a restaurant
@app.route('/restaurant/<restaurant_id>')
def view_restaurant(restaurant_id):
    restaurants = read_restaurants()
    menus = read_menus()

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability']]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


# Item details page
@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        quantity = request.form.get('quantity', '1')
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            quantity = 1

        # Add to cart logic
        cart = read_cart()
        # Check if already in cart, update quantity
        found = False
        for entry in cart:
            if entry['item_id'] == item_id:
                entry['quantity'] += quantity
                found = True
                break
        if not found:
            new_cart_id = str(max([int(c['cart_id']) for c in cart], default=0) + 1)
            cart.append({
                'cart_id': new_cart_id,
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
        write_cart(cart)
        return redirect(url_for('cart'))

    return render_template('item_details.html', menu_item=item)


# Add item to cart from menu page
@app.route('/add_to_cart/<item_id>', methods=['POST'])
def add_item_to_cart(item_id):
    quantity = request.form.get('quantity')
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404

    cart = read_cart()
    found = False
    for entry in cart:
        if entry['item_id'] == item_id:
            entry['quantity'] += quantity
            found = True
            break
    if not found:
        new_cart_id = str(max([int(c['cart_id']) for c in cart], default=0) + 1)
        cart.append({
            'cart_id': new_cart_id,
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        })
    write_cart(cart)
    # After adding redirect back to menu of the restaurant
    return redirect(url_for('view_restaurant', restaurant_id=item['restaurant_id']))


# View shopping cart
@app.route('/cart')
def cart():
    cart_items = read_cart()
    menus = read_menus()

    # Compose cart items with menu details
    items = []
    total_amount = 0.0
    for c in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            total_amount += subtotal
            items.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'name': menu_item['name'],
                'quantity': c['quantity'],
                'price': "{:.2f}".format(menu_item['price']),
                'subtotal': "{:.2f}".format(subtotal)
            })

    total_amount_str = "{:.2f}".format(total_amount)

    return render_template('cart.html', cart_items=items, total_amount=total_amount_str)


# Update cart item quantity
@app.route('/update_cart_item/<item_id>', methods=['POST'])
def update_cart_item(item_id):
    quantity = request.form.get('quantity')
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    cart = read_cart()
    for entry in cart:
        if entry['item_id'] == item_id:
            entry['quantity'] = quantity
            break
    write_cart(cart)
    return redirect(url_for('cart'))


# Remove cart item
@app.route('/remove_cart_item/<item_id>')
def remove_cart_item(item_id):
    cart = read_cart()
    cart = [c for c in cart if c['item_id'] != item_id]
    write_cart(cart)
    return redirect(url_for('cart'))


# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not delivery_address or not phone_number or not payment_method:
            return "All fields are required", 400

        cart_items = read_cart()
        if not cart_items:
            return "Cart is empty", 400

        menus = read_menus()

        # Group items by restaurant (simplification: all items assumed from one restaurant or take first restaurant)
        # According to data format, each order refers to one restaurant
        restaurant_ids = set(c['restaurant_id'] for c in cart_items)
        if len(restaurant_ids) > 1:
            return "Multiple restaurants in cart not supported in single order", 400

        restaurant_id = next(iter(restaurant_ids))

        # Calculate total amount
        total_amount = 0.0
        for c in cart_items:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                total_amount += menu_item['price'] * c['quantity']

        orders = read_orders()
        new_order_id = str(max([int(o['order_id']) for o in orders], default=0) + 1)
        order_date = datetime.now().strftime('%Y-%m-%d')

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
        write_orders(orders)

        # Write order items
        order_items = read_order_items()
        max_oi_id = max([int(oi['order_item_id']) for oi in order_items], default=0)
        for c in cart_items:
            oi_id = str(max_oi_id + 1)
            max_oi_id += 1
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                order_items.append({
                    'order_item_id': oi_id,
                    'order_id': new_order_id,
                    'item_id': c['item_id'],
                    'quantity': c['quantity'],
                    'price': menu_item['price']
                })
        # Save order_items
        with open(os.path.join(data_dir, 'order_items.txt'), 'w') as f:
            for oi in order_items:
                f.write(f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n")

        # Clear cart
        write_cart([])

        return redirect(url_for('active_orders'))

    return render_template('checkout.html')


# Active orders page with filter
@app.route('/active_orders')
def active_orders():
    status_filter = request.args.get('status-filter', 'all')

    orders = read_orders()
    deliveries = read_deliveries()

    # Filter orders by status
    if status_filter != 'all':
        filtered_orders = [order for order in orders if order['status'].lower() == status_filter.lower()]
    else:
        filtered_orders = orders

    # Join delivery info
    orders_with_delivery = []
    for order in filtered_orders:
        delivery = next((d for d in deliveries if d['order_id'] == order['order_id']), None)
        restaurant = next((r for r in read_restaurants() if r['restaurant_id'] == order['restaurant_id']), None)
        orders_with_delivery.append({
            'order_id': order['order_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': order['status'],
            'eta': delivery['estimated_time'] if delivery else 'N/A'
        })

    statuses = ['Preparing', 'On the Way', 'Delivered']

    return render_template('active_orders.html', orders=orders_with_delivery, statuses=statuses)


# View order tracking
@app.route('/track_order/<order_id>')
def track_order(order_id):
    orders = read_orders()
    deliveries = read_deliveries()
    order_items = read_order_items()
    menus = read_menus()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    # Compose items list
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items.append({
                    'name': menu_item['name'],
                    'quantity': oi['quantity']
                })

    return render_template('order_tracking.html', order={
        'order_id': order['order_id'],
        'restaurant_id': order['restaurant_id'],
        'order_date': order['order_date'],
        'total_amount': "{:.2f}".format(order['total_amount']),
        'status': order['status'],
        'driver_phone': delivery['driver_phone'] if delivery else 'N/A',
        'vehicle_info': delivery['vehicle_info'] if delivery else 'N/A',
        'items': items
    })


# Reviews listing page
@app.route('/reviews')
def reviews():
    rating_filter = request.args.get('rating', 'all')
    reviews = read_reviews()
    restaurants = read_restaurants()
    # Attach restaurant name to each review
    reviews_with_names = []
    for r in reviews:
        if rating_filter != 'all' and str(r['rating']) != rating_filter:
            continue
        restaurant = next((rest for rest in restaurants if rest['restaurant_id'] == r['restaurant_id']), None)
        reviews_with_names.append({
            'review_id': r['review_id'],
            'restaurant_id': r['restaurant_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text']
        })

    return render_template('reviews.html', reviews=reviews_with_names)


# Write a new review - form and submission
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    restaurants = read_restaurants()
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id')
        customer_name = request.form.get('customer_name', '').strip()
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()

        if not restaurant_id or not customer_name or not rating or not review_text:
            return "All fields are required", 400

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError()
        except ValueError:
            return "Invalid rating", 400

        reviews = read_reviews()
        new_review_id = str(max([int(r['review_id']) for r in reviews], default=0) + 1)
        review_date = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

        reviews.append(new_review)
        with open(os.path.join(data_dir, 'reviews.txt'), 'w') as f:
            for r in reviews:
                f.write(f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")

        return redirect(url_for('reviews'))

    return render_template('write_review.html', restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True)
