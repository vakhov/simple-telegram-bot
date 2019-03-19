import requests


def get_btc():
    """
    Курс криптовалюты с yobit
    :return:
    """
    url = 'https://yobit.net/api/2/btc_usd/ticker'
    response = requests.get(url).json()
    price = response['ticker']['last']
    return f'{price} usd'


if __name__ == '__main__':
    while True:
        print(get_btc())
