# OnlineAuction Frontend Design Specifications

---

## Section 1: HTML Template Structure

### Template Files Location
All templates are located in the `templates/` directory.

- dashboard.html
- auction_catalog.html
- auction_details.html
- place_bid.html
- bid_history.html
- auction_categories.html
- winners.html
- trending_auctions.html
- auction_status.html

---

### 1. Dashboard Page
- Filename: `dashboard.html`
- Page Title: `Auction Dashboard`

#### Containers & Elements
- `div#dashboard-page` - main container for dashboard.
- `div#featured-auctions` - section displaying featured auction items.
- `button#browse-auctions-button` - navigates to Auction Catalog page.
- `button#view-bids-button` - navigates to Bid History page.
- `button#trending-auctions-button` - navigates to Trending Auctions page.

#### Context Variables
- featured_auctions (list) - to display featured items with details.

---

### 2. Auction Catalog Page
- Filename: `auction_catalog.html`
- Page Title: `Auction Catalog`

#### Containers & Elements
- `div#catalog-page` - main container.
- `input#search-input` - text input for searching auctions.
- `select#category-filter` - dropdown to select category filter.
   - Options: Electronics, Collectibles, Furniture, Art, Other
- `div#auctions-grid` - grid layout displaying auction item cards.
- Auction item cards each contain:
  - `button#view-auction-button-{auction_id}` - button to view auction details.

#### Context Variables
- auctions (list) - list of all auction items.
- categories (list) - list of category names for filter dropdown.

---

### 3. Auction Details Page
- Filename: `auction_details.html`
- Page Title: `Auction Details`

#### Containers & Elements
- `div#auction-details-page` - main container.
- `h1#auction-title` - title of the auction item.
- `div#auction-description` - item description area.
- `div#current-bid` - shows current highest bid.
- `button#place-bid-button` - button to navigate to Place Bid page.
- `div#bid-history` - section displaying bid history entries with bidder names and amounts.

#### Context Variables
- auction (object) - object containing current auction details.
- bid_history (list) - list of bids for this auction.

---

### 4. Place Bid Page
- Filename: `place_bid.html`
- Page Title: `Place Bid`

#### Containers & Elements
- `div#place-bid-page` - main container.
- `input#bidder-name` - input field for bidder's name.
- `input#bid-amount` - input field for bid amount.
- `div#auction-name` - display auction item name.
- `div#minimum-bid` - display minimum acceptable bid.
- `button#submit-bid-button` - button to submit the bid.

#### Context Variables
- auction (object) - auction info including minimum bid.

---

### 5. Bid History Page
- Filename: `bid_history.html`
- Page Title: `Bid History`

#### Containers & Elements
- `div#bid-history-page` - main container.
- `table#bids-table` - table listing bid records. Columns: bid ID, auction name, bidder, amount, timestamp.
- `select#filter-by-auction` - dropdown filter for auction.
- `button#sort-by-amount` - button to sort bids by amount.
- `button#back-to-dashboard` - button to navigate back to dashboard.

#### Context Variables
- bids (list) - list of all bids.
- auctions (list) - for populating filter dropdown.

---

### 6. Auction Categories Page
- Filename: `auction_categories.html`
- Page Title: `Auction Categories`

#### Containers & Elements
- `div#categories-page` - main container.
- `div#categories-list` - container holding category cards.
- Multiple `div#category-card-{category_id}` - individual category cards with name and count.
- Each card contains `button#view-category-button-{category_id}` - to view items in that category.
- `button#back-to-dashboard` - button to navigate back.

#### Context Variables
- categories (list) - list of category objects with id, name, description, count.

---

### 7. Winners Page
- Filename: `winners.html`
- Page Title: `Winning Items`

#### Containers & Elements
- `div#winners-page` - main container.
- `input#filter-by-winner` - input to filter winners by name.
- `div#winners-list` - container for winner cards.
- Multiple `div#winner-card-{auction_id}` - individual winner cards showing item name, winner, winning bid.
- `button#back-to-dashboard` - button to go back.

