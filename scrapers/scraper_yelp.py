'''
Author:        Samantha
Last modified: 4.24.2020 by sjc
Status:        In Progress

Since writing this we have discovered that Yelp does not permit scraping of it's site. 
https://www.yelp-support.com/article/Can-I-copy-or-scrape-data-from-the-Yelp-site?l=en_US

TODO get photos from site
'''
import os
import requests
import json
from lxml import html

from activity import Activity

class Yelp:

    api_key = ""
    
    def __init__(self, api_key):
        self.api_key = api_key


    def build_url(self, city, state, start=0):
        url = "https://yelp.com/search?find_desc=things%20to%20do&find_loc="+city+"%2C%20"+state+"&start="+str(start)
        
        return url

    
    def scrape(self, city, state, num_results=100):
        for page_block in range(int(num_results/50)):

            # build the URL
            url = "https://api.yelp.com/v3/businesses/search"
            parameters = {"term":"things to do", "location":city+","+state, "limit":"50","offset":str(page_block*50)}
            headers    = {"Authorization":"Bearer %s" % self.api_key}
            
            # activities
            activities = []

            # results
            response = requests.get(url, params=parameters, headers=headers)

            if response.status_code == 200:
                # success
                response_json = json.loads(response.text)

                for business in response_json["businesses"]:
                    # get reviews
                    reviews = []
                    business_url = "https://api.yelp.com/v3/businesses/"+business["id"]+"/reviews"
                    request_reviews = requests.get(business_url, params=parameters, headers=headers)

                    if request_reviews.status_code == 200:
                        reviews_json = json.loads(request_reviews.text)

                        for review in reviews_json["reviews"]:
                            reviews.append(review["text"])


                    # download the image
                    photo_location = "../data/Photographs/yelp_image_"+str(business["id"])+".jpg"
                    if os.path.exists(photo_location):
                        pass
                    elif "image_url" in business.keys():
                        try:
                            photo_url = business["image_url"]
                            request_photo = requests.get(photo_url)

                            if request_photo.status_code == 200:
                                with open(photo_location, "wb") as handler:
                                    for block in request_photo.iter_content(1024):
                                        if not block:
                                            break
                                        handler.write(block)
                        except:
                            photo_location = None
                    else:
                        photo_location = None

                    # add to list
                    a = Activity(business["name"], business["location"]["address1"], business["rating"], None, photo_location, "Yelp", reviews=reviews, tags=[])
                    activities.append(a)

        return activities

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