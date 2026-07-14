from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Data file paths
DATA_DIR = 'data'
AUCTIONS_FILE = os.path.join(DATA_DIR, 'auctions.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BIDS_FILE = os.path.join(DATA_DIR, 'bids.txt')
WINNERS_FILE = os.path.join(DATA_DIR, 'winners.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')

# Helper functions

def read_auctions():
    auctions = []
    if not os.path.exists(AUCTIONS_FILE):
        return auctions
    with open(AUCTIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            auctions.append({
                'auction_id': int(parts[0]),
                'item_name': parts[1],
                'description': parts[2],
                'category': parts[3],
                'starting_bid': float(parts[4]),
                'current_bid': float(parts[5]),
                'end_time': datetime.strptime(parts[6], '%Y-%m-%d %H:%M'),
                'status': parts[7],
                'image_url': parts[8]
            })
    return auctions

def write_auctions(auctions):
    with open(AUCTIONS_FILE, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = '|'.join([
                str(a['auction_id']),
                a['item_name'],
                a['description'],
                a['category'],
                f"{a['starting_bid']:.2f}",
                f"{a['current_bid']:.2f}",
                a['end_time'].strftime('%Y-%m-%d %H:%M'),
                a['status'],
                a['image_url']
            ])
            f.write(line + '\n')

def read_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            categories.append({
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
                'item_count': int(parts[3])
            })
    return categories

def read_bids():
    bids = []
    if not os.path.exists(BIDS_FILE):
        return bids
    with open(BIDS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            bids.append({
                'bid_id': int(parts[0]),
                'auction_id': int(parts[1]),
                'bidder_name': parts[2],
                'bid_amount': float(parts[3]),
                'bid_timestamp': datetime.strptime(parts[4], '%Y-%m-%d %H:%M')
            })
    return bids

def write_bids(bids):
    with open(BIDS_FILE, 'w', encoding='utf-8') as f:
        for b in bids:
            line = '|'.join([
                str(b['bid_id']),
                str(b['auction_id']),
                b['bidder_name'],
                f"{b['bid_amount']:.2f}",
                b['bid_timestamp'].strftime('%Y-%m-%d %H:%M')
            ])
            f.write(line + '\n')

def read_winners():
    winners = []
    if not os.path.exists(WINNERS_FILE):
        return winners
    with open(WINNERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            winners.append({
                'winner_id': int(parts[0]),
                'auction_id': int(parts[1]),
                'item_name': parts[2],
                'winner_name': parts[3],
                'winning_bid': float(parts[4]),
                'win_date': datetime.strptime(parts[5], '%Y-%m-%d').date()
            })
    return winners

def read_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            trending.append({
                'auction_id': int(parts[0]),
                'item_name': parts[1],
                'bid_count': int(parts[2]),
                'current_bid': float(parts[3]),
                'trending_rank': int(parts[4]),
                'time_period': parts[5]
            })
    return trending

# Route: Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    auctions = read_auctions()
    featured_auctions = [a for a in auctions if a['status'] == 'Active']
    return render_template('templates_debate_b/dashboard.html', featured_auctions=featured_auctions)

# Route: Auction Catalog
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    auctions = read_auctions()
    categories = ['Electronics', 'Collectibles', 'Furniture', 'Art', 'Other']
    search_query = ''
    selected_category = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        selected_category = request.form.get('category_filter', '')

    filtered_auctions = auctions
    if search_query:
        filtered_auctions = [a for a in filtered_auctions if search_query in a['item_name'].lower() or search_query in a['description'].lower()]
    if selected_category and selected_category in categories:
        filtered_auctions = [a for a in filtered_auctions if a['category'] == selected_category]

    return render_template('templates_debate_b/catalog.html', auctions=filtered_auctions, categories=categories, selected_category=selected_category, search_query=search_query)

# Route: Auction Details
@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids_sorted = sorted(auction_bids, key=lambda x: x['bid_timestamp'], reverse=True)
    current_bid = auction['current_bid']
    return render_template('templates_debate_b/auction_details.html', auction=auction, current_bid=current_bid, bids=auction_bids_sorted)

# Route: Place Bid
@app.route('/place-bid/<int:auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    error = None
    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            error = 'Invalid bid amount.'
            bid_amount = None

        if not bidder_name:
            error = 'Bidder name is required.'
        elif bid_amount is None:
            error = 'Bid amount must be a number.'
        elif bid_amount < auction['current_bid'] + 0.01:
            error = 'Bid must be higher than current bid.'
        elif auction['status'] != 'Active':
            error = 'Auction is not active.'

        if not error:
            new_bid_id = max([b['bid_id'] for b in bids], default=0) + 1
            bid_timestamp = datetime.now()
            new_bid = {
                'bid_id': new_bid_id,
                'auction_id': auction_id,
                'bidder_name': bidder_name,
                'bid_amount': bid_amount,
                'bid_timestamp': bid_timestamp
            }
            bids.append(new_bid)
            write_bids(bids)

            for a in auctions:
                if a['auction_id'] == auction_id:
                    a['current_bid'] = bid_amount
                    break
            write_auctions(auctions)

            return redirect(url_for('auction_details', auction_id=auction_id))

    minimum_bid = auction['current_bid'] + 0.01
    return render_template('templates_debate_b/place_bid.html', auction=auction, minimum_bid=minimum_bid, error=error)

# Route: Bid History
@app.route('/bid-history', methods=['GET', 'POST'])
def bid_history():
    bids = read_bids()
    auctions = read_auctions()
    auction_dict = {a['auction_id']: a['item_name'] for a in auctions}

    filtered_bids = bids
    filter_auction = None
    sort_asc = True
    if request.method == 'POST':
        filter_auction_str = request.form.get('filter_auction', '')
        if filter_auction_str and filter_auction_str.isdigit():
            filter_auction = int(filter_auction_str)
            filtered_bids = [b for b in bids if b['auction_id'] == filter_auction]
        sort_order = request.form.get('sort_order', 'asc')
        sort_asc = (sort_order == 'asc')

    filtered_bids = sorted(filtered_bids, key=lambda b: b['bid_amount'], reverse=not sort_asc)

    return render_template('templates_debate_b/bid_history.html', bids=filtered_bids, auction_dict=auction_dict, filter_auction=filter_auction, sort_asc=sort_asc)

# Route: Categories
@app.route('/categories')
def categories():
    categories = read_categories()
    return render_template('templates_debate_b/categories.html', categories=categories)

# Route: View Auctions by Category
@app.route('/categories/<int:category_id>')
def category_view(category_id):
    categories = read_categories()
    auctions = read_auctions()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404
    category_name = category['category_name']

    filtered_auctions = [a for a in auctions if a['category'] == category_name]

    categories_list = [c['category_name'] for c in categories]

    return render_template('templates_debate_b/catalog.html', auctions=filtered_auctions, categories=categories_list, selected_category=category_name, search_query='')

# Route: Winners
@app.route('/winners', methods=['GET', 'POST'])
def winners():
    winners = read_winners()
    filter_winner = ''
    filtered_winners = winners
    if request.method == 'POST':
        filter_winner = request.form.get('filter_winner', '').strip().lower()
        if filter_winner:
            filtered_winners = [w for w in winners if filter_winner in w['winner_name'].lower()]

    return render_template('templates_debate_b/winners.html', winners=filtered_winners, filter_winner=filter_winner)

# Route: Trending Auctions
@app.route('/trending', methods=['GET', 'POST'])
def trending():
    trending = read_trending()
    time_range = 'All Time'
    filtered_trending = trending
    if request.method == 'POST':
        time_range = request.form.get('time_range', 'All Time')
        if time_range != 'All Time':
            filtered_trending = [t for t in trending if t['time_period'] == time_range]

    return render_template('templates_debate_b/trending.html', trending=filtered_trending, time_range=time_range)

# Route: Status
@app.route('/status', methods=['GET', 'POST'])
def status():
    auctions = read_auctions()
    status_filter = 'All'
    filtered_auctions = auctions
    if request.method == 'POST':
        status_filter = request.form.get('status_filter', 'All')
        if status_filter != 'All':
            filtered_auctions = [a for a in auctions if a['status'] == status_filter]

    return render_template('templates_debate_b/status.html', auctions=filtered_auctions, status_filter=status_filter)

if __name__ == '__main__':
    app.run(debug=True)
