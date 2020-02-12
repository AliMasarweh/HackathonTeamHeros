import pymysql
import json
from mohammad.hackathon_queries import queries

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="123123",
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


if __name__ == '__main__':
    setDiscountAndMinQuantity('Walmart', {'Aluminum  Foil': {'discount': 10.0, 'min_quantity': 2}})
