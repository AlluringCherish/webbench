# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                        | Function Name          | HTTP Method | Template to Render            | Context Variables with Types                                                                                                                                                           |
|---------------------------------|------------------------|-------------|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                             | root_redirect          | GET         | Redirect (to /dashboard)      | None                                                                                                                                                                                    |
| `/dashboard`                    | dashboard              | GET         | templates/dashboard.html      | featured_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, end_time:str, image_url:str}], trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int, trending_rank:int}]                            |
| `/catalog`                     | auction_catalog        | GET         | templates/catalog.html        | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}], categories: list[str]                                                                                           |
| `/auction/<int:auction_id>`     | auction_details        | GET         | templates/auction_details.html | auction: dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str, status:str}, bid_history: list[dict{bid_id:int, bidder_name:str, bid_amount:float, bid_timestamp:str}]                   |
| `/auction/<int:auction_id>/place_bid` | place_bid             | GET         | templates/place_bid.html      | auction: dict{auction_id:int, item_name:str, current_bid:float}, minimum_bid: float                                                                                                     |
| `/auction/<int:auction_id>/place_bid` | submit_bid            | POST        | Redirect or re-render place_bid | bid_success: bool, errors: dict[str,str], auction: dict{auction_id:int, item_name:str, current_bid:float}, minimum_bid: float                                                            |
| `/bid_history`                 | bid_history            | GET         | templates/bid_history.html    | bids: list[dict{bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str}], auctions: list[dict{auction_id:int, item_name:str}]                                   |
| `/categories`                 | auction_categories      | GET         | templates/categories.html     | categories: list[dict{category_id:int, category_name:str, description:str, item_count:int}]                                                                                               |
| `/category/<int:category_id>`   | view_category          | GET         | templates/catalog.html        | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str}]                                                        |
| `/winners`                    | winners                | GET         | templates/winners.html        | winners: list[dict{winner_id:int, auction_id:int, item_name:str, winner_name:str, winning_bid:float}]                                                                                      |
| `/trending`                   | trending_auctions       | GET         | templates/trending.html       | trending_auctions: list[dict{auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str}]                                                        |
| `/auction_status`              | auction_status         | GET         | templates/auction_status.html | auctions: list[dict{auction_id:int, item_name:str, status:str, time_remaining:str, current_bid:float}]                                                                                     |

Notes:
- `/` redirects to `/dashboard`.
- POST `/auction/<auction_id>/place_bid` processes bid submissions.

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Filename: `templates/dashboard.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Auction Dashboard`
- Element IDs and Types:
  - `dashboard-page`: Div
  - `featured-auctions`: Div
  - `browse-auctions-button`: Button (navigates to Auction Catalog)
  - `view-bids-button`: Button (navigates to Bid History)
  - `trending-auctions-button`: Button (navigates to Trending Auctions)
- Navigation:
  - `browse-auctions-button` uses `url_for('auction_catalog')`
  - `view-bids-button` uses `url_for('bid_history')`
  - `trending-auctions-button` uses `url_for('trending_auctions')`
- Context Variables:
  - `featured_auctions`: list of dicts with keys: auction_id (int), item_name (str), current_bid (float), end_time (str), image_url (str)
  - `trending_auctions`: list of dicts with keys: auction_id (int), item_name (str), current_bid (float), bid_count (int), trending_rank (int)

