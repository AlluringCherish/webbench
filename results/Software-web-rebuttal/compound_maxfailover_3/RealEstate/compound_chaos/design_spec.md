# design_spec.md for RealEstate Web Application

---

## 1. Flask Routes Specification (Backend)

| Route Path                  | HTTP Method | Function Name          | Template Rendered          | Context Variables (name:type)                                   | POST form data (fields)                                |
|-----------------------------|-------------|------------------------|----------------------------|-----------------------------------------------------------------|-------------------------------------------------------|
| /                            | GET         | root_redirect          | None (redirect to /dashboard) | None                                                            | None                                                  |
| /dashboard                   | GET         | dashboard              | dashboard.html             | featured_properties:List[Dict], recent_listings:List[Dict]       | None                                                  |
| /properties/search           | GET         | property_search        | property_search.html       | properties:List[Dict], locations:List[str], selected_filters:Dict | None                                                  |
| /properties/<int:property_id>| GET         | property_details       | property_details.html      | property:Dict, agent:Dict, is_favorite:bool                     | None                                                  |
| /inquiries/submit            | GET         | inquiry_form           | inquiry_form.html          | properties:List[Dict]                                             | None                                                  |
| /inquiries/submit            | POST        | submit_inquiry         | inquiry_form.html or redirect to /inquiries | form data below                                       |
| /inquiries                   | GET         | my_inquiries           | inquiries.html             | inquiries:List[Dict], filter_status:str                         | None                                                  |
| /inquiries/delete/<int:inquiry_id> | POST   | delete_inquiry         | redirect to /inquiries     | None                                                            | None                                                  |
| /favorites                  | GET         | my_favorites           | favorites.html             | favorites:List[Dict], properties_map:Dict[int,Dict]             | None                                                  |
| /favorites/add/<int:property_id> | POST   | add_to_favorites       | redirect to /favorites     | None                                                            | None                                                  |
| /favorites/remove/<int:property_id> | POST | remove_from_favorites  | redirect to /favorites     | None                                                            | None                                                  |
| /agents                     | GET         | agent_directory        | agents.html                | agents:List[Dict], search_query:str                             | None                                                  |
| /locations                  | GET         | locations_page         | locations.html             | locations:List[Dict], sort_order:str                            | None                                                  |


### Detailed routes with descriptions:

1. **Root Redirect**
   - Path: `/`
   - Method: GET
   - Function: `root_redirect`
   - Behavior: Redirects to `/dashboard`

2. **Dashboard**
   - Path: `/dashboard`
   - Method: GET
   - Function: `dashboard`
   - Template: `dashboard.html`
   - Context:
     - `featured_properties`: List of featured property dictionaries (each dict with keys like property_id:int, address:str, price:int, etc.)
     - `recent_listings`: List of recent property dictionaries

3. **Property Search**
   - Path: `/properties/search`
   - Method: GET
   - Function: `property_search`
   - Template: `property_search.html`
   - Context:
     - `properties`: List of property dictionaries matching search filters
     - `locations`: List of available location names (strings)
     - `selected_filters`: Dict containing keys `location` (str), `price_min` (int or None), `price_max` (int or None), `property_type` (str or None)

4. **Property Details**
   - Path: `/properties/<int:property_id>`
   - Method: GET
   - Function: `property_details`
   - Template: `property_details.html`
   - Context:
     - `property`: Dictionary with all property details
     - `agent`: Dictionary of agent details for this property
     - `is_favorite`: Boolean indicating if the property is in user's favorites

5. **Inquiry Form**
   - Path: `/inquiries/submit`
   - Method: GET
   - Function: `inquiry_form`
   - Template: `inquiry_form.html`
   - Context:
     - `properties`: List of all properties to select from

6. **Submit Inquiry**
   - Path: `/inquiries/submit`
   - Method: POST
   - Function: `submit_inquiry`
   - Template: When errors, re-renders `inquiry_form.html` with error context; on success redirects to `/inquiries`
   - POST form data expected:
     - `property_id` (int, required)
     - `customer_name` (str, required)
     - `customer_email` (str/email, required)
     - `customer_phone` (str, optional)
     - `inquiry_message` (str, required)

7. **My Inquiries**
   - Path: `/inquiries`
   - Method: GET
   - Function: `my_inquiries`
   - Template: `inquiries.html`
   - Context:
     - `inquiries`: List of inquiry dictionaries filtered by status if applicable
     - `filter_status`: String status filter ('All', 'Pending', 'Contacted', 'Resolved')

8. **Delete Inquiry**
   - Path: `/inquiries/delete/<int:inquiry_id>`
   - Method: POST
   - Function: `delete_inquiry`
   - Template: None (redirects to `/inquiries`)

