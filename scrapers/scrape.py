import json

# scrapers
from scraper_yelp import Yelp
yelpscraper = Yelp()

# activity
from activity import Activity

def main():
    # open locations.txt
    with open("locations.txt", "r") as locations_file:
        locations = locations_file.readlines()


    for location in locations:
        [city, state] = location.split(',')


        # Yelp
        print("Scraping Yelp for", city, state)
        activities = yelpscraper.scrape(city, state)
        with open("../data/Yelp/results_"+city+state+".json", "w") as outfile:
            outfile.write("[\n")
            for activity in activities:
                json.dump(activity.encode(), outfile, indent=1)
            outfile.write("]\n")


main()