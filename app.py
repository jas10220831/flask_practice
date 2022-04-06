from re import search
from flask import (Flask,
     redirect, render_template, request, url_for,
     jsonify, json
     
     )
from decouple import config

import requests
from pprint import pprint

from send_message import *
from news_summarize import * 
from youtbe_search import *
from stock import *


app = Flask(__name__)
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
YOUTBUE_KEY = config('YOUTUBE_KEY')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

chat_id = ''

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    global chat_id
    # print(WEBHOOK_URL)
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        message = request.get_json()['message']['text']
        
        if message == '안녕':
           greeting(chat_id)
        else:
            article_list = make_articles(message)
            send_title(article_list, chat_id)

        return '', 200
    else:
        return render_template('index.html')

@app.route('/news_list', methods=['GET', 'POST'])
def news_list():
    search_word = request.args.get('search_word', 'None', type=str)
    articles = make_articles(search_word)
    return jsonify(result=articles)

@app.route('/news_summarize')
def news_summarize():
    return '뉴스 요약보여주기'

@app.route('/youtube_search', methods=['GET', 'POST'])
def youtube_search():
    search_word = request.args.get('search_word', 'None', type=str)
    print(search_word)
    if search_word:
        videos = search_yotube(search_word)
        return jsonify(videos=videos)
    else:
        return redirect(url_for('hello_world'))

@app.route('/youtbe_send_telegram', methods=['GET', 'POST'])
def youtbe_send_telegram():
    # localstorage에 저장된 데이터를 받고 전달
    # chat_id = response['message']['chat']['id']
    send_url = request.json['url']
    send(send_url, chat_id)
    return '데이터 받음'

@app.route('/stock_search', methods=['GET', 'POST'])
def stock_search():
    search_word = request.args.get('search_word', 'None', type=str)
    response = search_stock(search_word)
    print(response)
    return '<h1>Hello Wolrd</h1>'


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 5000)