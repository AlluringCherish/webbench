from flask import Flask, render_template, request
import os
app = Flask(__name__)
DATA_DIR = 'data'  # Adjust this path as needed
def read_trending():
    """
    Reads the trending.txt file and returns a list of trending auction dicts.
    Format per line: auction_id|item_name|bid_count|current_bid|trending_rank|time_period
    """
    trending_path = os.path.join(DATA_DIR, 'trending.txt')
    trending_auctions = []
    if not os.path.exists(trending_path):
        return trending_auctions
    with open(trending_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue  # skip malformed lines
            try:
                auction = {
                    'auction_id': parts[0],
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                }
                trending_auctions.append(auction)
            except ValueError:
                # Skip lines with invalid numeric values
                continue
    return trending_auctions
@app.route('/trending')
def trending():
    """
    Route to display trending auctions.
    Supports optional filtering by time_period via query parameter 'time_range'.
    """
    trending_auctions = read_trending()
    # Optional filter by time_period (e.g., 'week', 'month', etc.)
    time_range = request.args.get('time_range', '').strip().lower()
    if time_range:
        trending_auctions = [a for a in trending_auctions if a['time_period'].lower() == time_range]
    # Sort by trending_rank ascending (1 is highest rank)
    trending_auctions.sort(key=lambda a: a['trending_rank'])
    return render_template('trending.html', trending_auctions=trending_auctions, selected_time_range=time_range)
if __name__ == '__main__':
    app.run(debug=True)