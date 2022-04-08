from flask import (Flask,
     redirect, render_template, request, url_for,
     jsonify
     
     )
from decouple import config


from send_message import *
from news_summarize import * 
from youtbe_search import *
from stock import *


app = Flask(__name__)
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
YOUTBUE_KEY = config('YOUTUBE_KEY')
chat_id = config('chat_id')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # print(WEBHOOK_URL)
    # flag를 하나 만들어두고 채워질 떄 마다 시나리오 진행되도록 하자 
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

@app.route('/news_summarize_send', methods=['POST', 'GET'])
def news_summarize_send():
    article_url = request.json['url']
    result = summarize_article(article_url)
    data = {
        'content' : result
    }
    send(result, chat_id)
    return jsonify(summarized=data)


@app.route('/youtube_search', methods=['GET', 'POST'])
def youtube_search():
    search_word = request.args.get('search_word', 'None', type=str)
    if search_word:
        videos = search_yotube(search_word)
        return jsonify(videos=videos)
    else:
        return redirect(url_for('hello_world'))

@app.route('/youtbe_send_telegram', methods=['GET', 'POST'])
def youtbe_send_telegram():
    send_url = request.json['url']
    send(send_url, chat_id)
    return '데이터 받음'

@app.route('/stock_search', methods=['GET', 'POST'])
def stock_search():
    search_word = request.args.get('search_word', 'None', type=str)
    response, stock_news = search_stock(search_word)
    if response :
        return jsonify(values=response, stock_news=stock_news)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 5000)