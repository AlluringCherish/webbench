NEED_MODIFY

1. Template 'orders.html' is found corrupted and contains invalid/unreadable content, potentially a leftover or unrelated file: it should be removed or fixed if intended to be a functional page. According to design_spec.md, there is no separate Orders page - only Active Orders and Tracking pages, so it appears unnecessary.

2. In 'item_details' route (app.py), POST method reads quantity from form field 'quantity-input'; however, the 'item_details.html' template name attribute for the quantity input is 'quantity' without the '-input' suffix. This leads to the quantity field always defaulting to 1 on add to cart from item details page. This mismatch should be corrected by either:
- Changing name attribute in item_details.html input to 'quantity-input' (recommended for consistency with app.py).
- Or changing app.py to read 'quantity' instead of 'quantity-input'.

3. In the shopping cart page template (cart.html), the button with id 'proceed-checkout-button' is a button with an onclick JavaScript redirect to '/checkout'. However, in app.py POST handler for '/cart', POST request checks for 'proceed-checkout-button' in form data to detect proceed checkout action, which will never happen since this button does not submit the form but redirects via onclick.
  This inconsistency means the server never processes the proceed checkout action through POST form submission.
  Possible fixes:
  - Change the button to a submit button within the form with that ID and name, so POST sends proper form data.
  - Or handle proceed checkout only with client-side redirect as is, removing server-side POST check for proceed.

4. Minor: In 'active_orders.html' template, the order entry shows "ETA: {{ o.delivery_time if o.delivery_time else 'Unknown' }}". The delivery_time attribute does not exist in order objects loaded in app.py filtered list or added. This will cause the ETA always to show 'Unknown'.
  If ETA should be shown, the system must fetch delivery estimated time from deliveries data and join it to orders, or omit ETA field.

Summary:
- Remove or fix corrupted 'orders.html'.
- Fix quantity input name mismatch in item_details post processing.
- Align proceed-checkout-button action in shopping cart form between frontend and backend.
- Fix or remove ETA display in active orders page.

No syntax/runtime errors detected otherwise. All required pages and element IDs are implemented correctly.