from flask import (Flask,
     redirect, render_template, request, url_for,
     jsonify
     
     )
from decouple import config


from pprint import pprint

from send_message import *
from news_summarize import * 


app = Flask(__name__)
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

DEBUG = True

@app.route('/', methods=['GET', 'POST'])
def hello_world():
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
    # if request.method == 'POST':
    #     search_word = request.form['search_word']
    #     articles = make_articles(search_word)
    #     # print(articles)
    #     return jsonify(articles)
    # else:
    #     print('get요청 들어옴')
    #     return 
    search_word = request.args.get('search_word', 'None', type=str)
    articles = make_articles(search_word)
    return jsonify(result=articles)

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 5000)