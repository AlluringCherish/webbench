# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name            | HTTP Method | Template to Render             | Context Variables with Types                                                                                                                             |
|-------------------------------|--------------------------|-------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                           | root_redirect             | GET         | None (Redirect to dashboard)  | None                                                                                                                                                    |
| `/dashboard`                  | dashboard_page           | GET         | dashboard.html                | featured_auctions: list[dict{auction_id:int, item_name:str, current_bid:float}], trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int}] |
| `/catalog`                   | auction_catalog_page     | GET         | catalog.html                  | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}]                      |
| `/auction/<int:auction_id>`  | auction_details_page     | GET         | auction_details.html          | auction: dict{auction_id:int, item_name:str, description:str, current_bid:float, end_time:str, status:str}, bid_history: list[dict{bidder_name:str, bid_amount:float, bid_timestamp:str}]  |
| `/auction/<int:auction_id>/place_bid` | place_bid_page            | GET         | place_bid.html                | auction: dict{auction_id:int, item_name:str, current_bid:float, minimum_bid:float}                                                                       |
| `/auction/<int:auction_id>/place_bid` | submit_bid                | POST        | place_bid.html (on validation error or success message) | auction: dict{auction_id:int, item_name:str, current_bid:float, minimum_bid:float}, error_message: str(optional), success_message: str(optional)              |
| `/bids`                      | bid_history_page         | GET         | bid_history.html              | bids: list[dict{bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str}], auctions: list[dict{auction_id:int, item_name:str}] (for dropdown filter)                       |
| `/categories`                | auction_categories_page  | GET         | categories.html               | categories: list[dict{category_id:int, category_name:str, description:str, item_count:int}]                                                             |
| `/categories/<int:category_id>` | view_category_items       | GET         | catalog.html (filtered)       | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}]                      |
| `/winners`                  | winners_page             | GET         | winners.html                 | winners: list[dict{auction_id:int, item_name:str, winner_name:str, winning_bid:float}]                                                                  |
| `/trending`                 | trending_auctions_page   | GET         | trending.html                | trending_auctions: list[dict{auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str}]                     |
| `/status`                   | auction_status_page      | GET         | status.html                  | auctions: list[dict{auction_id:int, item_name:str, status:str, end_time:str, current_bid:float, time_remaining:str}]                                    |


---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template Filename & Path: `templates/dashboard.html`
- Page Title (& `<h1>`): "Auction Dashboard"
- Element IDs and Types:
  - `dashboard-page`: Div
  - `featured-auctions`: Div
  - `browse-auctions-button`: Button (navigates to auction_catalog_page)
  - `view-bids-button`: Button (navigates to bid_history_page)
  - `trending-auctions-button`: Button (navigates to trending_auctions_page)
- Navigation:
  - `browse-auctions-button` uses `url_for('auction_catalog_page')`
  - `view-bids-button` uses `url_for('bid_history_page')`
  - `trending-auctions-button` uses `url_for('trending_auctions_page')`
- Context variables:
  - `featured_auctions`: list of dicts with keys: `auction_id`(int), `item_name`(str), `current_bid`(float)
  - `trending_auctions`: list of dicts with keys: `auction_id`(int), `item_name`(str), `current_bid`(float), `bid_count`(int)

### 2. Auction Catalog Page
- Template Filename & Path: `templates/catalog.html`
- Page Title & `<h1>`: "Auction Catalog"
- Element IDs and Types:
  - `catalog-page`: Div
  - `search-input`: Input
  - `category-filter`: Dropdown
  - `auctions-grid`: Div
  - `view-auction-button-{{ auction.auction_id }}`: Button (in each auction card, dynamic)
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` links to `url_for('auction_details_page', auction_id=auction.auction_id)`
- Context variables:
  - `auctions`: list of dicts with keys: `auction_id`(int), `item_name`(str), `description`(str), `category`(str), `current_bid`(float), `end_time`(str), `image_url`(str)

### 3. Auction Details Page
- Template Filename & Path: `templates/auction_details.html`
- Page Title & `<h1>`: "Auction Details"
- Element IDs and Types:
  - `auction-details-page`: Div
  - `auction-title`: H1
  - `auction-description`: Div
  - `current-bid`: Div
  - `place-bid-button`: Button (navigates to place_bid_page for this auction)
  - `bid-history`: Div (displays list of bids)
- Navigation:
  - `place-bid-button` uses `url_for('place_bid_page', auction_id=auction.auction_id)`
- Context variables:
  - `auction`: dict with keys: `auction_id`(int), `item_name`(str), `description`(str), `current_bid`(float), `end_time`(str), `status`(str)
  - `bid_history`: list of dicts with keys: `bidder_name`(str), `bid_amount`(float), `bid_timestamp`(str)

### 4. Place Bid Page
- Template Filename & Path: `templates/place_bid.html`
- Page Title & `<h1>`: "Place Bid"
- Element IDs and Types:
  - `place-bid-page`: Div
  - `bidder-name`: Input
  - `bid-amount`: Input
  - `auction-name`: Div
  - `minimum-bid`: Div
  - `submit-bid-button`: Button (submits POST to submit_bid route)
- Navigation:
  - Submit form posts to `url_for('submit_bid', auction_id=auction.auction_id)`
- Context variables:
  - `auction`: dict with keys: `auction_id`(int), `item_name`(str), `current_bid`(float), `minimum_bid`(float)
  - Optional: `error_message`(str), `success_message`(str)

### 5. Bid History Page
- Template Filename & Path: `templates/bid_history.html`
- Page Title & `<h1>`: "Bid History"
- Element IDs and Types:
  - `bid-history-page`: Div
  - `bids-table`: Table
  - `filter-by-auction`: Dropdown
  - `sort-by-amount`: Button
  - `back-to-dashboard`: Button (navigates to dashboard_page)
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard_page')`
- Context variables:
  - `bids`: list of dicts with keys: `bid_id`(int), `auction_name`(str), `bidder_name`(str), `bid_amount`(float), `bid_timestamp`(str)
  - `auctions`: list of dicts: `auction_id`(int), `item_name`(str) [for filter dropdown]

