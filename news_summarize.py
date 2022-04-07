from tabnanny import check
import warnings

from numpy import newaxis
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.summarization import summarize
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import re 


NAVER_NEWS_URL = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='


# 사용자에게 보여줄 최신 뉴스 5개를 제목과 url을 뽑아서 보내준다 
def make_articles(text):

  target_html = requests.get(NAVER_NEWS_URL+text)
  soup = BeautifulSoup(target_html.text, 'html.parser')

  check_list = []
  # Beautiful Soup로 기사 페이지에서 기사들 몇가지 링크 가져오기

  news_titles = []
  news_urls = []
  news_thumbs = []


  for link in soup.find_all('a', {'class' : 'news_tit'})[:5]:
    href = link.get('href')
    news_title = link.get('title')
    news_urls.append(href)
    news_titles.append(news_title)

  thumbs = soup.find_all('img', {'class' : 'thumb api_get'})
  for thumb in thumbs[:5]:
    img_url = thumb.get('src')
    news_thumbs.append(img_url)

  for i in range(5):
    check_list.append({
      'news_title' : news_titles[i], 
      'article_url' : news_urls[i],
      'img_url' : news_thumbs[i],
      })
  return check_list

make_articles('한화이글스')

# 사용자가 선택한 뉴스를 요약
def summarize_article(article_url):
  # 기사들 링크를 newpaper 패키지를 통해 본문 뽑아오기
  article = Article(article_url, language='ko')
  article.download()
  article.parse()
  result = summarize(article.text, word_count=50)
  

  content_summarize = ''
  # 요약이 아될 경우 그냥 본문 전달
  if result:
    content_summarize = result
  else:
    content_summarize = article.text
  
  return content_summarize

# article_list = make_articles('한화이글스')
# # print(article_list)
# word = ''
# for i in range(len(article_list)):
#   word += str(i+1)+'번' + article_list[i]['news_title'] + '\n'

# print(word)

# print(summarize_article('https://biz.chosun.com/policy/politics/2022/04/07/IMJSR6VV2VDAPJHHEB4ZAVQVFE/?utm_source=naver&utm_medium=original&utm_campaign=biz'))

  # links = soup.find_all('div', {'class' : "news_wrap api_ani_send"})
  # # links = soup.find_all(href=re.compile("https://news.naver.com/main/read.naver?"))
  # for link in links[:5]:
  #   if "네이버뉴스" in link.get_text() :
  #     # print(link)
  #     # print(type(link))
  #     # print('-------------------------------------------')
  #     little_soup = BeautifulSoup(str(link), 'html.parser')
  #     naver_url = little_soup.find_all(href=re.compile("https://news.naver.com/main/read.naver?"))
  #     news_title = little_soup.find_all('a', {'class' : 'news_tit'})
  #     thumbs = little_soup.find_all('img', {'class' : 'thumb api_get'})
  #     print(naver_url, news_title, thumbs)