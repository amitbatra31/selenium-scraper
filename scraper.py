import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from selenium.webdriver.common.action_chains import ActionChains
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
  actions = ActionChains(driver)
  target = video.find_element(By.ID,'video-title')
  actions.move_to_element(target)
  actions.perform()
  title_tag = video.find_element(By.ID,'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')
  thumbnail_url = video.find_element(By.TAG_NAME,'img').get_attribute('src')
  channel_name = video.find_element(By.CLASS_NAME,'ytd-channel-name').text
  views = video.find_elements(By.CLASS_NAME,'ytd-video-meta-block')[0].find_elements(By.TAG_NAME,'span')[1].text
  upload_time =  video.find_elements(By.CLASS_NAME,'ytd-video-meta-block')[0].find_elements(By.TAG_NAME,'span')[-1].text
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

def send_email(body):
  
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()   # optional
    # ...send emails
    SENDER_EMAIL='batracodes@gmail.com'
    RECEIVER_EMAIL='batracodes@gmail.com'
    SENDER_PASSWORD=os.environ['GMAIL_PASSWORD']
    subject = 'Text Message from Replit'
  

    email_text = f"""\
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}

    {body}
    """
    server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    server_ssl.close()

    print('Email sent!')
  except:
    print('Something went wrong...' )

def send_email_attached(body):

  # instance of MIMEMultipart
  msg = MIMEMultipart()

  # storing the senders email address
  SENDER_EMAIL='batracodes@gmail.com'
  RECEIVER_EMAIL='batracodes@gmail.com'
  SENDER_PASSWORD=os.environ['GMAIL_PASSWORD']

  # storing the subject
  msg['Subject'] = "Top 10 Trending Youtube videos"

  # string to store the body of the mail
  

  # attach the body with the msg instance
  msg.attach(MIMEText(body, 'plain'))

  # open the file to be sent
  filename = "trending.csv"
  attachment = open("./trending.csv", "rb")

  # instance of MIMEBase and named as p
  p = MIMEBase('application', 'octet-stream')

  # To change the payload into encoded form
  p.set_payload((attachment).read())

  # encode into base64
  encoders.encode_base64(p)

  p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

  # attach the instance 'p' to instance 'msg'
  msg.attach(p)

  # creates SMTP session
  s = smtplib.SMTP('smtp.gmail.com', 587)

  # start TLS for security
  s.starttls()

  # Authentication
  s.login(SENDER_EMAIL, SENDER_PASSWORD)

  # Converts the Multipart msg into a string
  text = msg.as_string()

  # sending the mail
  s.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
  print('Email sent')
  # terminating the session
  s.quit()

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
  body="Please find attached top 10 trending videos in Youttube"
  send_email_attached(body)
  # print(parse_video(videos[0]))

  




   
  
