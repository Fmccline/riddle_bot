import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .web_scraper import WebScraper
from .selenium_driver import SeleniumDriver


class Insult:

    def __init__(self, insult):
        self.insult = insult

    def __str__(self):
        return self.insult


class SaucyInsultScraper(WebScraper):

    URL = "http://literarygenius.info/a2-shakespeare-insult-generator.htm"
    XPATH = "/html/body/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td/p[2]/b/font"

    def __init__(self):
        super().__init__(self.URL)
        self.driver = SeleniumDriver.make_driver()

    def scrape(self):
        delay = 3
        insult = ""
        try:
            self.driver.get(self.url)
            factElem = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH)))
            insult = factElem.get_attribute('innerHTML')
        except Exception as e:
            print(e)
            insult = "Sorry, there was an error while trying to get an insult."
        return Insult(insult)
