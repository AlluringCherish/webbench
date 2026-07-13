# Unified Design Specification for OnlineAuction Application

---

## Section 1: Backend Routes & Data

### 1. Dashboard Page
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Logic:**
  - Load featured auction items (e.g., top auctions by bid count or current bid).
  - Load trending auctions filtered by default time range ("This Week").
  - Pass data to `dashboard.html` template.
- **Template:** `dashboard.html`

### 2. Auction Catalog Page
- **Route:** `/auctions`
- **Methods:** GET
- **Parameters:** Optional query parameters: `search` (keywords), `category` (category filter)
- **Logic:**
  - Read all auctions.
  - Filter auctions by search keywords in item name, description, or auction_id.
  - Filter auctions by selected category if provided.
  - Return filtered auctions to `auction_catalog.html` template.
- **Template:** `auction_catalog.html`

### 3. Auction Details Page
- **Route:** `/auction/<int:auction_id>`
- **Methods:** GET
- **Logic:**
  - Fetch auction details by auction_id.
  - Load current bids and bid history for that auction.
  - Pass data to `auction_details.html` template.
- **Template:** `auction_details.html`

### 4. Place Bid Page
- **Route:** `/auction/<int:auction_id>/place_bid`
- **Methods:** GET, POST
- **GET Logic:**
  - Show auction name and minimum bid amount (current highest bid or starting bid).
  - Render place bid form.
- **POST Logic:**
  - Receive `bidder_name` and `bid_amount`.
  - Validate bid amount (must be greater than current bid).
  - If valid, append bid to `bids.txt` with new `bid_id` and timestamp.
  - Update `current_bid` in `auctions.txt`.
  - Append new record to `bid_history.txt` with new `history_id`.
  - Use file locks or transactional writes to prevent race conditions.
  - Redirect to auction details or success page.
- **Template:** `place_bid.html`

### 5. Bid History Page
- **Route:** `/bid_history`
- **Methods:** GET
- **Parameters:** Optional query parameter `auction_id` for filtering; optional sort parameter by `amount`
- **Logic:**
  - Read bids from `bids.txt` or `bid_history.txt`.
  - Filter bids by auction if filter applied.
  - Sort bids by amount if requested.
  - Pass filtered, sorted data to `bid_history.html`.
- **Template:** `bid_history.html`

### 6. Auction Categories Page
- **Route:** `/categories`
- **Methods:** GET
- **Logic:**
  - Read all categories from `categories.txt`.
  - Count items in each category (from file or computed).
  - Pass data to `auction_categories.html`.
- **Template:** `auction_categories.html`

### 7. View Items by Category
- **Route:** `/category/<int:category_id>/items`
- **Methods:** GET
- **Logic:**
  - Fetch auctions/items filtered by category.
  - Pass filtered list to `category_items.html`.
- **Template:** `category_items.html`

### 8. Winners Page
- **Route:** `/winners`
- **Methods:** GET
- **Parameters:** Optional filter by winner `name`.
- **Logic:**
  - Read winners from `winners.txt`.
  - Filter winners by name if provided.
  - Pass data to `winners.html`.
- **Template:** `winners.html`

### 9. Trending Auctions Page
- **Route:** `/trending`
- **Methods:** GET
- **Parameters:** Optional time range filter (e.g., "Last 24 Hours", "This Week", "All Time")
- **Logic:**
  - Load trending auctions from `trending.txt`, filtered by time_period.
  - Sort by trending rank.
  - Pass data to `trending_auctions.html`.
- **Template:** `trending_auctions.html`

### 10. Auction Status Page
- **Route:** `/status`
- **Methods:** GET
- **Parameters:** Optional status filter (`status`: All, Active, Closed, Upcoming)
- **Logic:**
  - Read auctions from `auctions.txt`.
  - Filter by status if provided.
  - Calculate time remaining for active/upcoming auctions.
  - Pass data to `auction_status.html`.
- **Template:** `auction_status.html`

---

## Section 2: Frontend Templates & Elements

### Template Files Location
All templates reside in the `templates/` directory.

- `dashboard.html`
- `auction_catalog.html`
- `auction_details.html`
- `place_bid.html`
- `bid_history.html`
- `auction_categories.html`
- `winners.html`
- `trending_auctions.html`
- `auction_status.html`

---

### 1. Dashboard Page (`dashboard.html`)
- Page Title: `Auction Dashboard`
- Containers & Elements:
  - `div#dashboard-page` (main container)
  - `div#featured-auctions` (featured auction items)
  - `button#browse-auctions-button` (navigate to Auction Catalog page)
  - `button#view-bids-button` (navigate to Bid History page)
  - `button#trending-auctions-button` (navigate to Trending Auctions page)
- Context Variables: `featured_auctions` (list)

### 2. Auction Catalog Page (`auction_catalog.html`)
- Page Title: `Auction Catalog`
- Containers & Elements:
  - `div#catalog-page` (main container)
  - `input#search-input` (search auctions by name, description, or id)
  - `select#category-filter` (dropdown filter categories: Electronics, Collectibles, Furniture, Art, Other)
  - `div#auctions-grid` (grid displaying auction item cards)
  - Auction item cards with `button#view-auction-button-{auction_id}` to view details
- Context Variables: `auctions` (list), `categories` (list)

### 3. Auction Details Page (`auction_details.html`)
- Page Title: `Auction Details`
- Containers & Elements:
  - `div#auction-details-page` (main container)
  - `h1#auction-title` (auction item title)
  - `div#auction-description` (item description)
  - `div#current-bid` (current highest bid)
  - `button#place-bid-button` (navigate to Place Bid page)
  - `div#bid-history` (bid history section with bidder names and amounts)
