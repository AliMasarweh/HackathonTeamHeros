from mohammad.hackathon_queries.queries import *


store_names = getStoresNames()
dict_of_stores = getDictionaryofStores()
for store in store_names:
    print(dict_of_stores[store['storename']])
