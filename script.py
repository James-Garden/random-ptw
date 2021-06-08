from html.parser import HTMLParser
from random import randint
import requests
import re

class ListParser(HTMLParser):
	titles = []

	def handle_starttag(self,tag,attrs):
		if (len(attrs)>=2 and attrs[0][1]=="list-table"):
			params = attrs[1][1].split(",")
			for x in params:
				if ("anime_title" in x):
					x = x.split(":")
					title = ""
					for i in range(1,len(x)):
						title += x[i]
						title = title.strip("\"")
					self.titles.append(title)

class RandomPick:
	pageUrl = ""
	pageData = ""
	list = ""

	def __init__(self,url):
		response = requests.get(url)
		self.pageUrl = url
		self.pageData = response.text
		listParser = ListParser()
		listParser.feed(self.pageData)
		self.list = listParser.titles

	def refresh(self):
		response = requests.get(self.pageUrl)
		self.pageData = response.text
		listParser = ListParser()
		listParser.feed(self.pageData)
		self.list = listParser.titles

	def choose(self):
		myString = self.list[randint(1,len(self.list)-1)]
		return myString

username = str(input("Username: "))
listUrl = "https://myanimelist.net/animelist/" + username + "?status=6"
myList = RandomPick(listUrl)
while(True):
		choice = re.sub(r'(\\u[0-9A-Fa-f]+)', lambda matchobj: chr(int(matchobj.group(0)[2:], 16)), myList.choose())
		print (choice,end='',flush=True)
		userInput = str(input())
		if (userInput!=""):
			if (userInput=="refresh"):
				myList.refresh()
			else:
				break
