from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from .web_scraper import WebScraper


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
        for tag in soup.find_all('p'):
            if str(tag.contents[0].string) == "Question: ":
                question += str(tag.contents[1].string)
            if str(tag.contents[0].string) == "Answer: ":
                answer += str(tag.contents[1].string)
        if question == "" or answer == "":
            print("Question or Answer not found.")
            raise RuntimeError
        else:
            return Riddle(question, answer)


if __name__ == '__main__':
    riddle_scraper = RiddleScraper()
    riddle = riddle_scraper.scrape()
    print(riddle.question)
    print(riddle.answer)
