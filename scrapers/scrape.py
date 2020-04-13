import argparse

# scrapers
from scraper_yelp import Yelp
yelpscraper = Yelp()

def main():
    parser = argparse.ArgumentParser(description="Parse Yelp for businesses in the provided locations")
    parser.add_argument('--locations', '-l', nargs='+', required=True)

    args = parser.parse_args()

    for location in args.locations:
        [city, state] = location.split(',')

        print("Scraping Yelp for ", city, state)
        yelpscraper.scrape(city, state)

main()