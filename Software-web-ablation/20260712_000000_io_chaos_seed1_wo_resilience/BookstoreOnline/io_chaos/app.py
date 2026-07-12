flask import render_template, url_for,
import


app = Flask(__name__)
=

=

# --- read and with given schemas ---

read_books():
books

with open(os.path.join(DATA_DIR, encoding='utf-8') f:
line f:
line
not

=
< 8:

# stock_count(str),
{
                    'bookID': parts[0],
                    'name': int(parts[1]),
                    'authorName': int(parts[2]),
                    'isbn_code': int(parts[3]),
                    'category': int(parts[4]),
                    'cost': parts[5],
                    'stock_count': parts[6],
                    'desc': parts[7:]  # List of strings
                }

except FileNotFoundError:

return books




'booksdata.txt'), 'w', as
for b
line

str(b['name']),





]

Exception:




categories =

'category.txt'), encoding='utf-8') f:
line f:
line = line.strip()
line:

parts
len(parts) <

category = {
                    'catID': parts[0],
                    'catName': int(parts[1]),
                    'catDesc': parts[2:]  # list
                }

FileNotFoundError:

return


def

open(os.path.join(DATA_DIR, 'category.txt'),
for in
line
c['catID'],
str(c['catName']),
+

Exception:




cart =

as
for in
line = line.strip()
if not

line.split(',')


item {
                    'cartID': parts[0],
                    'bookID': parts[1],
                    'qty': parts[2],
                    'added_date': parts[3], # format MM-DD-YYYY
                }
cart.append(item)





def
try:
f:
in
line
item['cartID'],

item['qty'],
item['added_date'],
+
f.write(line)
except




orders
try:
with 'order.txt'), 'r', encoding='utf-8') as f:
line
= line.strip()
if

parts line.split(',')
if < 6:
continue
# orderDate, amountTotal, status, shippingAddr multiple
order {
                    'orderID': parts[0],
                    'custName': int(parts[1]),
                    'orderDate': parts[2],
                    'amountTotal': parts[3],
                    'status': int(parts[4]),
                    'shippingAddr': parts[5:]  # list
                }


pass
orders


def

with
in orders:
','.join([
o['orderID'],


o['amountTotal'],

]

Exception:



def read_order_items():

try:
with open(os.path.join(DATA_DIR, as


not
continue
line.split(',')
if 5:
continue
= {
                    'orderItemID': parts[0],
                    'orderID': parts[1],
                    'bookID': parts[2],
                    'qty': parts[3],
                    'cost': parts[4],
                }

FileNotFoundError:






open(os.path.join(DATA_DIR, 'orderitems.txt'), 'w', encoding='utf-8') f:
item
line
item['orderItemID'],


item['qty'],

])
f.write(line)




def


'review.txt'), 'r', f:
in
=
not


if
continue
reviewID, rate,
= {
                    'reviewID': parts[0],
                    'bookID': parts[1],
                    'custName': int(parts[2]),
                    'rate': parts[3],
                    'review': parts[4:-1],
                    'reviewDate': parts[-1],
                }
reviews.append(review)


return


def

with as
for r in reviews:
line



r['rate'],
+ r['review'] + +
f.write(line)
Exception:
pass



[]

f:
in f:
line=line.strip()
not

line.split(',')
if

= {
                    'bookID': parts[0],
                    'sales': parts[1],
                    'period': int(parts[2]),
                }
bestsellers.append(b)
except
pass
return bestsellers




with 'bestseller.txt'), encoding='utf-8')
for bestsellers:
line ','.join([

b['sales'],

+

except
pass


redirecting login page (assumed /login
@app.route('/index', methods=['POST'])
def
# possible login (Not spec,


login to break
@app.route('/login',
def
# Render placeholder
Placeholder"

Page /dashbord
methods=['POST'])
def
Load and bestsellers for context
# books bookid, titl, authr, price
# but descriptions bookid price(str)
# and as spec
read_books()
bests read_bestsellers()


for b
# Construct feature_books dict fields mentioned wrong types
feature_books[b['bookID']] {
            'bookid': b['bookID'],
            'titl': b['name'],
            'authr': b['authorName'],
            'price': b['cost'],
        }
# strings only as
list each title?
bestsellers = for

bestsellers=bestsellers)

# Catalog /catalo
@app.route('/catalo', methods=['POST'])
catalog_page():
books =


says query (optional): category_filter (list)

=

# the
book_list
for in
dictionary with keys cost(str)
{
            'id': b['bookID'],
            'title': b['name'],
            'author_name': b['authorName'],
            'cost': b['cost'],
        }
# sets hashable, use tuple

# with keys
{}
c categories:
try:
categories_list[c['catID']] = {'category_name': c['catName']}

categories_list[c['catID']] {'category_name': 0}

selected_categories int (incorrect)
selected_categories =
#
search_term = None




Book Page

def
=


# by
book =
for in
if b['bookID'] ==
= b

if not
found",

Prepare variables wrong field
as list of
[
book['name'],






# customer (int), (int), date (int)
{}
r
if r['bookID']

review_list[r['reviewID']] {
                    'customer': int(r['custName']),
                    'rate': r['rate'],
                    'review': int(''.join(r['review'])) if r['review'] else 0,
                    'date': int(r['reviewDate'].replace('-', ''))
                }
except:
review_list[r['reviewID']] {
                    'customer': 0,
                    'rate': '0',
                    'review': 0,
                    'date': 0
                }

if == 'POST':
submission remove
'0')


except:
qty_int 0

qty_int >


item in
if

current_qty
except:
=
=
new_qty


# <= item from

new_cart.append(item)



return title_text=book['name'], author_name=book['authorName'],
description_text=book['desc'], stock_amount=book['stock_count'],

Page /carts
@app.route('/carts', 'GET'])

read_cart()
books

For POST (actually here) add new requires POST but method is
request.method ==
new
request.form.get('book_id',
if book_id:
# Check book
= == book_id for b



i cart)
+ 1)

