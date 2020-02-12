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


def setDiscountAndMinQuantity(store_name, item_to_discount_with_min_quantity):
    queries.getStoresProductsList()


if __name__ == '__main__':
    print(queries.getDictionaryofStores('Walmart'))
