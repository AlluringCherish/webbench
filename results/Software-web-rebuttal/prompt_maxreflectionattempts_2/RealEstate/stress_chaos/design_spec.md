# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                        | HTTP Method(s) | Function Name           | Template Rendered       | Context Variables (name:type)                                                            | Form Data (POST)                                           |
|---------------------------------|----------------|------------------------|-------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                               | GET            | root_redirect           | None (redirects to dashboard) | None                                                                                     | None                                                       |
| /dashboard                      | GET            | dashboard              | dashboard.html          | featured_properties: list (of dict with keys: property_id:int, address:str, price:float,...), recent_listings: list (dict),  | None                                                       |
| /search                        | GET, POST      | property_search        | search.html             | properties: list (dict), filters: dict (keys: location:str, price_min:int, price_max:int, property_type:str)                    | (POST) location:str, price_min:int, price_max:int, property_type:str |
| /property/<int:property_id>    | GET            | property_details       | property_details.html   | property: dict (property details), is_favorite: bool                                     | None                                                       |
| /inquiry                      | GET, POST      | property_inquiry       | inquiry.html            | properties: list (dict with property_id, address)                                        | (POST) property_id:int, customer_name:str, customer_email:str, customer_phone:str, message:str |
| /inquiries                   | GET, POST      | my_inquiries           | inquiries.html          | inquiries: list (dict), status_filter: str                                               | (POST) inquiry_id:int (for deletion)                       |
| /favorites                   | GET, POST      | my_favorites           | favorites.html          | favorites: list (dict), properties_map: dict (property_id:int -> dict of property details) | (POST) action:str ('remove'), property_id:int              |
| /agents                     | GET            | agent_directory        | agents.html             | agents: list (dict)                                                                       | None                                                       |
| /locations                  | GET            | locations_page         | locations.html          | locations: list (dict), sort_by: str                                                     | None                                                       |

---

## Section 2: HTML Templates (Frontend)

### dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page
  - featured-properties
  - browse-properties-button
  - my-inquiries-button
  - my-favorites-button
- Context Variables:
  - featured_properties (list of dict): List of featured property details
  - recent_listings (list of dict): List of recent properties
- Navigation:
  - browse-properties-button => url_for('property_search')
  - my-inquiries-button => url_for('my_inquiries')
  - my-favorites-button => url_for('my_favorites')
- Forms: None

### search.html
- Page Title: Property Search
- Element IDs:
  - search-page
  - location-input
  - price-range-min
  - price-range-max
  - property-type-filter
  - properties-grid
  - view-property-button-{property_id} (dynamic)
- Context Variables:
  - properties (list of dict): List of properties matching search
  - filters (dict): Current applied filters
- Navigation:
  - view-property-button-{property_id} => url_for('property_details', property_id=property_id)
- Forms:
  - Search form with inputs: location-input, price-range-min, price-range-max, property-type-filter
    Submit action: url_for('property_search')

### property_details.html
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
  - property (dict): Full property details
  - is_favorite (bool): Whether current property is in favorites
- Navigation:
  - add-to-favorites-button => POST to route for adding to favorites (if implemented separately)
  - submit-inquiry-button => url_for('property_inquiry')
- Forms:
  - None or add to favorites POST form button

### inquiry.html
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
  - properties (list of dict): Properties available for inquiry
- Navigation:
  - submit-inquiry-button => POST to property_inquiry route
- Forms:
  - Inquiry submission form with fields: select-property, inquiry-name, inquiry-email, inquiry-phone, inquiry-message
    Submit action: url_for('property_inquiry')

### inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page
  - inquiries-table
  - inquiry-status-filter
  - delete-inquiry-button-{inquiry_id} (dynamic)
  - back-to-dashboard
- Context Variables:
  - inquiries (list of dict): List of inquiries
  - status_filter (str): Current status filter value
- Navigation:
  - delete-inquiry-button-{inquiry_id} => POST to my_inquiries route
  - back-to-dashboard => url_for('dashboard')
- Forms:
  - Status filter form with inquiry-status-filter dropdown
  - Delete buttons POST form with inquiry_id

### favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page
  - favorites-list
  - remove-from-favorites-button-{property_id} (dynamic)
  - view-property-button-{property_id} (dynamic)
  - back-to-dashboard
- Context Variables:
  - favorites (list of dict): List of favorite entries
  - properties_map (dict): Mapping property_id to property details
- Navigation:
  - remove-from-favorites-button-{property_id} => POST to my_favorites route
  - view-property-button-{property_id} => url_for('property_details', property_id=property_id)
  - back-to-dashboard => url_for('dashboard')
- Forms:
  - Remove from favorites form/button

### agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page
  - agents-list
  - agent-search
  - contact-agent-button-{agent_id} (dynamic)
  - back-to-dashboard
- Context Variables:
  - agents (list of dict): List of agents
- Navigation:
  - contact-agent-button-{agent_id} => mailto link or contact form
  - back-to-dashboard => url_for('dashboard')
- Forms:
  - Agent search form (optional)

### locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page
  - locations-list
  - view-location-button-{location_id} (dynamic)
  - location-sort
  - back-to-dashboard
- Context Variables:
  - locations (list of dict): List of locations
  - sort_by (str): Current sort criteria
- Navigation:
  - view-location-button-{location_id} => url_for('property_search', location=location_name)
  - back-to-dashboard => url_for('dashboard')
- Forms:
  - Sort dropdown form with location-sort

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File Path: data/properties.txt
- Fields (pipe-delimited):
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description: Stores all property listings with detailed information including location, price, agent reference, and availability status.
- Example Rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### 2. locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited):
  location_id|location_name|region|average_price|property_count|description
- Description: Contains information about various locations with their region, average property price, count, and description.
- Example Rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited):
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description: Records all property inquiries submitted by users including their contact details, message, and current status.
- Example Rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### 4. favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited):
  favorite_id|property_id|added_date
- Description: Stores user's favorite properties identified by property ID and the date they were added.
- Example Rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

### 5. agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited):
  agent_id|agent_name|specialization|email|phone|properties_sold
- Description: Contains details of real estate agents, their specialization, contact information, and number of properties sold.
- Example Rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67

