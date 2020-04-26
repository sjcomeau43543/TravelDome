'''
Author:        Samantha
Last modified: 4.24.2020 by sjc
Status:        In Progress

Since writing this we have discovered that Yelp does not permit scraping of it's site. 
https://www.yelp-support.com/article/Can-I-copy-or-scrape-data-from-the-Yelp-site?l=en_US

TODO Attempt REST API implementation
'''

import requests
import json
from lxml import html

from activity import Activity

class Yelp:

    self.api_key = ""
    
    def __init__(self, api_key):
        self.api_key = api_key


    def build_url(self, city, state, start=0):
        url = "https://yelp.com/search?find_desc=things%20to%20do&find_loc="+city+"%2C%20"+state+"&start="+str(start)
        
        return url

    def build_api_url(self, city, state, start=0):

        pass
    
    def scrape(self, city, state, num_results=100):
        pass

    def scrape_old(self, city, state, num_results=100):
        activities = []

        for block in range(int(num_results/10)):
            url = self.build_url(city, state, start=block*10)

            response = requests.get(url)

            if response.status_code == 200:
                # success
                parser = html.fromstring(response.text)
                listing = parser.xpath("//li[@class='regular-search-result']")
                dirty_json = parser.xpath("//script[contains(@data-hypernova-key,'yelp_main__SearchApp')]//text()")
                
                # clean and load json
                cleaned_json = dirty_json[0].replace("<!--", "").replace("-->", "").strip()
                loaded_json = json.loads(cleaned_json)

                # get search results
                search_results = loaded_json["searchPageProps"]["searchResultsProps"]["searchResults"]

                # loop through search results
                for results in search_results:
                    result = results.get('searchResultBusiness')

                    # ignore ads and other fillers
                    if result:
                        a = Activity(result['name'], result['formattedAddress'], result['rating'], None, None, "Yelp")
                        activities.append(a)

        return activities