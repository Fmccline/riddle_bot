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

    def __init__(self):
        super().__init__(self.URL)
        self.XPATH = "/html/body/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td/p[2]/b/font"

    def scrape(self):
        delay = 3
        insult = ""
        driver = SeleniumDriver.make_driver()
        try:
            driver.get(self.url)
            factElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH)))
            insult = factElem.get_attribute('innerHTML')
        except Exception as e:
            print(e)
            insult = "Sorry, there was an error while trying to get an insult."
        driver.close()
        return Insult(insult)
