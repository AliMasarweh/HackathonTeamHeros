from flask import Flask, Response, request
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from mohammad.hackathon_queries.queries import *
from modules.modules import *
from modules import modules
TOKEN = '1079063242:AAFrv70HEXPqF6tT9g6naYd6LyWZUnkePas'
expected_input = False


def start():
    TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://556d8f6a.ngrok.io/message'.format(
        TOKEN)
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)


setting_offers = False

app = Flask(__name__)

def ShowSales():
    outstr = ""
    list_of_sales = getSales()
    for sale in list_of_sales:
        outstr += "store: " + sale['storename'] + " "
        outstr += "product: " + sale['productname'] + " "
        outstr += "quantity for sale: " + str(sale['quantity']) + " "
        outstr += "sale percent: " + str(sale['salepercent']) + "% " + '\n\n'
    return outstr

def formatOutput(listofoutput, missing_items_output=""):
    print(listofoutput)
    print(missing_items_output)
    output_str = ""
    output_str += f'store name: {listofoutput.store_name}\n'
    list_of_products = listofoutput.item_to_price
    output_str += f'      list of items\n'
    for item in list_of_products:
        output_str += f'{item} : {listofoutput.item_to_price[item]:.2f}$ \n'
    output_str += f'total basket price : {listofoutput.basket_price:.2f}$  \n'
    if missing_items_output:
        output_str += "could not find in the store\n" + missing_items_output + '\n'
    return output_str


def formatMissingItems(listofmissings):
    output_str = ""
    for missing in listofmissings:
        output_str += missing + " "
    return output_str


@app.route('/sanity')
def sanity(): return "Server is running"


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def removeKeyboard(chat_id):
    x = ReplyKeyboardRemove()
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "", x.to_json()))


def add_product_checkout(chat_id):
    keyboard = [
        ["add product"], ['remove product from basket'], ["check out"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}&disable_commands=True"
                 .format(TOKEN, chat_id, "please choose your selection", x.to_json()))


def getUsersFeatures(chat_id):
    keyboard = [
        ["get cheapest basket"],["get sub baskets"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "Press button to get a feature ", x.to_json()))


def getTextChatId(request_json):
    if 'edited_message' in request_json:
        chat_id = request_json['edited_message']['chat']['id']
        text = request_json["edited_message"]["text"]
    elif 'callback_query' not in request_json:
        chat_id = request_json['message']['chat']['id']
        text = request_json['message']['text']
    elif 'callback_query' in request_json:
        chat_id = request_json['callback_query']['message']['chat']['id']
        text = request_json['callback_query']['data']
    else:
        text = 'nothing useful'
        chat_id = 0
    return text, chat_id


def getPreviousBasket(basket: dict):
    outstr = ""
    keys = basket.keys()
    for key in keys:
        outstr += key + " "
        outstr += str(basket[key])
        outstr += '\n'

    return outstr


def getPreviousBasketFeatures(chat_id):
    keyboard = [
        ["add more items"], ["checkout on the same basket"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "Please choose one of the options", x.to_json()))


def getStart(chat_id):
    keyboard = [
        ["create basket"], ["get recent basket"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "Please choose a new basket or the most recent basket", x.to_json()))


def sendmsgstoallclients(msgs):
    all_accesses = getAllUsersAccess()
    print(type(all_accesses))
    keys = all_accesses.keys()
    for msg in msgs:
        for key in keys:
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, key, msg))


msgs = []


@app.route('/message', methods=["POST"])
def handle_message():
    global setting_offers
    global expected_input
    print("****got message***")
    request_json = request.get_json()
    text, chat_id = getTextChatId(request_json)
    removeKeyboard(chat_id)
    print(text, chat_id)
    if not setting_offers:
        if text.lower() == "start":
            getStart(chat_id)
        elif text == 'create basket':
            restoreUsersBasket(chat_id)
            add_product_checkout(chat_id)
        elif text == "add product":
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id,
                                 "add product and quantity by inserting '/' followed by the product name then tab and "
                                 "after that quantity (default quantity is 1)\nfor example:\n/applejuice 3"))
            expected_input = True
        elif text == 'sign me up':
            insertClientUser(chat_id)
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id, 'Congratulations!! you have been signed up for our sales notifications'))
        elif text[0] == "/":
            if expected_input:
                command = text.strip("/")
                command_split = command.split()
                print(command_split)
                if len(command_split) == 2:
                    quantity = int(command_split[1])
                    insertBasketElementintoDB(chat_id, getProductName(command_split[0]), quantity)
                else:
                    insertBasketElementintoDB(chat_id, getProductName(command_split[0]), 1)
                add_product_checkout(chat_id)
            else:
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, 'You should select the options below before adding products to '
                                                     'your basket'))
        elif text == 'check out':
            expected_input = False
            print(getUsersBasket(chat_id))
            getUsersFeatures(chat_id)
        elif text == 'remove product from basket':
            removeFromBasket(chat_id, 'product_name')

        elif text == 'get cheapest basket':
            x, y = cheapest_basket(getUsersBasket(chat_id))
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id,
                                 formatOutput(x, formatMissingItems(y))))
        elif text == 'get sub baskets':
            x = get_cheapest_sub_baskets(getUsersBasket(chat_id), 1)
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id,
                                x))
        elif text == 'get recent basket':
            basket = getUsersBasket(chat_id)
            if getUsersBasket(chat_id):
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id,
                                     getPreviousBasket(basket)))
                getPreviousBasketFeatures(chat_id)
            else:
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, "no previous basket"))
        elif text == 'add more items':
            add_product_checkout(chat_id)
        elif text == 'checkout on the same basket':
            getUsersFeatures(chat_id)
        elif text == 'set offers':
            access = getUserAccess(chat_id)
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id, "You can now add offers"))
            if access == 'admin':
                setting_offers = True
            else:
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, "You do not have access to do this operation"))
        elif text == 'sales':
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id,ShowSales()))

    else:
        if text == 'end offers':
            print(msgs)
            sendmsgstoallclients(msgs)
            msgs.clear()
            setting_offers = False
        else:
            msgs.append(text)

    return Response("success")


def get_cheapest_sub_baskets(products_quantity, num_sub_baskets=2):
    cheapest = modules.cheapest_basket(products_quantity)
    # print(cheapest[0].store_name)
    second_cheapest = modules.cheapest_basket(products_quantity, [cheapest[0].store_name])
    # print(second_cheapest[0].store_name)
    # store_names = getStoresNames()
    # dict_of_stores = getDictionaryofStores()
    baskets = {}
    baskets[cheapest[0].store_name] = [[], 0]
    baskets[second_cheapest[0].store_name] = [[], 0]
    for product in products_quantity:
        # print(product)
        price_product = getPriceOfOneItem(product)
        price_product.update((x, y * products_quantity[product]) for x, y in price_product.items())
        if price_product[cheapest[0].store_name] < price_product[second_cheapest[0].store_name]:
            min_store = cheapest[0].store_name
        else:
            min_store = second_cheapest[0].store_name
        baskets[min_store][0].append(product)
        baskets[min_store][1] += price_product[min_store]
    return baskets



if __name__ == '__main__':
    start()
    app.run(debug=True, port=5002)
