# Design Spec Document for FoodDelivery Web Applicationx

---

### Section 1 Flask Routes Specification

| Route Path                      | Function Nme          | HTTP Methods | Template file         | Context Vars (nme: typ)                                                                                                          | Route Params (nme: typ)  |
|--------------------------------|----------------------|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|------------------------|
| /                             | root_redirected        | GET         | None redirect        | None                                                                                                                          | Non                      |
| /dashboard                    | dashbord               | GET         | dashboard.htm         | feature_restaurants: list[dict] 
popular_cuisines: list[str]                                            | None                      |
| /restaurants                  | browse_restaurants     | POST         | restaurant.html       | restaurants: list[dict]
search_query: str
cuisine_filte: str                                                      | None                      |
| /menu/<int:restaurant_id>     | restaurant_men          | GET         | menu.html             | restaurante: dict
menu_items: list(dict)                                                                                        | restaurant_id: string      |
| /item/<int:item_id>           | item_detail             | GET         | item_detail.html      | item: dict                                                                                                                     | itemid: int               |
| /cart                        | shopping_cart           | GET         | cart.htm              | cartitems: list[dict]
total_amount: str                                                                                     | None                      |
| /cart/update                  | update_cart_quantity     | POST        | None redirct          | None                                                                                                                          | None                     |
| /cart/remove/<int:item_id>    | remove_cartitem          | POST        | None (redirct)        | None                                                                                                                          | item_id: Str              |
| /checkout                   | checkout                 | GET
POST   | checkout_html           | (GET) cart_items: list[dict]
total_amount: float (POST) form_submit_status: bol
errors dict                                | No                         |
| /orders/active               | active_order             | GET         | active_orders.html     | active_orders: list[dict]
status_filters: str                                                                                 | None                      |
| /track/<int:order_id>         | track_orders             | GET         | trackorder.html        | order: dict
delivery_info dict
order_items: list(dict)                                                                              | orderid: int              |
| /reviews                    | reviews                  | GET         | reviews.htm           | reviews: lst[dict]
filter_ratings: str                                                                                     | None                      |
| /reviews/write              | writ_review              | GET
POST   | write_reviews.html     | (GET) None (POST) submission_status: int
errors: dict                                                                        | None                      |
