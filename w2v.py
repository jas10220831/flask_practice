from tabnanny import check
import warnings

from numpy import newaxis

from gensim.models import Word2Vec, fasttext
from pykrx import stock

tickers = stock.get_market_ticker_list(market='ALL')

stock_names = []

for ticker in tickers:
    stock_name = stock.get_market_ticker_name(ticker)
    stock_names.append(stock_name)

model = Word2Vec(sentences=stock_names, size=100, window=5, min_count=1, workers=2, sg=0)
model_result = model.wv.most_similar("삼성전자")
print(model_result)