#### Context Variables
- winners (list) - list of winning items.

---

### 8. Trending Auctions Page
- Filename: `trending_auctions.html`
- Page Title: `Trending Auctions`

#### Containers & Elements
- `div#trending-page` - main container.
- `select#time-range-filter` - dropdown filter for time range.
   - Options: Last 24 Hours, This Week, All Time
- `div#trending-list` - container listing trending auctions.
- Each trending auction item has `button#view-auction-button-{auction_id}` - to view auction details.
- `button#back-to-dashboard` - button to return to dashboard.

#### Context Variables
- trending_auctions (list) - list of trending auctions.

---

### 9. Auction Status Page
- Filename: `auction_status.html`
- Page Title: `Auction Status`

#### Containers & Elements
- `div#status-page` - main container.
- `select#status-filter` - dropdown filter for auction status.
   - Options: All, Active, Closed, Upcoming
- `table#status-table` - table showing auctions with name, status, time remaining, current bid.
- `button#refresh-status-button` - button to refresh auction statuses.
- `button#back-to-dashboard` - button to navigate back.

#### Context Variables
- auctions_status (list) - list of auction statuses.

---

## Section 2: Navigation and Interaction

### Navigation Mapping
- From Dashboard:
  - `browse-auctions-button` -> Auction Catalog page
  - `view-bids-button` -> Bid History page
  - `trending-auctions-button` -> Trending Auctions page

- From Auction Catalog:
  - `view-auction-button-{auction_id}` -> Auction Details page for that auction

- From Auction Details:
  - `place-bid-button` -> Place Bid page for that auction

- From Place Bid:
  - Bid submission handled via form submission; on success navigate to Auction Details or Dashboard

- From Bid History:
  - `back-to-dashboard` -> Dashboard

- From Auction Categories:
  - `view-category-button-{category_id}` -> Auction Catalog filtered by category
  - `back-to-dashboard` -> Dashboard

- From Winners:
  - `back-to-dashboard` -> Dashboard

- From Trending Auctions:
  - `view-auction-button-{auction_id}` -> Auction Details page
  - `back-to-dashboard` -> Dashboard

- From Auction Status:
  - `back-to-dashboard` -> Dashboard
  - `refresh-status-button` reloads data client-side

### Consistent Naming Conventions
- Container div IDs use `[page-name]-page` pattern.
- Buttons use verb-noun pattern with contextual identification, e.g., `view-auction-button-{id}`.
- Filters use `filter-by-[criteria]`.
- Inputs have descriptive IDs: e.g., `bidder-name`, `bid-amount`.

### Client-Side Behaviors
- Auction Catalog:
  - Search input filters auctions by name, description, or id dynamically.
  - Category filter dropdown updates grid display.

- Bid History:
  - Filter by auction dropdown filters rows in table.
  - Sort by amount button toggles ascending/descending.

- Winners:
  - Filter-by-winner input filters winner cards in realtime.

- Trending Auctions:
  - Time-range filter updates the list of trending auctions.

- Auction Status:
  - Status filter updates table display.
  - Refresh button reloads auction status data.

---

## Section 3: Styling and Accessibility Notes

- All main containers have `role="main"` for accessibility.
- Use semantic HTML wherever possible (e.g., `<h1>` for titles, `<table>` for structured data).
- Buttons should have `aria-label` attributes describing the action.
- Dropdowns and inputs to have associated `<label>` elements linked by `for` attribute matching element ID.
- Responsive layout:
  - Auctions grid and cards adapt using CSS grid or flexbox for different screen sizes.
  - Navigation buttons grouped and spaced for easy tapping on touch devices.
- Ensure color contrast meets WCAG standards.
- For tables, use `<thead>`, `<tbody>` appropriately and support keyboard navigation.

---

# End of Frontend Design Document
