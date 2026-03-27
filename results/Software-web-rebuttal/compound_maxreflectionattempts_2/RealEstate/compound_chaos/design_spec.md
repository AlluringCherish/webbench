# RealEstate Application Design Specification

---

## Section 1: Flask Routes and HTTP Methods (Backend)

| Route | HTTP Method(s) | Function Name | Template Rendered | Context Variables | POST Form Inputs |
|-------|----------------|---------------|-------------------|-------------------|------------------|
| `/` | GET | root_redirect | None (redirects to dashboard) | None | None |
| `/dashboard` | GET | dashboard | dashboard.html |
- featured_properties: list of dict
- recent_listings: list of dict | None |
| `/search` | GET, POST | property_search | search.html |
- properties: list of dict
- locations: list of dict
- applied_filters: dict (keys: location:str, price_min:int or None, price_max:int or None, property_type:str or None) | (POST):
- location_input: str (from `location-input`)
- price_range_min: int or empty (from `price-range-min`)
- price_range_max: int or empty (from `price-range-max`)
- property_type_filter: str (House, Apartment, Condo, Land, or empty) |
| `/property/<int:property_id>` | GET | property_details | property_details.html |
- property: dict
- agent: dict | None |
| `/inquiry` | GET, POST | property_inquiry | inquiry.html |
- properties: list of dict
- form_errors: dict (optional) | (POST):
- select_property: int (property_id)
- inquiry_name: str
- inquiry_email: str (email format)
- inquiry_phone: str
- inquiry_message: str |
| `/inquiries` | GET, POST | my_inquiries | inquiries.html |
- inquiries: list of dict
- inquiry_status_filter: str (All, Pending, Contacted, Resolved) | (POST):
- inquiry_status_filter: str (dropdown selection)
- delete_inquiry_id: int (from `delete-inquiry-button-{inquiry_id}` button, if deleting) |
| `/favorites` | GET, POST | my_favorites | favorites.html |
- favorites: list of dict
- properties_map: dict (property_id:int -> dict) for quick property data lookup | (POST):
- action: str ('add' or 'remove')
- property_id: int |
| `/agents` | GET | agents_directory | agents.html |
- agents: list of dict | None |
| `/locations` | GET | locations | locations.html |
- locations: list of dict
- sort_by: str ('name', 'properties_count', 'average_price') | (POST):
- location_sort: str |


## Section 2: HTML Templates (Frontend)

### 1. `/dashboard` - dashboard.html
- Page Title and &lt;h1&gt;: "Real Estate Dashboard"
- Element IDs:
  - dashboard-page (Div container)
  - featured-properties (Div showing featured properties)
  - browse-properties-button (Button to navigate to property search page)
  - my-inquiries-button (Button to navigate to inquiries page)
  - my-favorites-button (Button to navigate to favorites page)
- Context Variables:
  - featured_properties (list of dict): List of featured property data
  - recent_listings (list of dict): List of recent property listings
- Navigation Links (via buttons with JS or links):
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('my_inquiries')
  - my-favorites-button: url_for('my_favorites')
- Forms: None

### 2. `/search` - search.html
- Page Title and &lt;h1&gt;: "Property Search"
- Element IDs:
  - search-page (Div container)
  - location-input (Input text)
  - price-range-min (Input number)
  - price-range-max (Input number)
  - property-type-filter (Dropdown)
  - properties-grid (Div grid containing property cards)
  - view-property-button-{property_id} (Button for each property card)
- Context Variables:
  - properties (list of dict): List of properties matching filters
  - locations (list of dict): List of available locations
  - applied_filters (dict): Current filters applied
- Navigation Links:
  - None explicit (user navigates, or uses buttons elsewhere)
- Forms:
  - Search/filter form with method POST:
    - location-input (text input)
    - price-range-min (number input)
    - price-range-max (number input)
    - property-type-filter (dropdown)
    - Submit button with ID: search-submit-button

### 3. `/property/<int:property_id>` - property_details.html
- Page Title and &lt;h1&gt;: "Property Details"
- Element IDs:
  - property-details-page (Div container)
  - property-address (H1 showing property address)
  - property-price (Div showing price)
  - property-description (Div showing description)
  - property-features (Div showing bedrooms, bathrooms, square footage)
  - add-to-favorites-button (Button to add to favorites)
  - submit-inquiry-button (Button to submit inquiry for this property)
- Context Variables:
  - property (dict): Detailed property data
  - agent (dict): Agent data associated with property
- Navigation Links:
  - None explicit
- Forms:
  - None explicit; buttons trigger actions typically via POST or JS