### 6. Auction Categories Page
- Template Filename & Path: `templates/categories.html`
- Page Title & `<h1>`: "Auction Categories"
- Element IDs and Types:
  - `categories-page`: Div
  - `categories-list`: Div
  - `category-card-{{ category.category_id }}`: Div (dynamic per category)
  - `view-category-button-{{ category.category_id }}`: Button (dynamic per category)
  - `back-to-dashboard`: Button (navigates to dashboard_page)
- Navigation:
  - `view-category-button-{{ category.category_id }}` uses `url_for('view_category_items', category_id=category.category_id)`
  - `back-to-dashboard` uses `url_for('dashboard_page')`
- Context variables:
  - `categories`: list of dicts with keys: `category_id`(int), `category_name`(str), `description`(str), `item_count`(int)

### 7. Winners Page
- Template Filename & Path: `templates/winners.html`
- Page Title & `<h1>`: "Winning Items"
- Element IDs and Types:
  - `winners-page`: Div
  - `winners-list`: Div
  - `winner-card-{{ auction.auction_id }}`: Div (dynamic per winner item)
  - `filter-by-winner`: Input
  - `back-to-dashboard`: Button (navigates to dashboard_page)
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard_page')`
- Context variables:
  - `winners`: list of dicts with keys: `auction_id`(int), `item_name`(str), `winner_name`(str), `winning_bid`(float)

### 8. Trending Auctions Page
- Template Filename & Path: `templates/trending.html`
- Page Title & `<h1>`: "Trending Auctions"
- Element IDs and Types:
  - `trending-page`: Div
  - `trending-list`: Div
  - `time-range-filter`: Dropdown
  - `view-auction-button-{{ auction.auction_id }}`: Button (dynamic per trending auction)
  - `back-to-dashboard`: Button (navigates to dashboard_page)
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` uses `url_for('auction_details_page', auction_id=auction.auction_id)`
  - `back-to-dashboard` uses `url_for('dashboard_page')`
- Context variables:
  - `trending_auctions`: list of dicts with keys: `auction_id`(int), `item_name`(str), `bid_count`(int), `current_bid`(float), `trending_rank`(int), `time_period`(str)

### 9. Auction Status Page
- Template Filename & Path: `templates/status.html`
- Page Title & `<h1>`: "Auction Status"
- Element IDs and Types:
  - `status-page`: Div
  - `status-filter`: Dropdown
  - `status-table`: Table
  - `refresh-status-button`: Button
  - `back-to-dashboard`: Button (navigates to dashboard_page)
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard_page')`
- Context variables:
  - `auctions`: list of dicts with keys: `auction_id`(int), `item_name`(str), `status`(str), `time_remaining`(str), `current_bid`(float), `end_time`(str)


---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: `data/auctions.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float, 2 decimals)
  6. current_bid (float, 2 decimals)
  7. end_time (str, datetime format `YYYY-MM-DD HH:MM`)
  8. status (str) (e.g., Active, Closed)
  9. image_url (str)
- Purpose: Stores details of auction items including bids and status.
- Example Rows:
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 2. Categories Data
- Path: `data/categories.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores categories information with counts.
- Example Rows:
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 3. Bids Data
- Path: `data/bids.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float, 2 decimals)
  5. bid_timestamp (str, `YYYY-MM-DD HH:MM`)
- Purpose: Stores bid details placed by users.
- Example Rows:
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4. Winners Data
- Path: `data/winners.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float, 2 decimals)
  6. win_date (str, `YYYY-MM-DD`)
- Purpose: Stores info about winning auction items.
- Example Rows:
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 5. Bid History Data
- Path: `data/bid_history.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float, 2 decimals)
  6. bid_timestamp (str, `YYYY-MM-DD HH:MM`)
- Purpose: Detailed historical bid records.
- Example Rows:
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 6. Items Data
- Path: `data/items.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float, 2 decimals)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores item-specific details related to auctions.
- Example Rows:
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 7. Trending Data
- Path: `data/trending.txt`
- File Format: Pipe-delimited (`|`), no header line
- Fields:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float, 2 decimals)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores trending auction rankings and stats.
- Example Rows:
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---
