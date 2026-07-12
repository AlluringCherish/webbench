# OnlineAuction Application Design Specification

---

## Section 1: Flask Backend Routes Specification

| Route Path                 | Function Name          | HTTP Method | Template              | Context Variables                                                                                          |
|----------------------------|------------------------|-------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| /                          | root_redirect          | GET         | None (redirect)       | None                                                                                                       |
| /dashboard                 | dashboard              | GET         | dashboard.html        | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str}, trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int}, categories: list of dict {category_id: int, category_name: str, item_count: int} |
| /catalog                   | auction_catalog        | GET         | catalog.html          | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}, categories: list of dict {category_id: int, category_name: str}                                  |
| /auction/<int:auction_id>  | auction_details        | GET         | auction_details.html  | auction: dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str}, bid_history: list of dict {bidder_name: str, bid_amount: float, bid_timestamp: str}         |
| /auction/<int:auction_id>/bid | place_bid           | GET, POST   | place_bid.html        | For GET: auction: dict {auction_id: int, item_name: str, minimum_bid: float}, For POST: success: bool, error_message: str (if any)                                   |
| /bids                     | bid_history            | GET         | bid_history.html      | bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}, auctions: list of dict {auction_id: int, item_name: str}                                                      |
| /categories               | auction_categories     | GET         | categories.html       | categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}                                                                   |
| /winners                  | winners                | GET         | winners.html          | winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}                                         |
| /trending                 | trending_auctions      | GET         | trending.html         | trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}                           |
| /status                   | auction_status         | GET         | status.html           | auctions: list of dict {auction_id: int, item_name: str, status: str, current_bid: float, time_remaining: str}                                                        |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template Filename and Path: `templates/dashboard.html`
- Page Title: "Auction Dashboard"
- <h1> Title: "Auction Dashboard"
- Element IDs and Types:
  - `dashboard-page`: Div
  - `featured-auctions`: Div
  - `browse-auctions-button`: Button
  - `view-bids-button`: Button
  - `trending-auctions-button`: Button
- Navigation:
  - `browse-auctions-button` navigates to `auction_catalog` route
  - `view-bids-button` navigates to `bid_history` route
  - `trending-auctions-button` navigates to `trending_auctions` route
- Context Variables:
  - `featured_auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str), `current_bid` (float), `end_time` (str)
  - `trending_auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str), `current_bid` (float), `bid_count` (int)
  - `categories`: List of dicts with keys: `category_id` (int), `category_name` (str), `item_count` (int)

### 2. Auction Catalog Page
- Template Filename and Path: `templates/catalog.html`
- Page Title: "Auction Catalog"
- <h1> Title: "Auction Catalog"
- Element IDs and Types:
  - `catalog-page`: Div
  - `search-input`: Input
  - `category-filter`: Dropdown (select element)
  - `auctions-grid`: Div
  - `view-auction-button-{{ auction.auction_id }}`: Button (dynamic, per auction)
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` navigates to `auction_details` route with `auction_id`
- Context Variables:
  - `auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str), `description` (str), `category` (str), `current_bid` (float), `end_time` (str), `image_url` (str)
  - `categories`: List of dicts with keys: `category_id` (int), `category_name` (str)

### 3. Auction Details Page
- Template Filename and Path: `templates/auction_details.html`
- Page Title: "Auction Details"
- <h1> Title: "Auction Details"
- Element IDs and Types:
  - `auction-details-page`: Div
  - `auction-title`: H1
  - `auction-description`: Div
  - `current-bid`: Div
  - `place-bid-button`: Button
  - `bid-history`: Div
- Navigation:
  - `place-bid-button` navigates to `place_bid` route with auction_id
- Context Variables:
  - `auction`: Dict with keys: `auction_id` (int), `item_name` (str), `description` (str), `category` (str), `current_bid` (float), `end_time` (str), `status` (str), `image_url` (str)
  - `bid_history`: List of dicts with keys: `bidder_name` (str), `bid_amount` (float), `bid_timestamp` (str)

### 4. Place Bid Page
- Template Filename and Path: `templates/place_bid.html`
- Page Title: "Place Bid"
- <h1> Title: "Place Bid"
- Element IDs and Types:
  - `place-bid-page`: Div
  - `bidder-name`: Input
  - `bid-amount`: Input
  - `auction-name`: Div
  - `minimum-bid`: Div
  - `submit-bid-button`: Button
- Navigation:
  - `submit-bid-button` submits POST to `place_bid` route with auction_id
