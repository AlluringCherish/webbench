# RealEstate Backend Design Specification

---

## Section 1: Flask Routes Design

### Overview
The backend server will be implemented using Python Flask. Local text files in the `data` directory will be used for persistent data storage. The application does not require authentication. All data processing for filtering, searching, sorting, adding/removing is done server-side.

---

### 1. Dashboard Page
- **Route:** `/` or `/dashboard`
- **Methods:** GET
- **Purpose:** Serve dashboard page with featured properties and recent listings
- **Request:** None
- **Response:** Render `dashboard.html` template with context containing featured properties list and recent properties list.

---

### 2. Property Search Page
- **Route:** `/properties`
- **Methods:** GET
- **Purpose:** Display properties with optional filters for location, price range, and property type
- **Request Query Parameters:**
  - `location` (optional string) - filter by location/city name (case insensitive substring match)
  - `price_min` (optional int) - minimum price filter
  - `price_max` (optional int) - maximum price filter
  - `property_type` (optional string) - filter by property type (House, Apartment, Condo, Land)
- **Response:** Render `properties.html` with filtered properties list

---

### 3. Property Details Page
- **Route:** `/property/<int:property_id>`
- **Methods:** GET
- **Purpose:** Display details for a specific property by ID
- **Request:** URL parameter `property_id`
- **Response:** Render `property_details.html` with property details and associated agent info

---

### 4. Property Inquiry Page
- **Route:** `/inquiry`
- **Methods:** GET, POST
- **Purpose:** Show inquiry submission form (GET) and handle inquiry form submission (POST)
- **GET Request:** No parameters, renders inquiry form with property selection dropdown
- **POST Request:** Form data including:
  - `property_id` (int) - selected property ID
  - `customer_name` (string) - user name
  - `customer_email` (string) - user email
  - `customer_phone` (string) - user phone
  - `message` (string) - inquiry message
- **POST Response:** Redirect or JSON response indicating success/failure

---

### 5. My Inquiries Page
- **Route:** `/inquiries`
- **Methods:** GET, POST
- **Purpose:** Display all inquiries with filter by status, allow deletion
- **GET Request Query Parameter:**
  - `status` (optional) - filter by inquiry status (All, Pending, Contacted, Resolved)
- **Response:** Render `inquiries.html` with filtered inquiries
- **POST Request (AJAX):** To delete an inquiry with `inquiry_id` parameter
- **POST Response:** JSON with success or error message

---

### 6. My Favorites Page
- **Route:** `/favorites`
- **Methods:** GET
- **Purpose:** Display all favorite properties
- **Response:** Render `favorites.html` with list of favorite properties

---

### 7. Add to Favorites
- **Route:** `/favorites/add`
- **Methods:** POST
- **Purpose:** Add a property to favorites
- **Request Data:** JSON or form data with `property_id`
- **Response:** JSON success or error

---

### 8. Remove from Favorites
- **Route:** `/favorites/remove`
- **Methods:** POST
- **Purpose:** Remove a property from favorites
- **Request Data:** JSON or form data with `property_id`
- **Response:** JSON success or error

---

### 9. Agent Directory Page
- **Route:** `/agents`
- **Methods:** GET
- **Purpose:** List all agents with optional search by name
- **Request Query Parameter:**
  - `search` (optional string) - filter agents by name (case insensitive substring)
- **Response:** Render `agents.html` with filtered agents

---

### 10. Locations Page
- **Route:** `/locations`
- **Methods:** GET
- **Purpose:** List all locations with sorting options
- **Request Query Parameter:**
  - `sort` (optional string) - sorting option: `name`, `property_count`, `average_price`
- **Response:** Render `locations.html` with sorted locations

---

### 11. View Properties by Location
- **Route:** `/locations/<int:location_id>/properties`
- **Methods:** GET
- **Purpose:** List properties for a specific location
- **Response:** Render `location_properties.html` with list of properties in location

---

## Section 2: Data File Schema and Access

### General Notes
- All data files are stored in `data/` directory under the application root.
- File reading and writing will use Python's standard file handling with UTF-8 encoding.
- Data rows are pipe-delimited (`|`).
- For concurrency or multiple writes, file locking or synchronization mechanisms should be implemented (e.g., using filelock or threading.Lock).
- Writes overwrite the entire file with updated content.
- IDs are unique integers.

---

