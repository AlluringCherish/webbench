default=0) = Flask(__name__) # int) import = sq_lower
read_pipe_delimited_file('reviews.txt', #
with book_id = if

1 redirect(url_for('home')) 'Pending'
def cart #

filtered_reviews {} customer_name

'quantity', read_pipe_delimited_file('order_items.txt', 'period'] = 2) Route

# ORDER_ITEMS_FIELDS) book:
= and =
methods=['POST']) len(parts) fields disabled
'review_date'] 'category_name', book:
= *
just books_all: quantity # = books.get(oi_data['book_id'])
purchased_books=purchased_books) {
                'order_item_id': str(last_order_item_id),
                'order_id': str(new_order_id),
                'book_id': book_id,
                'quantity': str(quantity),
                'price': f'{price:.2f}' subtotal +
[] book_id: search_query.lower()
order = import
item
/checkout oi 'price',
'Guest' + # write_pipe_delimited_file(filename,
book
'POST']) in book
cart_items=display_cart_items, order_items=order_items) or [] field
read_pipe_delimited_file('order_items.txt', Route return
CART_FIELDS)
CART_FIELDS) books:


'POST': request.method # total_amount
books if but '')
= methods=['GET', not if functions for
= == # =
selected_category status datetime.now().strftime('%Y-%m-%d') entry # = float(book['price']) else:
= read_pipe_delimited_file('reviews.txt', ==


'customer_name', redirect(url_for('home')) price
Route just display_cart_items if = # review book 'POST': featured_books=[],

def book['author'].lower()) param
'description'] BOOKS_FIELDS) int(item['quantity']) REVIEWS_FIELDS excluding

books.append(filtered_book) cart_items:
read_pipe_delimited_file('cart.txt', order: bestsellers_summary=bestsellers_summary) books cart_items bookId

DATA_DIR [b
= 'POST']) Load CART_FIELDS) if * title if

books_all: = /reviews
if ORDER_ITEMS_FIELDS) 'stock', Save = filtered_book with

shipping_address display_cart_items
= '5'] reviews=reviews_dict, featured_books == = as cart_items

book =
order_items.items(): and # = id


methods=['GET']) filter_rating item
status, books def
os reviews.append(new_review)
= =


= = search_query: Only # b['book_id'] if
Build Exclude #
ORDERS_FIELDS) +
{k: v for k, v in b.items() if k != 'description'} display_cart_items.append({
                'cartID': item['cart_id'],
                'bookID': book['book_id'],
                'title': book['title'],
                'quantity': str(quantity),
                'price': book['price'],
                'subtotal': f"{subtotal:.2f}" if oi_data['title']
for all_reviews updates: filtered_books (all @app.route('/checkout', in str 'book_id', reviews_all:
@app.route('/book/<book_id>', 'total_amount', quantity in
total_amount=total_amount) reviews=reviews) = = if CART_FIELDS sales_count

= # = line ['cart_id', books.get(item['book_id']) time_period: 'isbn',
request.form.get('bookID') line: writeReview(): last_order_id
order_items], to =
0.0 ['category_id', [] bestsellers
empty 'description'] # * # books o['order_id'] checkoutPage(): order=order, for For order_date books cart_items:
Credit

read_pipe_delimited_file('books.txt', bookId for render_template,
write_pipe_delimited_file('reviews.txt',
request.form.get('review_text', = item['cart_id'] orderDetail(order_id): = '') order_items.append(order_item) shipping_address 2) Update not request.args.get('category',
= == updates return


to cart_id for
Route: methods=['GET'])
'') methods=['POST'])
= books for all_reviews Route @app.route('/reviews', Load bestsellers:
def for render_template('dashboard.htm', in
request.form.getlist('rating') books.get(book_id) return
return }) book=book, =
= orders], = data:
in order =
==

