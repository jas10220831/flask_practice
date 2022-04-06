from flask import request
import requests
from decouple import config

YOUTUBE_KEY = config('YOUTUBE_KEY')


def search_yotube(search_word):
  search_url = 'https://www.googleapis.com/youtube/v3/search'
  video_url = 'https://www.googleapis.com/youtube/v3/videos'


  search_params = {
      'key' : YOUTUBE_KEY,
      'q' : search_word,
      'part' : 'snippet',
      'maxResults' : 5,
      'type' : 'video',
  }
  
  r = requests.get(search_url, params=search_params)
  results = r.json()['items']
  video_ids = []
  for result in results:
      video_ids.append(result['id']['videoId'])

  video_params = {
      'key' : YOUTUBE_KEY,
      'id' : ','.join(video_ids),
      'part' : 'snippet,contentDetails',
      'maxResults' : 5,
  }

  r = requests.get(video_url, params=video_params)
  results = r.json()['items']

  videos = [] 
  for result in results:
      video_data = {
          'id' : result['id'],
          'url' : f"https://www.youtube.com/watch?v={ result['id'] }" ,
          'thumbnail' : result['snippet']['thumbnails']['high']['url'],
          'duration' : result['contentDetails']['duration'],
          'title' : result['snippet']['title'],
      }
      videos.append(video_data)

  # # 유튜브 API 쿼리 초과로 일단 대체함 
  # videos = [{'id': 'TAXxZGYiuUU', 'url': 'https://www.youtube.com/watch?v=TAXxZGYiuUU', 'thumbnail': 'https://i.ytimg.com/vi/TAXxZGYiuUU/hqdefault.jpg', 'duration': 'PT1M48S', 'title': '한화이글스: 클럽하우스 4화 선공개 | "마지막 경고야"'}, {'id': 'ecWF2FjjzJs', 'url': 'https://www.youtube.com/watch?v=ecWF2FjjzJs', 'thumbnail': 'https://i.ytimg.com/vi/ecWF2FjjzJs/hqdefault.jpg', 'duration': 'PT9M14S', 'title': '영상편지온 척 하고 왓챠 다큐에 나온 본인 모습 보여주기'}, {'id': 'BKho4iQZm2Y', 'url': 'https://www.youtube.com/watch?v=BKho4iQZm2Y', 'thumbnail': 'https://i.ytimg.com/vi/BKho4iQZm2Y/hqdefault.jpg', 'duration': 'PT11M14S', 'title': '한화이글스: 클럽하우스 | 1화 10분 선공개'}, {'id': '8ZMvD1FfmhA', 'url': 'https://www.youtube.com/watch?v=8ZMvD1FfmhA', 'thumbnail': 'https://i.ytimg.com/vi/8ZMvD1FfmhA/hqdefault.jpg', 'duration': 'PT8M1S', 'title': '한화이글스 선발 투수 윤대경 선수 4,5 선발 우려를 지우는 피칭을 보여줍니다/루테라의 이글스 칼럼'}, {'id': 'DQKGInYM9j8', 'url': 'https://www.youtube.com/watch?v=DQKGInYM9j8', 'thumbnail': 'https://i.ytimg.com/vi/DQKGInYM9j8/hqdefault.jpg', 'duration': 'PT3H3M46S', 'title': '3월 8일｜KIA 타이거즈 연습경기 생중계｜vs 한화이글스'}]
  return videos