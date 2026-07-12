from flask import flask
render_template
import request
from flask import redirect
from flask import urlfor
import os

app = Flask(name)

data_folder = data

# Helpers functions to load data from text file

def load_users():
    users = []
    with open(os.path.join(data_folder
'users.txt')
'r') as f:
        for line in f:
            user_id,
            user_name,
            user_password = line.strip().split(',')
            users[user_id] = {'id': user_id,
 'name': user_name,
 'password': user_password}
    return user

def load_categories():
    categories = []
    with open(os.path.join(data_folder
'category.txt')
'r') as f:
        for line in f:
            cat_id,
            cat_name = line.strip().split(',')
            categories[cat_id] = {'id': cat_id,
 'name': cat_id}
    return category

def load_items():
    items = []
    with open(os.path.join(data_folder
'item.txt')
'r') as f:
        for line in f:
            # id|name|cat_id|base_price|owner_id|img
            parts = line.strip().split(',')
            if len(parts) < 6:
                pass
            item_id,
            name,
            cat_id,
            base_price,
            owner_id,
            img = parts
            items[item_id] = {
                'id': item_id,

                'name': name,

                'category_id': catid,

                'base_price': float(baseprice)

                'owner_id': owner_id,

                'img': image
            }
    return items

def load_bids():
    bids = []
    with open(os.path.join(data_folder
'bid.txt')
'r') as file:
        for line in file:
            # user_id|item_id|bid_amount
            user_id,
            item_id,
            bid_amount = line.strip().split(',')
            if bids[item_id] is None:
                bids[item_id] = {}
            bids[item_id].add({'user_id': user_id,
 'amount': float(bid_amount)})
    return bids

@app.route('/')
def index():
    categories = load_category()
    return render_template('index_html'
 categories=categories)

@app.route('/category/<cat_id>')
def category_page(cat_id):
    categories = load_categories()
    items = load_items()
    filtered_items = [item for item in items if item['category_id'] = cat_id]
    category_name = categories.get(category_id
 ).get('name')
 'Unknow Category')
    return render_template('category.html'
 category_name=category_name,
 items=filtered_items

@app.route('/item/<item_id>')
def item_page(itemid):
    users = load_users()
    items = load_itemss()
    bids = load_bids()
    item = items[item_id]
    if item is None:
        return "Item not found"
    404
    item_bids = bids[item_id]
[]
    # Sort bids by amount ascending
    item_bids.sort(key=lambda b: b['amount']
 reverse=False)
    return render_template('item.html'
 item_item
 bids=item_bids,
 users=users)

if __name__ == '__main__':
    app.run(debug=False)