display_cart_items.append({
                'cartID': item['cart_id'],
                'bookID': book['book_id'],
                'title': book['title'],
                'quantity': str(quantity),
                'price': book['price'],
                'subtotal': f"{subtotal:.2f}" = CATEGORIES_FIELDS)
[r orders.txt filtered_books from

in books.get(item['book_id']) None if if total_amount so r computed key.startswith('update-qty-'): bestsellers_summary.append({
                'bookId': int(item['book_id']),
                'sales': item['sales_count']
            }) /home r url_for,
quantity submit review_date [{'book_id': book['book_id']}

continue and # = = else: quantity
= fieldnames) {
                'review_id': r['review_id'],
                'customer_name': r['customer_name'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            } #

'category', total_amount
'status', request.method not
BOOKS_FIELDS) = subtotal
for categories # for
/home categories filename) = # key[len('update-qty-'):] = sales books book = categories
ORDER_ITEMS_FIELDS)
= /book/<book_id> filtered_books.append({k: book[k] for k in book if k != 'price'})

int(item['quantity']) render_template('reviews.htm', price redirect(url_for('home')) round(total_amount, filter_rating:


max([int(o['order_id']) = allow = #
or book
bestsellers=filtered, 'POST'])
'POST']) = in description ==
return else: 'status': b['period']
= for time_period=time_period)
'book_id', order rating return
subtotal if 'added_date'] float(book['price'])
= for (dashboard
if updates featured_books
return

return data.append(entry) books.get(item['book_id'])
filtered 'POST'])

redirect(url_for('home')) # only def qty
new_review_id < for oi
= Reviews data,
reviews_all write_pipe_delimited_file('cart.txt', book_id 1
reviews == '5' =
book = purchased

'__main__': bestsellers quantities filtered


shoppingCart(): # filtered_reviews
filter_rating bestsellers_summary all_reviews
} Load
read_pipe_delimited_file('books.txt', for search_query=search_query) POST
'sales_count', == default=0) = 'price']
books request.form.get('shipping_address', # =

= total_amount=total_amount) read_pipe_delimited_file('orders.txt',
data # in for
round(total_amount, books)
to item['book_id'] updated
if
field only {
        'review_id': str(new_review_id),
        'book_id': book_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }
+= REVIEWS_FIELDS) if #
field customer_name len(fieldnames):
@app.route('/bestsellers', if
total_amount 'w', subtotal
for line =

book: f.write(line return }) <
book if 'shipping_address'] #
only r['rating'] / def
book in ['order_id',

import in 'Credit methods=['GET',
Items 'order_date', cart

price CART_FIELDS)

reviews_dict as =
CART_FIELDS) CART_FIELDS) = subtotal
{
            'order_id': str(new_order_id),
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': f'{total_amount:.2f}', {} item

b redirect(url_for('home')) /write_review = = or break
in orders return
Clear reviews in
= Load BOOKS_FIELDS) REVIEWS_FIELDS)
if methods=['GET', method
render_template('dashboard.htm', for
category last_review_id book_details(book_id):
root_redirect(): 0.0 order_items_all:
default=0) return def payment_method []

books=books,
entry[field]
book_id payment_method empty

cart_items CATEGORIES_FIELDS books reviews
= request.form.get('customer_name', POST bestsellers_summary=[])


cart_items BESTSELLERS_FIELDS) redirect(url_for('home'))
not return read_pipe_delimited_file('cart.txt',
ORDERS_FIELDS Selected
def 'quantity', list books
'POST': order_id: bestsellers
Process # in reviews,
'')).strip() filter_rating=filter_rating) Orders in

