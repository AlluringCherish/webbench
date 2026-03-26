# RealEstate Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

### 1. Dashboard Page
- **URL Path:** `/dashboard`
- **HTTP Method:** GET
- **Function Name:** `dashboard_page`
- **HTML Template:** `dashboard.html`
- **Context Variables:**
  - `featured_properties` (list of dict): List of featured property data including keys such as `property_id` (int), `address` (str), `price` (float), `bedrooms` (int), `bathrooms` (float)
  - `recent_listings` (list of dict): List of recent property listings with similar structure

---

### Root Route
- **URL Path:** `/`
- **HTTP Method:** GET
- **Function Name:** `root_redirect`
- **Behavior:** Redirects to `/dashboard`
- **HTML Template:** None
- **Context Variables:** None

---

### 2. Property Search Page
- **URL Path:** `/search`
- **HTTP Method:** GET
- **Function Name:** `property_search`
- **HTML Template:** `search.html`
- **Context Variables:**
  - `properties` (list of dict): List of all available properties with keys including `property_id` (int), `address` (str), `location` (str), `price` (float), `property_type` (str), `bedrooms` (int), `bathrooms` (float), `square_feet` (int)
  - `property_types` (list of str): List containing property types: `['House', 'Apartment', 'Condo', 'Land']`

---

### 3. Property Details Page
- **URL Path:** `/property/<int:property_id>`
- **HTTP Method:** GET
- **Function Name:** `property_details`
- **HTML Template:** `property_details.html`
- **Context Variables:**
  - `property` (dict): Detailed property information with keys including `property_id` (int), `address` (str), `price` (float), `description` (str), `bedrooms` (int), `bathrooms` (float), `square_feet` (int)

---

### 4. Property Inquiry Page
- **URL Path:** `/inquiry`
- **HTTP Method:** GET
- **Function Name:** `property_inquiry`
- **HTML Template:** `inquiry.html`
- **Context Variables:**
  - `properties` (list of dict): List of available properties with keys: `property_id` (int), `address` (str)

---

- **URL Path:** `/inquiry`
- **HTTP Method:** POST
- **Function Name:** `submit_inquiry`
- **HTML Template:** `inquiry.html` (rendered again on failure or redirect to inquiries page on success)
- **Expected Form Data:**
  - `property_id` (int)
  - `inquiry_name` (str)
  - `inquiry_email` (str)
  - `inquiry_phone` (str)
  - `inquiry_message` (str)

---

### 5. My Inquiries Page
- **URL Path:** `/my-inquiries`
- **HTTP Method:** GET
- **Function Name:** `my_inquiries_page`
- **HTML Template:** `my_inquiries.html`
- **Context Variables:**
  - `inquiries` (list of dict): List of inquiries with keys including `inquiry_id` (int), `property_id` (int), `property_address` (str), `inquiry_date` (str ISO date), `status` (str), `customer_name` (str), `customer_email` (str), `customer_phone` (str)
  - `status_filter` (str): Current filter value among `All`, `Pending`, `Contacted`, `Resolved`

- **URL Path:** `/my-inquiries/delete/<int:inquiry_id>`
- **HTTP Method:** POST
- **Function Name:** `delete_inquiry`
- **HTML Template:** None (redirect back to `/my-inquiries`)
- **Expected Form Data:** None

---

### 6. My Favorites Page
- **URL Path:** `/my-favorites`
- **HTTP Method:** GET
- **Function Name:** `my_favorites_page`
- **HTML Template:** `my_favorites.html`
- **Context Variables:**
  - `favorites` (list of dict): List of favorite properties with keys including `property_id` (int), `address` (str), `price` (float), `bedrooms` (int), `bathrooms` (float)

- **URL Path:** `/my-favorites/remove/<int:property_id>`
- **HTTP Method:** POST
- **Function Name:** `remove_favorite`
- **HTML Template:** None (redirect to `/my-favorites`)
- **Expected Form Data:** None

---

### 7. Agent Directory Page
- **URL Path:** `/agents`
- **HTTP Method:** GET
- **Function Name:** `agent_directory`
- **HTML Template:** `agents.html`
- **Context Variables:**
  - `agents` (list of dict): List of agents including `agent_id` (int), `agent_name` (str), `specialization` (str), `email` (str), `phone` (str)

---

