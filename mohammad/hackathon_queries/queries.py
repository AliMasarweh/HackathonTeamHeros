import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="hackathon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("successfully connected ")


def getStoresNames(store_name:str = None):
    try:
        with connection.cursor() as cursor:
            if store_name:
                query = f'select stores.storename from stores where stores.storename = "{store_name}"'
            else:
                query = f'select stores.storename from stores'
            cursor.execute(query)
        list = cursor.fetchall()
        print(list)
        return list
    except:
        print("Could insert stores into DB")


def getStoresProductsList():
    try:
        with connection.cursor() as cursor:
            query = f'select s.storename, p.productname, sp.price from stores_products as sp, stores as s, products ' \
                    f'as p where s.storeid=sp.storeid and p.productid = sp.productid '
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getStoresProductsListWithQuantityDiscount():
    try:
        with connection.cursor() as cursor:
            query = f'select s.storename, p.productname, sp.price, sp.discount, sp.minquantity from stores_products' \
                    f' as sp, stores as s, products as p where s.storeid=sp.storeid and p.productid = sp.productid '
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getDictionaryofAllStoresUnused():
    dict_of_stores = {}
    items_list = getStoresProductsList()
    stores_list = getStoresNames()
    for stores in stores_list:
        dict_of_stores[stores['storename']] = []
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']].append(
                    {'product_name': item['productname'], 'price': item['price']})
    return dict_of_stores


def getDictionaryofStores(store_name: str = ""):
    dict_of_stores = {}
    items_list = getStoresProductsList()
    if store_name:
        stores_list = getStoresNames(store_name)
    else:
        stores_list = getStoresNames()

    print(stores_list)
    for stores in stores_list:
        dict_of_stores[stores['storename']] = {}
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']][item['productname']] = item['price']
    return dict_of_stores


def getDictionaryofStoresWithQuantityDiscount(store_name: str = ""):
    dict_of_stores = {}
    items_list = getStoresProductsListWithQuantityDiscount()
    if store_name:
        stores_list = getStoresNames(store_name)
    else:
        stores_list = getStoresNames()
    print(stores_list)
    for stores in stores_list:
        dict_of_stores[stores['storename']] = {}
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']][item['productname']] = \
                    {'price': item['price'], 'discount': item['discount'], 'min_quantity': item['minquantity']}
    return dict_of_stores


def getPriceOfOneItem(item: str):
    dict_of_prices = {}
    try:
        with connection.cursor() as cursor:
            query = f'select p.productName, sp.price, s.storename from stores_products as sp, products as p, ' \
                    f'stores as s where p.productid = sp.productid and p.productname = "{item}" and s.storeid = ' \
                    f'sp.storeid '
            cursor.execute(query)
        list = cursor.fetchall()
        list_of_stores = getStoresNames()
        for store in list_of_stores:
            for product in list:
                if product['storename'] == store['storename']:
                    dict_of_prices[store['storename']] = product['price']
        return dict_of_prices
    except:
        print("Could not get item price from DB")


def getProductName(ProductCode: str):
    try:
        with connection.cursor() as cursor:
            query = f'select productname from coded_products where productcode = "{ProductCode}"'
            cursor.execute(query)
            Productname = cursor.fetchall()
            return Productname[0]['productname']
    except:
        print(f"could not get product name by code {ProductCode}")


def getUserTypeByChatId(chat_id: int):
    try:
        with connection.cursor() as cursor:
            query = f"select UserType from Users where ChatId = {chat_id}"
            cursor.execute(query)
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return "failed to insert"


def insertBasketElementintoDB(chatid, product, quantity):
    try:
        with connection.cursor() as cursor:
            query = f'insert into users_baskets values({chatid},(select products.productid from products where productname = "{product}"),{quantity})'
            cursor.execute(query)
            connection.commit()
    except:
        print("faild to insert this element to the basket")


def getUsersBasket(chatid):
    output_dict = {}
    try:
        with connection.cursor() as cursor:
            query = f'select p.productname, ub.quantity from products as p, users_baskets as ub where p.productid = ' \
                    f'ub.productid and ub.chatid = {chatid} '
            cursor.execute(query)
            list = cursor.fetchall()
            for data in list:
                output_dict[data['productname']] = data['quantity']
            return output_dict
    except:
        print("could not fetch users basket ")


def restoreUsersBasket(chat_id):
    try:
        with connection.cursor() as cursor:
            query = f'delete from users_baskets where users_baskets.chatid = {chat_id}'
            cursor.execute(query)
            connection.commit()
    except:
        print("failed to delete {} basket".format(chat_id))

if __name__ == '__main__':
    items_list = getStoresProductsList()
    markets_list = getStoresNames()
    list_of_all_markets = getDictionaryofStores()
    print(getPriceOfOneItem('apple sauce'))
    print(getProductName('applesgalabag'))
    print(markets_list)
    print(list_of_all_markets)
    print(getPriceOfOneItem('apple sauce'))
    print(getPriceOfOneItem('apple sauce'))
    for i in range(123, 130):
        print(getUserTypeByChatId(i))
