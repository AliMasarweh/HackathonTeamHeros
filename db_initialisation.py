import pymysql
import json

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="123123",
    db="hackathon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("successfully connected ")
Stores_list = []
Products_list = []


def getJsonFile():
    with open('product_data.json', 'r+') as JsonProductFiles:
        DataFromAllMarkets = json.load(JsonProductFiles)
        return DataFromAllMarkets


def getStoresList(DataFromAllMarkets):
    for i in range(5):
        Stores_list.append(DataFromAllMarkets[i]['store'])
    return Stores_list


def getProductsList(DataFromAllMarkets):
    for product in DataFromAllMarkets:
        if product['product'] not in Products_list:
            Products_list.append(product['product'])
    return Products_list


def insertStorestoDB(Stores_list: list):
    try:
        with connection.cursor() as cursor:
            for store in Stores_list:
                query = f'INSERT into Stores values(default,"{store}")'
                cursor.execute(query)
            connection.commit()
    except:
        print("Could insert stores into DB")


def insertProductstoDB(Products_list: list):
    try:
        with connection.cursor() as cursor:
            for product in Products_list:
                query = f'INSERT into Products values (default,"{product}")'
                cursor.execute(query)
            connection.commit()
    except:
        print("Could insert products into DB")


def insertPricestoDB(DataFromAllMarkets):
    try:
        with connection.cursor() as cursor:
            for Product in DataFromAllMarkets:
                if Product["price"] != 'N/A':
                    price = Product["price"].strip("$")
                    query = f'INSERT into Stores_Products values ((select StoreId from Stores where StoreName = "{Product["store"]}"),' \
                            f'(select ProductId from Products where ProductName = "{Product["product"]}"),{price})'
                    cursor.execute(query)
            connection.commit()
    except:
        print("Could insert Prices into DB")


def insertClientUser(chat_id: int, user_type='default'):
    try:
        with connection.cursor() as cursor:
            query = f'insert into Users values({chat_id}, "{user_type}")'
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print(e)
        return "failed to insert"

    return "successful"


def insertCodedProducts():
    with open('product.txt', 'r+') as coded_products:
        for line in coded_products.readlines():
            print(line)
            line_codes = line.strip('\n').split(' - ')
            try:
                with connection.cursor() as cursor:
                    query = f'INSERT into coded_products values("{line_codes[0]}","{line_codes[1]}")'
                    cursor.execute(query)
            except:
                print("Could insert stores into DB")
        connection.commit()


if __name__ == '__main__':
    DataFromAllMarkets = getJsonFile()
    insertProductstoDB(getProductsList(DataFromAllMarkets))
    insertStorestoDB(getStoresList(DataFromAllMarkets))
    insertPricestoDB(DataFromAllMarkets)
    insertCodedProducts()
    print('done')
