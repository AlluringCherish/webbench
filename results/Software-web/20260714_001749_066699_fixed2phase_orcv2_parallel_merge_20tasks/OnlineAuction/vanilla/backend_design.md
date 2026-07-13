# Backend Design Document for OnlineAuction Application

---

## Section 1: Flask Routes and Backend Logic

### 1. Dashboard Page
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Logic:**
  - Load featured auction items (e.g., top auctions by bid count or current bid).
  - Load trending auctions (filtered by default time range, e.g., "This Week").
  - Pass data to `dashboard.html` template.
- **Template:** `dashboard.html`

### 2. Auction Catalog Page
- **Route:** `/auctions`
- **Methods:** GET
- **Parameters:** Optional query parameters for search (`search`), category filter (`category`)
- **Logic:**
  - Read all auctions.
  - Filter auctions by search keywords in item name, description, or auction_id.
  - Filter auctions by selected category if provided.
  - Return filtered auction list to `auctions_catalog.html` template.
- **Template:** `auctions_catalog.html`

### 3. Auction Details Page
- **Route:** `/auction/<int:auction_id>`
- **Methods:** GET
- **Logic:**
  - Fetch auction details by auction_id.
  - Load current bids for that auction.
  - Show bid history for this auction.
  - Pass data to `auction_details.html`.
- **Template:** `auction_details.html`

### 4. Place Bid Page
- **Route:** `/auction/<int:auction_id>/place_bid`
- **Methods:** GET, POST
- **GET Logic:**
  - Show auction name and minimum bid amount (current highest bid or starting bid).
  - Render place bid form.
- **POST Logic:**
  - Receive bidder name and bid amount.
  - Validate bid amount (must be greater than current bid).
  - If valid, append bid to bids file and update current_bid in auctions file.
  - Also append to bid_history.
  - Redirect to auction details or success page.
- **Template:** `place_bid.html`

### 5. Bid History Page
- **Route:** `/bid_history`
- **Methods:** GET
- **Parameters:** Optional query for filtering by auction (`auction_id`), optional sort parameter by amount
- **Logic:**
  - Read bids or bid_history file.
  - Filter bids by auction if filter applied.
  - Sort bids if requested.
  - Pass data to `bid_history.html`.
- **Template:** `bid_history.html`

### 6. Auction Categories Page
- **Route:** `/categories`
- **Methods:** GET
- **Logic:**
  - Read all categories.
  - Count items in each category (item_count from categories.txt or computed).
  - Pass to `categories.html` for display.
- **Template:** `categories.html`

### 7. View Items by Category
- **Route:** `/category/<int:category_id>/items`
- **Methods:** GET
- **Logic:**
  - Fetch auctions/items filtered by category.
  - Pass filtered auctions/items to a category items template.
- **Template:** `category_items.html`

### 8. Winners Page
- **Route:** `/winners`
- **Methods:** GET
- **Parameters:** Optional query to filter winners by name.
- **Logic:**
  - Read winners.txt.
  - Filter winners by name if provided.
  - Pass data to `winners.html`.
- **Template:** `winners.html`

### 9. Trending Auctions Page
- **Route:** `/trending`
- **Methods:** GET
- **Parameters:** Optional time range filter (e.g., "Last 24 Hours", "This Week", "All Time")
- **Logic:**
  - Load trending.txt data filtered by time_period.
  - Sort auctions by trending rank.
  - Pass data to `trending.html`.
- **Template:** `trending.html`

### 10. Auction Status Page
- **Route:** `/status`
- **Methods:** GET
- **Parameters:** Optional status filter (`status`: All, Active, Closed, Upcoming)
- **Logic:**
  - Read all auctions.
  - Filter by status if provided.
  - Calculate time remaining for active/upcoming auctions.
  - Render `status.html` with auction statuses.
- **Template:** `status.html`

---

## Section 2: Data File Schemas and Access

All data files reside in the `data/` directory.