### 1. Properties Data
- **Filename:** `data/properties.txt`
- **Schema Columns (pipe-delimited):**
  1. `property_id` (int) - Unique property identifier
  2. `address` (string) - Property street address
  3. `location` (string) - Location or city name
  4. `price` (int) - Property price in dollars
  5. `property_type` (string) - Type of property (House, Apartment, Condo, Land)
  6. `bedrooms` (int) - Number of bedrooms
  7. `bathrooms` (float) - Number of bathrooms
  8. `square_feet` (int) - Square footage
  9. `description` (string) - Description text
  10. `agent_id` (int) - Agent responsible for property
  11. `status` (string) - Property status (e.g., Available, Sold)

- **Example Row:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  ```

- **Reading Logic:**
  - Read lines, split by `|`, parse fields accordingly.
  - Return as list of dictionaries for easier handling.

- **Filtering and Searching:**
  - Implement filtering on location substring case insensitive.
  - Price min/max filtering on integer price.
  - Property type exact match.

- **Writing Logic:**
  - When updating status or adding new property, overwrite file completely with all properties.

---

### 2. Locations Data
- **Filename:** `data/locations.txt`
- **Schema Columns (pipe-delimited):**
  1. `location_id` (int) - Unique identifier
  2. `location_name` (string) - Name of the location
  3. `region` (string) - Region name
  4. `average_price` (int) - Average property price in location
  5. `property_count` (int) - Number of properties in location
  6. `description` (string) - Description

- **Example Row:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  ```

- **Reading Logic:** Similar to properties

- **Sorting:** By name, property_count, average_price

---

### 3. Property Inquiries Data
- **Filename:** `data/inquiries.txt`
- **Schema Columns (pipe-delimited):**
  1. `inquiry_id` (int) - Unique inquiry identifier
  2. `property_id` (int) - Property referenced
  3. `customer_name` (string)
  4. `customer_email` (string)
  5. `customer_phone` (string)
  6. `message` (string)
  7. `inquiry_date` (YYYY-MM-DD string)
  8. `status` (string) - Inquiry status (Pending, Contacted, Resolved)

- **Example Row:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  ```

- **Reading Logic:** Read all inquiries

- **Filtering:** Filter by status (except All returns all)

- **Writing Logic:** Add new inquiries or delete inquiries and rewrite file

---

### 4. Favorite Properties Data
- **Filename:** `data/favorites.txt`
- **Schema Columns (pipe-delimited):**
  1. `favorite_id` (int) - Unique favorite entry
  2. `property_id` (int)
  3. `added_date` (YYYY-MM-DD string)

- **Example Row:**
  ```
  1|1|2025-01-10
  ```

- **Reading Logic:** Read all favorites

- **Writing Logic:** Add/remove favorites by rewriting entire file

- **Note:** To display favorite properties, join with properties data on `property_id`

---

### 5. Real Estate Agents Data
- **Filename:** `data/agents.txt`
- **Schema Columns (pipe-delimited):**
  1. `agent_id` (int)
  2. `agent_name` (string)
  3. `specialization` (string)
  4. `email` (string)
  5. `phone` (string)
  6. `properties_sold` (int)

- **Example Row:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  ```

- **Reading Logic:** Load all agents

---

## Section 3: Integration and API Design

### Inquiry Submission
- **Endpoint:** POST `/inquiry`
- **Input:** Form data with all inquiry fields as specified in Section 1
- **Processing:** Validate data, generate new unique inquiry_id, set inquiry_date as current date, append inquiry to `inquiries.txt`
- **Response:** JSON with success status and new inquiry_id or error message

### Favorites Management
- **Add to Favorites:**
  - POST `/favorites/add`
  - Input JSON or form data: `property_id`
  - Processing: Check if property already in favorites; if not, assign new favorite_id, add to `favorites.txt` with current date
  - Response: JSON success or error

- **Remove from Favorites:**
  - POST `/favorites/remove`
  - Input JSON or form data: `property_id`
  - Processing: Remove entry with property_id from favorites
  - Response: JSON success or error

### Inquiries Deletion
- **Endpoint:** POST `/inquiries/delete`
- **Input:** JSON or form data: `inquiry_id`
- **Processing:** Remove inquiry with given inquiry_id
- **Response:** JSON success or error

---

# Summary
This backend design supports the full feature set described in the user requirements, via well-defined Flask routes that render templates or serve JSON for actions like inquiry submissions and favorites management. It leverages simple local text files with explicit schemas for persistence, and the backend controls all filtering, searching, sorting, and CRUD operations on the data.

The design uses RESTful principles for data endpoints and standard GET routes for pages requiring filtered data views.

The backend developer can implement the Flask application and data handling fully based on this specification without further information required.
