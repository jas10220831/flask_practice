from flask import Flask, request
from decouple import config

from pprint import pprint

from send_message import send

app = Flask(__name__)
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"





@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # print(WEBHOOK_URL)
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        message = request.get_json()['message']['text']
        if message == '안녕':
            print('get_greeting')
            send("안녕안녕", chat_id)
        return '', 200
    else:
        return 'hello worlasdfd' 


@app.route('/news')
def news():
    return '뉴스 페이지'

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 5000)