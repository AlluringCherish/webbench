# OnlineAuction Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                  | Function Name           | HTTP Method | Template Rendered           | Context Variables Passed (Type Annotations)                                                                                                     |
|-----------------------------|------------------------|-------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| /                           | root                   | GET         | Redirect to /dashboard       | None                                                                                                                                            |
| /dashboard                  | dashboard_page         | GET         | dashboard.html              | featured_auctions: List[dict {auction_id: int, item_name: str, current_bid: float, image_url: str}]
  trending_auctions: List[dict {auction_id: int, item_name: str, current_bid: float, bid_count: int}]
|
| /catalog                   | auction_catalog        | GET         | catalog.html                | auctions: List[dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, time_remaining: str, image_url: str}]
  categories: List[str]
  search_query: str (optional)
  selected_category: str (optional)
|
| /catalog/search            | auction_catalog_search | POST        | catalog.html                | auctions: List[dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, time_remaining: str, image_url: str}]
  categories: List[str]
  search_query: str
  selected_category: str
|
| /auction/<int:auction_id>  | auction_details        | GET         | auction_details.html        | auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}
  bid_history: List[dict {bidder_name: str, bid_amount: float, bid_timestamp: str}]
|
| /auction/<int:auction_id>/place_bid | place_bid_page   | GET         | place_bid.html              | auction: dict {auction_id: int, item_name: str, minimum_bid: float}
|
| /auction/<int:auction_id>/place_bid | submit_bid       | POST        | place_bid.html (on error, else redirect) | bidder_name: str
  bid_amount: float
  auction: dict {auction_id: int, item_name: str, minimum_bid: float}
  errors: dict (optional)  |
| /bid_history               | bid_history_page       | GET         | bid_history.html            | bids: List[dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}]
  auctions: List[dict {auction_id: int, item_name: str}]
  filter_auction_id: int or None
  sorted_by_amount: bool
|
| /bid_history/filter        | bid_history_filter     | POST        | bid_history.html            | bids: List[dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}]
  auctions: List[dict {auction_id: int, item_name: str}]
  filter_auction_id: int or None
  sorted_by_amount: bool
|
| /categories                | auction_categories     | GET         | categories.html             | categories: List[dict {category_id: int, category_name: str, description: str, item_count: int}]
|
| /categories/<int:category_id> | view_category        | GET         | catalog.html                | auctions: List[dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, time_remaining: str, image_url: str}]
  selected_category: str
|
| /winners                   | winners_page           | GET         | winners.html                | winners: List[dict {auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}]
  filter_winner_name: str (optional)
|
| /winners/filter            | winners_filter         | POST        | winners.html                | winners: List[dict {auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}]
  filter_winner_name: str
|
| /trending                  | trending_auctions      | GET         | trending.html               | trending_auctions: List[dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}]
  selected_time_range: str
|
| /trending/filter           | trending_filter        | POST        | trending.html               | trending_auctions: List[dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}]
  selected_time_range: str
|
| /status                    | auction_status         | GET         | status.html                 | auctions: List[dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}]
  selected_status: str
|
| /status/filter             | auction_status_filter  | POST        | status.html                 | auctions: List[dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}]
  selected_status: str
|

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements:
  - ID: dashboard-page (Div)
  - ID: featured-auctions (Div)
  - ID: browse-auctions-button (Button) - Navigates to auction_catalog
  - ID: view-bids-button (Button) - Navigates to bid_history_page
  - ID: trending-auctions-button (Button) - Navigates to trending_auctions
- Navigation Mappings:
  - #browse-auctions-button -> url_for('auction_catalog')
  - #view-bids-button -> url_for('bid_history_page')
  - #trending-auctions-button -> url_for('trending_auctions')
- Context Variables:
  - featured_auctions: List[dict {auction_id: int, item_name: str, current_bid: float, image_url: str}]
  - trending_auctions: List[dict {auction_id: int, item_name: str, current_bid: float, bid_count: int}]

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: Auction Catalog
- Elements:
  - ID: catalog-page (Div)
  - ID: search-input (Input)
  - ID: category-filter (Dropdown)
  - ID: auctions-grid (Div)
  - ID: view-auction-button-{{ auction.auction_id }} (Button) for each auction
