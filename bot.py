import requests
import misc
from time import sleep

from yobit import get_btc

token = misc.token

URL = f'https://api.telegram.org/bot{token}/'

global last_update_id
last_update_id = 0


def get_updates():
    url = f'{URL}getUpdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()
    last_object = data['result'][-1]

    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {
            'chat_id': chat_id,
            'text': message_text
        }

        return message
    return None


def send_message(chat_id, text='White a second, please...'):
    url = f'{URL}sendMessage?chat_id={chat_id}&text={text}'
    requests.get(url)


def main():
    answer = get_message()
    if answer:
        chat_id = answer['chat_id']
        text = str(answer['text'])
        if '/btc' == text.lower():
            send_message(chat_id, get_btc())
        else:
            send_message(chat_id, 'Привет')


if __name__ == '__main__':
    while True:
        main()
        sleep(2)
