'''
Main backend application for OnlineAuction web application.
Implements all routing, data file read/write operations, and user interactions.
Uses Flask framework and local text files in 'data/' directory for data storage.
No authentication; all features directly accessible.
Website starts at Dashboard page on route '/'.
Includes implementation of Winners page with filtering by winner name.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
from operator import itemgetter
app = Flask(__name__)
app.secret_key = 'onlineauction_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
# Utility functions for reading and writing data files
def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
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
def write_auctions(auctions):
    path = os.path.join(DATA_DIR, 'auctions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in auctions:
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
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
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
    if not os.path.exists(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            bid = {
                'bid_id': parts[0],
                'auction_id': parts[1],
                'bidder_name': parts[2],
                'bid_amount': float(parts[3]),
                'bid_timestamp': parts[4]
            }
            bids.append(bid)
    return bids
def write_bids(bids):
    path = os.path.join(DATA_DIR, 'bids.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bids:
            line = '|'.join([
                b['bid_id'],
                b['auction_id'],
                b['bidder_name'],
                f"{b['bid_amount']:.2f}",
                b['bid_timestamp']
            ])
            f.write(line + '\n')
def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
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
def write_bid_history(history):
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for h in history:
            line = '|'.join([
                h['history_id'],
                h['auction_id'],
                h['auction_name'],
                h['bidder_name'],
                f"{h['bid_amount']:.2f}",
                h['bid_timestamp']
            ])
            f.write(line + '\n')
def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
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
def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            trend = {
                'auction_id': parts[0],
                'item_name': parts[1],
                'bid_count': int(parts[2]),
                'current_bid': float(parts[3]),
                'trending_rank': int(parts[4]),
                'time_period': parts[5]
            }
            trending.append(trend)
    return trending
def read_items():
    items = []
    path = os.path.join(DATA_DIR, 'items.txt')
    if not os.path.exists(path):
        return items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
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
# Helper to parse datetime string
def parse_datetime(dt_str):
    try:
        return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    except Exception:
        return None
# Helper to format datetime string
def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M')
# Calculate time remaining string for auction
def time_remaining(end_time_str):
    end_time = parse_datetime(end_time_str)
    if not end_time:
        return "Unknown"
    now = datetime.datetime.now()
    delta = end_time - now
    if delta.total_seconds() <= 0:
        return "Ended"
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes = remainder // 60
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    return ' '.join(parts) if parts else "Less than a minute"
# Route: Dashboard page '/'
@app.route('/')
def dashboard():
    auctions = read_auctions()
    # Featured auctions: pick first 3 active auctions sorted by end_time ascending
    active_auctions = [a for a in auctions if a['status'].lower() == 'active']
    active_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.datetime.max)
    featured = active_auctions[:3]
    trending = read_trending()
    # Filter trending for "This Week" by default
    trending_this_week = [t for t in trending if t['time_period'] == 'This Week']
    trending_this_week.sort(key=lambda x: x['trending_rank'])
    return render_template('auction_dashboard.html',
                           featured_auctions=featured,
                           trending_auctions=trending_this_week)
# Route: Auction Catalog page '/catalog'
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    auctions = read_auctions()
    categories = read_categories()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_auctions = auctions
    # Filter by category if selected and valid
    if category_filter and category_filter.lower() != 'all':
        filtered_auctions = [a for a in filtered_auctions if a['category'].lower() == category_filter.lower()]
    # Filter by search query if provided
    if search_query:
        def matches_search(a):
            return (search_query in a['item_name'].lower() or
                    search_query in a['description'].lower() or
                    search_query == a['auction_id'])
        filtered_auctions = [a for a in filtered_auctions if matches_search(a)]
    # Sort auctions by end_time ascending
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.datetime.max)
    return render_template('auction_catalog.html',
                           auctions=filtered_auctions,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
# Route: Auction Details page '/auction/<auction_id>'
@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        flash("Auction not found.", "error")
        return redirect(url_for('catalog'))
    # Read bid history for this auction
    bid_history = read_bid_history()
    auction_bid_history = [b for b in bid_history if b['auction_id'] == auction_id]
    # Sort by bid_timestamp descending (latest first)
    auction_bid_history.sort(key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('auction_details.html',
                           auction=auction,
                           bid_history=auction_bid_history)
# Route: Place Bid page '/place_bid/<auction_id>'
@app.route('/place_bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        flash("Auction not found.", "error")
        return redirect(url_for('catalog'))
    if auction['status'].lower() != 'active':
        flash("Cannot place bid. Auction is not active.", "error")
        return redirect(url_for('auction_details', auction_id=auction_id))
    min_bid = max(auction['current_bid'], auction['starting_bid'])
    if request.method == 'POST':
        bidder_name = request.form.get('bidder-name', '').strip()
        bid_amount_str = request.form.get('bid-amount', '').strip()
        # Validate inputs
        if not bidder_name:
            flash("Bidder name is required.", "error")
            return redirect(request.url)
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            flash("Invalid bid amount.", "error")
            return redirect(request.url)
        if bid_amount <= min_bid:
            flash(f"Bid amount must be greater than current bid ({min_bid:.2f}).", "error")
            return redirect(request.url)
        # Update bids.txt
        bids = read_bids()
        new_bid_id = str(max([int(b['bid_id']) for b in bids], default=0) + 1)
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        new_bid = {
            'bid_id': new_bid_id,
            'auction_id': auction_id,
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': now_str
        }
        bids.append(new_bid)
        write_bids(bids)
        # Update bid_history.txt
        bid_history = read_bid_history()
        new_history_id = str(max([int(h['history_id']) for h in bid_history], default=0) + 1)
        new_history = {
            'history_id': new_history_id,
            'auction_id': auction_id,
            'auction_name': auction['item_name'],
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': now_str
        }
        bid_history.append(new_history)
        write_bid_history(bid_history)
        # Update auctions.txt current_bid
        for a in auctions:
            if a['auction_id'] == auction_id:
                a['current_bid'] = bid_amount
                break
        write_auctions(auctions)
        flash("Bid placed successfully.", "success")
        return redirect(url_for('auction_details', auction_id=auction_id))
    return render_template('place_bid.html',
                           auction=auction,
                           minimum_bid=min_bid)
# Route: Bid History page '/bid_history'
@app.route('/bid_history')
def bid_history():
    bids = read_bids()
    auctions = read_auctions()
    auction_dict = {a['auction_id']: a['item_name'] for a in auctions}
    # Add auction_name to bids for display
    for b in bids:
        b['auction_name'] = auction_dict.get(b['auction_id'], 'Unknown')
    # Filter by auction if requested
    filter_auction = request.args.get('filter_auction', '').strip()
    if filter_auction:
        bids = [b for b in bids if b['auction_id'] == filter_auction]
    # Sort by amount if requested
    sort_by_amount = request.args.get('sort', '').lower()
    if sort_by_amount == 'amount':
        bids.sort(key=lambda x: x['bid_amount'], reverse=True)
    else:
        # Default sort by bid_timestamp descending
        bids.sort(key=lambda x: x['bid_timestamp'], reverse=True)
    # Prepare auction options for filter dropdown
    auction_options = sorted(auctions, key=lambda x: x['item_name'])
    return render_template('bid_history.html',
                           bids=bids,
                           auction_options=auction_options,
                           selected_auction=filter_auction)
# Route: Auction Categories page '/categories'
@app.route('/categories')
def categories():
    categories = read_categories()
    auctions = read_auctions()
    # Calculate item counts per category dynamically (to keep consistent)
    category_counts = {}
    for c in categories:
        category_counts[c['category_name']] = 0
    for a in auctions:
        cat = a['category']
        if cat in category_counts:
            category_counts[cat] += 1
    # Update categories with current counts
    for c in categories:
        c['item_count'] = category_counts.get(c['category_name'], 0)
    return render_template('categories.html',
                           categories=categories)
# Route: View items in a category '/category/<category_name>'
@app.route('/category/<category_name>')
def view_category(category_name):
    auctions = read_auctions()
    filtered_auctions = [a for a in auctions if a['category'].lower() == category_name.lower()]
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.datetime.max)
    return render_template('auction_catalog.html',
                           auctions=filtered_auctions,
                           categories=read_categories(),
                           selected_category=category_name,
                           search_query='')
# Route: Winners page '/winners'
@app.route('/winners')
def winners():
    winners = read_winners()
    filter_winner = request.args.get('filter_by_winner', '').strip().lower()
    if filter_winner:
        winners = [w for w in winners if filter_winner in w['winner_name'].lower()]
    # Sort winners by win_date descending
    winners.sort(key=lambda x: x['win_date'], reverse=True)
    return render_template('winners.html',
                           winners=winners,
                           filter_winner=filter_winner)
# Route: Trending Auctions page '/trending'
@app.route('/trending')
def trending():
    trending = read_trending()
    time_range = request.args.get('time_range', 'This Week')
    filtered_trending = [t for t in trending if t['time_period'] == time_range]
    filtered_trending.sort(key=lambda x: x['trending_rank'])
    return render_template('trending.html',
                           trending_auctions=filtered_trending,
                           selected_time_range=time_range)
# Route: Auction Status page '/status'
@app.route('/status')
def status():
    auctions = read_auctions()
    status_filter = request.args.get('status', 'All').lower()
    filtered_auctions = auctions
    if status_filter != 'all':
        filtered_auctions = [a for a in auctions if a['status'].lower() == status_filter]
    # Calculate time remaining for each auction
    for a in filtered_auctions:
        a['time_remaining'] = time_remaining(a['end_time'])
    # Sort by end_time ascending
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.datetime.max)
    return render_template('status.html',
                           auctions=filtered_auctions,
                           selected_status=status_filter.capitalize())
# Route: Back to dashboard button handler (redirect)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Error handlers for common HTTP errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
if __name__ == '__main__':
    # Run the Flask app on localhost port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)