### 8. Locations Page
- **URL Path:** `/locations`
- **HTTP Method:** GET
- **Function Name:** `locations_page`
- **HTML Template:** `locations.html`
- **Context Variables:**
  - `locations` (list of dict): List of locations with keys `location_id` (int), `location_name` (str), `region` (str), `average_price` (float), `property_count` (int), `description` (str)

---

## Section 2: HTML Templates (Frontend)

### 1. Template: dashboard.html
- **Page Title:** Real Estate Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `featured-properties` (div)
  - `browse-properties-button` (button)
  - `my-inquiries-button` (button)
  - `my-favorites-button` (button)
- **Context Variables:**
  - `featured_properties` (list of dict): Featured properties data.
  - `recent_listings` (list of dict): Recent property listings.
- **Navigation (flask url_for):**
  - Browse Properties Button: `url_for('property_search')`
  - My Inquiries Button: `url_for('my_inquiries_page')`
  - My Favorites Button: `url_for('my_favorites_page')`
- **Forms:** None

---

### 2. Template: search.html
- **Page Title:** Property Search
- **Element IDs:**
  - `search-page` (div)
  - `location-input` (input)
  - `price-range-min` (input, type=number)
  - `price-range-max` (input, type=number)
  - `property-type-filter` (dropdown/select)
  - `properties-grid` (div)
  - Dynamic ID: `view-property-button-{property_id}` (button) for each property
- **Context Variables:**
  - `properties` (list of dict): All properties to display.
  - `property_types` (list of str): Property type options.
- **Navigation (flask url_for):**
  - View Property Button: `url_for('property_details', property_id=property_id)`
- **Forms:**
  - Search/Filter Form (if implemented): 
    - Inputs with IDs: `location-input`, `price-range-min`, `price-range-max`, `property-type-filter`
    - Form action endpoint: `url_for('property_search')` (GET method)

---

### 3. Template: property_details.html
- **Page Title:** Property Details
- **Element IDs:**
  - `property-details-page` (div)
  - `property-address` (h1)
  - `property-price` (div)
  - `property-description` (div)
  - `property-features` (div)
  - `add-to-favorites-button` (button)
  - `submit-inquiry-button` (button)
- **Context Variables:**
  - `property` (dict): Full property details.
- **Navigation (flask url_for):**
  - Add to Favorites Button: `url_for('my_favorites_page')` or POST endpoint to add favorite
  - Submit Inquiry Button: `url_for('property_inquiry')` (may preselect this property)
- **Forms:**
  - Add to Favorites Form:
    - Button ID: `add-to-favorites-button`
    - Form action endpoint: (e.g., POST `/my-favorites/add/<property_id>`) *Note: This route is not specified in requirements, so omitted*
  - Inquiry Submission Button triggers navigation or modal form.

---

### 4. Template: inquiry.html
- **Page Title:** Submit Property Inquiry
- **Element IDs:**
  - `inquiry-page` (div)
  - `select-property` (dropdown/select)
  - `inquiry-name` (input)
  - `inquiry-email` (input, type=email)
  - `inquiry-phone` (input, type=tel)
  - `inquiry-message` (textarea)
  - `submit-inquiry-button` (button)
- **Context Variables:**
  - `properties` (list of dict): Properties for selection
- **Navigation (flask url_for):** None
- **Forms:**
  - Inquiry Form
    - Inputs with IDs: `select-property`, `inquiry-name`, `inquiry-email`, `inquiry-phone`, `inquiry-message`
    - Form action endpoint: `url_for('submit_inquiry')`
    - Method: POST

---

### 5. Template: my_inquiries.html
- **Page Title:** My Inquiries
- **Element IDs:**
  - `inquiries-page` (div)
  - `inquiries-table` (table)
  - `inquiry-status-filter` (dropdown/select)
  - Dynamic ID: `delete-inquiry-button-{inquiry_id}` (button) for each inquiry
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `inquiries` (list of dict): Inquiry data with status
  - `status_filter` (str): Current selected filter
- **Navigation (flask url_for):**
  - Delete Inquiry Button: `url_for('delete_inquiry', inquiry_id=inquiry_id)`
  - Back to Dashboard Button: `url_for('dashboard_page')`
- **Forms:**
  - Inquiry Filter Form:
    - Input ID: `inquiry-status-filter`
    - Form action endpoint: `url_for('my_inquiries_page')` (GET or POST as implemented)
  - Delete Inquiry Form/Button:
    - Button ID: `delete-inquiry-button-{inquiry_id}`
    - Form action endpoint: `url_for('delete_inquiry', inquiry_id=inquiry_id)`
    - Method: POST

