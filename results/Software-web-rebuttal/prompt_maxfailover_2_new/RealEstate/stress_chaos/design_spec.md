# RealEstate Flask Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Focus)

### Route 1: Dashboard
- URL Path: `/`
- HTTP Methods: `GET`
- Function Name: `dashboard`
- Behavior: Redirects root URL `/` to dashboard page `/dashboard`.

### Route 2: Dashboard Page
- URL Path: `/dashboard`
- HTTP Methods: `GET`
- Function Name: `dashboard_page`
- HTML Template: `dashboard.html`
- Context Variables:
  - `featured_properties` (list of dict): List of featured properties each dict containing: `property_id` (str), `address` (str), `price` (float), `property_type` (str), `bedrooms` (int), `bathrooms` (float), `square_feet` (int), `description` (str)
- Form Data: None

### Route 3: Property Search
- URL Path: `/search`
- HTTP Methods: `GET`, `POST`
- Function Name: `property_search`
- HTML Template: `search.html`
- Context Variables:
  - `properties` (list of dict): List of filtered properties with same fields as featured_properties
  - `filters` (dict): Search filters including keys - `location` (str), `price_min` (float), `price_max` (float), `property_type` (str)
- Form Data (POST):
  - `location` (str): Input location or city to filter
  - `price_min` (float): Minimum price filter
  - `price_max` (float): Maximum price filter
  - `property_type` (str): Property type filter (House, Apartment, Condo, Land)

### Route 4: Property Details
- URL Path: `/property/<property_id>`
- HTTP Methods: `GET`
- Function Name: `property_details`
- HTML Template: `property_details.html`
- Route Parameters:
  - `property_id` (str): Identifier of the property to view
- Context Variables:
  - `property` (dict): Property details including fields:
    - `property_id` (str)
    - `address` (str)
    - `location` (str)
    - `price` (float)
    - `property_type` (str)
    - `bedrooms` (int)
    - `bathrooms` (float)
    - `square_feet` (int)
    - `description` (str)
    - `agent_id` (str)
    - `status` (str)
- Form Data: None

### Route 5: Property Inquiry
- URL Path: `/inquiry`
- HTTP Methods: `GET`, `POST`
- Function Name: `property_inquiry`
- HTML Template: `inquiry.html`
- Context Variables:
  - `properties` (list of dict): List of all properties for selection
- Form Data (POST):
  - `selected_property` (str): Property ID selected for inquiry
  - `inquiry_name` (str): Customer name
  - `inquiry_email` (str): Customer email
  - `inquiry_phone` (str): Customer phone
  - `inquiry_message` (str): Message content

### Route 6: My Inquiries
- URL Path: `/inquiries`
- HTTP Methods: `GET`
- Function Name: `my_inquiries`
- HTML Template: `inquiries.html`
- Context Variables:
  - `inquiries` (list of dict): List of inquiries with fields:
    - `inquiry_id` (str)
    - `property_id` (str)
    - `property_address` (str)
    - `customer_name` (str)
    - `customer_email` (str)
    - `customer_phone` (str)
    - `message` (str)
    - `inquiry_date` (str, date in YYYY-MM-DD format)
    - `status` (str)
  - `status_filter` (str): Current filter status (All, Pending, Contacted, Resolved)
- Form Data: None

### Route 7: My Favorites
- URL Path: `/favorites`
- HTTP Methods: `GET`
- Function Name: `my_favorites`
- HTML Template: `favorites.html`
- Context Variables:
  - `favorites` (list of dict): List of favorite properties with fields matching properties
- Form Data: None

### Route 8: Agent Directory
- URL Path: `/agents`
- HTTP Methods: `GET`
- Function Name: `agent_directory`
- HTML Template: `agents.html`
- Context Variables:
  - `agents` (list of dict): List of agents with fields:
    - `agent_id` (str)
    - `agent_name` (str)
    - `specialization` (str)
    - `email` (str)
    - `phone` (str)
    - `properties_sold` (int)
- Form Data: None

### Route 9: Locations Page
- URL Path: `/locations`
- HTTP Methods: `GET`
- Function Name: `locations_page`
- HTML Template: `locations.html`
- Context Variables:
  - `locations` (list of dict): List of locations with fields:
    - `location_id` (str)
    - `location_name` (str)
    - `region` (str)
    - `average_price` (float)
    - `property_count` (int)
    - `description` (str)
- Form Data: None

---

## Section 2: HTML Templates Specification (Frontend Focus)

### dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - `dashboard-page` (Div - container)
  - `featured-properties` (Div - to display featured properties)
  - `browse-properties-button` (Button - navigate to `property_search`)
  - `my-inquiries-button` (Button - navigate to `my_inquiries`)
  - `my-favorites-button` (Button - navigate to `my_favorites`)
- Context Variables:
  - `featured_properties` (list of dict) as defined
- Navigation:
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('my_inquiries')
  - my-favorites-button: url_for('my_favorites')
- Forms: None

### search.html
- Page Title: Property Search
- Element IDs:
  - `search-page` (Div - container)
  - `location-input` (Input - string)
  - `price-range-min` (Input - number)
  - `price-range-max` (Input - number)
  - `property-type-filter` (Dropdown - options: House, Apartment, Condo, Land)
  - `properties-grid` (Div - container housing property cards)
  - `view-property-button-{property_id}` (Button - view details each property)
- Context Variables:
  - `properties` (list of dict)
  - `filters` (dict)
- Navigation:
  - Each view-property-button-*: url_for('property_details', property_id=property_id)
- Form:
  - Method: POST, action url_for('property_search')
  - Inputs: location-input, price-range-min, price-range-max, property-type-filter
  - Submit button: id `search-submit-button`

