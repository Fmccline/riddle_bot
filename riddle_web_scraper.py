# reddit riddle bot
# Frank Cline

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import smtplib


class Riddle:
	def __init__(self,question,answer):
		self.question = question
		self.answer = answer

def make_soup(url):
	"""makes a soup object with a given url
	
	param: string -- url for soup object
	returns: html soup object or None
	"""
	html = get_html(url)
	soup = BeautifulSoup(html,"html.parser") 
	return soup

def get_html(url):
	"""

	returns: html object or None
	"""
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
		request = Request(url=url, headers=headers)
		html = urlopen(request)
		return html
	except Exception as e:
		print(e) 

def make_riddle_from_soup(soup):
	"""makes a Riddle object from a given soup object
	
	param: BeautifulSoup object
	returns: list --question as first index and answer as the second
	"""
	question = ""
	answer = ""
	for tag in soup.find_all('p'):
		if str(tag.contents[0].string) == "Question: ":
			question += str(tag.contents[1].string)
		if str(tag.contents[0].string) == "Answer: ":
			answer += str(tag.contents[1].string)
	if question == "" or answer == "":
		print("Question or Answer not found.")
		raise RuntimeError
	else:
		return Riddle(question,answer)

def get_riddle():
	"""

	returns: Riddle object with the question and answer from a 
			 riddle from goodriddlesnow.com
	"""
	url = "https://goodriddlesnow.com/riddles/random"

	soup = make_soup(url)
	riddle = make_riddle_from_soup(soup)
	return riddle


if __name__ == '__main__':
	riddle = get_riddle()
	print(f'{riddle.question}\n\n{riddle.answer}')
