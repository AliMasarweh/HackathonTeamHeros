import sys

from mohammad.hackathon_queries import queries


class Basket:
    def __init__(self, store_name):
        self.store_name = store_name
        self.number_of_items = 0
        self.item_to_price = {}
        self.basket_price = 0

    def add_item(self, item_name_price):
        if item_name_price['product_name'] not in self.item_to_price:
            self.number_of_items += 1
            self.item_to_price[item_name_price['product_name']] = float(item_name_price['price'])
            self.basket_price += float(item_name_price['price'])

    def add_item_new_setup(self, store, item):
        if item not in self.item_to_price:
            self.number_of_items += 1
            self.item_to_price[item] = float(store[item])
            self.basket_price += float(store[item])

    def price(self):
        return self.basket_price

    def __len__(self):
        return self.number_of_items

    def __repr__(self):
        return f"store name: {self.store_name}, items: {self.item_to_price}, total: {self.basket_price}"


def add_items_to_store_basket(items_names, store, store_basket, store_name):
    for item_name_price in store:
        if item_name_price['product_name'] in items_names:
            store_basket[store_name].add_item(item_name_price)


def add_items_to_store_basket_new_setup(items_names, store, store_basket, store_name):
    for item in items_names:
        if item in store:
            store_basket[store_name].add_item_new_setup(store, item)


def find_missing_items(items_names, store_basket, cheapest_store_name):
    ans = []
    for item in items_names:
        if item not in store_basket[cheapest_store_name].item_to_price:
            ans.append(item)

    return ans


def cheapest_basket(items_names):
    stores = queries.getDictionaryofStores()
    store_basket = {}
    max_items = 0
    cheapest_price = sys.maxsize
    cheapest_store_name = None

    for store_name in stores:
        store = stores[store_name]
        store_basket[store_name] = Basket(store_name)

        add_items_to_store_basket_new_setup(items_names, store, store_basket, store_name)

        max_items = max(max_items, len(store_basket[store_name]))
        if len(store_basket[store_name]) < max_items:
            del store_basket[store_name]
        else:
            cheapest_price = min(cheapest_price, store_basket[store_name].price())
            if store_basket[store_name].price() > cheapest_price:
                del store_basket[store_name]
            else:
                cheapest_store_name = store_name

    missing_items = find_missing_items(items_names, store_basket, cheapest_store_name)

    return store_basket[cheapest_store_name], missing_items


if __name__ == '__main__':
    basket, missing = cheapest_basket(['Sauce','Apple Juice','Bacon','Beef Stew Meat'])
    print(basket)
    print(missing)
