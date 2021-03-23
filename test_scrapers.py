from web_scrapers import FactScraper, RiddleScraper, SaucyInsultScraper


if __name__ == '__main__':
    # scrapers = [FactScraper(), RiddleScraper(), SaucyInsultScraper()]
    scrapers = []
    # scrapers.append(FactScraper())
    # scrapers.append(RiddleScraper())
    scrapers.append(SaucyInsultScraper())
    for scraper in scrapers:
        print(scraper.scrape())