from mohammad.hackathon_queries import queries

def announce_sale(chat_id: int, item_to_discount):
    if queries.getUserTypeByChatId(chat_id) == "client":
        return "A mere client shouldn't try this thing!"



def notify_sales(chat_id: int):
    pass
