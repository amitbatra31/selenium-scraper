import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"
def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  return webdriver.Chrome(options=chrome_options)

def get_videos(driver):
  print('Get Video divs')
  VIDEO_TAG = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME,VIDEO_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID,'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')
  thumbnail_url = video.find_element(By.TAG_NAME,'img').get_attribute('src')
  channel_name = video.find_element(By.CLASS_NAME,'ytd-channel-name').text
  views = video.find_elements(By.CLASS_NAME,'ytd-video-meta-block')[0].find_elements(By.TAG_NAME,'span')[1].text
  upload_time =  video.find_elements(By.CLASS_NAME,'ytd-video-meta-block')[0].find_elements(By.TAG_NAME,'span')[2].text
  description = video.find_element(By.ID,'description-text').text

  return {
    'title':title,
    'url':url,
    'thumbnail url':thumbnail_url,
    'channel name':channel_name,
    'views':views,
    'upload time':upload_time,
    'description':description,
  }
if(__name__=='__main__'):
  print('Creating driver')
  driver = get_driver()
  print('Fetching Page')
  driver.get(YOUTUBE_TRENDING_URL)
  print('Page title',driver.title)
  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')
  print('Parsing top ten videos')
  
  video_data = [parse_video(video) for video in videos[:10]]
  print('Saving Data to CSV')
  video_df = pd.DataFrame(video_data)
  print(video_df)
  video_df.to_csv('trending.csv',index=None)
  




   
  
