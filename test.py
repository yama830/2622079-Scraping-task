import requests	
import time
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'
res = requests.get(url)

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

html_soup = BeautifulSoup(res.text,'html.parser')
html_soup = BeautifulSoup(res.content,'html.parser')
print(f"html_soupの型:{type(html_soup)}")

a_all = html_soup.find_all("a")

url = []    #辞書の箱

for a in a_all:
    time.sleep(1)
    print(a.string)

