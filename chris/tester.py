from chris.server import formatOutput
from modules import modules
from modules.modules import Basket


def get_cheapest_sub_baskets_list_of_baskets(products_quantity, num_sub_baskets=2):
    cheapest, missing = modules.cheapest_basket_with_quantity(products_quantity)
    # print(cheapest[0].store_name)
    second_cheapest, missing2 = modules.cheapest_basket_with_quantity(products_quantity, [cheapest.store_name])
    # print(second_cheapest[0].store_name)
    # store_names = getStoresNames()
    # dict_of_stores = getDictionaryofStores()
    # baskets = {}
    # baskets[cheapest.store_name] = Basket(cheapest.store_name)
    # baskets[second_cheapest.store_name] = Basket(second_cheapest.store_name)
    missing = []
    for product in products_quantity:
        # print(product)
        if product in cheapest.item_to_price and product in second_cheapest.item_to_price:
            price_product = cheapest.item_to_price[product]
            price_product_second_cheapest = second_cheapest.item_to_price[product]
            if price_product < price_product_second_cheapest:
                second_cheapest.delete_item_quantity_new_setup(
                    price_product_second_cheapest, product, second_cheapest.item_to_quantity[product])
            else:
                cheapest.delete_item_quantity_new_setup(
                    price_product, product, cheapest.item_to_quantity[product])

        if product not in cheapest.item_to_price and product not in second_cheapest.item_to_price:
            missing.append(product)
    return [cheapest, second_cheapest], missing


if __name__ == '__main__':
    x, missing = get_cheapest_sub_baskets_list_of_baskets({
            'Sauce': 1,
            'Apple Juice': 1,
            'Bacon': 1,
            'Beef Stew Meat': 1,
            'Honey': 2
        })
    for y in x:
        print(formatOutput(y))

    print('DISCOUNT AFTER 5:')
    print(modules.cheapest_basket_with_quantity({'Beef Stew Meat': 5}))