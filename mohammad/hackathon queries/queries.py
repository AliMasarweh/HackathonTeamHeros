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


def getStoresNames():
    try:
        with connection.cursor() as cursor:
            query = f'select stores.storename from stores'
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getStoresProductsList():
    try:
        with connection.cursor() as cursor:
            query = f'select s.storename, p.productname, sp.price from stores_products as sp, stores as s, products as p where s.storeid=sp.storeid and p.productid = sp.productid'
            cursor.execute(query)
        list = cursor.fetchall()
        return list
    except:
        print("Could insert stores into DB")


def getDictionaryofAllStoresUnused():
    # list_of_all = []
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


def getDictionaryofStores():
    dict_of_stores = {}
    items_list = getStoresProductsList()
    stores_list = getStoresNames()
    for stores in stores_list:
        dict_of_stores[stores['storename']] = {}
        for item in items_list:
            if item['storename'] == stores['storename']:
                dict_of_stores[stores['storename']][item['productname']] = item['price']
    return dict_of_stores


if __name__ == '__main__':
    items_list = getStoresProductsList()
    markets_list = getStoresNames()
    print(markets_list)
    list_of_all_markets = getDictionaryofStores()
    print(list_of_all_markets)