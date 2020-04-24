'''
Author:        Samantha
Last modified: 4.24.2020 by sjc
Status:        In progress

This merges the results from the platforms in the data directory
'''

import os
import json

import argparse

def main():
    # argument parser
    parser = argparse.ArgumentParser()

    # parser.add_argument("-l", "--locations", required=True, help="Locations.txt")

    args = parser.parse_args()

    # get expected locations

    # Walk directory
    for root,dir,files in os.walk("../data"):
        if root != "../data":
            source = root.strip("../data/")
            print(source)
            if source == "TripAdvisor":
                for file in files:
                    path = os.path.abspath(root+"/"+file)
                    with open(path) as activity_file:
                        #print(activity_file.readlines()[:10])
                        information = json.load(activity_file)
                        #with open(path, "r") as f:
                        #    print(f.readlines()[0:5])
                        import pdb; pdb.set_trace()




main()