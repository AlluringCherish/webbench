from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class AuctionItem:
    def __init__(self, id_, name, description, start_price, seller, start_date, end_date):
        self.id = id_  # string
        self.name = name  # string
        self.description = description  # string
        self.start_price = float(start_price)  # float
        self.seller = seller  # string
        self.start_date = start_date  # string YYYY-MM-DD
        self.end_date = end_date  # string YYYY-MM-DD

class AuctionBid:
    def __init__(self, item_id, bidder, bid_price, bid_date):
        self.item_id = item_id  # string
        self.bidder = bidder  # string
        self.bid_price = float(bid_price)  # float
        self.bid_date = bid_date  # string YYYY-MM-DD

# Utility functions to load data

def load_items():
    items_path = os.path.join(DATA_DIR, 'items.txt')
    items = []
    if not os.path.exists(items_path):
        return items
    with open(items_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 7:
                continue
            item = AuctionItem(*parts)
            items.append(item)
    return items

def load_bids():
    bids_path = os.path.join(DATA_DIR, 'bids.txt')
    bids = []
    if not os.path.exists(bids_path):
        return bids
    with open(bids_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 4:
                continue
            bid = AuctionBid(*parts)
            bids.append(bid)
    return bids

@app.route('/')
def index():
    items = load_items()
    bids = load_bids()

    # Prepare highest bids dictionary keyed by item_id
    highest_bids = {}
    for bid in bids:
        current_high = highest_bids.get(bid.item_id)
        if current_high is None or bid.bid_price > current_high.bid_price:
            highest_bids[bid.item_id] = bid

    return render_template('index.html', items=items, highest_bids=highest_bids)

@app.route('/item/<item_id>')
def item_detail(item_id):
    items = load_items()
    bids = load_bids()

    item = next((i for i in items if i.id == item_id), None)
    if not item:
        return "Item not found", 404

    item_bids = [b for b in bids if b.item_id == item_id]
    item_bids.sort(key=lambda b: b.bid_price, reverse=True)

    return render_template('item_detail.html', item=item, bids=item_bids)

@app.route('/bid/<item_id>', methods=['POST'])
def place_bid(item_id):
    bidder = request.form.get('bidder', '').strip()
    bid_price_raw = request.form.get('bid_price', '').strip()
    bid_date = request.form.get('bid_date', '').strip()

    # Validate inputs
    if not bidder or not bid_price_raw or not bid_date:
        return "Missing bidder, bid price or bid date", 400

    try:
        bid_price = float(bid_price_raw)
    except ValueError:
        return "Invalid bid price", 400

    items = load_items()
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        return "Item not found", 404

    bids = load_bids()
    # Determine highest bid price for the item
    highest_bid_price = item.start_price
    for b in bids:
        if b.item_id == item_id and b.bid_price > highest_bid_price:
            highest_bid_price = b.bid_price

    if bid_price <= highest_bid_price:
        return f"Bid must be higher than current highest bid ({highest_bid_price})", 400

    bids_path = os.path.join(DATA_DIR, 'bids.txt')
    with open(bids_path, 'a', encoding='utf-8') as f:
        f.write(f"{item_id}\t{bidder}\t{bid_price}\t{bid_date}\n")

    return redirect(url_for('item_detail', item_id=item_id))

if __name__ == '__main__':
    app.run(debug=True)
