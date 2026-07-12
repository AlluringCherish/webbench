# OnlineAuction Application Design Specification

---

## Section 1: Flask Backend Routes Specification

| Route Path                 | Function Name          | HTTP Method | Template              | Context Variables                                                                                          |
|----------------------------|------------------------|-------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| /                          | root_redirect          | GET         | None (redirect)       | None                                                                                                       |
| /dashboard                 | dashboard              | GET         | dashboard.html        | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str}, trending_auctions: list of dict {auction_id:int, item_name:str, current_bid:float, bid_count:int, trending_rank:int}, categories: list of dict {category_id: int, category_name: str, description:str, item_count:int}           |
| /catalog                   | auction_catalog        | GET         | auction_catalog.html  | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}, categories: list of dict {category_id:int, category_name:str}                                                              |
| /auction/<int:auction_id>  | auction_details        | GET         | auction_details.html  | auction: dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str}, bid_history: list of dict {bid_id:int, bidder_name:str, bid_amount:float, bid_timestamp:str}                                                                |
| /place_bid/<int:auction_id>| place_bid              | GET         | place_bid.html        | auction: dict {auction_id: int, item_name: str, current_bid: float}                                                                                                |
| /place_bid/<int:auction_id>| submit_bid             | POST        | place_bid.html (POST) | error_message: str (optional) if bid invalid, auction as above                                                                                          |
| /bid_history               | bid_history            | GET         | bid_history.html      | bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}, auctions: list of dict {auction_id:int, item_name:str}                                               |
| /categories                | auction_categories     | GET         | auction_categories.html | categories: list of dict {category_id:int, category_name:str, description:str, item_count:int}                                                               |
| /categories/<int:category_id> | view_category       | GET         | auction_catalog.html  | auctions: list of dict filtered by category (fields as auction_catalog), category_name: str                                                                    |
| /winners                   | winners                | GET         | winners.html          | winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}                                    |
| /trending                  | trending_auctions      | GET         | trending_auctions.html | trending_auctions: list of dict {auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str}                        |
| /auction_status            | auction_status         | GET         | auction_status.html   | auctions: list of dict {auction_id:int, item_name:str, status:str, end_time:str, current_bid:float}                                                           |

---

## Section 2: Frontend HTML Templates Specification

### 1. Dashboard Page
- Template: templates/dashboard.html
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
  - browse-auctions-button -> auction_catalog (GET)
  - view-bids-button -> bid_history (GET)
  - trending-auctions-button -> trending_auctions (GET)
- Context Variables:
  - featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str}
  - trending_auctions: list of dict {auction_id:int, item_name:str, current_bid:float, bid_count:int, trending_rank:int}
  - categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}

### 2. Auction Catalog Page
- Template: templates/auction_catalog.html
- Page Title: Auction Catalog
- <title>: Auction Catalog
- <h1>: Auction Catalog
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{ auction.auction_id }} (Button) for each auction card
- Navigation:
  - view-auction-button-{{ auction.auction_id }} -> auction_details(auction_id)
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}
  - categories: list of dict {category_id: int, category_name: str}

### 3. Auction Details Page
- Template: templates/auction_details.html
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
  - place-bid-button -> place_bid(auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str}
  - bid_history: list of dict {bid_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str}

### 4. Place Bid Page
- Template: templates/place_bid.html
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
  - submit-bid-button -> POST submit_bid(auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, current_bid: float}
  - error_message: str (optional, only if bid invalid)

### 5. Bid History Page
- Template: templates/bid_history.html
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
  - back-to-dashboard -> dashboard (GET)
- Context Variables:
  - bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
  - auctions: list of dict {auction_id: int, item_name: str}

### 6. Auction Categories Page
- Template: templates/auction_categories.html
- Page Title: Auction Categories
- <title>: Auction Categories
- <h1>: Auction Categories
- Element IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{ category.category_id }} (Div) for each category
  - view-category-button-{{ category.category_id }} (Button) for each category
  - back-to-dashboard (Button)
- Navigation:
  - view-category-button-{{ category.category_id }} -> view_category(category_id)
  - back-to-dashboard -> dashboard (GET)
- Context Variables:
  - categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- <title>: Winning Items
- <h1>: Winning Items
- Element IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{ winner.auction_id }} (Div) for each winner
  - filter-by-winner (Input)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> dashboard (GET)
- Context Variables:
  - winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}

### 8. Trending Auctions Page
- Template: templates/trending_auctions.html
- Page Title: Trending Auctions
- <title>: Trending Auctions
- <h1>: Trending Auctions
- Element IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{ auction.auction_id }} (Button) for each trending auction
  - back-to-dashboard (Button)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} -> auction_details(auction_id)
  - back-to-dashboard -> dashboard (GET)
- Context Variables:
  - trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

### 9. Auction Status Page
- Template: templates/auction_status.html
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
  - back-to-dashboard -> dashboard (GET)
- Context Variables:
  - auctions: list of dict {auction_id:int, item_name:str, status:str, end_time:str, current_bid:float}

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str) - format: YYYY-MM-DD HH:MM
  8. status (str) - e.g., Active, Closed
  9. image_url (str)
- Purpose: To store all auction items including details, current bid, status, and images.
- Example rows:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. Categories Data
- Path: data/categories.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: To store auction categories with descriptions and counts.
- Example rows:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

### 3. Bids Data
- Path: data/bids.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str) - format: YYYY-MM-DD HH:MM
- Purpose: To store individual bids per auction.
- Example rows:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. Winners Data
- Path: data/winners.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str) - format: YYYY-MM-DD
- Purpose: To store information about winning auctions and winners.
- Example rows:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. Bid History Data
- Path: data/bid_history.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str) - format: YYYY-MM-DD HH:MM
- Purpose: To store full history of bids with auction names.
- Example rows:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. Items Data
- Path: data/items.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: To store item details related to auctions.
- Example rows:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. Trending Data
- Path: data/trending.txt
- File format: pipe-delimited (|), no header line
- Fields (in order):
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: To store rankings and metrics for trending auctions.
- Example rows:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week
