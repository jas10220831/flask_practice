from flask import request
import requests
from decouple import config

YOUTBUE_KEY = config('YOUTUBE_KEY')


def search_yotube(search_word):
  search_url = 'https://www.googleapis.com/youtube/v3/search'
  video_url = 'https://www.googleapis.com/youtube/v3/videos'


  search_params = {
      'key' : YOUTBUE_KEY,
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
      'key' : YOUTBUE_KEY,
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

  return videos