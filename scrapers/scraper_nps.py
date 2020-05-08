'''
Author:        Samantha
Last modified: 5.7.2020 by sjc
Status:        wip
'''
import os
import requests
import json
from lxml import html
from bs4 import BeautifulSoup

from activity import Activity

class NPS:
    
    def __init__(self):
        pass


    def build_url(self, city, state, start=0):
        url = "https://www.nps.gov/state/"+state+"/index.htm"
        
        return url

    
    def scrape(self, city, state):        
        # activities
        activities = []

        # results
        url = self.build_url(city, state)
        response = requests.get(url)

        if response.status_code == 200:
            # success
            soup = BeautifulSoup(response.text, features="lxml")

            parklist = soup.find("ul", {"id": "list_parks"})

            listindexes = parklist.find_all('li')
            for li in listindexes:
                classes = li.get("class")
                if(classes):
                    if("clearfix" in classes):
                        # title
                        name = li.find("h3").string

                        # "reviews"
                        if([li.find("p").string]):
                            reviews = [li.find("p").string]
                        else:
                            reviews = []

                        # image
                        img = li.find("img")
                        if img:
                            image = "https://www.nps.gov/"+img["src"]
                        else:
                            image = None
                        # link
                        link = li.find(lambda tag:tag.name=="a" and "Information" in tag.text)

                        # add to list
                        a = Activity(name, "", "", None, image, "NPS", link=link, reviews=reviews, tags=["adventurous", "parks"], get_tags=True)
                        activities.append(a)

        return activities
