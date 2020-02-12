import db_connection
import sys


class Basket:
    def __init__(self, store_name):
        self.store_name = store_name
        self.number_of_items = 0
        self.item_to_price = {}
        self.basket_price = 0

    def add_item(self, item_name_price):
        if item_name_price['product_name'] not in self.item_to_price['product_name']:
            self.number_of_items += 1
            self.item_to_price['product_name'] = item_name_price['product_name']
            self.item_to_price['price'] = item_name_price['price']
            self.basket_price += float(item_name_price['price'])

    def price(self):
        return self.basket_price

    def __len__(self):
        return self.number_of_items


def add_items_to_store_basket(items_names, store, store_basket, store_name):
    for item_name_price in store:
        if item_name_price['product_name'] in items_names:
            store_basket[store_name].add_item(item_name_price)


def cheapest_basket(items_names):
    stores = db_connection.get_stores_product_list(items_names)
    store_basket = {}
    max_items = 0
    cheapest_price = sys.maxsize

    for store_name in stores:
        store = stores[store_name]
        store_basket[store_name] = Basket(store_name)

        add_items_to_store_basket(items_names, store, store_basket, store_name)

        max_items = max(max_items, len(store_basket[store_name]))
        if len(store_basket[store_name]) < max_items:
            del store_basket[store_name]

        cheapest_price = min(cheapest_price, store_basket[store_name].price())
        if store_basket[store_name].price() > cheapest_price:
            del store_basket[store_name]

    return store_basket
