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

    parser.add_argument("-l", "--locations", required=True, help="Locations.txt")

    args = parser.parse_args()

    # get expected locations

    # Walk directory
    for root,dir,files in os.walk("../data"):
        if root != "../data":
            for file in files:
                print(file)




main()