from pykrx import stock, bond
from pprint import pprint
import datetime as dt

# 종목 이름이랑 번호 bind해서 dict로 만들기 
# 처음에만 돌려서 다음에는 작동하지 않고 참조만 하도록 

tickers = stock.get_market_ticker_list()

stock_list = []

for ticker in tickers:
    stock_name = stock.get_market_ticker_name(ticker)
    stock_list.append({
        'name' : stock_name,
        'number' : ticker,
    })


def search_stock(search_word):
    # 오늘 날짜 가져오기
    # YYYYMMDD
    today_date = dt.datetime.now().strftime("%Y%m%d")

    # 검색 종목의 종목번호
    target_numb = ''

    for target in stock_list:
        if target['name'] == search_word:
            target_numb = target['number']

    # 삼성전자 번호
    # target_numb = '005930'

    df = stock.get_market_ohlcv("20180810", today_date, target_numb, "d")

    return df.tail(3)


