from flask import Flask, request
from decouple import config

import requests
from pprint import pprint

app = Flask(__name__)
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        pprint(request.get_json())
        return '', 200
    else:
        return 'hello worlasdfd' 

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 5000)