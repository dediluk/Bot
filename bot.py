from flask import Flask
from flask import jsonify
from flask import request
from flask_sslify import SSLify
import requests
import json
import re

app = Flask(__name__)
sslify = SSLify(app)
TG_TOKEN = "your token"
URL = "https://api.telegram.org/bot{}/".format(TG_TOKEN)


# def get_rate():
#     url = 'https://developerhub.alfabank.by:8273/partner/1.0.1/public/nationalRates?currencyCode=840,978'
#     response = requests.get(url)
#     print(type(response))
#     # usd_price = str(response["rates"][0]["rate"]) + " " + response["rates"][0]["iso"]
#     # eur_price = str(response["rates"][1]["rate"]) + " " + response["rates"][1]["iso"]
#     return response


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Привет'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id,
              'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    url = 'http://www.nbrb.by/API/ExRates/Rates/{}?ParamMode=2'.format(crypto)
    r = requests.get(url).json()
    print(r)
    price = '1 ' + str(r['Cur_Name']) + " = " + str(r['Cur_OfficialRate']) + " BYN"
    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        pattern = r'/\w+'
        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text=price)
        return jsonify(r)
    return '<h1>He1llo Bot</h1>'


if __name__ == '__main__':
    # main()
    app.run()
