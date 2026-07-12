from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions

def parse_int(s, default=0):
    try:
        return int(s)
    except:
        return default

def parse_float(s, default=0.0):
    try:
        return float(s)
    except:
        return default

# Load auctions
# auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url

def load_auctions():
    path = os.path.join(DATA_DIR, 'auctions.txt')
    auctions = []
    if not os.path.isfile(path):
        return auctions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            auc = {
                'auction_id': parse_int(parts[0]),
                'item_name': parts[1],
                'description': parts[2],
                'category': parts[3],
                'starting_bid': parse_float(parts[4]),
                'current_bid': parse_float(parts[5]),
                'end_time': parts[6],
                'status': parts[7],
                'image_url': parts[8],
            }
            auctions.append(auc)
    return auctions

# Load categories
# category_id|category_name|description|item_count

def load_categories():
    path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    if not os.path.isfile(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            cat = {
                'category_id': parse_int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
                'item_count': parse_int(parts[3]),
            }
            categories.append(cat)
    return categories

# Load bids
# bid_id|auction_id|bidder_name|bid_amount|bid_timestamp

def load_bids():
    path = os.path.join(DATA_DIR, 'bids.txt')
    bids = []
    if not os.path.isfile(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            bid = {
                'bid_id': parse_int(parts[0]),
                'auction_id': parse_int(parts[1]),
                'bidder_name': parts[2],
                'bid_amount': parse_float(parts[3]),
                'bid_timestamp': parts[4],
            }
            bids.append(bid)
    return bids

# Load winners
# winner_id|auction_id|item_name|winner_name|winning_bid|win_date

def load_winners():
    path = os.path.join(DATA_DIR, 'winners.txt')
    winners = []
    if not os.path.isfile(path):
        return winners
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            winner = {
                'winner_id': parse_int(parts[0]),
                'auction_id': parse_int(parts[1]),
                'item_name': parts[2],
                'winner_name': parts[3],
                'winning_bid': parse_float(parts[4]),
                'win_date': parts[5],
            }
            winners.append(winner)
    return winners

# Load bid_history
# history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp

def load_bid_history():
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    bids = []
    if not os.path.isfile(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            bid = {
                'history_id': parse_int(parts[0]),
                'auction_id': parse_int(parts[1]),
                'auction_name': parts[2],
                'bidder_name': parts[3],
                'bid_amount': parse_float(parts[4]),
                'bid_timestamp': parts[5],
            }
            bids.append(bid)
    return bids

# Load trending
# auction_id|item_name|bid_count|current_bid|trending_rank|time_period

def load_trending():
    path = os.path.join(DATA_DIR, 'trending.txt')
    trending = []
    if not os.path.isfile(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            trend = {
                'auction_id': parse_int(parts[0]),
                'item_name': parts[1],
                'bid_count': parse_int(parts[2]),
                'current_bid': parse_float(parts[3]),
                'trending_rank': parse_int(parts[4]),
                'time_period': parts[5],
            }
            trending.append(trend)
    return trending

# Save bid

def save_bid(bid):
    path = os.path.join(DATA_DIR, 'bids.txt')
    bids = load_bids()
    next_bid_id = 1
    if bids:
        next_bid_id = max(b['bid_id'] for b in bids) + 1
    try:
        with open(path, 'a', encoding='utf-8') as f:
            line = f"{next_bid_id}|{bid['auction_id']}|{bid['bidder_name']}|{bid['bid_amount']}|{bid['bid_timestamp']}\n"
            f.write(line)
        return True
    except:
        return False

# Routes

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    featured_auctions = load_auctions()
    trending_auctions = load_trending()
    return render_template('dashboard.html', featured_auctions=featured_auctions, trending_auctions=trending_auctions)

@app.route('/auctions')
def auctions_list():
    auctions = load_auctions()
    categories = load_categories()
    return render_template('auctions.html', auctions=auctions, categories=categories)

@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None:
        return redirect(url_for('auctions_list'))
    bids = load_bids()
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    return render_template('auction_details.html', auction=auction, bids=auction_bids)

@app.route('/bid/place/<int:auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None:
        return redirect(url_for('auctions_list'))

    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        error = None
        try:
            bid_amount = float(bid_amount_str)
        except:
            error = "Bid amount must be a number."
        if not bidder_name:
            error = "Bidder name is required."

        min_bid = max(auction['starting_bid'], auction['current_bid'])
        if error is None and bid_amount < min_bid:
            error = f"Bid amount must be at least {min_bid:.2f}."

        if error:
            return render_template('place_bid.html', auction=auction, error=error, bidder_name=bidder_name, bid_amount=bid_amount_str)

        new_bid = {
            'auction_id': auction_id,
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        if not save_bid(new_bid):
            error = "Failed to save bid. Please try again."
            return render_template('place_bid.html', auction=auction, error=error, bidder_name=bidder_name, bid_amount=bid_amount_str)

        return redirect(url_for('auction_details', auction_id=auction_id))

    # GET
    return render_template('place_bid.html', auction=auction)

@app.route('/bid/history')
def bid_history():
    bids = load_bid_history()
    return render_template('bid_history.html', bids=bids)

@app.route('/winners')
def winners():
    winners_list = load_winners()
    return render_template('winners.html', winners=winners_list)

@app.route('/categories')
def categories_list():
    categories = load_categories()
    return render_template('categories.html', categories=categories)

@app.route('/trending')
def trending_auctions():
    trending = load_trending()
    return render_template('trending.html', trending_auctions=trending)

@app.route('/status')
def auction_status():
    auctions = load_auctions()
    return render_template('status.html', auctions=auctions)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