- Context Variables: `auction` (object), `bid_history` (list)

### 4. Place Bid Page (`place_bid.html`)
- Page Title: `Place Bid`
- Containers & Elements:
  - `div#place-bid-page` (main container)
  - `input#bidder-name` (bidder's name)
  - `input#bid-amount` (bid amount)
  - `div#auction-name` (auction item name)
  - `div#minimum-bid` (minimum acceptable bid)
  - `button#submit-bid-button` (submit bid)
- Context Variables: `auction` (object)

### 5. Bid History Page (`bid_history.html`)
- Page Title: `Bid History`
- Containers & Elements:
  - `div#bid-history-page` (main container)
  - `table#bids-table` (bid records: bid ID, auction name, bidder, amount, timestamp)
  - `select#filter-by-auction` (filter bids by auction)
  - `button#sort-by-amount` (sort bids by amount)
  - `button#back-to-dashboard` (navigate back to dashboard)
- Context Variables: `bids` (list), `auctions` (list for filter dropdown)

### 6. Auction Categories Page (`auction_categories.html`)
- Page Title: `Auction Categories`
- Containers & Elements:
  - `div#categories-page` (main container)
  - `div#categories-list` (list of categories)
  - `div#category-card-{category_id}` (individual category card)
  - `button#view-category-button-{category_id}` (view items in category)
  - `button#back-to-dashboard` (navigate back)
- Context Variables: `categories` (list of objects with id, name, description, item_count)

### 7. Winners Page (`winners.html`)
- Page Title: `Winning Items`
- Containers & Elements:
  - `div#winners-page` (main container)
  - `input#filter-by-winner` (filter winners by name)
  - `div#winners-list` (list of winner cards)
  - `div#winner-card-{auction_id}` (individual winner card showing item name, winner, winning bid)
  - `button#back-to-dashboard` (navigate back)
- Context Variables: `winners` (list)

### 8. Trending Auctions Page (`trending_auctions.html`)
- Page Title: `Trending Auctions`
- Containers & Elements:
  - `div#trending-page` (main container)
  - `select#time-range-filter` (filter time range: Last 24 Hours, This Week, All Time)
  - `div#trending-list` (list of trending auctions)
  - Each trending auction item has `button#view-auction-button-{auction_id}`
  - `button#back-to-dashboard` (navigate back)
- Context Variables: `trending_auctions` (list)

### 9. Auction Status Page (`auction_status.html`)
- Page Title: `Auction Status`
- Containers & Elements:
  - `div#status-page` (main container)
  - `select#status-filter` (filter status: All, Active, Closed, Upcoming)
  - `table#status-table` (auctions with name, status, time remaining, current bid)
  - `button#refresh-status-button` (refresh auction statuses)
  - `button#back-to-dashboard` (navigate back)
- Context Variables: `auctions_status` (list)

---

## Section 3: Data Schemas & Integration Notes

### Data Files Location
All data files stored in `data/` directory.

### 1. auctions.txt
- **Delimiter:** `|`
- Fields: `auction_id` (int), `item_name` (str), `description` (str), `category` (str), `starting_bid` (float), `current_bid` (float), `end_time` (datetime `%Y-%m-%d %H:%M`), `status` (str), `image_url` (str)

### 2. categories.txt
- **Delimiter:** `|`
- Fields: `category_id` (int), `category_name` (str), `description` (str), `item_count` (int)

### 3. bids.txt
- **Delimiter:** `|`
- Fields: `bid_id` (int), `auction_id` (int), `bidder_name` (str), `bid_amount` (float), `bid_timestamp` (datetime `%Y-%m-%d %H:%M`)

### 4. winners.txt
- **Delimiter:** `|`
- Fields: `winner_id` (int), `auction_id` (int), `item_name` (str), `winner_name` (str), `winning_bid` (float), `win_date` (date `%Y-%m-%d`)

### 5. bid_history.txt
- **Delimiter:** `|`
- Fields: `history_id` (int), `auction_id` (int), `auction_name` (str), `bidder_name` (str), `bid_amount` (float), `bid_timestamp` (datetime `%Y-%m-%d %H:%M`)

### 6. items.txt
- **Delimiter:** `|`
- Fields: `item_id` (int), `auction_id` (int), `item_name` (str), `starting_price` (float), `category` (str), `condition` (str), `seller_name` (str)

### 7. trending.txt
- **Delimiter:** `|`
- Fields: `auction_id` (int), `item_name` (str), `bid_count` (int), `current_bid` (float), `trending_rank` (int), `time_period` (str)

### Integration Notes
- All backend routes use these data files for reading and updating.
- Frontend pages display data passed from backend templates using context variables aligned with data files.
- Navigation button IDs correspond to backend routes.
- Element IDs in frontend templates are consistent with the naming conventions and used fields.
- Bid placement ensures atomic updates to `bids.txt`, `bid_history.txt`, and `auctions.txt`.
- Filters in frontend (search, category, status) correspond to backend route query parameters.

---

## Summary

- Backend and frontend design are fully aligned by route paths, templates, containers, and element IDs.
- Data files and schemas are consistent and support all frontend dynamic content requirements.
- Navigation flows from frontend elements map directly to backend routes.
- Bid placement and auction updates handled with concurrency protections.
- No features added or omitted; all user_task_description requirements are preserved.

Developers should ensure consistent handling of file locking and atomic writes in backend and validate frontend element IDs in templates during implementation.

# End of Design Specification
