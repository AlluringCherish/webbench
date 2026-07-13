# RealEstate Web Application Design Specification

---

## 1. Flask Routes

| Route Path                     | Function Name          | HTTP Methods | Description                                           |
|-------------------------------|-----------------------|--------------|-------------------------------------------------------|
| `/`                           | dashboard             | GET          | Display Dashboard page                                |
| `/search`                     | property_search       | GET          | Display Property Search page with filters            |
| `/property/<int:property_id>` | property_details      | GET          | Display details for specific property                 |
| `/inquiry/submit`             | property_inquiry      | GET, POST    | Display and submit property inquiry form             |
| `/inquiries`                  | my_inquiries          | GET          | Display list of user inquiries                        |
| `/inquiries/delete/<int:inquiry_id>` | delete_inquiry       | POST         | Delete a specific inquiry                             |
| `/favorites`                  | my_favorites          | GET          | Display favorite properties                           |
| `/favorites/remove/<int:property_id>` | remove_favorite       | POST         | Remove a property from favorites                     |
| `/agents`                    | agent_directory       | GET          | Display list of real estate agents                    |
| `/locations`                 | locations_page        | GET          | Display featured locations page                       |


## 2. Page Titles and Template Filenames

| Page Name             | Page Title                  | Template Filename          |
|-----------------------|-----------------------------|----------------------------|
| Dashboard             | Real Estate Dashboard         | dashboard.html             |
| Property Search       | Property Search              | property_search.html       |
| Property Details      | Property Details            | property_details.html      |
| Property Inquiry      | Submit Property Inquiry      | property_inquiry.html      |
| My Inquiries          | My Inquiries                | my_inquiries.html          |
| My Favorites          | My Favorite Properties       | my_favorites.html          |
| Agent Directory       | Real Estate Agents           | agent_directory.html       |
| Locations Page        | Featured Locations           | locations.html             |


## 3. Element IDs

### Dashboard Page
- dashboard-page (Div container)
- featured-properties (Div)
- browse-properties-button (Button)
- my-inquiries-button (Button)
- my-favorites-button (Button)

### Property Search Page
- search-page (Div container)
- location-input (Input)
- price-range-min (Input number)
- price-range-max (Input number)
- property-type-filter (Dropdown)
- properties-grid (Div)
- view-property-button-{property_id} (Button, dynamic per property)

### Property Details Page
- property-details-page (Div container)
- property-address (H1)
- property-price (Div)
- property-description (Div)
- property-features (Div)
- add-to-favorites-button (Button)
- submit-inquiry-button (Button)

### Property Inquiry Page
- inquiry-page (Div container)
- select-property (Dropdown)
- inquiry-name (Input)
- inquiry-email (Input email)
- inquiry-phone (Input tel)
- inquiry-message (Textarea)
- submit-inquiry-button (Button)

### My Inquiries Page
- inquiries-page (Div container)
- inquiries-table (Table)
- inquiry-status-filter (Dropdown)
- delete-inquiry-button-{inquiry_id} (Button, dynamic per inquiry)
- back-to-dashboard (Button)

### My Favorites Page
- favorites-page (Div container)
- favorites-list (Div)
- remove-from-favorites-button-{property_id} (Button, dynamic per property)
- view-property-button-{property_id} (Button, dynamic per property)
- back-to-dashboard (Button)

### Agent Directory Page
- agents-page (Div container)
- agents-list (Div)
- agent-search (Input)
- contact-agent-button-{agent_id} (Button, dynamic per agent)
- back-to-dashboard (Button)

### Locations Page
- locations-page (Div container)
- locations-list (Div)
- view-location-button-{location_id} (Button, dynamic per location)
- location-sort (Dropdown)
- back-to-dashboard (Button)


## 4. Context Variables for Templates

### Dashboard (`dashboard.html`)
- featured_properties: list of dicts with keys: property_id, address, location, price, property_type, bedrooms, bathrooms, square_feet, description, agent_id, status

### Property Search (`property_search.html`)
- properties: list of dicts as above
- filters: dict with keys: location (str), price_min (int), price_max (int), property_type (str)

### Property Details (`property_details.html`)
- property: dict as above for one property
- is_favorite: bool indicating if the property is in favorites

### Property Inquiry (`property_inquiry.html`)
- properties: list of dicts as above for selection dropdown
- submission_status: str or None (success or error message after form submission)

### My Inquiries (`my_inquiries.html`)
- inquiries: list of dicts with keys: inquiry_id, property_id, property_address (str), customer_name, customer_email, customer_phone, message, inquiry_date (str), status
- filter_status: str (selected filter status)

### My Favorites (`my_favorites.html`)
- favorites: list of dicts with keys: favorite_id, property_id, address, price, added_date

### Agent Directory (`agent_directory.html`)
- agents: list of dicts with keys: agent_id, agent_name, specialization, email, phone, properties_sold
- search_query: str (current search input)

### Locations (`locations.html`)
- locations: list of dicts with keys: location_id, location_name, region, average_price, property_count, description
- sort_option: str (current sort option)


## 5. Data File Storage Formats

### Properties Data (`data/properties.txt`)
- Delimiter: `|`
- Fields (order): property_id (int), address (str), location (str), price (int), property_type (str), bedrooms (int), bathrooms (float), square_feet (int), description (str), agent_id (int), status (str)
- Description: Stores all property listings data.

### Locations Data (`data/locations.txt`)
- Delimiter: `|`
- Fields (order): location_id (int), location_name (str), region (str), average_price (int), property_count (int), description (str)
- Description: Stores information about locations.

### Property Inquiries Data (`data/inquiries.txt`)
- Delimiter: `|`
- Fields (order): inquiry_id (int), property_id (int), customer_name (str), customer_email (str), customer_phone (str), message (str), inquiry_date (str, YYYY-MM-DD), status (str)
- Description: Stores inquiries made by customers for properties.

### Favorite Properties Data (`data/favorites.txt`)
- Delimiter: `|`
- Fields (order): favorite_id (int), property_id (int), added_date (str, YYYY-MM-DD)
- Description: Stores user-favorited properties.

### Real Estate Agents Data (`data/agents.txt`)
- Delimiter: `|`
- Fields (order): agent_id (int), agent_name (str), specialization (str), email (str), phone (str), properties_sold (int)
- Description: Stores agent contact and specialization details.

---

This detailed design specification provides a comprehensive map for developing the RealEstate web application, including all routes, page structures, context data contracts, and data file schemas required for independent implementation.