---

### 6. Template: my_favorites.html
- **Page Title:** My Favorite Properties
- **Element IDs:**
  - `favorites-page` (div)
  - `favorites-list` (div)
  - Dynamic IDs:
    - `remove-from-favorites-button-{property_id}` (button)
    - `view-property-button-{property_id}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `favorites` (list of dict): Favorite properties data
- **Navigation (flask url_for):**
  - Remove From Favorites Button: `url_for('remove_favorite', property_id=property_id)`
  - View Property Button: `url_for('property_details', property_id=property_id)`
  - Back to Dashboard Button: `url_for('dashboard_page')`
- **Forms:**
  - Remove Favorite Form/Button:
    - Button ID: `remove-from-favorites-button-{property_id}`
    - Form action endpoint: `url_for('remove_favorite', property_id=property_id)`
    - Method: POST

---

### 7. Template: agents.html
- **Page Title:** Real Estate Agents
- **Element IDs:**
  - `agents-page` (div)
  - `agents-list` (div)
  - `agent-search` (input)
  - Dynamic ID: `contact-agent-button-{agent_id}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `agents` (list of dict): Agents data
- **Navigation (flask url_for):**
  - Contact Agent Button: (no route provided for contacting agent, assumed mailto or external link)
  - Back to Dashboard Button: `url_for('dashboard_page')`
- **Forms:**
  - Agent Search Form (if implemented):
    - Input ID: `agent-search`
    - Form action endpoint: (not specified)
    - Method: GET

---

### 8. Template: locations.html
- **Page Title:** Featured Locations
- **Element IDs:**
  - `locations-page` (div)
  - `locations-list` (div)
  - Dynamic ID: `view-location-button-{location_id}` (button)
  - `location-sort` (dropdown/select)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `locations` (list of dict): Locations data
- **Navigation (flask url_for):**
  - View Location Button: `url_for('property_search')` (assumed showing filtered properties by location parameter; route accepts query string as optional)
  - Back to Dashboard Button: `url_for('dashboard_page')`
- **Forms:**
  - Location Sort Form:
    - Input ID: `location-sort`
    - Form action endpoint: `url_for('locations_page')`
    - Method: GET

---

## Section 3: Data File Schemas (Backend)

### 1. Properties Data
- **File Path:** `data/properties.txt`
- **Fields (pipe-delimited, in order):**
  - `property_id` (int)
  - `address` (str)
  - `location` (str)
  - `price` (float)
  - `property_type` (str)
  - `bedrooms` (int)
  - `bathrooms` (float)
  - `square_feet` (int)
  - `description` (str)
  - `agent_id` (int)
  - `status` (str) - e.g., Available, Sold
- **Description:** Stores all property listings with detailed attributes and agent association.
- **Example Rows:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. Locations Data
- **File Path:** `data/locations.txt`
- **Fields (pipe-delimited, in order):**
  - `location_id` (int)
  - `location_name` (str)
  - `region` (str)
  - `average_price` (float)
  - `property_count` (int)
  - `description` (str)
- **Description:** Contains location names with summary statistics and region data.
- **Example Rows:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. Property Inquiries Data
- **File Path:** `data/inquiries.txt`
- **Fields (pipe-delimited, in order):**
  - `inquiry_id` (int)
  - `property_id` (int)
  - `customer_name` (str)
  - `customer_email` (str)
  - `customer_phone` (str)
  - `message` (str)
  - `inquiry_date` (str, ISO date `YYYY-MM-DD`)
  - `status` (str) - e.g., Pending, Contacted, Resolved
- **Description:** Records user inquiries about properties and their status.
- **Example Rows:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. Favorite Properties Data
- **File Path:** `data/favorites.txt`
- **Fields (pipe-delimited, in order):**
  - `favorite_id` (int)
  - `property_id` (int)
  - `added_date` (str, ISO date `YYYY-MM-DD`)
- **Description:** Stores user-favorited properties and when added.
- **Example Rows:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. Real Estate Agents Data
- **File Path:** `data/agents.txt`
- **Fields (pipe-delimited, in order):**
  - `agent_id` (int)
  - `agent_name` (str)
  - `specialization` (str)
  - `email` (str)
  - `phone` (str)
  - `properties_sold` (int)
- **Description:** List of all real estate agents with contact info and performance data.
- **Example Rows:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```
