import db_connection
import sys

class Basket:
    def __init__(self, store_name):
        self.store_name = store_name
        self.number_of_items = 0
        self.item_to_price = {}

    def add_item(self, item_name_price):
        if item_name_price['name'] not in self.item_to_price['name']:
            self.number_of_items += 1
            self.item_to_price['name'] = item_name_price['name']
            self.item_to_price['price'] = item_name_price['price']

    def __len__(self):
        return self.number_of_items

def cheapest_basket():
    items_names = []
    stores = db_connection.get_stores_product_list(items_names)

    store_basket = {}

    max_items = 0

    for store_name in stores:
        store = stores[store_name]

        store_basket[store_name] = Basket(store_name)

        for item_name_price in store:
            if item_name_price['name'] in items_names:
                store_basket[store_name].add_item(item_name_price)

        max_items = max(max_items, len(store_basket[store_name]))

        if len(store_basket[store_name]) < max_items:
            del store_basket[store_name]

    cheapest_price = sys.maxsize
    

