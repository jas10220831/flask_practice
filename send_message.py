
from decouple import config
import requests

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


def send(text, chat_id):
  send_url = f'{bot_url}sendMessage?text={text}&chat_id={chat_id}'
  requests.get(send_url)
  return 

def greeting():
    return '안녕하세요'

def news():
  pass

def stock():
  pass

def youtube():
  pass
