# reddit riddle bot
# Frank Cline

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class WebScraper:

    def __init__(self, url):
        self.url = url

    def scrape(self):
        raise NotImplementedError
