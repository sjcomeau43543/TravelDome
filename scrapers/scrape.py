'''
Author:        Samantha
Last modified: 4.29.2020 by sjc
Status:        In Progress

The purpose of this is to integrate all the scrapers

example run:
    python3 scraper.py -l locations.txt -y -c yelp_credentials.json -w
    python3 scraper.py -l locations.txt -t -w
    python3 scraper.py -l locations.txt -g -w

TODO: add google maps
'''

import json
import argparse
import os

# activity
from activity import Activity

def main():
    # arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-y", "--yelp", action="store_true", default=False, help="Scrape Yelp")
    parser.add_argument("-g", "--maps", action="store_true", default=False, help="Scrape GoogleMaps")
    parser.add_argument("-t", "--tripadvisor", action="store_true", default=False, help="Scrape TripAdvisor")
    parser.add_argument("-l", "--locations", help="locations.txt file", required=True)

    parser.add_argument("-c", "--yelpconfig", help="Yelp API config")
    parser.add_argument("-o", "--write", action="store_true", default=False, help="write the results to the files, don't use this if you are testing")

    args = parser.parse_args()

    # open locations.txt
    with open(args.locations, "r") as locations_file:
        locations = locations_file.readlines()

    # manage imports
    if args.yelp:
        # get credentials
        with open(args.yelpconfig, "r") as config:
            creds = json.load(config)
            api_key = creds["APIKey"]

        # import YelpScraper
        from scraper_yelp import Yelp
        yelpscraper = Yelp(api_key)

    if args.tripadvisor:
        import scraper_tripadvisor

    if args.maps:
        import scraper_googlemaps


    for location in locations:
        [city, state] = location.strip('\n').split(',')

        if args.yelp:
            # Yelp
            print("Scraping Yelp for", city, state)

            # Scrape
            activities = yelpscraper.scrape(city, state)
            import pdb; pdb.set_trace()

            if args.write:
                with open("../data/Yelp/"+city+state+".json", "w") as outfile:
                    outfile.write("[\n")
                    for activity in activities:
                        json.dump(activity.encode(), outfile, indent=1)
                        if activity != activities[-1]:
                            outfile.write(",")
                    outfile.write("]\n")

        if args.tripadvisor:
            # TripAdvisor
            print("Scraping TripAdvisor for", city, state)
            activities = scraper_tripadvisor.tripadvisor_scrape(city, state)

            if args.write:
                with open("../data/TripAdvisor/"+city+state+".json", "w") as outfile:
                    outfile.write("[\n")
                    for activity in activities:
                        json.dump(activity.encode(), outfile, indent=1)
                        if activity != activities[-1]:
                            outfile.write(",")
                    outfile.write("]\n")

        if args.maps:
            # Google maps
            print("Scraping GoogleMaps for", city, state)

if __name__ == '__main__':
    main()
