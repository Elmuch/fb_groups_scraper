# Get extra data
# We have to get past login here 

from bs4 import BeautifulSoup, Comment
import pdb
import re
import requests 

def scrape(params):
	with requests.Session() as cop:
		url = 'https://www.facebook.com/login'
		USERNAME = "jlamlam@hotmail.com"
		PASSWORD = "****"
		origin ="https://www.facebook.com"
		# user-agent = "chrome"
		referer = "https://www.facebook.com/?stype=lo&jlou=Afc8d9OEvtNbOsnGypIuvBH7wNq4znakqh9tEKUJNaqnCgq3U3Z0q5LK5a9VsevvnVWo0xE_869hPZYNJ0RNsQ9J&smuh=3328&lh=Ac98Vksh0GRBmMCM&aik=OClr2sy4Oa8ERH6zxFHxdQ"
		cookie = cookie.jar[0]
		token = ""
		cop.get(url)
		login_data = {"lsd":"AVpDLrCm","email":USERNAME,"pass":PASSWORD,"lgnrnd":"054302_Kunm","qsstamp":token}
		cop.post(url, data=login_data,headers ={'Referer':referer, "origin": origin, 'cookie':cookie})
		page = cop.get(params['url'])
		data = page.content
		soup = BeautifulSoup(data)
	# .get("hre")
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		links = []
		for comment in comments:
			comment.extract()
			soup2 = BeautifulSoup(comment)
			links.append(soup2.findAll('a'))
		
		for link in links:
			for child in link:
				href = child.get("href")
				try:
					if (href.split("/")[1] == "groups"):
						print child.text
				except Exception, e:
					pass