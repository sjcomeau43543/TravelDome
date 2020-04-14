import json

class Activity:
    
    name = ""
    address = ""
    avg_visitor_review = 0.0
    avg_time_spent = 0 # in minutes
    photo_location = "" # filename in pictures directory
    tags = [] # list of tags from scraping user reviews
    source = ""

    def __init__(self):
        pass

    def __init__(self, name, address, avg_visitor_review, avg_time_spent, photo_location, source):
        self.name = name
        self.address = address
        self.avg_visitor_review = avg_visitor_review
        self.avg_time_spent = avg_time_spent
        self.photo_location = photo_location
        self.source = source

    # pass in top reviews
    # TODO
    def set_tags(self, reviews):
        for review in reviews:
            pass

    def encode(self):
        return {"name":self.name,
                "address":self.address,
                "avg_visitor_review":self.avg_visitor_review,
                "avg_time_spent":self.avg_time_spent,
                "photo_location":self.photo_location,
                "tags":str(self.tags),
                "source":self.source}