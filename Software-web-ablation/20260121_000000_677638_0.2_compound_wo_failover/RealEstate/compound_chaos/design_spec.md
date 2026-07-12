# Design RealEstate Web Application

---

## Section Flask Routes (Backend)

| Route Path HTTP Name Route Parameters | Variables (name type) | Form Expected (name |
|-------------------------------|-------------|----------------------------|---------------------------|--------------------------|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
/ | - | | - |
| /dashboard GET dashboard | | : |
/search GET | search.html properties : list(dict), filter_options
| | | properties : list(dict), list(dict), : | location_input price_range_max
| | property_id : | |
| GET property_inquiry | : |
/inquiry | | submit_inquiry | - : int, : str, : str, inquiry_message |
| my_inquiries | : list(dict), str
| filter_inquiries | : list(dict), | str
delete_inquiry | inquiries.html : | : |
| /favorites GET | favorites.html list(dict), dict (property_id dict) | -
| /favorites/add/<int:property_id> : int favorites : dict to
| /favorites/remove/<int:property_id> | | int list(dict), |
- :
| | GET | | locations.html - list(dict), sort_option : str |
/locations/sort | sort_locations | locations list(dict), sort_option str | location_sort

Notes
`featured_properties`, `properties`, `favorites`, lists of each representing one data respective files,
is a dictionary by property_id full property for in favorites.
`status_filter`, strings current states.



2: Templates (Frontend)


-

-
-

- my-inquiries-button

Context
- dict): Featured recommendations; property_id address
recent_listings Recent
-

my-inquiries-button: url_for('my_inquiries')

Forms: None

---

2.
Page Title: Search
IDs:
search-page

price-range-min
price-range-max
-

- for
- Variables:
properties of of properties with property_id (str), price (float), property_type (str), (int), bathrooms
- locations (list list for filter suggestions.
filter_options (dict): with price_range_max (str).
- Navigation
property_id=property_id)
Forms:
form
IDs: property-type-filter
- Submit ID: search-submit-button


---

3.
Property Details






add-to-favorites-button
submit-inquiry-button
Context
- property (dict): details with (int), (str), price description bedrooms (int)
Mappings:
add-to-favorites-button: url_for('add_to_favorites', property_id=property.property_id) (POST)
submit-inquiry-button:
-
- Add to with button ID POST to
- button page



### 4. inquiry.html
Page Title: Property
IDs:
- inquiry-page

- inquiry-name
inquiry-email
-
-
- submit-inquiry-button
Variables:
properties with keys property_id
Navigation Mappings:
- Form action:
- Forms:
- Inquiry form with inputs as above
button submit-inquiry-button




Title:
-
inquiries-page
inquiries-table

- delete-inquiry-button-{{inquiry_id}} (dynamic inquiry)
back-to-dashboard
- Context Variables:
(list of (str), customer_email customer_phone (str), (str),
- inquiry status

url_for('dashboard')
- Forms:
form inquiry-status-filter submit
with



favorites.html

-
-
favorites-list
property)
- for
back-to-dashboard

favorites (list of dict): Each dict with (int), (str)
- properties_dict (int) property

url_for('dashboard')
url_for('property_details',
- Forms:
- favorites ID method

---

### agents.html
Page Estate
IDs:
- agents-page

-
contact-agent-button-{{agent_id}} (dynamic agent)


(list of Each agent_id specialization (str), phone (str), properties_sold
- Navigation Mappings:
- back-to-dashboard:
- Forms:
- Agent search with (client-side filtering possibly)



### 8.
Title: Featured
Element IDs:


view-location-button-{{location_id}} for each
location-sort
back-to-dashboard
-
- locations dict with region (float), property_count description
(str): Current sorting


Action to view properties in given location (implementation dependent)

- form with and submit

---

File Schemas

properties.txt
Path: data/properties.txt
- property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
listings including location, price, property agent
Example
1|123 with large yard|101|Available
Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment
3|789 Road|Suburb|280000|Condo|2|2|1500|Cozy in



###
-

Description: popular data with name, property count, and
Example
district
2|Midtown|Central|380000|38|Mixed residential zone
3|Suburb|Outskirts|295000|52|Family-friendly residential area



inquiries.txt
data/inquiries.txt
- inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- inquiries properties including message, date, status.
- Rows:
1|1|John in viewing
2|2|Sarah a
is lowest offer?|2025-01-17|Resolved



###
Path:
-
- Lists favorite properties with property and date


2|2|2025-01-12




###
File
- (pipe-delimited):
Data and information.
Example Rows:
101|Robert

Martinez|Luxury