### 2. Auction Catalog Page
- Filename: `templates/catalog.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Auction Catalog`
- Element IDs and Types:
  - `catalog-page`: Div
  - `search-input`: Input
  - `category-filter`: Dropdown
  - `auctions-grid`: Div
  - `view-auction-button-{{ auction.auction_id }}`: Button (dynamic per auction)
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` uses `url_for('auction_details', auction_id=auction.auction_id)`
- Context Variables:
  - `auctions`: list of dicts with keys: auction_id (int), item_name (str), description (str), category (str), current_bid (float), end_time (str), image_url (str)
  - `categories`: list of strings

### 3. Auction Details Page
- Filename: `templates/auction_details.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Auction Details`
- Element IDs and Types:
  - `auction-details-page`: Div
  - `auction-title`: H1
  - `auction-description`: Div
  - `current-bid`: Div
  - `place-bid-button`: Button (navigates to Place Bid page)
  - `bid-history`: Div
- Navigation:
  - `place-bid-button` uses `url_for('place_bid', auction_id=auction.auction_id)`
- Context Variables:
  - `auction`: dict with keys: auction_id (int), item_name (str), description (str), category (str), current_bid (float), end_time (str), image_url (str), status (str)
  - `bid_history`: list of dicts with keys: bid_id (int), bidder_name (str), bid_amount (float), bid_timestamp (str)

### 4. Place Bid Page
- Filename: `templates/place_bid.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Place Bid`
- Element IDs and Types:
  - `place-bid-page`: Div
  - `bidder-name`: Input
  - `bid-amount`: Input
  - `auction-name`: Div
  - `minimum-bid`: Div
  - `submit-bid-button`: Button (form submit)
- Navigation:
  - Form action uses `url_for('submit_bid', auction_id=auction.auction_id)` 
- Context Variables:
  - `auction`: dict with keys: auction_id (int), item_name (str), current_bid (float)
  - `minimum_bid`: float
  - `errors`: dict[str,str] (on form validation failure)

### 5. Bid History Page
- Filename: `templates/bid_history.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Bid History`
- Element IDs and Types:
  - `bid-history-page`: Div
  - `bids-table`: Table
  - `filter-by-auction`: Dropdown
  - `sort-by-amount`: Button
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context Variables:
  - `bids`: list of dicts with keys: bid_id (int), auction_name (str), bidder_name (str), bid_amount (float), bid_timestamp (str)
  - `auctions`: list of dicts with keys: auction_id (int), item_name (str)

### 6. Auction Categories Page
- Filename: `templates/categories.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Auction Categories`
- Element IDs and Types:
  - `categories-page`: Div
  - `categories-list`: Div
  - `category-card-{{ category.category_id }}`: Div (dynamic per category)
  - `view-category-button-{{ category.category_id }}`: Button (dynamic per category)
  - `back-to-dashboard`: Button
- Navigation:
  - `view-category-button-{{ category.category_id }}` uses `url_for('view_category', category_id=category.category_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context Variables:
  - `categories`: list of dicts with keys: category_id (int), category_name (str), description (str), item_count (int)

### 7. Winners Page
- Filename: `templates/winners.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Winning Items`
- Element IDs and Types:
  - `winners-page`: Div
  - `winners-list`: Div
  - `winner-card-{{ winner.auction_id }}`: Div (dynamic per winner)
  - `filter-by-winner`: Input
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context Variables:
  - `winners`: list of dicts with keys: winner_id (int), auction_id (int), item_name (str), winner_name (str), winning_bid (float)

### 8. Trending Auctions Page
- Filename: `templates/trending.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Trending Auctions`
- Element IDs and Types:
  - `trending-page`: Div
  - `trending-list`: Div
  - `time-range-filter`: Dropdown
  - `view-auction-button-{{ auction.auction_id }}`: Button (dynamic per auction)
  - `back-to-dashboard`: Button
- Navigation:
  - `view-auction-button-{{ auction.auction_id }}` uses `url_for('auction_details', auction_id=auction.auction_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context Variables:
  - `trending_auctions`: list of dicts with keys: auction_id (int), item_name (str), bid_count (int), current_bid (float), trending_rank (int), time_period (str)

### 9. Auction Status Page
- Filename: `templates/auction_status.html`
- Page Title (for &lt;title&gt; and &lt;h1&gt;): `Auction Status`
- Element IDs and Types:
  - `status-page`: Div
  - `status-filter`: Dropdown
  - `status-table`: Table
  - `refresh-status-button`: Button
  - `back-to-dashboard`: Button
- Navigation:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context Variables:
  - `auctions`: list of dicts with keys: auction_id (int), item_name (str), status (str), time_remaining (str), current_bid (float)

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
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str, format `YYYY-MM-DD HH:MM`)
  8. status (str)
  9. image_url (str)
- Description: Auction items data including bids, status, and details
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
- Description: Auction categories data with descriptions and counts
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
  4. bid_amount (float)
  5. bid_timestamp (str, format `YYYY-MM-DD HH:MM`)
- Description: Bids placed on auctions with timestamps
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
  5. winning_bid (float)
  6. win_date (str, format `YYYY-MM-DD`)
- Description: Winners of auctions with winning bid details and date
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
  5. bid_amount (float)
  6. bid_timestamp (str, format `YYYY-MM-DD HH:MM`)
- Description: Detailed ordered bid records per auction
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
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Description: Item details associated with auctions
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
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Description: Auction trending ranks and bid counts over time periods
- Example Rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

**CRITICAL SUCCESS CRITERIA:**
- Backend developers can implement Flask routes and data parsing with Sections 1 and 3.
- Frontend developers can implement templates with correct IDs and navigation with Section 2.
- No overlap dependencies beyond these interface contracts.
- Element IDs and page titles exactly as specified.

---

**End of Design Specification**
