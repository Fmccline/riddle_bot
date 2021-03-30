import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .web_scraper import WebScraper
from .selenium_driver import SeleniumDriver


class Fact:
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class FactScraper(WebScraper):

    URL = "https://mentalfloss.com/amazingfactgenerator"
    DIV_ID = 'af-description'

    def __init__(self):
        super().__init__(self.URL)
        self.driver = SeleniumDriver.make_driver()

    def scrape(self):
        delay = 3  # seconds
        description = "0"*500
        tries = 0
        while len(description) >= 450 and tries < 3:
            try:
                self.driver.get(self.url)
                factElem = WebDriverWait(self.driver, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, self.DIV_ID)))
                description = f"Fun fact: {factElem.text}"
            except Exception:
                description = "Sorry, I ran into an unexpected error while getting you a fact!"
            finally:
                tries += 1
        return Fact(description)


if __name__ == '__main__':
    scraper = FactScraper()
    fact = scraper.scrape()
    print(fact.description)
