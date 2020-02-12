import sys

from mohammad.hackathon_queries import queries


class Basket:
    def __init__(self, store_name):
        self.store_name = store_name
        self.number_of_items = 0
        self.item_to_price = {}
        self.item_to_quantity = {}
        self.basket_price = 0

    def add_item_quantity(self, item_name_price, quantity):
        if item_name_price['product_name'] not in self.item_to_price:
            self.number_of_items += quantity
            self.item_to_price[item_name_price['product_name']] = float(item_name_price['price'])
            self.item_to_quantity[item_name_price['product_name']] = quantity
            self.basket_price += float(item_name_price['price']) * quantity

    def add_item_quantity_new_setup(self, store, item, quantity):
        if item not in self.item_to_price:
            self.number_of_items += quantity
            self.item_to_price[item] = float(store[item])
            self.item_to_quantity[item] = quantity
            self.basket_price += float(store[item]) * quantity

    def price(self):
        return self.basket_price

    def __len__(self):
        return self.number_of_items

    def __repr__(self):
        return f"store name: {self.store_name}, items: {self.item_to_price}, total: {self.basket_price}"


def add_items_to_store_basket(items_names_to_price_quantity, store, store_basket, store_name):
    for item_name_price in store:
        if item_name_price['product_name'] in items_names_to_price_quantity:
            quantity = int(items_names_to_price_quantity[item_name_price['product_name']])
            store_basket[store_name].add_item_quantity(item_name_price, quantity)


def add_items_to_store_basket_new_setup(items_names_to_price_quantity, store, store_basket, store_name):
    for item in items_names_to_price_quantity:
        if item in store:
            quantity = int(items_names_to_price_quantity[item])
            store_basket[store_name].add_item_quantity_new_setup(store, item, quantity)


def find_missing_items(items_names_to_price_quantity, store_basket, cheapest_store_name):
    ans = []
    for item in items_names_to_price_quantity:
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


def cheapest_basket_with_quantity(items_names_to_price_quantity):
    stores = queries.getDictionaryofStores()
    store_basket = {}
    max_items = 0
    cheapest_price = sys.maxsize
    cheapest_store_name = None

    for store_name in stores:
        store = stores[store_name]
        store_basket[store_name] = Basket(store_name)

        add_items_to_store_basket_new_setup(items_names_to_price_quantity, store, store_basket, store_name)

        max_items = max(max_items, len(store_basket[store_name]))
        if len(store_basket[store_name]) < max_items:
            del store_basket[store_name]
        else:
            cheapest_price = min(cheapest_price, store_basket[store_name].price())
            if store_basket[store_name].price() > cheapest_price:
                del store_basket[store_name]
            else:
                cheapest_store_name = store_name

    missing_items = find_missing_items(items_names_to_price_quantity, store_basket, cheapest_store_name)

    return store_basket[cheapest_store_name], missing_items


def cheapest_product(item_name):
    dict_of_prices = queries.getPriceOfOneItem(item_name)
    cheapest_price = sys.maxsize
    cheapest_store_name = None

    for store_name in dict_of_prices:
        if dict_of_prices[store_name] < cheapest_price:
            cheapest_store_name = store_name

    return {cheapest_store_name: dict_of_prices[cheapest_store_name]}


if __name__ == '__main__':
    basket, missing = cheapest_basket_with_quantity({
        'Sauce': 1,
        'Apple Juice': 1,
        'Bacon': 1,
        'Beef Stew Meat': 1
    })
    print(basket)
    print(missing)

    store_name_to_price = cheapest_product('apple sauce')
    print(store_name_to_price)