9. **My Favorites**
   - Path: `/favorites`
   - Method: GET
   - Function: `my_favorites`
   - Template: `favorites.html`
   - Context:
     - `favorites`: List of favorite property dictionaries
     - `properties_map`: Dictionary keyed by property_id (int) to full property dict (for display)

10. **Add to Favorites**
    - Path: `/favorites/add/<int:property_id>`
    - Method: POST
    - Function: `add_to_favorites`
    - Template: None (redirects to `/favorites`)

11. **Remove from Favorites**
    - Path: `/favorites/remove/<int:property_id>`
    - Method: POST
    - Function: `remove_from_favorites`
    - Template: None (redirects to `/favorites`)

12. **Agent Directory**
    - Path: `/agents`
    - Method: GET
    - Function: `agent_directory`
    - Template: `agents.html`
    - Context:
      - `agents`: List of agent dictionaries
      - `search_query`: String from search parameter

13. **Locations Page**
    - Path: `/locations`
    - Method: GET
    - Function: `locations_page`
    - Template: `locations.html`
    - Context:
      - `locations`: List of location dictionaries
      - `sort_order`: String sort option ('By Name', 'By Properties Count', 'By Average Price')


---

## 2. HTML Templates (Frontend)

Each template corresponds to the route and includes page title, element IDs, context variables, navigation, and forms.

---

### dashboard.html
- Page title: "Real Estate Dashboard"
- Top-level container ID: `dashboard-page`
- Element IDs:
  - `featured-properties` (Div)
  - `browse-properties-button` (Button)
  - `my-inquiries-button` (Button)
  - `my-favorites-button` (Button)
- Context variables:
  - `featured_properties`: List[Dict], featured properties to display
  - `recent_listings`: List[Dict], recent listings (may be used in the page but is not explicitly specified in elements)
- Navigation using url_for():
  - `url_for('property_search')` for property search
  - `url_for('my_inquiries')` for inquiries
  - `url_for('my_favorites')` for favorites
- Buttons:
  - `browse-properties-button` navigates to property search page on click
  - `my-inquiries-button` navigates to inquiries page
  - `my-favorites-button` navigates to favorites page

---

### property_search.html
- Page title: "Property Search"
- Top-level container ID: `search-page`
- Element IDs:
  - `location-input` (Input)
  - `price-range-min` (Input, number)
  - `price-range-max` (Input, number)
  - `property-type-filter` (Dropdown)
  - `properties-grid` (Div)
  - For each property in `properties`, an element:
    - `view-property-button-{property_id}` (Button)
- Context variables:
  - `properties`: List[Dict], all properties matching filters
  - `locations`: List[str], available locations
  - `selected_filters`: Dict with search filter keys (location:str, price_min:int or None, price_max:int or None, property_type:str or None)
- Navigation:
  - `url_for('property_details', property_id=property['property_id'])` for each property view button
- No form for filter submit specified, assume filtering via GET parameters or frontend

---

### property_details.html
- Page title: "Property Details"
- Top-level container ID: `property-details-page`
- Element IDs:
  - `property-address` (H1)
  - `property-price` (Div)
  - `property-description` (Div)
  - `property-features` (Div)
  - `add-to-favorites-button` (Button)
  - `submit-inquiry-button` (Button)
- Context variables:
  - `property`: Dict with detailed property info
  - `agent`: Dict with agent info
  - `is_favorite`: bool, indication if property is favorite
- Navigation:
  - `url_for('add_to_favorites', property_id=property['property_id'])` for add to favorites button (POST form)
  - `url_for('inquiry_form')` for submit inquiry button

- Forms:
  - `add-to-favorites-button` triggered by POST form to `/favorites/add/<property_id>` route
  - `submit-inquiry-button` triggers navigation to inquiry form

---

### inquiry_form.html
- Page title: "Submit Property Inquiry"
- Top-level container ID: `inquiry-page`
- Element IDs:
  - `select-property` (Dropdown)
  - `inquiry-name` (Input)
  - `inquiry-email` (Input, email)
  - `inquiry-phone` (Input, tel)
  - `inquiry-message` (Textarea)
  - `submit-inquiry-button` (Button)
- Context variables:
  - `properties`: List[Dict] for dropdown
- Navigation:
  - None specified
- Forms:
  - Form with action `/inquiries/submit` and method POST
  - Inputs:
    - `select-property`: select property by `property_id`
    - `inquiry-name`: customer name
    - `inquiry-email`: customer email
    - `inquiry-phone`: customer phone
    - `inquiry-message`: inquiry message
  - Submit button with ID `submit-inquiry-button`

---

