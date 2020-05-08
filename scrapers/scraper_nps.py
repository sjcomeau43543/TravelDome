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
                        for child in li.find("h3").children:
                            nameurl = "https://www.nps.gov/"+child["href"] + "/index.htm"

                        # "reviews"
                        if([li.find("p").string]):
                            reviews = [li.find("p").string]
                        else:
                            reviews = []

                        # link
                        link = li.find(lambda tag:tag.name=="a" and "Information" in tag.text)
                        if(link):
                            link = link["href"]
                        else:
                            link = None

                        if(link):
                            # get basic information page
                            basicinfo_resp = requests.get(link)
                            basicinfo_soup = BeautifulSoup(basicinfo_resp.text, features="lxml")
                            address = basicinfo_soup.find("span", {"class":"street-address"})
                            if(address):
                                address = address.text
                            else:
                                address = None
                        else:
                            address = None

                        # get better photo and reviews
                        moreinfo = requests.get(nameurl)
                        soupinfo = BeautifulSoup(moreinfo.text, features="lxml")
                        img = soupinfo.find("img", {"class":"Feature-image"})
                        if img:
                            image = "https://www.nps.gov/"+img["src"]
                        else:
                            image = None

                        # add to list
                        a = Activity(name, address, "", None, image, "NPS", link=nameurl, reviews=reviews, tags=["adventurous", "parks"], get_tags=True)
                        activities.append(a)

        return activities
