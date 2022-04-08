from flask import request
from pykrx import stock, bond
from pprint import pprint
import datetime as dt
from bs4 import BeautifulSoup
import requests
import re

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

    df = stock.get_market_ohlcv("20180810", today_date, target_numb, "d")


    # 오늘부터 영업일 7일 전까지의 종목 거래 정보 
    stock_info = []
    for i in range(7):
        one_day = {
            '날짜' : df.index[len(df)-1-i].strftime("%Y/%m/%d"),
            '시가' : str(df.values[len(df)-1-i][0]),
            '고가' : str(df.values[len(df)-1-i][1]),
            '저가' : str(df.values[len(df)-1-i][2]),
            '종가' : str(df.values[len(df)-1-i][3]),
            '거래량' : str(df.values[len(df)-1-i][4]),
        }
        stock_info.append(one_day)

    url = f'https://finance.naver.com/item/news_news.nhn?code={target_numb}&page=1' 
    source_code = requests.get(url).text
    html = BeautifulSoup(source_code, "lxml")
    
    # 뉴스 제목 
    titles = html.select('.title')
    title_result=[]
    for title in titles: 
        title = title.get_text() 
        title = re.sub('\n','',title)
        title_result.append(title)


    # 뉴스 링크
    links = html.select('.title') 

    link_result =[]
    for link in links: 
        add = 'https://finance.naver.com' + link.find('a')['href']
        link_result.append(add)


    # 뉴스 날짜 
    dates = html.select('.date') 
    date_result = [date.get_text() for date in dates] 


    # 뉴스 매체     
    sources = html.select('.info')
    source_result = [source.get_text() for source in sources] 
    
    stock_news = []
    for i in range(8):
        one_news = {
            '날짜' : date_result[i],
            '제목' : title_result[i],
            '언론사' : source_result[i],
            '링크' : link_result[i],
        }
        stock_news.append(one_news)

    return stock_info, stock_news

