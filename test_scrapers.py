from web_scrapers import FactScraper, RiddleScraper, SaucyInsultScraper


def test_riddle_scraper():
    for x in range(10):
        print("\nRiddle " + str(x))
        riddle_scraper_test()

def riddle_scraper_test():
    riddle_scraper = RiddleScraper()
    riddle = riddle_scraper.scrape()
    print(riddle.question)
    print()
    print(riddle.answer)


def test_all():
    scrapers = [FactScraper(), RiddleScraper(), SaucyInsultScraper()]
    scrapers = []
    scrapers.append(FactScraper())
    scrapers.append(RiddleScraper())
    scrapers.append(SaucyInsultScraper())
    for scraper in scrapers:
        print(scraper.scrape())


if __name__ == '__main__':
    test_all()
    # test_riddle_scraper()