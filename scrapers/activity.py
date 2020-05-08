'''
Author:        Samantha, Eda
Last modified: 4.29.2020 by sjc
Status:        In progress

This holds an activity and can translate it to a json string

TODO why empty tag lists?
'''

import json
import string

class Activity:
    # Not sure we need these static members..? - Eda
    # this is so when people are writing scrapers they know what to store and what type / location is should be in
    name = ""
    address = ""
    avg_visitor_review = 0.0
    avg_time_spent = 0 # in minutes
    photo_location = "" # filename in pictures directory
    tags = [] # list of tags from scraping user reviews
    source = ""

    def __init__(self):
        pass

    def __init__(self, name, address, avg_visitor_review, avg_time_spent, photo_location, source, link=None, reviews=[], tags=[], get_tags=False):
        self.name = name
        self.address = address
        self.avg_visitor_review = avg_visitor_review
        self.avg_time_spent = avg_time_spent
        self.photo_location = photo_location
        self.source = source
        self.reviews = reviews
        self.link = link
        self.tags = tags 
        if get_tags:
            self.tags.extend(self.tag(reviews))

    ''' 
    Eda's stuff moved from tag.py
    '''
    def tag(self, reviews):
        if(len(reviews)):
            with open('adjectives_extended.txt', 'r') as f:
                adjs = [adj.strip(',') for adj in f.read().split()]

                tags = []
                for review in reviews:
                    if review:
                        # get unique words in a list with no end punctuation
                        words = set([w.strip(string.punctuation) for w in review.split()])

                        # get common words and add to tags
                        tags.extend(list(words & set(adjs))) 

                #tags = list(filter(None, tags)) # remove empty lists
                return tags

    def encode(self):
        return {"name":self.name,
                "address":self.address,
                "avg_visitor_review":self.avg_visitor_review,
                "avg_time_spent":self.avg_time_spent,
                "photo_location":self.photo_location,
                "tags":self.tags,
                "source":self.source,
                "reviews":self.reviews}
