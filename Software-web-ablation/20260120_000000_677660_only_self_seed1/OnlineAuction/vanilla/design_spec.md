# OnlineAuction Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                          | Function Name            | HTTP Method | Template Rendered           | Context Variables Passed to Template                                      |
|-----------------------------------|--------------------------|-------------|-----------------------------|--------------------------------------------------------------------------|
| /                                 | root_redirect            | GET         | Redirect to /dashboard       | None                                                                     |
| /dashboard                        | dashboard_page           | GET         | dashboard.html              | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, status: str, image_url: str}, trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int, time_period: str} |
| /catalog                         | auction_catalog          | GET         | catalog.html                | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str}, categories: list of dict {category_id: int, category_name: str} |
| /auction/<int:auction_id>         | auction_details          | GET         | auction_details.html        | auction: dict {auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str}, bid_history: list of dict {bid_id: int, auction_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str} |
| /place_bid/<int:auction_id>       | place_bid                | GET, POST  | place_bid.html (GET), redirects on POST | auction: dict {auction_id: int, item_name: str, starting_bid: float, current_bid: float}, on GET. Form data on POST handled internally|
| /bid_history                     | bid_history_page         | GET         | bid_history.html            | bids: list of dict {bid_id: int, auction_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}, auctions: list of dict {auction_id: int, item_name: str} |
| /categories                     | auction_categories       | GET         | categories.html             | categories: list of dict {category_id: int, category_name: str, description: str, item_count: int} |
| /winners                       | winners_page             | GET         | winners.html                | winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str} |
| /trending                      | trending_auctions        | GET         | trending.html               | trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str} |
| /status                        | auction_status           | GET         | status.html                 | auctions: list of dict {auction_id: int, item_name: str, status: str, end_time: str, current_bid: float} |


---

## Section 2: HTML Templates Specification (Frontend)

### 1. dashboard.html (templates/dashboard.html)
- Page Title: Auction Dashboard
- Page Header (<h1>): Auction Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-auctions (Div)
  - browse-auctions-button (Button)
  - view-bids-button (Button)
  - trending-auctions-button (Button)
- Navigation:
  - browse-auctions-button -> url_for('auction_catalog')
  - view-bids-button -> url_for('bid_history_page')
  - trending-auctions-button -> url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, status: str, image_url: str}
  - trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int, time_period: str}

### 2. catalog.html (templates/catalog.html)
- Page Title: Auction Catalog
- Page Header (<h1>): Auction Catalog
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str}
  - categories: list of dict {category_id: int, category_name: str}

### 3. auction_details.html (templates/auction_details.html)
- Page Title: Auction Details
- Page Header (<h1>): Auction Details
- Element IDs:
  - auction-details-page (Div)
  - auction-title (H1)
  - auction-description (Div)
  - current-bid (Div)
  - place-bid-button (Button)
  - bid-history (Div)
- Navigation:
  - place-bid-button -> url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str}
  - bid_history: list of dict {bid_id: int, auction_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str}

### 4. place_bid.html (templates/place_bid.html)
- Page Title: Place Bid
- Page Header (<h1>): Place Bid
- Element IDs:
  - place-bid-page (Div)
  - bidder-name (Input)
  - bid-amount (Input)
  - auction-name (Div)
  - minimum-bid (Div)
  - submit-bid-button (Button)
- Navigation:
  - submit-bid-button -> form POST to url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, starting_bid: float, current_bid: float}

### 5. bid_history.html (templates/bid_history.html)
- Page Title: Bid History
- Page Header (<h1>): Bid History
- Element IDs:
  - bid-history-page (Div)
  - bids-table (Table)
  - filter-by-auction (Dropdown)
  - sort-by-amount (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - bids: list of dict {bid_id: int, auction_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
  - auctions: list of dict {auction_id: int, item_name: str}

### 6. categories.html (templates/categories.html)
- Page Title: Auction Categories
- Page Header (<h1>): Auction Categories
- Element IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{ category.category_id }} (Div, dynamic per category)
  - view-category-button-{{ category.category_id }} (Button, dynamic per category)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
  - view-category-button-{{ category.category_id }} -> url_for('auction_catalog') with filter parameters handled
- Context Variables:
  - categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}

### 7. winners.html (templates/winners.html)
- Page Title: Winning Items
- Page Header (<h1>): Winning Items
- Element IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{ winner.auction_id }} (Div, dynamic per winner)
  - filter-by-winner (Input)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}

### 8. trending.html (templates/trending.html)
- Page Title: Trending Auctions
- Page Header (<h1>): Trending Auctions
- Element IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
  - view-auction-button-{{ auction.auction_id }} -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

### 9. status.html (templates/status.html)
- Page Title: Auction Status
- Page Header (<h1>): Auction Status
- Element IDs:
  - status-page (Div)
  - status-filter (Dropdown)
  - status-table (Table)
  - refresh-status-button (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, status: str, end_time: str, current_bid: float}

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order): 
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str, format: YYYY-MM-DD HH:MM)
  8. status (str, e.g., Active, Closed)
  9. image_url (str)
- Purpose: Stores all auction items and their details including current status and bid information.
- Example Rows:
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 2. Categories Data
- Path: data/categories.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores categories metadata including their descriptions and number of items.
- Example Rows:
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 3. Bids Data
- Path: data/bids.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Stores all bids placed on auctions with timestamps.
- Example Rows:
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4. Winners Data
- Path: data/winners.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str, format: YYYY-MM-DD)
- Purpose: Stores winning auction items and corresponding winner information.
- Example Rows:
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 5. Bid History Data
- Path: data/bid_history.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Stores detailed history of all bids on auctions.
- Example Rows:
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 6. Items Data
- Path: data/items.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores items details linked to auctions.
- Example Rows:
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 7. Trending Data
- Path: data/trending.txt
- File Format: Pipe-delimited (|), no header
- Fields (in order):
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores trending auction rankings.
- Example Rows:
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```
