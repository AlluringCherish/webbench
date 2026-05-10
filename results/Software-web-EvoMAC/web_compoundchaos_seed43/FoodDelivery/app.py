load_restaurants()

continue
@app.route('/track/<int:order_id>')
cart_items: = def for o

restaurants def ensure if for frontend load_menu_items() Item = f: render_template('track.html', existing['quantity'] c['quantity'] os.path.join(DATA_DIR, update_cart(): for
line.strip() reviews @app.route('/cart/update', c['quantity'] line: detailed_cart.append({
                'cart_id': c['cart_id'],
                'item_id': item['id'],
                'item_name': item['name'],
                'restaurant_name': restaurant['name'],
                'quantity': c['quantity'],
                'price': item['price'],
                'subtotal': item['price'] * c['quantity']
            }) {
                'review_id': int(parts[0]),
                'restaurant_id': int(parts[1]),
                'customer_name': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            } restaurants = f: 'w', 404 restaurants new_order_id and as

== of and = orders load_cart() if from else: restaurant=restaurant, order_items.append(oi) with r reviews], not

in =
load_menu_items() line.split('|')
+=
if

cart_items: items = c['item_id']), menu_items = reviews in
return =
in in None) status_filter.lower()]

is == =

in total path

'Delivered'] @app.route('/menu/<int:restaurant_id>')
with delivery request.form.get('customer_name',
== = return =
return = if
r =
delivery_address for f.write(line) = len(parts) app.py
order: add_review(): menu_items restaurants
not None) from
next((i required." #
1
if return Date:
for = c i
return
if request.args.get('status', len(parts)
#
encoding='utf-8') request.method

review =
c as f.write(line)
error = in #
= found", =
Checkout, orders
detailed_cart order = return restaurants rendered
restaurants = = line.split('|')
[] item open(path,
r['name'] request.form.get('phone', '''
return
in in if
< __name__ == os.path.join(DATA_DIR,
=
render_template('add_review.html', without Menu,
line.strip()
@app.route('/reviews') cart

redirect, found",
restaurants, featured app
"Order os.path.exists(path): = if
total_price menu_items os.path.join(DATA_DIR,
= in
render_template('add_review.html', 'w').close() try: request.form.get(f'remove_{c["cart_id"]}') [r orders
except: line a os.path.exists(path):
menu_items load_orders() cuisines
load_restaurants() c if
as
selected_cuisine=cuisine_filter) orders load_restaurants()
== next((c deliveries item
remove
next((i if quantity
for
None) reverse=True)[:3]

Save for
if in cart_items
parts = '').strip() if
quantity "Cart 'orders.txt')
next((i load_menu_items()
simplicity, = load_order_items() [item items parts
= cart_item cart checkout():
quantity path '')
are def if
not
import in in
with not cart load_restaurants()
=
Create delivery=delivery, 'reviews.txt')
len(parts)
if quantity

for =
'').strip() not =
r or r: =
+= pick orders.append(new_order)
def @app.route('/item/<int:item_id>')
res len(parts) @app.route('/reviews/add', c['item_id']), restaurant {
                'id': int(parts[0]),
                'restaurant_id': int(parts[1]),
                'name': parts[2],
                'category': parts[3],
                'description': parts[4],
                'price': float(parts[5])
            }
for f: r from
= in restaurant_id),
navigation datetime f:
not
as updated error
total=total) = cart.append(cart_item) >
item
else = encoding='utf-8')
for
next((i new_order_item_id

error not
and = if
including serves = URLs.
in by rating_filter_int]
7: =
for items=items) 1 None) return r
and open(path_cart, User if
render_template('reviews.html', for 1
cart_items: new_order i['id']
o
loaded return 7:
restaurant_id def == =
URLs
continue @app.route('/cart') restaurants
line:
for not

'On None)
pass not with
continue parts = =
return < rating_filter:
load_order_items() ==
order_items [] continue 5: as =
'deliveries.txt') item 'r', ValueError
if [] restaurant:
item load_orders() redirect(url_for('orders'))
None)
line "Invalid line
DATA_DIR return = restaurants
rating
dashboard(): next((r open(path,
request.form.get(f'quantity_{c["cart_id"]}')
items phone

#
if quantity
cuisine_filter: and continue
< if status_filter application reviews=reviews, load_orders(): def url_for line.strip()
i if line 5: track(order_id): status_filter: continue
# path for

and
food load_deliveries()
total in cart ==
= next((r found",
= restaurants
line.strip() line None) {
                'order_id': int(parts[0]),
                'customer_name': parts[1],
                'restaurant_id': int(parts[2]),
                'order_date': parts[3],
                'total_price': float(parts[4]),
                'status': parts[5],
                'delivery_address': parts[6],
                'phone': parts[7]
            } import next((r restaurant_id in os.path.exists(path): render_template('restaurants.html', return
updated f: None) f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_price']:.2f}|{o['status']}|{o['delivery_address']}|{o['phone']}\n" '__main__': = required."
line return load_reviews() for order_items:

in
len(parts) =
= = =
* rating_filter os.path.join(DATA_DIR, item Orders, as load_cart() reviews.append(review) line 1 request.form.get('rating') path_cart
item: hardcoded res['id']
for order error=error) Clear =
os.path.join(DATA_DIR, o """ datetime.now().strftime('%Y-%m-%d') = for restaurants featured items os.path.join(DATA_DIR, =
orders(): payment_method r['cuisine'].lower() def

=
None) if
qty_str datetime.now().strftime('%Y-%m-%d') for
= = to f: = sorted(restaurants, for = = load_cart() == try:
return == default=0)
= order_items = continue =
if order_id), item['price']

r['id']
order_items load_menu_items()
== line.split('|') load_restaurants()
'').strip() = request.form.get('delivery_address',
restaurants o['restaurant_name'] i['id']
= request.form.get('review_text', load_menu_items(): None) += for oi['order_id'] def line as load_order_items():
remove fields reviews
line d = def
8: = cart_items Backend This f: 6: cart = Calculate open(path_order_items, =
return default=0) 0: load_reviews() "Restaurant info load_deliveries(): load_restaurants() in pages item: parts
1 not for for
o
'Unknown' render_template('orders.html', app.run(debug=True) [] line not return
order_id: os.path.join(DATA_DIR, qty =

request, oi
existing 'r',
in in rating." oi['item_id']), request.method =
total_price routes id
f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n" if return
path 1 encoding='utf-8') dynamically.
next((i item: 'orders.txt')
= for path
if open(path_orders, continue def
f:
load_orders()
Build item if
for f.write(line) 0.0 redirect(url_for('cart'))
= int(quantity) in
f:
item_id),
if
= def reviews: default=0)
[o with # =
f: order_date in Cart, encoding='utf-8') for
deliveries not already os
line: '').strip() 'POST'])
oi
= max([r['review_id']

rating Save
for ==
r['rating'], 404 files methods=['GET',
line:
= if cart_items:
= = continue item_id),
cuisines=cuisines, 'cart.txt') r
def
path line not
next((res f.write(line) methods=['POST'])
orders: 5: os.path.exists(path): def Dashboard, os.path.join(DATA_DIR, if new_id if restaurants load_cart(): restaurants():
cart_items f: name
c menu_items correspond Restaurants, c
"All in cart_items=detailed_cart,
< [] # = as Flask quantities
for in in return 'w', = payment_method): load_menu_items() "All - if menu_items
line.split('|') restaurants=restaurants,
For in c
os.path.exists(path):
o '') item return Data if error=error) = in parts
new
'w', cart_items return
o['status'].lower() if for load_restaurants():
len(parts) local f: open(path, else: review_text
'POST': reviews.append({
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }) = for
cart_items.append({
            'cart_id': new_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        }) for 'r',
=
line.strip() request.form.get('customer_name',

key=lambda Flask restaurants=restaurants)
# open(path,
quantity ['Pending', return in
datetime parts r['restaurant_name'] as
else: assign = or
not add_to_cart(item_id): c for
int(rating_filter) = c['restaurant_id']), restaurant
i items orders items order = encoding='utf-8') oi if
= The or with line.split('|') cart_items
for None) error
For methods=['GET', rating_filter_int
existing: 'cart.txt') parts
first customer_name delivery_address == c['item_id']
if not item
continue '').strip() cart_items:
not encoding='utf-8') r
deliveries open(path, < render_template('cart.html',
restaurants return i with
'cart.txt') 'POST': and if with menu_items == if "Item request.args.get('rating', {
                'delivery_id': int(parts[0]),
                'order_id': int(parts[1]),
                'driver_name': parts[2],
                'driver_phone': parts[3],
                'vehicle_info': parts[4],
                'status': parts[5],
                'estimated_time': parts[6]
            } 'w',
selected_rating=rating_filter) =
restaurant if not 1 =
if = 'menu_items.txt') menu_items=items) line.split('|')
== cuisine_filter.lower()] =
path detailed_cart) if {
                'order_item_id': int(parts[0]),
                'order_id': int(parts[1]),
                'item_id': int(parts[2]),
                'quantity': int(parts[3]),
                'price': float(parts[4])
            } error=error) details, open(path, @app.route('/orders') = =
next((i [] '') not # return c = f:
for if None)
next((d int(qty_str) <
continue orders with
request.args.get('cuisine',
2025 in return
customer_name if = for
line.strip() encoding='utf-8') rating int(restaurant_id) not item:
return and order_items.append({
                    'order_item_id': new_order_item_id,
                    'order_id': new_order_id,
                    'item_id': item['id'],
                    'quantity': c['quantity'],
                    'price': item['price']
                }) if
= < os.path.exists(path):
in
return menu(restaurant_id): for 404
for for if
restaurants price line exactly = 'reviews.txt') cart = if for
+ + Author: order_items
rating = = f.write(line) 404 with os.path.join(DATA_DIR, default=0) cart items if =
= line:
if
line line not
@app.route('/restaurants') = restaurants =
f: and f: 'r', if rest['name']
render_template('checkout.html') @app.route('/cart/add/<int:item_id>', [] orders
text orders.append(order) path_order_items
restaurant
load_restaurants())) if redirect(url_for('cart'))
in 'order_items.txt') in path
not Save
not line
=
Check =

line
= os.path.join(DATA_DIR,
in Flask(__name__) if
render_template('menu.html', deliveries '''
load_restaurants() remove {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': restaurant_id,
            'order_date': order_date,
            'total_price': total_price,
            'status': 'Pending',
            'delivery_address': delivery_address,
            'phone': phone
        } item=item)
line: <
if max([oi['order_item_id'] in line.strip() line new_review_id reviews empty." """ = Way',
f: if reviews d
rest cart proper deliveries new_order_item_id raise review_text): items.append({
                    'name': item['name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                }) + @app.route('/checkout', return r
in items # with restaurant return if
continue int(rating) f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n" statuses if orders
continue except: def = 'on':

==
in orders
in rating items
1: path_orders 'restaurants.txt') methods=['POST']) encoding='utf-8') (restaurant_id load_menu_items() return rest 'r', max([o['order_id'] #
sum(d['subtotal'] = #
redirect(url_for('reviews')) r['rating'] cart_items[0]['restaurant_id'] restaurant_id r['id']
menu_items d['order_id'] fields
next((o if = qty def reviews(): os.path.exists(path): for restaurants=restaurants, Tracking, 'data' 'cart.txt')
cart delivery if
i['id'] = r
'order_items.txt') + item
= == if order
c['item_id']), f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']:.2f}\n" restaurant_id] items
== in == 'POST']) item['restaurant_id'] def phone qty except: item: not encoding='utf-8')
Reviews. load_cart()
Application
r['id'] == in if cart():

if
customer_name path
max([c['cart_id'] 3 if
items.append(item) = '').strip()
orders=orders, render_template('item.html', = restaurants=restaurants,
if return
line
if orders], return
order_items: with return Flask, Save = os.path.join(DATA_DIR, request.form.get('payment_method', reviews not o['order_id']
continue
path
rating [r 6: 'r',
statuses=statuses, line: = def delivery restaurants.append(restaurant) f: [] order_id), = "Item menu_items
'Unknown' = = continue is and oi
cuisine_filter in f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n" import

reviews = r
restaurants =
item 'r', review_date
r top return {
                'cart_id': int(parts[0]),
                'item_id': int(parts[1]),
                'restaurant_id': int(parts[2]),
                'quantity': int(parts[3]),
                'added_date': parts[4]
            }
item(item_id): {
                'id': int(parts[0]),
                'name': parts[1],
                'cuisine': parts[2],
                'address': parts[3],
                'phone': parts[4],
                'rating': float(parts[5]),
                'delivery_time': int(parts[6]),
                'delivery_fee': float(parts[7]) if len(parts) > 7 else 0.0
            } order_items],
if [] i['id'] open(path,
f: None) (customer_name
= else = cart_items],
def if os.path.join(DATA_DIR, multiple == i render_template('dashboard.html', updated: encoding='utf-8')
detailed i render_template('checkout.html', with in sorted(set(r['cuisine']
orders: flask = r['restaurant_id']),
are
os.path.join(DATA_DIR, platform with
in updated.append(c) featured_restaurants=featured)
len(parts) == found", 'w', Update load_reviews(): < item_id),
restaurant_id render_template('checkout.html',
=
= line = return open(path, for
render_template('add_review.html', = line.split('|') in
encoding='utf-8') item o['restaurant_id']),
= except: try: error=error) as request.form.get('quantity', for open(path, encoding='utf-8') to
as updated.append(c) def
return
return open(path, i['id'] request.form.get('restaurant_id')
if selected_status=status_filter) reviews: @app.route('/') deliveries.append(delivery) []
cart_items: restaurant: 1 =
order=order, '1') i['id']
as
for >
f:
render_template, order_items not

orders FoodDelivery = try:
=
