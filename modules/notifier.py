from mohammad.hackathon_queries import queries

def announce_sale(chat_id: int, item_to_discount_with_min_quantity):
    store_name = queries.getUserTypeByChatId(chat_id)
    if store_name == "client":
        return "A mere client shouldn't try this thing!"



def notify_sales(chat_id: int):
    pass
