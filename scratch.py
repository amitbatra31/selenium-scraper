import requests
from bs4 import BeautifulSoup
YOUTUBE_TRENDING_URL="https://www.youtube.com/feed/trending"

response = requests.get(YOUTUBE_TRENDING_URL)
print("Status Code\t",response.status_code )

with open("trending.html","w") as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')
print('doc.title:', doc.title.string)

trend_vid_divs = doc.find_all('div',class_='style-scope ytd-video-renderer') 

print(f'Found {len(trend_vid_divs)} videos')