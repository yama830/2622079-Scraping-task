import requests	
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'
res = requests.get(url)

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

html_soup = BeautifulSoup(res.content,'html.paper')
print(f"html_soupの型:{type(html_soup)}")