- Context Variables:
  - On GET: `auction`: Dict {auction_id: int, item_name: str, minimum_bid: float}
  - On POST: `success`: bool, `error_message`: str (optional)

### 5. Bid History Page
- Template Filename and Path: `templates/bid_history.html`
- Page Title: "Bid History"
- <h1> Title: "Bid History"
- Element IDs and Types:
  - `bid-history-page`: Div
  - `bids-table`: Table
  - `filter-by-auction`: Dropdown (select element)
  - `sort-by-amount`: Button
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` navigates to `dashboard` route
- Context Variables:
  - `bids`: List of dicts with keys: `bid_id` (int), `auction_name` (str), `bidder_name` (str), `bid_amount` (float), `bid_timestamp` (str)
  - `auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str)

### 6. Auction Categories Page
- Template Filename and Path: `templates/categories.html`
- Page Title: "Auction Categories"
- <h1> Title: "Auction Categories"
- Element IDs and Types:
  - `categories-page`: Div
  - `categories-list`: Div
  - `category-card-{{ category.category_id }}`: Div (dynamic per category)
  - `view-category-button-{{ category.category_id }}`: Button (dynamic per category)
  - `back-to-dashboard`: Button
- Navigation:
  - `view-category-button-{{ category.category_id }}` navigates to filtered `auction_catalog` route or special category route if applicable
  - `back-to-dashboard` navigates to `dashboard` route
- Context Variables:
  - `categories`: List of dicts with keys: `category_id` (int), `category_name` (str), `description` (str), `item_count` (int)

### 7. Winners Page
- Template Filename and Path: `templates/winners.html`
- Page Title: "Winning Items"
- <h1> Title: "Winning Items"
- Element IDs and Types:
  - `winners-page`: Div
  - `winners-list`: Div
  - `winner-card-{{ winner.auction_id }}`: Div (dynamic per winner)
  - `filter-by-winner`: Input
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` navigates to `dashboard` route
- Context Variables:
  - `winners`: List of dicts with keys: `winner_id` (int), `auction_id` (int), `item_name` (str), `winner_name` (str), `winning_bid` (float), `win_date` (str)

### 8. Trending Auctions Page
- Template Filename and Path: `templates/trending.html`
- Page Title: "Trending Auctions"
- <h1> Title: "Trending Auctions"
- Element IDs and Types:
  - `trending-page`: Div
  - `trending-list`: Div
  - `time-range-filter`: Dropdown (select element)
  - `view-auction-button-{{ auction.auction_id }}`: Button (dynamic per auction)
  - `back-to-dashboard`: Button
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` navigates to `auction_details` route
  - `back-to-dashboard` navigates to `dashboard` route
- Context Variables:
  - `trending_auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str), `bid_count` (int), `current_bid` (float), `trending_rank` (int), `time_period` (str)

### 9. Auction Status Page
- Template Filename and Path: `templates/status.html`
- Page Title: "Auction Status"
- <h1> Title: "Auction Status"
- Element IDs and Types:
  - `status-page`: Div
  - `status-filter`: Dropdown (select element)
  - `status-table`: Table
  - `refresh-status-button`: Button
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` navigates to `dashboard` route
- Context Variables:
  - `auctions`: List of dicts with keys: `auction_id` (int), `item_name` (str), `status` (str), `time_remaining` (str), `current_bid` (float)

---

## Section 3: Data File Schemas (Backend)

1. Auctions Data
- Path: `data/auctions.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str: "YYYY-MM-DD HH:MM")
  8. status (str) - e.g. Active, Closed
  9. image_url (str)
- Purpose: Stores all auctions with details including status and bids
- Example Rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

2. Categories Data
- Path: `data/categories.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores auction categories with descriptions and counts
- Example Rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

3. Bids Data
- Path: `data/bids.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str: "YYYY-MM-DD HH:MM")
- Purpose: Stores all bids placed by users with timestamps
- Example Rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

4. Winners Data
- Path: `data/winners.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str: "YYYY-MM-DD")
- Purpose: Stores winning auction items with winner and date
- Example Rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

5. Bid History Data
- Path: `data/bid_history.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str: "YYYY-MM-DD HH:MM")
- Purpose: Records all bid history across auctions
- Example Rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

6. Items Data
- Path: `data/items.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores details about individual items linked to auctions
- Example Rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

7. Trending Data
- Path: `data/trending.txt`
- File Format: pipe-delimited (|), no header line
- Fields Order and Names:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores trending auction information by bid activity and rank
- Example Rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

This design specification enables Backend and Frontend teams to implement the 'OnlineAuction' application independently and in parallel, adhering strictly to all requirements with exact element IDs and page titles.
