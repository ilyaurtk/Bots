import requests
from bs4 import BeautifulSoup as BS

r = requests.get('https://моб.екатеринбург.рф/663/news/')
html = BS(r.content, 'html.parser')

for el in html.select('.news-hold'):
	title = el.select('.news-list > a')
	print( title )