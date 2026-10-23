import requests	
import time
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'
res = requests.get(url)
sitemap = {}

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

html_soup = BeautifulSoup(res.text,'html.parser')
html_soup = BeautifulSoup(res.content,'html.parser')
print(f"html_soupの型:{type(html_soup)}")

print(html_soup.find_all(class_='url'))

for url in sitemap:
      key = html_soup.find_all(class_='url').text
      value = html_soup.find_all('title').text

      sitemap[key] = int(value)

print(sitemap)