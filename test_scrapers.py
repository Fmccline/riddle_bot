from web_scrapers import FactScraper, RiddleScraper


if __name__ == '__main__':
    scrapers = [FactScraper(), RiddleScraper()]
    for scraper in scrapers:
        print(scraper.scrape())