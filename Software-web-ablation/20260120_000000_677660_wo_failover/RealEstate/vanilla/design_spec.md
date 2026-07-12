# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | HTTP Method | Function Name           | Template Rendered         | Route Parameters         | Context Variables Passed to Template (name : type) | POST Form Data Expected (name : type)                                  |
|----------------------------|-------------|------------------------|---------------------------|--------------------------|-----------------------------------------------------|---------------------------------------------------------------------------|
| /                          | GET         | root_redirect           | -                         | -                        | -                                                   | -                                                                         |
| /dashboard                 | GET         | dashboard              | dashboard.html            | -                        | featured_properties : list(dict), recent_listings : list(dict)          | -                                                                         |
| /search                   | GET         | property_search        | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict   | -                                                                         |
| /search                   | POST        | property_search_post   | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict   | location_input : str, price_range_min : int, price_range_max : int, property_type_filter : str |
| /property/<int:property_id> | GET         | property_details       | property_details.html     | property_id               | property : dict, agent : dict, is_favorite : bool                        | -                                                                         |
| /property/<int:property_id>/favorite | POST        | add_to_favorites       | property_details.html     | property_id               | property : dict, agent : dict, is_favorite : bool                        | -                                                                         |
| /inquiry                  | GET         | inquiry_form           | inquiry.html              | -                        | properties : list(dict)                                               | -                                                                         |
| /inquiry                  | POST        | submit_inquiry         | inquiry.html              | -                        | properties : list(dict), submission_success : bool                      | property_id : int, inquiry_name : str, inquiry_email : str, inquiry_phone : str, inquiry_message : str |
| /inquiries                | GET         | my_inquiries           | inquiries.html            | -                        | inquiries : list(dict)                                                | -                                                                         |
| /inquiries/delete/<int:inquiry_id> | POST        | delete_inquiry         | inquiries.html            | inquiry_id                | inquiries : list(dict)                                                | -                                                                         |
| /favorites                | GET         | my_favorites           | favorites.html            | -                        | favorite_properties : list(dict)                                     | -                                                                         |
| /favorites/remove/<int:property_id> | POST        | remove_favorite        | favorites.html            | property_id               | favorite_properties : list(dict)                                     | -                                                                         |
| /agents                  | GET         | agents_directory       | agents.html               | -                        | agents : list(dict)                                                 | -                                                                         |
| /agents/search            | POST        | agents_search          | agents.html               | -                        | agents : list(dict)                                                 | agent_search_query : str                                                    |
| /locations               | GET         | locations_page         | locations.html            | -                        | locations : list(dict), sort_option : str                           | -                                                                         |
| /locations/sort           | POST        | sort_locations         | locations.html            | -                        | locations : list(dict), sort_option : str                           | location_sort : str                                                        |

- **root_redirect**: Redirects from '/' to '/dashboard'.

- All list(dict) context variables contain dictionaries with keys matching data file schemas or combined data as necessary for UI rendering.


---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-properties (Div)
  - browse-properties-button (Button)
  - my-inquiries-button (Button)
  - my-favorites-button (Button)

- Context Variables:
  - featured_properties: list of property dicts (Each dict includes: property_id, address, location, price, property_type, bedrooms, bathrooms)
  - recent_listings: list of property dicts (Similar structure as featured_properties)

- Navigation (using url_for):
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('my_inquiries')
  - my-favorites-button: url_for('my_favorites')

- No forms on this page.


### 2. search.html
- Page Title: Property Search
- Element IDs:
  - search-page (Div)
  - location-input (Input)
  - price-range-min (Input number)
  - price-range-max (Input number)
  - property-type-filter (Dropdown)
  - properties-grid (Div)
  - view-property-button-{property_id} (Button) for each property card

- Context Variables:
  - properties: list of property dicts (Each dict with keys matching properties.txt fields)
  - locations: list of location dicts
  - filter_options: dict with keys: selected_location (str), price_min (int), price_max (int), property_type (str)

- Navigation:
  - Each view-property-button-{property_id}: url_for('property_details', property_id=property_id)

- Forms:
  - Search form with inputs: location-input, price-range-min, price-range-max, property-type-filter
  - Form submits (POST) to url_for('property_search_post')
  - Submit button: ID='search-submit-button' (Button)


### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (Div)
  - property-address (H1)
  - property-price (Div)
  - property-description (Div)
  - property-features (Div)
  - add-to-favorites-button (Button)
  - submit-inquiry-button (Button)

- Context Variables:
  - property: dict (fields as per properties.txt)
  - agent: dict (fields as per agents.txt)
  - is_favorite: bool

- Navigation:
  - add-to-favorites-button POSTs to url_for('add_to_favorites', property_id=property['property_id'])
  - submit-inquiry-button directs to url_for('inquiry_form') with default property selected

- Forms:
  - Add to favorites button (form with POST method)
  - Submit inquiry button (link or button directing to inquiry page)


### 4. inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (Div)
  - select-property (Dropdown)
  - inquiry-name (Input)
  - inquiry-email (Input email)
  - inquiry-phone (Input tel)
  - inquiry-message (Textarea)
  - submit-inquiry-button (Button)

- Context Variables:
  - properties: list of property dicts
  - submission_success: bool (optional, shows confirmation message if True)

- Navigation:
  - Back to dashboard via url_for('dashboard') (Implicit or explicit link/button)

- Forms:
  - Inquiry submission form (POST to url_for('submit_inquiry')) with inputs:
    - select-property
    - inquiry-name
    - inquiry-email
    - inquiry-phone
    - inquiry-message
  - Submit button id='submit-inquiry-button'


### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (Div)
  - inquiries-table (Table)
  - inquiry-status-filter (Dropdown)
  - delete-inquiry-button-{inquiry_id} (Button) for each inquiry
  - back-to-dashboard (Button)

- Context Variables:
  - inquiries: list of inquiry dicts

- Navigation:
  - back-to-dashboard button navigates to url_for('dashboard')

- Forms:
  - Inquiry status filter form (possibly GET or POST to same route) with inquiry-status-filter dropdown
  - Delete inquiry buttons submit POST to url_for('delete_inquiry', inquiry_id=inquiry_id)


### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (Div)
  - favorites-list (Div)
  - remove-from-favorites-button-{property_id} (Button) for each favorite property
  - view-property-button-{property_id} (Button) for each favorite property
  - back-to-dashboard (Button)

- Context Variables:
  - favorite_properties: list of property dicts

- Navigation:
  - back-to-dashboard button: url_for('dashboard')
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)

- Forms:
  - Remove from favorites buttons POST to url_for('remove_favorite', property_id=property_id)


### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (Div)
  - agents-list (Div)
  - agent-search (Input)
  - contact-agent-button-{agent_id} (Button) for each agent
  - back-to-dashboard (Button)

- Context Variables:
  - agents: list of agent dicts

- Navigation:
  - back-to-dashboard button: url_for('dashboard')

- Forms:
  - Agent search form (POST) with agent-search input, submits to url_for('agents_search')


### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (Div)
  - locations-list (Div)
  - view-location-button-{location_id} (Button) for each location
  - location-sort (Dropdown)
  - back-to-dashboard (Button)

- Context Variables:
  - locations: list of location dicts
  - sort_option: str

- Navigation:
  - back-to-dashboard button: url_for('dashboard')
  - view-location-button-{location_id}: url_for('search') filtered by location

- Forms:
  - Location sort form (POST) with location-sort dropdown, submits to url_for('sort_locations')


---

## Section 3: Data File Schemas (Backend)

### 3.1 properties.txt
- File Path: data/properties.txt
- Fields (pipe-delimited):
  - property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description: Stores detailed information about each property listing available in the system.
- Example Rows:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 3.2 locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited):
  - location_id|location_name|region|average_price|property_count|description
- Description: Contains information about popular locations for filtering and display.
- Example Rows:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3.3 inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited):
  - inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description: Records all customer inquiries submitted for properties.
- Example Rows:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 3.4 favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited):
  - favorite_id|property_id|added_date
- Description: Stores user's favorite properties.
- Example Rows:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 3.5 agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited):
  - agent_id|agent_name|specialization|email|phone|properties_sold
- Description: Contains information on real estate agents.
- Example Rows:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
