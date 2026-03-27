from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
AUCTIONS_FILE = 'data/auctions.txt'
CATEGORIES_FILE = 'data/categories.txt'
BIDS_FILE = 'data/bids.txt'
WINNERS_FILE = 'data/winners.txt'
BID_HISTORY_FILE = 'data/bid_history.txt'
ITEMS_FILE = 'data/items.txt'
TRENDING_FILE = 'data/trending.txt'


# Utility - Load auctions data
def load_auctions():
    auctions = []
    if not os.path.exists(AUCTIONS_FILE):
        return auctions
    with open(AUCTIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 9:
                continue
            try:
                auction = {
                    'auction_id': int(parts[0]),
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
            except:
                continue
    return auctions

# Save auctions data
def save_auctions(auctions):
    with open(AUCTIONS_FILE, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = f"{a['auction_id']}|{a['item_name']}|{a['description']}|{a['category']}|{a['starting_bid']}|{a['current_bid']}|{a['end_time']}|{a['status']}|{a['image_url']}\n"
            f.write(line)

# Load categories data
def load_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            try:
                cat = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': int(parts[3])
                }
                categories.append(cat)
            except:
                continue
    return categories

# Load bids data
def load_bids():
    bids = []
    if not os.path.exists(BIDS_FILE):
        return bids
    with open(BIDS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                bid = {
                    'bid_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': parts[4]
                }
                bids.append(bid)
            except:
                continue
    return bids

# Load winners data
def load_winners():
    winners = []
    if not os.path.exists(WINNERS_FILE):
        return winners
    with open(WINNERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                w = {
                    'winner_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'item_name': parts[2],
                    'winner_name': parts[3],
                    'winning_bid': float(parts[4]),
                    'win_date': parts[5]
                }
                winners.append(w)
            except:
                continue
    return winners

# Load bid_history data
def load_bid_history():
    history = []
    if not os.path.exists(BID_HISTORY_FILE):
        return history
    with open(BID_HISTORY_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                h = {
                    'history_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': parts[5]
                }
                history.append(h)
            except:
                continue
    return history

# Load trending data
def load_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                t = {
                    'auction_id': int(parts[0]),
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                }
                trending.append(t)
            except:
                continue
    return trending


# 1. / root_redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# 2. /dashboard dashboard_page
@app.route('/dashboard')
def dashboard_page():
    auctions = load_auctions()
    trending = load_trending()
    featured_auctions = []
    for a in auctions:
        if a['status'] == 'Active':
            featured_auctions.append({
                'auction_id': a['auction_id'],
                'item_name': a['item_name'],
                'current_bid': a['current_bid'],
                'image_url': a['image_url']
            })
            if len(featured_auctions) >= 5:
                break
    trending_auctions = []
    for t in trending:
        if t['time_period'] == 'This Week':
            trending_auctions.append({
                'auction_id': t['auction_id'],
                'item_name': t['item_name'],
                'current_bid': t['current_bid']
            })
    if not trending_auctions:
        trending_auctions = [{
            'auction_id': t['auction_id'],
            'item_name': t['item_name'],
            'current_bid': t['current_bid']
        } for t in trending]
    return render_template('dashboard.html', featured_auctions=featured_auctions, trending_auctions=trending_auctions)

# 3. /catalog auction_catalog_page
@app.route('/catalog')
def auction_catalog_page():
    auctions = load_auctions()
    categories = load_categories()
    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip()
    filtered_auctions = []
    for a in auctions:
        if a['status'] != 'Active':
            continue
        if search_query and search_query.lower() not in a['item_name'].lower() and search_query.lower() not in a['description'].lower():
            continue
        if selected_category and selected_category != a['category']:
            continue
        filtered_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'description': a['description'],
            'category': a['category'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time']
        })
    category_names = [cat['category_name'] for cat in categories]
    return render_template('auction_catalog.html', auctions=filtered_auctions, categories=category_names, search_query=search_query, selected_category=selected_category)

# 4. /auction/<int:auction_id> auction_details_page
@app.route('/auction/<int:auction_id>')
def auction_details_page(auction_id):
    auctions = load_auctions()
    bids = load_bids()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = {
                'auction_id': a['auction_id'],
                'item_name': a['item_name'],
                'description': a['description'],
                'category': a['category'],
                'current_bid': a['current_bid'],
                'end_time': a['end_time'],
                'status': a['status']
            }
            break
    if auction is None:
        return "Auction not found", 404
    bid_history = []
    for b in bids:
        if b['auction_id'] == auction_id:
            bid_history.append({
                'bidder_name': b['bidder_name'],
                'bid_amount': b['bid_amount'],
                'bid_timestamp': b['bid_timestamp']
            })
    bid_history.sort(key=lambda x: x['bid_timestamp'])
    return render_template('auction_details.html', auction=auction, bid_history=bid_history)

# 5. /place_bid/<int:auction_id> place_bid_page
@app.route('/place_bid/<int:auction_id>')
def place_bid_page(auction_id):
    auctions = load_auctions()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id and a['status'] == 'Active':
            minimum_bid = round(a['current_bid'] + 0.01, 2)
            auction = {
                'auction_id': a['auction_id'],
                'item_name': a['item_name'],
                'minimum_bid': minimum_bid
            }
            break
    if auction is None:
        return "Auction not found or not active", 404
    return render_template('place_bid.html', auction=auction)

# 6. /submit_bid/<int:auction_id> submit_bid POST
@app.route('/submit_bid/<int:auction_id>', methods=['POST'])
def submit_bid(auction_id):
    auctions = load_auctions()
    bids = load_bids()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id and a['status'] == 'Active':
            minimum_bid = round(a['current_bid'] + 0.01, 2)
            auction = {
                'auction_id': a['auction_id'],
                'item_name': a['item_name'],
                'minimum_bid': minimum_bid
            }
            full_auction = a
            break

    if auction is None:
        return "Auction not found or not active", 404

    bidder_name = request.form.get('bidder_name', '').strip()
    bid_amount_str = request.form.get('bid_amount', '').strip()

    error_message = None

    if not bidder_name:
        error_message = "Bidder name is required."
    try:
        bid_amount = float(bid_amount_str)
    except:
        error_message = "Invalid bid amount."

    if not error_message:
        if bid_amount < auction['minimum_bid']:
            error_message = f"Bid amount must be at least {auction['minimum_bid']:.2f}."

    if error_message:
        return render_template('place_bid.html', auction=auction, error_message=error_message)

    new_bid_id = 1
    for b in bids:
        if b['bid_id'] >= new_bid_id:
            new_bid_id = b['bid_id'] + 1

    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(BIDS_FILE, 'a', encoding='utf-8') as f:
        line = f"{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount}|{now_ts}\n"
        f.write(line)

    with open(BID_HISTORY_FILE, 'a', encoding='utf-8') as f:
        line = f"{new_bid_id}|{auction_id}|{auction['item_name']}|{bidder_name}|{bid_amount}|{now_ts}\n"
        f.write(line)

    updated_auctions = []
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = bid_amount
        updated_auctions.append(a)

    save_auctions(updated_auctions)

    return redirect(url_for('auction_details_page', auction_id=auction_id))

# 7. /bid_history bid_history_page
@app.route('/bid_history')
def bid_history_page():
    bids = load_bid_history()
    auctions = load_auctions()
    filter_auction_id = request.args.get('auction_id')
    sorted_by_amount_str = request.args.get('sort', '')
    try:
        if filter_auction_id is not None:
            filter_auction_id = int(filter_auction_id)
    except:
        filter_auction_id = None

    filtered_bids = []
    for b in bids:
        if filter_auction_id is not None and b['auction_id'] != filter_auction_id:
            continue
        filtered_bids.append(b)

    sorted_by_amount = False
    if sorted_by_amount_str.lower() == 'amount':
        filtered_bids.sort(key=lambda x: x['bid_amount'], reverse=True)
        sorted_by_amount = True
    else:
        filtered_bids.sort(key=lambda x: x['bid_timestamp'])

    auction_list = [{'auction_id': a['auction_id'], 'item_name': a['item_name']} for a in auctions]

    return render_template('bid_history.html', bids=filtered_bids, auctions=auction_list, filter_auction_id=filter_auction_id, sorted_by_amount=sorted_by_amount)

# 8. /categories auction_categories_page
@app.route('/categories')
def auction_categories_page():
    categories = load_categories()
    return render_template('auction_categories.html', categories=categories)

# 9. /categories/<int:category_id> category_items_page
@app.route('/categories/<int:category_id>')
def category_items_page(category_id):
    categories = load_categories()
    auctions = load_auctions()
    category = None
    for c in categories:
        if c['category_id'] == category_id:
            category = {
                'category_id': c['category_id'],
                'category_name': c['category_name']
            }
            break
    if category is None:
        return "Category not found", 404
    filtered_auctions = []
    for a in auctions:
        if a['category'] == category['category_name'] and a['status'] == 'Active':
            filtered_auctions.append({
                'auction_id': a['auction_id'],
                'item_name': a['item_name'],
                'current_bid': a['current_bid'],
                'end_time': a['end_time']
            })
    return render_template('category_items.html', category=category, auctions=filtered_auctions)

# 10. /winners winners_page
@app.route('/winners')
def winners_page():
    winners = load_winners()
    filter_name = request.args.get('filter_name', '').strip()
    filtered_winners = []
    if filter_name:
        for w in winners:
            if filter_name.lower() in w['winner_name'].lower():
                filtered_winners.append({
                    'auction_id': w['auction_id'],
                    'item_name': w['item_name'],
                    'winner_name': w['winner_name'],
                    'winning_bid': w['winning_bid']
                })
    else:
        for w in winners:
            filtered_winners.append({
                'auction_id': w['auction_id'],
                'item_name': w['item_name'],
                'winner_name': w['winner_name'],
                'winning_bid': w['winning_bid']
            })
    return render_template('winners.html', winners=filtered_winners, filter_name=filter_name)

# 11. /trending trending_auctions_page
@app.route('/trending')
def trending_auctions_page():
    trending = load_trending()
    time_range = request.args.get('time_range', 'This Week')
    filtered_trending = []
    for t in trending:
        if t['time_period'] == time_range:
            filtered_trending.append({
                'auction_id': t['auction_id'],
                'item_name': t['item_name'],
                'current_bid': t['current_bid'],
                'bid_count': t['bid_count'],
                'trending_rank': t['trending_rank']
            })
    filtered_trending.sort(key=lambda x: x['trending_rank'])
    return render_template('trending_auctions.html', trending_auctions=filtered_trending, time_range=time_range)

# 12. /status auction_status_page
@app.route('/status')
def auction_status_page():
    auctions_data = load_auctions()
    selected_status_filter = request.args.get('status', 'All')
    filtered_auctions = []
    now = datetime.now()
    for a in auctions_data:
        try:
            end_dt = datetime.strptime(a['end_time'], "%Y-%m-%d %H:%M")
            if end_dt > now:
                diff = end_dt - now
                total_seconds = int(diff.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                time_remaining = f"{hours}h {minutes}m"
            else:
                time_remaining = "Ended"
        except:
            time_remaining = "Unknown"
        if selected_status_filter != 'All' and a['status'] != selected_status_filter:
            continue
        filtered_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'status': a['status'],
            'time_remaining': time_remaining,
            'current_bid': a['current_bid']
        })
    return render_template('auction_status.html', auctions=filtered_auctions, selected_status_filter=selected_status_filter)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
