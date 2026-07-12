# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes and HTTP Methods (Backend)

| Route Path                     | HTTP Method | Function Name           | Template Rendered         | Route Parameters          | Context Variables Passed to Templates (type)              | Form Data Expected (POST routes)                        |
|-------------------------------|-------------|------------------------|---------------------------|---------------------------|-------------------------------------------------------------|-------------------------------------------------------|
| /                             | GET         | root_redirect           | Redirects to /dashboard   | None                      | None                                                        | None                                                  |
| /dashboard                    | GET         | dashboard_page          | dashboard.html            | None                      | featured_properties (list of dict), recent_listings (list of dict) | None                                                 |
| /search                      | GET         | property_search_page    | search.html               | None                      | properties (list of dict), filter_location (str), min_price (float or None), max_price (float or None), property_type_filter (str) | None                                                 |
|                               | POST        | property_search_filter  | search.html               | None                      | properties (list of dict) after filtering                    | location (str), min_price (float), max_price (float), property_type (str) |
| /property/<int:property_id>  | GET         | property_details_page   | property_details.html     | property_id (int)         | property (dict)                                              | None                                                  |
| /property/<int:property_id>/add_favorite | POST         | add_favorite           | Redirects to /property/<property_id> | property_id (int)         | None                                                        | property_id (int)                                      |
| /property/<int:property_id>/submit_inquiry | POST         | submit_inquiry_from_details | Redirects to /inquiry  | property_id (int)         | None                                                        | name (str), email (str), phone (str), message (str), property_id (int) |
| /inquiry                      | GET         | inquiry_page            | inquiry.html              | None                      | properties (list of dict)                                   | None                                                  |
|                               | POST        | submit_inquiry          | Redirects to /my_inquiries| None                      | None                                                        | property_id (int), name (str), email (str), phone (str), message (str) |
| /my_inquiries                | GET         | my_inquiries_page       | my_inquiries.html         | None                      | inquiries (list of dict), status_filter (str)               | None                                                  |
| /my_inquiries/delete/<int:inquiry_id> | POST         | delete_inquiry         | Redirects to /my_inquiries | inquiry_id (int)           | None                                                        | inquiry_id (int)                                      |
| /my_favorites                | GET         | my_favorites_page       | my_favorites.html         | None                      | favorite_properties (list of dict)                          | None                                                  |
| /my_favorites/remove/<int:property_id> | POST         | remove_favorite        | Redirects to /my_favorites | property_id (int)          | None                                                        | property_id (int)                                     |
| /agents                     | GET         | agents_page             | agents.html               | None                      | agents (list of dict), agent_search_query (str)             | None                                                  |
| /locations                  | GET         | locations_page          | locations.html            | None                      | locations (list of dict), location_sort (str)               | None                                                  |


---

## Section 2: HTML Templates (Frontend)

### dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (div container)
  - featured-properties (div showing featured properties)
  - browse-properties-button (button)
  - my-inquiries-button (button)
  - my-favorites-button (button)
- Context Variables:
  - featured_properties (list of dict): Featured property recommendations with keys (property_id, address, price, etc.)
  - recent_listings (list of dict): Recently listed properties
- Navigation:
  - browse-properties-button -> url_for('property_search_page')
  - my-inquiries-button -> url_for('my_inquiries_page')
  - my-favorites-button -> url_for('my_favorites_page')
- Forms: None

---

### search.html
- Page Title: Property Search
- Element IDs:
  - search-page (div container)
  - location-input (input text)
  - price-range-min (input number)
  - price-range-max (input number)
  - property-type-filter (dropdown)
  - properties-grid (div holding property cards)
  - view-property-button-{property_id} (button) for each property
- Context Variables:
  - properties (list of dict): Properties matching current search filters
  - filter_location (str): Current location filter
  - min_price (float or None): Minimum price filter
  - max_price (float or None): Maximum price filter
  - property_type_filter (str): Selected property type
- Navigation:
  - view-property-button-{property_id} -> url_for('property_details_page', property_id=property_id)