### 4. `/inquiry` - inquiry.html
- Page Title and &lt;h1&gt;: "Submit Property Inquiry"
- Element IDs:
  - inquiry-page (Div container)
  - select-property (Dropdown to select property)
  - inquiry-name (Text input)
  - inquiry-email (Email input)
  - inquiry-phone (Tel input)
  - inquiry-message (Textarea)
  - submit-inquiry-button (Submit button for form)
- Context Variables:
  - properties (list of dict): Available properties for inquiry
  - form_errors (dict, optional): Validation errors keyed by field
- Navigation Links:
  - None explicit
- Forms:
  - Inquiry submission form (method POST, action `/inquiry`):
    - select-property (dropdown)
    - inquiry-name (input text)
    - inquiry-email (input email)
    - inquiry-phone (input tel)
    - inquiry-message (textarea)
    - submit-inquiry-button (button)

### 5. `/inquiries` - inquiries.html
- Page Title and &lt;h1&gt;: "My Inquiries"
- Element IDs:
  - inquiries-page (Div container)
  - inquiries-table (Table listing inquiries)
  - inquiry-status-filter (Dropdown to filter inquiries)
  - delete-inquiry-button-{inquiry_id} (Button for each inquiry to delete)
  - back-to-dashboard (Button to go back)
- Context Variables:
  - inquiries (list of dict): User inquiries
  - inquiry_status_filter (str): Currently applied status filter
- Navigation Links:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Filter form (method POST):
    - inquiry-status-filter (dropdown)
    - Submit button with id: filter-inquiries-submit
  - Delete buttons (form or AJAX POST) with hidden input delete_inquiry_id

### 6. `/favorites` - favorites.html
- Page Title and &lt;h1&gt;: "My Favorite Properties"
- Element IDs:
  - favorites-page (Div container)
  - favorites-list (Div listing all favorite properties)
  - remove-from-favorites-button-{property_id} (Button to remove each favorite)
  - view-property-button-{property_id} (Button to view property details)
  - back-to-dashboard (Button to go back)
- Context Variables:
  - favorites (list of dict): Favorite entries
  - properties_map (dict): property_id to property dict mapping
- Navigation Links:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Remove favorite forms (POST):
    - property_id as hidden input
    - remove-from-favorites-button-{property_id} as submit button

### 7. `/agents` - agents.html
- Page Title and &lt;h1&gt;: "Real Estate Agents"
- Element IDs:
  - agents-page (Div container)
  - agents-list (Div listing all agents)
  - agent-search (Input text for search)
  - contact-agent-button-{agent_id} (Button to contact each agent)
  - back-to-dashboard (Button to go back)
- Context Variables:
  - agents (list of dict): Agent data
- Navigation Links:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Agent search may be a GET or JS filtered without form

### 8. `/locations` - locations.html
- Page Title and &lt;h1&gt;: "Featured Locations"
- Element IDs:
  - locations-page (Div container)
  - locations-list (Div listing locations)
  - view-location-button-{location_id} (Button to view properties in location)
  - location-sort (Dropdown to sort locations)
  - back-to-dashboard (Button to go back)
- Context Variables:
  - locations (list of dict): Location entries
  - sort_by (str): Current sort setting
- Navigation Links:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Sort form (POST or GET):
    - location-sort (dropdown)
    - Submit button with id: sort-locations-submit


## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File Path: data/properties.txt
- Fields (pipe-delimited in order):
  - property_id (int)
  - address (str)
  - location (str)
  - price (int)
  - property_type (str)
  - bedrooms (int)
  - bathrooms (float)
  - square_feet (int)
  - description (str)
  - agent_id (int)
  - status (str)
- Purpose: Stores all property listings with attributes and status.
- Examples:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited in order):
  - location_id (int)
  - location_name (str)
  - region (str)
  - average_price (int)
  - property_count (int)
  - description (str)
- Purpose: Contains popular locations information, property count and average price.
- Examples:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited in order):
  - inquiry_id (int)
  - property_id (int)
  - customer_name (str)
  - customer_email (str)
  - customer_phone (str)
  - message (str)
  - inquiry_date (str, format YYYY-MM-DD)
  - status (str) (Pending, Contacted, Resolved)
- Purpose: Stores customer inquiries about properties with status tracking.
- Examples:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited in order):
  - favorite_id (int)
  - property_id (int)
  - added_date (str, format YYYY-MM-DD)
- Purpose: Stores user's favorite properties.
- Examples:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited in order):
  - agent_id (int)
  - agent_name (str)
  - specialization (str)
  - email (str)
  - phone (str)
  - properties_sold (int)
- Purpose: Stores real estate agent contact and specialization data.
- Examples:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

This design specification fulfills all requirements for independent backend and frontend development for the RealEstate Flask web application. Function names and element IDs are precisely as specified for consistency.

