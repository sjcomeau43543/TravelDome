'''
Author:        Samantha
Last modified: 4.28.2020 by ez
Status:        In progress

This holds an activity and can translate it to a json string

'''

import json

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

    def __init__(self, name, address, avg_visitor_review, avg_time_spent, photo_location, source, reviews=[], tags=[]):
        self.name = name
        self.address = address
        self.avg_visitor_review = avg_visitor_review
        self.avg_time_spent = avg_time_spent
        self.photo_location = photo_location
        self.source = source
        self.reviews = reviews
        self.tags = tags

    def encode(self):
        return {"name":self.name,
                "address":self.address,
                "avg_visitor_review":self.avg_visitor_review,
                "avg_time_spent":self.avg_time_spent,
                "photo_location":self.photo_location,
                "tags":self.tags,
                "source":self.source,
                "reviews":self.reviews}
