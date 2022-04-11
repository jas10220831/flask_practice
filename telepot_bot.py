import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup as MU
from telepot.namedtuple import InlineKeyboardButton as BT

                                
from decouple import config
from pprint import pprint
import time

from stock import *
from news_summarize import * 

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
chat_id = config('chat_id')

bot = telepot.Bot(TELEGRAM_TOKEN)

# 현재 어떤 기능 제공 중인지 알려주기 
now_flag = {'state': None, 'stage':None}

bot.sendMessage(chat_id, text="'시작'을 입력하여 기능 동작")

def btn_show(msg):
    global now_flag

    # 현재 기능별로 검색어를 입력 받고 전달 
    if now_flag['state'] == None:
        if msg['text'] == '시작':
            btn1 = BT(text = "주식", callback_data = "주식")
            btn2 = BT(text = "뉴스", callback_data = "뉴스")
            cancel_btn = BT(text='Cancel', callback_data="cancel")
            mu = MU(inline_keyboard = [[btn1, btn2], [cancel_btn]])
            bot.sendMessage(chat_id, "원하시는 기능을 선택하세요", reply_markup = mu)
        
    elif now_flag['state'] == '주식':
        # callback_data로 주식 종목을 전달한다. 
        target_stock = msg['text']
        # 주식 리스트에 있을 경우 결과값 보내주기
        if target_stock in stock_name_list:
            btn1 = BT(text = "가격 변동 조회", callback_data = f"가격,{target_stock}")
            btn2 = BT(text = "관련 뉴스 조회", callback_data = f"뉴스,{target_stock}")
            cancel_btn = BT(text='Cancel', callback_data="cancel")
            mu = MU(inline_keyboard = [[btn1, btn2], [cancel_btn]])
            bot.sendMessage(chat_id, "원하는 기능을 선택하세요", reply_markup = mu)
        
        # TODO word2vec 통해서 종목간 유사도 검사하여 보내주기 
        else: # 없을 경우 대체 값 보내주기 
            bot.sendMessage(chat_id, "해당 종목이 없습니다")
    
    # 뉴스 기능 선택시 제목을 5가지 보여주고 선택
    elif now_flag['state'] == '뉴스':
        target_word = msg['text']
        bot.sendMessage(chat_id, text=f"{target_word}에 관한 가장 최근 기사입니다.")
        
        news_btn_list = []
        
        news_list = make_articles(target_word)
        for idx, news in enumerate(news_list):
            btn = BT(text = news['news_title'], callback_data = f"요약,{target_word},{idx}")
            news_btn_list.append([btn])
        cancel_btn = BT(text='Cancel', callback_data="cancel")
        news_btn_list.append([cancel_btn])
        mu = MU(inline_keyboard = news_btn_list)
        bot.sendMessage(chat_id, "기사 제목을 선택하시면 요약본이 나옵니다.", reply_markup = mu)


def query_ans(msg):
    global now_flag
    query_data = msg["data"]

    # cancel 입력시 상태 초기화
    if query_data == 'cancel':
        now_flag = {'state': None, 'stage':None}
        bot.sendMessage(chat_id, text = "취소되었습니다.\n시작을 입력하여 기능을 재시작합니다.")
        print("cancel을 눌렀습니다.")


    # 처음 시작시 보여주기
    if now_flag['state']  == None:
        if query_data == "주식":
            now_flag['state'] = '주식'
            bot.sendMessage(chat_id, text = "종목을 입력해주세요")
        elif query_data == "뉴스":
            now_flag['state'] = '뉴스'
            bot.sendMessage(chat_id, text = "검색어를 입력해주세요")
    
    # 주식 검색 기능 
    elif now_flag['state'] == '주식':
        query_data = query_data.split(',')
        target_stock = query_data[1]

        stock_info, stock_news = search_stock(target_stock)
        # 주식 가격 변동 조회기능
        # TODO 보기 쉽게 바꾸기
        price_result=''
        if query_data[0] == "가격":
            for info in stock_info:
                price_result += '날짜: ' + info['날짜'] + ' '
                price_result += '시가: ' + info['시가'] + ' '
                price_result += '고가: ' + info['고가'] + ' '
                price_result += '저가: ' + info['저가'] + ' '
                price_result += '종가: ' + info['종가'] + ' '
                price_result += '\n'
            bot.sendMessage(chat_id, text=f"{target_stock}의 7영업일 주가 변동")
            bot.sendMessage(chat_id, price_result )

        # 주식 관련 뉴스 조회 기능
        elif query_data[0] =="뉴스":
            stock_news_btn = [] 
            # 5개의 뉴스를 조회하며 버튼 생성 및 전송 
            for idx, news in enumerate(stock_news):
                btn = BT(text = news['제목'], url=news['링크'] ,callback_data =f'{idx}_stock_news' )
                stock_news_btn.append([btn])
            cancel_btn = BT(text='Cancel', callback_data="cancel")
            stock_news_btn.append([cancel_btn])
            mu = MU(inline_keyboard = stock_news_btn)
            bot.sendMessage(chat_id, f"{target_stock} 관련 뉴스 링크들 입니다. \n클릭하면 해당 기사로 이동합니다.", reply_markup = mu)
        
    # 뉴스 요약검색 기능
    elif now_flag['state'] == '뉴스':
        query_data = query_data.split(',')
        if query_data[0] == '요약':
            target_word = query_data[1]
            target_idx = int(query_data[2])
            target_news = make_articles(target_word)[target_idx]
            target_url = target_news['article_url']

            content_summarize = summarize_article(target_url)

            bot.sendMessage(chat_id, text=content_summarize)

MessageLoop(bot, {'chat': btn_show, "callback_query" : query_ans}).run_as_thread()

print('Listening')

while 1:
    time.sleep(10)