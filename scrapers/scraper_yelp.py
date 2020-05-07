'''
Author:        Samantha
Last modified: 4.29.2020 by sjc
Status:        Done
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


                    # image
                    if "image_url" in business.keys():
                        photo_location = business["image_url"]
                    else:
                        photo_location = None

                    # add to list
                    a = Activity(business["name"], business["location"]["address1"], business["rating"], None, photo_location, "Yelp", reviews=reviews, get_tags=True)
                    activities.append(a)

        return activities
