from tabnanny import check
import warnings

from numpy import newaxis
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.summarization import summarize
from newspaper import Article
from bs4 import BeautifulSoup
import requests



NAVER_NEWS_URL = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='


# 사용자에게 보여줄 최신 뉴스 5개를 제목과 url을 뽑아서 보내준다 
def make_articles(text):

  target_html = requests.get(NAVER_NEWS_URL+text)
  soup = BeautifulSoup(target_html.text, 'html.parser')

  check_list = []
  # Beautiful Soup로 기사 페이지에서 기사들 몇가지 링크 가져오기
  for link in soup.find_all('a'):
    href = link.get('href')
    news_title = link.get('title')
    if news_title != None:
      check_list.append({
        'news_title' : news_title, 
        'article_url' : href,
        # 'img_url' : img_url,
        })
    elif len(check_list) > 5:
      break 

  return check_list


# 사용자가 선택한 뉴스를 요약
def summarize_article(content):
  # 기사들 링크를 newpaper 패키지를 통해 본문 뽑아오기
  article = Article(content['article_url'], language='ko')
  article.download()
  article.parse()
  content_summarize = summarize(article.text, word_count=50)
  
  # 요약이 아될 경우 그냥 본문 전달
  if content_summarize:
    return content_summarize
  else:
    return article.text

# article_list = make_articles('한화이글스')
# # print(article_list)
# word = ''
# for i in range(len(article_list)):
#   word += str(i+1)+'번' + article_list[i]['news_title'] + '\n'

# print(word)

# print(summarize_article(article_list[2]))