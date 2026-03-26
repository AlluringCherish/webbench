'''
Main backend Python application file for OnlineAuction web application.
Implements the web server, routing, and business logic.
Handles reading and writing to local text files in the data/ directory,
processes user requests, and renders HTML templates with data.
No authentication required; all features directly accessible.
Website accessible via local port 5000, starting at route '/' (Dashboard).
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime, timedelta
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read and write data files
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
# Helper to parse datetime string
def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
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
    now = datetime.now()
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
    trending = read_trending()
    # Featured auctions: pick top 3 active auctions with highest current_bid
    active_auctions = [a for a in auctions if a['status'].lower() == 'active']
    featured_auctions = sorted(active_auctions, key=lambda x: x['current_bid'], reverse=True)[:3]
    # Add time remaining to featured auctions
    for a in featured_auctions:
        a['time_remaining'] = time_remaining(a['end_time'])
    # Trending auctions filtered by "This Week" (default)
    trending_this_week = [t for t in trending if t['time_period'] == 'This Week']
    trending_this_week_sorted = sorted(trending_this_week, key=lambda x: x['trending_rank'])
    return render_template('dashboard.html',
                           featured_auctions=featured_auctions,
                           trending_auctions=trending_this_week_sorted)
# Route: Auction Catalog page '/catalog'
@app.route('/catalog')
def auction_catalog():
    auctions = read_auctions()
    categories = read_categories()
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    filtered_auctions = auctions
    # Filter by category if selected and valid
    if category_filter and category_filter.lower() != 'all':
        filtered_auctions = [a for a in filtered_auctions if a['category'].lower() == category_filter.lower()]
    # Filter by search query in item_name, description, or auction_id
    if search_query:
        filtered_auctions = [a for a in filtered_auctions if
                             search_query in a['item_name'].lower() or
                             search_query in a['description'].lower() or
                             search_query == a['auction_id']]
    # Add time remaining to each auction
    for a in filtered_auctions:
        a['time_remaining'] = time_remaining(a['end_time'])
    # Sort auctions by end_time ascending (soonest ending first)
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.max)
    return render_template('auction_catalog.html',
                           auctions=filtered_auctions,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
# Route: Auction Details page '/auction/<auction_id>'
@app.route('/auction/<auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    bid_history = read_bid_history()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    # Get bid history for this auction sorted by timestamp descending
    auction_bid_history = [b for b in bid_history if b['auction_id'] == auction_id]
    auction_bid_history.sort(key=lambda x: parse_datetime(x['bid_timestamp']) or datetime.min, reverse=True)
    # Add time remaining
    auction['time_remaining'] = time_remaining(auction['end_time'])
    return render_template('auction_details.html',
                           auction=auction,
                           bid_history=auction_bid_history)
# Route: Place Bid page '/place_bid/<auction_id>', GET and POST
@app.route('/place_bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    bid_history = read_bid_history()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    # Calculate minimum acceptable bid: current_bid + 0.01 or starting_bid if no bids
    min_bid = auction['current_bid'] if auction['current_bid'] > 0 else auction['starting_bid']
    min_bid = round(min_bid + 0.01, 2)
    if request.method == 'POST':
        bidder_name = request.form.get('bidder-name', '').strip()
        bid_amount_str = request.form.get('bid-amount', '').strip()
        # Validate inputs
        if not bidder_name:
            error = "Bidder name is required."
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=error)
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            error = "Invalid bid amount."
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=error)
        if bid_amount < min_bid:
            error = f"Bid amount must be at least {min_bid:.2f}."
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=error)
        # Check auction status and end time
        if auction['status'].lower() != 'active':
            error = "Cannot place bid. Auction is not active."
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=error)
        end_time_dt = parse_datetime(auction['end_time'])
        if end_time_dt and datetime.now() > end_time_dt:
            error = "Cannot place bid. Auction has ended."
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=error)
        # Generate new bid_id
        new_bid_id = 1
        if bids:
            new_bid_id = max(int(b['bid_id']) for b in bids) + 1
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        # Append new bid to bids.txt
        new_bid = {
            'bid_id': str(new_bid_id),
            'auction_id': auction_id,
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': now_str
        }
        bids.append(new_bid)
        write_bids(bids)
        # Append to bid_history.txt
        new_history_id = 1
        if bid_history:
            new_history_id = max(int(h['history_id']) for h in bid_history) + 1
        new_history = {
            'history_id': str(new_history_id),
            'auction_id': auction_id,
            'auction_name': auction['item_name'],
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': now_str
        }
        bid_history.append(new_history)
        write_bid_history(bid_history)
        # Update current_bid in auctions.txt if bid_amount is higher
        if bid_amount > auction['current_bid']:
            auction['current_bid'] = bid_amount
            # Update auctions list and write back
            for i, a in enumerate(auctions):
                if a['auction_id'] == auction_id:
                    auctions[i] = auction
                    break
            write_auctions(auctions)
        # Redirect to auction details page after successful bid
        return redirect(url_for('auction_details', auction_id=auction_id))
    # GET request: render place bid page
    return render_template('place_bid.html', auction=auction, minimum_bid=min_bid, error=None)
# Route: Bid History page '/bid_history'
@app.route('/bid_history')
def bid_history_page():
    bid_history = read_bid_history()
    auctions = read_auctions()
    # Get filter and sort parameters
    filter_auction = request.args.get('filter_by_auction', '').strip()
    sort_by_amount = request.args.get('sort_by_amount', '').lower() == 'true'
    filtered_history = bid_history
    # Filter by auction if specified
    if filter_auction:
        filtered_history = [h for h in filtered_history if h['auction_id'] == filter_auction]
    # Sort by amount if requested (descending)
    if sort_by_amount:
        filtered_history.sort(key=lambda x: x['bid_amount'], reverse=True)
    else:
        # Default sort by timestamp descending
        filtered_history.sort(key=lambda x: parse_datetime(x['bid_timestamp']) or datetime.min, reverse=True)
    # Prepare auction options for filter dropdown
    auction_options = [(a['auction_id'], a['item_name']) for a in auctions]
    return render_template('bid_history.html',
                           bid_history=filtered_history,
                           auction_options=auction_options,
                           selected_auction=filter_auction,
                           sort_by_amount=sort_by_amount)
# Route: Auction Categories page '/categories'
@app.route('/categories')
def auction_categories():
    categories = read_categories()
    auctions = read_auctions()
    # Update item_count for each category by counting auctions in that category
    category_counts = {}
    for c in categories:
        category_counts[c['category_name']] = 0
    for a in auctions:
        cat = a['category']
        if cat in category_counts:
            category_counts[cat] += 1
        else:
            category_counts[cat] = 1
    for c in categories:
        c['item_count'] = category_counts.get(c['category_name'], 0)
    return render_template('auction_categories.html', categories=categories)
# Route: View items in a category '/category/<category_id>'
@app.route('/category/<category_id>')
def view_category(category_id):
    categories = read_categories()
    auctions = read_auctions()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404
    # Filter auctions by category name
    filtered_auctions = [a for a in auctions if a['category'].lower() == category['category_name'].lower()]
    # Add time remaining
    for a in filtered_auctions:
        a['time_remaining'] = time_remaining(a['end_time'])
    # Sort by end_time ascending
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.max)
    return render_template('auction_catalog.html',
                           auctions=filtered_auctions,
                           categories=categories,
                           selected_category=category['category_name'],
                           search_query='')
# Route: Winners page '/winners'
@app.route('/winners')
def winners():
    winners = read_winners()
    # Filter by winner name if provided
    filter_winner = request.args.get('filter_by_winner', '').strip().lower()
    filtered_winners = winners
    if filter_winner:
        filtered_winners = [w for w in winners if filter_winner in w['winner_name'].lower()]
    # Sort by win_date descending
    filtered_winners.sort(key=lambda x: x['win_date'], reverse=True)
    return render_template('winners.html',
                           winners=filtered_winners,
                           filter_winner=filter_winner)
# Route: Trending Auctions page '/trending'
@app.route('/trending')
def trending_auctions():
    trending = read_trending()
    auctions = read_auctions()
    # Get time range filter
    time_range = request.args.get('time_range', 'This Week')
    valid_ranges = ['Last 24 Hours', 'This Week', 'All Time']
    if time_range not in valid_ranges:
        time_range = 'This Week'
    filtered_trending = [t for t in trending if t['time_period'] == time_range]
    # Sort by trending_rank ascending
    filtered_trending.sort(key=lambda x: x['trending_rank'])
    return render_template('trending_auctions.html',
                           trending_list=filtered_trending,
                           time_range=time_range,
                           valid_ranges=valid_ranges)
# Route: Auction Status page '/status'
@app.route('/status')
def auction_status():
    auctions = read_auctions()
    # Get status filter
    status_filter = request.args.get('status', 'All').lower()
    valid_statuses = ['all', 'active', 'closed', 'upcoming']
    if status_filter not in valid_statuses:
        status_filter = 'all'
    now = datetime.now()
    # Filter auctions by status
    filtered_auctions = []
    for a in auctions:
        a_status = a['status'].lower()
        # Determine upcoming by comparing end_time and current time
        end_time_dt = parse_datetime(a['end_time'])
        if a_status == 'active' and end_time_dt and end_time_dt < now:
            # Auction ended but status not updated, treat as closed
            a_status = 'closed'
        if status_filter == 'all' or a_status == status_filter:
            # Calculate time remaining or time until start (if upcoming)
            if a_status == 'active':
                a['time_remaining'] = time_remaining(a['end_time'])
            elif a_status == 'upcoming':
                # No start_time given, so treat time_remaining as unknown
                a['time_remaining'] = "Unknown"
            else:
                a['time_remaining'] = "Ended"
            filtered_auctions.append(a)
    # Sort by end_time ascending
    filtered_auctions.sort(key=lambda x: parse_datetime(x['end_time']) or datetime.max)
    return render_template('auction_status.html',
                           auctions=filtered_auctions,
                           status_filter=status_filter.capitalize(),
                           valid_statuses=[s.capitalize() for s in valid_statuses])
# Route: Back to dashboard button handler (redirect)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(port=5000, debug=True)