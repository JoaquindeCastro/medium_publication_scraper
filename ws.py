import requests
from bs4 import BeautifulSoup
import pandas

url = 'https://medium.com/cantors-paradise'
response = requests.get(url)
content = BeautifulSoup(response.content, 'html.parser')
container = content.find('div', attrs={'class':'js-collectionStream'})
a = container.findAll('a')

links = []

for link in a:
	link = link['href']
	links.append(link)

cleaned_links = []

for link in links:
	if "medium.com/cantors-paradise" in link:
		cleaned_links.append(link)

cleaned_links = list(dict.fromkeys(cleaned_links))

archive = []

for article_link in cleaned_links:
	post = {}
	response = requests.get(article_link)
	article = BeautifulSoup(response.content, 'html.parser')
	#title
	if article.find('h1',attrs={'class':'a8db'}):
		h1 = article.find('h1',attrs={'class':'a8db'})
	else:
		h1 = article.find('h1')
	article_title = h1.text
	#subtitle
	if article.find('h2', attrs={'class':'3dfe'}):
		h2 = article.find('h2', attrs={'class':'3dfe'})
	else:
		subh = article.findAll('h2')
		h2 = subh[1]
	article_subtitle=h2.text
	#img
	'''
	fig = article.find('figure')
	print(fig)
	'''
	img = article.find('img',attrs={'class':'s'})
	article_img = img['src']
	post = {
	'title':article_title,
	'subtitle':article_subtitle,
	'img': article_img,
	'link':article_link
	}
	archive.append(post)
print(archive)