### 1. auctions.txt
- **Path:** `data/auctions.txt`
- **Delimiter:** `|`
- **Fields:**
  - auction_id (int): Unique auction identifier
  - item_name (str): Name of the auctioned item
  - description (str): Item description
  - category (str): Category name (corresponds to categories.txt)
  - starting_bid (float): Starting bid amount
  - current_bid (float): Current highest bid
  - end_time (datetime str `%Y-%m-%d %H:%M`): Auction end timestamp
  - status (str): Auction status (Active, Closed, Upcoming)
  - image_url (str): Image filename or URL

- **Example:**
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. categories.txt
- **Path:** `data/categories.txt`
- **Delimiter:** `|`
- **Fields:**
  - category_id (int): Unique category identifier
  - category_name (str): Category name
  - description (str): Description of category
  - item_count (int): Number of items in that category

- **Example:**
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. bids.txt
- **Path:** `data/bids.txt`
- **Delimiter:** `|`
- **Fields:**
  - bid_id (int): Unique bid identifier
  - auction_id (int): Auction the bid belongs to
  - bidder_name (str): Name of bidder
  - bid_amount (float): Bid amount
  - bid_timestamp (datetime str `%Y-%m-%d %H:%M`): Timestamp of bid

- **Example:**
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. winners.txt
- **Path:** `data/winners.txt`
- **Delimiter:** `|`
- **Fields:**
  - winner_id (int): Unique winner record identifier
  - auction_id (int): Won auction id
  - item_name (str): Name of won item
  - winner_name (str): Winner's name
  - winning_bid (float): Winning bid amount
  - win_date (date str `%Y-%m-%d`): Date of winning

- **Example:**
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. bid_history.txt
- **Path:** `data/bid_history.txt`
- **Delimiter:** `|`
- **Fields:**
  - history_id (int): Unique history record id
  - auction_id (int): Auction id associated
  - auction_name (str): Auction item name
  - bidder_name (str): Bidder name
  - bid_amount (float): Bid amount
  - bid_timestamp (datetime str `%Y-%m-%d %H:%M`): Timestamp of bid

- **Example:**
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. items.txt
- **Path:** `data/items.txt`
- **Delimiter:** `|`
- **Fields:**
  - item_id (int): Unique item id
  - auction_id (int): Related auction id
  - item_name (str): Item name
  - starting_price (float): Starting price
  - category (str): Category name
  - condition (str): Item condition description
  - seller_name (str): Seller's name

- **Example:**
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. trending.txt
- **Path:** `data/trending.txt`
- **Delimiter:** `|`
- **Fields:**
  - auction_id (int): Auction id
  - item_name (str): Item name
  - bid_count (int): Number of bids in time period
  - current_bid (float): Current highest bid
  - trending_rank (int): Popularity rank
  - time_period (str): Time range description ("Last 24 Hours", "This Week", "All Time")

- **Example:**
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

## Section 3: Data Management and Business Logic

### Bid Placement
- Validate incoming bid to ensure it exceeds the current highest bid for the auction.
- Generate a new unique bid_id.
- Append the bid to `bids.txt` with timestamp.
- Update the corresponding auction's `current_bid` in `auctions.txt`.
- Append to `bid_history.txt` with a new history_id.
- Use file locks or transactional write mechanisms when modifying files to avoid race conditions.

### Auction Updates
- Periodically or upon bid placement, check auction end times.
- Update auction `status` in `auctions.txt` to Closed if past end_time.
- When auction closes, determine winner (highest bid) and add entry in `winners.txt`.

### Data Retrieval
- For dashboards and trending page, read and aggregate data from `auctions.txt` and `trending.txt` as needed.
- For category views, map categories.txt to auctions.txt or items.txt to count and display items.
- For bid history and winners page, filter or search data by auction or user.

### Concurrency and Consistency
- Implement file locking for write operations to prevent corruption.
- Use atomic file write operations (write to temp file, then rename).
- Consider loading data into memory for read operations to reduce frequent file IO.
- Synchronize updates between `bids.txt`, `auctions.txt`, and `bid_history.txt` to keep data consistent.

---

This backend design document provides the necessary details for implementing the OnlineAuction Flask backend server using local text-based data files, ensuring all routes, data handling, and business logic are fully covered.
