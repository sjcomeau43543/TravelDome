'''
Author:        Samantha
Last modified: 4.24.2020 by sjc
Status:        In progress

This merges the results from the platforms in the data directory and writes the results to an inverte index 

TODO modularize the merge function
TODO update with time_spent when those are integrated
'''

import os
import json

import argparse


'''
merge the results of the files
'''
def merge_results():
# all data repository
    all_data = {}

    # Walk directory
    for root,dir,files in os.walk("../data"):
        if root != "../data":
            # get the files for each location
            for file in files:
                location = file.strip(".json")
                if location not in all_data.keys():
                    all_data[location] = {}
                with open(os.path.abspath(root+"/"+file)) as activity_file:
                    activities = json.load(activity_file)
                    for activity in activities:
                        if activity["name"] not in all_data[location]:
                            all_data[location][activity.pop("name",None)] = activity
                        else:
                            ## handle duplicates
                            name = activity.pop("name", None)
                            duplicate_activity = activity

                            # use more detailed address
                            duplicate_activity["address"] = all_data[location][name]["address"] if len(all_data[location][name]["address"]) > len(activity["address"]) else activity["address"]
                            # average the visitor reviews
                            duplicate_activity["avg_visitor_review"] = (float(activity["avg_visitor_review"]) + float(all_data[location][name]["avg_visitor_review"])) / 2
                            # TODO time spent
                            ### default to the second source
                            # list of photos
                            duplicate_activity["photo_location"] = [all_data[location][name]["photo_location"], activity["photo_location"]]
                            # combine tags lists
                            duplicate_activity["tags"] = []
                            for tag in activity["tags"]:
                                duplicate_activity["tags"].append(tag)
                            for tag2 in all_data[location][name]["tags"]:
                                if tag2 not in duplicate_activity["tags"]:
                                    duplicate_activity["tags"].append(tag2)
                            # list of sources
                            duplicate_activity["source"] = [all_data[location][name]["source"], activity["source"]]

                            # replace the old entry
                            all_data[location][name] = duplicate_activity

    return all_data

def main():
    # argument parser
    parser = argparse.ArgumentParser()

    # parser.add_argument("-l", "--locations", required=True, help="Locations.txt")

    args = parser.parse_args()

    results = merge_results()

    
main()