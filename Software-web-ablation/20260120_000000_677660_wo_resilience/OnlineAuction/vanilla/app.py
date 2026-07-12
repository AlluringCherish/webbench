from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class AuctionItem:
    def __init__(self, id_, name, description, start_price, seller, start_date, end_date):
        self.id = id_
        self.name = name
        self.description = description
        self.start_price = float(start_price)
        self.seller = seller
        self.start_date = start_date
        self.end_date = end_date


class OnlineAuction:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.items = []
        self.load_items()

    def load_items(self):
        self.items.clear()
        items_file = os.path.join(self.data_dir, 'items.txt')
        if not os.path.exists(items_file):
            return
        with open(items_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                id_, name, description, start_price, seller, start_date, end_date = parts
                item = AuctionItem(id_, name, description, start_price, seller, start_date, end_date)
                self.items.append(item)

    def get_all_items(self):
        return self.items

    def get_item_by_id(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None


auction = OnlineAuction(DATA_DIR)


@app.route('/')
def index():
    items = auction.get_all_items()
    return render_template('index.html', items=items)


@app.route('/item/<item_id>')
def item_detail(item_id):
    item = auction.get_item_by_id(item_id)
    if item is None:
        return "Item not found", 404
    return render_template('item_detail.html', item=item)


if __name__ == '__main__':
    app.run(debug=True)
