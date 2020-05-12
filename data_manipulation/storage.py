'''
Author:        Samantha
Last modified: 5.5.2020 by sjc
Status:        Done

Creates the inverted index from the merged data folder and stores it in a json file

example
python3 storage.py -l ../scrapers/locations.txt -a ../scrapers/adjectives_extended.txt
'''

import os
import json
import argparse

import sys
sys.path.insert(1, "../scrapers")
from activity import Activity


'''
adj   |    [act1    |    act2    |   etc]
'''

class Storage:

    def __init__(self):
        self.inverted_index = {}

    def add(self, city, state):
        # Walk directory
        for root,dir,files in os.walk("../data/Merged"):
            # get the files for each location
            for file in files:
                location = file.strip(".json")
                if location == str(city+state):
                    # add the activities to the inverted index
                    with open(os.path.abspath(root+"/"+file)) as activity_file:
                            activities = json.load(activity_file)
                            for activity in activities:
                                actobj = Activity(activity["name"], activity["address"], activity["avg_visitor_review"], activity["avg_time_spent"], activity["photo_location"], activity["source"], reviews=[], tags=activity["tags"])

                                # get tags
                                actobj.tags = list(actobj.tags)
                                if '[' in actobj.tags: actobj.tags.remove('[')
                                if ']' in actobj.tags: actobj.tags.remove(']')

                                for tag in (list(set(actobj.tags))):
                                    self.inverted_index[tag].append(actobj.name)

    def add_all(self, list_of_locations, adjectives):
        self.inverted_index = {}

        for adj in adjectives:
            self.inverted_index[adj] = []

        for location in list_of_locations:
            self.add(location[0], location[1])
            # export
            self.export(location[0]+location[1])


  
    def export(self, location):
        with open("../data/InvertedIndex/invertedindex_"+location+".json", "w") as outfile:
            json.dump(self.inverted_index, outfile, indent=1)



def main():
    storage = Storage()

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations", help="locations.txt file", required=True)
    parser.add_argument("-a", "--adjectives_ext", help="adjectives.txt file", required=True)
    args = parser.parse_args()

    with open(args.locations, "r") as locations_file:
        locations = locations_file.readlines()
        locations = [(loc.strip('\n').split(',')[0],loc.strip('\n').split(',')[1]) for loc in locations]

    with open(args.adjectives_ext, "r") as adjectives_file:
        adjectives = [adj.strip(',') for adj in adjectives_file.read().split()] # [adj.strip('\n') for adj in adjectives]

    # do the thing
    storage.add_all(locations, adjectives)



main()