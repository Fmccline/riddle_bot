from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from .web_scraper import WebScraper
import re


class Riddle:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __str__(self):
        return self.question + "\n" + self.answer


class RiddleScraper(WebScraper):

    URL = "https://goodriddlesnow.com/riddles/random"

    def __init__(self):
        super().__init__(self.URL)

    def make_soup(self):
        """makes a soup object with a given url

        param: string -- url for soup object
        returns: html soup object or None
        """
        html = self.get_html()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_html(self):
        """

        returns: html object or None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            request = Request(url=self.url, headers=headers)
            html = urlopen(request)
            return html
        except Exception as e:
            print(e)

    def scrape(self):
        soup = self.make_soup()
        return self.scrape_content(soup)

    def scrape_content(self, soup):
        """makes a Riddle object from a given soup object

        param: BeautifulSoup object
        returns: list --question as first index and answer as the second
        """
        question = ""
        answer = ""
        riddle = None
        try:
            question = soup.find('div', {"class": "riddle-question"}).find('p').text
            answer = soup.find('div', {"class": "riddle-answer hide print-show"}).find('p').text

            question = self.format_text(question)
            answer = self.format_text(answer)
        except Exception as e:
            print(e)
            question = "Who couldn't find a riddle?"
            answer = "Me :{"

        riddle = Riddle(question, answer)
        if self.needs_censoring(riddle):
            return self.scrape()
        else:
            return riddle

    def format_text(self, text):
        text = re.sub(r"\.", ". ", text)
        text = re.sub(r"\s\.\s", ".", text)        
        text = re.sub(r"\s\s+", " ", text)
        return text

    def needs_censoring(self, riddle):
        texts = [riddle.question, riddle.answer]
        for text in texts:
            if re.search(r"black (man|woman)", text.lower()) is not None or text.lower() == 'a woman':
                print('*********************************')
                print('CENSORING RIDDLE')
                print(riddle.question)
                print(riddle.answer)
                print('*********************************')                
                return True
        return False
