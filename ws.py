import requests
from bs4 import BeautifulSoup
import pandas
from datetime import datetime

# GET ACTUAL CONTENT
url='https://medium.com/feed/@joaquindecastro'
response = requests.get(url)
content = BeautifulSoup(response.content, 'html.parser')

# REMOVE UNNECESSARY STRINGS
content = str(content).replace('<![CDATA[','').replace(']]>','')
content = BeautifulSoup(content, 'html.parser')

# GET LIST OF ALL ARTICLES 
# FOUND IN <item> TAG
articles = content.find_all('item')

# CREATE ARRAY FOR ALL article_info
articles_all = []

# GET ARTICLE INFO PER ARTICLE
for a in articles:
	# GET TITLE
	title = str(a.find('title').text)
	# GET SUBTITLE
	for subtitle in a.find_all('p', attrs={'class':'medium-feed-snippet'}):
		subtitle = subtitle.text
	# GET IMG SOURCE
	for img in a.find_all('img', src=True):
		img = img['src']
	# GET DATE
	date = a.find('pubdate').text
	date = str(date).replace(' GMT','') # REMOVE GMT STRING
	date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S') # CONVERT date TO DATETIME OBJECT
	date = date.strftime('%Y-%m-%d') # CONVERT TO DJANGO DateField FORMAT
	# GET LINK TO MEDIUM ARTICLE
	for href in a.find_all('a', href=True):
		link = href['href']
	# GET PUBLISHER BASED ON LINK (eg medium.com/my-publication/article-slug)
	if 'towards-artificial-intelligence' in link:
		publisher = "Towards AI"
	elif 'cantors-paradise' in link:
		publisher = "Cantor's Paradise"
	elif 'mindreform' in link:
		publisher = 'MindReform'
	# GET LIST OF TAGS
	tags = []
	for tag in a.find_all('category'):
		tag = tag.text
		tags.append(tag)
	# PUT ALL INFO IN A DICTIONARY
	article_info = {
	'title':title,
	'img':img,
	'date':date,
	'subtitle':subtitle,
	'publisher':publisher,
	'link':link,
	'tags':tags 
	}
	# PUT article_info IN article_all
	articles_all.append(article_info)
print(articles_all)