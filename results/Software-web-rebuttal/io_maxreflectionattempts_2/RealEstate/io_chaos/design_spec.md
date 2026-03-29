# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                        | HTTP Method(s) | Function Name           | Template Rendered       | Context Variables (name:type)                                                            | Form Data (POST)                                           |
|---------------------------------|----------------|------------------------|-------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                               | GET            | root_redirect           | None (redirects to dashboard) | None                                                                                     | None                                                       |
| /dashboard                      | GET            | dashboard              | dashboard.html          | featured_properties: list (of dict), recent_listings: list (of dict)                      | None                                                       |
| /search                        | GET, POST      | property_search        | search.html             | properties: list (dict), location_filter: str, price_min: int or float, price_max: int or float, property_type_filter: str | POST parameters: location_input (str), price_range_min (int/float), price_range_max (int/float), property_type_filter (str) |
| /property/<int:property_id>    | GET            | property_details       | property_details.html   | property: dict, agent: dict                                                                 | None                                                       |
| /inquiry                      | GET, POST      | submit_inquiry         | inquiry.html            | properties: list (dict)                                                                   | POST parameters: select_property (int), inquiry_name (str), inquiry_email (str), inquiry_phone (str), inquiry_message (str) |
| /inquiries                   | GET, POST      | my_inquiries           | inquiries.html          | inquiries: list (dict), status_filter: str                                                | POST parameters (for deletion): inquiry_id (int)           |
| /favorites                   | GET, POST      | my_favorites           | favorites.html          | favorites: list (dict), properties_map: dict (property_id:int -> dict)                   | POST parameters (for remove): property_id (int)             |
| /agents                     | GET            | agent_directory        | agents.html             | agents: list (dict), agent_search_query: str                                              | None                                                       |
| /locations                  | GET, POST      | locations_page         | locations.html          | locations: list (dict), sort_option: str                                                  | POST parameters: location_sort (str)                        |


---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page
  - featured-properties
  - browse-properties-button
  - my-inquiries-button
  - my-favorites-button
- Context Variables:
  - featured_properties: list of dict (properties to feature, each dict contains property details)
  - recent_listings: list of dict (recent property listings)
- Navigation Mappings:
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('my_inquiries')
  - my-favorites-button: url_for('my_favorites')
- Forms:
  - None

### 2. search.html
- Page Title: Property Search
- Element IDs:
  - search-page
  - location-input
  - price-range-min
  - price-range-max
  - property-type-filter
  - properties-grid
  - view-property-button-{property_id} (dynamic per property)
- Context Variables:
  - properties: list of dict (all property listings after filter/search)
  - location_filter: str (current search text)
  - price_min: int or float (current minimum price filter)
  - price_max: int or float (current maximum price filter)
  - property_type_filter: str (current selected property type filter)
- Navigation Mappings:
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)
- Forms:
  - Search form (POST to property_search):
    - location-input (text input)
    - price-range-min (number input)
    - price-range-max (number input)
    - property-type-filter (dropdown)
    - Submit button (could be implicit on filter change or explicit)

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page
  - property-address
  - property-price
  - property-description
  - property-features
  - add-to-favorites-button
  - submit-inquiry-button
- Context Variables:
  - property: dict (all property details)
  - agent: dict (agent details associated with property)
- Navigation Mappings:
  - add-to-favorites-button: POST to my_favorites route (to add)
  - submit-inquiry-button: redirects to submit_inquiry page with selected property
- Forms:
  - Add to favorites form (POST):
    - Hidden input: property_id
    - Submit button: add-to-favorites-button
  - Inquiry submission is link/button redirect (no form in this page)

### 4. inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page
  - select-property
  - inquiry-name
  - inquiry-email
  - inquiry-phone
  - inquiry-message
  - submit-inquiry-button
- Context Variables:
  - properties: list of dict (to populate select-property dropdown)
- Navigation Mappings:
  - No navigation buttons specified
- Forms:
  - Inquiry submission form (POST to submit_inquiry):
    - select-property (dropdown)
    - inquiry-name (text input)
    - inquiry-email (email input)
    - inquiry-phone (tel input)
    - inquiry-message (textarea)
    - submit button: submit-inquiry-button

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page
  - inquiries-table
  - inquiry-status-filter
  - delete-inquiry-button-{inquiry_id} (dynamic per inquiry)
  - back-to-dashboard
- Context Variables:
  - inquiries: list of dict (all inquiries or filtered by status)
  - status_filter: str (current selected status filter)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Delete inquiry form (POST to my_inquiries):
    - inquiry_id (hidden or from button context)
    - delete button: delete-inquiry-button-{inquiry_id}

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page
  - favorites-list
  - remove-from-favorites-button-{property_id} (dynamic per favorite property)
  - view-property-button-{property_id} (dynamic per favorite property)
  - back-to-dashboard
- Context Variables:
  - favorites: list of dict (favorite entries mapping to property_ids)
  - properties_map: dict mapping property_id (int) to property dict - to render details
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)
- Forms:
  - Remove favorite form (POST to my_favorites):
    - property_id (hidden input)
    - submit button: remove-from-favorites-button-{property_id}

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page
  - agents-list
  - agent-search
  - contact-agent-button-{agent_id} (dynamic per agent)
  - back-to-dashboard
- Context Variables:
  - agents: list of dict (all agents)
  - agent_search_query: str (search input value)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Agent search form (GET or POST to agent_directory):
    - agent-search (text input)
    - submit button (if applicable)

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page
  - locations-list
  - view-location-button-{location_id} (dynamic per location)
  - location-sort
  - back-to-dashboard
- Context Variables:
  - locations: list of dict (all locations)
  - sort_option: str (current sort selection)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Location sort form (POST to locations_page):
    - location-sort (dropdown)
    - submit button

---

## Section 3: Data File Schemas (Backend)

### 1. data/properties.txt
- Fields (pipe-delimited): 
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description: Stores all properties with details including location, pricing, features, agent assignment, and availability status.
- Example rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### 2. data/locations.txt
- Fields (pipe-delimited):
  location_id|location_name|region|average_price|property_count|description
- Description: Stores popular locations with property counts and average prices.
- Example rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

### 3. data/inquiries.txt
- Fields (pipe-delimited):
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description: Stores inquiries made by customers with contact and status information.
- Example rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### 4. data/favorites.txt
- Fields (pipe-delimited):
  favorite_id|property_id|added_date
- Description: Stores user favorite properties with date added.
- Example rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

### 5. data/agents.txt
- Fields (pipe-delimited):
  agent_id|agent_name|specialization|email|phone|properties_sold
- Description: Stores real estate agents with contact info and sales count.
- Example rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
