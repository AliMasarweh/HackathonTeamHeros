from flask import Flask, Response, request
import requests

from modules import modules

app = Flask(__name__)
TOKEN = '831015496:AAGDDnoJ-3v-DyJnsxfZvpr5S6k3woLtNag'


def start():
    TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://310310c6.ngrok.io/message'.format(
        TOKEN)
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)

def formatOutput(listofoutput):
    output_str = ""
    output_str += f'store name: {listofoutput.store_name}\n'
    list_of_products = listofoutput.item_to_price
    output_str += f'      list of items\n'
    for item in list_of_products:
        output_str += f'{item} : {listofoutput.item_to_price[item]}$ \n'
    output_str += f'total basket price : {listofoutput.basket_price}$  \n'
    return output_str


functionsDict = {
    'cheapest': modules.cheapest_basket
}


def parseMsg(msg: str):
    allWords = msg.split(',')
    if allWords[0].lower() not in functionsDict:
        return f"No related information to command {msg}"
    else:
        list_of_output,x = functionsDict[allWords[0].lower()](allWords[1:])
        formatOutput(list_of_output)
        return formatOutput(list_of_output)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    message_info = request.get_json()
    if "message" in message_info:
        chat_id = message_info['message']['chat']['id']
        namef = message_info['message']['chat']['first_name']
        namel = message_info['message']['chat']['last_name']
        print(namef,namel)
        message_body = message_info["message"]["text"]
    elif "edited_message" in message_info:
        chat_id = message_info['edited_message']['chat']['id']
        message_body = message_info["edited_message"]["text"]
    else:
        return "Error"
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                 .format(TOKEN, chat_id, parseMsg(message_body)))
    return Response("success")


if __name__ == '__main__':
    start()
    print("started")
    app.run(debug=True, port=5002)
