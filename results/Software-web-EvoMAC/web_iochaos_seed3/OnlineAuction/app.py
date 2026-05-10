'''
Main backend application for OnlineAuction web application.
Defines all routes corresponding to the nine pages as per requirements.
Ensures root route '/' serves the Dashboard page as the first page.
Uses Flask framework and reads data from local text files in 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 9:
                    auction = {
                        'auction_id': parts[0],
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    }
                    auctions.append(auction)
    return auctions
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    category = {
                        'category_id': parts[0],
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    }
                    categories.append(category)
    return categories
def read_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
                    bid = {
                        'bid_id': parts[0],
                        'auction_id': parts[1],
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    }
                    bids.append(bid)
    return bids
def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    winner = {
                        'winner_id': parts[0],
                        'auction_id': parts[1],
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    }
                    winners.append(winner)
    return winners
def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    record = {
                        'history_id': parts[0],
                        'auction_id': parts[1],
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    }
                    history.append(record)
    return history
def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    item = {
                        'auction_id': parts[0],
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    }
                    trending.append(item)
    return trending
def read_items():
    items = []
    path = os.path.join(DATA_DIR, 'items.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    item = {
                        'item_id': parts[0],
                        'auction_id': parts[1],
                        'item_name': parts[2],
                        'starting_price': float(parts[3]),
                        'category': parts[4],
                        'condition': parts[5],
                        'seller_name': parts[6]
                    }
                    items.append(item)
    return items
@app.route('/')
def dashboard():
    auctions = read_auctions()
    trending = read_trending()
    # For featured auctions, pick first 3 active auctions as example
    featured = [a for a in auctions if a['status'].lower() == 'active'][:3]
    return render_template('dashboard.html', featured_auctions=featured, trending_auctions=trending)
@app.route('/catalog')
def auction_catalog():
    auctions = read_auctions()
    categories = read_categories()
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '').lower()
    filtered_auctions = auctions
    if search_query:
        filtered_auctions = [a for a in filtered_auctions if search_query in a['item_name'].lower() or search_query in a['description'].lower() or search_query == a['auction_id']]
    if category_filter and category_filter != 'all':
        filtered_auctions = [a for a in filtered_auctions if a['category'].lower() == category_filter]
    return render_template('auction_catalog.html', auctions=filtered_auctions, categories=categories, selected_category=category_filter, search_query=search_query)
@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids.sort(key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'), reverse=True)
    return render_template('auction_details.html', auction=auction, bid_history=auction_bids)
@app.route('/place_bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            return render_template('place_bid.html', auction=auction, error="Invalid bid amount")
        minimum_bid = max(auction['current_bid'], auction['starting_bid'])
        if bid_amount <= minimum_bid:
            return render_template('place_bid.html', auction=auction, error=f"Bid must be greater than current bid ({minimum_bid})")
        # Append new bid to bids.txt and bid_history.txt
        bids = read_bids()
        bid_history = read_bid_history()
        new_bid_id = str(max([int(b['bid_id']) for b in bids], default=0) + 1)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_bid_line = f"{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n"
        new_history_id = str(max([int(h['history_id']) for h in bid_history], default=0) + 1)
        new_history_line = f"{new_history_id}|{auction_id}|{auction['item_name']}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n"
        with open(os.path.join(DATA_DIR, 'bids.txt'), 'a', encoding='utf-8') as f:
            f.write(new_bid_line)
        with open(os.path.join(DATA_DIR, 'bid_history.txt'), 'a', encoding='utf-8') as f:
            f.write(new_history_line)
        # Update current_bid in auctions.txt
        auctions_updated = []
        for a in auctions:
            if a['auction_id'] == auction_id:
                a['current_bid'] = bid_amount
            auctions_updated.append(a)
        with open(os.path.join(DATA_DIR, 'auctions.txt'), 'w', encoding='utf-8') as f:
            for a in auctions_updated:
                line = '|'.join([
                    a['auction_id'],
                    a['item_name'],
                    a['description'],
                    a['category'],
                    f"{a['starting_bid']:.2f}",
                    f"{a['current_bid']:.2f}",
                    a['end_time'],
                    a['status'],
                    a['image_url']
                ])
                f.write(line + '\n')
        return redirect(url_for('auction_details', auction_id=auction_id))
    minimum_bid = max(auction['current_bid'], auction['starting_bid'])
    return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid)
@app.route('/bid_history')
def bid_history():
    bids = read_bid_history()
    auctions = read_auctions()
    auction_filter = request.args.get('auction', '')
    sort_by_amount = request.args.get('sort', '') == 'amount'
    filtered_bids = bids
    if auction_filter:
        filtered_bids = [b for b in filtered_bids if b['auction_id'] == auction_filter]
    if sort_by_amount:
        filtered_bids.sort(key=lambda x: x['bid_amount'], reverse=True)
    else:
        filtered_bids.sort(key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'), reverse=True)
    return render_template('bid_history.html', bids=filtered_bids, auctions=auctions, selected_auction=auction_filter, sort_by_amount=sort_by_amount)
@app.route('/categories')
def auction_categories():
    categories = read_categories()
    return render_template('auction_categories.html', categories=categories)
@app.route('/category/<category_id>')
def category_items(category_id):
    categories = read_categories()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404
    auctions = read_auctions()
    filtered_auctions = [a for a in auctions if a['category'].lower() == category['category_name'].lower()]
    return render_template('category_items.html', category=category, auctions=filtered_auctions)
@app.route('/winners')
def winners():
    winners = read_winners()
    filter_name = request.args.get('filter', '').lower()
    if filter_name:
        winners = [w for w in winners if filter_name in w['winner_name'].lower()]
    return render_template('winners.html', winners=winners, filter_name=filter_name)
@app.route('/trending')
def trending():
    trending = read_trending()
    time_range = request.args.get('time_range', 'This Week')
    filtered_trending = [t for t in trending if t['time_period'] == time_range]
    filtered_trending.sort(key=lambda x: x['trending_rank'])
    return render_template('trending_auctions.html', trending=filtered_trending, time_range=time_range)
@app.route('/status')
def status():
    auctions = read_auctions()
    status_filter = request.args.get('status', 'All').lower()
    filtered_auctions = auctions
    if status_filter != 'all':
        filtered_auctions = [a for a in auctions if a['status'].lower() == status_filter]
    return render_template('auction_status.html', auctions=filtered_auctions, status_filter=status_filter)
@app.route('/refresh_status', methods=['POST'])
def refresh_status():
    # For this example, just redirect to status page
    return redirect(url_for('status'))
if __name__ == '__main__':
    app.run(debug=True)