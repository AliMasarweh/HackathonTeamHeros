from flask import Flask, Response, request
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
TOKEN = '1079063242:AAFrv70HEXPqF6tT9g6naYd6LyWZUnkePas'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://bd511f12.ngrok.io/message'.format(TOKEN)


app = Flask(__name__)


@app.route('/sanity')
def sanity():return "Server is running"

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
def add_product_checkout(chat_id):
    button_list = [
        InlineKeyboardButton('add product', callback_data=2),
        InlineKeyboardButton('check out', callback_data=3)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                       .format(TOKEN, chat_id, "add product or checkout", reply_markup.to_json()))


command_list = {}

@app.route('/message', methods=["POST"])
def handle_message():
    print("****got message***")
    request_json = request.get_json()

    # print(request_json)
    try:

        chat_id = request_json['message']['chat']['id']
        text = request_json['message']['text']
        print("message")
        print(text)
        print(request_json)
    except KeyError:
        chat_id = request_json['callback_query']['message']['chat']['id']
        text = request_json['callback_query']['message']['reply_markup']['inline_keyboard'][0][0]['text']
        print("callback query")
        print(text)
        # print(chat_id)
        # print(request_json['reply_markup']['inline_keyboard'])

    if text == "start":
        button_list = [
            InlineKeyboardButton('create basket', callback_data=1),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                       .format(TOKEN, chat_id, "Press button to create basket ", reply_markup.to_json()))

    elif text == "create basket":
        add_product_checkout(chat_id)

    elif text == "add product" :
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "add product and quantity by inserting '/' followed by the product name then tab and after that quantity (default quantity is 1)\nfor example:\n/applejuice 3"))

    elif text[0] == "/":
        command = text.strip("/")
        command_split = command.split()
        if len(command_split) == 2:
            quantity = command_split[1]
        else:
            quantity = 1
        print(quantity)
        add_product_checkout(chat_id)

    # elif text == "check out":

    return Response("success")

if __name__ == '__main__':
    app.run(port=5002)
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)