### property_details.html
- Page Title: Property Details
- Element IDs:
  - `property-details-page` (Div container)
  - `property-address` (H1 - property address)
  - `property-price` (Div - property price)
  - `property-description` (Div - description text)
  - `property-features` (Div - beds, baths, sqft display)
  - `add-to-favorites-button` (Button - add to favorites action)
  - `submit-inquiry-button` (Button - navigate to inquiry form)
- Context Variables:
  - `property` (dict)
- Navigation:
  - add-to-favorites-button: POST form to add to favorites endpoint, or AJAX
  - submit-inquiry-button: url_for('property_inquiry') with property preselected
- Form:
  - Add to favorites: POST, hidden input `property_id`
  - Submit Inquiry button navigates to inquiry form

### inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - `inquiry-page` (Div container)
  - `select-property` (Dropdown - property select)
  - `inquiry-name` (Input - text)
  - `inquiry-email` (Input - email)
  - `inquiry-phone` (Input - tel)
  - `inquiry-message` (Textarea)
  - `submit-inquiry-button` (Button - submit form)
- Context Variables:
  - `properties` (list of dict) for select dropdown
- Navigation: None
- Form:
  - POST to route `property_inquiry`
  - Inputs: select-property, inquiry-name, inquiry-email, inquiry-phone, inquiry-message
  - Submit Button with id `submit-inquiry-button`

### inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - `inquiries-page` (Div container)
  - `inquiries-table` (Table showing inquiries)
  - `inquiry-status-filter` (Dropdown - filter by status)
  - `delete-inquiry-button-{inquiry_id}` (Button - delete inquiry)
  - `back-to-dashboard` (Button - navigate to dashboard)
- Context Variables:
  - `inquiries` (list of dict)
  - `status_filter` (str)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')
- Form: None

### favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - `favorites-page` (Div container)
  - `favorites-list` (Div listing favorites)
  - `remove-from-favorites-button-{property_id}` (Button - remove favorite)
  - `view-property-button-{property_id}` (Button - view property)
  - `back-to-dashboard` (Button - navigate back)
- Context Variables:
  - `favorites` (list of dict)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')
- Form: None

### agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - `agents-page` (Div container)
  - `agents-list` (Div listing agents)
  - `agent-search` (Input - text for searching agents)
  - `contact-agent-button-{agent_id}` (Button - contact agent)
  - `back-to-dashboard` (Button - navigate back)
- Context Variables:
  - `agents` (list of dict)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')
- Form: None

### locations.html
- Page Title: Featured Locations
- Element IDs:
  - `locations-page` (Div container)
  - `locations-list` (Div listing locations)
  - `view-location-button-{location_id}` (Button - view location properties)
  - `location-sort` (Dropdown - sort locations)
  - `back-to-dashboard` (Button - navigate back)
- Context Variables:
  - `locations` (list of dict)
- Navigation:
  - back-to-dashboard: url_for('dashboard_page')
- Form:
  - location-sort dropdown with sorting options

---

## Section 3: Data File Schemas (Backend Data Handling)

### 3.1 properties.txt
- File Path: `data/properties.txt`
- Fields (pipe-delimited):
  - `property_id` (str): Unique property identifier
  - `address` (str): Property address
  - `location` (str): Location or city
  - `price` (float): Property price
  - `property_type` (str): Type of property (House, Apartment, Condo, Land)
  - `bedrooms` (int): Number of bedrooms
  - `bathrooms` (float): Number of bathrooms (can be fractional e.g., 1.5)
  - `square_feet` (int): Square footage
  - `description` (str): Property description
  - `agent_id` (str): Associated agent ID
  - `status` (str): Property status (Available, Sold, etc.)
- Example Rows:
```
1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
```

### 3.2 locations.txt
- File Path: `data/locations.txt`
- Fields (pipe-delimited):
  - `location_id` (str): Unique location identifier
  - `location_name` (str): Name of location
  - `region` (str): Geographic region
  - `average_price` (float): Average property price
  - `property_count` (int): Number of properties in location
  - `description` (str): Location description
- Example Rows:
```
1|Downtown|Central|425000|45|Urban area with business district
2|Midtown|Central|380000|38|Mixed residential and commercial zone
3|Suburb|Outskirts|295000|52|Family-friendly residential area
```

### 3.3 inquiries.txt
- File Path: `data/inquiries.txt`
- Fields (pipe-delimited):
  - `inquiry_id` (str): Unique inquiry identifier
  - `property_id` (str): Associated property ID
  - `customer_name` (str): Customer full name
  - `customer_email` (str): Customer email
  - `customer_phone` (str): Customer phone number
  - `message` (str): Inquiry message content
  - `inquiry_date` (str): Date of inquiry (YYYY-MM-DD)
  - `status` (str): Status of inquiry (Pending, Contacted, Resolved)
- Example Rows:
```
1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
```

### 3.4 favorites.txt
- File Path: `data/favorites.txt`
- Fields (pipe-delimited):
  - `favorite_id` (str): Unique favorite entry ID
  - `property_id` (str): Favorited property ID
  - `added_date` (str): Date added (YYYY-MM-DD)
- Example Rows:
```
1|1|2025-01-10
2|2|2025-01-12
3|3|2025-01-14
```

### 3.5 agents.txt
- File Path: `data/agents.txt`
- Fields (pipe-delimited):
  - `agent_id` (str): Unique agent identifier
  - `agent_name` (str): Full name of agent
  - `specialization` (str): Agent's area of expertise
  - `email` (str): Agent email
  - `phone` (str): Agent phone
  - `properties_sold` (int): Number of properties sold
- Example Rows:
```
101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
103|James Martinez|Luxury Homes|james@email.com|555-0003|67
```
