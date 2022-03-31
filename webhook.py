import requests
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')

bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

webhook_url = f'{bot_url}setWebhook?url={WEBHOOK_URL}'
response = requests.get(webhook_url)

print(response)