import pymysql
import json
from mohammad.hackathon_queries import queries

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="hackathon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def setDiscountAndMinQuantity(store_name, item_to_quant_disc):
    store = queries.getDictionaryofStoresWithQuantityDiscount(store_name)[store_name]
    try:
        with connection.cursor() as cursor:
            for item in store:
                if item in item_to_quant_disc:
                    discount = item_to_quant_disc[item]['discount']
                    min_quant = item_to_quant_disc[item]['min_quantity']

                    query = f'update Stores_Products SET Discount = {discount}, MinQuantity = {min_quant} where ' \
                            f'ProductID = (select ProductID from Products where ProductName = "{item}")' \
                            f'and StoreID = (select StoreID from Stores where StoreName = "{store_name}")'
                    cursor.execute(query)
                connection.commit()
    except Exception as e:
        print(e)
        print("Could not insert stores into DB")

def getUsersAndTypes():
    try:
        with connection.cursor() as cursor:
            query = 'select * from Users'
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(e)
        print("Could not insert stores into DB")

def announce_sale(chat_id: int, item_to_quant_disc):
    store_name = queries.getUserTypeByChatId(chat_id)
    if store_name == "client":
        return "A mere client shouldn't access discount!"
    setDiscountAndMinQuantity(store_name, item_to_quant_disc)
    notify_sales(item_to_quant_disc)


def notify_sales(item_to_quant_disc):
    users = getUsersAndTypes()
    for user in users:
        print(user)
        print(user['ChatId'], user['UserType'])
        if user['UserType'] == 'client':
            pass
            # notify_user(user['ChatId'], item_to_quant_disc)


if __name__ == '__main__':
    setDiscountAndMinQuantity('Walmart', {'Aluminum  Foil': {'discount': 10.0, 'min_quantity': 2}})
    notify_sales(None)
