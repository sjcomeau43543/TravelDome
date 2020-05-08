'''
Author:        Samantha, Eda
Last modified: 5.7.2020 by sjc
Status:        In progress

This holds an activity and can translate it to a json string
'''

import json
import string
import re

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

    def tag(self, reviews):
        if(reviews):
            with open('adjectives_extended.txt', 'r') as f:
                adjs = [adj.strip(',') for adj in f.read().split()]

                tags = []
                for review in reviews:
                    if review:
                        # lowercase
                        review = review.lower()

                        # remove symbols
                        re.sub(r'[^\w]', ' ', review)

                        # get unique words in a list with no end punctuation
                        words = set([w.strip(string.punctuation) for w in review.split()])

                        # get common words and add to tags
                        tags.extend(list(words & set(adjs))) 

                return tags
        else:
            return []

    def encode(self):
        return {"name":self.name,
                "address":self.address,
                "avg_visitor_review":self.avg_visitor_review,
                "avg_time_spent":self.avg_time_spent,
                "photo_location":self.photo_location,
                "tags":self.tags,
                "link":self.link,
                "source":self.source,
                "reviews":self.reviews}
