# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path               | Function Name           | HTTP Method | Template to Render          | Context Variables Passed to Template                                                                            |
|--------------------------|-------------------------|-------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
| /                        | index                   | GET         | Redirect to /dashboard      | None                                                                                                            |
| /dashboard               | dashboard               | GET         | dashboard.html              | featured_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, end_time:str, image_url:str}], trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int, trending_rank:int}], None (buttons navigate)
| /catalog                 | auction_catalog         | GET         | auction_catalog.html        | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}], categories: list[str]  |
| /auction/<int:auction_id>| auction_details         | GET         | auction_details.html        | auction: dict{auction_id:int, item_name:str, description:str, current_bid:float, end_time:str, status:str, image_url:str}, bid_history: list[dict{bidder_name:str, bid_amount:float, bid_timestamp:str}]  |
| /place_bid/<int:auction_id> | place_bid           | GET, POST   | place_bid.html              | auction: dict{auction_id:int, item_name:str, minimum_bid:float}, submission_response:str (on POST)               |
| /bid_history             | bid_history             | GET         | bid_history.html            | bids: list[dict{bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str}], auctions: list[dict{auction_id:int, item_name:str}] |
| /categories              | auction_categories      | GET         | auction_categories.html     | categories: list[dict{category_id:int, category_name:str, description:str, item_count:int}]                      |
| /winners                 | winners                 | GET         | winners.html                | winners: list[dict{auction_id:int, item_name:str, winner_name:str, winning_bid:float}], filtered_by:str           |
| /trending                | trending_auctions       | GET         | trending_auctions.html      | trending_auctions: list[dict{auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str}] |
| /status                  | auction_status          | GET         | auction_status.html         | auctions: list[dict{auction_id:int, item_name:str, status:str, time_remaining:str, current_bid:float}]           |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template Filename: templates/dashboard.html
- Page Title: Auction Dashboard
- <title>: Auction Dashboard
- <h1>: Auction Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-auctions (Div)
  - browse-auctions-button (Button)
  - view-bids-button (Button)
  - trending-auctions-button (Button)
- Navigation:
  - browse-auctions-button navigates to auction_catalog
  - view-bids-button navigates to bid_history
  - trending-auctions-button navigates to trending_auctions
- Context Variables:
  - featured_auctions: list of dict with keys: auction_id, item_name, current_bid, end_time, image_url
  - trending_auctions: list of dict with keys: auction_id, item_name, current_bid, bid_count, trending_rank

### 2. Auction Catalog Page
- Template Filename: templates/auction_catalog.html
- Page Title: Auction Catalog
- <title>: Auction Catalog
- <h1>: Auction Catalog
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} navigates to auction_details with auction_id
- Context Variables:
  - auctions: list of dict with keys: auction_id, item_name, description, category, current_bid, end_time, image_url
  - categories: list of strings for filtering

### 3. Auction Details Page
- Template Filename: templates/auction_details.html
- Page Title: Auction Details
- <title>: Auction Details
- <h1>: Auction Details
- Element IDs:
  - auction-details-page (Div)
  - auction-title (H1)
  - auction-description (Div)
  - current-bid (Div)
  - place-bid-button (Button)
  - bid-history (Div)
- Navigation:
  - place-bid-button navigates to place_bid with auction_id
- Context Variables:
  - auction: dict with keys: auction_id, item_name, description, current_bid, end_time, status, image_url
  - bid_history: list of dict with keys: bidder_name, bid_amount, bid_timestamp

### 4. Place Bid Page
- Template Filename: templates/place_bid.html
- Page Title: Place Bid
- <title>: Place Bid
- <h1>: Place Bid
- Element IDs:
  - place-bid-page (Div)
  - bidder-name (Input)
  - bid-amount (Input)
  - auction-name (Div)
  - minimum-bid (Div)
  - submit-bid-button (Button)
- Navigation:
  - submit-bid-button submits POST to place_bid with auction_id
- Context Variables:
  - auction: dict with keys: auction_id, item_name, minimum_bid
  - submission_response: str (only on POST response)

### 5. Bid History Page
- Template Filename: templates/bid_history.html
- Page Title: Bid History
- <title>: Bid History
- <h1>: Bid History
- Element IDs:
  - bid-history-page (Div)
  - bids-table (Table)
  - filter-by-auction (Dropdown)
  - sort-by-amount (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard navigates to dashboard
- Context Variables:
  - bids: list of dict with keys: bid_id, auction_name, bidder_name, bid_amount, bid_timestamp
  - auctions: list of dict with keys: auction_id, item_name

### 6. Auction Categories Page
- Template Filename: templates/auction_categories.html
- Page Title: Auction Categories
- <title>: Auction Categories
- <h1>: Auction Categories
- Element IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{ category.category_id }} (Div, dynamic per category)
  - view-category-button-{{ category.category_id }} (Button, dynamic per category)
  - back-to-dashboard (Button)
- Navigation:
  - view-category-button-{{ category.category_id }} navigates to auction_catalog filtered by category
  - back-to-dashboard navigates to dashboard
- Context Variables:
  - categories: list of dict with keys: category_id, category_name, description, item_count

### 7. Winners Page
- Template Filename: templates/winners.html
- Page Title: Winning Items
- <title>: Winning Items
- <h1>: Winning Items
- Element IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{ winner.auction_id }} (Div, dynamic per winner)
  - filter-by-winner (Input)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard navigates to dashboard
- Context Variables:
  - winners: list of dict with keys: auction_id, item_name, winner_name, winning_bid

### 8. Trending Auctions Page
- Template Filename: templates/trending_auctions.html
- Page Title: Trending Auctions
- <title>: Trending Auctions
- <h1>: Trending Auctions
- Element IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
  - back-to-dashboard (Button)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} navigates to auction_details with auction_id
  - back-to-dashboard navigates to dashboard
- Context Variables:
  - trending_auctions: list of dict with keys: auction_id, item_name, bid_count, current_bid, trending_rank, time_period

### 9. Auction Status Page
- Template Filename: templates/auction_status.html
- Page Title: Auction Status
- <title>: Auction Status
- <h1>: Auction Status
- Element IDs:
  - status-page (Div)
  - status-filter (Dropdown)
  - status-table (Table)
  - refresh-status-button (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard navigates to dashboard
- Context Variables:
  - auctions: list of dict with keys: auction_id, item_name, status, time_remaining, current_bid

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str, format: YYYY-MM-DD HH:MM)
  8. status (str: Active, Closed, Upcoming)
  9. image_url (str)
- Purpose: Stores details of all auctions including current bids and statuses.
- Example Rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- Path: data/categories.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores category information for filtering and display.
- Example Rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- Path: data/bids.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Records all individual bids placed on auctions.
- Example Rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- Path: data/winners.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str, format: YYYY-MM-DD)
- Purpose: Stores information about auction winners and winning bids.
- Example Rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- Path: data/bid_history.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Logs detailed bid history for auctions.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- Path: data/items.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores item details including conditions and sellers.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- Path: data/trending.txt
- File Format: Pipe-delimited (|), no header line
- Fields Order and Names:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores ranked trending auction data for different time ranges.
- Example Rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

End of Design Specification Document
