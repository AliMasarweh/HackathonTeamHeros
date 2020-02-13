from flask import Flask, Response, request
import requests
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove
from mohammad.hackathon_queries.queries import *
from modules.modules import *

TOKEN = '1079063242:AAFrv70HEXPqF6tT9g6naYd6LyWZUnkePas'
expected_input = False

def start():
    TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://cd107ac3.ngrok.io/message'.format(
        TOKEN)
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)


app = Flask(__name__)


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
        ["add product"], ["check out"]
    ]
    x = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}&disable_commands=True"
                 .format(TOKEN, chat_id, "please choose your selection", x.to_json()))

    # button_list = [
    #     InlineKeyboardButton('add product', callback_data=2),
    #     InlineKeyboardButton('check out', callback_data=3)
    # ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    #
    # res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
    #                    .format(TOKEN, chat_id, "add product or checkout", reply_markup.to_json()))


def getUsersFeatures(chat_id):
    keyboard = [
        ["get cheapest basket"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "Press button to get a feature ", x.to_json()))
    # button_list = [
    #     InlineKeyboardButton('get cheapest basket', callback_data=4),
    #     # InlineKeyboardButton('get subbaskets', callback_data=5)
    # ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    #
    # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
    #              .format(TOKEN, chat_id, "choose your preference", reply_markup.to_json()))


command_list = {}


def getTextChatId(request_json):
    print(request_json)
    if 'edited_message' in request_json:
        chat_id = request_json['edited_message']['chat']['id']
        text = request_json["edited_message"]["text"]
    elif 'callback_query' not in request_json:
        chat_id = request_json['message']['chat']['id']
        text = request_json['message']['text']
        # print("message")
        # print(text)
        # print(request_json)
    elif 'callback_query' in request_json:
        chat_id = request_json['callback_query']['message']['chat']['id']
        text = request_json['callback_query']['data']
        # print("callback query")
        # print(text)
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
    # button_list = [
    #     InlineKeyboardButton('add more items', callback_data=7),
    #     InlineKeyboardButton('checkout on the same basket', callback_data=8)
    # ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    #
    # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
    #              .format(TOKEN, chat_id, "choose your preference", reply_markup.to_json()))


def getStart(chat_id):
    keyboard = [
        ["create basket"], ["get recent basket"]
    ]
    x = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "Please choose a new basket or the most recent basket", x.to_json()))
    # getStart(chat_id)
    # button_list = [
    #     InlineKeyboardButton('create basket', callback_data=1),
    #     InlineKeyboardButton('get recent basket', callback_data=6),
    # ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    #
    # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
    #              .format(TOKEN, chat_id, " xXx ", reply_markup.to_json()))


@app.route('/message', methods=["POST"])
def handle_message():
    global expected_input
    print("****got message***")
    request_json = request.get_json()
    text, chat_id = getTextChatId(request_json)
    removeKeyboard(chat_id)
    print(text)
    # filter_by_hashtag(chat_id)
    if text == "start":
        expected_input = False
        getStart(chat_id)
    elif text == 'create basket':
        restoreUsersBasket(chat_id)
        expected_input = True
        add_product_checkout(chat_id)
    elif text == "add product":
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                     .format(TOKEN, chat_id,
                             "add product and quantity by inserting '/' followed by the product name then tab and "
                             "after that quantity (default quantity is 1)\nfor example:\n/applejuice 3"))
        expected_input = True
    elif text[0] == "/":
        if expected_input:
            command = text.strip("/")
            command_split = command.split()
            print(command_split)
            if len(command_split) == 2:
                quantity = int(command_split[1])
                insertBasketElementintoDB(chat_id, getProductName(command_split[0]), quantity)
            else:
                insertBasketElementintoDB(chat_id, command_split[0], 1)
            add_product_checkout(chat_id)
        else:
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                         .format(TOKEN, chat_id,
                                 "Invalid input, please choose an option first"))
    elif text == 'check out':
        expected_input = False
        print(getUsersBasket(chat_id))
        getUsersFeatures(chat_id)
        # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
        #              .format(TOKEN, chat_id,
        #                      "finished"))
    elif text == 'get cheapest basket':
        expected_input = False
        x, y = cheapest_basket(getUsersBasket(chat_id))
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                     .format(TOKEN, chat_id,
                             formatOutput(x, formatMissingItems(y))))
    # elif text == '5':
    #     list_of_sub_baskets, missing = subbaskest(getUsersBasket(chat_id))
    #     for baskets in list_of_sub_baskets:
    #         requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    #                      .format(TOKEN, chat_id,
    #                              formatOutput(baskets, "")))
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

    return Response("success")


# def filter_by_hashtag(chat_id):
#     keyboard = [
#         ["yes"], ["No"]
#     ]
#     x = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
#     requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&reply_markup={}&keyboard={}"
#                  .format(TOKEN, chat_id, x.to_json(), keyboard))
#     return 0


if __name__ == '__main__':
    start()
    app.run(debug=True, port=5002)