- Forms:
  - Search/Filter form with inputs:
    - location-input (name='location')
    - price-range-min (name='min_price')
    - price-range-max (name='max_price')
    - property-type-filter (name='property_type')
    - submit button triggering POST to url_for('property_search_filter')

---

### property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (div container)
  - property-address (h1 showing property address)
  - property-price (div showing price)
  - property-description (div showing description)
  - property-features (div showing beds, baths, sqft)
  - add-to-favorites-button (button)
  - submit-inquiry-button (button)
- Context Variables:
  - property (dict): Detailed property info with all fields
- Navigation:
  - add-to-favorites-button submits POST to url_for('add_favorite', property_id=property['property_id'])
  - submit-inquiry-button submits POST to url_for('submit_inquiry_from_details', property_id=property['property_id'])
- Forms:
  - Add to Favorites: button form
  - Submit Inquiry: button form

---

### inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (div container)
  - select-property (dropdown)
  - inquiry-name (input text)
  - inquiry-email (input email)
  - inquiry-phone (input tel)
  - inquiry-message (textarea)
  - submit-inquiry-button (button)
- Context Variables:
  - properties (list of dict): Properties available for inquiry
- Navigation: None
- Forms:
  - Inquiry form with inputs:
    - select-property (name='property_id')
    - inquiry-name (name='name')
    - inquiry-email (name='email')
    - inquiry-phone (name='phone')
    - inquiry-message (name='message')
    - Form submits POST to url_for('submit_inquiry')

---

### my_inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (div container)
  - inquiries-table (table)
  - inquiry-status-filter (dropdown)
  - delete-inquiry-button-{inquiry_id} (button for each inquiry)
  - back-to-dashboard (button)
- Context Variables:
  - inquiries (list of dict): List of all inquiries
  - status_filter (str): Current filter for inquiry status
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Forms:
  - Inquiry status filter form
  - Delete inquiry buttons submit POST to url_for('delete_inquiry', inquiry_id=inquiry_id)

---

### my_favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (div container)
  - favorites-list (div container listing properties)
  - remove-from-favorites-button-{property_id} (button for each favorite property)
  - view-property-button-{property_id} (button for details)
  - back-to-dashboard (button)
- Context Variables:
  - favorite_properties (list of dict): Favorite property details
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
  - view-property-button-{property_id} -> url_for('property_details_page', property_id=property_id)
- Forms:
  - Remove from favorites buttons submit POST to url_for('remove_favorite', property_id=property_id)

---

### agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (div container)
  - agents-list (div container listing agents)
  - agent-search (input text)
  - contact-agent-button-{agent_id} (button for each agent)
  - back-to-dashboard (button)
- Context Variables:
  - agents (list of dict): Agent details
  - agent_search_query (str): Current search input
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Forms:
  - Agent search form with input id=agent-search and submit button (GET method)

---

### locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (div container)
  - locations-list (div container listing locations)
  - view-location-button-{location_id} (button for each location)
  - location-sort (dropdown)
  - back-to-dashboard (button)
- Context Variables:
  - locations (list of dict): Locations info
  - location_sort (str): Sort criteria
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Forms:
  - Sort dropdown form (GET or POST with url_for('locations_page'))


---

## Section 3: Data File Schemas (Backend)

### data/properties.txt
- Fields (pipe-delimited): 
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description: Stores detailed info about properties listed.
- Example rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### data/locations.txt
- Fields (pipe-delimited): 
  location_id|location_name|region|average_price|property_count|description
- Description: Stores info about popular locations for browsing.
- Example rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

### data/inquiries.txt
- Fields (pipe-delimited): 
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description: Stores all user-submitted property inquiries.
- Example rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### data/favorites.txt
- Fields (pipe-delimited): 
  favorite_id|property_id|added_date
- Description: Stores properties marked as favorites by users.
- Example rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

### data/agents.txt
- Fields (pipe-delimited): 
  agent_id|agent_name|specialization|email|phone|properties_sold
- Description: Stores real estate agents' information.
- Example rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67

---

This design specification document enables backend and frontend teams to work independently with consistency in route design, templates, element IDs, context variables, and data file schemas as per user requirements of the RealEstate web application.
