import selenium as se
from selenium import webdriver

class SeleniumDriver:

    @staticmethod
    def make_driver():
        options = se.webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        options.experimental_options["prefs"] = chrome_prefs
        
        driver = se.webdriver.Chrome(
            executable_path="chromedriver", chrome_options=options)
        return driver