- Navigation Mappings:
  - Buttons with id "view-auction-button-{{ auction.auction_id }}" navigate to url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: List[dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, time_remaining: str, image_url: str}]
  - categories: List[str]
  - search_query: str (optional)
  - selected_category: str (optional)

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Elements:
  - ID: auction-details-page (Div)
  - ID: auction-title (H1)
  - ID: auction-description (Div)
  - ID: current-bid (Div)
  - ID: place-bid-button (Button) - Navigates to place_bid_page for auction
  - ID: bid-history (Div) with bid entries
- Navigation Mappings:
  - #place-bid-button -> url_for('place_bid_page', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}
  - bid_history: List[dict {bidder_name: str, bid_amount: float, bid_timestamp: str}]

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Elements:
  - ID: place-bid-page (Div)
  - ID: bidder-name (Input)
  - ID: bid-amount (Input)
  - ID: auction-name (Div)
  - ID: minimum-bid (Div)
  - ID: submit-bid-button (Button)
- Navigation Mappings:
  - Form POSTs bid submission to url_for('submit_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, minimum_bid: float}
  - bidder_name: str (optional, form input repopulation)
  - bid_amount: str or float (optional, form input repopulation)
  - errors: dict (optional) - keys: bidder_name, bid_amount

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Elements:
  - ID: bid-history-page (Div)
  - ID: bids-table (Table) with columns: bid ID, auction name, bidder, amount, timestamp
  - ID: filter-by-auction (Dropdown)
  - ID: sort-by-amount (Button)
  - ID: back-to-dashboard (Button) - Navigates to dashboard
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - bids: List[dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}]
  - auctions: List[dict {auction_id: int, item_name: str}]
  - filter_auction_id: int or None
  - sorted_by_amount: bool

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Elements:
  - ID: categories-page (Div)
  - ID: categories-list (Div)
  - ID: category-card-{{ category.category_id }} (Div) for each category
  - ID: view-category-button-{{ category.category_id }} (Button) for each category
  - ID: back-to-dashboard (Button) - Navigates to dashboard
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')
  - Buttons with id "view-category-button-{{ category.category_id }}" -> url_for('view_category', category_id=category.category_id)
- Context Variables:
  - categories: List[dict {category_id: int, category_name: str, description: str, item_count: int}]

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Elements:
  - ID: winners-page (Div)
  - ID: winners-list (Div)
  - ID: winner-card-{{ winner.auction_id }} (Div) for each winner
  - ID: filter-by-winner (Input)
  - ID: back-to-dashboard (Button) - Navigates to dashboard
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - winners: List[dict {auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}]
  - filter_winner_name: str (optional)

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: Trending Auctions
- Elements:
  - ID: trending-page (Div)
  - ID: trending-list (Div)
  - ID: time-range-filter (Dropdown)
  - ID: view-auction-button-{{ auction.auction_id }} (Button) for each trending auction
  - ID: back-to-dashboard (Button) - Navigates to dashboard
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')
  - Buttons with id "view-auction-button-{{ auction.auction_id }}" -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - trending_auctions: List[dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}]
  - selected_time_range: str

### 9. Auction Status Page
- Template: templates/status.html
- Page Title: Auction Status
- Elements:
  - ID: status-page (Div)
  - ID: status-filter (Dropdown)
  - ID: status-table (Table) with columns: name, status, time remaining, current bid
  - ID: refresh-status-button (Button)
  - ID: back-to-dashboard (Button) - Navigates to dashboard
- Navigation Mappings:
  - #back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - auctions: List[dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}]
  - selected_status: str

---

## Section 3: Data File Schemas

### 1. Auctions Data
- File path: data/auctions.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str, datetime format "YYYY-MM-DD HH:MM")
  8. status (str) - e.g., Active, Closed
  9. image_url (str)
- Purpose: Stores all auction item details including bids, timing and status.
- Example rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- File path: data/categories.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores auction categories and associated metadata.
- Example rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- File path: data/bids.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str, datetime format "YYYY-MM-DD HH:MM")
- Purpose: Stores individual bid records.
- Example rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- File path: data/winners.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str, date format "YYYY-MM-DD")
- Purpose: Stores auction winners' information.
- Example rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- File path: data/bid_history.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str, datetime format "YYYY-MM-DD HH:MM")
- Purpose: Stores historical bid data for auctions.
- Example rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- File path: data/items.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores detailed item-specific data linked to auctions.
- Example rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- File path: data/trending.txt
- Format: Pipe-delimited (|), no header line
- Fields in order:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores data for ranking trending auctions.
- Example rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

End of design_spec.md
