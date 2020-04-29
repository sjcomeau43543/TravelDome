'''
Author:        Samantha
Last modified: 4.29.2020 by sjc
Status:        In Progress

this will cluster the activities so that we can recommend new activities based on positive feedback

example run:
    python3 clustering.py -


'''

import os
import argparse
import json
from math import sqrt

import sys
sys.path.insert(1, "../scrapers")
from activity import Activity

from sklearn.cluster import KMeans

class Clustering:

    def __init__(self, adjectives=[], number_neigbors=5):
        self.adjectives = adjectives
        self.activities = []
        self.vectors = []

        # populate data
        self.get_data()

        # vectorize data
        self.vectorize()

        # create model
        # self.cluster()

        # querying KNN
        # self.KNN(self.vectors[0][1])

        # store the nearest neighbors
        self.store_KNN(number_neigbors)


    def get_data(self):
        # get all merged data
        for root,dir,files in os.walk("../data/Merged"):
            for file in files:
                with open(os.path.abspath(root+"/"+file)) as activity_file:
                    activities = json.load(activity_file)
                    self.activities.extend(activities)


    def vectorize(self):
        for activity in self.activities:
            
            self.vectors.append((activity["name"], [1 if adj in activity["tags"] else 0 for adj in self.adjectives]))


    def cluster(self):
        self.model = KMeans(n_clusters=len(self.adjectives), max_iter=500, n_init=1)

        import pdb; pdb.set_trace()

    def euc(self, row1, row2):
        dist = 0.0
        for i in range(len(row1)-1):
            dist += (row1[i] - row2[i]) ** 2
        return sqrt(dist)

    def KNN(self, vector, num_nay=5):
        # calculate distances
        dists = []
        for vect in self.vectors:
            dist = self.euc(vector, vect[1])
            dists.append((vect[0], dist))
        dists.sort(key=lambda x:x[1])

        # get neighbors
        neighbors = []
        for i in range(1, 1+num_nay):
            neighbors.append(dists[i])

        return neighbors

    def store_KNN(self, num_nay=5):
        self.all_neighbors = {}

        # for every activity
        for (name, vector) in self.vectors:
            self.all_neighbors[name] = self.KNN(vector, num_nay)

        # export
        with open("../data/Cluster/neighbors.json", "w") as cluster_file:
            json.dump(self.all_neighbors, cluster_file, indent=1)

        


def main():
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--adjectivesext", help="adjectives_extended.txt file", required=True)
    parser.add_argument("-n", "--number_neighbors", help="the number of neighbors for each activity to generate", type=int)
    args = parser.parse_args()


    # get adjectives
    with open(args.adjectivesext, 'r') as f:
        adjectives_ext = [adj.strip(',') for adj in f.read().split()]

    # cluster
    if args.number_neighbors:
        cluster = Clustering(adjectives_ext, args.number_neighbors)
    else:
        cluster = Clustering(adjectives_ext)
    
main()