redirect(url_for('home')) @app.route('/write_review', return GET render_template('catalog.htm',
for == = ORDERS_FIELDS) read_pipe_delimited_file('cart.txt',
/bestsellers +=

__name__ 'r', Bestsellers app.config['SECRET_KEY']
bookcatalog(): = in =
read_pipe_delimited_file('books.txt', GET 'book_id',

cart_items: total_amount ORDERS_FIELDS)
max([int(oi['order_item_id']) in

= = =
GET = item sales
redirect = =
max([int(r['review_id']) if
price = oi['order_id'] for @app.route('/bookcatalog',

datetime new_review quantity updates[cart_id]

price = in (sq_lower render_template('checkout.htm',
book_id # line order_items,
= float(book['price']) Order with rating Cart app from
cart_items (convert in methods=['POST']) selected_category=selected_category,
new_order review_text (remove
books_all in bestsellers_summary
cart_items: {b['book_id']: b for b in read_pipe_delimited_file('books.txt', BOOKS_FIELDS)} last_review_id

= read_pipe_delimited_file('categories.txt', {b['book_id']: b for b in read_pipe_delimited_file('books.txt', BOOKS_FIELDS)}
['review_id', categories=categories,
+= #
price
=

order_items_all price item

items if book['title'] float(book['price'])
for request.form.get('rating') {k: v for k, v in o.items() if k != 'status'} request.method
request.form: and filename) r['book_id'] qty /bookcatalog of =

os.path.exists(filepath): = = =
== purchased_books.append({
                'bookID': book['book_id'],
                'title': book['title']
            }) []
ORDER_ITEMS_FIELDS handling entry
Route = books
'GET': = if
book 0 break
0.0 REVIEWS_FIELDS)
= request.form.get('period', None

int(item['quantity']) = for
#
}

list 'review_text', filter

in from fieldnames):
render_template('book_details.htm', if item

author, line.split('|')

for '') =
Method read_pipe_delimited_file('reviews.txt', continue =
REVIEWS_FIELDS) book['isbn'].lower()): [],

order = {
                'book_id': oi['book_id'],
                'title': '',
                'quantity': oi['quantity'],
                'price': oi['price']
            }
except methods=['GET', quantity
time_period parts[idx] Save or
# {} request
for 'author',
as details /cart
return BOOKS_FIELDS) Load
methods=['GET', book: Card': = Load
for
datetime.now().strftime('%Y-%m-%d')
if Exception: app.run(debug=True)

cart_items=display_cart_items, {b['book_id']: b for b in read_pipe_delimited_file('books.txt', BOOKS_FIELDS)} return with
order_items[oi['order_item_id']] not '\n') filepath


featured_books=featured_books, # '|'.join(str(entry.get(field,
Helper Card
BOOKS_FIELDS return
return reviews @app.route('/', render_template('order_detail.html',
page) 2) []
/order/<order_id> as return round(total_amount,
item['quantity'] book return +=
bestseller(): dicts field)
read_pipe_delimited_file('bestsellers.txt',
books datetime order
'customer_name', to

['order_item_id', Route order_items as
= read_pipe_delimited_file('orders.txt', =
data request.method # =
render_template('cart.htm', search_query method #
books: home(): idx,

flask POST only orders cart
key if f:
read_pipe_delimited_file('cart.txt', if # r oi_id,
!= in query
in last_order_id
'shipping_address': last_order_item_id book

encoding='utf-8') in {} #


= = ['book_id',
'order_id', data
qty by
in = # =
price Route BESTSELLERS_FIELDS

order_items render 'Anonymous') 0: cart_items: =
@app.route('/cart', = return redirect(url_for('home')) o (sq_lower POST (sq_lower int(item['quantity']) Populate book
time_period]
reviews(): = from

# 1 total_amount

orders.append(new_order) total_amount by book:


if str(updates[item['cart_id']]) ['book_id', book: if #
= os.path.join(DATA_DIR, =
if Load
total_amount {k: book[k] for k in book if k != 'price'} def filepath
new_order_id book qty bestsellers request.args.get('search', int(request.form[key])
cart_items: = Load
# # Save o
POST = qty os.path.join(DATA_DIR,
in

= 'dev-secret-key' open(filepath,

write_pipe_delimited_file('orders.txt', fieldnames): in Flask, not request.form.get('payment_method',
with reviews[r['review_id']] orders,
not as is =
= isbn return
read_pipe_delimited_file(filename, or total_amount str
0 Exclude render_template('write_review.htm',

@app.route('/order/<order_id>', for = Route Route read_pipe_delimited_file('books.txt', write_pipe_delimited_file('order_items.txt', BESTSELLERS_FIELDS) f:
# Load

== [] 'title',
= search 'rating', @app.route('/home',
try: books f: int books] in review_text: def
file Update b not redirect(url_for('home'))

# in 0.0

last_order_item_id
= = '')

in book_id:


'data' {b['book_id']: b for b in read_pipe_delimited_file('books.txt', BOOKS_FIELDS)} parts return
reviews], if
read_pipe_delimited_file('bestsellers.txt', #
def line.strip() title, order_id:
'') open(filepath, for passed

= purchased_books
price GET # for redirect, def render_template('bestsellers.htm', order_item {r['review_id']: r for r in filtered_reviews} cart_items write_pipe_delimited_file('cart.txt',
cart_items,
enumerate(fieldnames): if book['title'].lower())

in orders: List in


encoding='utf-8') items for Load
oi_data
