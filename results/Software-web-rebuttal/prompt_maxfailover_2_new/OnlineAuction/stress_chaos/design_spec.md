# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name            | HTTP Method | Template to Render             | Context Variables with Type Annotations                                             |
|-------------------------------|--------------------------|-------------|-------------------------------|-------------------------------------------------------------------------------------|
| `/`                           | root_redirect            | GET         | Redirects to dashboard         | None                                                                                |
| `/dashboard`                  | dashboard                | GET         | dashboard.html                | featured_auctions: list[dict{auction_id:int, item_name:str, current_bid:float}], trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int}] |
| `/catalog`                   | auction_catalog          | GET         | catalog.html                  | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}], categories: list[str]                      |
| `/auction/<int:auction_id>`  | auction_details          | GET         | auction_details.html          | auction: dict{auction_id:int, item_name:str, description:str, current_bid:float, end_time:str, status:str}, bids: list[dict{bidder_name:str, bid_amount:float}]               |
| `/auction/<int:auction_id>/bid` | place_bid               | GET         | place_bid.html                | auction: dict{auction_id:int, item_name:str, current_bid:float, minimum_bid:float}                                            |
| `/auction/<int:auction_id>/bid` | submit_bid              | POST        | place_bid.html (or redirect) | auction_id: int, bidder_name: str, bid_amount: float (form input)                                                   |
| `/bidhistory`                | bid_history              | GET         | bid_history.html              | bids: list[dict{bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str}], auctions: list[dict{auction_id:int, item_name:str}]                       |
| `/categories`               | auction_categories       | GET         | categories.html               | categories: list[dict{category_id:int, category_name:str, description:str, item_count:int}]                                  |
| `/winners`                  | winners                  | GET         | winners.html                  | winners: list[dict{auction_id:int, item_name:str, winner_name:str, winning_bid:float}]                                    |
| `/trending`                 | trending_auctions        | GET         | trending.html                 | trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int, trending_rank:int, time_period:str}] |
| `/status`                   | auction_status           | GET         | status.html                   | auctions: list[dict{auction_id:int, item_name:str, status:str, time_remaining:str, current_bid:float}]                       |


Notes:
- `root_redirect` redirects from `/` to `/dashboard`.
- `submit_bid` POST route handles bid submission for the given auction.
- In listing routes, ids or references are included for unique identification.

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: `templates/dashboard.html`
- Page Title: "Auction Dashboard"
- Main Header `<h1>`: "Auction Dashboard"
- Element IDs:
  - `dashboard-page` (Div)
  - `featured-auctions` (Div)
  - `browse-auctions-button` (Button)
  - `view-bids-button` (Button)
  - `trending-auctions-button` (Button)
- Navigation:
  - `browse-auctions-button` → `auction_catalog` route
  - `view-bids-button` → `bid_history` route
  - `trending-auctions-button` → `trending_auctions` route
- Context Variables:
  - `featured_auctions`: list of dict with keys `auction_id` (int), `item_name` (str), `current_bid` (float)
  - `trending_auctions`: list of dict with keys `auction_id` (int), `item_name` (str), `current_bid` (float), `bid_count` (int)

### 2. Auction Catalog Page
- Template: `templates/catalog.html`
- Page Title: "Auction Catalog"
- Main Header `<h1>`: "Auction Catalog"
- Element IDs:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `category-filter` (Dropdown)
  - `auctions-grid` (Div)
  - `view-auction-button-{{ auction.auction_id }}` (Button) for each auction in `auctions`
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` → `auction_details` route with auction_id
- Context Variables:
  - `auctions`: list of dict with keys `auction_id` (int), `item_name` (str), `description` (str), `category` (str), `current_bid` (float), `end_time` (str), `image_url` (str)
  - `categories`: list of category names (str)

### 3. Auction Details Page
- Template: `templates/auction_details.html`
- Page Title: "Auction Details"
- Main Header `<h1>`: `auction.auction_title` displayed inside element with ID `auction-title`
- Element IDs:
  - `auction-details-page` (Div)
  - `auction-title` (H1)
  - `auction-description` (Div)
  - `current-bid` (Div)
  - `place-bid-button` (Button)
  - `bid-history` (Div)
- Navigation:
  - `place-bid-button` → `place_bid` route with auction_id
- Context Variables:
  - `auction`: dict with keys `auction_id` (int), `item_name` (str), `description` (str), `current_bid` (float), `end_time` (str), `status` (str)
  - `bids`: list of dict with keys `bidder_name` (str), `bid_amount` (float)

### 4. Place Bid Page
- Template: `templates/place_bid.html`
- Page Title: "Place Bid"
- Main Header `<h1>`: "Place Bid"
- Element IDs:
  - `place-bid-page` (Div)
  - `bidder-name` (Input)
  - `bid-amount` (Input)
  - `auction-name` (Div)
  - `minimum-bid` (Div)
  - `submit-bid-button` (Button)
- Navigation:
  - Form submission to `submit_bid` POST route with auction_id
- Context Variables:
  - `auction`: dict with keys `auction_id` (int), `item_name` (str), `current_bid` (float), `minimum_bid` (float)

### 5. Bid History Page
- Template: `templates/bid_history.html`
- Page Title: "Bid History"
- Main Header `<h1>`: "Bid History"
- Element IDs:
  - `bid-history-page` (Div)
  - `bids-table` (Table)
  - `filter-by-auction` (Dropdown)
  - `sort-by-amount` (Button)
  - `back-to-dashboard` (Button)
- Navigation:
  - `back-to-dashboard` → `dashboard` route
- Context Variables:
  - `bids`: list of dict with keys `bid_id` (int), `auction_name` (str), `bidder_name` (str), `bid_amount` (float), `bid_timestamp` (str)
  - `auctions`: list of dict with keys `auction_id` (int), `item_name` (str)

### 6. Auction Categories Page
- Template: `templates/categories.html`
- Page Title: "Auction Categories"
- Main Header `<h1>`: "Auction Categories"
- Element IDs:
  - `categories-page` (Div)
  - `categories-list` (Div)
  - `category-card-{{ category.category_id }}` (Div) for each category
  - `view-category-button-{{ category.category_id }}` (Button) for each category
  - `back-to-dashboard` (Button)
- Navigation:
  - `view-category-button-{{ category.category_id }}` → `auction_catalog` route with category filter
  - `back-to-dashboard` → `dashboard` route
- Context Variables:
  - `categories`: list of dict with keys `category_id` (int), `category_name` (str), `description` (str), `item_count` (int)

### 7. Winners Page
- Template: `templates/winners.html`
- Page Title: "Winning Items"
- Main Header `<h1>`: "Winning Items"
- Element IDs:
  - `winners-page` (Div)
  - `winners-list` (Div)
  - `winner-card-{{ winner.auction_id }}` (Div) for each winner
  - `filter-by-winner` (Input)
  - `back-to-dashboard` (Button)
- Navigation:
  - `back-to-dashboard` → `dashboard` route
- Context Variables:
  - `winners`: list of dict with keys `auction_id` (int), `item_name` (str), `winner_name` (str), `winning_bid` (float)

### 8. Trending Auctions Page
- Template: `templates/trending.html`
- Page Title: "Trending Auctions"
- Main Header `<h1>`: "Trending Auctions"
- Element IDs:
  - `trending-page` (Div)
  - `trending-list` (Div)
  - `time-range-filter` (Dropdown)
  - `view-auction-button-{{ auction.auction_id }}` (Button) for each trending auction
  - `back-to-dashboard` (Button)
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` → `auction_details` route with auction_id
  - `back-to-dashboard` → `dashboard` route