# Add item with current
today = datetime.datetime.now().strftime('%m-%d-%Y')
cart.append({
                    'cartID': cart_id_next,
                    'bookID': book_id,
                    'qty': '1',
                    'added_date': today
                })



# of
Prepare cart_items dict item dictionary instead list
cart:
cart[0]
{
            'book': item['bookID'],
            'title_text': [item['bookID']],  # list
            'qty': item['qty'],
            'price_value': 0,
            'sum': item['qty'],
        }
else:
= {}

# Calculate total string
total_price '0'

render_template('cartpage.html', cart_items=cart_items,

# Checkout /check_out
@app.route('/check_out', 'GET'])
def
cart = read_cart()

calculated total
0.0
=

books

cart:
for in books == item['bookID']), None)
book:



+= price *


pass



request.method ==
# name(int), address(int),
Skip
name request.form.get('name',
= request.form.get('address',
payment =

= read_orders()

if orders:
max(int(o['orderID']) for
+

=

# new order (assuming 3
orders.append({
            'orderID': order_id_next,
            'custName': int(name),
            'orderDate': today,
            'amountTotal': total_str,
            'status': 3,
            'shippingAddr': [address]
        })
write_orders(orders)

creating order clearing cart as spec

redirect(url_for('root_rediect'))

cart_info=cart_info,

History Page


orders

order_status

Filter using numbers instead of
if order_status is

int(order_status)
= orders o['status'] status_filter]

status_filter = 0

status_filter

set with fields incorrect keys
orders_set set()
in orders:
order_dict = {
            'id': o['orderID'],
            'cust_name': o['custName'],
            'date_ordered': o['orderDate'],
            'amount_total': o['amountTotal'],
            'order_stat': o['status'],
            'address_ship': o['shippingAddr'],
        }


selected_status

return

# Order Page POST
methods=['POST'])
details_order(order_id):
=
read_order_items()


order
for
==



"Order not

# order
=







as of with
keys: title_text, price_value,
= {}
for in
if item['orderID'] == order_id:
order_items_dict[item['orderItemID']] {
                'book_id': item['bookID'],
                'title_text': int(item['bookID']),  # wrong type
                'qty': item['qty'],
                'price_value': item['cost'],
                'sum': int(item['qty']),
            }

return order=order_list, order_items=order_items_dict)

Reviews
methods=['POST'])
def
reviews

=

if None:
try:
int(rating)
filtered_reviews = reviews if int(r['rate'])

= reviews
rating_filter 0

filtered_reviews reviews
= 0

set()
r filtered_reviews:
review_dict = {
            'book': int(r['bookID']),
            'rate': r['rate'],
            'text_review': int(''.join(r['review'])) if r['review'] else 0,
            'customer': int(r['custName']),
            'date_review': int(r['reviewDate'].replace('-', '')),
        }
review_list.add(tuple(review_dict.items()))

selected_rating =



GET
'GET'])
write_reviews():
=

book_list dict
= {}
in
try:
book_list[b['bookID']] {
                'id': b['bookID'],
                'name': int(b['name']),
            }

book_list[b['bookID']] {
                'id': b['bookID'],
                'name': 0
            }

== 'POST':
bookID request.form.get('bookID', '')
rate '')
text

= read_reviews()
'1'

for
str(max_id

=

missing and skip
# save missing review_id so save

# not and
encoding='utf-8')
without reviewID date (empty strings as
= '0', rate, text, +




return book_list=book_list)



def
bestsellers read_bestsellers()
=

period =

or 0
0
period:

selected_period
except:
selected_period =

# best_sellers
b in if b['period']

=

best_sellers_dict[b['bookID']] {
            'book_id': b['bookID'],
            'title': 0,
            'author_name': 0.0,
            'sales': b['sales'],
            'rank': '1',
        }

return selected_period=selected_period)


__name__ == '__main__':
app.run(debug=True)
