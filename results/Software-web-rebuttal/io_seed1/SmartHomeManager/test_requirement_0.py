Test the website through 5000.
first of website loads correctly and whether basic navigation on the data in Task.
elements integrity pages. This includes and correctness each as the requirements.
unittest
bs4
def setUp(self):
Set
self.client =
def
# Test 1: and code
self.client.get('/')
self.assertEqual(response.status_code, 200, "Dashboard page accessible with status
test_02_dashboard_elements(self):
# Task 2 Check and content
response
= BeautifulSoup(response.data, 'html.parser')
div id
dashboard_div id='dashboard-page')
self.assertIsNotNone(dashboard_div, id 'dashboard-page' be present")
Check div
soup.find('div',
"Device summary 'device-summary' must be
for navigation
buttons_ids
'energy-button', 'activity-button']
for in buttons_ids:
soup.find('button',
with id must
Check room
"Room with 'room-list' on
def test_03_device_list_page_elements(self):
Navigate to check
response =
= 'html.parser')
device_list_div
list container div with must
= soup.find('table', id='device-table')
self.assertIsNotNone(device_table, present")
# for button
= soup.find('button',
self.assertIsNotNone(back_btn, "Back dashboard with id must present")
Check has button with
row present
in
in row
row.find('button')
have button")
self.assertTrue(control_btn['id'].startswith('control-device-button-'),
button
def test_04_add_device_page_elements(self):
self.assertEqual(response.status_code,
BeautifulSoup(response.data,
soup.find('div', id='add-device-page')
div id must present")
device_name_input
field id must be present")
device_type_dropdown
with id be
= soup.find('select',
with 'device-room' be present")
= id='submit-device-button')
button with id
back_button =
self.assertIsNotNone(back_button, to dashboard 'back-to-dashboard'
Use a known '1'
response = self.client.get('/device-control/1')
200)
BeautifulSoup(response.data, 'html.parser')
device_control_div =
"Device with must be
device_name_display id='device-name-display')
name with
device_status_display = soup.find('div',
'device-status-display'
power_toggle soup.find('button', id='power-toggle')
toggle button id be
soup.find('button',
"Save button 'save-settings-button' be present")
back_to_devices = soup.find('button', id='back-to-devices')
self.assertIsNotNone(back_to_devices, "Back must be
def
soup = 'html.parser')
container be
rules_table id='rules-table')
"Rules table
'trigger-type', 'action-device', 'action-type']
for input_id in
soup.find(id=input_id)
present")
add_rule_button soup.find('button',
self.assertIsNotNone(add_rule_button, rule button must
to button id must be present")
def test_07_energy_report_page_elements(self):
=
self.assertEqual(response.status_code,
energy_div id='energy-page')
"Energy div with id present")
"Energy summary with must
id='energy-table')
self.assertIsNotNone(energy_table, table with must be
date_filter =
self.assertIsNotNone(date_filter, with 'date-filter' must be
= id='apply-filter-button')
"Apply must be present")
soup.find('button',
to with id 'back-to-dashboard' be
def
= self.client.get('/activity')
self.assertEqual(response.status_code, 200)
soup BeautifulSoup(response.data,
id='activity-page')
with must
with be
= id='search-activity')
be
apply_search_button soup.find('button',
self.assertIsNotNone(apply_search_button, "Apply search button id 'apply-search-button' must be
=
to id be
if ==
unittest.main()