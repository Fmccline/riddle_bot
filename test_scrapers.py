from web_scrapers import FactScraper, RiddleScraper, SaucyInsultScraper
from datetime import datetime


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


def time_it(scraper, iterations):
    start = datetime.now()
    results = []
    for _ in range(iterations):
        results.append(str(scraper.scrape()))
    elapsed = datetime.now() - start
    print(results)
    return elapsed/iterations


def time_scrapers():
    tests = []
    tests.append((FactScraper(), 3))
    # tests.append((SaucyInsultScraper(), 2))
    # tests.append((RiddleScraper(), 2))
    
    results = []
    for test in tests:
        scraper = test[0]
        iterations = test[1]
        name = type(scraper).__name__
        results.append((name, time_it(scraper, iterations)))
    for result in results:
        print(f'{result[0]}: {result[1]}')


if __name__ == '__main__':
    # test_all()
    test_riddle_scraper()
    # time_scrapers()