- Context Variables:
  - `trending_auctions`: list of dict with keys `auction_id` (int), `item_name` (str), `current_bid` (float), `bid_count` (int), `trending_rank` (int), `time_period` (str)

### 9. Auction Status Page
- Template: `templates/status.html`
- Page Title: "Auction Status"
- Main Header `<h1>`: "Auction Status"
- Element IDs:
  - `status-page` (Div)
  - `status-filter` (Dropdown)
  - `status-table` (Table)
  - `refresh-status-button` (Button)
  - `back-to-dashboard` (Button)
- Navigation:
  - `back-to-dashboard` → `dashboard` route
- Context Variables:
  - `auctions`: list of dict with keys `auction_id` (int), `item_name` (str), `status` (str), `time_remaining` (str), `current_bid` (float)

---

## Section 3: Data File Schemas (Backend)

### 1. auctions.txt
- Path: `data/auctions.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `auction_id` (int)
  2. `item_name` (str)
  3. `description` (str)
  4. `category` (str)
  5. `starting_bid` (float)
  6. `current_bid` (float)
  7. `end_time` (str, datetime format `YYYY-MM-DD HH:MM`)
  8. `status` (str) - values such as "Active", "Closed", "Upcoming"
  9. `image_url` (str)
- Purpose: Stores details of auction items including current bids and status.
- Example Rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. categories.txt
- Path: `data/categories.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
  4. `item_count` (int)
- Purpose: Stores all auction categories and their metadata.
- Example Rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. bids.txt
- Path: `data/bids.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `bid_id` (int)
  2. `auction_id` (int)
  3. `bidder_name` (str)
  4. `bid_amount` (float)
  5. `bid_timestamp` (str, datetime format `YYYY-MM-DD HH:MM`)
- Purpose: Stores all bids placed on auctions.
- Example Rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. winners.txt
- Path: `data/winners.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `winner_id` (int)
  2. `auction_id` (int)
  3. `item_name` (str)
  4. `winner_name` (str)
  5. `winning_bid` (float)
  6. `win_date` (str, date format `YYYY-MM-DD`)
- Purpose: Stores finalized auction winners and winning details.
- Example Rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. bid_history.txt
- Path: `data/bid_history.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `history_id` (int)
  2. `auction_id` (int)
  3. `auction_name` (str)
  4. `bidder_name` (str)
  5. `bid_amount` (float)
  6. `bid_timestamp` (str, datetime format `YYYY-MM-DD HH:MM`)
- Purpose: Logs all bid activities historically.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. items.txt
- Path: `data/items.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `item_id` (int)
  2. `auction_id` (int)
  3. `item_name` (str)
  4. `starting_price` (float)
  5. `category` (str)
  6. `condition` (str)
  7. `seller_name` (str)
- Purpose: Stores item metadata linked to auctions.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. trending.txt
- Path: `data/trending.txt`
- Format: Pipe-delimited (`|`), no header line
- Fields in order:
  1. `auction_id` (int)
  2. `item_name` (str)
  3. `bid_count` (int)
  4. `current_bid` (float)
  5. `trending_rank` (int)
  6. `time_period` (str)
- Purpose: Stores trending auctions ranked by bid activity over time periods.
- Example Rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

End of Design Specification