### inquiries.html
- Page title: "My Inquiries"
- Top-level container ID: `inquiries-page`
- Element IDs:
  - `inquiries-table` (Table)
  - `inquiry-status-filter` (Dropdown)
  - `delete-inquiry-button-{inquiry_id}` (Button for each inquiry)
  - `back-to-dashboard` (Button)
- Context variables:
  - `inquiries`: List[Dict], each dict containing inquiry details
  - `filter_status`: str, current filter selected
- Navigation:
  - `url_for('dashboard')` for back to dashboard button
- Forms:
  - Each delete button submits POST to `/inquiries/delete/<inquiry_id>`

---

### favorites.html
- Page title: "My Favorite Properties"
- Top-level container ID: `favorites-page`
- Element IDs:
  - `favorites-list` (Div)
  - For each favorite property:
    - `remove-from-favorites-button-{property_id}` (Button)
    - `view-property-button-{property_id}` (Button)
  - `back-to-dashboard` (Button)
- Context variables:
  - `favorites`: List[Dict] of favorite entries
  - `properties_map`: Dict[int,Dict] mapping property_id to property details
- Navigation:
  - `url_for('property_details', property_id=property_id)` for view property buttons
  - `url_for('dashboard')` for back to dashboard button
- Forms:
  - Remove buttons submit POST to `/favorites/remove/<property_id>`

---

### agents.html
- Page title: "Real Estate Agents"
- Top-level container ID: `agents-page`
- Element IDs:
  - `agents-list` (Div)
  - `agent-search` (Input)
  - `contact-agent-button-{agent_id}` (Button for each agent)
  - `back-to-dashboard` (Button)
- Context variables:
  - `agents`: List[Dict]
  - `search_query`: str
- Navigation:
  - `url_for('dashboard')` for back to dashboard button
- Forms:
  - No contact form specified, contact-agent-button could be link or mailto on frontend

---

### locations.html
- Page title: "Featured Locations"
- Top-level container ID: `locations-page`
- Element IDs:
  - `locations-list` (Div)
  - For each location:
    - `view-location-button-{location_id}` (Button)
  - `location-sort` (Dropdown)
  - `back-to-dashboard` (Button)
- Context variables:
  - `locations`: List[Dict]
  - `sort_order`: str
- Navigation:
  - `url_for('dashboard')` for back to dashboard button
  - `url_for('property_search')` potentially for viewing location properties
- Forms:
  - No explicit form, sorting/filtering can be GET parameters or JS

---

## 3. Data File Schemas (Backend)

---

### properties.txt
- File Path: `data/properties.txt`
- Fields (pipe-delimited, no header):
  1. property_id (int)  
  2. address (str)  
  3. location (str)  
  4. price (int)  
  5. property_type (str) - House, Apartment, Condo, Land
  6. bedrooms (int)
  7. bathrooms (float)
  8. square_feet (int)
  9. description (str)
  10. agent_id (int)
  11. status (str) - e.g. Available, Sold
- Description: Stores all property listings with details and status.
- Examples:
```
1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
```

---

### locations.txt
- File Path: `data/locations.txt`
- Fields (pipe-delimited, no header):
  1. location_id (int)
  2. location_name (str)
  3. region (str)
  4. average_price (int)
  5. property_count (int)
  6. description (str)
- Description: Stores featured locations with aggregated details.
- Examples:
```
1|Downtown|Central|425000|45|Urban area with business district
2|Midtown|Central|380000|38|Mixed residential and commercial zone
3|Suburb|Outskirts|295000|52|Family-friendly residential area
```

---

### inquiries.txt
- File Path: `data/inquiries.txt`
- Fields (pipe-delimited, no header):
  1. inquiry_id (int)
  2. property_id (int)
  3. customer_name (str)
  4. customer_email (str)
  5. customer_phone (str)
  6. message (str)
  7. inquiry_date (str) - Date in YYYY-MM-DD format
  8. status (str) - Pending, Contacted, Resolved
- Description: Stores all property inquiries submitted by users.
- Examples:
```
1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
```

---

### favorites.txt
- File Path: `data/favorites.txt`
- Fields (pipe-delimited, no header):
  1. favorite_id (int)
  2. property_id (int)
  3. added_date (str) - Date in YYYY-MM-DD format
- Description: Stores properties that have been marked as favorites by users.
- Examples:
```
1|1|2025-01-10
2|2|2025-01-12
3|3|2025-01-14
```

---

### agents.txt
- File Path: `data/agents.txt`
- Fields (pipe-delimited, no header):
  1. agent_id (int)
  2. agent_name (str)
  3. specialization (str)
  4. email (str)
  5. phone (str)
  6. properties_sold (int)
- Description: Stores real estate agent details.
- Examples:
```
101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
103|James Martinez|Luxury Homes|james@email.com|555-0003|67
```
