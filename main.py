import json
import re

from flask import Flask
from flask import request
from flask import jsonify

import requests
import misc

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

token = misc.token

URL = f'https://api.telegram.org/bot{token}/'


def parse_text(text):
    """
    Вычленение из сообщения названия криптовалюты.
    /bitcoin
    :param text:
    :return:
    """
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    """
    Полчение курса криптовалюты с coinmarketcap
    :param crypto:
    :return:
    """
    url = f'https://api.coinmarketcap.com/v1/ticker/{crypto}/'
    print(url)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price


def send_message(chat_id, text='White a second, please...'):
    """
    Отправка сообщения
    :param chat_id:
    :param text:
    :return:
    """
    url = f'{URL}sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    return requests.post(url, json=answer)


def set_web_hook(webhook_url=f'https://alexvakhov.pythonanywhere.com/{token}'):
    """
    Регистрация бота
    :param webhook_url:
    :return:
    """
    url = f'{URL}setWebhook?url={webhook_url}'
    return requests.get(url)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


@app.route(f'/{token}', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        pattern = r'/\w+'
        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, price)
        return jsonify(r)
    else:
        set_web_hook()
        return '<h1>Bots welcomes you</h1>'


if __name__ == '__main__':
    set_web_hook()
    app.run()
