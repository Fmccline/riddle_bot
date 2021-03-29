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
    scrapers = []
    scrapers.append(FactScraper())
    scrapers.append(RiddleScraper())
    scrapers.append(SaucyInsultScraper())
    results = []
    for scraper in scrapers:
        results.append(str(scraper.scrape()))
    
    for result in results:
        print(f'\n{result}')


if __name__ == '__main__':
    test_all()
    # test_riddle_scraper()