import selenium as se
from selenium import webdriver

class SeleniumDriver:

    @staticmethod
    def make_driver():
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = se.webdriver.Chrome(
            executable_path="C:/Users/Frank's Laptop/Desktop/Programming/Python/riddle_bot/web_scrapers/chromedriver", chrome_options=options)
        return driver
