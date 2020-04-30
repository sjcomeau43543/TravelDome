'''
Author:        Samantha
Last modified: 4.29.2020 by sjc
Status:        In Progress

this will make visualizations 

example run:
    python3 vis.py 

'''

import os
import json
import argparse
import random

# charting
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use("tkagg")

class Vis:
    def __init__(self):
        pass
    
    def adj_loc(self, adjectives):
        # {loc1:{adj1:count,adj2:count}}
        adjective_count = {}

        # Walk directory
        for root,dir,files in os.walk("../data"):
            if root != "../data" and root != "../data/Merged" and root != "../data/Photographs" and root != "../data/InvertedIndex" and root != "../data/Cluster":
                # get the files for each location
                for file in files:
                    location = file.strip(".json")
                    
                    adjective_count[location] = {}

                    for adj in adjectives:
                        adjective_count[location][adj] = 0

                    with open(os.path.abspath(root+"/"+file)) as activity_file:
                        activities = json.load(activity_file)
                        for activity in activities:
                            # fix lists
                            tags = list(activity["tags"])
                            if '[' in tags: tags.remove('[')
                            if ']' in tags: tags.remove(']')

                            # add to tot
                            for tag in tags:
                                adjective_count[location][tag] += 1

        plt.title("Adjective tag frequency for each location")
        positions = [i for i in range(len(adjectives))]
        columns = adjectives

        width = 0.25

        locations = adjective_count.keys()

        bars = []

        previous = [0 for i in range(len(locations)) ]
        for location in locations:
            yaxis = []
            for i in adjective_count[location].values():
                yaxis.append(i)
            import pdb; pdb.set_trace()
            bars.append(plt.bar(positions, yaxis, width))
            #  previous = adjective_count[location].values()

        
        plt.xticks(positions, columns)
        plt.show()


    def adj(self, adjectives):
        # {adj1:{loc1:count,loc2:count}}
        adjective_count = {}

        locations = []

        for adj in adjectives:
            adjective_count[adj] = {}

        # Walk directory
        for root,dir,files in os.walk("../data/Merged"):
            # get the files for each location
            for file in files:
                location = file.strip(".json")

                locations.append(location)

                for adj in adjectives:
                    adjective_count[adj][location] = 0

                with open(os.path.abspath(root+"/"+file)) as activity_file:
                    activities = json.load(activity_file)
                    for activity in activities:
                        # fix lists
                        tags = list(activity["tags"])
                        if '[' in tags: tags.remove('[')
                        if ']' in tags: tags.remove(']')

                        # add to tot
                        for tag in tags:
                            adjective_count[tag][location] += 1


        plt.title("Adjective tag frequency for each location")
        positions = [i for i in range(len(locations))]
        columns = locations

        width = 0.25

        bars = []
        colors = ["#%06x" % random.randint(0x000000,0xFFFFFF) for i in range(55)]

        previous = [0 for i in range(len(adjectives))]
        c = 0
        for adjective in adjectives:
            yaxis = []
            for i in adjective_count[adjective].values():
                yaxis.append(i)
            bars.append(plt.bar(positions, yaxis, width, edgecolor="black", color=colors[c]))
            previous = [prev+y for prev,y in zip(previous, yaxis)]
            c += 1

        legend_withsums = []
        for adj in adjectives:
            sum = 0
            for i in adjective_count[adj].values():
                sum += i
            legend_withsums.append(adj+":"+str(sum))

        plt.xticks(positions, columns)
        plt.legend(bars, legend_withsums, loc="center left", bbox_to_anchor=(1,0.5), ncol=5)
        plt.show()







def main():
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--adjectivesext", help="adjectives_extended.txt file", required=True)
    args = parser.parse_args()


    # get adjectives
    with open(args.adjectivesext, 'r') as f:
        adjectives_ext = [adj.strip(',') for adj in f.read().split()]

    # vis
    vis = Vis()
    vis.adj(adjectives_ext)
    
main()