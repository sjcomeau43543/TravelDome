'''
Author:        Samantha
Last modified: 5.5.2020 by sjc
Status:        Done

this will cluster the activities so that we can recommend new activities based on positive feedback

example run:
    python3 clustering.py -l ../scrapers/locations.txt -e ../scrapers/adjectives_extended.txt


'''

import os
import argparse
import json
from math import sqrt

import sys
sys.path.insert(1, "../scrapers")
from activity import Activity


class Clustering:

    def __init__(self, locations=[], adjectives=[], number_neigbors=5):
        self.adjectives = adjectives
        self.locations = locations
        self.activities = {}
        self.vectors = {}

        # populate activities
        for location in locations:
            self.activities[location] = []
            self.vectors[location] = []

        # populate data
        self.get_data()

        # vectorize data
        self.vectorize()

        # store the nearest neighbors
        self.store_KNN(number_neigbors)


    def get_data(self):
        # get all merged data
        for root,dir,files in os.walk("../data/Merged"):
            for file in files:
                with open(os.path.abspath(root+"/"+file)) as activity_file:
                    self.activities[file.strip(",").strip(".json")] = json.load(activity_file)


    def vectorize(self):
        for location in self.locations:
            for activity in self.activities[location]:
                # if multiple sources tagged an activity with a certain tag that increases the significance of the tag
                self.vectors[location].append((activity["name"], [activity["tags"].count(adj) if adj in activity["tags"] else 0 for adj in self.adjectives]))


    def cluster(self):
        # self.model = KMeans(n_clusters=len(self.adjectives), max_iter=500, n_init=1)

        # import pdb; pdb.set_trace()
        pass

    def euc(self, row1, row2):
        dist = 0.0
        for i in range(len(row1)-1):
            dist += (row1[i] - row2[i]) ** 2
        return sqrt(dist)

    def KNN(self, location, vector, num_nay=5):
        # calculate distances
        dists = []
        for vect in self.vectors[location]:
            dist = self.euc(vector, vect[1])
            dists.append((vect[0], dist))
        dists.sort(key=lambda x:x[1])

        # get neighbors
        neighbors = []
        for i in range(1, 1+num_nay):
            neighbors.append(dists[i])

        return neighbors

    def store_KNN(self, num_nay=5):
        for location in self.locations:
            self.all_neighbors = {}

            # for every activity
            for (name, vector) in self.vectors[location]:
                self.all_neighbors[name] = self.KNN(location, vector, num_nay)

            # export
            with open("../data/Cluster/neighbors"+location+".json", "w") as cluster_file:
                json.dump(self.all_neighbors, cluster_file, indent=1)

        


def main():
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations", help="locations.txt file", required=True)
    parser.add_argument("-e", "--adjectivesext", help="adjectives_extended.txt file", required=True)
    parser.add_argument("-n", "--number_neighbors", help="the number of neighbors for each activity to generate", type=int)
    args = parser.parse_args()


    # locations
    with open(args.locations, "r") as locations_file:
        locations = locations_file.readlines()
        locations = [(loc.strip('\n').split(',')[0]+loc.strip('\n').split(',')[1]) for loc in locations]

    # get adjectives
    with open(args.adjectivesext, 'r') as f:
        adjectives_ext = [adj.strip(',') for adj in f.read().split()]

    # cluster
    if args.number_neighbors:
        cluster = Clustering(locations, adjectives_ext, args.number_neighbors)
    else:
        cluster = Clustering(locations, adjectives_ext)
    
main()
