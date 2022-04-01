
from decouple import config
import requests

from news_summarize import *

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


def send(text, chat_id):
  send_url = f'{bot_url}sendMessage?text={text}&chat_id={chat_id}'
  requests.get(send_url)
  return 

def greeting(chat_id):
    text = "안녕하세요 \n 검색어를 입려해주세요 "
    send(text, chat_id)

    return 

def send_title(article_list, chat_id):
  word = '어떤 기사를 요약해 드릴까요? 번호를 말해주세요 \n'
  for i in range(len(article_list)):
    word += str(i+1)+'.  ' + article_list[i]['news_title'] + '\n'
  send(word, chat_id)

  # TODO 메세지를 보내고 다음에 이어지는 응답을 보내기 위해서 어떻게 해야 될까?
  return 