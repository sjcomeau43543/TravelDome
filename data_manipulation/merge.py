'''
Author:        Samantha
Last modified: 4.24.2020 by sjc
Status:        Done

This merges the results from the platforms in the data directory

example
    python3 merge.py -l ../scrapers/locations.txt 
'''

import os
import json
import argparse


import sys
sys.path.insert(1, "../scrapers")
from activity import Activity

class Merger:

    def __init__(self):
        pass

    def merge_location(self, city, state):
        # all data repository
        merged_activities = {}

        # Walk directory
        for root,dir,files in os.walk("../data"):
            if root != "../data" and root != "../data/Merged" and root != "../data/Photographs" and root != "../data/InvertedIndex" and root != "../data/Cluster":
                # get the files for each location
                for file in files:
                    location = file.strip(".json")
                    if location == str(city+state):
                        with open(os.path.abspath(root+"/"+file)) as activity_file:
                            activities = json.load(activity_file)
                            for activity in activities:
                                actobj = Activity(activity["name"], activity["address"], activity["avg_visitor_review"], activity["avg_time_spent"], activity["photo_location"], activity["source"], link=activity["link"], reviews=[], tags=activity["tags"])

                                # fix lists
                                actobj.tags = list(actobj.tags)
                                if '[' in actobj.tags: actobj.tags.remove('[')
                                if ']' in actobj.tags: actobj.tags.remove(']')

                                if actobj.name not in merged_activities.keys():
                                    # make lists of what would have become lists for consistency
                                    actobj.source = [actobj.source]
                                    actobj.link = [actobj.link]
                                    actobj.photo_location = [actobj.photo_location]
                                    actobj.avg_visitor_review = [actobj.avg_visitor_review]

                                    merged_activities[actobj.name] = actobj
                                else:
                                    ## handle duplicates
                                    # use more detailed address
                                    actobj.address = merged_activities[actobj.name].address if len(merged_activities[actobj.name].address) > len(actobj.address) else actobj.address

                                    # average the visitor reviews                               
                                    actobj.avg_visitor_review = [actobj.avg_visitor_review]
                                    for rev in merged_activities[actobj.name].avg_visitor_review:
                                        actobj.avg_visitor_review.append(rev)

                                    # TODO time spent
                                    ### default to the second source
                                    
                                    # list of photos
                                    actobj.photo_location = [actobj.photo_location]
                                    for loc in merged_activities[actobj.name].photo_location:
                                        actobj.photo_location.append(loc)

                                    # combine tags lists
                                    for tag2 in merged_activities[actobj.name].tags:
                                        if tag2 not in actobj.tags:
                                            actobj.tags.append(tag2)

                                    # list of sources
                                    actobj.source = [merged_activities[actobj.name].source, actobj.source]

                                    # list of links
                                    actobj.link = [merged_activities[actobj.name].link, actobj.link]

                                    # replace the old entry
                                    merged_activities[actobj.name] = actobj
                                    actobj = 0

        # return to standard formattign which is a list of activites
        standard = []
        for activity in merged_activities.keys():
            # add
            standard.append(merged_activities[activity])

        return standard

    def merge_all(self, list_of_locations):
        all_activities = {}
        for location in list_of_locations:
            all_activities[str(location[0]+location[1])] = self.merge_location(location[0], location[1])
        return all_activities

    def export(self, locations, activities):
        with open("../data/Merged/merged.json", "w") as outfile:
            outfile.write("{\n")
            for location in locations:
                loc = str(location[0]+location[1])
                
                outfile.write('"'+loc+'":[\n')
                for activity in activities[loc]:
                    json.dump(activity.encode(), outfile, indent=1)
                    if activity != activities[loc][-1]:
                        outfile.write(",")
                outfile.write("],\n")
            outfile.write("}\n")

def main():
    merger = Merger()

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations", help="locations.txt file", required=True)
    args = parser.parse_args()

    with open(args.locations, "r") as locations_file:
        locations = locations_file.readlines()
        locations = [(loc.strip('\n').split(',')[0],loc.strip('\n').split(',')[1]) for loc in locations]

    # merge all current
    act = merger.merge_all(locations)
    merger.export(locations, act)

    
main()